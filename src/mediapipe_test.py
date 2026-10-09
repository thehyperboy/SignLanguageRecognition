"""
Sign Language Recognition for Accessibility
Step 2 - Part B: MediaPipe Holistic Landmark Detection Test

This script captures webcam frames in real time, processes them through MediaPipe Holistic,
draws Pose, Left-Hand, and Right-Hand landmarks, displays FPS and landmark detection status,
and handles all exceptions cleanly.
"""

import sys
import time
import cv2
import mediapipe as mp


def initialize_holistic():
    """
    Initialize MediaPipe Holistic detector according to the installed package version.
    Supports both legacy Solutions API and modern Tasks API.
    """
    version_str = getattr(mp, "__version__", "unknown")
    print(f"Detected MediaPipe version: {version_str}")

    # Check for legacy Solutions API: mp.solutions.holistic
    if hasattr(mp, "solutions") and hasattr(mp.solutions, "holistic"):
        print("Using MediaPipe Solutions API (mp.solutions.holistic).")
        mp_holistic = mp.solutions.holistic
        mp_drawing = mp.solutions.drawing_utils
        mp_drawing_styles = mp.solutions.drawing_styles

        try:
            holistic = mp_holistic.Holistic(
                static_image_mode=False,
                model_complexity=1,
                smooth_landmarks=True,
                enable_segmentation=False,
                smooth_segmentation=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5,
            )
            return "solutions", holistic, mp_drawing, mp_drawing_styles, mp_holistic
        except Exception as exc:
            print(f"ERROR: Failed to initialize MediaPipe Solutions Holistic: {exc}")
            raise

    # Fallback / Tasks API check
    elif hasattr(mp, "tasks") and hasattr(mp.tasks, "vision"):
        print("Using MediaPipe Tasks API (mp.tasks.vision).")
        try:
            from mediapipe.tasks import python
            from mediapipe.tasks.python import vision

            # Return tasks indicator
            return "tasks", vision, None, None, None
        except Exception as exc:
            print(f"ERROR: Failed to initialize MediaPipe Tasks API: {exc}")
            raise
    else:
        raise RuntimeError(f"Unsupported MediaPipe API layout in version {version_str}")


def run_mediapipe_test() -> None:
    """Run real-time webcam MediaPipe landmark detection."""
    print("=" * 60)
    print("SIGN LANGUAGE RECOGNITION - MEDIAPIPE HOLISTIC TEST")
    print("=" * 60)

    try:
        api_type, holistic_engine, mp_drawing, mp_drawing_styles, mp_holistic = initialize_holistic()
    except Exception as exc:
        print(f"CRITICAL: MediaPipe initialization failed: {exc}")
        print("Exiting application cleanly.")
        print("=" * 60)
        sys.exit(1)

    print("Opening webcam feed (device index 0)...")
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("ERROR: Could not open the webcam.")
        print("Please check camera connections and permissions.")
        print("=" * 60)
        sys.exit(1)

    # Set frame dimensions to 1280x720 (if supported by webcam)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    window_name = "Sign Language Recognition - MediaPipe"
    cv2.namedWindow(window_name, cv2.WINDOW_AUTOSIZE)

    print("Webcam initialized. Displaying live MediaPipe landmark detection stream.")
    print("Press 'Q' to quit.")

    prev_time = time.perf_counter()
    fps = 0.0

    try:
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                print("ERROR: Could not read frame from webcam.")
                break

            curr_time = time.perf_counter()
            time_diff = curr_time - prev_time
            if time_diff > 0:
                fps = 1.0 / time_diff
            prev_time = curr_time

            # Flags & detection status
            pose_status = "not detected"
            left_hand_status = "not detected"
            right_hand_status = "not detected"

            if api_type == "solutions":
                # Convert frame from BGR to RGB before processing
                image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_rgb.flags.writeable = False

                # Process frame with MediaPipe Holistic
                results = holistic_engine.process(image_rgb)

                image_rgb.flags.writeable = True

                # Check and draw Pose landmarks
                if results.pose_landmarks:
                    pose_status = "detected"
                    mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        mp_holistic.POSE_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
                    )

                # Check and draw Left Hand landmarks
                if results.left_hand_landmarks:
                    left_hand_status = "detected"
                    mp_drawing.draw_landmarks(
                        frame,
                        results.left_hand_landmarks,
                        mp_holistic.HAND_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style(),
                        connection_drawing_spec=mp_drawing_styles.get_default_hand_connections_style(),
                    )

                # Check and draw Right Hand landmarks
                if results.right_hand_landmarks:
                    right_hand_status = "detected"
                    mp_drawing.draw_landmarks(
                        frame,
                        results.right_hand_landmarks,
                        mp_holistic.HAND_CONNECTIONS,
                        landmark_drawing_spec=mp_drawing_styles.get_default_hand_landmarks_style(),
                        connection_drawing_spec=mp_drawing_styles.get_default_hand_connections_style(),
                    )

            # Overlay information on frame
            cv2.putText(
                frame,
                "MediaPipe Holistic Detection",
                (20, 35),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame,
                "Press Q to quit",
                (20, 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame,
                f"FPS: {int(fps)}",
                (20, 95),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
                cv2.LINE_AA,
            )

            # Overlay Landmark detection status
            cv2.putText(
                frame,
                f"Pose: {pose_status}",
                (20, 130),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0) if pose_status == "detected" else (0, 0, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame,
                f"Left Hand: {left_hand_status}",
                (20, 155),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0) if left_hand_status == "detected" else (0, 0, 255),
                2,
                cv2.LINE_AA,
            )
            cv2.putText(
                frame,
                f"Right Hand: {right_hand_status}",
                (20, 180),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0) if right_hand_status == "detected" else (0, 0, 255),
                2,
                cv2.LINE_AA,
            )

            cv2.imshow(window_name, frame)

            # Exit cleanly if 'q' or 'Q' is pressed
            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), ord("Q")):
                print("User pressed 'Q'. Exiting MediaPipe test...")
                break

    except Exception as exc:
        print(f"ERROR: An unexpected exception occurred during execution: {exc}")
    finally:
        if api_type == "solutions" and holistic_engine is not None:
            holistic_engine.close()
        cap.release()
        cv2.destroyAllWindows()
        print("MediaPipe detector closed, webcam released, and OpenCV windows destroyed cleanly.")
        print("=" * 60)


if __name__ == "__main__":
    run_mediapipe_test()
