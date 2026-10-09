import sys
import os
sys.path.insert(0, os.path.abspath("."))

import cv2
import numpy as np
import mediapipe as mp
from src.inference import SignLanguageRecognizer

print("Initializing SignLanguageRecognizer...")
rec = SignLanguageRecognizer()
print("SignLanguageRecognizer initialized successfully!")

# Create a blank 640x480 frame
frame = np.zeros((480, 640, 3), dtype=np.uint8)

print("Processing blank frame...")
res = rec.process_frame(frame)
print("Blank frame processed. Result keys:", res.keys())
print("Prediction:", res.get("prediction"), "Ready:", res.get("ready"), "Frames:", res.get("frames"))

rec.close()
print("Recognizer closed successfully.")
