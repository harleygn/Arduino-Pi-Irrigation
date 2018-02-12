import datetime
import json
import time


def read_schedule(schedule_date):
    schedule_path = 'schedules/' + schedule_date + '_schedule.json'
    with open(schedule_path, 'r') as schedule_json:
        schedule = json.load(schedule_json)
    return schedule['schedule']


def check_timings(schedule):
    time = datetime.datetime.now().time()
    hour = time.hour
    morning_start = datetime.datetime.strptime(schedule[0]['start'], '%H:%M:%S').time()
    morning_end = datetime.datetime.strptime(schedule[0]['end'], '%H:%M:%S').time()
    afternoon_start = datetime.datetime.strptime(schedule[1]['start'], '%H:%M:%S').time()
    afternoon_end = datetime.datetime.strptime(schedule[1]['end'], '%H:%M:%S').time()
    if hour < 12:
        return morning_start <= time < morning_end
    elif hour >= 12:
        return afternoon_start <= time < afternoon_end


def issue_command(current_state, desired_state):
    if (current_state is True) and (desired_state is True):
        print('Tap is already on!')
        return True
    elif (current_state is False) and (desired_state is True):
        print('Tap turned on!')
        return True
    elif (current_state is False) and (desired_state is False):
        print('Tap is already off!')
        return False
    elif (current_state is True) and (desired_state is False):
        print('Tap turned off!')
        return False


if __name__ == '__main__':
    date = date = datetime.datetime.now().strftime("%d-%m-%Y")
    tap_state = False
    while True:
        tap_state = issue_command(tap_state, check_timings(read_schedule(date)))
        time.sleep(3)