import requests
import json
import datetime


def get_forecast_data(api_key, location):
    # URL of the WeatherUnderground API for a 10 day forecast
    url = "http://api.wunderground.com/api/" + api_key + "/forecast10day/q/" + location + ".json"
    # Calls the API using 'GET' to retrieve the data as a JSON
    api_response = json.loads(requests.get(url).content)
    # Parses the JSON to extract the relevant forecast type
    weather = api_response["forecast"]["simpleforecast"]["forecastday"]
    # Parses the data to extract tomorrow's forecast only
    tomorrow_weather = weather[1]
    # Assigns the high/low temperature and humidity data to a new dictionary
    forecast_data = {"high_temp": int(tomorrow_weather["high"]["celsius"]),
                     "low_temp": int(tomorrow_weather["low"]["celsius"]),
                     "average_hum": int(tomorrow_weather["avehumidity"])}
    return forecast_data


def check_template_exists(schedule_path):
    try:
        open(schedule_path)
        return True
    except FileNotFoundError:
        return False


def load_schedule_template(schedule_path):
    if check_template_exists(schedule_path):
        with open(schedule_path, "r") as template:
            schedule = json.load(template)  # The schedule template
        return schedule
    else:
        print("Schedule not found")


def add_minutes(time, minutes):
    """Increases a given time by a given number of minutes"""
    default_time = datetime.datetime.strptime(time, "%H:%M:%S")
    new_time = default_time + datetime.timedelta(minutes=minutes)
    return new_time.strftime("%H:%M:%S")


def adjust_time(schedule_template, weather_forecast):
    temp_difference = int(weather_forecast["high_temp"]) - int(schedule_template["conditions"]["high_temp"])
    adjustment_level = temp_difference * 5
    start_time = schedule_template["schedule"][0]["start"]
    end_time = schedule_template["schedule"][0]["end"]
    end_time = add_minutes(end_time, adjustment_level)
    duration = str(datetime.datetime.strptime(end_time, "%H:%M:%S") - datetime.datetime.strptime(start_time, "%H:%M:%S"))
    schedule_template["schedule"][0]["end"] = str(end_time).zfill(4)
    schedule_template["schedule"][0]["duration"] = str(duration)
    return schedule_template


def save_schedule(updated_schedule, schedule_dir):
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    path = schedule_dir + '/' + date + "_schedule.json"
    with open(path, 'w') as write_schedule:
        json.dump(updated_schedule, write_schedule)


if __name__ == "__main__":
    defaults = load_schedule_template("schedules/schedule_template.json")
    forecast = get_forecast_data("1fbed46a06fcec66", "UK/Chilwell")
    new_schedule = adjust_time(defaults, forecast)
    save_schedule(new_schedule, 'schedules')
