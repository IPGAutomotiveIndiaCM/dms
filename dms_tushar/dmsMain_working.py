import numpy as np
from handsOnSteeringDetection import *
from shoulderHeadDetection import *
from eyeBallDetection import *
from YawningDetection import *
#creating random images
frame1 = np.random.randint(0, 256, (300, 300, 3), dtype=np.uint8)
frame2 = np.random.randint(0, 256, (300, 300, 3), dtype=np.uint8)

cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
ctime=0
ptime=0


# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

#initialization of eyeball tracking

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default_eyeBase.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
detector_params = cv2.SimpleBlobDetector_Params()
detector_params.filterByArea = True
detector_params.maxArea = 1500
detector1 = cv2.SimpleBlobDetector_create(detector_params)
#creating a new bar on the same image for defining the eye ball threshold
cv2.namedWindow('image')
cv2.createTrackbar('threshold', 'image', 0, 255, nothing)

#initialization of yawninng  and Initialize Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, refine_landmarks=True)
#handtracking 
detector = HandTrackingDynamic()
while True:
    ret, frame = cap.read()
    #check for HandOn detection
    
    frame = handsOnSteeringDetection(cap,detector,ctime,ptime)
    #display the text on picture
    cv2.imshow('frame', frame)
            #check head and shoulder movement
    shoulderheadFrame,nose_x,nose_y,left_x,left_y,right_x,right_y = shoulderHeadDetection(frame,mp_pose,pose,mp_drawing)
            #display shoulder and head movement
    displayShoulderHead(shoulderheadFrame,nose_x,nose_y,left_x,left_y,right_x,right_y)
    cv2.imshow('frame', shoulderheadFrame)
            #check eyeBall movement
    eyeFrame = eyeBallDetection(frame,face_cascade,eye_cascade,detector1)
    cv2.imshow('frame',eyeFrame)
            #check Face yawning
    #yawnningFrame = yawningDetection(cap,face_mesh)
    #cv2.imshow('frame',yawnningFrame)

    cv2.waitKey(1)
    if cv2.waitKey(1) & 0xff == ord('q'): 
        break

cap.release()
cv2.destroyAllWindows()