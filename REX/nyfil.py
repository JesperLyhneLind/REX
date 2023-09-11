import time
from time import sleep
import robot

arlo = robot.Robot()

sleep(1)
Front_sensor = arlo.read_front_ping_sensor()
Right_sensor = arlo.read_right_ping_sensor()
Left_sensor = arlo.read_left_ping_sensor()

def check():
    while(True):
        Front_sensor = arlo.read_front_ping_sensor()
        print(Front_sensor)
        Right_sensor = arlo.read_right_ping_sensor()
        print(Right_sensor)
        Left_sensor = arlo.read_left_ping_sensor()
        print(Left_sensor)
        
        if Left_sensor < 200 or Right_sensor < 200 or Front_sensor < 250:
            print(arlo.stop())
            return


def drive(): 
    arlo.go_diff(60, 60, 1, 1)
    check()
    if Left_sensor > Right_sensor:
        print(arlo.go_diff(41, 41, 0, 1))
        sleep(0.7)# Wait a little bit while robot moves backwards
        print(arlo.stop())
        sleep(0.041)
    else:
        print(arlo.go_diff(41, 41, 1, 0))
        sleep(0.7)# Wait a bit while robot moves backwards
        print(arlo.stop())
        sleep(0.041)
    drive()
    
    
drive()       