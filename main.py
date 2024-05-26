from adafruit import *
from timer_interrupt import *
import threading
import fsm
import time
import random
import json
import os
from controller import *
from datetime import datetime
import requests
import json

state = {
    "next-cycle": 1,
    "mixer1": 5,
    "mixer2": 4,
    "mixer3": 3,
    "pump-in": 2,
    "pump-out": 2,
    "active": 0,
    "startTime": "19:48",
}

def fetch_data(url, output_file):
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        with open(output_file, 'w') as file:
            json.dump(data, file)

        print("Data saved to", output_file)
    else:
        print("Failed to fetch data from", url, ". Status code:", response.status_code)

def get_scheduler():
    with open('./data/scheduler.json', 'r') as file:
        data = file.read()
    return json.loads(data)

def get_area():
    with open('./data/area-selector.json', 'r') as file:
        data = file.read()
    return json.loads(data)

def data_callback(feed_id, payload):
    key = feed_id.replace("sys.", "")
    # print(f"{key} updated: {payload}")
    # if key in state:
    #     # state[key] = payload
    #     #TODO: control physical.
    #     # control.setActuators(address_feed[key], payload)
    #     # print(f"Updated {key} to {payload}")
    #     # time.sleep(1)
    # else:
    #     print(f"No handler found for feed: {feed_id}")

client.setRecvCallBack(data_callback)

sched_active = [state]
start_sched = fsm.FarmScheduler()
control = Physic()
counter = 30
control.selectArea(get_area())

# os.system("clear")

while True:
    counter -= 1
    if counter <= 0:
        control.readSensors("soil_temperature")
        control.readSensors("soil_moisture")

    if not sched_active:
        current_time = datetime.now().strftime('%H:%M')
        if current_time == state["startTime"] and state["active"] == True:
            state["onSchedule"] == 1
            sched_active.append(state.copy())
            print("Activated new schedule!")

    if sched_active:
        start_sched.add_schedule(sched_active[0])
        print("SCHEDULE PROCESSING: ", sched_active[0])
        start_sched.run()
        sched_active.remove(sched_active[0])