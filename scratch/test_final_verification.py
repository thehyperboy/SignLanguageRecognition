import sys
import os
sys.path.insert(0, os.path.abspath("."))
import cv2
import numpy as np
from src.inference import SignLanguageRecognizer

print("--- STEP 1: Initializing SignLanguageRecognizer ---")
rec = SignLanguageRecognizer()
print("SignLanguageRecognizer initialized successfully.")

print("\n--- STEP 2: Testing Frame Processing & Landmarking ---")
dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
res = rec.process_frame(dummy_frame, mirror_display=True)

assert "annotated_frame" in res, "Missing annotated_frame in res"
assert res["annotated_frame"].shape == (480, 640, 3), f"Wrong shape: {res['annotated_frame'].shape}"
assert "prediction" in res, "Missing prediction in res"
assert "confidence" in res, "Missing confidence in res"
assert "hand_detected" in res, "Missing hand_detected in res"
print("Blank frame processed cleanly.")

print("\n--- STEP 3: Testing Predictions on Real Dataset Sequences ---")
for sign in ["hello", "thank_you", "yes", "no", "help", "love"]:
    sample_file = f"dataset/{sign}/sequence_001.npy"
    if os.path.exists(sample_file):
        seq = np.load(sample_file) # (30, 258)
        rec.reset()
        for frame_feat in seq:
            rec.sequence.append(frame_feat)
        pred, conf = rec.predict_sequence()
        print(f"Sign: {sign:<10} -> Model Predicted: {pred:<10} | Confidence: {conf*100:.2f}%")
        assert pred == sign, f"Expected {sign}, got {pred}"

print("\n--- STEP 4: Testing Dominant Hand Auto-Mapping for Left-Handed Signers ---")
# hello sequence with RH features moved to LH (simulating left-handed signer)
hello_seq = np.load("dataset/hello/sequence_001.npy")
lh_hello_seq = hello_seq.copy()
lh_hello_seq[:, 132:195] = hello_seq[:, 195:258]
lh_hello_seq[:, 195:258] = 0.0

rec.reset()
for frame_feat in lh_hello_seq:
    rec.sequence.append(frame_feat)
pred, conf = rec.predict_sequence()
print(f"Left-Handed 'hello' -> Model Predicted: {pred:<10} | Confidence: {conf*100:.2f}%")
assert pred == "hello", f"Expected hello for left-handed sign, got {pred}"

rec.close()
print("\nALL VERIFICATION CHECKS PASSED WITH 100% ACCURACY!")
