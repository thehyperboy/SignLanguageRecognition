"""
Sign Language Recognition - Dataset Collection System
------------------------------------------------------
Stage: Step 3A - Landmark Sequence Dataset Collection

Captures webcam frames, extracts MediaPipe Holistic keypoints (Pose, Left Hand, Right Hand),
packages 30 consecutive frames into a 1D feature array (shape: 30x258), and saves sequences
as zero-padded NumPy .npy files (e.g., dataset/hello/sequence_001.npy).

Controls:
  Q -> Quit program
  S -> Skip current sign
"""

import os
import sys
import time
from pathlib import Path
import cv2
import numpy as np
import mediapipe as mp

from src.extract_landmarks import extract_keypoints, FEATURE_DIMENSION

# ==============================================================================
# TOP-LEVEL CONFIGURATION
# ==============================================================================

DATASET_PATH = Path("dataset")

# List of target sign classes for dataset collection
SIGNS = ["hello"]

# Sequence recording settings
SEQUENCE_LENGTH = 30       # Number of consecutive frames per sequence
SEQUENCES_PER_SIGN = 2     # Number of sequences to record per sign



# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def create_directories(dataset_path: Path, signs: list) -> None:
    """Automatically create missing sign folders under dataset directory."""
    for sign in signs:
        sign_dir = dataset_path / sign
        sign_dir.mkdir(parents=True, exist_ok=True)


def get_next_sequence_number(sign_dir: Path) -> int:
    """
    Find existing sequence_XXX.npy files and return the next sequence number.
    Ensures dataset collection can resume without overwriting existing files.
    """
    if not sign_dir.exists():
        return 1

    existing_files = list(sign_dir.glob("sequence_*.npy"))
    if not existing_files:
        return 1

    sequence_nums = []
    for filepath in existing_files:
        stem = filepath.stem  # e.g., "sequence_005"
        parts = stem.split("_")
        if len(parts) >= 2 and parts[-1].isdigit():
            sequence_nums.append(int(parts[-1]))

    return max(sequence_nums) + 1 if sequence_nums else 1


def validate_sequence(sequence_array: np.ndarray, expected_length: int, expected_dim: int) -> bool:
    """
    Validate data quality of sequence array before saving.

    Checks:
      1. Expected shape (SEQUENCE_LENGTH, FEATURE_DIMENSION).
      2. No NaN values.
      3. No Infinite values.
      4. Valid numeric data type.
    """
    if sequence_array is None:
        print(" [VALIDATION FAILED] Sequence array is None.")
        return False

    expected_shape = (expected_length, expected_dim)
    if sequence_array.shape != expected_shape:
        print(f" [VALIDATION FAILED] Invalid shape: {sequence_array.shape}, expected {expected_shape}.")
        return False

    if np.isnan(sequence_array).any():
        print(" [VALIDATION FAILED] Array contains NaN values.")
        return False

    if np.isinf(sequence_array).any():
        print(" [VALIDATION FAILED] Array contains Infinite values.")
        return False

    if not np.issubdtype(sequence_array.dtype, np.number):
        print(f" [VALIDATION FAILED] Non-numeric data type: {sequence_array.dtype}.")
        return False

    return True


def initialize_mediapipe():
    """Initialize MediaPipe Holistic detector cleanly."""
    if hasattr(mp, "solutions") and hasattr(mp.solutions, "holistic"):
        mp_holistic = mp.solutions.holistic
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles

        try:
            holistic = mp_holistic.Holistic(
                static_image_mode=False,
                model_complexity=1,
                smooth_landmarks=True,
                enable_segmentation=False,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
            )
            return holistic, mp_drawing, mp_drawing_styles, mp_holistic
        except Exception as exc:
            print(f"ERROR: Failed to initialize MediaPipe Holistic: {exc}")
            raise
    else:
        raise RuntimeError("MediaPipe Solutions Holistic API is not accessible in current environment.")


# ==============================================================================
# MAIN COLLECTION PIPELINE
# ==============================================================================

