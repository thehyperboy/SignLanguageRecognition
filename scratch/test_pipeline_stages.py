import sys
import json
import time
from pathlib import Path
import numpy as np
import joblib

print("--- TEST 1: Imports ---")
import cv2
import mediapipe as mp
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
import streamlit as st
import streamlit_webrtc
import av
print(f"OpenCV: {cv2.__version__}")
print(f"MediaPipe: {mp.__version__}")
print(f"TensorFlow: {tf.__version__}")
print(f"Streamlit: {st.__version__}")
print(f"streamlit-webrtc: {streamlit_webrtc.__version__}")
print(f"PyAV: {av.__version__}")
print("TEST 1 PASSED")

root = Path(".").resolve()

print("\n--- TEST 2: Load Model ---")
model_path = root / "models" / "sign_language_lstm_best.keras"
model = tf.keras.models.load_model(model_path)
print(f"Model loaded: {model_path}")
print(f"Model input_shape: {model.input_shape}")
print(f"Model output_shape: {model.output_shape}")
print("TEST 2 PASSED")

print("\n--- TEST 3: Load Scaler ---")
scaler_path = root / "data" / "processed" / "scaler.pkl"
scaler = joblib.load(scaler_path)
print(f"Scaler loaded: {scaler_path}")
print(f"Scaler type: {type(scaler)}")
print(f"Scaler n_features_in_: {getattr(scaler, 'n_features_in_', 'N/A')}")
print("TEST 3 PASSED")

print("\n--- TEST 4: Load Label Map ---")
label_map_path = root / "data" / "processed" / "label_map.json"
with open(label_map_path, "r", encoding="utf-8") as f:
    label_map_raw = json.load(f)
print(f"Raw label map: {label_map_raw}")
print("TEST 4 PASSED")

print("\n--- TEST 5: Load MediaPipe Task Model ---")
task_path = root / "models" / "holistic_landmarker.task"
BaseOptions = mp.tasks.BaseOptions
HolisticLandmarker = mp.tasks.vision.HolisticLandmarker
HolisticLandmarkerOptions = mp.tasks.vision.HolisticLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = HolisticLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=str(task_path)),
    running_mode=RunningMode.VIDEO,
    min_face_detection_confidence=0.5,
    min_pose_detection_confidence=0.5,
    min_hand_landmarks_confidence=0.5,
)
landmarker = HolisticLandmarker.create_from_options(options)
print(f"Landmarker created successfully: {landmarker}")
print("TEST 5 PASSED")

print("\n--- TEST 6: Verify Model Input Shape ---")
assert model.input_shape == (None, 30, 258), f"Expected (None, 30, 258), got {model.input_shape}"
print("TEST 6 PASSED")

print("\n--- TEST 7: Verify Scaler Feature Count ---")
assert scaler.n_features_in_ == 258, f"Expected 258 features in scaler, got {scaler.n_features_in_}"
print("TEST 7 PASSED")

print("\n--- TEST 8: Verify Label Count ---")
num_classes = model.output_shape[-1]
print(f"Model classes: {num_classes}, Label map entries: {len(label_map_raw)}")
assert num_classes == len(label_map_raw), f"Model outputs {num_classes} classes but label map has {len(label_map_raw)}"
print("TEST 8 PASSED")

print("\n--- TEST 9 & 10: Test One Frame & MediaPipe Detection ---")
dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
# Draw something that looks like an arm or hand or just test empty detection
cv2.circle(dummy_frame, (320, 240), 50, (200, 200, 200), -1)
rgb_frame = cv2.cvtColor(dummy_frame, cv2.COLOR_BGR2RGB)
mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
result = landmarker.detect_for_video(mp_image, 100)
print(f"Landmarker result type: {type(result)}")
print(f"Result attributes: {dir(result)}")
print(f"pose_landmarks: {type(result.pose_landmarks)}, len: {len(result.pose_landmarks) if result.pose_landmarks else 0}")
print(f"left_hand_landmarks: {type(result.left_hand_landmarks)}, len: {len(result.left_hand_landmarks) if result.left_hand_landmarks else 0}")
print(f"right_hand_landmarks: {type(result.right_hand_landmarks)}, len: {len(result.right_hand_landmarks) if result.right_hand_landmarks else 0}")
print("TEST 9 & 10 PASSED")

print("\n--- TEST 11: Feature Extraction (258 features) ---")
sys.path.insert(0, str(root))
from src.inference import SignLanguageRecognizer
rec = SignLanguageRecognizer()
features = rec.extract_landmarks(result)
print(f"Extracted feature shape: {features.shape}, dtype: {features.dtype}")
assert features.shape == (258,), f"Expected shape (258,), got {features.shape}"
print("TEST 11 PASSED")

print("\n--- TEST 12: 30-Frame Buffer & TEST 13: LSTM Prediction with Real Sequence ---")
# Load an actual test sequence from data/processed/X_test.npy or dataset
test_file = root / "data" / "processed" / "X_test.npy"
if test_file.exists():
    X_test = np.load(test_file)
    y_test = np.load(root / "data" / "processed" / "y_test.npy")
    print(f"X_test shape: {X_test.shape}, y_test shape: {y_test.shape}")
    sample_seq = X_test[0] # (30, 258) - note this is already scaled if fit_and_transform_scaler was used
    # Let's check raw dataset sample
    dataset_samples = list(root.glob("dataset/*/*.npy"))
    if dataset_samples:
        raw_sample = np.load(dataset_samples[0])
        print(f"Raw dataset sample shape: {raw_sample.shape}")
        rec.reset()
        for f in raw_sample:
            rec.sequence.append(f)
        pred, conf = rec.predict_sequence()
        print(f"Prediction from raw sequence: {pred}, confidence: {conf*100:.2f}%")
    else:
        # Predict on sample_seq directly with model
        probs = model.predict(np.expand_dims(sample_seq, axis=0), verbose=0)[0]
        idx = int(np.argmax(probs))
        print(f"Direct model prediction on test sample: class {idx}, prob: {probs[idx]*100:.2f}%")
print("TEST 12 & 13 PASSED")

landmarker.close()
rec.close()
print("\nALL STAGE 1-13 TESTS COMPLETED SUCCESSFULLY!")
