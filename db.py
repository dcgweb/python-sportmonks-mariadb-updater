from sqlalchemy.orm import sessionmaker
import helper, secrets, constants, logging
from logging.handlers import RotatingFileHandler
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import INTEGER, MEDIUMBLOB, TEXT, TINYINT, VARCHAR, BIGINT, MEDIUMTEXT, LONGTEXT
from sqlalchemy import Column, LargeBinary, TIMESTAMP, create_engine, inspect, text, select, func

class Db:
    def __init__(self):
        self.engine = create_engine(f"mysql+pymysql://{secrets.MDB_USERNAME}:{secrets.MDB_PASSWORD}@{secrets.MDB_ADDRESS}/{secrets.MDB_DATABASE}", echo=False)
        self.inspect = inspect(self.engine) if constants.DEBUG else None
        self.session = sessionmaker
        self.select = select
        self.func = func
        self.text = text
        self.mapper = {'api_queries': ApiQuery, 'countries': Country, 'fixtures': Fixture, 'heartbeat': Heartbeat, 'leagues': League, 'lineups': Lineup, 'players': Player, 'seasons': Season, 'standings': Standing, 'teams': Team, 'venues': Venue, 'news': News}
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, str(constants.LOG_LEVEL)))
        self.file_handler = RotatingFileHandler(constants.DB_LOG_FILENAME, maxBytes=constants.LOG_MAX_BYTES, backupCount=constants.LOG_BACKUP_COUNT)
        self.file_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
        self.logger.addHandler(self.file_handler)

    def __enter__(self):
        self.logger.info('DB Class created successfully')
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.logger.error(f'Suppressing exception: {exc_type}')
            self.logger.error(f'Traceback: {exc_tb}')
        return True

    def insert_or_update(self, table = None, datas = []):
        """ Inserts and/or updates multiple data into
        it's respective tables using SQLAlchemy

        Args:
            table (string, required): The table to insert/update in. Defaults to None
            datas (list, required): List of dictionaries to be inserted/updated. Defaults to []

        Returns:
            tuple: Counts of records that were affected
        """
        if(table == None or len(datas)==0):
            self.logger.warning('Table and/or data values must not be empty.')
            self.logger.warning(f'Received Table = {str(table)} and data = {str(datas)}')
            return False

        separated_list = self.__separate_insert_update(self.mapper[table], datas)

        Session = self.session(self.engine)

        # If tbi is not empty, then there's something to insert
        if(len(separated_list['tbi']) != 0):
            # Begin Session with Context Manager
            with Session.begin() as session:
                to_be_inserted = []
                for tbi in separated_list['tbi']:
                    to_be_inserted.append(
                        self.mapper[table](**tbi)
                    )
                session.add_all(to_be_inserted)

        # If tbu is empty, then there's nothing to update
        if(len(separated_list['tbu']) != 0):
            with Session.begin() as session:
                for tbu in separated_list['tbu']:
                    # Update dictionaries we do not use
                    # or require and id column will be
                    # omitted for each element
                    id_omitted_tbu = helper.remove_key(tbu, 'id')
                    session.query(self.mapper[table]).filter(self.mapper[table].id == tbu['id']).update(id_omitted_tbu, synchronize_session = False)
        return (len(separated_list['tbi']), len(separated_list['tbu']))

    def __separate_insert_update(self, table, raw_data = []):
        separated_list = {'tbi': [], 'tbu': []}

        if(len(raw_data) == 0):
            self.logger.warning(f"Raw data count was {len(raw_data)}")
            return separated_list

        # Get only id's from raw_data list
        # Returns a list of id's by default
        # Default behaviour can be changed
        # with a "True" 3rd parameter for a
        # comma separated string return.
        all_raw_ids = helper.get_keys_from_dict(raw_data)

        if(len(all_raw_ids) == 0):
            self.logger.warning(f"all_raw_ids were {str(len(all_raw_ids))}")
            return separated_list
        if(all_raw_ids == False):
            self.logger.warning(f"all_raw_ids were {str(all_raw_ids)}")
            return separated_list

        # Query database with where_in to find
        # all records with
        with self.session(self.engine).begin() as session:
            criteria = table.id.in_(all_raw_ids)
            db_records = session.query(table).filter(criteria).all()

            # By default db_records will return a list of objects
            # from the  table in question, we will convert them
            # into a dictionary for later comparison.
            all_db_ids = helper.get_keys_from_db_dataset(db_records)

        # Do a quick search and separate
        # the raw_data dictionaries into two
        # separate lists named tbi and tbu
        for data in raw_data:
            search = data['id'] not in all_db_ids
            if(search):
                # Database has no record for this
                # raw_data.id so this data goes
                # to the insert bucket (tbi)
                separated_list['tbi'].append(data)

                # Here we can continue because no data
                # can and cannot be in the database
                # at the same time
                continue

            if(search == False):
                # Database has a record for this
                # raw_data.id so this data goes
                # to the update bucket (tbu)

                separated_list['tbu'].append(data)

        return separated_list

    def get_all_filter(self, s = None, table = None, column = None, where = None):
        if(table == None or column == None or s == None): return False
        return s.query(self.mapper[table]).filter(getattr(self.mapper[table], str(column)) == str(where)).all()

    def get_one_filter(self, s = None, table = None, column = None, where = None):
        if(table == None or column == None or s == None): return False
        return s.query(self.mapper[table]).filter(getattr(self.mapper[table], str(column)) == str(where)).one()

    def query(self, table = None, column = None, where = None):
        Session = self.session(self.engine)
        with Session.begin() as se:
            tbl = self.mapper[table]
            return se.query(tbl).filter(getattr(tbl, column) == where)




            #return session.query(self.mapper[table]).filter(getattr(self.mapper[table], str(column)) == str(where))


