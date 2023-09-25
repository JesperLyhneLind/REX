import numpy as np
import cv2
from cv2 import aruco
import time
from time import sleep
import robot
from enum import Enum

arlo = robot.Robot()

try:
    import picamera2
    print("Camera.py: Using picamera2 module")
except ImportError:
    print("Camera.py: picamera2 module not available")
    exit(-1)

def gstreamer_pipeline(capture_width=1024, capture_height=720, framerate=30):
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

while cv2.waitKey(4) == -1: # Wait for a key pressed event
    retval, frameReference = cam.read() # Read frame
    

    if not retval: # Error
        print("Error!")
        exit(-1)

    # Show frames
    cv2.imshow(WIN_RF, frameReference)

    params = aruco.DetectorParameters_create()
    corners, ids, rejected_corners = aruco.detectMarkers(frameReference, aruco_dict, parameters=params)
    #print(aruco.detectMarkers(frameReference, aruco_dict, params))
    #print("ids: ", ids)
    #print("corners: ", corners)

    # c_x = captureWidth / 2 and c_y = captureHeight / 2
    camMatrix = np.matrix([[42.83075, 0, 612],
                           [0, 42.83075, 360],
                           [0, 0, 1]])

    rvecs, tvecs, objPoints = aruco.estimatePoseSingleMarkers(corners, 145, camMatrix, None, None)
    print("tvecs: ", tvecs)

    z_vector = np.array([0, 0, 1])

    if tvecs is not None:
        dist = np.linalg.norm(tvecs) #distance to the box
        dot = np.dot((tvecs / dist), z_vector)
        angle = np.degrees(np.arccos(dot))
        print("angle: ", angle)
        print("tvec norm", np.linalg.norm(tvecs))
        angle_sign = np.sign(tvecs[0]) # 1 is right, -1 is left
        
        print("angle sign: ", angle_sign)
        print("angle sign[0]: ", angle_sign[0])
        print("t_vecs: ", tvecs)
        print("t_vecs[0]: ", tvecs[0])


        if angle_sign[0] == -1:
            turn(Direction.Left, angle)
            driveM((dist - 500) / 100)
        elif angle_sign[0] == 1:
            turn(Direction.Right, angle)
            driveM((dist - 500) / 100)
        else:
            driveM((dist - 500) / 100)




    




#print("ArUCo type '{}' with ID '{}".format(aruco_type, id))
#tag_size = 600
#tag = np.zeros((tag_size, tag_size, 1), dtype="uint8")
#aruco.drawMarker(aruco_dict, id, tag_size, tag, 1)

#tag_name = "arucoMarkers/" + str(aruco_type) + "_" + str(id) + ".png"
#cv2.imwrite(tag_name, tag)