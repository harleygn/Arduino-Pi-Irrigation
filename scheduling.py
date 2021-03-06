# Import modules for handling API calls, JSON files and date/time objects
import requests
import json
import datetime as dt
import os


def get_forecast_data(api_key, location):
    # URL of the WeatherUnderground API for a 10 day forecast
    url = 'http://api.wunderground.com/api/{}/forecast10day/q/{}.json'.format(
        api_key, location)
    # Calls the API using 'GET' to retrieve the data as a JSON
    api_response = json.loads(requests.get(url).content.decode('utf-8'))
    # Parses the JSON to extract the relevant forecast type
    weather = api_response['forecast']['simpleforecast']['forecastday']
    # Parses the data to extract tomorrow's forecast only
    tomorrow_weather = weather[1]
    # Assigns the high/low temperature and humidity data to a new dictionary
    forecast_data = {'high_temp': int(tomorrow_weather['high']['celsius']),
                     'low_temp': int(tomorrow_weather['low']['celsius']),
                     'average_hum': int(tomorrow_weather['avehumidity'])}
    print('Forecast data obtained: {}'.format(forecast_data))
    return forecast_data


# Loads a JSON schedule template, configured for a typical day,
# which is used for comparison
def load_schedule_template(schedule_path):
    # Returns an error if the template is not found
    if not os.path.isfile(schedule_path):
        print('Schedule template not found at {}'.format(schedule_path))
    else:
        project_root = os.path.dirname(os.path.realpath(__file__))
        schedule_path = project_root + '/' + schedule_path
        # Returns the JSON as a a dictionary, allowing it to be modified
        with open(schedule_path, 'r') as template:
            schedule = json.load(template)  # The schedule template
        return schedule, project_root


# Adjusts a timestamp by a given number of minutes
def add_minutes(time, minutes):
    # Converts the input time as a formatted datetime object
    default_time = dt.datetime.strptime(time, '%H:%M:%S')
    # Increases the time by adding the specified minutes as timedelta object
    new_time = default_time + dt.timedelta(minutes=minutes)
    # Returns the new time in the correct format
    return new_time.strftime('%H:%M:%S')


# Alters the new schedule time parameters according to the forecasted difference
# in temperature against the template
def adjust_time(schedule_template, weather_forecast):
    # Finds the difference in in forecasted temperature compared to
    # typical temperature
    temp_difference = int(weather_forecast['high_temp']) - int(
        schedule_template['conditions']['high_temp'])
    # Multiplies by five to create a significant difference,
    # else the change wouldn't be enough
    adjustment_level = temp_difference * 5
    # Gets the typical start and end times for the morning schedule
    start_time = schedule_template['schedule'][0]['start']
    end_time = schedule_template['schedule'][0]['end']
    # Adjusts the end time according the temperature differential
    end_time = add_minutes(end_time, adjustment_level)
    # Adjusts the duration to match the start and end times
    duration = dt.datetime.strptime(
        end_time, '%H:%M:%S') - dt.datetime.strptime(start_time, '%H:%M:%S')
    # Schedule is altered with new calculations
    schedule_template['schedule'][0]['end'] = str(end_time)
    schedule_template['schedule'][0]['duration'] = str(duration)
    schedule = update_forecast(schedule_template, weather_forecast)
    print(json.dumps(schedule, indent=4))
    return schedule


# Records the weather forecast data to the JSON schedule
def update_forecast(schedule, weather_forecast):
    # Extracts and assigns the data from the forecast to the schedule
    schedule['conditions']['high_temp'] = weather_forecast['high_temp']
    schedule['conditions']['low_temp'] = weather_forecast['low_temp']
    schedule['conditions']['humidity'] = weather_forecast['average_hum']
    # Returns the now fully updated schedule for saving
    return schedule


# Saves a the new schedule as JSON, named according the the date,
# for use by other programs
def save_schedule(updated_schedule, project_root, schedule_dir):
    # Gets the current date
    date = dt.datetime.now().strftime('%d-%m-%Y')
    # Formulates an appropriate file name in the specified directory
    path = project_root + '/' + schedule_dir + '/' + date + '_schedule.json'
    # Creates the new JSON file
    with open(path, 'w') as write_schedule:
        # Exports the JSON data to the file and saves it
        json.dump(updated_schedule, write_schedule)
        print('Schedule for {} saved to {}'.format(date, path))


def main():
    # Specifies location of the template schedule
    defaults, root = load_schedule_template('schedules/schedule_template.json')
    # Specifies the key and location to be used in the Wunderground API call
    forecast = get_forecast_data('1fbed46a06fcec66', 'UK/Chilwell')
    # Creates the new schedule as a dictionary object
    new_schedule = adjust_time(defaults, forecast)
    # Saves the new schedule
    save_schedule(new_schedule, root, 'schedules')


# Entry point for the script
if __name__ == '__main__':
    main()
