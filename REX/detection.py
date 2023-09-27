import numpy as np
import cv2
from cv2 import aruco
import time
from time import sleep
import robot
from enum import Enum
# import statemachine
arlo = robot.Robot()

try:
    import picamera2
    print("Camera.py: Using picamera2 module")
except ImportError:
    print("Camera.py: picamera2 module not available")
    exit(-1)

def gstreamer_pipeline(capture_width=1024, capture_height=720, framerate=15):
    """Utility function for setting parameters for the gstreamer camera pipeline"""
    return (
        "libcamerasrc !"
        "videobox autocrop=true !"
        "video/x-raw, width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! "
        "videoconvert ! "
        "appsink"
        % (
            capture_width,
            capture_height,
            framerate,
        )
    )

# Open a camera device for capturing
cam = cv2.VideoCapture(gstreamer_pipeline(), apiPreference=cv2.CAP_GSTREAMER)


if not cam.isOpened(): # Error
    print("Could not open camera")
    exit(-1)

time.sleep(1)  # wait for camera to setup

WIN_RF = "Ottos camera"
cv2.namedWindow(WIN_RF)
cv2.moveWindow(WIN_RF, 100, 100)


# Defining the ArUCo types.
aruco_type = aruco.DICT_6X6_250
#id = 2
aruco_dict = aruco.Dictionary_get(aruco_type)

class Direction(Enum):
    Left = 1
    Right = 2

# Turns the robot angle degrees.
def turn(dir: Direction, angle: int):
    if dir == Direction.Left:
        print(arlo.go_diff(49, 49, 0, 1))
        sleep(angle/90)
        print(arlo.stop())
        sleep(0.041)
    else:
        print(arlo.go_diff(49, 49, 1, 0))
        sleep(angle/90)
        print(arlo.stop())
        sleep(0.041)

# Drives one meter.
def driveM(meters):
    leftSpeed = 70
    rightSpeed = 70
    print(arlo.go_diff(leftSpeed, rightSpeed, 1, 1))
    # Wait a bit while robot moves forward
    sleep(1.7*meters)
    # send a stop command
    print(arlo.stop())   
    sleep(0.041)  

def go_to_box(angle_sign, angle, dist, ids):
        print("going to box")
        print("id: ", ids)
        print("dist: ", dist)
        print("actual dist:", (dist - 50) / 10)
        if angle_sign == -1:
            turn(Direction.Left, angle) 
            driveM((dist - 50) / 100) #drive to box with 50 cm to spare
            print(arlo.stop()) 
        elif angle_sign == 1:
            turn(Direction.Right, angle)
            driveM((dist - 50) / 100)
            print(arlo.stop()) 
        else:
            driveM((dist - 50) / 100)
            print(arlo.stop()) 

while cv2.waitKey(4) == -1: # Wait for a key pressed event
    retval, frameReference = cam.read() # Read frame

    if not retval: # Error
        print("Error!")
        exit(-1)

    # Show frames
    cv2.imshow(WIN_RF, frameReference)

    params = aruco.DetectorParameters_create()
    corners, ids, rejected_corners = aruco.detectMarkers(frameReference, aruco_dict, parameters=params)
    camMatrix = np.matrix([[459.3346823, 0, 612], # 612 px = 161.925 mm
                           [0, 459.3346823, 360],   # 360 px = 95.25 mm
                           [0, 0, 1]])

    rvecs, tvecs, objPoints = aruco.estimatePoseSingleMarkers(corners, 145, camMatrix, None, None)
    z_vector = np.array([0, 0, 1])

    if tvecs is not None:
        # print(arlo.stop()) 
        norms = []
        for i in range(len(tvecs)):
            norms.append(np.linalg.norm(tvecs[i]))
        maxvecidx = int(norms.index(min(norms)))
        vec = tvecs[norms.index(min(norms))][0] #choose the closest vector
        dist = np.linalg.norm(vec) #distance to the box
        dot = np.dot((vec / dist), z_vector)
        angle = np.degrees(np.arccos(dot))
        angle_sign = np.sign(vec) # 1 is right, -1 is left
        print("tvecs:",tvecs)
        print("norms:",norms)
        print("maxvecidx:",maxvecidx)
        print("vec:",vec)
        print("angle:", angle)
        print("ids", ids)
        go_to_box(angle_sign[0], angle, dist, ids[maxvecidx])

    else:
        turn(Direction.Right, 30)
        sleep(2)
 
#print("ArUCo type '{}' with ID '{}".format(aruco_type, id))
#tag_size = 600
#tag = np.zeros((tag_size, tag_size, 1), dtype="uint8")
#aruco.drawMarker(aruco_dict, id, tag_size, tag, 1)

#tag_name = "arucoMarkers/" + str(aruco_type) + "_" + str(id) + ".png"
#cv2.imwrite(tag_name, tag)