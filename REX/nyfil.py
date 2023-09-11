import time
from time import sleep
import robot

arlo = robot.Robot()

sleep(1)
global Front_sensor
global Right_sensor
global Left_sensor

def check():
    while(True):
        Front_sensor = arlo.read_front_ping_sensor()
        Right_sensor = arlo.read_right_ping_sensor()
        Left_sensor = arlo.read_left_ping_sensor()

        if Left_sensor < 200 or Right_sensor < 200 or Front_sensor < 250:
            print("Left: " + str(Left_sensor))
            print("Front: " + str(Front_sensor))
            print("Right: " + str(Right_sensor))
            print(arlo.stop())
            return


def drive(): 
    arlo.go_diff(50, 50, 1, 1)
    check()
    if Left_sensor >= Right_sensor:
        print("\n")
        print("LEFT_SENSOR: " + str(Left_sensor))
        print("RIGHT_SENSOR: " + str(Right_sensor))
        print(arlo.go_diff(41, 41, 0, 1))
        sleep(0.7)# Wait a little bit while robot moves backwards
        print(arlo.stop())
        print("Left")
        sleep(0.041)
    elif Right_sensor > Left_sensor:
        print("\n")
        print("LEFT_SENSOR: " + str(Left_sensor))
        print("RIGHT_SENSOR: " + str(Right_sensor))
        print(arlo.go_diff(41, 41, 1, 0))
        sleep(0.7)# Wait a bit while robot moves backwards
        print(arlo.stop())
        print("Right")
        sleep(0.041)
    else:
        pass
    drive()

drive()       