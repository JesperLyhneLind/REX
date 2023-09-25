import numpy as np
import cv2
from cv2 import aruco
#import matplotlib.pyplot as plt
#import matplotlib as mpl
#import pandas as pd
import time


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

#print("ArUCo type '{}' with ID '{}".format(aruco_type, id))
#tag_size = 600
#tag = np.zeros((tag_size, tag_size, 1), dtype="uint8")
#aruco.drawMarker(aruco_dict, id, tag_size, tag, 1)

#tag_name = "arucoMarkers/" + str(aruco_type) + "_" + str(id) + ".png"
#cv2.imwrite(tag_name, tag)

while cv2.waitKey(4) == -1: # Wait for a key pressed event
    retval, frameReference = cam.read() # Read frame

    if not retval: # Error
        print("Error!")
        exit(-1)

    # Show frames
    cv2.imshow(WIN_RF, frameReference)

    params = cv2.aruco.DetectorParameters_create()
    corners, ids, rejected_corners = aruco.detectMarkers(frameReference, aruco_dict, parameters=params)
    #print(aruco.detectMarkers(frameReference, aruco_dict, params))
    #print("ids: ", ids)
    #print("corners: ", corners)

    camMatrix = np.array([42.83075, 0, 612], #c_x = captureWidth / 2 and c_y = captureHeight / 2
                         [0, 42.83075, 360],
                         [0, 0, 1])

    rvecs, tvecs, objPoints = aruco.estimatePoseSingleMarkers(corners, 145, camMatrix, None, None)
    print("tvecs: ", tvecs)


#markerlength = 14,5 cm
#distcoeff = none
    text = input('')    
    if text == 'q':
        break

#cv2.imshow("ArUCo Tag", tag)

#cv2.waitKey(0)

#cv2.destroyAllWindows()

#fig = plt.figure()
#nx = 4
#ny = 3
#for i in range(1, nx*ny+1):
#    ax = fig.add_subplot(ny,nx, i)
#    img = aruco.drawMarker(aruco_dict,i, 700)
#    plt.imshow(img, cmap = mpl.cm.gray, interpolation = "nearest")
#    ax.axis("off")

#plt.savefig("_data/markers.pdf")
#plt.show()
