import requests
from datetime import datetime
import smtplib

MY_LAT = 43.222015
MY_LONG = 76.851250
my_email = "TestPythonEmailSMTP@gmail.com"
my_password = "testpythonemailsmtp"

def is_iss_overhead():
    response_from_ISS = requests.get("http://api.open-notify.org/iss-now.json")
    data_ISS = response_from_ISS.json()
    latitude_ISS = float(data_ISS["iss_position"]["latitude"])
    longitude_ISS = float(data_ISS["iss_position"]["longitude"])
    if MY_LAT-5 <= latitude_ISS <= MY_LAT+5 and MY_LONG-5 <= longitude_ISS <= MY_LONG+5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    today_date = datetime.now()
    today_hour = today_date.hour

    if today_hour >= sunset or today_hour <= sunrise:
        return True



if is_iss_overhead() and is_night():
    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()
    connection.login(user=my_email, password=my_password)
    connection.sendmail(from_addr=my_email, to_addrs=my_email, msg="Subject:Look Up!\n\nTHE ISS IS ABOVE YOUR CURRENT LOCATION!")

