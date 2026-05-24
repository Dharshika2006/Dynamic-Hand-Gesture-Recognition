import cv2
import mediapipe as mp
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from collections import deque

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Configuration
GESTURES = ['thin', 'go', 'who', 'help', 'thanksgiving', 'tall', 'short', 'what', 'shirt', 'yes']
MODEL_PATH = 'gesture_model_10_5frame.keras'
SEQUENCE_LENGTH = 5
NUM_FEATURES = 63  # 21 landmarks * 3 (x, y, z)

def live_prediction():
    model = load_model(MODEL_PATH)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot open webcam")
        return

    sequence = deque(maxlen=SEQUENCE_LENGTH)
    print("Starting live prediction...")

    while True:
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
            landmarks = [0.0] * NUM_FEATURES

        sequence.append(landmarks)
        if len(sequence) == SEQUENCE_LENGTH:
            X = np.array([sequence])
            prediction = model.predict(X, verbose=0)[0]
            gesture_idx = np.argmax(prediction)
            confidence = prediction[gesture_idx]
            gesture = GESTURES[gesture_idx]
            if confidence > 0.5:
                text = f"{gesture} ({confidence:.2f})"
            else:
                text = "Unknown"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow('Live Prediction', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print("✅ Live prediction complete!")

if __name__ == "__main__":
    live_prediction()