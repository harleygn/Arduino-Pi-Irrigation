# -*- coding: utf-8 -*-

# Import modules
import datetime
import csv
import os
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import serial
import time
import plotly.offline as offline


# Breaks down a 10 digit data package into its three components
def deconstruct(data):
    data = data
    # Extracts the timestamp and converts it into a readable format
    formatted_timestamp = reformat_timestamp(data[:4])
    # Extracts the temperature value and converts it into a decimal value
    temp = int(data[4:8]) / 100
    # Extracts the humidity value
    hum = data[-2:]
    # Returns all three values to be handled by another function
    print('Data package {} deconstructed'.format(data))
    print('Time: {}'.format(formatted_timestamp))
    print('Temperature: {} C'.format(temp))
    print('Humidity: {}%'.format(hum))
    return formatted_timestamp, temp, hum


# Reformats a 4 digit timestamp (HHMM) into a readable format (HH:MM)
def reformat_timestamp(time_str):
    # Slices the timestamp into two parts and inserts a colon
    formatted_time = time_str[:2] + ':' + time_str[2:4]
    return formatted_time


# Write the values to CSV file in labeled by date in a specified directory
def log_values(log_dir, time_val, temp, hum):
    project_root = os.path.dirname(os.path.realpath(__file__))
    # Open up the directory
    log_dir = '{}/{}/'.format(project_root, log_dir)
    # Get today's date in the format DD-MM-YYYY
    date = datetime.datetime.now().strftime('%d-%m-%Y')
    # Builds a filename with the date and relevant filename
    file_name = date + '_log.csv'
    # The path variable is created separately to allow it returned separately
    path = log_dir + file_name
    # Checks if the specified directory is present
    if not os.path.exists(log_dir):
        # If not, it is created
        os.makedirs(log_dir)
        print('Log directory {} created'.format(log_dir))
    # Checks if the log file already exists and sets a flag
    file_exists = os.path.isfile(path)
    # Opens up the log file for appending or creates a new one if it doesn't exist, closes automatically after use
    with open(path, 'a') as logCSV:
        # Defines the column names for the CSV file
        headers = ['Time', 'Temperature (C)', 'Humidity (%)']
        # Creates a CSV object with the previous column names for writing to
        log = csv.DictWriter(logCSV, fieldnames=headers)
        # If, according the the flag, the log file did not previously exist, the column names are added
        if not file_exists:
            log.writeheader()
            print('CSV log file {} created at {}'.format(file_name, log_dir))
        # The writes the log data the relevant columns
        log.writerow({'Time': time_val, 'Temperature (C)': temp, 'Humidity (%)': hum})
    # Returns the path of the log file and the current date
    return project_root, path, date


# Plots the current logs to a time-series chart with a double Y axis, saved to the Plotly API
def plot_data(project_root, csv_path, date):
    chart_dir = project_root + '/interface/charts/'
    # Loads the current CSV log file
    # Raises an error if the file cannot be found
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print('CSV file for {} not found'.format(date))
    # Checks if the chart directory is present
    if not os.path.exists(chart_dir):
        # If not, it is created
        os.makedirs(chart_dir)
        print('Chart directory created at {}'.format(chart_dir))
    # Formats a matching filename for the chart
    filename = '{}/interface/charts/{}_chart'.format(project_root, date)
    # Specifies the parameters for the first line plot (Temperature)
    trace1 = go.Scatter(
        # Loads the time values as the X axis
        x=df['Time'],
        # Loads the temperature values as the Y axis
        y=df['Temperature (C)'],
        # Names the plot, shown in the legend
        name='Temperature (°C)',
        # Specifies the shape of the plot, spline meaning curved
        line={'shape': 'spline'})
    # Specifies the parameters for the second line plot (Humidity)
    trace2 = go.Scatter(
        # Loads the time values as the X axis
        x=df['Time'],
        # Loads the humidity values as the Y axis
        y=df['Humidity (%)'],
        # Names the plot, shown in the legend
        name='Humidity (%)',
        # Indicates that this is a secondary Y axis
        yaxis='y2',
        # Specifies the shape of the plot, spline meaning curved
        line={'shape': 'spline'})
    # Combines the two trace objects
    data = [trace1, trace2]
    # Specifies the parameters for the chart figure
    layout = go.Layout(
        # Creates a chart title for today's data
        title=(date + ' Temperature & Humidity'),
        # Specifies the X axis title
        xaxis=dict(title='Time'),
        # Specifies the first Y axis title (Temperature)
        yaxis=dict(title='Temperature (°C)'),
        # Specifies the parameters for the second Y axis (Humidity)
        yaxis2=dict(
            # Specifies the Y axis title
            title='Humidity (%)',
            # Indicates which trace is to lie on top of the other
            overlaying='y',
            # This Y axis will be displayed on the right-hand side
            side='right'))
    # Builds the figure object with the previously defined data and layout
    fig = go.Figure(data=data, layout=layout)
    # Plots the figure object to the Plotly API with the given filename
    offline.plot(fig, filename=(filename + '.html'), auto_open=False)
    py.plot(fig, filename='test', auto_open=False)
    print('Chart saved using Plotly to ' + chart_dir)


