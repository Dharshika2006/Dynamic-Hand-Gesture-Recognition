import cv2
import mediapipe as mp
import pandas as pd
import os
import numpy as np
from tqdm import tqdm

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Configuration
GESTURES = ['thin', 'go', 'who', 'help', 'thanksgiving', 'tall', 'short', 'what', 'shirt', 'yes']
NUM_VIDEOS = 30
FRAMES_PER_VIDEO = 30
LANDMARKS_DIR = 'gesture_landmarks'
FPS = 30

# Create directories
os.makedirs(LANDMARKS_DIR, exist_ok=True)
for gesture in GESTURES:
    os.makedirs(os.path.join(LANDMARKS_DIR, gesture), exist_ok=True)

def collect_landmarks():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open webcam")
        return

    print("Starting data collection...")
    for gesture in GESTURES:
        print(f"Collecting data for: {gesture}")
        for video_idx in tqdm(range(NUM_VIDEOS), desc="Videos"):
            landmarks_list = []
            input(f"Press Enter to start collecting {gesture} video {video_idx+1}...")
            
            for frame_idx in range(FRAMES_PER_VIDEO):
                ret, frame = cap.read()
                if not ret:
                    print("Error: Failed to capture frame")
                    break
                
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frame_rgb)
                
                landmarks = []
                if results.multi_hand_landmarks:
                    hand_landmarks = results.multi_hand_landmarks[0]
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    for lm in hand_landmarks.landmark:
                        landmarks.extend([lm.x, lm.y, lm.z])
                else:
                    landmarks = [0.0] * 63  # 21 landmarks * 3 (x, y, z)

                landmarks_list.append(landmarks)
                cv2.imshow('Data Collection', frame)
                if cv2.waitKey(1000 // FPS) & 0xFF == ord('q'):
                    break

            # Save landmarks
            df = pd.DataFrame(landmarks_list, columns=[f'lm_{i}_{coord}' for i in range(21) for coord in ['x', 'y', 'z']])
            csv_path = os.path.join(LANDMARKS_DIR, gesture, f'{gesture}_{video_idx}_landmarks.csv')
            df.to_csv(csv_path, index=False)
            print(f"Saved: {csv_path}")

    cap.release()
    cv2.destroyAllWindows()
    print("✅ Data collection complete!")

if __name__ == "__main__":
    collect_landmarks()