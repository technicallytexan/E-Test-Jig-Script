import serial
__author__ = 'Dustin'

ser = serial.Serial('COM10', 115200, timeout=None, parity=serial.PARITY_NONE, bytesize=serial.EIGHTBITS, stopbits=serial.STOPBITS_ONE, rtscts=0)

while ser.inWaiting():
    pass
print(ser.read(6))

print(ser.write("I\r\n"))

ser.flushInput()
ser.flush()
ser.flushOutput()

while ser.inWaiting():
    pass
print(ser.read(6))
