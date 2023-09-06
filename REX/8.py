# Simpelt eksempel fra absalon
from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")


# send a go_diff command to drive forward

for i in range(1):
    

    # rotate 90 degrees
    print(arlo.go_diff(0, 41, 1,1))
    sleep(7)# Wait a bit while robot moves backwards
    # print(arlo.go_diff(41, 0, 1,1))
    # sleep(7)



print("Finished")
