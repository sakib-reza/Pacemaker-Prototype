import serial
import time
import struct
ser = serial.Serial(
    port='COM8',\
    baudrate=115200)

print("connected to: " + ser.portstr)
count=1
start_time = time.time()
temp_time = 0
line = []
while True:
    for c in ser.read():
        line.append(chr(c))
        if c == 1:
            print(line)
            print(int(time.time() - start_time))
            line = []
            break
        '''elif c == 2:
            print(sum(line[9:])/9)
            
            line = []
            break'''

ser.close()
