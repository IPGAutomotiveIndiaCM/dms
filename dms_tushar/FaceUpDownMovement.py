import cv2
import mediapipe as mp

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1,
                                   refine_landmarks=True, min_detection_confidence=0.5)

# Start webcam
cap = cv2.VideoCapture(1)

def get_pixel_coords(landmark, frame_shape):
    h, w = frame_shape[:2]
    return int(landmark.x * w), int(landmark.y * h)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)
    face_direction = "Face: Neutral"

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Key facial landmarks
            forehead = face_landmarks.landmark[10]     # Upper part of face (forehead/glabella)
            nose_tip = face_landmarks.landmark[1]      # Nose tip
            chin = face_landmarks.landmark[152]        # Chin bottom

            # Convert to pixel coordinates
            forehead_x, forehead_y = get_pixel_coords(forehead, frame.shape)
            nose_x, nose_y = get_pixel_coords(nose_tip, frame.shape)
            chin_x, chin_y = get_pixel_coords(chin, frame.shape)

            # Draw points
            cv2.circle(frame, (forehead_x, forehead_y), 5, (255, 0, 0), -1)
            cv2.circle(frame, (nose_x, nose_y), 5, (0, 255, 0), -1)
            cv2.circle(frame, (chin_x, chin_y), 5, (0, 0, 255), -1)

            # Print raw Y values
            print(f"Forehead Y: {forehead_y}, Nose Y: {nose_y}, Chin Y: {chin_y}")

            # Calculate vertical distances
            forehead_to_nose = nose_y - forehead_y
            nose_to_chin = chin_y - nose_y

            print(f"Forehead→Nose: {forehead_to_nose}, Nose→Chin: {nose_to_chin}")

            # Determine face direction
            if forehead_to_nose > nose_to_chin + 10:
                face_direction = "Face: Down"
            elif nose_to_chin > forehead_to_nose + 10:
                face_direction = "Face: Up"
            else:
                face_direction = "Face: Neutral"

            # Display result on frame
            cv2.putText(frame, face_direction, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    # Show frame
    cv2.imshow("Face Up/Down Detection", frame)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
