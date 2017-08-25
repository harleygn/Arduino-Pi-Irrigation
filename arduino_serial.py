import serial

def createBlankCsv(date):
	path = date + "temp_reading.csv"
	with open(path, "a+") as currentCsv:
		print("key, date, time, temp\n")
	
ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
	temp = ser.readline()
	temp = temp.decode().strip()
	print(temp)
