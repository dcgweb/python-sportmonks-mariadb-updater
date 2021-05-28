# Debug disables the logging to be printed on screen, writes all logs to a file
DEBUG = True

# Loggging configuration
LOG_LEVEL = 'INFO'
LOG_MAX_BYTES = 1000000
LOG_BACKUP_COUNT = 5

APP_LOG_FILENAME = "./logs/app.log"
EP_LOG_FILENAME  = "./logs/endpoint.log"
API_LOG_FILENAME = "./logs/api.log"
DB_LOG_FILENAME = "./logs/db.log"
DATA_LOG_FILENAME = "./logs/data.log"

LOG_FORMAT = '%(asctime)s:%(name)s:%(levelname)s:%(funcName)s:%(message)s'


# Defines timeouts for every api query and etc.
DEFAULT_TIMEOUT = (15, 30)



SECOND_API_URL = "https://www.thesportsdb.com/api/v1/json/"
TWITTER_API_URL = ""

API_URL = 'https://soccer.sportmonks.com/api/v2.0/'  # URL for API endpoint

ACCOUNT_LIST = [
    'premierleague',
    'ChampionsLeague',
    'EuropaLeague',
    'eredivisie',
    'Bundesliga_EN',
    'TFF_Org',
    'seriea',
    'LaLigaEN',
    'Ligue1_ENG',
    'ligaportugal',
    'ProLeagueBE',
    'allsvenskanuk'
]


SELECTED_LEAGUES = [2,5,8,72,82,208,301,384,462,564,573,600]

API_MULTI_QUERY_LIMIT = 25
HARD_LIST_ACTIVE_SEASONS = [17299, 17367, 17420, 17426, 17228, 17361, 17138, 17160, 17488, 17463, 17480, 16838, 17449]    # I am sick and tired of duplicate PRIMARY key integrity errors. So, here we go aq!

THIS_YEAR_00_TS = 1609459200 # 2021-01-01- 00:00:00