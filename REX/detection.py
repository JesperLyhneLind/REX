import numpy as np
import cv2, PIL
from cv2 import aruco
#import matplotlib.pyplot as plt
#import matplotlib as mpl
#import pandas as pd

try:
    import picamera2
    print("Camera.py: Using picamera2 module")
except ImportError:
    print("Camera.py: picamera2 module not available")
    exit(-1)

aruco_type = aruco.DICT_6X6_250
id = 3
aruco_dict = aruco.Dictionary_get(aruco_type)

print("ArUCo type '{}' with ID '{}".format(aruco_type, id))
tag_size = 600
tag = np.zeros((tag_size, tag_size, 1), dtype="uint8")
aruco.drawMarker(aruco_dict, id, tag_size, tag, 1)

tag_name = "arucoMarkers/" + str(aruco_type) + "_" + str(id) + ".png"
cv2.imwrite(tag_name, tag)
cv2.imshow("ArUCo Tag", tag)

cv2.waitKey(0)

cv2.destroyAllWindows()

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
