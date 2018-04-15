import datetime
import serial
import time

# Serial Parameters
port = '/dev/ttyUSB0'
baud = 921600
dataBits = 8
parity = 'N'
stopBits = 1

# Log File Parameters
# filename = "/home/pi/DataLogging/logs/" + str(datetime.datetime.now().date()) + ".txt"
bufferSize = -1


# Reads serial data byte by byte and formats to space separated CAN.
def readCAN():
    message = ''

    # Message ID
    message += ser.read(3).decode('utf-8')

    # Length
    length = ser.read().decode('utf-8')
    message += ' ' + length

    # Bytes
    try:
        for _ in range(int(length)):
            message += ' '
            message += ser.read(2).decode('utf-8')
    except ValueError:
        message = 'ERROR'

    # Cleanup
    while True:
        if ser.read().decode('utf-8') == 't':  # Messages are terminated with 't'
            return message


if __name__ == "__main__":
    i = 0
    filename = "/home/pi/DataLogging/logs/log" + str(i) + ".txt"
    flag = True
    while flag:
        try:
            with open(filename, 'r') as fp:
                i += 1
                filename = "/home/pi/DataLogging/logs/log" + str(i) + ".txt"
        except FileNotFoundError:
            flag = False
    with open(filename, 'a', bufferSize) as fp:
        while True:
            try:
                with serial.Serial(port, baud, dataBits, parity, stopBits) as ser:
                    ser.write(bytes([0x0D, 0x53, 0x36, 0x0D]))  # Sets CAN speed to 500K
                    ser.write(bytes([0x0D, 0x4F, 0x0D]))  # Opens the CAN-Bus
                    time.sleep(1)
                    while True:
                        clock = str(datetime.datetime.now().time()).split('.')
                        line = readCAN()
                        try:
                            fp.write(clock[0] + ' ' + clock[1] + ' ' + line + '\n')
                            print(clock[0] + ' ' + clock[1] + ' ' + line)
                        except IndexError:
                            continue
            except serial.serialutil.SerialException:
                time.sleep(1)
