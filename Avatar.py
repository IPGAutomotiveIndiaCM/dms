import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Face Mesh
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Initialize drawing utilities
mp_drawing = mp.solutions.drawing_utils

# Start webcam
cap = cv2.VideoCapture(1)

# Define video writer
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
out = cv2.VideoWriter('avatar_output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 20, (frame_width, frame_height))

def draw_avatar_landmarks(frame, landmarks):
    avatar_frame = np.ones_like(frame) * 255  # white background
    h, w, _ = frame.shape

    # Head (simple circle)
    center = (w//2, h//2)
    radius = 100
    cv2.circle(avatar_frame, center, radius, (0, 200, 255), -1)

    # Draw facial features (eyes, mouth)
    for idx in [33, 263, 61, 291, 199]:  # Eye corners and lips (key points)
        landmark = landmarks[idx]
        x = int(landmark.x * w)
        y = int(landmark.y * h)
        cv2.circle(avatar_frame, (x, y), 5, (255, 0, 0), -1)

    return avatar_frame

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Flip frame horizontally for natural view
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Draw custom avatar based on landmarks
            avatar_frame = draw_avatar_landmarks(frame, face_landmarks.landmark)
            out.write(avatar_frame)
            cv2.imshow('3D Avatar', avatar_frame)

    else:
        out.write(frame)
        cv2.imshow('3D Avatar', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release everything
cap.release()
out.release()
cv2.destroyAllWindows()

print("Avatar video saved as 'avatar_output.mp4'")
