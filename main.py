import db, endpoint, time, helper, logging, constants
from logging.handlers import RotatingFileHandler
from datetime import datetime
from phpserialize import serialize

class App:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, str(constants.LOG_LEVEL)))
        self.file_handler = RotatingFileHandler(constants.APP_LOG_FILENAME, maxBytes=constants.LOG_MAX_BYTES, backupCount=constants.LOG_BACKUP_COUNT)
        self.file_handler.setFormatter(logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(funcName)s:%(message)s'))
        self.logger.addHandler(self.file_handler)

    def livescores(self):
        start = time.time()
        tbi = []
        #init endpoint class with context manager
        with endpoint.Endpoint() as ep:
            ep.query('livescores', ["goals", "cards", "stats", "tvstations", "comments"])

            # If there are no records returned from API
            if(len(ep.data) == 0):
                logging.warning('Api query returned 0 results')
                return False

            for api_fixture in ep.data:
                tbi.append(
                    {
                        'id': api_fixture['id'],
                        'league_id': api_fixture['league_id'],
                        'season_id': api_fixture['season_id'],
                        'stage_id': api_fixture['stage_id'],
                        'round_id': api_fixture['round_id'],
                        'group_id': api_fixture['group_id'],
                        'aggregate_id': api_fixture['aggregate_id'],
                        'venue_id': api_fixture['venue_id'],
                        'referee_id': api_fixture['referee_id'],
                        'localteam_id': api_fixture['localteam_id'],
                        'visitorteam_id': api_fixture['visitorteam_id'],
                        'winner_team_id': api_fixture['winner_team_id'],
                        'weather_report': serialize(api_fixture['weather_report']) if api_fixture['weather_report']!=None else None,
                        'attendance': api_fixture['attendance'],
                        'details': api_fixture['details'],
                        'formations': serialize(api_fixture['formations']) if api_fixture['formations']!=None else None,
                        'scores': serialize(api_fixture['scores']) if api_fixture['scores']!=None else None,
                        'status': api_fixture['time']['status'],
                        'date_time': api_fixture['time']['starting_at']['date_time'],
                        'time': api_fixture['time']['starting_at']['time'],
                        'timestamp': api_fixture['time']['starting_at']['timestamp'],
                        'minute': api_fixture['time']['minute'] if 'minute' in api_fixture['time'] else None,
                        'second': api_fixture['time']['second'] if 'second' in api_fixture['time'] else None,
                        'coaches': serialize(api_fixture['coaches']) if api_fixture['coaches']!=None else None,
                        'standings': serialize(api_fixture['standings']) if api_fixture['standings']!=None else None,
                        'assistants': serialize(api_fixture['assistants']) if api_fixture['assistants']!=None else None,
                        'colors': serialize(api_fixture['colors']) if api_fixture['colors']!=None else None,
                        'goals': serialize(api_fixture['goals']) if api_fixture['goals']!=None else None,
                        'cards': serialize(api_fixture['cards']) if api_fixture['cards']!=None else None,
                        'stats': serialize(api_fixture['stats']) if api_fixture['stats']!=None else None,
                        'tvstations': serialize(api_fixture['tvstations']) if api_fixture['tvstations']!=None else None,
                        'comments': serialize(api_fixture['comments']) if api_fixture['comments']!=None else None,
                        'updated_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                    }
                )

            with db.Db() as database:
                affected_rows = database.insert_or_update('fixtures', tbi)
                helper.db_summary(affected_rows)
        logging.info(f"Took {str(round(time.time() - start,3))} seconds")


if __name__ == "__main__":
    gololdu = App()
    gololdu.livescores()