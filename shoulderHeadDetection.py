import cv2
import mediapipe as mp


def displayShoulderHead(image,nose_x,nose_y,left_x,left_y,right_x,right_y):
    cv2.putText(image, f"Head: ({nose_x}, {nose_y})", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    cv2.putText(image, f"Left Shoulder: ({left_x}, {left_y})", (10, 70),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
    cv2.putText(image, f"Right Shoulder: ({right_x}, {right_y})", (10, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)

# Open webcam
def shoulderHeadDetection(frame,mp_pose,pose,mp_drawing):
    # Convert to RGB for MediaPipe
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)

    # Back to BGR for OpenCV
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Get frame dimensions
    height, width, _ = image.shape

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Get landmarks
        landmarks = results.pose_landmarks.landmark

        # Get head (nose)
        nose = landmarks[mp_pose.PoseLandmark.NOSE]
        nose_x = int(nose.x * width)
        nose_y = int(nose.y * height)

        # Get shoulders
        left_shoulder = landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER]
        right_shoulder = landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        left_x = int(left_shoulder.x * width)
        left_y = int(left_shoulder.y * height)
        right_x = int(right_shoulder.x * width)
        right_y = int(right_shoulder.y * height)

        # Draw circles
        cv2.circle(image, (nose_x, nose_y), 8, (0, 255, 0), -1)
        cv2.circle(image, (left_x, left_y), 8, (255, 0, 0), -1)
        cv2.circle(image, (right_x, right_y), 8, (255, 0, 0), -1)

        # Print values to console
        print(f"Head (Nose): X={nose_x}, Y={nose_y}")
        print(f"Left Shoulder: X={left_x}, Y={left_y}")
        print(f"Right Shoulder: X={right_x}, Y={right_y}")
        print("-" * 50)
        # Show values on screen
    return image,nose_x,nose_y,left_x,left_y,right_x,right_y

    # Show frame
    #cv2.imshow('Head & Shoulder Position', image)
