import helper, requests, json, secrets, constants
from api import Api

class Endpoint(Api):
    def __init__(self):
        Api.__init__(self)

    def query(self, action, includes = []):
        self.action = action
        self.includes = includes
        self.latest_query = self.action
        with requests.Session() as r:
            # try to call api with no params // todo => add params
            try:
                response = r.get(constants.API_URL + self.action, params=[('api_token', secrets.API_KEY),('page', "1"),('include', ",".join(self.includes))], timeout=constants.DEFAULT_TIMEOUT)
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