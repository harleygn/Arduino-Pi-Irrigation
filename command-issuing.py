# Import modules
from datetime import datetime as dt
import json
import time
import serial
import os


# Loads the current schedule from the JSON file
def read_schedule(schedule_date):
    project_root = os.path.dirname(os.path.realpath(__file__))
    # Builds the schedule path using the current data
    schedule_path = '{}/schedules/{}_schedule.json'.format(project_root,
                                                           schedule_date)
    # Opens the schedule file
    with open(schedule_path, 'r') as schedule_json:
        # Loads the JSON data as a string
        schedule = json.load(schedule_json)
    # Returns only the schedule data
    return schedule['schedule']


# Checks whether a the schedule should be active
def check_timings(schedule):
    # Gets the current time as a datetime object
    current_time = dt.now().time()
    # Gets the hour from the time object
    hour = current_time.hour
    # Converts the timestamps to datetime objects
    # This allows comparison between the timestamps
    morning_start = dt.strptime(schedule[0]['start'], '%H:%M:%S').time()
    morning_end = dt.strptime(schedule[0]['end'], '%H:%M:%S').time()
    afternoon_start = dt.strptime(schedule[1]['start'], '%H:%M:%S').time()
    afternoon_end = dt.strptime(schedule[1]['end'], '%H:%M:%S').time()
    # If the hour is less than 12 the morning schedules are used
    # Compares the current time to the start and end times
    # This determines if the schedule should be active
    if hour < 12:
        return morning_start <= current_time < morning_end
    elif hour >= 12:
        return afternoon_start <= current_time < afternoon_end


# Determines which command to be issued
def issue_command(current_state, desired_state):
    # Gets serial connection information
    serial_conn = check_connection()
    # If the tap is off, but should be on:
    if (current_state is False) and (desired_state is True):
        # Sends command to turn tap on
        tap_control(serial_conn, desired_state)
        # Sets current state to 'on'
        return True
    # If the tap is on, but should be off:
    elif (current_state is True) and (desired_state is False):
        # Sends command to turn tap off
        tap_control(serial_conn, desired_state)
        # Sets the current state to 'off'
        return False
    # Else if the tap is does not need switching on/off:
    else:
        # Maintains the current tap state
        return current_state


# Issues the command via serial to the tap controller
def tap_control(serial_conn, state):
    # Sets the boolean flag for call/response status
    connection = False
    # If the tap should be on:
    if state:
        # 'On' command is assigned
        command = 'on'
    # Else if the tap should be off:
    else:
        # 'Off' command is set
        command = 'off'
    # If no serial connection is available:
    if not serial_conn:
        # Message is printed to the terminal
        print('Tap turned {} at {}'.format(command, time.strftime('%X')))
    # Otherwise, a serial connection is available:
    else:
        # While there is no response
        while not connection:
            # Send the 'call' signal
            serial_conn.write(bytes('call\n', 'utf-8'))
            # If the message is a valid 'response'
            if serial_conn.readline().decode().strip() == 'response':
                # Sets the flag to indicate a valid call/response
                connection = True
                # Sends the command via the serial port
                serial_conn.write(bytes(command + '\n', 'utf-8'))


# Attempts to open serial port, defaults to manual input
def check_connection():
    # Attempts to open the first possible serial port
    try:
        serial_conn = serial.Serial('/dev/ttyUSB0', 9600)
    # If this fails to open:
    except serial.serialutil.SerialException:
        # The other possible port is attempted
        try:
            serial_conn = serial.Serial('/dev/ttyACM0', 9600)
        # If this fails also, no serial connection is made
        except serial.serialutil.SerialException:
            # Indicates that output should be sent to terminal
            serial_conn = False
    return serial_conn


# Main execution of the script
def main():
    # Gets the current date in the format 'DD-MM-YYYY'
    date = dt.now().strftime('%d-%m-%Y')
    # Sets the tap state boolean flag to closed
    tap_state = False
    # Checks if the tap should be open or closed every minute
    while True:
        tap_state = issue_command(tap_state, check_timings(read_schedule(date)))
        time.sleep(3)


# Insertion point for the script
if __name__ == '__main__':
    main()
