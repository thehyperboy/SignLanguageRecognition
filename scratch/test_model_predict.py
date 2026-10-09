import sys
import os
sys.path.insert(0, os.path.abspath("."))

import numpy as np
from src.inference import SignLanguageRecognizer

rec = SignLanguageRecognizer()

# Create dummy sequence of 30 frames with 258 features
# Add some artificial non-zero hand keypoints to simulate a hand gesture
dummy_seq = []
for i in range(30):
    vec = np.random.randn(258).astype(np.float32) * 0.1
    rec.sequence.append(vec)

pred, conf = rec.predict_sequence()
print("Predict result with synthetic sequence:")
print(" - Prediction:", pred)
print(" - Confidence:", conf)

rec.close()
