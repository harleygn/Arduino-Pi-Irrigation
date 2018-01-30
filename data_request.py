import datetime
import csv
import os
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


if __name__ == '__main__':
    data_package = 170420219050
    timestamp, temperature, humidity = deconstruct(data_package)
    log_values('logs/', timestamp, temperature, humidity)
