import os
import smtplib

from twilio.rest import Client

API_KEY = os.environ['TWILIO_API_KEY']
TWILIO_ACCOUNT_SID = os.environ['TWILIO_ACCOUNT_SID']
TWILIO_TOKEN = os.environ['TWILIO_AUTH_TOKEN']

MY_EMAIL = "sobakacast@gmail.com"
PASSWORD = "vdtrpwbkqmcypvcv"

TWILIO_PHONE_NUMBER = '+15075807312'
RECIPIENT_PHONE_NUMBER = '+48791533936'

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_TOKEN)


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def send_text(self, flight_data):
        twilio_client.messages \
            .create(
                body=f"Low price alert! Only {flight_data.price}USD to fly from{flight_data.origin_city} "
                     f"to {flight_data.destination_city}, from {flight_data.out_date} to {flight_data.return_date}.",
                from_=TWILIO_PHONE_NUMBER,
                to=RECIPIENT_PHONE_NUMBER
            )

    def send_text_with_stopover(self, flight_data):
        twilio_client.messages \
            .create(
                body=f"Low price alert! Only {flight_data.price}USD to fly from{flight_data.origin_city} "
                     f"to {flight_data.destination_city}, from {flight_data.out_date} to {flight_data.return_date}."
                     f"Flight has {flight_data.stop_overs} stop over, via {flight_data.via_city}.",
                from_=TWILIO_PHONE_NUMBER,
                to=RECIPIENT_PHONE_NUMBER
            )

    def send_email(self, email, flight_data):
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=email,
                msg=f"Subject: Flight Alert!\n\n Only {flight_data.price}USD to fly from {flight_data.origin_city.encode('utf-8')} "
                    f"to {flight_data.destination_city.encode('ascii')}, from {flight_data.out_date} to {flight_data.return_date}."
            )
