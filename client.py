#   Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020


import socket

import protocol


IP = '127.0.0.1'
PORT = 8821
SAVED_PHOTO_LOCATION = r"C:\Users\User\Pictures\result.jpeg"


def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive

        Args:
            my_socket (socket): the client socket
            cmd (string): the command that was given to the server

        Returns:
                the appropriate response the server returned
    """

    if cmd != 'SEND_PHOTO':
        valid_protocol, server_response = protocol.get_msg(my_socket)
        print(server_response)
    else:
        length_of_file = int(my_socket.recv(10).decode())
        length_of_picture = int(my_socket.recv(int(length_of_file)).decode())
        f = open(SAVED_PHOTO_LOCATION, 'wb')
        picture = my_socket.recv(length_of_picture)
        f.write(picture)
        f.close()


def main():
    # open socket with the server
    try:
        my_socket = socket.socket()
        my_socket.connect((IP, PORT))

        # print instructions
        print('Welcome to remote computer application. Available commands are:\n')
        print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit

        while True:
            cmd = input("Please enter command:\n").upper()
            if protocol.check_cmd(cmd):
                packet = protocol.create_msg(cmd)
                my_socket.send(packet)
                if cmd == 'EXIT':
                    break
                handle_server_response(my_socket, cmd)
            else:
                print("Not a valid command, or missing parameters\n")
    except KeyboardInterrupt:
        print("Server was closed!")
    except ConnectionResetError:
        print("Server was closed!")
    except ConnectionRefusedError:
        print("Open the server first!")
    my_socket.close()


if __name__ == '__main__':
    main()
