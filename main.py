from datetime import datetime, timedelta
from adafruit import *
from timer_interrupt import *
import threading
import fsm
import time
import random
import json
import os
from controller import *
# from rs485 import *


state = {
    "next-cycle": 13,
    "mixer1": 4,
    "mixer2": 2,
    "mixer3": 3,
    "pump-in": 2,
    "pump-out": 2,
    "active": 1,
    "start-time": "12:30",
}

new_state = {
    "next-cycle": 1,
    "mixer1": 4,
    "mixer2": 2,
    "mixer3": 3,
    "pump-in": 2,
    "pump-out": 2,
    "active": 1,
    "start-time": "10:25",
}

# address_feed = {
#     "mixer1": 2,
#     "mixer2": 3,
#     "mixer3": 4,
#     "pump-in": 5,
#     "pump-out": 6
# }

sched_active = []



def data_callback(feed_id, payload):
    key = feed_id.replace("sys.", "")

    if key in state:

        # state[key] = payload
        #TODO: control physical.
        # control.setActuators(address_feed[key], payload)
        print(f"Updated {key} to {payload}")
        time.sleep(1)

    else:
        print(f"No handler found for feed: {feed_id}")


def add_seconds_to_time(time_str, seconds):
    time_format = "%H:%M"
    time_obj = datetime.strptime(time_str, time_format)
    delta = timedelta(seconds=seconds)
    new_time_obj = time_obj + delta
    return new_time_obj.strftime(time_format)


def calculate_stop_time(schedule):
    schedule_time = 0
    for key in schedule:
        if key != 'active' and key != 'next-cycle' and key != 'start-time':
            schedule_time += schedule[key]
    stop_time = add_seconds_to_time(schedule["start-time"], schedule_time * schedule["next-cycle"])
    schedule["stop-time"] = stop_time


# adafruit_client = Adafruit_MQTT()
client.setRecvCallBack(data_callback)


start_sched = fsm.FarmScheduler()
control = Physic()
os.system("clear")
while True:

    if state["active"] == 1:
        calculate_stop_time(state)
        print(state)
        sched_active.append(state.copy())
        print("Activated new schedule!")
        print(state)
        state["active"] = 0  # Reset the active flag


    for schedule in sched_active:
        start_sched.add_schedule(schedule)
        start_sched.run()
        sched_active.remove(schedule)

    # time.sleep(1)