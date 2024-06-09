from datetime import datetime
# from rs485 import *
from timer_interrupt import *
from controller import *
import json
import time

PHYSIC = Physic()

class FarmScheduler():
    def __init__(self):
        self.schedules = []
        self.current_schedule = None
        self.current_state = IdleState()

    def run(self):
        time.sleep(2)
        while True:
            if not self.current_schedule:
                self.current_schedule = self.check_schedule()
                if not self.current_schedule:
                    time.sleep(1)
                    continue

            self.current_state = self.current_state.run(self.current_schedule)
            if isinstance(self.current_state, IdleState) and self.current_schedule['cycle'] <= 0:
                self.schedules.pop(0)
                print("Cycle complete, checking for new schedules.")
                self.current_schedule = None
                break

            time.sleep(1)

    def add_schedule(self, new_schedule):
        self.schedules.append(new_schedule)

    def check_schedule(self):
        for schedule in self.schedules:
            return schedule
        return None

class State:
    def __init__(self):
        print("STATE INITIALIZED")

    def run(self, schedule):
        raise NotImplementedError

class IdleState(State):
    def run(self, schedule):
        print("IDLE STATE")
        if schedule['cycle'] > 0:
            schedule['cycle'] = schedule['cycle'] - 1
            return Mixer1State()
        else:
            print("FINISHED !!!")
            return self

class Mixer1State(State):
    def run(self, schedule):
        PHYSIC.setActuators(MIXER1, 1)
        setTimer(0, int(schedule['mixer1']))
        PHYSIC.setActuators(MIXER1, 0)
        print("MIXER1 STATE - Complete")
        return Mixer2State()

class Mixer2State(State):
    def run(self, schedule):
        PHYSIC.setActuators(MIXER2, 1)
        setTimer(0, int(schedule['mixer2']))
        PHYSIC.setActuators(MIXER2, 0)
        print("MIXER2 STATE - Complete")
        return Mixer3State()

class Mixer3State(State):
    def run(self, schedule):
        PHYSIC.setActuators(MIXER3, 1)
        setTimer(0, int(schedule['mixer3']))
        PHYSIC.setActuators(MIXER3, 0)
        print("MIXER3 STATE - Complete")
        return PumpInState()

class PumpInState(State):
    def run(self, schedule):
        PHYSIC.setActuators(PUMPIN, 1)
        setTimer(0, int(schedule['pump-in']))
        PHYSIC.setActuators(PUMPIN, 0)
        print("PUMP IN STATE - Complete")
        return PumpOutState()

class PumpOutState(State):
    def run(self, schedule):
        PHYSIC.setActuators(PUMPOUT, 1)
        setTimer(0, int(schedule['pump-out']))
        PHYSIC.setActuators(PUMPOUT, 0)
        print("PUMP OUT STATE - Complete")
        return IdleState()
