import helper, mariadb, secrets
from termcolor import colored
from mariadb import Error

class Db:
    def __init__(self):
        self.user = secrets.MDB_USERNAME
        self.password = secrets.MDB_PASSWORD
        self.host = secrets.MDB_ADDRESS
        self.port = secrets.MDB_SRVPORT
        self.database = secrets.MDB_DATABASE
        self.conn = None
        self.cursor = None
        self.e = None
        self.last_query = None

    def __enter__(self):
        try:
            self.conn = mariadb.connect(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database
            )
        except Exception as e:
            helper.write_log(e)
            return False
        finally:
            # returns mariadb cursor
            self.cursor = self.conn.cursor(dictionary=True)
            print('Successfully connected to database')
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # close db connection
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            helper.write_log(e)
        finally:
            print('Disconnected from database')
            return self

    def query(self, query):
        try:
            self.last_query = query
            # Returns the cursor object
            self.cursor.execute(self.last_query)
        except Exception as e:
            helper.write_log(e)
            return False
        else:
            return self.cursor