Base = declarative_base()
metadata = Base.metadata
class ApiQuery(Base):
    __tablename__ = 'api_queries'
    __table_args__ = {'comment': 'Keeps track of API queries'}

    id = Column(INTEGER(11), primary_key=True)
    action = Column(VARCHAR(255))
    params = Column(VARCHAR(255))
    result = Column(VARCHAR(255))
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP()"))

class Country(Base):
    __tablename__ = 'countries'

    id = Column(INTEGER(11), primary_key=True, unique=True)
    name = Column(VARCHAR(255))
    image_path = Column(VARCHAR(255))
    extra = Column(MEDIUMBLOB)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP()"))

class Fixture(Base):
    __tablename__ = 'fixtures'
    __table_args__ = {'comment': 'Endpoint:\thttps://soccer.sportmonks.com/api/v2.0/fixtures/da'}

    id = Column(INTEGER(11), primary_key=True)
    league_id = Column(INTEGER(11))
    season_id = Column(INTEGER(11))
    stage_id = Column(INTEGER(11))
    round_id = Column(INTEGER(11))
    group_id = Column(INTEGER(11))
    aggregate_id = Column(INTEGER(11))
    venue_id = Column(INTEGER(11))
    referee_id = Column(INTEGER(11))
    localteam_id = Column(INTEGER(11))
    visitorteam_id = Column(INTEGER(11))
    winner_team_id = Column(INTEGER(11))
    weather_report = Column(MEDIUMBLOB)
    attendance = Column(INTEGER(11))
    details = Column(INTEGER(11))
    formations = Column(LargeBinary)
    scores = Column(LargeBinary)
    status = Column(VARCHAR(255))
    date_time = Column(VARCHAR(255))
    time = Column(VARCHAR(255))
    timestamp = Column(INTEGER(11), index=True)
    minute = Column(INTEGER(11))
    second = Column(VARCHAR(50))
    coaches = Column(MEDIUMBLOB)
    standings = Column(MEDIUMBLOB)
    assistants = Column(MEDIUMBLOB)
    colors = Column(LargeBinary)
    goals = Column(MEDIUMBLOB)
    cards = Column(MEDIUMBLOB)
    stats = Column(MEDIUMBLOB)
    tvstations = Column(MEDIUMBLOB)
    comments = Column(MEDIUMBLOB)
    updated_at = Column(TIMESTAMP, nullable=False, index=True, server_default=text("CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP()"))

class Heartbeat(Base):
    __tablename__ = 'heartbeat'
    __table_args__ = {'comment': 'Stores the latest python application heartbeat to check if update app is working'}

    id = Column(INTEGER(11), nullable=False, index=True, primary_key=True)
    email_sent = Column(INTEGER(11), nullable=False, server_default=text("0"))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("current_timestamp() ON UPDATE current_timestamp()"))

class League(Base):
    __tablename__ = 'leagues'

    id = Column(INTEGER(11), primary_key=True)
    active = Column(TINYINT(2))
    type = Column(VARCHAR(255))
    legacy_id = Column(INTEGER(11))
    country_id = Column(INTEGER(11))
    logo_path = Column(VARCHAR(255))
    name = Column(VARCHAR(255))
    is_cup = Column(TINYINT(2))
    current_season_id = Column(INTEGER(11))
    current_round_id = Column(INTEGER(11))
    current_stage_id = Column(INTEGER(11))
    coverage = Column(LargeBinary)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP()"))

class Lineup(Base):
    __tablename__ = 'lineups'
    __table_args__ = {'comment': 'This table does not exist as an API endpoint\\r\\nIt was created'}

    id = Column(INTEGER(11), primary_key=True)
    lineup = Column(MEDIUMBLOB)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP()"))

