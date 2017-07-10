import serial
ser = serial.Serial('/dev/ttyACM0', 9600)

while True:
	temp = ser.readline()
	temp = temp.rstrip()
	print(temp)
