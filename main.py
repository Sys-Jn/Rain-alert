import requests
from twilio.rest import Client
import os

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"

api_key = os.getenv("OWM_API_KEY")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
to_number = os.getenv("TO_NUMBER")
from_number = os.getenv("FROM_NUMBER")

weather_params = {
    "lat": 26.912434,
    "lon": 75.787270,
    "appid": api_key,
    "cnt": 6,
}

response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()
weather_data = response.json()
# weather_id = weather_data["list"][0]["weather"][0]["id"]
will_rain = False
for hour_data in weather_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code)<700:
        will_rain = True

client = Client(account_sid, auth_token)

if will_rain:
    body = "🌧 It's going to rain! Remember to bring an umbrella!"
else:
    body = "☀ It's a clear day! Have fun."

message = client.messages.create(
    body=body,
    from_=from_number,
    to=to_number
)