import serial
import time

ser = serial.Serial('COM6', 9600)
ser.timeout = 1

while True:
    i = input("input(on/off): ").strip()
    if i == 'done':
        print("finished program")
        break
    ser.write(i.encode())
    time.sleep(0.5)
    print(ser.readline().decode('ascii'))

ser.close()