class Player(Base):
    __tablename__ = 'players'

    id = Column(INTEGER(11), primary_key=True)
    position_id = Column(INTEGER(11))
    captain = Column(TINYINT(2))
    number = Column(INTEGER(11))
    injured = Column(TINYINT(2))
    minutes = Column(INTEGER(11))
    appearences = Column(INTEGER(11))
    lineups = Column(INTEGER(11))
    goals = Column(INTEGER(11))
    assists = Column(INTEGER(11))
    saves = Column(INTEGER(11))
    inside_box_saves = Column(INTEGER(11))
    interceptions = Column(INTEGER(11))
    yellowcards = Column(INTEGER(11))
    yellowred = Column(INTEGER(11))
    redcards = Column(INTEGER(11))
    tackles = Column(INTEGER(11))
    blocks = Column(INTEGER(11))
    cleansheets = Column(INTEGER(11))
    rating = Column(VARCHAR(255))
    passes = Column(LargeBinary)
    shots = Column(LargeBinary)
    team_id = Column(INTEGER(11), index=True)
    country_id = Column(INTEGER(11))
    common_name = Column(VARCHAR(255))
    display_name = Column(VARCHAR(255))
    fullname = Column(VARCHAR(255))
    firstname = Column(VARCHAR(255))
    lastname = Column(VARCHAR(255))
    nationality = Column(VARCHAR(255))
    birthdate = Column(VARCHAR(255))
    birthcountry = Column(VARCHAR(255))
    birthplace = Column(VARCHAR(255))
    height = Column(VARCHAR(255))
    weight = Column(VARCHAR(255))
    image_path = Column(VARCHAR(255))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP()"))

class Season(Base):
    __tablename__ = 'seasons'
    __table_args__ = {'comment': 'Endpoint:\thttps://soccer.sportmonks.com/api/v2.0/seasons\\r\\nIn'}

    id = Column(INTEGER(11), primary_key=True)
    name = Column(VARCHAR(255))
    league_id = Column(INTEGER(11))
    is_current_season = Column(TINYINT(2))
    current_round_id = Column(INTEGER(11))
    current_stage_id = Column(INTEGER(11))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP()"))

class Standing(Base):
    __tablename__ = 'standings'
    __table_args__ = {'comment': 'Endpoint:\thttps://soccer.sportmonks.com/api/v2.0/standings/s'}

    id = Column(INTEGER(11), primary_key=True)
    name = Column(VARCHAR(255))
    league_id = Column(INTEGER(11))
    season_id = Column(INTEGER(11))
    round_id = Column(INTEGER(11))
    round_name = Column(INTEGER(11))
    type = Column(VARCHAR(255))
    stage_id = Column(INTEGER(11))
    stage_name = Column(VARCHAR(255))
    resource = Column(VARCHAR(255))
    standings = Column(MEDIUMBLOB)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP()"))

class Team(Base):
    __tablename__ = 'teams'
    __table_args__ = {'comment': 'Endpoint:\thttps://soccer.sportmonks.com/api/v2.0/teams/seaso'}

    id = Column(INTEGER(11), primary_key=True)
    legacy_id = Column(INTEGER(11))
    name = Column(VARCHAR(255))
    short_code = Column(VARCHAR(255))
    twitter = Column(VARCHAR(255))
    country_id = Column(INTEGER(11))
    national_team = Column(TINYINT(2))
    founded = Column(INTEGER(11))
    logo_path = Column(TEXT)
    venue_id = Column(INTEGER(11))
    current_season_id = Column(INTEGER(11), index=True)
    stats = Column(MEDIUMBLOB)
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP()"))

class Venue(Base):
    __tablename__ = 'venues'
    __table_args__ = {'comment': 'Endpoint:\thttps://soccer.sportmonks.com/api/v2.0/venues/seas'}

    id = Column(INTEGER(11), primary_key=True)
    name = Column(VARCHAR(255))
    surface = Column(VARCHAR(255))
    address = Column(VARCHAR(255))
    city = Column(VARCHAR(255))
    capacity = Column(INTEGER(11))
    image_path = Column(VARCHAR(255))
    coordinates = Column(VARCHAR(255))
    updated_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP() ON UPDATE CURRENT_TIMESTAMP()"))

class News(Base):
    __tablename__ = 'news'

    id = Column(BIGINT(20), primary_key=True)
    url = Column(VARCHAR(250))
    title = Column(MEDIUMTEXT)
    second_title = Column(MEDIUMTEXT)
    category = Column(TINYINT(4))
    active = Column(TINYINT(4))
    text = Column(LONGTEXT)
    ext_image = Column(MEDIUMTEXT)
    hashtags = Column(MEDIUMTEXT)
    account_id = Column(MEDIUMTEXT)
    account_screen_name = Column(MEDIUMTEXT)
    account_name = Column(MEDIUMTEXT)
    account_logo = Column(MEDIUMTEXT)
    last_update = Column(TIMESTAMP)
