import serial, time

arduino = serial.Serial('', )

time.sleep(2)
String = arduino.readline()
print(String)