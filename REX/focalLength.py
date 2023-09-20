import cv2 # Import the OpenCV library

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

print("OpenCV version = " + cv2.__version__)

# Open a camera device for capturing
cam = cv2.VideoCapture(gstreamer_pipeline(), apiPreference=cv2.CAP_GSTREAMER)

if not cam.isOpened(): # Error
    print("Could not open camera")
    exit(-1)

# Open a window
WIN_RF = "Focal Length"
cv2.namedWindow(WIN_RF)
cv2.moveWindow(WIN_RF, 100, 100)

#while cv2.waitKey(4) == -1: # Wait for a key pressed event
#    retval, frameReference = cam.read() # Read frame
    
#    if not retval: # Error
#        print(" < < <  Game over!  > > > ")
#        exit(-1)
    
    # Show frames
#    cv2.imshow(WIN_RF, frameReference)

cnt = 40.0
while cv2.waitKey(4) == -1: # Wait for a key pressed event
    retval, frameReference = cam.read() # Read frame

    if not retval: # Error
        print("):< ):< ):< Error >:( >:( >:(")
        exit(-1)

    # Show frames
    cv2.imshow(WIN_RF, frameReference)
    if cv2.waitKey(4) == 32: # Takes picture when pressing space
        print("pressed space")
        path = '../REX/REX/pictures'
        filename = 'pictures/' + str(cnt) + '.jpg'
        cv2.imwrite(filename, frameReference) # Saving the image
        print("The image saved succesfully: " + cv2.imwrite(filename, frameReference))
        print(" ")
        print("After saving image:")  
        print(os.listdir(directory))
        cnt += 0.1
        #cnt += 20


# Finished successfully
