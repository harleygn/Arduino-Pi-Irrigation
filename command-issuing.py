from datetime import datetime as dt
import json
import time
import serial


def read_schedule(schedule_date):
    schedule_path = 'schedules/' + schedule_date + '_schedule.json'
    with open(schedule_path, 'r') as schedule_json:
        schedule = json.load(schedule_json)
    return schedule['schedule']


# Checks whether a the schedule should be active
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
    serial_conn = check_connection()
    if (current_state is False) and (desired_state is True):
        tap_control(serial_conn, desired_state)
        return True
    elif (current_state is True) and (desired_state is False):
        tap_control(serial_conn, desired_state)
        return False
    else:
        return current_state


def tap_control(serial_conn, state):
    connection = False
    if state:
        command = 'on\n'
    else:
        command = 'off\n'
    if not serial_conn:
        print('Tap turned {}'.format(command))
    else:
        while not connection:
            serial_conn.write(bytes('call\n', 'utf-8'))
            if serial_conn.readline().decode().strip() == 'response':
                connection = True
                serial_conn.write(bytes(command, 'utf-8'))


# Attempts to open serial port, defaults to manual input
def check_connection():
    try:
        serial_conn = serial.Serial('/dev/ttyUSB0', 9600)
    except serial.serialutil.SerialException:
        try:
            serial_conn = serial.Serial('/dev/ttyACM0', 9600)
        except serial.serialutil.SerialException:
            serial_conn = False
    return serial_conn


if __name__ == '__main__':
    time.sleep(2)
    date = date = dt.now().strftime('%d-%m-%Y')
    tap_state = False
    while True:
        tap_state = issue_command(tap_state, check_timings(read_schedule(date)))
        time.sleep(3)
