import time
from time import sleep
import robot
from enum import Enum

arlo = robot.Robot()

class Direction(Enum):
    Left = 1
    Right = 2

# Checks if there's any object in the path of the robot & stops the robot if that's the case.    
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
            return Left_sensor, Right_sensor
        
# Turns the robot 90 degrees.
def turn90(dir: Direction):
    if dir == Direction.Left:
        print(arlo.go_diff(30, 30, 0, 1))
        sleep(0.7)
        print(arlo.stop())
        sleep(0.041)
    else:
        print(arlo.go_diff(30, 30, 1, 0))
        sleep(0.7)
        print(arlo.stop())
        sleep(0.041)

# Drives one meter.
def driveM(meters):
    leftSpeed = 64
    rightSpeed = 64
    print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
    # Wait a bit while robot moves forward
    sleep(1.5*meters)
    # send a stop command
    print(arlo.stop())   
    sleep(0.041)   

# Drives the robot and checks which direction to go for avoiding an object.
def drive(): 
    arlo.go_diff(50, 50, 1, 1)
    Left_sensor, Right_sensor = check()
    if Left_sensor >= Right_sensor:
        print("left")
        turn90(Direction.Left)
        driveM(0.3)
        turn90(Direction.Right)
        driveM(0.3)
        turn90(Direction.Left)

    elif Right_sensor > Left_sensor:
        print("Right")
        turn90(Direction.Right)
        driveM(0.3)
        turn90(Direction.Left)
        driveM(0.3)
        turn90(Direction.Right)
    else:
        pass 

drive()        