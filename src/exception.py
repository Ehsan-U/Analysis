#Any exception that the code has is automatically 
#sent to sys libary

import sys
from src.logger import logging


def error_message_detail(error, error_detail:sys):
    """
    The last information gives us on which file and the line number
    the exception has occurred
    """
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message: error message[{2}]".format(
                    file_name, 
                    exc_tb.tb_lineno, 
                    str(error)
    )
    return error_message

class CustomException(Exception):
    
    def __init__(self, error_message, error_detail:sys):
        super().__init__(self, error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self):
        return self.error_message

if __name__ == "__main__":
    try:
        a = 1/0
    except Exception as e:
        logging.info("Logging works")
        raise CustomException(e, sys)
