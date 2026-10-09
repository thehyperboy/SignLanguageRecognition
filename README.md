# 🖐️ Sign Language Recognition for Accessibility

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.12+-orange.svg)](https://www.tensorflow.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Holistic-teal.svg)](https://developers.google.com/mediapipe)
[![React](https://img.shields.io/badge/React-19-61dafb.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-6-646cff.svg)](https://vitejs.dev/)
[![TailwindCSS](https://img.shields.io/badge/TailwindCSS-v4-38bdf8.svg)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An end-to-end, real-time sign language recognition system designed to bridge communication gaps for the deaf and hard-of-hearing communities. The system combines **MediaPipe Holistic landmark extraction**, a **two-layer LSTM recurrent neural network**, a **low-latency WebSocket streaming API**, and an **interactive React frontend with 60 FPS live tracking and tactile 3D interactions**.

---

## 🌟 Key Features

- **⚡ Real-Time 60 FPS Native Tracking**: Direct hardware-accelerated video rendering with zero camera lag, paired with an optional MediaPipe skeleton mesh overlay.
- **🧠 258-Dimensional Spatial Modeling**: Extracts and normalizes 33 pose landmarks, 21 left-hand landmarks, and 21 right-hand landmarks across temporal 30-frame sliding windows.
- **🎯 2-Layer LSTM Recurrent Neural Network**: Captures motion trajectories across 8 isolated dynamic signs with high confidence and soft argmax smoothing.
- **🔊 Instant Voice Synthesis**: Integrated text-to-speech engine (`pyttsx3`) that vocalizes recognized signs in real-time.
- **🎨 Modern Web Application**:
  - **Live Recognition Studio**: Real-time webcam viewport, neural probability meters, temporal buffer visualization, and recent history feed.
  - **Gesture Library**: Searchable matrix of all 8 supported gestures with practice cards.
  - **Neural Architecture Explorer**: Interactive breakdown of the 258 feature vectors and recurrent LSTM layers.
  - **Accessibility Mission Hub**: Overview of universal communication impact and on-device privacy.
- **🖥️ Dual Frontends**:
  - **Modern React + Vite Frontend** (Port `5173`)
  - **Streamlit Classic Dashboard** (Port `8501`)

---

## 📐 System Architecture

```text
 Webcam Input (60 FPS Native)
       │
       ▼
 [React Web Client / Streamlit]
       │  (WebSocket / HTTP JSON Stream)
       ▼
 [Starlette / Uvicorn API Bridge]
       │
       ▼
 [MediaPipe Holistic Pipeline]
   ├── Pose Landmarks (33 × 4: x, y, z, visibility)  → 132 features
   ├── Left Hand      (21 × 3: x, y, z)              →  63 features
   └── Right Hand     (21 × 3: x, y, z)              →  63 features
                                                    ─────────────
                               Total Spatial Vector:  258 features
       │
       ▼
 [30-Frame Temporal Sliding Buffer] (Shape: 30 × 258)
       │
       ▼
 [2-Layer LSTM Classification Network]
   ├── LSTM Layer 1 (64 units, Dropout 0.2)
   ├── LSTM Layer 2 (32 units, Dropout 0.2)
   ├── Dense Layer  (32 units, ReLU)
   └── Output Dense (8 classes, Softmax)
       │
       ▼
 [Confidence Thresholding (≥ 70%) & Debounce Filter]
       │
       ├── Text Display & HUD Notification
       └── Pyttsx3 Real-Time Speech Synthesis
```

---

## 🤟 Supported Vocabulary

The model currently recognizes 8 isolated sign language gestures:

| Class | Gesture | Description |
|:---:|:---|:---|
| 0 | `hello` | Open palm wave starting near temple |
| 1 | `thank_you` | Flat hand moving forward from chin |
| 2 | `yes` | Nodding fist up and down |
| 3 | `no` | Index and middle finger snapping to thumb |
| 4 | `please` | Flat hand rubbing chest in circular motion |
| 5 | `sorry` | Fist with thumb rubbing circular on chest |
| 6 | `help` | Thumbs up on flat palm moving upwards |
| 7 | `more` | Fingertips and thumbs tapping together |

---

## 📁 Repository Structure

```text
SignLanguageRecognition/
│
├── api_server.py           # High-speed WebSocket / HTTP API backend (Port 8000)
├── app.py                  # Streamlit alternative frontend (Port 8501)
├── requirements.txt        # Python dependencies
│
├── models/                 # Pretrained weights & task files
│   ├── sign_language_lstm_best.keras   # Trained LSTM weights (3.0 MB)
│   ├── holistic_landmarker.task        # MediaPipe holistic model (13.6 MB)
│   └── training_history.json           # Validation metrics
│
├── src/                    # Core Python ML & Vision Modules
│   ├── inference.py        # SignLanguageRecognizer pipeline (buffer, prediction, overlay)
│   ├── model.py            # Keras LSTM architecture definition
│   ├── train.py            # Training pipeline with EarlyStopping & ModelCheckpoint
│   ├── extract_landmarks.py# MediaPipe feature extraction (258 dimensions)
│   ├── preprocess.py       # Sequence formatting and normalization
│   ├── speech.py           # Asynchronous pyttsx3 text-to-speech
│   └── evaluate.py         # Confusion matrix and test suite
│
├── frontend/               # Modern React + Vite Web Application
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   └── src/
│       ├── App.jsx                     # Root application & WebSocket coordinator
│       ├── index.css                   # Custom theme & animation styles
│       └── components/
│           ├── Navbar.jsx              # 3D motion graphic navigation bar
│           ├── TrackerPage.jsx         # 60 FPS Live video tracking studio
│           ├── GestureLibraryPage.jsx  # Interactive 8-gesture directory
│           ├── ArchitecturePage.jsx    # Model inspector & feature breakdown
│           └── AccessibilityPage.jsx   # Mission & accessibility impact
│
└── scratch/                # Verification and benchmark scripts
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- **Python 3.10+** (Tested on Python 3.10, 3.11, 3.12)
- **Node.js 18+** & npm (for the modern React frontend)
- A working webcam

---

### 2. Python Backend Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/<your-username>/SignLanguageRecognition.git
   cd SignLanguageRecognition
   ```

2. **Create and activate a virtual environment**:
   ```bash
   # Windows PowerShell
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

### 3. Launch the Application

#### Option A: Modern React + Vite App (Recommended)

1. **Start the Python API Server**:
   ```bash
   python api_server.py
   ```
   *Runs at `http://localhost:8000` with WebSocket support at `ws://localhost:8000/ws/stream`.*

2. **In a second terminal, start the React frontend**:
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   *Opens at `http://localhost:5173`.*

#### Option B: Classic Streamlit App

Run the standalone Streamlit dashboard:
```bash
streamlit run app.py
```
*Opens at `http://localhost:8501`.*

---

## 🧪 Training & Customization

To train the LSTM on your own gesture dataset:

1. **Collect samples**:
   ```bash
   python src/collect_data.py
   ```
2. **Extract landmarks**:
   ```bash
   python src/extract_landmarks.py
   ```
3. **Train the LSTM model**:
   ```bash
   python src/train.py
   ```
4. **Evaluate performance**:
   ```bash
   python src/evaluate.py
   ```

---

## 🔒 Privacy & On-Device Processing

All video frames are processed **locally** in real-time. No video data, facial images, or personal biometrics are recorded, stored, or transmitted over external networks.

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
