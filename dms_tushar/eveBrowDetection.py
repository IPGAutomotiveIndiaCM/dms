import cv2
import mediapipe as mp

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Open webcam
cap = cv2.VideoCapture(1)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    height, width, _ = frame.shape

    # Convert to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_rgb.flags.writeable = False
    results = face_mesh.process(frame_rgb)

    frame_rgb.flags.writeable = True
    frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Left eyebrow top (landmark 65), Right eyebrow top (landmark 295)
            left_eyebrow = face_landmarks.landmark[65]
            right_eyebrow = face_landmarks.landmark[295]

            # Convert normalized coords to pixel coords
            left_x, left_y = int(left_eyebrow.x * width), int(left_eyebrow.y * height)
            right_x, right_y = int(right_eyebrow.x * width), int(right_eyebrow.y * height)

            # Draw circles at eyebrow points
            cv2.circle(frame, (left_x, left_y), 5, (0, 255, 0), -1)
            cv2.circle(frame, (right_x, right_y), 5, (0, 255, 0), -1)

            # Print values to console
            print(f"Left Eyebrow Y: {left_y} | Right Eyebrow Y: {right_y}")

            # Display values on screen
            cv2.putText(frame, f"L: {left_y}", (left_x, left_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            cv2.putText(frame, f"R: {right_y}", (right_x, right_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)

    # Show frame
    cv2.imshow("Eyebrow Movement Detection", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
