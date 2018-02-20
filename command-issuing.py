from datetime import datetime as dt
import json
import time
import serial


def read_schedule(schedule_date):
    schedule_path = 'schedules/' + schedule_date + '_schedule.json'
    with open(schedule_path, 'r') as schedule_json:
        schedule = json.load(schedule_json)
    return schedule['schedule']


def check_timings(schedule):
    current_time = dt.now().time()
    hour = current_time.hour
    morning_start = dt.strptime(schedule[0]['start'], '%H:%M:%S').time()
    morning_end = dt.strptime(schedule[0]['end'], '%H:%M:%S').time()
    afternoon_start = dt.strptime(schedule[1]['start'], '%H:%M:%S').time()
    afternoon_end = dt.strptime(schedule[1]['end'], '%H:%M:%S').time()
    if hour < 12:
        return morning_start <= current_time < morning_end
    elif hour >= 12:
        return afternoon_start <= current_time < afternoon_end


def issue_command(current_state, desired_state):
    if (current_state is True) and (desired_state is True):
        print('Tap is already on!')
        return True
    elif (current_state is False) and (desired_state is True):
        tap_control(serial, desired_state)
        print('Tap turned on!')
        return True
    elif (current_state is False) and (desired_state is False):
        print('Tap is already off!')
        return False
    elif (current_state is True) and (desired_state is False):
        tap_control(serial, desired_state)
        print('Tap turned off!')
        return False


def tap_control(serial, state):
    connection = False
    time.sleep(1)
    serial.setDTR(0)
    time.sleep(1)
    while not connection:
        serial.write(bytes('call\n', 'utf-8'))
        if serial.readline() == 'response':
            connection = True
    if connection:
        if state:
            serial.write(bytes('on'))
        elif not state:
            serial.write(bytes('off'))


if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    date = date = dt.now().strftime("%d-%m-%Y")
    tap_state = False
    while True:
        tap_state = issue_command(tap_state, check_timings(read_schedule(date)))
        time.sleep(3)
