import os
import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv('.env')

parameters = {
    "lat": 33.838249,
    "lon": -83.902153,
    "exclude": "current,minutely,daily",
    "appid": os.environ.get('API_KEY')
}

req = requests.get(url='https://api.openweathermap.org/data/2.5/onecall', params=parameters)
req.raise_for_status()
weather_data = req.json()


def check_for_rain():
    for i in range(12):
        will_rain = weather_data['hourly'][i]['weather'][0]['id']
        if will_rain < 700:
            return True
        else:
            return False


numbers_to_message = [os.environ.get('NUMBER_1'), os.environ.get('NUMBER_2')]

if check_for_rain():
    for numbers in numbers_to_message:
        account_sid = os.environ.get('ACCOUNT_SID')
        auth_token = os.environ.get('AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
            body="It's going to rain today. Remember to bring an ☂️",
            from_=os.environ.get('TWILIO_NUMBER'),
            to=numbers
        )
    print(message.status)
