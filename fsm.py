from datetime import datetime
# from rs485 import *
from timer_interrupt import *
from controller import *
import json
import time

PHYSIC = Physic()


class FarmScheduler():
    def __init__(self, debug=True):
        self.debug = debug
        self.schedules = []
        self.current_schedule = None
        self.current_state = IdleState(debug=self.debug)

    def run(self):
        time.sleep(2)
        while True:
            if not self.current_schedule:
                self.current_schedule = self.check_schedule()
                if not self.current_schedule:
                    time.sleep(1)  # Sleep briefly to avoid busy waiting
                    continue

            self.current_state = self.current_state.execute(self.current_schedule)
            if isinstance(self.current_state, IdleState) and self.current_schedule['next-cycle'] <= 0:
                self.schedules.pop(0)
                print("Cycle complete, checking for new schedules.")
                self.current_schedule = None
                break

            time.sleep(1)  # Main loop tick rate

    def add_schedule(self, new_schedule):
        for sched in self.schedules:
            if new_schedule["startTime"] < sched["startTime"]:
                return False
        self.schedules.append(new_schedule)

    def check_schedule(self):
        # This is a placeholder for actual schedule checking logic
        for schedule in self.schedules:
            return schedule
        return None

class State:
    def __init__(self, debug=True):
        self.debug = debug

    def execute(self, schedule):
        raise NotImplementedError

    def wait_for_timer(self, timer_id):
        while timer_counter[timer_id] > 0:
            timer_run(timer_id)
            time.sleep(1)  # Sleep to simulate time passing

class IdleState(State):
    def execute(self, schedule):
        if self.debug:
            print("IDLE STATE")
        if schedule['next-cycle'] > 0:
            schedule['next-cycle'] = schedule['next-cycle'] -1
            return Mixer1State(debug=self.debug)
        else:
            print("FINISHED !!!")
            return self

class Mixer1State(State):
    def execute(self, schedule):
        PHYSIC.setActuators(MIXER1,1)
        setTimer(0, int(schedule['mixer1']))
        # self.wait_for_timer(0)
        PHYSIC.setActuators(MIXER1,0)
        if self.debug:
            print("MIXER1 STATE - Complete")
        return Mixer2State(debug=self.debug)

class Mixer2State(State):
    def execute(self, schedule):
        PHYSIC.setActuators(MIXER2,1)
        setTimer(0, int(schedule['mixer2']))
        # self.wait_for_timer(0)
        PHYSIC.setActuators(MIXER2,0)
        if self.debug:
            print("MIXER2 STATE - Complete")
        return Mixer3State(debug=self.debug)

class Mixer3State(State):
    def execute(self, schedule):
        PHYSIC.setActuators(MIXER3,1)
        setTimer(0, int(schedule['mixer3']))
        # self.wait_for_timer(0)
        PHYSIC.setActuators(MIXER3,0)
        if self.debug:
            print("MIXER3 STATE - Complete")
        return PumpInState(debug=self.debug)

class PumpInState(State):
    def execute(self, schedule):
        PHYSIC.setActuators(PUMPIN,1)
        setTimer(0, int(schedule['pump-in']))
        # self.wait_for_timer(0)
        PHYSIC.setActuators(PUMPIN,0)
        if self.debug:
            print("PUMP IN STATE - Complete")
        return PumpOutState(debug=self.debug)

class PumpOutState(State):
    def execute(self, schedule):
        PHYSIC.setActuators(PUMPOUT,1)
        setTimer(0, int(schedule['pump-out']))
        # self.wait_for_timer(0)
        PHYSIC.setActuators(PUMPOUT,0)
        if self.debug:
            print("PUMP OUT STATE - Complete")
        return IdleState(debug=self.debug)



def convert_schedule_json_to_dict(json_data):
    print("DEBUG: We been heerre")
    return json.loads(json_data)




