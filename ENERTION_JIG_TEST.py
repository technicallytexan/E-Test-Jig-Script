import serial
import serial.tools.list_ports_windows
import os
import re
import time

__author__ = 'Dustin'

print("ENERTION PROGRAMMING AND TESTING")

file_in = "NONE"
cwd_dir_files = os.listdir(os.getcwd())
# Get filename for binary
for file in cwd_dir_files:
    if re.search("(.bin|.hex)$", file):
        file_in = file
        break
if file_in == "NONE":
    print("ERROR: BINARY FILE NOT FOUND")
    exit(1)

ST_LINK_FOUND = 0
for file in cwd_dir_files:
    if re.search("(ST-LINK[\w]*.exe)", file):
        ST_LINK_FOUND = 1
if ST_LINK_FOUND == 0:
    print("ERROR: ST-LINK COMMAND LINE INTERFACE NOT FOUND")
    exit(1)

# Find COM port
port_found = 0
initial_count = time.clock()
print("SEARCHING FOR JIG...")
while port_found == 0:
    COM_ports = serial.tools.list_ports_windows.comports()
# Search for correct COM port and open it
    for port in COM_ports:
        if re.search("!PRODUCT ID HERE!", port.pid):    
            ser = serial.Serial(port, 115200, timeout=None, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS, 
                                stopbits=serial.STOPBITS_ONE, rtscts=0)
            print("SERIAL COM PORT CONNECTED")
            port_found = 1
            break
    if (time.clock() - initial_count) >= 30:
        print("ERROR: TIMED OUT - CANNOT FIND JIG")
        exit(1)

# Commence the jigglin'
print("BEGINNING ENERTION PROGRAMMING SEQUENCE")
while True:
    print("PRESS ENTER WHEN PANEL IS INSERTED INTO THE JIG")
    print("TYPE \"EXIT\" TO CLOSE THE PROGRAM")
    op_input = input("")
    if re.search("^[Ee][Xx][Ii][Tt]$", op_input):
        exit(0)
    if re.search("DB87", op_input):
        break
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
        # ser.write("".join(["PB", i, "\r\n"]))
        ser.flushOutput()
# Wait for response
        while ser.inWaiting():
            pass
        inbuffer = ser.read(6)
        ser.flushInput()
# Program board
        print("".join(["PROGRAMMING BOARD ", i, "..."])
        os.system("".join(["ST-LINK_CLI.exe -c SWD SWCLK=9 -P \"", file_in, "\" 0x08000000 -V"]))
        ser.write("PC\r\n")
        print("".join(["TESTING BOARD ", i, "... "], end="")
        ser.flushOutput()
# Wait for response
        while ser.inWaiting():
            pass
        inbuffer = ser.read(6)
        print("COMPLETE")
        ser.flushInput()
# Test if pass or fail
        if re.search("PA", inbuffer):
            results.append("PASS")
        else:
            results.append("FAIL")
    print("TESTING RESULTS:")
    i = 1
    for result in results:
        print("".join(["BOARD ", i, " RESULT: ", result]))
        i += 1
    del results[:]

while True:
    print("###########################################")
    print("###########################################")
    print("## SUPER DUPER TOP SECRET DEBUGGING MENU ##")
    print("## OPTIONS:                              ##")
    print("##    1:  PROGRAM AND TEST BOARD 1       ##")
    print("##    2:  PROGRAM AND TEST BOARD 2       ##")
    print("##    3:  PROGRAM AND TEST BOARD 3       ##")
    print("##    4:  PROGRAM AND TEST BOARD 4       ##")
    print("##    5:  PROGRAM AND TEST BOARD 5       ##")
    print("##    6:  PROGRAM AND TEST BOARD 6       ##")
    print("##    7:  PROGRAM AND TEST BOARD 7       ##")
    print("##    8:  PROGRAM AND TEST BOARD 8       ##")
    print("##    9:  PROGRAM AND TEST BOARD 9       ##")
    print("##   10:  PROGRAM AND TEST BOARD 10      ##")
    print("## EXIT:  EXIT PROGRAM                   ##")
    print("###########################################")
    print("###########################################")
    op_input = input(">> ")
    
    if re.search("^[Ee][Xx][Ii][Tt]$", op_input):
        exit(0)
    elif re.search("^[1-9]0?$", op_input):
        print("BEGINNING ENERTION PROGRAMMING SEQUENCE")
        print("PRESS ENTER WHEN PANEL IS INSERTED INTO THE JIG OR EXIT THE PROGRAM IF FINISHED")
        op_input = input("")
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
        ser.write("".join(["PB", op_input, "\r\n"]))
        ser.flushOutput()
# Wait for response
        while ser.inWaiting():
            pass
        inbuffer = ser.read(6)
           ser.flushInput()
# Program board
        print("".join(["PROGRAMMING BOARD ", op_input, "..."])
        os.system("".join(["ST-LINK_CLI.exe -c SWD SWCLK=9 -P \"", file_in, "\" 0x08000000 -V"]))
#os.system("TASKKILL /F /IM ST-LINK_CLI.exe")    # Not needed apparently :)
        ser.write("PC\r\n")
        print("".join(["TESTING BOARD ", op_input, "... "], end="")
        ser.flushOutput()
# Wait for response
        while ser.inWaiting():
            pass
        inbuffer = ser.read(6)
        print("COMPLETE")
        ser.flushInput()
# Test if pass or fail
        if re.search("PA", inbuffer):
            results.append("PASS")
        else:
            results.append("FAIL")
        print("TESTING RESULTS:")
        i = 1
        for result in results:
            print("".join(["BOARD ", op_input, " RESULT: ", result]))
            i += 1
        del results[:]
    else:
        print("WRONG COMMAND ENTERED.  TRY AGAIN.")

    
