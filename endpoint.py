from api import Api
from logging.handlers import RotatingFileHandler
import db, requests, json, secrets, constants, logging

class Endpoint(Api):

    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, str(constants.LOG_LEVEL)))
        self.file_handler = RotatingFileHandler(constants.EP_LOG_FILENAME, maxBytes=constants.LOG_MAX_BYTES, backupCount=constants.LOG_BACKUP_COUNT)
        self.file_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
        self.logger.addHandler(self.file_handler)
        self.data = []
        self.injection = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.data = []
        self.includes = []
        self.action = None
        self.latest_query = None
        if exc_val:
            self.logger.error(f'Suppressing exception: {exc_type}')
            self.logger.error(f'Traceback: {exc_tb}')
        else:
            self.logger.info(f"Total Queries : {self.query_amt}")
            print(f"Total Queries : {self.query_amt}")
        self.logger.removeHandler(self.file_handler)
        return True


    def get_total_pages(self, data):
        try:
            total_pages = data['meta']['pagination']['total_pages']
        except:
            # self.logger.warning(f"Total pages count could not be determined, presuming it to be 1")
            return 1
        else:
            self.logger.info(f"{str(total_pages)} in total")
            return total_pages

    def paginator(self, last_page = None):
        if(last_page == None):
            return False

        for page in range(2, int(last_page) + 1):
            print(f'Paginating on {self.action}:{self.includes}:P{page}')
            self.query(self.action, self.includes, page)

    def query(self, action, includes = [], page = 1):
        self.action = self.latest_query = action
        self.includes = includes

        with requests.Session() as r:
            try:
                response = r.get(constants.API_URL + self.action, params=[('api_token', secrets.API_KEY), ('page', str(page)), ('per_page', str(150)), ('include', ",".join(self.includes))], timeout=constants.DEFAULT_TIMEOUT)
                self.query_amt += 1
            except Exception as e:
                self.logger.error(f"API query : {self.latest_query} failed with {e}")
                self.error = e
                return False
            else:
                self.logger.debug(f"Response = {str(r)}")
                raw_data = json.loads(response.text)

                # Check if it's already being paginated
                if(page == 1):
                    # find last page if there's pagination in the result
                    last_page = self.get_total_pages(raw_data)

                    # paginate if last_page is bigger than 1
                    if(int(last_page) > 1):
                        # paginate the result ( with extra api queries )
                        self.paginator(last_page)

            if(isinstance(raw_data, dict) == False):
                return False
            if('data' not in raw_data):
                return False
            if(len(raw_data['data']) == 0):
                return False

            self.data.extend(raw_data['data'])
