"""
Sign Language Recognition for Accessibility
Step 2 - Part A: Webcam Access Verification Test

This script verifies OpenCV webcam access without MediaPipe dependencies.
"""

import sys
import cv2


def run_camera_test() -> None:
    """Open default webcam feed and display live stream until 'Q' is pressed."""
    print("=" * 60)
    print("SIGN LANGUAGE RECOGNITION - CAMERA TEST")
    print("=" * 60)
    print("Attempting to open default webcam (device index 0)...")

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Could not open the webcam.")
        print("Please check that:")
        print("  1. A working webcam is connected or built into your system.")
        print("  2. Camera permissions are enabled in Windows Settings.")
        print("  3. No other application (Zoom, Teams, Browser) is using the camera.")
        print("=" * 60)
        sys.exit(1)

    print("Webcam opened successfully.")
    print("Displaying live camera feed. Press 'Q' to quit.")

    window_name = "Sign Language Recognition - Camera Test"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    try:
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("ERROR: Could not read frame from webcam.")
                break

            # Overlay instruction text on frame
            cv2.putText(
                frame,
                "Sign Language Recognition - Camera Test",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame,
                "Press Q to quit",
                (20, 75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )

            cv2.imshow(window_name, frame)

            # Exit cleanly when 'q' or 'Q' is pressed
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), ord("Q")):
                print("Quit key 'Q' pressed by user. Exiting camera test...")
                break

    except Exception as exc:
        print(f"ERROR: An unexpected runtime exception occurred: {exc}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Webcam released and OpenCV windows closed cleanly.")
        print("=" * 60)


if __name__ == "__main__":
    run_camera_test()
