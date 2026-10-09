import cv2
import sys

def test_camera():
    print("=" * 50)
    print("SIGN LANGUAGE RECOGNITION - CAMERA TEST")
    print("=" * 50)
    print("Initializing camera feed... (Press 'q' in the window to exit)\n")

    # Attempt to open default webcam (device index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Could not open the webcam.")
        print("Please verify that:")
        print(" 1. A working camera is attached or built into your system.")
        print(" 2. Camera access permissions are granted in Windows Settings.")
        print(" 3. No other application (Zoom, Teams, Browser, etc.) is currently using the camera.")
        print("=" * 50)
        sys.exit(1)

    window_name = "Sign Language Recognition - Camera Test"
    print(f"Webcam opened successfully. Displaying stream window: '{window_name}'")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("ERROR: Failed to grab frame from webcam.")
                break

            # Overlay quit instructions on frame
            cv2.putText(
                frame,
                "Press 'q' to quit camera test",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2,
                cv2.LINE_AA
            )

            cv2.imshow(window_name, frame)

            # Exit cleanly if 'q' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quit key 'q' pressed by user. Exiting camera test...")
                break

    except Exception as e:
        print(f"An unexpected error occurred during camera stream: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()
        print("Camera released and window destroyed cleanly.")
        print("=" * 50)

if __name__ == "__main__":
    test_camera()
