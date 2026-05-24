import json

# Path to WLASL JSON file
mapping_file = 'WLASL_v0.3.json'

# Load and print JSON structure
with open(mapping_file, 'r') as f:
    data = json.load(f)

# Print basic info
print("Type of data:", type(data))
print("Number of entries:", len(data))
print("Sample entries (first 2):")
for entry in data[:2]:
    print(entry)