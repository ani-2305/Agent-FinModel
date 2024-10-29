# error_handling.py

import logging

def handle_error(e: Exception) -> str:
    """
    Handles exceptions by logging and returning an error message.

    :param e: The exception to handle.
    :return: A string containing the error message.
    """
    error_message = str(e)
    logging.error(f"Error: {error_message}")
    return error_message

# Configure logging
logging.basicConfig(level=logging.ERROR, filename='agent_errors.log',
                    format='%(asctime)s - %(levelname)s - %(message)s')
