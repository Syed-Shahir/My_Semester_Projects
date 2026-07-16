# Smart Eyewear Recommender System

An AI-driven computer vision application designed to provide personalized eyewear recommendations by analyzing facial features in real-time. This system tracks facial landmarks to determine face shape and calculates precise anthropometric measurements to suggest optimal frame sizes and styles.

## Key Features
* **Real-time Facial Analysis**: Utilizes MediaPipe Face Mesh for accurate, low-latency tracking of facial landmarks.
* **Automated Anthropometry**: Instantly calculates critical metrics, including Pupillary Distance (PD), face width, jaw width, and temple length.
* **Face Shape Classification**: Categorizes users into face shapes (e.g., Oval, Round, Square, Heart) using geometric ratios.
* **Intelligent Recommendations**: Suggests ideal frame types and dimensions based on standard optometric guidelines.
* **Virtual Try-On**: Features an interactive interface to overlay digital frames onto the live camera feed for a preview.
* **Manual Recalibration**: Supports user-defined IPD (Inter-Pupillary Distance) input to improve measurement accuracy.

## Tech Stack
* **Language**: Python 3.10
* **Computer Vision**: OpenCV, MediaPipe
* **GUI Framework**: PyQt5
* **Math/Logic**: NumPy

## Installation & Setup
Due to specific dependency requirements for the computer vision backends, it is highly recommended to use a dedicated environment to avoid version conflicts.

### 1. Create and Activate Environment
```bash
conda create -n eyewear_recommender python=3.10 -y
conda activate eyewear_recommender
pip install numpy==1.26.4
pip install opencv-python==4.9.0.80
pip install mediapipe==0.10.14
pip install protobuf==4.25.3
pip install PyQt5
