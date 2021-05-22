from api import Api
from logging.handlers import RotatingFileHandler
import requests, json, secrets, constants, logging

class Endpoint(Api):

    def __enter__(self):
        return self

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, str(constants.LOG_LEVEL)))
        self.file_handler = RotatingFileHandler(constants.EP_LOG_FILENAME, maxBytes=constants.LOG_MAX_BYTES, backupCount=constants.LOG_BACKUP_COUNT)
        self.file_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
        self.logger.addHandler(self.file_handler)

    def query(self, action, includes = []):
        self.data = []
        self.action = action
        self.includes = includes
        self.latest_query = self.action
        with requests.Session() as r:
            try:
                response = r.get(constants.API_URL + self.action, params=[('api_token', secrets.API_KEY),('page', "1"),('include', ",".join(self.includes))], timeout=constants.DEFAULT_TIMEOUT)
                self.query_amt += 1
            except Exception as e:
                self.logger.error(f"API query : {self.latest_query} failed with {e}")
                self.error = e
                return False
            else:
                self.logger.debug(f"Response = {str(r)}")
                raw_data = json.loads(response.text)

                # find last page if there's pagination in the result
                last_page = self.get_total_pages(raw_data)

                # paginate if last_page is bigger than 1
                if(int(last_page) > 1):
                    # return paginated result ( merged list of dictionaries )
                    self.paginator(raw_data, last_page)
                else:
                    if(isinstance(raw_data, dict) == False):
                        return False
                    if('data' not in raw_data):
                        return False



                self.data = raw_data['data']



    def __exit__(self, exc_type, exc_val, exc_tb):
        self.data = []
        self.action = None
        self.includes = []
        self.latest_query = None
        self.logger.debug(f"Total Queries : {self.query_amt}")