from adafruit import *
from timer_interrupt import *
import threading
import fsm
import time
import random
import json
from controller import *
# from rs485 import *


state = {
    "next-cycle": 1,
    "mixer1": 4,
    "mixer2": 12,
    "mixer3": 12,
    "pump-in": 2,
    "pump-out": 2,
    "active": 1,
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
        

# adafruit_client = Adafruit_MQTT()
client.setRecvCallBack(data_callback)


start_sched = fsm.FarmScheduler()
control = Physic()
while True:

    if state["active"] == 1:
        sched_active.append(state.copy())
        print("Activated new schedule!")
        print(state)
        state["active"] = 0  # Reset the active flag


    for schedule in sched_active:
        start_sched.add_schedule(schedule)
        start_sched.run()
        sched_active.remove(schedule)

    # time.sleep(1)