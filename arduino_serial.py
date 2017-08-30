
import serial
import time

#def createBlankCsv(date):
#	newCsv = date + "temp_reading.csv"
#	path = newCsv
#	with open(newCsv, "a+") as currentCsv:
#		currentCsv.write("key, time, temp\n")

with serial.Serial("/dev/ttyACM0", 9600) as ser:
	connect = False
	while connect == False:
		ser.write(bytes(1, "ascii")
		if ser.readline().decode().strip() == 1:
			connect = True
	while True:
		command = input("Enter command: ")
		ser.write(bytes(command, "ascii"))
		time.sleep(3)
		temp = ser.readline().decode().strip()
		print(temp)
