import datetime
import json


def read_schedule(schedule_date):
    schedule_path = 'schedules/' + schedule_date + '_schedule.json'
    with open(schedule_path, 'r') as schedule_json:
        schedule = json.load(schedule_json)
    morning_schedule = schedule['schedule'][0]
    evening_schedule = schedule['schedule'][1]
    return morning_schedule, evening_schedule


if __name__ == '__main__':
    date = date = datetime.datetime.now().strftime("%d-%m-%Y")
    print(read_schedule(date))