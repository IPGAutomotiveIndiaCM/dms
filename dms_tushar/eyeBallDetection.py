import cv2
import time
import numpy as np

import time
from typing import Optional, Tuple

def detect_faces(img, cascade):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = cascade.detectMultiScale(gray_frame, 1.3, 5)
    if len(coords) > 1:
        biggest = (0, 0, 0, 0)
        for i in coords:
            if i[3] > biggest[3]:
                biggest = i
        biggest = np.array([i], np.int32)
    elif len(coords) == 1:
        biggest = coords
    else:
        return None
    for (x, y, w, h) in biggest:
        frame = img[y:y + h, x:x + w]
    return frame


def detect_eyes(img, cascade):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = cascade.detectMultiScale(gray_frame, 1.3, 5)  # detect eyes
    width = np.size(img, 1)  # get face frame width
    height = np.size(img, 0)  # get face frame height
    left_eye = None
    right_eye = None
    for (x, y, w, h) in eyes:
        if y > height / 2:
            pass
        eyecenter = x + w / 2  # get the eye center
        if eyecenter < width * 0.5:
            left_eye = img[y:y + h, x:x + w]
        else:
            right_eye = img[y:y + h, x:x + w]
    return left_eye, right_eye


def cut_eyebrows(img):
    height, width = img.shape[:2]
    eyebrow_h = int(height / 4)
    img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)

    return img


def blob_process(img, threshold, detector):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
    img = cv2.erode(img, None, iterations=2)
    img = cv2.dilate(img, None, iterations=4)
    img = cv2.medianBlur(img, 5)
    keypoints = detector.detect(img)
    print(keypoints)
    return keypoints


def nothing(x):
    pass

def monitorEyeBallMovement(keypoints):
    if(keypoints == ()):
        seconds = time.time()
        local_time = time.ctime(seconds)
        print(local_time)
    else:
        seconds = 0

def validate_tuple_stays_empty(keypoints_tuple,counterStart,driverFocusedEyeThreshold) -> bool:
    #checking if every element in input_tuple is an empty tuple.
    if all(isinstance(t, tuple) and not t for t in keypoints_tuple):
        while counterStart < driverFocusedEyeThreshold:
            #print(f"Tuple remained empty for the whole duration")
            return False
        time.sleep(1)
    return True

def eyeBallDetection(frame,face_cascade,eye_cascade,detector1):
    keypoints_tuple =[]
    face_frame = detect_faces(frame, face_cascade)
    if face_frame is not None:
        eyes = detect_eyes(face_frame, eye_cascade)
        for eye in eyes:
            if eye is not None:
                threshold = r = cv2.getTrackbarPos('threshold', 'image')
                eye = cut_eyebrows(eye)
                keypoints = blob_process(eye, threshold, detector1)
                eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                keypoints_tuple.append(keypoints)
    return frame, keypoints_tuple