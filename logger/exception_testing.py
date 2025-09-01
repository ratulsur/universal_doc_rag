import sys
import traceback
from custom_logger import CustomLogger  
logger = CustomLogger().get_logger(__file__)  

class DocumentPortalException(Exception):
    def __init__(self, error_message, error_details):
        _, _, exc_tb = error_details.exc_info()
        self.file_name = exc_tb.tb_frame.f_code.co_filename
        self.lineno = exc_tb.tb_lineno
        self.error_message = str(error_message)
        self.traceback_str = ''.join(traceback.format_exception(*error_details.exc_info()))

    def __str__(self):
        return f"""
        Error in [{self.file_name}] at line [{self.lineno}]
        Message: {self.error_message}
        Traceback:
        {self.traceback_str}
        """

if __name__ == "__main__":
    try:
        a = 1 / 0  # deliberate error
    except Exception as e:
        logger.exception("Original exception:")  # Logs traceback
        app_exc = DocumentPortalException(e, sys)
        logger.error(str(app_exc))               # Logs custom-formatted message
        raise app_exc
