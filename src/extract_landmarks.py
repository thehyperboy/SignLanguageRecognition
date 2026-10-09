"""
Landmark Extraction Module
--------------------------
Stage: Step 3A - Landmark Keypoint Extraction

Extracts pose, left-hand, and right-hand landmarks from MediaPipe Holistic results,
flattening them into a single 1D numerical numpy array of constant size (258 features).

Feature Breakdown:
- Pose Landmarks       : 33 points x 4 values (x, y, z, visibility) = 132 features
- Left Hand Landmarks  : 21 points x 3 values (x, y, z)             = 63 features
- Right Hand Landmarks : 21 points x 3 values (x, y, z)             = 63 features
-----------------------------------------------------------------------------------
Total Feature Vector Dimension per frame                             = 258 features

Note: Normalization will be performed in the preprocessing stage before LSTM training.
"""

import numpy as np

# Total constant feature vector dimension per frame
FEATURE_DIMENSION = 258


def extract_keypoints(results) -> np.ndarray:
    """
    Extract keypoint coordinates from MediaPipe Holistic detection results.

    Maintains a consistent 258-element 1D feature vector length for every frame.
    If a hand or pose is not detected, its positions are padded with zeros.

    Args:
        results: MediaPipe Holistic process results object.

    Returns:
        np.ndarray: 1D numpy array of shape (258,) and dtype float32.
    """
    if results is None:
        return np.zeros(FEATURE_DIMENSION, dtype=np.float32)

    # 1. Pose landmarks (33 points * 4 coordinates = 132 features)
    pose = np.zeros(33 * 4, dtype=np.float32)
    if hasattr(results, "pose_landmarks") and results.pose_landmarks:
        raw_pose = results.pose_landmarks
        if hasattr(raw_pose, "landmark"):
            lms = raw_pose.landmark
        elif isinstance(raw_pose, list):
            lms = raw_pose[0] if (len(raw_pose) > 0 and isinstance(raw_pose[0], list)) else raw_pose
        else:
            lms = []
        if lms:
            pose_arr = np.zeros((33, 4), dtype=np.float32)
            for i in range(min(len(lms), 33)):
                lm = lms[i]
                pose_arr[i] = [
                    getattr(lm, "x", 0.0),
                    getattr(lm, "y", 0.0),
                    getattr(lm, "z", 0.0),
                    getattr(lm, "visibility", 0.0) if getattr(lm, "visibility", None) is not None else 0.0,
                ]
            pose = pose_arr.flatten()

    # 2. Left Hand landmarks (21 points * 3 coordinates = 63 features)
    lh = np.zeros(21 * 3, dtype=np.float32)
    if hasattr(results, "left_hand_landmarks") and results.left_hand_landmarks:
        raw_lh = results.left_hand_landmarks
        if hasattr(raw_lh, "landmark"):
            lms = raw_lh.landmark
        elif isinstance(raw_lh, list):
            lms = raw_lh[0] if (len(raw_lh) > 0 and isinstance(raw_lh[0], list)) else raw_lh
        else:
            lms = []
        if lms:
            lh_arr = np.zeros((21, 3), dtype=np.float32)
            for i in range(min(len(lms), 21)):
                lm = lms[i]
                lh_arr[i] = [
                    getattr(lm, "x", 0.0),
                    getattr(lm, "y", 0.0),
                    getattr(lm, "z", 0.0),
                ]
            lh = lh_arr.flatten()

    # 3. Right Hand landmarks (21 points * 3 coordinates = 63 features)
    rh = np.zeros(21 * 3, dtype=np.float32)
    if hasattr(results, "right_hand_landmarks") and results.right_hand_landmarks:
        raw_rh = results.right_hand_landmarks
        if hasattr(raw_rh, "landmark"):
            lms = raw_rh.landmark
        elif isinstance(raw_rh, list):
            lms = raw_rh[0] if (len(raw_rh) > 0 and isinstance(raw_rh[0], list)) else raw_rh
        else:
            lms = []
        if lms:
            rh_arr = np.zeros((21, 3), dtype=np.float32)
            for i in range(min(len(lms), 21)):
                lm = lms[i]
                rh_arr[i] = [
                    getattr(lm, "x", 0.0),
                    getattr(lm, "y", 0.0),
                    getattr(lm, "z", 0.0),
                ]
            rh = rh_arr.flatten()

    # Concatenate in order: Pose -> Left Hand -> Right Hand (Total = 258)
    return np.concatenate([pose, lh, rh]).astype(np.float32)
