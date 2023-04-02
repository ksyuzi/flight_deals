import os

import requests

SHEET_ENDPOINT = os.environ["SHEET_ENDPOINT"]
BEARER_TOKEN = os.environ["BEARER_TOKEN"]
SHEETY_USERS_ENDPOINT = "https://api.sheety.co/d2f7acbfc3ba12c7b5744c3fc255ace9/flightDeals/users"


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.authorization_header = {"Authorization": f"Bearer {BEARER_TOKEN}"}

    def get_sheety_data(self):
        sheety_response = requests.get(url=SHEET_ENDPOINT, headers=self.authorization_header)
        sheety_data = sheety_response.json()
        return sheety_data

    def put_iata_to_sheety(self, iata, row):
        passing_iata = {
            "price": {
                "iataCode": iata
            }
        }
        url = f"{SHEET_ENDPOINT}/{row}"
        requests.put(url=url, json=passing_iata, headers=self.authorization_header)

    def get_users_data(self):
        users_response = requests.get(url=SHEETY_USERS_ENDPOINT, headers=self.authorization_header)
        return users_response.json()
