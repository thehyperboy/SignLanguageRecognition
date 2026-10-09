import sys
import os
sys.path.insert(0, os.path.abspath("."))
import cv2
import time
from src.inference import SignLanguageRecognizer

print("Initializing SignLanguageRecognizer...")
rec = SignLanguageRecognizer()
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Camera 0 could not be opened.")
else:
    print("Camera 0 opened. Testing capture and tracking for 20 frames...")
    for i in range(20):
        ret, frame = cap.read()
        if not ret or frame is None:
            print(f"Frame {i}: Could not read frame")
            break
        res = rec.process_frame(frame)
        p = res["pose_detected"]
        lh = res["left_hand_detected"]
        rh = res["right_hand_detected"]
        buf = res["frames"]
        pred = res["prediction"]
        conf = res["confidence"] * 100
        print(f"Frame {i:02d}: Pose={p} | LH={lh} | RH={rh} | Buffer={buf} | Pred={pred} | Conf={conf:.1f}%")
        time.sleep(0.05)
    cap.release()

rec.close()
print("Camera tracking test finished.")
