import data as formatter
from logging.handlers import RotatingFileHandler
import db, endpoint, time, helper, logging, constants


class App:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, str(constants.LOG_LEVEL)))
        self.file_handler = RotatingFileHandler(constants.APP_LOG_FILENAME, maxBytes=constants.LOG_MAX_BYTES, backupCount=constants.LOG_BACKUP_COUNT)
        self.file_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
        self.logger.addHandler(self.file_handler)

    def go(self, api_endpoint = None, api_includes = []):
        if(api_endpoint == None):
            self.logger.warning(f"api_endpoint parameter must not be empty")
            return False
        start = time.time()
        self.api_endpoint = api_endpoint
        self.api_includes = api_includes
        #init endpoint class with context manager
        with endpoint.Endpoint() as ep:
            ep.query(self.api_endpoint, self.api_includes)
            # If there are no records returned from API
            if(len(ep.data) == 0):
                logging.warning('Api query returned 0 results')
                return False

            with formatter.Data() as f_d:
                f_d.reshape(ep.data, self.api_endpoint)
                with db.Db() as database:
                    affected_rows = database.insert_or_update('fixtures', f_d.reshaped_data)
                    helper.db_summary(affected_rows)

        logging.info(f"Took {str(round(time.time() - start,3))} seconds")


if __name__ == "__main__":
    gololdu = App()
    gololdu.go('livescores', ["goals", "cards", "stats", "tvstations", "comments"])