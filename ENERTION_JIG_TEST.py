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
    print("BINARY FILE NOT FOUND")
    exit(1)

ST_LINK_FOUND = 0
for file in cwd_dir_files:
    if re.search("(ST-LINK[\w]*.exe)", file):
        ST_LINK_FOUND = 1
if ST_LINK_FOUND == 0:
    print("ST-LINK COMMAND LINE INTERFACE NOT FOUND")
    exit(1)

# Find COM port
COM_ports = serial.tools.list_ports_windows.comports()
# Search for correct COM port and open it
for port in COM_ports:
    if re.search("DNDKSY0A", port.serial_number):    # TODO: This needs to be changed to another serial port parameter
        ser = serial.Serial('COM10', 115200, timeout=None, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, rtscts=0)
        print("SERIAL COM PORT CONNECTED")
        break

# Commence the jigglin'
print("BEGINNING ENERTION PROGRAMMING SEQUENCE")
while True:
    print("PRESS ENTER WHEN PANEL IS INSERTED INTO THE JIG OR EXIT THE PROGRAM IF FINISHED")
    raw_input("")
    for i in range(1,10):
        ser.flushInput()
        ser.flushOutput()
# Send initialize command
        ser.write("INIT\r\n")
        ser.flushOutput()
# Wait for response
        while ser.inWaiting():
            pass
        inbuffer = ser.read(6)
        ser.flushInput()
# Send command to open programming lines for board
        time.sleep(1)
        ser.write("PB\r\n")
        ser.flushOutput()
# Wait for response
        while ser.inWaiting():
            pass
        inbuffer = ser.read(6)
        ser.flushInput()
# Program board
        print("".join(["PROGRAMMING BOARD ", i, "..."])
        os.system("".join(["ST-LINK_CLI.exe -c SWD SWCLK=9 -P \"", file_in, "\" 0x08000000 -V"]))
#os.system("TASKKILL /F /IM ST-LINK_CLI.exe")    # Not needed apparently :)
        ser.write("PC\r\n")
        print("".join(["TESTING BOARD ", i, "... "], end="")
        ser.flushOutput()
# Wait for response
        while ser.inWaiting():
            pass
        inbuffer = ser.read(6)
        print("COMPLETE")
        ser.flushInput()
        if re.search("PA", inbuffer):
            results.append("PASS")
        else:
            results.append("FAIL")
    print("TESTING RESULTS:")
    i = 1
    for result in results:
        print("".join(["Board ", i, " Result: ", result]))
        i += 1
