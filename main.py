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
from dotenv import load_dotenv

load_dotenv()

area_api_url = os.getenv("AREA_API_URL")
area_selector = {
    "area1": "",
    "area2": "",
    "area3": "",
}

def fetch_area_selector():
    global area_selector, area_api_url

    while(True):
        response = requests.get(area_api_url + "sys.area1")
        area_selector["area1"] = response.json()["last_value"]

        response = requests.get(area_api_url + "sys.area2")
        area_selector["area2"] = response.json()["last_value"]

        response = requests.get(area_api_url + "sys.area3")
        area_selector["area3"] = response.json()["last_value"]

        time.sleep(1)


sched_api_url = os.getenv("SCHEDULE_API_URL")
sched_dict = {}

def fetch_scheduler():
    global sched_api_url, sched_dict
    while True:
        response = requests.get(sched_api_url)

        if response.status_code == 200:
            data = response.json()

            current_time = datetime.utcnow()

            for item in data:
                item_id = item.get('_id')
                item_start_time = item.get('startTime')

                if item_id is not None and item_start_time is not None:
                    start_time = datetime.strptime(item_start_time, "%Y-%m-%dT%H:%M:%S.%fZ")
                    if start_time < current_time:
                        continue

                if item_id is not None and item_id not in sched_dict:
                    sched_dict[item_id] = item

            sched_dict = dict(sorted(sched_dict.items(), key=lambda x: x[1]['startTime']))
        else:
            print("Failed to fetch data from", sched_api_url, ". Status code:", response.status_code)

        time.sleep(1)

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

sched_active = []
sched_fsm = fsm.FarmScheduler()
control = Physic()
counter = 30


def active_schedule():
    global counter, sched_active, sched_fsm, sched_dict, control
    while True:
        counter -= 1
        if counter <= 0:
            control.readSensors("soil_temperature")
            control.readSensors("soil_moisture")
            counter = 30

        if not sched_active:
            current_time = datetime.now().strftime('%H:%M')
            top_sched_in_dict = list(sched_dict.values())[0]
            if len(sched_dict) and current_time == top_sched_in_dict["startTime"] and top_sched_in_dict["active"] == True:
                top_sched_in_dict["onSchedule"] = 1
                sched_active.append(top_sched_in_dict.copy())
                print("Activated new schedule!")

        if sched_active:
            sched_fsm.add_schedule(sched_active[0])
            print("SCHEDULE PROCESSING: ", sched_active[0])
            sched_fsm.run()
            sched_active.remove(sched_active[0])

thread1 = threading.Thread(target=fetch_area_selector)
thread2 = threading.Thread(target=fetch_scheduler)
thread3 = threading.Thread(target=active_schedule)

thread1.start()
thread2.start()
thread3.start()

thread1.join()
thread2.join()
thread3.join()