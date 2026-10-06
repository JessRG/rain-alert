import requests
# from twilio.rest import Client
import os
import smtplib
from dotenv import load_dotenv

# load .env environment variables
load_dotenv()

SMTP_GMAIL = os.getenv("SMTP_GMAIL", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "")
TO_EMAIL = os.getenv("TO_EMAIL", "")
PASS_CODE = os.getenv("PASS_CODE", "")
PORT = int(os.getenv("PORT", 2525))
PHONE_NUMBER = os.getenv("PHONE_NUMBER", "")

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
OWN_API_KEY = os.getenv("OWM_API_KEY", "")
# OWN_API_KEY = os.environ["TWILIO_API_KEY"]
# TWILIO_API_SECRET = os.environ["TWILIO_API_SECRET"]
# TWILIO_SID = os.getenv("TWILIO_SID", "")
# TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")

weather_params = {
    "lat": os.getenv("LAT", 0.000000),
    "lon": os.getenv("LNG", 0.000000),
    "appid": OWN_API_KEY,
    "cnt": 4,
}

response = requests.get(url=OWM_Endpoint, params=weather_params)
response.raise_for_status()

forecast_list = response.json()["list"]

will_rain = False
for hour_data in forecast_list:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    # client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    # message = client.messages.create(
    #     body="sms_appointment_reminders",
    #     from_=TWILIO_PHONE_NUMBER,
    #     to=PHONE_NUMBER,
    # )
    #
    # print(message.body)
    message_text = (
        "Subject: Raining Today\n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/plain; charset=utf-8\n\n"
        "It's going to rain today. Remember to bring an umbrella ☔"
    )
    with smtplib.SMTP(SMTP_GMAIL, port=PORT) as smtp:
        smtp.starttls()
        smtp.login(FROM_EMAIL, PASS_CODE)
        smtp.sendmail(
            from_addr=FROM_EMAIL,
            to_addrs=TO_EMAIL,
            msg=message_text.encode('utf-8')
        )