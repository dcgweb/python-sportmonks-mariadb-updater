import requests, constants, json, helper
from termcolor import colored

class Api:
    def __enter__(self):
        return self

    def __init__(self):
        self.latest_query = None
        self.query_amt = 0
        self.data = []
        self.error = None
        print('Successfully initialized API Class')

    def query(self, action):
        self.action = action
        self.latest_query = self.action
        with requests.Session() as r:
            # try to call api with no params // todo => add params
            try:
                response = r.get(constants.API_URL + self.action, params=[('api_token', constants.API_KEY), ('page', "1")], timeout=constants.DEFAULT_TIMEOUT)
                self.query_amt += 1
            except Exception as e:
                helper.write_log(f"Latest API query of : {self.latest_query} failed with {e}")
                self.error = e
                return False

            raw_data = json.loads(response.text)
            # find last page if there's pagination in the result
            last_page = self.get_total_pages(raw_data)

            # paginate if last_page is bigger than 1
            if(int(last_page) > 1):
                # return paginated result ( merged list of dictionaries )
                self.paginator(raw_data, last_page)
            else:
                # return json object's data key ( where the meat really is )
                try:
                    self.data = raw_data['data']
                except Exception as e:
                    helper.write_log(f"Latest API query of : {self.latest_query} failed with {e}")
                    self.error = e
                    return False
                else:
                    return True

    def get_total_pages(self, data):
        try:
            total_pages = data['meta']['pagination']['total_pages']
        except:
            helper.write_log('Total pages was undefined, assuming it to be 1')
            total_pages = 1
        finally:
            return total_pages

    def paginator(self, data, last_page):
        merged_data = []
        data_list = [].append(data)
        for page in range(2, int(last_page) + 1):
            with requests.Session() as r:
                try:
                    response = r.get(constants.API_URL + self.action, params=[('api_token', constants.API_KEY), ('page', str(page))], timeout=constants.DEFAULT_TIMEOUT)
                    self.query_amt += 1
                except Exception as e:
                    helper.write_log(f"Latest API query of : {self.latest_query} failed with {e}")
                    self.error = e
                    return False
                else:
                    data_list.append(json.loads(response.text))
            for f_data in data_list:
                for c_data in f_data['data']:
                    merged_data.append(c_data)
            self.data = merged_data
            return True

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Total Queries : {self.query_amt}")
        if(self.error):
            print(f"Errors : {self.error}")
        print('Successfully destroyed the API Class')
