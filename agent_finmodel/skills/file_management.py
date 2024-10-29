# file_management.py

import os
import shutil
from .error_handling import handle_error

def validate_file_path(file_path: str) -> bool:
    """
    Validates whether the file path exists.

    :param file_path: The path to the file.
    :return: True if the file exists, False otherwise.
    """
    return os.path.exists(file_path)

def save_file(data: bytes, output_path: str) -> bool:
    """
    Saves data to the specified file path.

    :param data: The data to save.
    :param output_path: The path to save the file.
    :return: True if successful, False otherwise.
    """
    try:
        with open(output_path, 'wb') as file:
            file.write(data)
        return True
    except Exception as e:
        handle_error(e)
        return False

def backup_file(file_path: str) -> bool:
    """
    Creates a backup of the specified file.

    :param file_path: The path to the file to backup.
    :return: True if successful, False otherwise.
    """
    try:
        if not os.path.exists(file_path):
            return False
        backup_path = file_path + '.bak'
        shutil.copyfile(file_path, backup_path)
        return True
    except Exception as e:
        handle_error(e)
        return False
