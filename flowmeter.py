import serial

ser = serial.serial('COM4', 19200)
data = ser.readline()