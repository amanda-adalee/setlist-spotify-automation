from exceptions import ResponseException
import requests
class Setlist:
    def __init__(self, setlist_id):
        self.id = setlist_id
        self.all_details = self.get_setlist()
        self.tour_name = self.get_tour_name()

    def get_setlist(self):

        url = f"https://api.setlist.fm/rest/1.0/setlist/{self.id}"

        headers = {
            "Accept": "application/json",
            "x-api-key": "3iaIHpoxCTKgxBjemKGQGjy7dGE2aj9llRvJ"
            }

        response = requests.get(url, headers=headers)

        # check for valid response status
        if response.status_code != 200:
            raise ResponseException(response.status_code)

        json_response = response.json()

        return json_response

    def get_tour_name(self):

        tour_name = self.get_setlist()["tour"]["name"]

        return tour_name