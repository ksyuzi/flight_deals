from datetime import datetime, timedelta

from data_manager import DataManager
from flight_searcher import FlightSearcher
from notification_manager import NotificationManager

ORIGIN_CITY_IATA = "KRK"

sheety_data_manager = DataManager()
flight_searcher = FlightSearcher()
notification_manager = NotificationManager()

json_data = sheety_data_manager.get_sheety_data()
sheet_prices_data = json_data["prices"]

users_json_data = sheety_data_manager.get_users_data()
sheet_users_data = users_json_data["users"]

date_from = (datetime.now() + timedelta(days=1)).strftime("%d/%m/%Y")
date_to = (datetime.now() + timedelta(days=6 * 30)).strftime("%d/%m/%Y")

for city in sheet_prices_data:
    if city['iataCode'] == "":
        iata_code = flight_searcher.get_iata_code(city['city'])
        city['iataCode'] = iata_code
        city_row_in_sheet = city['id']
        sheety_data_manager.put_iata_to_sheety(iata=iata_code, row=city_row_in_sheet)

    flight = flight_searcher.search_flights(ORIGIN_CITY_IATA, city['iataCode'], date_from, date_to)
    try:
        is_cheaper = flight.price < city['lowestPrice']
    except AttributeError:
        continue
    else:
        if is_cheaper:
            for user_data in sheet_users_data:
                email = user_data["email"]
                if flight.stop_overs > 0:
                    notification_manager.send_text_with_stopover(flight)
                    notification_manager.send_email(email, flight)
                else:
                    notification_manager.send_text(flight)
                    notification_manager.send_email(email, flight)







