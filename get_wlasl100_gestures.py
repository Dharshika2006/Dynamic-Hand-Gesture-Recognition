import json

nslt_file = 'nslt_100.json'
wlasl_file = 'WLASL_v0.3.json'

# Load nslt_100.json
with open(nslt_file, 'r') as f:
    nslt_data = json.load(f)

# Get unique action IDs
action_ids = set(metadata['action'][0] for metadata in nslt_data.values())

# Load WLASL JSON to map video IDs to gloss
video_to_gloss = {}
glosses = set()
with open(wlasl_file, 'r') as f:
    wlasl_data = json.load(f)

for entry in wlasl_data:
    gloss = entry['gloss']
    for instance in entry['instances']:
        video_id = instance['video_id']
        video_to_gloss[video_id] = gloss

# Map action IDs to glosses via video IDs
action_to_gloss = {}
for video_id, metadata in nslt_data.items():
    action_id = metadata['action'][0]
    gloss = video_to_gloss.get(video_id, None)
    if gloss:
        action_to_gloss[action_id] = gloss
        glosses.add(gloss)

print("WLASL100 Gestures:", sorted(glosses))
print("Number of gestures:", len(glosses))