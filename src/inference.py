"""
Sign Language Recognition - Machine Learning Inference Engine
=============================================================
Module: src/inference.py

Contains the reusable SignLanguageRecognizer class for loading the 
LSTM model, StandardScaler, label map, and MediaPipe Tasks HolisticLandmarker,
processing real-time BGR video frames, maintaining a 30-frame buffer,
extracting 258 landmark features, and predicting sign language gestures
with confidence and temporal stability filtering.
"""

from pathlib import Path
from collections import deque, Counter
import json
import joblib
import cv2
import numpy as np
import tensorflow as tf
import mediapipe as mp
import time
import threading


FRAME_WIDTH = 640
FRAME_HEIGHT = 480

HAND_CONNECTIONS = [
    # Thumb
    (0, 1), (1, 2), (2, 3), (3, 4),
    # Index finger
    (0, 5), (5, 6), (6, 7), (7, 8),
    # Middle finger
    (9, 10), (10, 11), (11, 12),
    # Ring finger
    (13, 14), (14, 15), (15, 16),
    # Pinky finger
    (17, 18), (18, 19), (19, 20),
    # Palm connections
    (5, 9), (9, 13), (13, 17), (0, 17), (0, 5)
]


def draw_landmarks(
    frame: np.ndarray,
    result,
    mirror: bool = False,
    prediction: str = "",
    confidence: float = 0.0,
    buffer_count: int = 0,
    sequence_length: int = 30,
    hand_detected: bool = False,
    display_prediction: str = "",
    display_confidence: float = 0.0,
    is_latched: bool = False
) -> np.ndarray:
    """
    Draws 21 MediaPipe hand landmark points, skeleton connections, upper-body pose,
    hand bounding boxes, glowing fingertip halos, and on-frame real-time HUD with persistent gesture results.
    Supports mirror mode to maintain 1:1 pixel alignment on flipped user displays.
    """
    h, w = frame.shape[:2]

    # In mirror mode, we flip the background frame for natural interaction
    if mirror:
        annotated = cv2.flip(frame, 1)
        def to_pix(lm):
            return int((1.0 - getattr(lm, 'x', 0.0)) * w), int(getattr(lm, 'y', 0.0) * h)
    else:
        annotated = frame.copy()
        def to_pix(lm):
            return int(getattr(lm, 'x', 0.0) * w), int(getattr(lm, 'y', 0.0) * h)

    # 1. Subtle camera framing guide corners
    margin_x, margin_y = int(w * 0.08), int(h * 0.06)
    box_color = (0, 230, 110) if hand_detected else (70, 75, 85)
    corner_len = 22
    cv2.line(annotated, (margin_x, margin_y), (margin_x + corner_len, margin_y), box_color, 2, cv2.LINE_AA)
    cv2.line(annotated, (margin_x, margin_y), (margin_x, margin_y + corner_len), box_color, 2, cv2.LINE_AA)
    cv2.line(annotated, (w - margin_x, margin_y), (w - margin_x - corner_len, margin_y), box_color, 2, cv2.LINE_AA)
    cv2.line(annotated, (w - margin_x, margin_y), (w - margin_x, margin_y + corner_len), box_color, 2, cv2.LINE_AA)
    cv2.line(annotated, (margin_x, h - margin_y), (margin_x + corner_len, h - margin_y), box_color, 2, cv2.LINE_AA)
    cv2.line(annotated, (margin_x, h - margin_y), (margin_x, h - margin_y - corner_len), box_color, 2, cv2.LINE_AA)
    cv2.line(annotated, (w - margin_x, h - margin_y), (w - margin_x - corner_len, h - margin_y), box_color, 2, cv2.LINE_AA)
    cv2.line(annotated, (w - margin_x, h - margin_y), (w - margin_x, h - margin_y - corner_len), box_color, 2, cv2.LINE_AA)

    # 2. Pose upper-body landmarks & skeleton (shoulders, elbows, wrists)
    POSE_UPPER_CONNECTIONS = [(11, 12), (11, 13), (13, 15), (12, 14), (14, 16)]
    if hasattr(result, "pose_landmarks") and result.pose_landmarks:
        p_landmarks = result.pose_landmarks
        if isinstance(p_landmarks, list) and len(p_landmarks) > 0 and isinstance(p_landmarks[0], list):
            p_landmarks = p_landmarks[0]
        if isinstance(p_landmarks, list) and len(p_landmarks) > 0:
            p_coords = {
                i: to_pix(p_landmarks[i])
                for i in range(min(len(p_landmarks), 17))
            }
            for start_idx, end_idx in POSE_UPPER_CONNECTIONS:
                if start_idx in p_coords and end_idx in p_coords:
                    cv2.line(annotated, p_coords[start_idx], p_coords[end_idx], (230, 130, 210), 2, cv2.LINE_AA)
            for idx in [11, 12, 13, 14, 15, 16]:
                if idx in p_coords:
                    cv2.circle(annotated, p_coords[idx], 5, (245, 170, 230), -1, cv2.LINE_AA)
                    cv2.circle(annotated, p_coords[idx], 7, (20, 20, 20), 1, cv2.LINE_AA)

    # 3. Left Hand: Bounding box, skeleton connections, & glowing fingertips (Cyan / Amber)
    if hasattr(result, "left_hand_landmarks") and result.left_hand_landmarks:
        landmarks = result.left_hand_landmarks
        if isinstance(landmarks, list) and len(landmarks) > 0 and isinstance(landmarks[0], list):
            landmarks = landmarks[0]
        coords = [to_pix(lm) for lm in landmarks]

        if coords:
            # Dynamic hand bounding box
            xs = [c[0] for c in coords]
            ys = [c[1] for c in coords]
            bx1, bx2 = max(0, min(xs) - 16), min(w, max(xs) + 16)
            by1, by2 = max(0, min(ys) - 16), min(h, max(ys) + 16)
            c_len = min(18, max(8, (bx2 - bx1) // 4))
            col_lh = (255, 185, 0)
            cv2.line(annotated, (bx1, by1), (bx1 + c_len, by1), col_lh, 2, cv2.LINE_AA)
            cv2.line(annotated, (bx1, by1), (bx1, by1 + c_len), col_lh, 2, cv2.LINE_AA)
            cv2.line(annotated, (bx2, by1), (bx2 - c_len, by1), col_lh, 2, cv2.LINE_AA)
            cv2.line(annotated, (bx2, by1), (bx2, by1 + c_len), col_lh, 2, cv2.LINE_AA)
            cv2.line(annotated, (bx1, by2), (bx1 + c_len, by2), col_lh, 2, cv2.LINE_AA)
            cv2.line(annotated, (bx1, by2), (bx1, by2 - c_len), col_lh, 2, cv2.LINE_AA)
            cv2.line(annotated, (bx2, by2), (bx2 - c_len, by2), col_lh, 2, cv2.LINE_AA)
            cv2.line(annotated, (bx2, by2), (bx2, by2 - c_len), col_lh, 2, cv2.LINE_AA)
            cv2.putText(annotated, "LEFT HAND", (bx1, max(16, by1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.36, col_lh, 1, cv2.LINE_AA)

        for start_idx, end_idx in HAND_CONNECTIONS:
            if start_idx < len(coords) and end_idx < len(coords):
                cv2.line(annotated, coords[start_idx], coords[end_idx], (255, 175, 0), 2, cv2.LINE_AA)

        for i, pt in enumerate(coords):
            if i in (4, 8, 12, 16, 20):
                # Glowing fingertip halo
                cv2.circle(annotated, pt, 8, (255, 220, 100), 1, cv2.LINE_AA)
                cv2.circle(annotated, pt, 5, (0, 255, 255), -1, cv2.LINE_AA)
            else:
                cv2.circle(annotated, pt, 4, (0, 210, 255), -1, cv2.LINE_AA)
                cv2.circle(annotated, pt, 5, (20, 20, 20), 1, cv2.LINE_AA)

    # 4. Right Hand: Bounding box, skeleton connections, & glowing fingertips (Emerald / Lime)
    if hasattr(result, "right_hand_landmarks") and result.right_hand_landmarks:
        landmarks = result.right_hand_landmarks
        if isinstance(landmarks, list) and len(landmarks) > 0 and isinstance(landmarks[0], list):
            landmarks = landmarks[0]
        coords = [to_pix(lm) for lm in landmarks]

        if coords:
            # Dynamic hand bounding box
            xs = [c[0] for c in coords]
            ys = [c[1] for c in coords]
            bx1, bx2 = max(0, min(xs) - 16), min(w, max(xs) + 16)
            by1, by2 = max(0, min(ys) - 16), min(h, max(ys) + 16)
            c_len = min(18, max(8, (bx2 - bx1) // 4))
            col_rh = (0, 230, 110)
            cv2.line(annotated, (bx1, by1), (bx1 + c_len, by1), col_rh, 2, cv2.LINE_AA)
            cv2.line(annotated, (bx1, by1), (bx1, by1 + c_len), col_rh, 2, cv2.LINE_AA)
            cv2.line(annotated, (bx2, by1), (bx2 - c_len, by1), col_rh, 2, cv2.LINE_AA)
            cv2.line(annotated, (bx2, by1), (bx2, by1 + c_len), col_rh, 2, cv2.LINE_AA)
            cv2.line(annotated, (bx1, by2), (bx1 + c_len, by2), col_rh, 2, cv2.LINE_AA)
            cv2.line(annotated, (bx1, by2), (bx1, by2 - c_len), col_rh, 2, cv2.LINE_AA)
            cv2.line(annotated, (bx2, by2), (bx2 - c_len, by2), col_rh, 2, cv2.LINE_AA)
            cv2.line(annotated, (bx2, by2), (bx2, by2 - c_len), col_rh, 2, cv2.LINE_AA)
            cv2.putText(annotated, "RIGHT HAND", (bx1, max(16, by1 - 5)), cv2.FONT_HERSHEY_SIMPLEX, 0.36, col_rh, 1, cv2.LINE_AA)

        for start_idx, end_idx in HAND_CONNECTIONS:
            if start_idx < len(coords) and end_idx < len(coords):
                cv2.line(annotated, coords[start_idx], coords[end_idx], (0, 215, 100), 2, cv2.LINE_AA)

        for i, pt in enumerate(coords):
            if i in (4, 8, 12, 16, 20):
                # Glowing fingertip halo
                cv2.circle(annotated, pt, 8, (120, 255, 180), 1, cv2.LINE_AA)
                cv2.circle(annotated, pt, 5, (0, 255, 120), -1, cv2.LINE_AA)
            else:
                cv2.circle(annotated, pt, 4, (0, 240, 0), -1, cv2.LINE_AA)
                cv2.circle(annotated, pt, 5, (20, 20, 20), 1, cv2.LINE_AA)

    # 5. Top-Left Live Status Pill
    hud_bg = (12, 14, 18)
    overlay = annotated.copy()
    cv2.rectangle(overlay, (14, 14), (230, 46), hud_bg, -1)
    cv2.addWeighted(overlay, 0.82, annotated, 0.18, 0, annotated)
    cv2.rectangle(annotated, (14, 14), (230, 46), (45, 52, 62), 1, cv2.LINE_AA)

    if hand_detected:
        cv2.circle(annotated, (28, 30), 5, (0, 230, 110), -1, cv2.LINE_AA)
        cv2.putText(annotated, "LIVE TRACKING ACTIVE", (42, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1, cv2.LINE_AA)
    else:
        cv2.circle(annotated, (28, 30), 4, (120, 130, 145), -1, cv2.LINE_AA)
        cv2.putText(annotated, "SHOW HAND TO TRACK", (42, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (180, 190, 205), 1, cv2.LINE_AA)

    # 6. Top-Right / Center Recognized Gesture Card (Persistent & Vibrant)
    active_label = display_prediction if display_prediction else prediction
    active_conf = display_confidence if display_confidence > 0 else confidence

    if active_label and active_label not in ("Waiting...", "Uncertain") and active_conf >= 0.60:
        tag_str = "[RECOGNIZED]" if is_latched else "[LIVE]"
        banner_text = f"{tag_str} {active_label.upper()} {active_conf * 100:.0f}%"
        (text_w, text_h), _ = cv2.getTextSize(banner_text, cv2.FONT_HERSHEY_SIMPLEX, 0.54, 2)
        box_w = text_w + 32
        b_x = max(240, w - box_w - 14)

        card_overlay = annotated.copy()
        cv2.rectangle(card_overlay, (b_x, 14), (w - 14, 46), (5, 45, 20), -1)
        cv2.addWeighted(card_overlay, 0.88, annotated, 0.12, 0, annotated)
        cv2.rectangle(annotated, (b_x, 14), (w - 14, 46), (0, 230, 110), 1, cv2.LINE_AA)

        # Checkmark icon dot
        cv2.circle(annotated, (b_x + 16, 30), 7, (0, 230, 110), -1, cv2.LINE_AA)
        cv2.putText(annotated, "v", (b_x + 13, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(annotated, banner_text, (b_x + 30, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.50, (255, 255, 255), 2, cv2.LINE_AA)

    elif buffer_count > 1 and hand_detected:
        buf_text = f"MOTION: {buffer_count}/{sequence_length}"
        (text_w, text_h), _ = cv2.getTextSize(buf_text, cv2.FONT_HERSHEY_SIMPLEX, 0.44, 1)
        b_x = w - text_w - 34
        b_overlay = annotated.copy()
        cv2.rectangle(b_overlay, (b_x, 14), (w - 14, 46), (15, 20, 28), -1)
        cv2.addWeighted(b_overlay, 0.85, annotated, 0.15, 0, annotated)
        cv2.rectangle(annotated, (b_x, 14), (w - 14, 46), (40, 50, 65), 1, cv2.LINE_AA)
        cv2.circle(annotated, (b_x + 14, 30), 4, (255, 126, 95), -1, cv2.LINE_AA)
        cv2.putText(annotated, buf_text, (b_x + 24, 34), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (220, 230, 240), 1, cv2.LINE_AA)

    # 7. Bottom Glowing Progress Bar
    if sequence_length > 0:
        bar_h = 6
        fill_w = int(w * min(buffer_count / float(sequence_length), 1.0))
        cv2.rectangle(annotated, (0, h - bar_h), (w, h), (18, 22, 28), -1)
        if fill_w > 0:
            bar_col = (0, 230, 110) if buffer_count >= sequence_length else (255, 126, 95)
            cv2.rectangle(annotated, (0, h - bar_h), (fill_w, h), bar_col, -1)

    return annotated


class SignLanguageRecognizer:
    """
    Reusable inference engine for real-time sign language recognition.
    """

    def __init__(
        self,
        model_path=None,
        scaler_path=None,
        label_map_path=None,
        mediapipe_model_path=None,
        sequence_length=30,
        expected_features=258,
        confidence_threshold=0.65,
        stability_window=5,
        stability_count=2,
        grace_frames=2
    ):
        # Determine project root relative to src/inference.py
        self.root_dir = Path(__file__).resolve().parents[1]

        self.model_path = Path(model_path) if model_path else self.root_dir / "models" / "sign_language_lstm_best.keras"
        self.scaler_path = Path(scaler_path) if scaler_path else self.root_dir / "data" / "processed" / "scaler.pkl"
        self.label_map_path = Path(label_map_path) if label_map_path else self.root_dir / "data" / "processed" / "label_map.json"
        self.mediapipe_model_path = Path(mediapipe_model_path) if mediapipe_model_path else self.root_dir / "models" / "holistic_landmarker.task"

        self.sequence_length = sequence_length
        self.expected_features = expected_features
        self.confidence_threshold = confidence_threshold
        self.stability_window = stability_window
        self.stability_count = stability_count
        self.grace_frames = grace_frames

        self.model = None
        self.scaler = None
        self.label_map = {}
        self.landmarker = None

        self.sequence = deque(maxlen=self.sequence_length)
        self.prediction_history = deque(maxlen=self.stability_window)
        self.frame_timestamp = 0
        self.no_hand_counter = 0
        self.last_features = None
        self.latched_gesture = ""
        self.latched_confidence = 0.0
        self.latched_time = 0.0
        self.process_lock = threading.Lock()

        # Initialize resources
        self.load_models()

    def load_models(self):
        """
        Loads the trained LSTM model, StandardScaler, label map JSON,
        and initializes the MediaPipe Tasks HolisticLandmarker with optimized confidence thresholds.
        """
        # Validate path existence
        for path_name, path_obj in [
            ("Model", self.model_path),
            ("Scaler", self.scaler_path),
            ("Label Map", self.label_map_path),
            ("MediaPipe Task", self.mediapipe_model_path)
        ]:
            if not path_obj.exists():
                raise FileNotFoundError(f"{path_name} file not found at: {path_obj}")

        # 1. Load LSTM Model
        self.model = tf.keras.models.load_model(self.model_path)

        # Model validation
        if self.model.input_shape != (None, self.sequence_length, self.expected_features):
            raise ValueError(
                f"Model input shape mismatch! Expected (None, {self.sequence_length}, {self.expected_features}), "
                f"but found {self.model.input_shape}."
            )

        if self.expected_features != 258:
            raise ValueError(f"Feature dimension must be 258, found {self.expected_features}.")

        # 2. Load Scaler
        self.scaler = joblib.load(self.scaler_path)

        # 3. Load Label Map
        with open(self.label_map_path, "r", encoding="utf-8") as f:
            raw_map = json.load(f)

        if not isinstance(raw_map, dict):
            raise ValueError("label_map.json must contain a JSON dictionary.")

        self.label_map = {}
        for key, value in raw_map.items():
            if isinstance(value, int):
                self.label_map[int(value)] = str(key)
            else:
                try:
                    self.label_map[int(key)] = str(value)
                except ValueError:
                    raise ValueError(f"Unsupported label map entry: {key}: {value}")

        if not self.label_map:
            raise ValueError("Label map is empty.")

        # 4. Initialize MediaPipe Tasks HolisticLandmarker with increased sensitivity
        BaseOptions = mp.tasks.BaseOptions
        HolisticLandmarker = mp.tasks.vision.HolisticLandmarker
        HolisticLandmarkerOptions = mp.tasks.vision.HolisticLandmarkerOptions
        RunningMode = mp.tasks.vision.RunningMode

        options = HolisticLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(self.mediapipe_model_path)),
            running_mode=RunningMode.VIDEO,
            min_face_detection_confidence=0.4,
            min_face_landmarks_confidence=0.4,
            min_pose_detection_confidence=0.45,
            min_pose_landmarks_confidence=0.45,
            min_hand_landmarks_confidence=0.35,  # Robust hand tracking under motion
            output_face_blendshapes=False,
            output_segmentation_mask=False
        )

        self.landmarker = HolisticLandmarker.create_from_options(options)

    def extract_landmarks(self, result) -> np.ndarray:
        """
        Extracts exactly 258 features from MediaPipe detection result:
        - Pose: 33 landmarks × 4 values (x, y, z, visibility) = 132
        - Left Hand: 21 landmarks × 3 values (x, y, z) = 63
        - Right Hand: 21 landmarks × 3 values (x, y, z) = 63
        Total = 258 features.
        """
        # Pose (33 x 4)
        pose = np.zeros((33, 4), dtype=np.float32)
        if hasattr(result, "pose_landmarks") and result.pose_landmarks:
            landmarks = result.pose_landmarks
            if isinstance(landmarks, list) and len(landmarks) > 0 and isinstance(landmarks[0], list):
                landmarks = landmarks[0]
            count = min(len(landmarks), 33)
            for i in range(count):
                lm = landmarks[i]
                pose[i] = [
                    getattr(lm, "x", 0.0),
                    getattr(lm, "y", 0.0),
                    getattr(lm, "z", 0.0),
                    getattr(lm, "visibility", 0.0) if getattr(lm, "visibility", None) is not None else 0.0
                ]

        # Left Hand (21 x 3)
        left_hand = np.zeros((21, 3), dtype=np.float32)
        if hasattr(result, "left_hand_landmarks") and result.left_hand_landmarks:
            landmarks = result.left_hand_landmarks
            if isinstance(landmarks, list) and len(landmarks) > 0 and isinstance(landmarks[0], list):
                landmarks = landmarks[0]
            count = min(len(landmarks), 21)
            for i in range(count):
                lm = landmarks[i]
                left_hand[i] = [getattr(lm, "x", 0.0), getattr(lm, "y", 0.0), getattr(lm, "z", 0.0)]

        # Right Hand (21 x 3)
        right_hand = np.zeros((21, 3), dtype=np.float32)
        if hasattr(result, "right_hand_landmarks") and result.right_hand_landmarks:
            landmarks = result.right_hand_landmarks
            if isinstance(landmarks, list) and len(landmarks) > 0 and isinstance(landmarks[0], list):
                landmarks = landmarks[0]
            count = min(len(landmarks), 21)
            for i in range(count):
                lm = landmarks[i]
                right_hand[i] = [getattr(lm, "x", 0.0), getattr(lm, "y", 0.0), getattr(lm, "z", 0.0)]

        # Concatenate in strict order: pose, left hand, right hand
        features = np.concatenate([
            pose.flatten(),
            left_hand.flatten(),
            right_hand.flatten()
        ])

        return features.astype(np.float32)

    def predict_sequence(self) -> tuple[str, float]:
        """
        Scales the 30-frame sequence buffer, runs LSTM model inference,
        and applies confidence threshold & stability filtering.
        Supports automatic dominant hand mapping so left-handed signing is recognized as accurately as right-handed.

        Returns:
            (predicted_label, confidence)
        """
        sequence_array = np.array(self.sequence, dtype=np.float32)
        scaled_sequence = self.scaler.transform(sequence_array)
        model_input = np.expand_dims(scaled_sequence, axis=0)

        probabilities = self.model.predict(model_input, verbose=0)[0]
        predicted_index = int(np.argmax(probabilities))
        confidence = float(probabilities[predicted_index])
        predicted_label = self.label_map.get(predicted_index, f"class_{predicted_index}")

        # Fallback check: if confidence is moderate (< 0.75) and only Left Hand is active, test mapped sequence
        lh_norm = float(np.mean(np.linalg.norm(sequence_array[:, 132:195], axis=1)))
        rh_norm = float(np.mean(np.linalg.norm(sequence_array[:, 195:258], axis=1)))

        if confidence < 0.75 and lh_norm > 0.5 and rh_norm < 0.3:
            mapped_seq = sequence_array.copy()
            mapped_seq[:, 195:258] = sequence_array[:, 132:195]
            mapped_seq[:, 132:195] = 0.0
            scaled_mapped = self.scaler.transform(mapped_seq)
            m_probs = self.model.predict(np.expand_dims(scaled_mapped, axis=0), verbose=0)[0]
            m_idx = int(np.argmax(m_probs))
            m_conf = float(m_probs[m_idx])
            if m_conf > confidence:
                predicted_label = self.label_map.get(m_idx, f"class_{m_idx}")
                confidence = m_conf

        # Temporal stability filtering
        if confidence >= self.confidence_threshold:
            self.prediction_history.append(predicted_label)
        else:
            self.prediction_history.append("Uncertain")

        counts = Counter(self.prediction_history)
        stable_label, stable_count = counts.most_common(1)[0]

        # Return prediction immediately on high confidence, or require stability_count voting
        if stable_label != "Uncertain" and (
            stable_count >= self.stability_count or
            (len(self.prediction_history) < self.stability_count and confidence >= 0.75)
        ):
            final_prediction = stable_label
        else:
            final_prediction = "Uncertain"

        return final_prediction, confidence

    def predict_partial_sequence(self) -> tuple[str, float]:
        """
        Runs early prediction on partial sequences (12-29 frames) via temporal linear resampling.
        Enables instantaneous live gesture feedback without waiting 30 full frames.
        """
        buf = list(self.sequence)
        n = len(buf)
        if n < 12:
            return "Waiting...", 0.0

        indices = np.linspace(0, n - 1, self.sequence_length).astype(int)
        seq_array = np.array([buf[i] for i in indices], dtype=np.float32)
        scaled_seq = self.scaler.transform(seq_array)
        probs = self.model.predict(np.expand_dims(scaled_seq, axis=0), verbose=0)[0]
        idx = int(np.argmax(probs))
        conf = float(probs[idx])
        label = self.label_map.get(idx, f"class_{idx}")

        # Check LH dominance mapping if LH active and RH empty
        lh_norm = float(np.mean(np.linalg.norm(seq_array[:, 132:195], axis=1)))
        rh_norm = float(np.mean(np.linalg.norm(seq_array[:, 195:258], axis=1)))
        if conf < 0.75 and lh_norm > 0.5 and rh_norm < 0.3:
            mapped = seq_array.copy()
            mapped[:, 195:258] = seq_array[:, 132:195]
            mapped[:, 132:195] = 0.0
            m_probs = self.model.predict(np.expand_dims(self.scaler.transform(mapped), axis=0), verbose=0)[0]
            m_idx = int(np.argmax(m_probs))
            m_conf = float(m_probs[m_idx])
            if m_conf > conf:
                label = self.label_map.get(m_idx, f"class_{m_idx}")
                conf = m_conf

        return label, conf

    def process_frame(self, frame: np.ndarray, mirror_display: bool = True) -> dict:
        """
        Processes an OpenCV BGR frame:
        1. Ensures 640x480 resolution
        2. MediaPipe detection on raw unmirrored coordinates to match trained model
        3. Feature extraction (258 features)
        4. Hand detection with grace period for temporary motion blur
        5. Live temporal buffering & early/sliding-window prediction
        6. Result persistence (latched for 1.5s so results stay visible)
        7. Landmark, hand bounding box, & on-frame HUD overlay
        """
        if self.landmarker is None:
            raise RuntimeError("MediaPipe Landmarker is not initialized.")

        with self.process_lock:
            # Safety dimension normalization to 640x480
            h, w = frame.shape[:2]
            if w != FRAME_WIDTH or h != FRAME_HEIGHT:
                frame = cv2.resize(frame, (FRAME_WIDTH, FRAME_HEIGHT))

            # 1. BGR -> RGB on raw unmirrored frame
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # 2. MediaPipe Image
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

            # 3. Monotonically Increasing Timestamp Fix
            current_time_ms = int(time.perf_counter() * 1000)
            if current_time_ms <= self.frame_timestamp:
                self.frame_timestamp += 33
            else:
                self.frame_timestamp = current_time_ms

            # 4. Landmarker detection on raw frame
            result = self.landmarker.detect_for_video(mp_image, self.frame_timestamp)

            # 5. Extract features
            features = self.extract_landmarks(result)

            # Check landmark detection presence
            pose_det = bool(hasattr(result, "pose_landmarks") and result.pose_landmarks and len(result.pose_landmarks) > 0)
            lh_det = bool(hasattr(result, "left_hand_landmarks") and result.left_hand_landmarks and len(result.left_hand_landmarks) > 0)
            rh_det = bool(hasattr(result, "right_hand_landmarks") and result.right_hand_landmarks and len(result.right_hand_landmarks) > 0)
            hand_det = lh_det or rh_det

            if hand_det:
                self.no_hand_counter = 0
                self.last_features = features.copy()
                self.sequence.append(features)
                effective_hand_det = True
            else:
                self.no_hand_counter += 1
                # Grace period: if hand was detected recently, survive brief dropped frames from motion blur
                if self.no_hand_counter <= self.grace_frames and len(self.sequence) > 0 and self.last_features is not None:
                    self.sequence.append(self.last_features)
                    effective_hand_det = True
                else:
                    effective_hand_det = False
                    if self.no_hand_counter >= 12:
                        self.sequence.clear()
                        self.prediction_history.clear()
                        self.last_features = None

            # 6. Live prediction with early preview & continuous sliding window
            prediction = "Waiting..."
            confidence = 0.0
            ready = False

            if effective_hand_det:
                buf_len = len(self.sequence)
                if buf_len >= self.sequence_length:
                    prediction, confidence = self.predict_sequence()
                    ready = True
                elif buf_len >= 12:
                    # Live dynamic early preview for instant responsiveness
                    p_label, p_conf = self.predict_partial_sequence()
                    if p_conf >= 0.55:
                        prediction, confidence = p_label, p_conf
                        ready = True

            # 7. Result Latching with buffer flush
            curr_now = time.perf_counter()
            if ready and prediction in self.label_map.values() and confidence >= self.confidence_threshold:
                self.latched_gesture = prediction
                self.latched_confidence = confidence
                self.latched_time = curr_now
                # Flush the sequence buffer so that the previous sign does not contaminate the next sign
                if len(self.sequence) >= self.sequence_length:
                    self.sequence = deque(list(self.sequence)[-4:], maxlen=self.sequence_length)
                    self.prediction_history.clear()

            # Determine display prediction (live if ready, otherwise latched within 1.5 seconds)
            is_latched = False
            display_pred = prediction
            display_conf = confidence

            if (not ready or prediction in ("Waiting...", "Uncertain")) and self.latched_gesture:
                time_since_latch = curr_now - self.latched_time
                if time_since_latch < 1.5:
                    display_pred = self.latched_gesture
                    display_conf = self.latched_confidence
                    is_latched = True

            # 8. Draw MediaPipe hand & pose landmarks live on frame (mirrored for user view)
            annotated_frame = draw_landmarks(
                frame,
                result,
                mirror=mirror_display,
                prediction=prediction,
                confidence=confidence,
                buffer_count=len(self.sequence),
                sequence_length=self.sequence_length,
                hand_detected=effective_hand_det,
                display_prediction=display_pred,
                display_confidence=display_conf,
                is_latched=is_latched
            )

            return {
                "prediction": prediction,
                "confidence": confidence,
                "display_prediction": display_pred,
                "display_confidence": display_conf,
                "is_latched": is_latched,
                "ready": ready or is_latched,
                "frames": len(self.sequence),
                "hand_detected": effective_hand_det,
                "left_hand_detected": lh_det,
                "right_hand_detected": rh_det,
                "pose_detected": pose_det,
                "annotated_frame": annotated_frame
            }

    def reset(self):
        """Resets the sequence buffer, prediction history, latched results, and counters."""
        self.sequence.clear()
        self.prediction_history.clear()
        self.no_hand_counter = 0
        self.last_features = None
        self.latched_gesture = ""
        self.latched_confidence = 0.0
        self.latched_time = 0.0

    def close(self):
        """Releases MediaPipe landmarker resources."""
        if self.landmarker is not None:
            try:
                self.landmarker.close()
            except Exception:
                pass
            self.landmarker = None
