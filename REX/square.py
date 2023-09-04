# Simpelt eksempel fra absalon
from time import sleep

import robot

# Create a robot object and initialize
arlo = robot.Robot()

print("Running ...")


# send a go_diff command to drive forward
leftSpeed = 64
rightSpeed = 64

for i in range(3):
    # 1m forward
    print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
    sleep(2.5)
    print(arlo.stop())
    sleep(0.041)

    # rotate 90 degrees
    print(arlo.go_diff(leftSpeed, rightSpeed, 0,1))
    sleep(0.785)# Wait a bit while robot moves backwards
    print(arlo.stop())
    sleep(0.041)




# request to read Front sonar ping sensor
print("Front sensor = ", arlo.read_front_ping_sensor())
sleep(0.041)


# request to read Back sonar ping sensor
print("Back sensor = ", arlo.read_back_ping_sensor())
sleep(0.041)

# request to read Right sonar ping sensor
print("Right sensor = ", arlo.read_right_ping_sensor())
sleep(0.041)

# request to read Left sonar ping sensor
print("Left sensor = ", arlo.read_left_ping_sensor())
sleep(0.041)







print("Finished")
