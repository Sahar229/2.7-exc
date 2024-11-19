import glob
import os
import shutil
import subprocess
import pyautogui

PHOTO_PATH = r"C:\Users\User\Pictures\screen.jpeg"


def dir_(params):
    """
        showing all the files in a directory

        Args:
            params (list): the directory

        Returns:
            files_string (string): the files
    """
    path = params[0]
    files = glob.glob(path + r'\\*')
    files_string = ", ".join(str(x) for x in files)
    return files_string


def delete_(params):
    """
        deleting file

        Args:
            params (list): the path of the file

        Returns:
            confirmation message
    """
    try:
        path = params[0]
        os.remove(path)
        return "Deleted Successfully"
    except FileNotFoundError:
        return "Invalid Path!"


def copy_(params):
    """
        copying file to another place

        Args:
            params (list): list of the file and the destination place


        Returns:
            confirmation message
    """
    try:
        file = params[0]
        path = params[1]
        shutil.copy(file, path)
        return f"Copied Successfully"
    except FileNotFoundError:
        return "Invalid Path!"


def execute_(params):
    """
        executing a program

        Args:
            params (list): the path of the program

        Returns:
            confirmation message
    """
    try:
        path = params[0]
        subprocess.call(path)
        return f"Executed Successfully"
    except FileNotFoundError:
        return "Invalid Path!"


def take_screenshot_():
    """
        taking a screenshot

        Returns:
            confirmation message
    """
    try:
        image = pyautogui.screenshot()
        image.save(PHOTO_PATH)
        return f"Screenshot Taken Successfully"
    except FileNotFoundError:
        return "Invalid Path!"


CMD_FUNCS = {'DIR': dir_, 'DELETE': delete_, 'COPY': copy_, 'EXECUTE': execute_, 'TAKE_SCREENSHOT': take_screenshot_}
CMD_PARAMS = {'DIR': 1, 'DELETE': 1, 'COPY': 2, 'EXECUTE': 1, 'TAKE_SCREENSHOT': 0, 'SEND_PHOTO': 0, 'EXIT': 0}
