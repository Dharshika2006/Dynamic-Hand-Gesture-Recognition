import json

# Path to JSON file
mapping_file = 'nslt_100.json'

# Load and print JSON structure
with open(mapping_file, 'r') as f:
    data = json.load(f)

# Print basic info
print("Type of data:", type(data))
print("Number of entries:", len(data))
print("Sample keys:", list(data.keys())[:5])  # First 5 keys

# Print sample values
print("Sample values (first 2 entries):")
for key in list(data.keys())[:2]:
    print(f"Key: {key}, Value: {data[key]}")