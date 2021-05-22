import requests, constants, json, secrets, logging
from logging.handlers import RotatingFileHandler

class Api:
    def __enter__(self):
        return self

    def __init__(self):
        self.error = None
        self.query_amt = 0
        self.latest_query = None
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, str(constants.LOG_LEVEL)))
        self.file_handler = RotatingFileHandler(constants.API_LOG_FILENAME, maxBytes=constants.LOG_MAX_BYTES, backupCount=constants.LOG_BACKUP_COUNT)
        self.file_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
        self.logger.addHandler(self.file_handler)

    def get_total_pages(self, data):
        try:
            total_pages = data['meta']['pagination']['total_pages']
        except:
            self.logger.warning(f"Total pages count could not be determined, presuming it to be 1")
            total_pages = 1
        finally:
            self.logger.debug(f"{str(total_pages)} in total")
            return total_pages

    def paginator(self, data, last_page):
        merged_data = []
        data_list = [].append(data)
        for page in range(2, int(last_page) + 1):
            with requests.Session() as r:
                try:
                    response = r.get(secrets.API_URL + self.action, params=[('api_token', secrets.API_KEY), ('page', str(page))], timeout=constants.DEFAULT_TIMEOUT)
                    self.query_amt += 1
                except Exception as e:
                    self.logger.error(f"Latest API query of : {str(self.latest_query)} failed with {str(e)}")
                    self.error = e
                    return False
                else:
                    data_list.append(json.loads(response.text))
            for f_data in data_list:
                for c_data in f_data['data']:
                    merged_data.append(c_data)
            self.data = merged_data
            return True

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logger.debug(f"Total Queries : {self.query_amt}")
        if(self.error):
            self.logger.error(f"Errors : {self.error}")