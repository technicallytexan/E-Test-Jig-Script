import serial
import serial.tools.list_ports_windows
import os
import re
import time

__author__ = 'Dustin'

file_in = "NONE"
cwd_dir_files = os.listdir(os.getcwd())
# Get filename for binary
for file in cwd_dir_files:
    if re.search("(.bin|.hex)$", file):
        file_in = file
        break
if file_in == "NONE":
    print("Binary file not found.  Please ensure that .bin file is in the same directory as this script.")
    exit(1)

ST_LINK_FOUND = 0
for file in cwd_dir_files:
    if re.search("(ST-LINK[\w]*.exe)", file):
        ST_LINK_FOUND = 1
if ST_LINK_FOUND == 0:
    print("ST-LINK Command Line Programmer Not Found.")
    exit(1)

# Find COM port
COM_ports = serial.tools.list_ports_windows.comports()
# Search for correct COM port and open it
for port in COM_ports:
    if re.search("DNDKSY0A", port.serial_number):
        ser = serial.Serial('COM10', 115200, timeout=None, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, rtscts=0)
        print("SERIAL COM PORT CONNECTED")
        break
ser.flushInput()
ser.flush()
ser.flushOutput()
while ser.inWaiting():
    pass
print(ser.read(6))
ser.flushInput()
ser.flush()
ser.flushOutput()
inbuffer = []
# Send initialize command
print(ser.write("I\r\n"))
print("BEGINNING ENERTION PROGRAMMING SEQUENCE")
ser.flushInput()
ser.flush()
ser.flushOutput()
# Wait for response
while ser.inWaiting():
    pass
inbuffer = ser.read(6)
#   ######DEBUGGING#####
print(inbuffer)
#   ######DEBUGGING#####
ser.flushInput()
ser.flush()
ser.flushOutput()
inbuffer = []
# Send command to open programming lines for board 1
print("PROGRAMMING BOARD 1")
time.sleep(1)
print(ser.write("I\r\n"))
ser.flushInput()
ser.flush()
ser.flushOutput()

# Wait for response
while ser.inWaiting():
    pass
inbuffer = ser.read(6)
#   ######DEBUGGING#####
print(inbuffer)
#   ######DEBUGGING#####
ser.flushInput()
ser.flush()
ser.flushOutput()
# Program board 1
os.system("".join(["ST-LINK_CLI.exe -c SWD SWCLK=9 -P \"", file_in, "\" 0x08000000 -V"]))
#os.system("TASKKILL /F /IM ST-LINK_CLI.exe")
print(ser.write("PC\r\n"))
ser.flushInput()
ser.flush()
ser.flushOutput()
# Wait for response
while ser.inWaiting():
    pass
inbuffer = ser.read(6)
#   ######DEBUGGING#####
print(inbuffer)
#   ######DEBUGGING#####
ser.flushInput()
ser.flush()
ser.flushOutput()
if re.search("(PA)", inbuffer):
    print("BOARD 1 TESTING PASSED")
else:
    print("BOARD 1 TESTING FAILED")
print("CONTINUING TO NEXT BOARD")