import datetime
import csv
import os
import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd
# RADIO/SERIAL STUFF HERE


def deconstruct(data):
    data = str(data)
    time = reformat_timestamp(data[:6])
    temp = int(data[6:10]) / 100
    hum = data[-2:]
    return time, temp, hum


def reformat_timestamp(time_str):
    formatted_time = time_str[:2] + ':' + time_str[2:4] + ':' + time_str[-2:]
    return formatted_time


def log_values(log_dir, time, temp, hum):
    log_dir = log_dir + '/'
    date = datetime.datetime.now().strftime("%d-%m-%Y")
    file_name = date + '_log.csv'
    path = log_dir + file_name
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    file_exists = os.path.isfile(path)
    with open(path, 'a') as logCSV:
        headers = ['Time', 'Temperature (C)', 'Humidity (%)']
        log = csv.DictWriter(logCSV, fieldnames=headers)
        if not file_exists:
            log.writeheader()
        log.writerow({'Time': time, 'Temperature (C)': temp, 'Humidity (%)': hum})
    return path, date


def plot_data(csv_path, date):
    df = pd.read_csv(csv_path)
    filename = date + '_graph'
    trace1 = go.Scatter(
        x=df['Time'],
        y=df['Temperature (C)'],
        name='Temperature (°C)',
        line={'shape': 'spline'})
    trace2 = go.Scatter(
        x=df['Time'],
        y=df['Humidity (%)'],
        name='Humidity (%)',
        yaxis='y2',
        line={'shape': 'spline'})
    data = [trace1, trace2]
    layout = go.Layout(
        title='04-02-2018 Temperature & Humidity',
        xaxis=dict(
            title='Time'),
        yaxis=dict(
            title='Temperature (°C)'),
        yaxis2=dict(
            title='Humidity (%)',
            titlefont=dict(color='rgb(148, 103, 189)'),
            tickfont=dict(color='rgb(148, 103, 189)'),
            overlaying='y',
            side='right'))
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=filename, auto_open=False)


if __name__ == '__main__':
    data_package = 170420219050
    timestamp, temperature, humidity = deconstruct(data_package)
    log_file, date_today = log_values('logs', timestamp, temperature, humidity)
    plot_data(log_file, date_today)
