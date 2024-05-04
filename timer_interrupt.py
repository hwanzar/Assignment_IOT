'''
    Software timer
'''
import numpy as np
import time

NUM_TIMERS = 4

timer_counter = np.zeros(NUM_TIMERS, dtype = int)
timer_flag = np.zeros(NUM_TIMERS, dtype = int)

for i in range(NUM_TIMERS):
    timer_flag[i] = 1
    timer_counter[i] = 0

def setTimer(index, duration):

    if index >= 0 and index < NUM_TIMERS:
        timer_counter[index] = duration
        timer_flag[index] = 0  # Reset the flag when setting the time
        timer_run(index)
# def timerRun():
#     """
#     Decrements active timers and sets flags for timers that reach zero.
#     This function should be called periodically to update timers.
#     """
#     for i in range(NUM_TIMERS):
#         if timer_counter[i] > 0:
#             timer_counter[i] -= 1
#             if timer_counter[i] == 0:
#                 timer_flag[i] = 1



def timer_run(i):
    while (timer_counter[i] > 0):
            print(str(timer_counter[i]) + " ")
            timer_counter[i] -= 1
            time.sleep(1)
            if (timer_counter[i] <= 0):
                timer_flag[i] = 1


def timerRun():
    timer_run(0)
    timer_run(1)
    timer_run(2)