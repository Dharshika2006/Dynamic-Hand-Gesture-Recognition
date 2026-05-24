import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
from tqdm import tqdm

# Configuration
GESTURES = ['thin', 'go', 'who', 'help', 'thanksgiving', 'tall', 'short', 'what', 'shirt', 'yes']
LANDMARKS_DIR = 'gesture_landmarks'
MODEL_PATH = 'gesture_model_10_5frame.keras'
SEQUENCE_LENGTH = 5
NUM_FEATURES = 63  # 21 landmarks * 3 (x, y, z)

def load_data():
    X, y = [], []
    for gesture_idx, gesture in enumerate(GESTURES):
        gesture_dir = os.path.join(LANDMARKS_DIR, gesture)
        if not os.path.exists(gesture_dir):
            print(f"Warning: {gesture_dir} does not exist")
            continue

        for csv_file in tqdm(os.listdir(gesture_dir), desc=gesture):
            if csv_file.endswith('.csv'):
                df = pd.read_csv(os.path.join(gesture_dir, csv_file))
                if len(df) >= SEQUENCE_LENGTH:
                    for start_idx in range(0, len(df) - SEQUENCE_LENGTH + 1):
                        sequence = df.iloc[start_idx:start_idx + SEQUENCE_LENGTH].values
                        X.append(sequence)
                        y.append(gesture_idx)

    X = np.array(X)
    y = to_categorical(y, num_classes=len(GESTURES))
    return X, y

def build_model():
    model = Sequential([
        LSTM(64, return_sequences=True, activation='relu', input_shape=(SEQUENCE_LENGTH, NUM_FEATURES)),
        LSTM(128, return_sequences=False, activation='relu'),
        Dense(64, activation='relu'),
        Dropout(0.3),
        Dense(len(GESTURES), activation='softmax')
    ])
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return model

def train_model():
    print("Loading data...")
    X, y = load_data()
    if len(X) == 0:
        print("Error: No data loaded")
        return

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = build_model()
    print("Training model...")
    history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=1)
    model.save(MODEL_PATH)
    print(f"Saved model to {MODEL_PATH}")
    print("✅ Training complete!")
    print(f"Final training accuracy: {history.history['accuracy'][-1]:.4f}")
    print(f"Final validation accuracy: {history.history['val_accuracy'][-1]:.4f}")

if __name__ == "__main__":
    train_model()