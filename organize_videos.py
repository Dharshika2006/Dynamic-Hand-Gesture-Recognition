import os
import json
import shutil

# Paths
videos_folder = 'videos'  # Where WLASL videos are
output_folder = 'gesture_data'  # Where organized videos will go
nslt_file = 'nslt_100.json'  # Video ID to action ID
wlasl_file = 'WLASL_v0.3.json'  # Video ID to gloss

# Create output folder
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load WLASL JSON to map video IDs to gloss
video_to_gloss = {}
with open(wlasl_file, 'r') as f:
    wlasl_data = json.load(f)

for entry in wlasl_data:
    gloss = entry['gloss']
    for instance in entry['instances']:
        video_id = instance['video_id']
        # Sanitize gloss to avoid invalid folder names
        sanitized_gloss = gloss.replace(' ', '_').replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_').replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_').replace('|', '_')
        video_to_gloss[video_id] = sanitized_gloss

# Load nslt_100.json and organize videos
with open(nslt_file, 'r') as f:
    nslt_data = json.load(f)

unmatched_videos = []
for video_id, metadata in nslt_data.items():
    label = video_to_gloss.get(video_id, 'unknown')  # Default to 'unknown' if not found
    src_video_path = os.path.join(videos_folder, video_id + '.mp4')
    
    if label == 'unknown':
        unmatched_videos.append(video_id)
    
    if os.path.exists(src_video_path):
        label_folder = os.path.join(output_folder, label)
        if not os.path.exists(label_folder):
            os.makedirs(label_folder)
        
        dest_video_path = os.path.join(label_folder, video_id + '.mp4')
        shutil.copy(src_video_path, dest_video_path)
    else:
        print(f"Missing video: {video_id}.mp4")

# Report unmatched videos
if unmatched_videos:
    print(f"Warning: {len(unmatched_videos)} videos had no matching gloss in WLASL_v0.3.json:")
    print(unmatched_videos[:10], "..." if len(unmatched_videos) > 10 else "")

print("✅ Videos organized by gesture!")