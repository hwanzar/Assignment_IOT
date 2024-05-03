print("Sensors and Actuators")
import re
import time
import serial.tools.list_ports

def getPort(state):
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB" in strPort:
            splitPort = strPort.split(" ")
            commPort = (splitPort[0])
    # return commPort
    # return "/dev/ttyUSB1"
    with open("ports.txt", "r") as file:
        output = file.read()
    matches = re.findall(r'PTY is (\S+)', output)
    if len(matches) == 2:
        pty1, pty2 = matches
        
    if state == 1:
        print(pty1)
        return pty1
    else: 
        print(pty2)
        return pty2

portName = getPort(1)
# print(portName)



try:
    ser = serial.Serial(port=portName, baudrate=9600)
    print("Open successfully")
except:
    print("Can not open the port")

def processData(client, data):
    data = data.replace("[", "")
    data = data.replace("]", "")
    splitData = data.split(",")
    print("HELO")
    print(splitData)
    if splitData[1] == "T":
        client.publish("sys.temperature", splitData[5])
    # if splitData[1] == "H":
    #     client.publish("humidity1", splitData[2])
    # if splitData[1] == "L":
    #     client.publish("light1", splitData[2])
    # if splitData[1] == "A":
    #     client.publish("button1", splitData[2])
    # if splitData[1] == "B":
    #     client.publish("button2", splitData[2])
mess = ""
def serial_read_data(client):
    bytesToRead = ser.inWaiting()
    if (bytesToRead > 0):
        print("CAN WRITE")
        global mess
        mess = mess + ser.read(bytesToRead).decode("UTF-8")
        # print(ser.read(bytesToRead).decode("UTF-8"))
        print(mess)
        while ("[" in mess) and ("]" in mess):
            start = mess.find("[")
            end = mess.find("]")
            processData(client, mess[start:end + 1])
            if (end == len(mess)):
                mess = ""
            else:
                mess = mess[end+1:]


'''
id , function, data[2:5], crc[6:7]
mixer 234 (available)

function: 
    6 : wr
    3 : rd

data:
    0, 0, 0, 255 -> ON
    0, 0, 0, 0 -> OFF

crc: 
    0, 6, 0, 0, 0, 255 -> hexMODBUS -> 5BC8 -> C8 5B -> 200 91
    ([0, 6, 0, 0, 0, 255]) = [200, 91]


'''

# relay1_ON  = [0, 6, 0, 0, 0, 255, 200, 91]
# relay1_OFF = [0, 6, 0, 0, 0, 0, 136, 27]

# def setDevice1(state):
#     if state == True:
#         ser.write(relay1_ON)
#     else:
#         ser.write(relay1_OFF)
#     time.sleep(1)
#     print(serial_read_data(ser))

# while True:
#      setDevice1(True)
#      print(True)
#      time.sleep(2)
#      setDevice1(False)
#      time.sleep(2)


# soil_temperature =[1, 3, 0, 6, 0, 1, 100, 11]
# def readTemperature():
#     serial_read_data(ser)
#     ser.write(soil_temperature)
#     time.sleep(1)
#     return serial_read_data(ser)

# soil_moisture = [1, 3, 0, 7, 0, 1, 53, 203]
# def readMoisture():
#     serial_read_data(ser)
#     ser.write(soil_moisture)
#     time.sleep(1)
#     return serial_read_data(ser)

# while True:
#     print("TEST SENSOR")
#     print(readMoisture())
#     time.sleep(1)
#     print(readTemperature())
#     time.sleep(1)