import os
import cv2
import csv
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

dataset_path = 'gesture_data'

gesture = input("Enter gesture folder name to preview: ").strip()
folder_path = os.path.join(dataset_path, gesture)
csv_path = os.path.join(folder_path, f"{gesture}_landmarks.csv")

# Show images
if os.path.exists(folder_path):
    images = [img for img in os.listdir(folder_path) if img.endswith('.jpg') or img.endswith('.png')]
    for img_file in images:
        img_path = os.path.join(folder_path, img_file)
        img = cv2.imread(img_path)
        if img is not None:
            cv2.imshow(f"{gesture} - {img_file}", img)
            if cv2.waitKey(500) & 0xFF == ord('q'):
                break
    cv2.destroyAllWindows()
else:
    print(f"No folder found for: {gesture}")

# Plot one landmark sample in 3D
if os.path.exists(csv_path):
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)
        if rows:
            sample = [float(val) for val in rows[0]]
            x = sample[0::3]
            y = sample[1::3]
            z = sample[2::3]

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(x, y, z, c='blue', marker='o')
            for i in range(21):
                ax.text(x[i], y[i], z[i], f"{i}", size=10)
            ax.set_title(f"3D Landmarks for gesture: {gesture}")
            plt.show()
        else:
            print("CSV file is empty.")
else:
    print("Landmark CSV file not found.")
