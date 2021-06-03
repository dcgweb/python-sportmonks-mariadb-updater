# Debug disables the logging to be printed on screen, writes all logs to a file
DEBUG = True

# Loggging configuration
LOG_LEVEL = 'WARNING'
LOG_MAX_BYTES = 10000000
LOG_BACKUP_COUNT = 5

APP_LOG_FILENAME = "./logs/app.log"
EP_LOG_FILENAME  = "./logs/endpoint.log"
API_LOG_FILENAME = "./logs/api.log"
DB_LOG_FILENAME = "./logs/db.log"
DATA_LOG_FILENAME = "./logs/data.log"
TWITTER_LOG_FILENAME = "./logs/twitter.log"
ITER_TXT_FILE = "./iter.txt"

BASE_ITERATION  = 50
ITERATION_STEP = 1
LOG_FORMAT = '%(asctime)s:%(name)s:%(levelname)s:%(funcName)s:%(message)s'

DEFAULT_SLEEP_INTERVAL = 30
# Defines timeouts for every api query and etc.
DEFAULT_TIMEOUT = (15, 30)
TWITTER_BLOG_POST_CATEGORY = 3 # this is purely required for my specific configuration, can be overlooked


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

LEAGUE_NAMES_LIST = [
    'Premier League',
    'Eredivisie',
    'Bundesliga',
    'Pro League',
    'Ligue 1',
    'Serie A',
    'Primeira Liga',
    'La Liga',
    'Allsvenskan',
    'Super Lig'
]


SELECTED_LEAGUES = [2,5,8,72,82,208,301,384,462,564,573,600]
ACTIVE_COUNTRIES = [11, 17, 20, 32, 38, 41, 47, 251, 404, 462, 556]
API_MULTI_QUERY_LIMIT = 25

THIS_YEAR_00_TS = 1609459200 # 2021-01-01- 00:00:00