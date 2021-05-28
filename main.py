import data as formatter
from logging.handlers import RotatingFileHandler
import db, endpoint, helper, logging, constants


class App:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, str(constants.LOG_LEVEL)))
        self.file_handler = RotatingFileHandler(constants.APP_LOG_FILENAME, maxBytes=constants.LOG_MAX_BYTES, backupCount=constants.LOG_BACKUP_COUNT)
        self.file_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
        self.logger.addHandler(self.file_handler)
        self.current_ep = None
        self.current_db_tbl = None

    def insert(self, unformatted_data = None):
        if(unformatted_data == None):
            self.logger.info("API response is empty")
            return False

        with formatter.Data() as f_d:
            f_d.reshape(unformatted_data, self.current_ep)
            with db.Db() as database:
                try:
                    helper.db_summary(database.insert_or_update(self.current_db_tbl, f_d.reshaped_data), self.current_ep, self.current_db_tbl)
                except Exception as e:
                    self.logger.error(e)
                    return False
                else:
                    self.logger.info(f"{getattr(self, 'current_ep')} -> {getattr(self, 'current_db_tbl')}")
                    return True

    def extra_insert(self, unformatted_data = None, ep = None, db_tbl = None):
        # This part is hacky but I cannot think of
        # a better way to update more than one tables
        # with one api query since livescores query result
        # also should contain lineups data. So here we go!

        # Update current objects props
        self.current_ep = ep
        self.current_db_tbl = db_tbl

        # With these object props changed, it will
        # now insert the extra data into other db tables
        self.insert(unformatted_data)

    def run(self, api_endpoint = None, api_includes = [], db_tbl = None):
        if(api_endpoint == None or db_tbl == None):
            return False

        # Set initializing values of the app object
        self.current_ep = api_endpoint
        self.current_db_tbl = db_tbl
        with endpoint.Endpoint() as ep:
            ep.query(self.current_ep, api_includes)
            if not ep.error == None:
                return False

            self.insert(ep.data)
            if(api_endpoint == 'livescores'):
                self.extra_insert(ep.data, 'lineups', 'lineups')


if __name__ == "__main__":
    gololdu = App()
    gololdu.run('livescores', ["goals", "cards", "stats", "tvstations", "comments", "lineup"], 'fixtures')
    #gololdu.run('countries', [], 'countries')
