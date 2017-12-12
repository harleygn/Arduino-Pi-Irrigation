import requests
import json
import datetime


def add_minutes(time, minutes):
    full_date = datetime.strptime(time, "%H%M")
    full_date = full_date + datetime.timedelta(minutes=minutes)
    return full_date.time()


def adjust_time(schedule_template, weather_forecast):
    temp_difference = int(default_conditions["high_temp"]) - int(weather_forecast["high_temp"])
    end_time = schedule_template["schedule"][0]["end"]
    end_time = add_minutes(end_time, temp_difference * 10)
    schedule_template["schedule"][0]["end"] = str(end_time).zfill(4)
    return schedule_template


# URL of the WeatherUnderground API
url = "http://api.wunderground.com/api/1fbed46a06fcec66/forecast10day/q/UK/Chilwell.json"
# Calls the API using 'GET' to retrieve the 10 day forecast as a JSON

api_response = json.loads(requests.get(url).content)
# Parses the JSON to extract the relevant forecast type
weather = api_response["forecast"]["simpleforecast"]["forecastday"]
# Parses the data to extract tomorrow's forecast only
tomorrowWeather = weather[1]
# Assigns the high/low temperature and humidity data to a new dictionary
forecast = {"high_temp": int(tomorrowWeather["high"]["celsius"]), "low_temp": int(tomorrowWeather["low"]["celsius"]),
            "average_hum": int(tomorrowWeather["avehumidity"])}

with open("schedule_template.json", "r") as template:
    schedule = json.load(template)  # The schedule template
    default_conditions = schedule["conditions"]
    default_timings = schedule["schedule"]

print(schedule)
print(adjust_time(schedule, forecast))
print(forecast)
