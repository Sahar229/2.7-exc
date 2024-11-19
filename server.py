#   Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020

import socket
import os

import protocol
import cmd_funcs

try:
    IP = '127.0.0.1'
    PORT = 8821
    PHOTO_PATH = r"C:\Users\User\Pictures\screen.jpeg"


    def check_client_request(cmd):  # done
        """
        Break cmd to command and parameters
        Check if the command and params are good.

        For example, the filename to be copied actually exists

        Returns:
            valid: True/False
            command: The requested cmd (ex. "DIR")
            params of the cmd params (ex. ["c:\\cyber"])
        """
        # Use protocol.check_cmd first

        # Then make sure the params are valid
        valid = protocol.check_cmd(cmd)
        list = cmd.split(' ')
        for x in list[1:]:
            if not os.path.exists(x):
                valid = False
        return valid, list[0], list[1:]


    def handle_client_request(command, params):
        """Create the response to the client, given the command is legal and params are OK

        For example, return the list of filenames in a directory
        Note: in case of SEND_PHOTO, only the length of the file will be sent
        Args:
            command (string): the command to do
            params (list): the appropriate parameters for the command function

        Returns:
            response: the requested data

        """
        if command != "TAKE_SCREENSHOT":
            response = cmd_funcs.CMD_FUNCS[command](params)
        else:
            response = cmd_funcs.CMD_FUNCS[command]()
        return response


    def main():
        try:
            # open socket with client
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((IP, PORT))
            server_socket.listen(1)
            print(f'server is up at {IP}:{PORT}')
        except socket.error:
            print(f"Socket error")
            # Handle the error appropriately

        try:
            # connecting with client
            client_socket, client_address = server_socket.accept()
        except socket.error:
            print(f"Accept error:")
            # Handle the error appropriately
        print(f'server has connected successfully {client_address}')

        # handle requests until user asks to exit
        try:
            while True:
                # Check if protocol is OK, e.g. length field OK
                valid_protocol, cmd = protocol.get_msg(client_socket)
                if valid_protocol:
                    # Check if params are good, e.g. correct number of params, file name exists
                    valid_cmd, command, params = check_client_request(cmd)
                    if valid_cmd:
                        if command == 'SEND_PHOTO':
                            with open(PHOTO_PATH, "rb") as image_file:
                                image_data = image_file.read()
                                image_length = len(image_data)
                                image_length_length = str(len(str(image_length))).zfill(10)

                                client_socket.send(image_length_length.encode())
                                client_socket.send(str(image_length).encode())
                                client_socket.send(image_data)
                                print("Sent photo successfully!")

                        elif command == 'EXIT':
                            break

                        else:
                            message = handle_client_request(command, params)
                            message = protocol.create_msg(message)
                            client_socket.send(message)

                    else:
                        # prepare proper error to client
                        message = 'Bad command or parameters'
                        message = protocol.create_msg(message)
                        client_socket.send(message)
                        # send to client

                else:
                    # prepare proper error to client
                    message = 'Packet not according to protocol'
                    message = protocol.create_msg(message)
                    client_socket.send(message)

                    # Attempt to clean garbage from socket
                    client_socket.recv(1024)
        except ConnectionAbortedError:
            print("Client was closed!")

        # close sockets
        print("Closing connection")
        client_socket.close()
        server_socket.close()
except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    main()
