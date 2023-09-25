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

def gstreamer_pipeline(capture_width=900, capture_height=500, framerate=50):
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

while cv2.waitKey(4) == -1: # Wait for a key pressed event
    retval, frameReference = cam.read() # Read frame

    if not retval: # Error
        print("):< ):< ):< Error >:( >:( >:(")
        exit(-1)

    # Show frames
    cv2.imshow(WIN_RF, frameReference)

aruco_type = aruco.DICT_6X6_250
id = 3
aruco_dict = aruco.Dictionary_get(aruco_type)

print("ArUCo type '{}' with ID '{}".format(aruco_type, id))
tag_size = 600
tag = np.zeros((tag_size, tag_size, 1), dtype="uint8")
aruco.drawMarker(aruco_dict, id, tag_size, tag, 1)

tag_name = "arucoMarkers/" + str(aruco_type) + "_" + str(id) + ".png"
cv2.imwrite(tag_name, tag)
#params = cv2.aruco.DetectorParameters_create
#corners, ids, rejected = aruco.detectMarkers(cam.capture_array("main"), aruco_dict, params)
#print(aruco.detectMarkers(image, aruco_dict, params))

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
