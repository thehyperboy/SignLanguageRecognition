import sys
import os
sys.path.insert(0, os.path.abspath("."))
import cv2
import mediapipe as mp
import numpy as np

# Load landmarker
task_path = "models/holistic_landmarker.task"
BaseOptions = mp.tasks.BaseOptions
HolisticLandmarker = mp.tasks.vision.HolisticLandmarker
HolisticLandmarkerOptions = mp.tasks.vision.HolisticLandmarkerOptions
RunningMode = mp.tasks.vision.RunningMode

options = HolisticLandmarkerOptions(
    base_options=BaseOptions(model_asset_path=task_path),
    running_mode=RunningMode.IMAGE,
)
landmarker = HolisticLandmarker.create_from_options(options)

# Capture 1 frame
cap = cv2.VideoCapture(0)
for _ in range(5): # warm up
    ret, frame = cap.read()
cap.release()

if ret and frame is not None:
    frame = cv2.resize(frame, (640, 480))
    # Test 1: Unflipped (same as collect_data.py)
    rgb_raw = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    mp_img_raw = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_raw)
    res_raw = landmarker.detect(mp_img_raw)

    # Test 2: Flipped (same as app.py)
    flipped = cv2.flip(frame, 1)
    rgb_flip = cv2.cvtColor(flipped, cv2.COLOR_BGR2RGB)
    mp_img_flip = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_flip)
    res_flip = landmarker.detect(mp_img_flip)

    print("RAW (unflipped):")
    print(" - Pose:", len(res_raw.pose_landmarks) if res_raw.pose_landmarks else 0)
    print(" - LH:", len(res_raw.left_hand_landmarks) if res_raw.left_hand_landmarks else 0)
    print(" - RH:", len(res_raw.right_hand_landmarks) if res_raw.right_hand_landmarks else 0)

    print("FLIPPED:")
    print(" - Pose:", len(res_flip.pose_landmarks) if res_flip.pose_landmarks else 0)
    print(" - LH:", len(res_flip.left_hand_landmarks) if res_flip.left_hand_landmarks else 0)
    print(" - RH:", len(res_flip.right_hand_landmarks) if res_flip.right_hand_landmarks else 0)
else:
    print("Could not grab frame from camera.")

landmarker.close()
