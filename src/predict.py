"""
Real-Time Sign Language Recognition Application
===============================================
Module: src/predict.py

Desktop OpenCV application utilizing SignLanguageRecognizer from src/inference.py
for real-time camera feed processing and gesture prediction display.
"""

import cv2
import sys
from pathlib import Path

# Add project root to sys.path to enable direct module execution
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.inference import SignLanguageRecognizer


def main():
    print("=" * 50)
    print("REAL-TIME SIGN LANGUAGE PREDICTION")
    print("MediaPipe Tasks API + LSTM Engine")
    print("=" * 50)

    # 1. Instantiate Recognizer Engine
    try:
        recognizer = SignLanguageRecognizer()
        print("LSTM model loaded successfully")
        print("Scaler loaded successfully")
        print("Label map loaded successfully")
        print(f"Feature dimension: {recognizer.expected_features}")
        print(f"Number of classes: {len(recognizer.label_map)}")
        print(f"Model input shape: {recognizer.model.input_shape}")
        print("MediaPipe Holistic Landmarker initialized successfully")
    except Exception as e:
        print(f"\nCRITICAL ERROR initializing SignLanguageRecognizer: {e}")
        return

    # 2. Open Webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("\nERROR: Could not open webcam.")
        recognizer.close()
        return

    print("Webcam opened successfully")
    print("\nControls:")
    print("Q - Quit")
    print("=" * 50)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("ERROR: Could not read webcam frame.")
                break

            # Process raw webcam frame with inference engine
            # mirror_display=True automatically draws landmarks and HUD onto mirrored user display
            result = recognizer.process_frame(frame, mirror_display=True)
            annotated_frame = result.get("annotated_frame", frame)

            cv2.imshow("Sign Language Recognition", annotated_frame)

            # Keyboard Exit handling
            key = cv2.waitKey(1) & 0xFF
            if key == ord("q") or key == ord("Q"):
                break

    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"\nERROR during video stream processing: {e}")
    finally:
        print("\nClosing application...")
        cap.release()
        cv2.destroyAllWindows()
        recognizer.close()
        print("Application closed.")


if __name__ == "__main__":
    main()