import sys
import os
sys.path.insert(0, os.path.abspath("."))

import cv2
import numpy as np
from src.inference import SignLanguageRecognizer

print("Initializing SignLanguageRecognizer...")
recognizer = SignLanguageRecognizer()
print("Success! Models loaded:")
print(" - LSTM Model Input Shape:", recognizer.model.input_shape)
print(" - Label Map:", recognizer.label_map)

# Process 35 blank frames to verify buffer and output keys
for i in range(35):
    frame = np.zeros((480, 640, 3), dtype=np.uint8)
    res = recognizer.process_frame(frame)

print("Frame 35 Result:")
print(" - prediction:", res["prediction"])
print(" - confidence:", res["confidence"])
print(" - ready:", res["ready"])
print(" - frames:", res["frames"])
print(" - hand_detected:", res["hand_detected"])

recognizer.close()
print("Pipeline test completed cleanly.")
