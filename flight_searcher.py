import os

import requests

from flight_data import FlightData

LOCATION_ENDPOINT = "https://tequila-api.kiwi.com/locations/query"
SEARCH_ENDPOINT = "https://api.tequila.kiwi.com/v2/search"
TEQUILA_API = os.environ["TEQUILA_API"]


class FlightSearcher:
    # This class is responsible for talking to the Flight Search API.
    def get_iata_code(self, city):
        header = {"apikey": TEQUILA_API}
        query = {
            "term": city,
            "location_types": "city",
        }
        tequila_response = requests.get(url=LOCATION_ENDPOINT, params=query, headers=header)
        data = tequila_response.json()
        return data["locations"][0]["code"]

    def search_flights(self, origin_city_code, destination_city_code, date_from, date_to):
        header = {"apikey": TEQUILA_API}
        query = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": date_from,
            "date_to": date_to,
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD",
        }
        tequila_response = requests.get(url=SEARCH_ENDPOINT, params=query, headers=header)
        try:
            data = tequila_response.json()["data"][0]
        except IndexError:
            query["max_stopovers"] = 2
            tequila_response = requests.get(url=SEARCH_ENDPOINT, params=query, headers=header)
            try:
                data = tequila_response.json()["data"][0]
            except IndexError:
                flight_data = None
            else:
                flight_data = FlightData(
                    price=data['price'],
                    origin_city=data["route"][0]["cityFrom"],
                    origin_airport=data["route"][0]["flyFrom"],
                    destination_city=data["route"][1]["cityTo"],
                    destination_airport=data["route"][1]["flyTo"],
                    out_date=data["route"][0]["local_departure"].split("T")[0],
                    return_date=data["route"][2]["local_departure"].split("T")[0],
                    stop_overs=1,
                    via_city=data["route"][0]["cityTo"]
                )
        else:
            flight_data = FlightData(
                price=data["price"],
                origin_city=data["route"][0]["cityFrom"],
                origin_airport=data["route"][0]["flyFrom"],
                destination_city=data["route"][0]["cityTo"],
                destination_airport=data["route"][0]["flyTo"],
                out_date=data["route"][0]["local_departure"].split("T")[0],
                return_date=data["route"][1]["local_departure"].split("T")[0],
            )
        return flight_data
