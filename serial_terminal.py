import serial
import serial.tools.list_ports as ports
from datetime import datetime
import re

def write_csv(filename, line):
    with open(filename, 'a',newline = '\n') as f:
        f.write(f"{str(line)}\n")

def extract_data(filename, line):
    if re.search('DataApollo', line):
        data = line.split()[5:13]
        if not (int(data[1]) == 0 or int(data[3]) == 0):
            data = " ".join(data)
            write_csv(filename, data)


log_filename  = datetime.now().strftime('monitorlog_%Y-%m-%d.txt')       
com_ports = list(ports.comports())  # create a list of com ['COM1','COM2']
for i in com_ports:
    print(i.device)  # returns 'COMx'

ser = serial.Serial(
    port='COM11',\
    baudrate=1000000,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
if not ser.isOpen():
    ser.open()

print("connected to: " + ser.portstr)
count=1

while True:
    line = ser.readline()
    if line:
        line = str(line)
        print(line)
        extract_data(log_filename, line)

ser.close()

