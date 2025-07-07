import cv2
import mediapipe as mp

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Convert to RGB
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = pose.process(image)

    # Back to BGR for OpenCV
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Get image dimensions
    height, width, _ = image.shape

    if results.pose_landmarks:
        # Draw pose landmarks
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        # Get nose landmark
        nose = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE]

        # Convert to pixel coordinates
        nose_x = int(nose.x * width)
        nose_y = int(nose.y * height)

        # Draw circle at nose
        cv2.circle(image, (nose_x, nose_y), 8, (0, 255, 0), -1)

        # Print head (nose) position
        print(f"Head Position - X: {nose_x}, Y: {nose_y}")

        # Display coordinates on screen
        position_text = f"X: {nose_x}, Y: {nose_y}"
        cv2.putText(image, position_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX,
                    1, (0, 255, 255), 2)

    # Show image
    cv2.imshow('Head Movement Detection', image)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release
cap.release()
cv2.destroyAllWindows()
