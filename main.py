import db, api
class App:
    def __init__(self):
        #init db etc
        with db.Db() as d:
            print('doing stuff with database')

        #init api class
        with api.Api() as sm:
            print('pulling stuff from api')

if __name__ == "__main__":
    App()