import cv2

def shoulderHeadDetection(frame, mp_pose, pose, mp_drawing):
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    height, width, _ = image.shape

    # ✅ Predefine output variables
    nose_x = nose_y = left_x = left_y = right_x = right_y = None

    if results.pose_landmarks:
        try:
            mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            landmarks = results.pose_landmarks.landmark

            nose = landmarks[mp_pose.PoseLandmark.NOSE]
            left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
            right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]

            nose_x = int(nose.x * width)
            nose_y = int(nose.y * height)
            left_x = int(left_shoulder.x * width)
            left_y = int(left_shoulder.y * height)
            right_x = int(right_shoulder.x * width)
            right_y = int(right_shoulder.y * height)

        except Exception as e:
            print(" Error accessing landmarks:", e)

    #  Debug print before return
    print("shoulderHeadDetection() running — nose_x initialized as:", nose_x)
    return image, nose_x, nose_y, left_x, left_y, right_x, right_y
