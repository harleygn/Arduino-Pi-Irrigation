import datetime
import json


def read_schedule(schedule_date):
    schedule_path = 'schedules/' + schedule_date + '_schedule.json'
    with open(schedule_path, 'r') as schedule_json:
        schedule = json.load(schedule_json)
    return schedule['schedule']


def check_timings(schedule):
    time = datetime.datetime.now()
    hour = time.hour
    morning_start = datetime.datetime.strptime(schedule[0]['start'], '%H:%M:%S')
    morning_end = datetime.datetime.strptime(schedule[0]['end'], '%H:%M:%S')
    afternoon_start = datetime.datetime.strptime(schedule[1]['start'], '%H:%M:%S')
    afternoon_end = datetime.datetime.strptime(schedule[1]['end'], '%H:%M:%S')
    if hour < 12:
        return morning_start <= time < morning_end
    elif hour >= 12:
        return afternoon_start <= time < afternoon_end


if __name__ == '__main__':
    date = date = datetime.datetime.now().strftime("%d-%m-%Y")
    print(check_timings(read_schedule(date)))
