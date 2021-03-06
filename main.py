#!/usr/bin/python3.6
from time import sleep
import data as formatter
from datetime import datetime
from logging.handlers import RotatingFileHandler
import db, endpoint, helper, logging, constants, twitter, iterator



class App:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, str(constants.LOG_LEVEL)))
        self.file_handler = RotatingFileHandler(constants.APP_LOG_FILENAME, maxBytes=constants.LOG_MAX_BYTES, backupCount=constants.LOG_BACKUP_COUNT)
        self.file_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
        self.logger.addHandler(self.file_handler)
        self.current_ep = None
        self.current_db_tbl = None
        self.iterator = iterator.Iterator()

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

            if(api_endpoint == 'teams'):
                for country_id in constants.ACTIVE_COUNTRIES:

                    temp_ep = f"countries/{country_id}/teams"
                    # https://soccer.sportmonks.com/api/v2.0/countries/{ID}/teams
                    ep.query(temp_ep, api_includes)

                    if(ep.error != None or len(ep.data) == 0): continue

                    self.insert(ep.data)
                    ep.data = []

            if(api_endpoint == "players"):
                # https://soccer.sportmonks.com/api/v2.0/squad/season/{season_ID}/team/{team_ID}
                with db.Db() as d:
                    s = d.session(d.engine)
                    with s.begin() as sess:
                        for country_id in constants.ACTIVE_COUNTRIES:
                            if(country_id == 41): continue

                            leagues = d.get_all_filter(sess, 'leagues', 'country_id', country_id)

                            for league_obj in leagues:
                                league = league_obj.__dict__
                                if(league['name'] not in constants.LEAGUE_NAMES_LIST): continue

                                teams = d.get_all_filter(sess, 'teams', 'current_season_id', league['current_season_id'])

                                for team_obj in teams:
                                    team = team_obj.__dict__
                                    temp_ep = f"squad/season/{league['current_season_id']}/team/{team['id']}"
                                    self.logger.info(f"Working on {league['name']} - {team['name']} players")
                                    ep.query(temp_ep, api_includes)

                                    if(ep.error != None or len(ep.data) == 0): continue

                                    self.insert(ep.data)
                                    ep.data = []

            if(api_endpoint == "standings"):
                # Endpoint:	https://soccer.sportmonks.com/api/v2.0/standings/season/__ID__
                with db.Db() as d:
                    s = d.session(d.engine)
                    with s.begin() as sess:
                        for country_id in constants.ACTIVE_COUNTRIES:
                            if(country_id == 41): continue

                            leagues = d.get_all_filter(sess, 'leagues', 'country_id', country_id)

                            for league_obj in leagues:
                                league = league_obj.__dict__
                                if(league['name'] not in constants.LEAGUE_NAMES_LIST): continue


                                temp_ep = f"standings/season/{league['current_season_id']}"
                                self.logger.info(f"Working on {league['name']} standings")
                                ep.query(temp_ep, api_includes)

                                if(ep.error != None or len(ep.data) == 0): continue

                                self.insert(ep.data)
                                ep.data = []

            else:
                ep.query(self.current_ep, api_includes)

                if(ep.error != None): return False

                self.insert(ep.data)
                if(api_endpoint == 'livescores'):
                    self.extra_insert(ep.data, 'lineups', 'lineups')
        sleep(constants.DEFAULT_SLEEP_INTERVAL)
        # Heartbeat
        self.heartbeat()

    def heartbeat(self):
        self.current_ep = self.current_db_tbl = 'heartbeat'
        self.insert([{'heartbeat'}])

if __name__ == "__main__":
    app = App()
    while True:
        # every 6 days
        if(int(app.iterator.get_iterator()) % 2882 == 0):
            app.run('players', ["player"], 'players')
            app.run('countries', [], 'countries')
        # every 24 hours
        if(int(app.iterator.get_iterator()) % 480 == 0):
            app.logger.info('24 hours mark')
            app.run('teams', ["stats"], 'teams')
            app.run('leagues', [], 'leagues')
        # every 25 minutes
        if(int(app.iterator.get_iterator()) % 50 == 0):
            app.logger.info('25 minutes mark')
            twitter.Twitter().run()
            app.run('seasons', [], 'seasons')
            app.run('standings', ["standings.team"], 'standings')
        app.run('livescores', ["goals", "cards", "stats", "tvstations", "comments", "lineup"], 'fixtures')
        app.iterator.set_iterator(app.iterator.get_iterator() + constants.ITERATION_STEP)
