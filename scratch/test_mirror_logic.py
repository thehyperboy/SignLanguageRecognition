import sys
import os
sys.path.insert(0, os.path.abspath("."))
import cv2
import numpy as np
import mediapipe as mp
import joblib, json
import tensorflow as tf

# Load resources
model = tf.keras.models.load_model("models/sign_language_lstm_best.keras")
scaler = joblib.load("data/processed/scaler.pkl")
with open("data/processed/label_map.json") as f:
    label_map = json.load(f)
inv_map = {v: k for k, v in label_map.items()}

# Verify on a sample
sample = np.load("dataset/hello/sequence_001.npy")
scaled = scaler.transform(sample)
p = model.predict(np.expand_dims(scaled, 0), verbose=0)[0]
idx = np.argmax(p)
print(f"Sample prediction: {inv_map[idx]} ({p[idx]*100:.2f}%)")
print("Verification complete.")
