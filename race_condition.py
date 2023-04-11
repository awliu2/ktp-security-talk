from threading import Thread
from time import sleep

shared_var = 0


def increase_by(n):
    global shared_var

    local_copy = shared_var
    local_copy += n

    sleep(0.1)
    shared_var = local_copy


thread_1 = Thread(target = increase_by, args=(1,))
thread_2 = Thread(target = increase_by, args=(2,))

# these threads run in parallel (at the same time) 
thread_1.start()
thread_2.start()

# join tells the main program to wait for the threads to finish
# before continuing execution
thread_1.join()
thread_2.join()

print(f'the final value of shared_var is {shared_var}')