from setlist_auth import API_KEY
import requests

class Setlist:

    def __init__(self, url):
        self.id = self.get_setlist_id(url)
        self.json_data = self.get_setlist()

    def get_setlist_id(self, url):

        # extract the setlist id from user input url
        last_dash_index = url.rfind("-")
        last_period_index = url.rfind(".")
        setlist_id = url[last_dash_index + 1:last_period_index]

        return setlist_id

    # api request for retrieving setlist data in json format
    def get_setlist(self):

        url = f"https://api.setlist.fm/rest/1.0/setlist/{self.id}"

        headers = {
            "Accept": "application/json",
            "x-api-key": f"{API_KEY}"
            }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        json_response = response.json()

        return json_response
