import requests, constants, json, secrets, logging
from logging.handlers import RotatingFileHandler

class Api:
    def __enter__(self):
        return self

    def __init__(self):
        self.error = None
        self.query_amt = 0
        self.latest_query = None
        # self.logger = logging.getLogger(__name__)
        # self.logger.setLevel(getattr(logging, str(constants.LOG_LEVEL)))
        # self.file_handler = RotatingFileHandler(constants.API_LOG_FILENAME, maxBytes=constants.LOG_MAX_BYTES, backupCount=constants.LOG_BACKUP_COUNT)
        # self.file_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
        # self.logger.addHandler(self.file_handler)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            pass
        #     self.logger.error(f'Suppressing exception: {exc_type}')
        #     self.logger.error(f'Traceback: {exc_tb}')
        # self.logger.removeHandler(self.file_handler)
        return True
