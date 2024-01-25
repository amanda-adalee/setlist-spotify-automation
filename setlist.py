import requests
import os

class Setlist:

    # Setlist constructor
    def __init__(self, url):
        self.id = self.get_setlist_id(url)
        self.json_data = self.get_setlist()

    # extract the setlist id from user input url
    def get_setlist_id(self, url):

        last_dash_index = url.rfind("-")
        last_period_index = url.rfind(".")
        setlist_id = url[last_dash_index + 1:last_period_index]

        return setlist_id

    # api request for retrieving setlist data returns json data
    def get_setlist(self):

        url = f"https://api.setlist.fm/rest/1.0/setlist/{self.id}"

        headers = {
            "Accept": "application/json",
            "x-api-key": os.environ['setlist.fm_api_key']
            }

        # send the request and save the response
        response = requests.get(url, headers=headers)

        # raise an exception if the status code is not successful
        response.raise_for_status()

        json_response = response.json()

        return json_response