def main():
    """Run real-time webcam dataset collection workflow."""
    print("=" * 65)
    print("SIGN LANGUAGE RECOGNITION - DATASET COLLECTION SYSTEM")
    print("=" * 65)
    print(f"Signs to Collect   : {SIGNS}")
    print(f"Sequences per Sign : {SEQUENCES_PER_SIGN}")
    print(f"Sequence Length    : {SEQUENCE_LENGTH} frames")
    print(f"Feature Dimension  : {FEATURE_DIMENSION} features/frame")
    print(f"Dataset Location   : {DATASET_PATH.resolve()}")
    print("=" * 65)

    create_directories(DATASET_PATH, SIGNS)

    try:
        holistic, mp_drawing, mp_drawing_styles, mp_holistic = initialize_mediapipe()
    except Exception as exc:
        print(f"CRITICAL ERROR initializing MediaPipe: {exc}")
        sys.exit(1)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("ERROR: Could not open default webcam (index 0).")
        print("Please check camera connections and Windows privacy permissions.")
        sys.exit(1)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    window_name = "Sign Language Dataset Collection"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    summary_stats = {}

    try:
        for sign_idx, sign in enumerate(SIGNS, 1):
            sign_dir = DATASET_PATH / sign
            start_seq_num = get_next_sequence_number(sign_dir)
            target_end_num = start_seq_num + SEQUENCES_PER_SIGN - 1

            print(f"\n[{sign_idx}/{len(SIGNS)}] TARGET SIGN: '{sign.upper()}'")
            print(f"     Recording sequences {start_seq_num:03d} to {target_end_num:03d}...")

            skip_current_sign = False
            seq_recorded_count = 0

            for seq_num in range(start_seq_num, start_seq_num + SEQUENCES_PER_SIGN):
                if skip_current_sign:
                    break

                # -------------------------------------------------------------
                # 1. COUNTDOWN PHASE (Get Ready)
                # -------------------------------------------------------------
                countdown_seconds = 2
                countdown_start = time.perf_counter()

                while time.perf_counter() - countdown_start < countdown_seconds:
                    ret, frame = cap.read()
                    if not ret or frame is None:
                        break

                    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image_rgb.flags.writeable = False
                    results = holistic.process(image_rgb)
                    image_rgb.flags.writeable = True

                    # Draw landmarks live so user can position themselves
                    if results.pose_landmarks:
                        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
                    if results.left_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                    if results.right_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

                    time_remaining = max(1, int(np.ceil(countdown_seconds - (time.perf_counter() - countdown_start))))

                    # Display Countdown UI
                    cv2.putText(
                        frame,
                        f"GET READY FOR: {sign.upper()}",
                        (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (0, 255, 255),
                        2,
                        cv2.LINE_AA,
                    )
                    cv2.putText(
                        frame,
                        f"Sequence: {seq_num:03d} / {target_end_num:03d}",
                        (20, 75),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.65,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA,
                    )
                    cv2.putText(
                        frame,
                        f"RECORDING IN: {time_remaining}s",
                        (20, 120),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1.0,
                        (0, 165, 255),
                        3,
                        cv2.LINE_AA,
                    )
                    cv2.putText(
                        frame,
                        "Press Q to Quit | Press S to Skip",
                        (20, 160),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (200, 200, 200),
                        1,
                        cv2.LINE_AA,
                    )

                    cv2.imshow(window_name, frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key in (ord("q"), ord("Q")):
                        print("\nUser pressed 'Q'. Quitting dataset collection...")
                        return
                    if key in (ord("s"), ord("S")):
                        print(f"\nUser pressed 'S'. Skipping sign '{sign.upper()}'...")
                        skip_current_sign = True
                        break

                if skip_current_sign:
                    break

                # -------------------------------------------------------------
                # 2. SEQUENCE CAPTURE PHASE (30 Frames)
                # -------------------------------------------------------------
                sequence_frames = []

                for frame_num in range(1, SEQUENCE_LENGTH + 1):
                    ret, frame = cap.read()
                    if not ret or frame is None:
                        print(" [ERROR] Failed to capture webcam frame.")
                        break

                    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image_rgb.flags.writeable = False
                    results = holistic.process(image_rgb)
                    image_rgb.flags.writeable = True

                    # Extract numerical landmarks (258 features)
                    keypoints = extract_keypoints(results)
                    sequence_frames.append(keypoints)

                    # Landmark detection flags
                    pose_det = "DETECTED" if results.pose_landmarks else "NOT DETECTED"
                    lh_det = "DETECTED" if results.left_hand_landmarks else "NOT DETECTED"
                    rh_det = "DETECTED" if results.right_hand_landmarks else "NOT DETECTED"

                    # Draw landmarks on frame
                    if results.pose_landmarks:
                        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS)
                    if results.left_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                    if results.right_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

                    # Overlay Recording Status Display
                    cv2.putText(
                        frame,
                        f"SIGN: {sign.upper()}",
                        (20, 35),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.75,
                        (0, 0, 255),
                        2,
                        cv2.LINE_AA,
                    )
                    cv2.putText(
                        frame,
                        f"Sequence: {seq_num:03d} / {target_end_num:03d}",
                        (20, 65),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (255, 255, 255),
                        2,
                        cv2.LINE_AA,
                    )
                    cv2.putText(
                        frame,
                        f"Frame: {frame_num:02d} / {SEQUENCE_LENGTH:02d}",
                        (20, 95),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.6,
                        (0, 255, 0),
                        2,
                        cv2.LINE_AA,
                    )

                    cv2.putText(
                        frame,
                        f"Pose: {pose_det}",
                        (20, 130),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (0, 255, 0) if pose_det == "DETECTED" else (0, 0, 255),
                        2,
                        cv2.LINE_AA,
                    )
                    cv2.putText(
                        frame,
                        f"Left Hand: {lh_det}",
                        (20, 155),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (0, 255, 0) if lh_det == "DETECTED" else (0, 0, 255),
                        2,
                        cv2.LINE_AA,
                    )
                    cv2.putText(
                        frame,
                        f"Right Hand: {rh_det}",
                        (20, 180),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (0, 255, 0) if rh_det == "DETECTED" else (0, 0, 255),
                        2,
                        cv2.LINE_AA,
                    )

                    cv2.putText(
                        frame,
                        "Press Q to Quit | Press S to Skip",
                        (20, 215),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.55,
                        (200, 200, 200),
                        1,
                        cv2.LINE_AA,
                    )

                    cv2.imshow(window_name, frame)
                    key = cv2.waitKey(1) & 0xFF
                    if key in (ord("q"), ord("Q")):
                        print("\nUser pressed 'Q'. Quitting dataset collection...")
                        return
                    if key in (ord("s"), ord("S")):
                        print(f"\nUser pressed 'S'. Skipping sign '{sign.upper()}'...")
                        skip_current_sign = True
                        break

                if skip_current_sign:
                    break

                # -------------------------------------------------------------
                # 3. SAVE SEQUENCE TO .NPY FILE
                # -------------------------------------------------------------
                seq_array = np.array(sequence_frames, dtype=np.float32)

                # Validate shape and data quality
                if validate_sequence(seq_array, SEQUENCE_LENGTH, FEATURE_DIMENSION):
                    file_path = sign_dir / f"sequence_{seq_num:03d}.npy"
                    np.save(file_path, seq_array)
                    seq_recorded_count += 1
                    print(f"  Saved sequence_{seq_num:03d}.npy -> Shape: {seq_array.shape}")
                else:
                    print(f"  [SKIPPED] Sequence {seq_num:03d} failed validation check.")

            if not skip_current_sign:
                print(f"--- {sign.upper()} COMPLETED ---")
            summary_stats[sign] = len(list(sign_dir.glob("sequence_*.npy")))

        print("\n" + "=" * 65)
        print("ALL SIGNS COMPLETED")
        print("=" * 65)
        print("COLLECTION SUMMARY:")
        for sign_name, count in summary_stats.items():
            print(f"  {sign_name:<12} : {count} sequences")
        print("=" * 65)

    except Exception as exc:
        print(f"\nERROR: Unexpected exception during data collection: {exc}")
    finally:
        if 'holistic' in locals() and holistic is not None:
            holistic.close()
        cap.release()
        cv2.destroyAllWindows()
        print("Webcam released and MediaPipe resources closed cleanly.")


if __name__ == "__main__":
    main()
