import logging, constants, helper
from datetime import datetime
from phpserialize import serialize
from logging.handlers import RotatingFileHandler



class Data:

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(getattr(logging, str(constants.LOG_LEVEL)))
        self.file_handler = RotatingFileHandler(constants.DATA_LOG_FILENAME, maxBytes=constants.LOG_MAX_BYTES, backupCount=constants.LOG_BACKUP_COUNT)
        self.file_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
        self.logger.addHandler(self.file_handler)
        self.reshaped_data = []

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            self.logger.error(f'Suppressing exception: {exc_type}')
            self.logger.error(f'Traceback: {exc_tb}')
        return True

    def __is_valid_type(self, data):
        """ Validates data which is accessed
            from its self instance
        """
        if(isinstance(data, list) == False):
            return False

        if(len(data) == 0):
            return False

        for _dict in data:
            if(isinstance(_dict, dict)):
                return True

    def reshape(self, data, endpoint = None):
        """ Validates data and removes or adds
            columns etc. and returns the shaped
            data

        Args:
            data ([list]): List of dictionaries usually
            coming straight from the API and
            in [{...},{...}] format

            type ([string]): Represents the logic type
            of reshaping based on API endpoint name
            valid are one livescores, fixtures, ...
        """
        if(isinstance(type, str)):
            return False

        if(self.__is_valid_type(data) == False):
            return False

        self.raw_data = data
        self.endpoint = endpoint

        self.__do()

        return self.reshaped_data

    def __do(self):

        if(self.endpoint == 'twitter'):
            self.reshaped_data.append(
                {
                    'id': int(self.raw_data[0].id),
                    'url': f"{str(helper.clean_string(self.raw_data[0].full_text[:15])).lower().replace(' ', '-')}-{str(self.raw_data[0].id)}",
                    'title': f"{self.raw_data[0].user.name}",
                    'second_title': f"{str(helper.de_url(helper.de_emojify(self.raw_data[0].full_text[:150])))}",
                    'category': 3,
                    'active': 1,
                    'text': f"{str(helper.de_url(helper.de_emojify(self.raw_data[0].full_text)))}",
                    'ext_image': str(helper.media_key(self.raw_data[0].entities, 'media')).replace('http://', 'https://'),
                    'hashtags': serialize(helper.extract_hashtags(self.raw_data[0].full_text)) if helper.extract_hashtags(self.raw_data[0].full_text)!=None else None,
                    'account_id': str(self.raw_data[0].user.id),
                    'account_screen_name': str(self.raw_data[0].user.screen_name),
                    'account_name': str(self.raw_data[0].user.name),
                    'account_logo': str(self.raw_data[0].user.profile_image_url_https),
                    'last_update': str(self.raw_data[0].created_at.strftime('%Y-%m-%d %H:%M:%S'))
                }
            )
        else:
            for elem in self.raw_data:
                if(self.endpoint == 'livescores' or self.endpoint == 'fixtures/now' or self.endpoint == 'fixtures'):
                    # Livescore structure
                    self.reshaped_data.append(
                        {
                            'id': elem['id'],
                            'league_id': elem['league_id'],
                            'season_id': elem['season_id'],
                            'stage_id': elem['stage_id'],
                            'round_id': elem['round_id'],
                            'group_id': elem['group_id'],
                            'aggregate_id': elem['aggregate_id'],
                            'venue_id': elem['venue_id'] if isinstance(elem['venue_id'], int) else 0,
                            'referee_id': elem['referee_id'],
                            'localteam_id': elem['localteam_id'],
                            'visitorteam_id': elem['visitorteam_id'],
                            'winner_team_id': elem['winner_team_id'],
                            'weather_report': serialize(elem['weather_report']) if elem['weather_report']!=None else None,
                            'attendance': elem['attendance'],
                            'details': elem['details'],
                            'formations': serialize(elem['formations']) if elem['formations']!=None else None,
                            'scores': serialize(elem['scores']) if elem['scores']!=None else None,
                            'status': elem['time']['status'],
                            'date_time': elem['time']['starting_at']['date_time'],
                            'time': elem['time']['starting_at']['time'],
                            'timestamp': elem['time']['starting_at']['timestamp'],
                            'minute': elem['time']['minute'] if 'minute' in elem['time'] else None,
                            'second': elem['time']['second'] if 'second' in elem['time'] else None,
                            'coaches': serialize(elem['coaches']) if elem['coaches']!=None else None,
                            'standings': serialize(elem['standings']) if elem['standings']!=None else None,
                            'assistants': serialize(elem['assistants']) if elem['assistants']!=None else None,
                            'colors': serialize(elem['colors']) if elem['colors']!=None else None,
                            'goals': serialize(elem['goals']) if elem['goals']!=None else None,
                            'cards': serialize(elem['cards']) if elem['cards']!=None else None,
                            'stats': serialize(elem['stats']) if elem['stats']!=None else None,
                            'tvstations': serialize(elem['tvstations']) if elem['tvstations']!=None else None,
                            'comments': serialize(elem['comments']) if elem['comments']!=None else None,
                            'updated_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
                elif(self.endpoint == 'lineups'):
                    self.reshaped_data.append(
                        {
                            'id': elem['id'],
                            'lineup': serialize(elem['lineup']['data']) if elem['lineup']['data']!=None else None,
                            'updated_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
                elif(self.endpoint == 'countries'):
                    self.reshaped_data.append(
                        {
                            'id': elem['id'],
                            'name': elem['name'],
                            'image_path': elem['image_path'],
                            'extra': serialize(elem['extra']) if elem['extra']!=None else None,
                            'updated_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
                elif(self.endpoint == 'leagues'):
                    self.reshaped_data.append(
                        {
                            'id': elem['id'],
                            'active': elem['active'],
                            'type': elem['type'],
                            'legacy_id': elem['legacy_id'],
                            'country_id': elem['country_id'],
                            'logo_path': elem['logo_path'],
                            'name': elem['name'],
                            'is_cup': elem['is_cup'],
                            'current_season_id': elem['current_season_id'],
                            'current_round_id': elem['current_round_id'],
                            'current_stage_id': elem['current_stage_id'],
                            'coverage': serialize(elem['coverage']) if elem['coverage']!=None else None,
                            'updated_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
                elif(self.endpoint == 'fixtures/multi'):
                    self.reshaped_data.append(
                        {
                            'id': elem['id'],
                            'lineup': serialize(elem['lineup']['data']),
                            'updated_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
                elif(self.endpoint == 'players'):
                    self.reshaped_data.append(
                        {
                            'id': elem['player_id'],
                            'position_id': elem['position_id'],
                            'number': elem['number'],
                            'captain': elem['captain'],
                            'injured': elem['injured'],
                            'minutes': elem['minutes'],
                            'appearences': elem['appearences'],
                            'lineups': elem['lineups'],
                            'goals': elem['goals'],
                            'assists': elem['assists'],
                            'saves': elem['saves'],
                            'inside_box_saves': elem['inside_box_saves'],
                            'interceptions': elem['interceptions'],
                            'yellowcards': elem['yellowcards'],
                            'yellowred': elem['yellowred'],
                            'redcards': elem['redcards'],
                            'tackles': elem['tackles'],
                            'blocks': elem['blocks'],
                            'cleansheets': elem['cleansheets'],
                            'rating': elem['rating'],
                            'passes': serialize(elem['passes']) if elem['passes']!=None else None,
                            'shots': serialize(elem['shots']) if elem['shots']!=None else None,
                            'team_id': elem['player']['data']['team_id'],
                            'country_id': elem['player']['data']['country_id'],
                            'common_name': elem['player']['data']['common_name'],
                            'display_name': elem['player']['data']['display_name'],
                            'fullname': elem['player']['data']['fullname'],
                            'firstname': elem['player']['data']['firstname'],
                            'lastname': elem['player']['data']['lastname'],
                            'nationality': elem['player']['data']['nationality'],
                            'birthdate': elem['player']['data']['birthdate'],
                            'birthcountry': elem['player']['data']['birthcountry'],
                            'birthplace': elem['player']['data']['birthplace'],
                            'height': elem['player']['data']['height'],
                            'weight': elem['player']['data']['weight'],
                            'image_path': elem['player']['data']['image_path'],
                            'updated_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
                elif(self.endpoint == 'seasons'):
                    self.reshaped_data.append(
                        {
                            'id': elem['id'],
                            'name': elem['name'],
                            'league_id': elem['league_id'],
                            'is_current_season': elem['is_current_season'],
                            'current_round_id': elem['current_round_id'],
                            'current_stage_id': elem['current_stage_id'],
                            'updated_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
                elif(self.endpoint == 'standings'):
                    self.reshaped_data.append(
                        {
                            'id': elem['id'],
                            'name': elem['name'],
                            'league_id': elem['league_id'],
                            'season_id': elem['season_id'],
                            'round_id': elem['round_id'],
                            'round_name': elem['round_name'],
                            'stage_id': elem['stage_id'],
                            'stage_name': elem['stage_name'],
                            'resource': elem['resource'],
                            'standings': serialize(elem['standings']['data']) if elem['standings']['data']!=None else None,
                            'updated_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
                elif(self.endpoint == 'teams'):
                    self.reshaped_data.append(
                        {
                            'id': elem['id'],
                            'legacy_id': elem['legacy_id'],
                            'name': elem['name'],
                            'short_code': elem['short_code'],
                            'twitter': elem['twitter'],
                            'country_id': elem['country_id'],
                            'national_team': elem['national_team'],
                            'founded': elem['founded'],
                            'logo_path': elem['logo_path'],
                            'venue_id': elem['venue_id'],
                            'current_season_id': elem['current_season_id'],
                            'stats': serialize(elem['stats']) if elem['stats']!=None else None,
                            'updated_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )
                elif(self.endpoint == 'venues/season'):
                    self.reshaped_data.append(
                        {
                            'id': elem['id'],
                            'name': elem['name'],
                            'surface': elem['surface'],
                            'address': elem['address'],
                            'city': elem['city'],
                            'capacity': elem['capacity'],
                            'image_path': elem['image_path'],
                            'coordinates': elem['coordinates'],
                            'updated_at': datetime.today().strftime('%Y-%m-%d %H:%M:%S')
                        }
                    )

    def api_result_path_mapper(self, endpoint = None, data = None):
        if(isinstance(data, list) == False or isinstance(endpoint, str) == False):
            return False

        if(endpoint == 'standings/season'):
            if('data' not in data):
                return False

            if('standings' not in data['data']):
                return False

            if('data' not in data['data']['standings']):
                return False

            return data['data']['standings']['data']