# Requests a data package via serial or input
def request_data():
    # Sets boolean flag for package validity
    package_valid = False
    # Obtains serial connection information
    serial_conn = check_connection()
    # While the package is invalid:
    while not package_valid:
        # If no serial connection can be made
        if not serial_conn:
            # Defaults to manual input (for testing)
            package = input('Enter sample data: ')
        # If a serial connection can be made
        else:
            # Sets boolean flag for call/response
            connection = False
            # Disables Data Terminal Ready to allow scripted communication
            time.sleep(1)
            serial_conn.setDTR(0)
            time.sleep(1)
            # While there is no response
            while not connection:
                # Send the 'call' signal
                serial_conn.write(bytes('call\n', 'utf-8'))
                # Reads the line in the buffer, decodes and removes newlines
                # If the message is a valid 'response'
                if serial_conn.readline().decode().strip() == 'response':
                    print('Valid response received, requesting data')
                    # Sets the flag to indicate a valid call/response
                    connection = True
                else:
                    print('Invalid response, reattempting call')
            # With a healthy connection, the data request is sent in UTF-8
            serial_conn.write(bytes('datarequest\n', 'utf-8'))
            # Decodes the package from binary and removes newlines
            package = serial_conn.readline().decode().strip()
            print('Data package {} received'.format(package))
        # Checks that the package is in a valid format
        package_valid = validate_data(package)
    return package


# Checks that the package is in the correct format
def validate_data(package):
    # Checks that the package is a string
    valid = isinstance(package, str)
    # Checks that the package is 10 digits long
    if len(package) != 10:
        valid = False
    # Checks that the first 2 digits (hours) is below 24
    elif int(package[:2]) > 23:
        valid = False
    # Checks that the second 2 digits (minutes) is below 60
    elif int(package[2:4]) > 59:
        valid = False
    # Checks that the digits 4-8 (temperature) are realistic (below 40)
    elif int(package[4:8]) > 4000:
        valid = False
    # Checks that the last 2 digits (humidity) is within 100%
    elif int(package[-2:]) >= 100:
        valid = False
    # If any checks fail:
    if not valid:
        # The data package is marked as invalid
        print('Invalid data package or unknown command')
        return False
    # Otherwise the data package is accepted
    else:
        print('Data package {} is valid'.format(package))
        return True


# Attempts to open serial port, defaults to manual input
def check_connection():
    # Attempts to open the first possible serial port
    try:
        serial_conn = serial.Serial('/dev/ttyACM0', 9600)
    # If this fails to open:
    except serial.serialutil.SerialException:
        # The other possible port is attempted
        try:
            serial_conn = serial.Serial('/dev/ttyUSB0', 9600)
        # If this fails also, no serial connection is made
        except serial.serialutil.SerialException:
            # Indicates that manual input must be used
            serial_conn = False
    return serial_conn


# Main execution of the script
def main():
    # Gets data package
    data_package = request_data()
    # Gets individual data values
    timestamp, temperature, humidity = deconstruct(data_package)
    # Saves data to current CSV
    root, log_file, date_today = log_values('logs', timestamp, temperature, humidity)
    # Plots data to a chart
    plot_data(root, log_file, date_today)


# Insertion point for the script
if __name__ == '__main__':
    main()
