# 🖐️ Dynamic Hand Gesture Recognition using WLASL Dataset and MediaPipe-based Models

## 📘 Overview
This project focuses on **real-time dynamic hand gesture recognition** using the **WLASL dataset** and **MediaPipe** for hand landmark detection.  
It combines **computer vision** and **machine learning** to classify hand gestures from live video input accurately.  

The goal is to interpret sign language gestures dynamically — building a foundation for assistive technologies and gesture-based human-computer interaction.

---

## 🚀 Features
- Real-time hand tracking using **MediaPipe Hands**
- Custom **Machine Learning model** trained on **WLASL (Word-Level American Sign Language)** dataset
- Dynamic gesture recognition and classification
- Modular and extensible Python scripts for training and testing
- Lightweight and runs in real-time on most systems

---

## 🧠 Tech Stack
- **Programming Language:** Python  
- **Libraries:** MediaPipe, OpenCV, TensorFlow / scikit-learn, NumPy, Pandas  
- **Dataset:** [WLASL Processed Dataset (Kaggle)](https://www.kaggle.com/datasets/risangbaskoro/wlasl-processed)

---

## 🗂️ Dataset
Due to GitHub’s **100 MB file size limit**, the dataset and trained model files are **not included** in this repository.  
You can download the dataset separately from Kaggle here:  
👉 [https://www.kaggle.com/datasets/risangbaskoro/wlasl-processed](https://www.kaggle.com/datasets/risangbaskoro/wlasl-processed)

After downloading, place the dataset folder inside your project directory:
```
project_root/
├── app.py
├── test_cam.py
├── model.pkl
├── requirements.txt
├── README.md
└── wlasl_dataset/
```

## 📸 Output Example
When the script is running, you’ll see:
- Real-time video feed from your webcam  
- Detected hand landmarks using MediaPipe  
- Recognized gesture displayed on-screen  

---

## 🧩 Future Improvements
- Integrate dynamic sequence models (LSTM/GRU) for improved accuracy  
- Extend dataset support for more sign languages  
- Build a GUI or web interface for accessibility  

---

## 👨‍💻 Author
**Dharshika Katta**  
B.Tech in Computer Science (AI & ML)  
Passionate about AI, computer vision, and building real-world intelligent systems.
