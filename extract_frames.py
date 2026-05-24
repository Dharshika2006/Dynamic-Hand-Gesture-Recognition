import cv2
import os
from tqdm import tqdm

# Configuration
GESTURES = ['thin', 'go', 'who', 'help', 'thanksgiving', 'tall', 'short', 'what', 'shirt', 'yes']
VIDEO_DIR = 'gesture_data'
FRAMES_DIR = 'gesture_frames'
FRAMES_PER_VIDEO = 30

# Create directories
os.makedirs(FRAMES_DIR, exist_ok=True)
for gesture in GESTURES:
    os.makedirs(os.path.join(FRAMES_DIR, gesture), exist_ok=True)

def extract_frames():
    print("Starting frame extraction...")
    for gesture in GESTURES:
        video_dir = os.path.join(VIDEO_DIR, gesture)
        frame_dir = os.path.join(FRAMES_DIR, gesture)
        if not os.path.exists(video_dir):
            print(f"Warning: {video_dir} does not exist")
            continue

        for video_file in tqdm(os.listdir(video_dir), desc=gesture):
            if video_file.endswith('.mp4'):
                video_path = os.path.join(video_dir, video_file)
                cap = cv2.VideoCapture(video_path)
                if not cap.isOpened():
                    print(f"Error: Cannot open {video_path}")
                    continue

                total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                frame_interval = max(1, total_frames // FRAMES_PER_VIDEO)
                frame_count = 0
                saved_frames = 0

                while saved_frames < FRAMES_PER_VIDEO:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    if frame_count % frame_interval == 0:
                        frame_path = os.path.join(frame_dir, f'{video_file[:-4]}_frame_{saved_frames}.jpg')
                        cv2.imwrite(frame_path, frame)
                        saved_frames += 1
                    frame_count += 1

                cap.release()
                print(f"Extracted {saved_frames} frames from {video_file}")

    print("✅ Frame extraction complete!")

if __name__ == "__main__":
    extract_frames()