# -*- coding: utf-8 -*-

# Import modules for handling date/time objects, CSV files, OS commands and graphs
import datetime
import csv
import os
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
import serial
import time


# Breaks down a 10 digit data package into its three components
def deconstruct(data):
    data = data
    # Extracts the timestamp and converts it into a readable format
    time = reformat_timestamp(data[:4])
    # Extracts the temperature value and converts it into a decimal value
    temp = int(data[4:8]) / 100
    # Extracts the humidity value
    hum = data[-2:]
    # Returns all three values to be handled by another function
    return time, temp, hum


# Reformats a 4 digit timestamp (HHMM) into a readable format (HH:MM)
def reformat_timestamp(time_str):
    # Slices the timestamp into two parts and inserts a colon
    formatted_time = time_str[:2] + ':' + time_str[2:4]
    return formatted_time


# Write the values to CSV file in labeled by date in a specified directory
def log_values(log_dir, time, temp, hum):
    # Open up the directory
    log_dir = '/home/pi/Arduino-Pi-Irrigation/' + log_dir + '/'
    # Get today's date in the format DD-MM-YYYY
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    # Builds a filename with the date and relevant filename
    file_name = date + '_log.csv'
    # The path variable is created separately to allow it returned separately
    path = log_dir + file_name
    # Checks if the specified directory is present
    if not os.path.exists(log_dir):
        # If not, it is created
        os.makedirs(log_dir)
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
        # The writes the log data the relevant columns
        log.writerow({'Time': time, 'Temperature (C)': temp, 'Humidity (%)': hum})
    # Returns the path of the log file and the current date
    return path, date


# Plots the current logs to a time-series graph with a double Y axis, saved to the Plotly API
def plot_data(csv_path, date):
    # Loads the current CSV log file
    df = pd.read_csv(csv_path)
    # Creates a matching filename for the graph
    filename = date + '_graph'
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
    # Specifies the parameters for the graph figure
    layout = go.Layout(
        # Creates a graph title for today's data
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
    py.plot(fig, filename=filename, auto_open=False)
    print('Graphed to Plotly')


# Sends the request for the data package
def request_data_test():
    package = input('Enter sample data: ')
    return package


def request_data_serial(serial):
    time.sleep(1)
    serial.setDTR(0)
    time.sleep(1)
    serial.write(bytes('datarequest\n', 'utf-8'))
    package = serial.readline().decode().strip()
    return package


# Insertion point for the script
if __name__ == '__main__':
    data_package = request_data_test()
    # ser = serial.Serial('/dev/ttyACM0', 9600)
    # data_package = request_data_serial(ser)
    timestamp, temperature, humidity = deconstruct(data_package)
    log_file, date_today = log_values('logs', timestamp, temperature, humidity)
    plot_data(log_file, date_today)
