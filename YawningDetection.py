import cv2
import mediapipe as mp


def get_pixel_coords(landmark, shape):
    h, w = shape[:2]
    return int(landmark.x * w), int(landmark.y * h)

def yawningDetection(cap,face_mesh):

    success, frame = cap.read()
    if not success:
        return

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Inner upper and lower lips
            top_lip = face_landmarks.landmark[13]
            bottom_lip = face_landmarks.landmark[14]

            top_x, top_y = get_pixel_coords(top_lip, frame.shape)
            bottom_x, bottom_y = get_pixel_coords(bottom_lip, frame.shape)

            # Vertical mouth open distance
            mouth_open = abs(bottom_y - top_y)

            # Print values to console
            print(f"Mouth Open Distance: {mouth_open} pixels")

            # Determine status
            if mouth_open < 10:
                status = "Mouth Closed"
            elif 10 <= mouth_open < 34:
                status = "Mouth Open"
            else:
                status = "Yawning"

            # Draw lip points
            cv2.circle(frame, (top_x, top_y), 4, (0, 255, 0), -1)
            cv2.circle(frame, (bottom_x, bottom_y), 4, (0, 0, 255), -1)

            # Show info
            cv2.putText(frame, status, (30, 40), cv2.FONT_HERSHEY_SIMPLEX,
                        1.0, (255, 255, 0) if "Yawning" in status else (0, 255, 255), 2)
            cv2.putText(frame, f"Distance: {mouth_open}", (30, 80),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        print(mouth_open)
            
    return frame
