import tweepy, db, constants, helper, secrets, logging
from logging.handlers import RotatingFileHandler
import data as formatter

class Twitter:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, str(constants.LOG_LEVEL)))
        self.file_handler = RotatingFileHandler(constants.TWITTER_LOG_FILENAME, maxBytes=constants.LOG_MAX_BYTES, backupCount=constants.LOG_BACKUP_COUNT)
        self.file_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
        self.logger.addHandler(self.file_handler)
        self.consumer_key = secrets.CONSUMER_KEY
        self.consumer_secret = secrets.CONSUMER_SECRET
        self.access_token = secrets.ACCESS_TOKEN
        self.access_token_secret = secrets.ACCESS_TOKEN_SECRET
        self.conn = self.__auth()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.logger.error(f'Suppressing exception: {exc_type}')
            self.logger.error(f'Traceback: {exc_tb}')
        return True

    def __auth(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        return tweepy.API(auth)


    def query(self, account, c = 1):
        if(self.conn):
            return self.conn.user_timeline(
                screen_name=str(account), # Account to be queried
                count=int(c), # 2 is the maximum allowed count
                include_rts = False, # Including retweets in the response will only increase overall transferred bytes.
                tweet_mode = 'extended' # Necessary to keep full_text otherwise only the first 140 words are extracted
            )
        else:
            self.logger.warning('Twitter connection was not authorized!')
            return False

    def retweet(self, tweet_id):
        if(self.conn):
            return self.conn.retweet(tweet_id)
        else:
            self.logger.warning('Twitter connection was not authorized!')
            return False

    def __check_db_for_(self, record_id):
        with db.Db() as database:
            s = database.session(database.engine)
            with s.begin() as sess:
                # Get all tweets from local db
                return True if database.get_one_filter(sess, 'news', 'id', record_id) else False

    def run(self):
        for account in constants.ACCOUNT_LIST:
            tweet = self.query(str(account))

            if(self.__check_db_for_(tweet[0].id)): continue

            # Insert tweet into db
            with formatter.Data() as f_d:
                formatted_data = f_d.reshape(tweet, 'twitter')
                with db.Db() as database:
                    database.insert_or_update('news', formatted_data)

            # Retweet
            self.logger.info(self.conn.retweet(tweet[0].id))

Twitter().run()