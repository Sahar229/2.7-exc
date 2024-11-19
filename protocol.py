#   Ex. 2.7 template - protocol

import cmd_funcs

LENGTH_FIELD_SIZE = 10
PORT = 8820

def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE c:\work\file.txt is good, but DELETE alone is not

        Args:
            data (string): the command that was given by the client

        Returns:
                boolean if the command is valid according to the protocol

    """
    command = data.split(' ', 1)[0]
    if command in cmd_funcs.CMD_PARAMS:
        return cmd_funcs.CMD_PARAMS[command] == data.count(' ')
    return False


def create_msg(data):
    """
    Create a valid protocol message, with length field

        Args:
            data (string): the string one socket is sending to the other

        Returns:
                the message suited according to the protocol
    """
    length = str(len(str(data)))
    header = length.zfill(LENGTH_FIELD_SIZE)
    message = header + str(data)
    return message.encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"

        Args:
            my_socket (socket): the socket who's receiving the message

        Returns:
                the message extracted from the protocol
    """
    length = (my_socket.recv(LENGTH_FIELD_SIZE)).decode()
    if length.isdigit():
        data = my_socket.recv(int(length)).decode()
        return True, data
    return False, "Error"



