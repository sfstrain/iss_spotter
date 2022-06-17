import requests
import datetime as dt
import time

# Latitude and longitude for Memphis, TN, USA from https://www.latlong.net/
MEM_LAT = 35.143379
MEM_LONG = -90.052139
MEM_UTC_OFFSET = -5  # CDT; -6 for CST


iss_url = "http://api.open-notify.org/iss-now.json"
location_tracking = []

while True:
    response = requests.get(url=iss_url)
    response.raise_for_status()
    data = response.json()
    iss_longitude = float(data["iss_position"]["longitude"])
    iss_latitude = float(data["iss_position"]["latitude"])

    iss_position = (iss_latitude, iss_longitude)
    memphis_position = (MEM_LAT, MEM_LONG)

    parameters = {
        "lat": MEM_LAT,
        "lng": MEM_LONG,
        "formatted": 0,
    }

    sunrise_url = "https://api.sunrise-sunset.org/json"
    response = requests.get(url=sunrise_url, params=parameters)
    response.raise_for_status()
    data = response.json()

    utc_offset = dt.timedelta(hours=float(MEM_UTC_OFFSET))
    sunrise = dt.datetime.strptime(data["results"]["sunrise"], "%Y-%m-%dT%H:%M:%S%z")
    sunset = dt.datetime.strptime(data["results"]["sunset"], "%Y-%m-%dT%H:%M:%S%z")
    time_now = dt.datetime.now(dt.timezone.utc)

    # # print(f"{'Sunrise:':15} {sunrise}")
    # # print(f"{'Sunset:':15} {sunset}")
    print(f"{'Current time:':15} {time_now}")
    print(f"{'Location of the ISS:':24} {iss_position}")
    print(f"   ")
    # print(f"{'My Location:':24}{memphis_position}")

    if abs(MEM_LAT - iss_latitude) < 5 and abs(MEM_LONG - iss_longitude) < 5:
        print(f"The ISS is overhead at {time_now}")

    # if sunrise < time_now < sunset and abs(MEM_LAT - iss_latitude) < 5 and abs(MEM_LONG - iss_longitude) < 5:
    #     print("Dr. Angela, I'm not sending an email because it's a security violation!!")

    time.sleep(60)
