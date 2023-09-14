from exceptions import ResponseException
import requests
class Setlist:
    def __init__(self, setlist_id):
        self.id = setlist_id
        self.json_data = self.get_setlist()

    def get_setlist(self):

        url = f"https://api.setlist.fm/rest/1.0/setlist/{self.id}"

        headers = {
            "Accept": "application/json",
            "x-api-key": "3iaIHpoxCTKgxBjemKGQGjy7dGE2aj9llRvJ"
            }

        response = requests.get(url, headers=headers)

        # check for valid response status
        if response.status_code != 201:
            raise ResponseException(response.status_code)

        json_response = response.json()
        print(json_response)
        return json_response
