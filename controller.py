import sys
import time
import serial.tools.list_ports
# from main import adafruit_client
import random
from adafruit import client
import re
MIXER1 = 2
MIXER2 = 3
MIXER3 = 4
PUMPIN = 5
PUMPOUT = 6
AREA1 = 7
AREA2 = 8
AREA3 = 9

pub_feed = ["sys.temperature", "sys.humidity", "sys.mixer1", 
                        "sys.mixer2", 
                        "sys.mixer3",
                        "sys.pump-in",
                        "sys.pump-out",
                        "sys.area1",
                        "sys.area2",
                        "sys.area3",
                        "sys.next-cycle",
                        "sys.area2",
                        "sys.active"]

class Physic:
    def __init__(self):        
        self.RS485_actuators_format = {
            'relay1_ON': [1, 6, 0, 0, 0, 255, 201, 138],
             'relay1_OFF': [1, 6, 0, 0, 0, 0, 137, 202],
             'relay2_ON': [2, 6, 0, 0, 0, 255, 201, 185],
             'relay2_OFF': [2, 6, 0, 0, 0, 0, 137, 249],
             'relay3_ON': [3, 6, 0, 0, 0, 255, 200, 104],
             'relay3_OFF': [3, 6, 0, 0, 0, 0, 136, 40],
             'relay4_ON': [4, 6, 0, 0, 0, 255, 201, 223],
             'relay4_OFF': [4, 6, 0, 0, 0, 0, 137, 159],
             'relay5_ON': [5, 6, 0, 0, 0, 255, 200, 14],
             'relay5_OFF': [5, 6, 0, 0, 0, 0, 136, 78],
             'relay6_ON': [6, 6, 0, 0, 0, 255, 200, 61],
             'relay6_OFF': [6, 6, 0, 0, 0, 0, 136, 125],
             'relay7_ON': [7, 6, 0, 0, 0, 255, 201, 236],
             'relay7_OFF': [7, 6, 0, 0, 0, 0, 137, 172],
             'relay8_ON': [8, 6, 0, 0, 0, 255, 201, 19],
             'relay8_OFF': [8, 6, 0, 0, 0, 0, 137, 83]
        }

        self.RS485_sensors_format = {
                "soil_temperature" : [1, 3, 0, 6, 0, 1, 100, 11],
                "soil_moisture" : [1, 3, 0, 7, 0, 1, 53, 203]
            }

        self.portname = self.getPort(1)  
        try:
            self.ser = serial.Serial(port=self.portname, baudrate=9600)
            print("Open successfully port: ", self.portname)
        except:
            print("Exception: Can not open the port", self.portname)
            sys.exit() 

    def getPort(self, state):
        """Searches for and returns the first available USB serial port."""
        ports = serial.tools.list_ports.comports()
        commPort = "None"
        for i in range(len(ports)):
            port = ports[i]
            strPort = str(port)
            if "USB" in strPort:  # Checks if the port description contains 'USB'
                splitPort = strPort.split(" ")
                commPort = splitPort[0]  # Assumes the first part is the port name
        # return commPort
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

    def serial_read_data(self):
        bytesToRead = self.ser.inWaiting() 
        if bytesToRead > 0:
            out = self.ser.read(bytesToRead)
            data_array = [b for b in out]  # Converts the bytes to a list for easier processing
            print(data_array)
            if len(data_array) >= 7:
                array_size = len(data_array)
                value = data_array[array_size - 4] * 256 + data_array[array_size - 3]
                return value
            else:
                return -1
        return 0

    def setActuators(self, ID, state):
        """Sends a command to set the state of an actuator (relay) based on its ID."""
        command_key = f'relay{ID}_{"ON" if state else "OFF"}'
        # command_data = self.RS485_actuators_format.get(command_key)
        client.publish(pub_feed[ID], state)
        # self.ser.write(command_data)  

    def readSensors(self, sensorName):
        """Sends a command to read data from a specified sensor."""
        # self.serial_read_data()
        # command_data = self.RS485_sensors_format.get(sensorName)
        if sensorName == "soil_temperature":
            temperature = random.randint(0, 100)
            print("TEMP", temperature)
            client.publish(pub_feed[0], temperature)
        elif sensorName == "soil_moisture":
            moisture = random.randint(0, 100)
            client.publish(pub_feed[1], moisture)
        # self.ser.write(command_data) 
        time.sleep(1)  
        # return self.serial_read_data()  

    def selectArea(self, area_state):
        self.setActuators(7, area_state["area1"])
        self.setActuators(8, area_state["area2"])
        self.setActuators(9, area_state["area3"])
        print("AREA SELECTED")
        
        
        

# if __name__ == '__main__':
#     physic = Physic(True)  # Initialize the class with debug mode enabled

#     # Test sequence for actuators and sensors
#     while True:
#         # Testing actuator control
#         print("Testing Actuators with ID 2: ")
#         print("Turn on relay_2: ")
#         physic.setActuators(2, True)  # Turn on relay 2
#         time.sleep(2)
#         print("Turn off relay_2: ")
#         physic.setActuators(2, False)  # Turn off relay 2
#         time.sleep(2)

#         # Testing sensor reading
#         # print("\nTesting reading sensor: ")
#         # print("Soil temperature: ", physic.readSensors(TEMP))  # Read and print soil temperature
#         # time.sleep(1)
#         # print("Soil moisture: ", physic.readSensors(MOISTURE))  # Read and print soil moisture
#         # time.sleep(5)
