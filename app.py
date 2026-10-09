"""
Sign Language Recognition - Apple Minimalist Black & White System
==================================================================
Module: app.py

A high-performance real-time Sign Language Recognition web application
recreated with Apple's iconic minimalist design language:
- Pure Black & White / Grayscale aesthetic (SF Pro typography, #F5F5F7 canvas, #FFFFFF cards)
- Direct real-time camera tracking (instant auto-start, zero button friction)
- Native lightweight rendering: ultra-low bandwidth JPEG streaming, zero backend collapses
- High-contrast Neural Console displaying accurate recognized gestures, confidence, and audio
- 100% AUTHORITATIVE ML PIPELINE PRESERVED:
    * MediaPipe Tasks HolisticLandmarker (258 features)
    * 30-frame temporal motion sequence buffer
    * StandardScaler normalization
    * 2-layer LSTM classification model
    * pyttsx3 asynchronous voice audio synthesis worker
"""

import sys
import time
import textwrap
from pathlib import Path

import cv2
import numpy as np
import streamlit as st

# Ensure project root is in sys.path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.inference import SignLanguageRecognizer, FRAME_WIDTH, FRAME_HEIGHT
from src.speech import speak_text

# ============================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SignFlow • Real-Time Gesture Recognition",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# APPLE MINIMALIST BLACK & WHITE THEME - CSS STYLING
# ============================================================

APPLE_BW_CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">

<style>
    /* ===== APPLE MINIMALIST DESIGN SYSTEM (BLACK & WHITE) ===== */
    :root {
        --apple-bg: #F5F5F7;
        --apple-surface: #FFFFFF;
        --apple-surface-dark: #1D1D1F;
        --apple-text-primary: #1D1D1F;
        --apple-text-secondary: #86868B;
        --apple-text-tertiary: #6E6E73;
        --apple-border: rgba(0, 0, 0, 0.08);
        --apple-border-light: #E5E5EA;
        --apple-black: #000000;
        --apple-white: #FFFFFF;
        --radius-apple-sm: 12px;
        --radius-apple-md: 18px;
        --radius-apple-lg: 24px;
        --radius-apple-pill: 9999px;
        --shadow-apple-subtle: 0 2px 10px rgba(0, 0, 0, 0.03);
        --shadow-apple-card: 0 6px 24px rgba(0, 0, 0, 0.04);
        --shadow-apple-elevated: 0 16px 36px rgba(0, 0, 0, 0.08);
    }

    /* Base Canvas */
    html, body, [data-testid="stAppViewContainer"] {
        background-color: var(--apple-bg) !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", "Helvetica Neue", "Inter", sans-serif !important;
        color: var(--apple-text-primary) !important;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }

    #MainMenu, footer {
        visibility: hidden !important;
        height: 0 !important;
    }
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* Block Container */
    .main .block-container {
        max-width: 1140px !important;
        margin: 0 auto !important;
        padding: 2rem 2.2rem 3.8rem !important;
    }

    @media (max-width: 768px) {
        .main .block-container {
            padding: 1.2rem 1rem 2.5rem !important;
        }
    }

    /* Apple Frosted Navbar */
    .apple-nav-brand {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: -0.025em;
        color: var(--apple-text-primary);
    }

    .apple-nav-badge {
        font-size: 0.68rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        background: #000000;
        color: #FFFFFF;
        padding: 3px 10px;
        border-radius: var(--radius-apple-pill);
    }

    /* Hero */
    .apple-hero {
        text-align: center;
        padding: 1.8rem 1rem 2.2rem;
        max-width: 720px;
        margin: 0 auto;
    }

    .apple-hero-eyebrow {
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--apple-text-secondary);
        margin-bottom: 0.6rem;
    }

    .apple-hero-title {
        font-size: 2.5rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        line-height: 1.08;
        color: var(--apple-text-primary);
        margin-bottom: 0.8rem;
    }

    .apple-hero-desc {
        font-size: 0.98rem;
        line-height: 1.5;
        color: var(--apple-text-secondary);
        max-width: 600px;
        margin: 0 auto;
    }

    /* Apple Section Header */
    .apple-section-header {
        display: flex;
        align-items: baseline;
        justify-content: space-between;
        margin-bottom: 0.9rem;
        padding-bottom: 0.4rem;
        border-bottom: 1px solid var(--apple-border-light);
    }

    .apple-section-title {
        font-size: 1.15rem;
        font-weight: 700;
        letter-spacing: -0.02em;
        color: var(--apple-text-primary);
    }

    .apple-section-meta {
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        color: var(--apple-text-secondary);
    }

    /* Video Frame Container */
    [data-testid="stImage"] {
        border-radius: var(--radius-apple-md) !important;
        overflow: hidden !important;
        border: 1px solid #1D1D1F !important;
        box-shadow: var(--shadow-apple-card) !important;
        background: #000000 !important;
    }

    [data-testid="stImage"] img {
        border-radius: var(--radius-apple-md) !important;
        display: block !important;
        width: 100% !important;
    }

    /* Neural Console Card (Dark Apple B&W) */
    .apple-hud-card {
        background: #1D1D1F;
        border: 1px solid rgba(255, 255, 255, 0.12);
        border-radius: 20px;
        padding: 1.8rem;
        color: #FFFFFF;
        box-shadow: 0 12px 32px rgba(0, 0, 0, 0.12);
        display: flex;
        flex-direction: column;
        gap: 1.15rem;
        box-sizing: border-box;
    }

    .apple-hud-status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.02em;
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.12);
        padding: 5px 14px;
        border-radius: 9999px;
        width: fit-content;
    }

    .apple-hud-indicator {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        display: inline-block;
    }

    .apple-hud-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #86868B;
    }

    .apple-hud-main-val {
        font-size: 2.3rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        line-height: 1.1;
        color: #FFFFFF;
    }

    .apple-hud-main-val.waiting {
        color: #86868B;
    }

    .apple-hud-conf-badge {
        display: inline-flex;
        align-items: center;
        background: rgba(0, 230, 118, 0.15);
        color: #00E676;
        border: 1px solid rgba(0, 230, 118, 0.3);
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 0.82rem;
        font-weight: 600;
        width: fit-content;
    }

    .apple-hud-conf-badge.waiting {
        background: rgba(255, 255, 255, 0.06);
        color: #86868B;
        border-color: rgba(255, 255, 255, 0.1);
    }

    .apple-hud-buffer-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: #86868B;
    }

    .apple-hud-progress-bg {
        width: 100%;
        height: 8px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 9999px;
        overflow: hidden;
    }

    .apple-hud-progress-bar {
        height: 100%;
        background: #00E676;
        border-radius: 9999px;
        transition: width 0.15s ease;
    }

    .apple-hud-audio-status {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        font-size: 0.8rem;
        font-weight: 500;
        color: rgba(255, 255, 255, 0.85);
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 6px 14px;
        border-radius: 9999px;
        width: fit-content;
    }

    /* Apple Cards */
    .apple-card {
        background: var(--apple-surface);
        border: 1px solid var(--apple-border-light);
        border-radius: var(--radius-apple-md);
        padding: 1.8rem;
        box-shadow: var(--shadow-apple-card);
    }

    .apple-gesture-card {
        background: #FFFFFF;
        border: 1px solid var(--apple-border-light);
        border-radius: var(--radius-apple-md);
        padding: 1.4rem;
        box-shadow: var(--shadow-apple-subtle);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
        transition: all 0.2s ease;
    }

    .apple-gesture-card:hover {
        border-color: #000000;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
        transform: translateY(-2px);
    }

    /* Apple Segmented Control */
    div[data-testid="stSegmentedControl"] {
        background: #E5E5EA !important;
        padding: 3px !important;
        border-radius: var(--radius-apple-pill) !important;
        border: none !important;
    }

    div[data-testid="stSegmentedControl"] button {
        border-radius: var(--radius-apple-pill) !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif !important;
        font-size: 0.84rem !important;
        font-weight: 500 !important;
        border: none !important;
        padding: 5px 18px !important;
        color: #6E6E73 !important;
        background: transparent !important;
    }

    div[data-testid="stSegmentedControl"] button[aria-checked="true"] {
        background: #FFFFFF !important;
        color: #000000 !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12) !important;
    }

    /* Buttons */
    div.stButton > button {
        border-radius: var(--radius-apple-pill) !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        background: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #D2D2D7 !important;
        padding: 0.45rem 1.2rem !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button:hover {
        background: #000000 !important;
        color: #FFFFFF !important;
        border-color: #000000 !important;
    }
</style>
"""

st.html(APPLE_BW_CSS)

# ============================================================
# AUTHORITATIVE CONSTANTS & GESTURE DICTIONARIES
# ============================================================

SEQUENCE_LENGTH = 30

DISPLAY_LABEL_MAP = {
    "hello": "HELLO",
    "help": "HELP",
    "love": "LOVE",
    "no": "NO",
    "please": "PLEASE",
    "sorry": "SORRY",
    "thank_you": "THANK YOU",
    "yes": "YES",
    "Waiting...": "Waiting...",
    "Uncertain": "Uncertain"
}

SPEECH_LABEL_MAP = {
    "hello": "Hello",
    "help": "Help",
    "love": "I love you",
    "no": "No",
    "please": "Please",
    "sorry": "Sorry",
    "thank_you": "Thank you",
    "yes": "Yes"
}

SIGN_GUIDE_DATA = {
    "HELLO": {
        "icon": "👋",
        "label": "HELLO",
        "instructions": "Raise dominant hand to shoulder height with open palm and wave naturally from side to side.",
        "dataset_note": "Standard waving greeting motion across 30 frames."
    },
    "THANK YOU": {
        "icon": "🙏",
        "label": "THANK YOU",
        "instructions": "Touch fingertips to chin/lips and move hand smoothly forward toward the camera.",
        "dataset_note": "Chin-to-front forward trajectory."
    },
    "YES": {
        "icon": "🙆",
        "label": "YES",
        "instructions": "Form a relaxed fist at chest level and nod your wrist up and down repeatedly.",
        "dataset_note": "Vertical wrist nod motion representing nodding head."
    },
    "NO": {
        "icon": "🙅",
        "label": "NO",
        "instructions": "Extend index and middle fingers together and snap them down onto the thumb.",
        "dataset_note": "Index-middle finger pinch snap."
    },
    "HELP": {
        "icon": "🆘",
        "label": "HELP",
        "instructions": "Place a closed fist with thumb upright upon an open flat palm and elevate both slightly.",
        "dataset_note": "Dual-hand supportive elevation gesture."
    },
    "LOVE": {
        "icon": "🤟",
        "label": "LOVE",
        "instructions": "Extend thumb, index, and pinky fingers while curling middle and ring fingers down.",
        "dataset_note": "Standard I-Love-You ASL handshape."
    },
    "PLEASE": {
        "icon": "🤲",
        "label": "PLEASE",
        "instructions": "Place open flat palm against center of chest and rub in a gentle circular motion.",
        "dataset_note": "Chest-centered circular palm motion."
    },
    "SORRY": {
        "icon": "✊",
        "label": "SORRY",
        "instructions": "Form a fist against center of chest and rub in a gentle circular motion.",
        "dataset_note": "Chest-centered circular fist apology."
    }
}

# ============================================================
# CACHED RECOGNIZER SINGLETON
# ============================================================

@st.cache_resource(show_spinner="Initializing neural recognition model...")
def get_cached_recognizer() -> SignLanguageRecognizer:
    return SignLanguageRecognizer()


# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

if "current_nav" not in st.session_state:
    st.session_state.current_nav = "Live Tracking"

if "practice_sign" not in st.session_state:
    st.session_state.practice_sign = None


# ============================================================
# HUD HTML BUILDER (CLEAN & ERROR-FREE)
# ============================================================

def build_hud_html(res: dict, last_spoken: str, last_spoken_time: float) -> str:
    """Builds clean, unindented HTML for the Apple Neural Console."""
    if not res:
        pred_label = "Waiting..."
        conf_val = 0.0
        frames = 0
        hand_detected = False
        is_latched = False
    else:
        pred_label = res.get("display_prediction") or res.get("prediction", "Waiting...")
        conf_val = res.get("display_confidence", 0.0) if res.get("display_confidence", 0.0) > 0 else res.get("confidence", 0.0)
        frames = res.get("frames", 0)
        hand_detected = res.get("hand_detected", False)
        is_latched = res.get("is_latched", False)

    formatted_sign = DISPLAY_LABEL_MAP.get(pred_label, pred_label.upper())
    buffer_pct = int(min(frames / float(SEQUENCE_LENGTH), 1.0) * 100)

    is_recognized = is_latched or (pred_label in DISPLAY_LABEL_MAP and pred_label not in ("Waiting...", "Uncertain") and conf_val >= 0.60)

    if is_recognized:
        status_text = "Gesture Recognized"
        status_dot = "#00E676"
        sign_display = formatted_sign
        sign_class = ""
        conf_display = f"{conf_val * 100.0:.1f}% Confidence"
        conf_class = ""
    elif hand_detected:
        if frames < 12:
            status_text = f"Tracking Motion ({frames}/{SEQUENCE_LENGTH})"
            status_dot = "#FF9500"
            sign_display = "Tracking..."
            sign_class = " waiting"
            conf_display = f"Capturing motion ({frames}/{SEQUENCE_LENGTH})"
            conf_class = " waiting"
        else:
            status_text = "Classifying Sequence"
            status_dot = "#007AFF"
            sign_display = formatted_sign if conf_val >= 0.55 else "Evaluating..."
            sign_class = "" if conf_val >= 0.55 else " waiting"
            conf_display = f"{conf_val * 100.0:.1f}% Confidence"
            conf_class = ""
    else:
        status_text = "Show Hand to Camera"
        status_dot = "#8E8E93"
        sign_display = "Waiting..."
        sign_class = " waiting"
        conf_display = "Position hand in frame"
        conf_class = " waiting"

    now = time.perf_counter()
    if last_spoken and (now - last_spoken_time) < 4.0:
        audio_text = f'Spoken: "{SPEECH_LABEL_MAP.get(last_spoken, last_spoken)}"'
        audio_dot = "#00E676"
    else:
        audio_text = "Voice Output: Active"
        audio_dot = "#8E8E93"

    html = f"""<div class="apple-hud-card">
  <div class="apple-hud-status-badge">
    <span class="apple-hud-indicator" style="background-color: {status_dot};"></span>
    <span>{status_text}</span>
  </div>
  <div>
    <div class="apple-hud-label">Recognized Gesture</div>
    <div class="apple-hud-main-val{sign_class}">{sign_display}</div>
  </div>
  <div>
    <span class="apple-hud-conf-badge{conf_class}">{conf_display}</span>
  </div>
  <div>
    <div class="apple-hud-buffer-header">
      <span>Temporal Buffer</span>
      <span>{frames} / {SEQUENCE_LENGTH} Frames</span>
    </div>
    <div class="apple-hud-progress-bg">
      <div class="apple-hud-progress-bar" style="width: {buffer_pct}%;"></div>
    </div>
  </div>
  <div class="apple-hud-audio-status">
    <span style="color: {audio_dot};">●</span>
    <span>{audio_text}</span>
  </div>
</div>"""
    return html


# ============================================================
# 1. APPLE MINIMALIST NAVBAR
# ============================================================

NAV_OPTIONS = ["Live Tracking", "Gesture Library", "Neural Architecture", "Accessibility"]

nav_col1, nav_col2 = st.columns([1.2, 2.6], vertical_alignment="center")

with nav_col1:
    st.html(
        """
        <div class="apple-nav-brand">
            <span style="font-size: 1.35rem;"></span>
            <span>SignFlow</span>
            <span class="apple-nav-badge">AI Vision</span>
        </div>
        """
    )

with nav_col2:
    selected_nav = st.segmented_control(
        "Navigation",
        NAV_OPTIONS,
        default=st.session_state.current_nav,
        key="apple_nav_control",
        label_visibility="collapsed"
    )
    if selected_nav and selected_nav != st.session_state.current_nav:
        st.session_state.current_nav = selected_nav
        st.rerun()

current_view = st.session_state.current_nav
st.html("<div style='height: 12px;'></div>")

# ============================================================
# VIEW 1: LIVE TRACKING
# ============================================================

if current_view == "Live Tracking":

    # Hero
    st.html(
        """
        <div class="apple-hero">
            <div class="apple-hero-eyebrow">Neural Sign Language Recognition</div>
            <h1 class="apple-hero-title">Powerful gestures.<br>Instantly recognized.</h1>
            <p class="apple-hero-desc">
                Real-time MediaPipe holistic landmark tracking, 30-frame temporal LSTM modeling,
                and low-latency vocal synthesis. Camera starts automatically.
            </p>
        </div>
        """
    )

    if st.session_state.practice_sign:
        prac_c1, prac_c2 = st.columns([3.5, 1.0], vertical_alignment="center")
        with prac_c1:
            st.html(
                f"""
                <div style="background: #FFFFFF; border: 1px solid #1D1D1F; border-radius: 9999px; padding: 10px 24px; text-align: center; font-weight: 600; font-size: 0.88rem; color: #1D1D1F; box-shadow: 0 2px 8px rgba(0,0,0,0.04);">
                    Practice Mode &bull; Focus camera on <strong>{st.session_state.practice_sign}</strong> gesture
                </div>
                """
            )
        with prac_c2:
            if st.button("Exit Practice ✕", key="exit_prac_btn", width="stretch"):
                st.session_state.practice_sign = None
                st.rerun()

    # Bento Grid: Camera Viewport (Left) + Neural Console (Right)
    cam_col, hud_col = st.columns([1.25, 0.95], gap="large")

    with cam_col:
        st.html(
            """
            <div class="apple-section-header">
                <span class="apple-section-title">Camera Viewport</span>
                <span class="apple-section-meta">Live Video Stream</span>
            </div>
            """
        )
        cam_placeholder = st.empty()

    with hud_col:
        st.html(
            """
            <div class="apple-section-header">
                <span class="apple-section-title">Neural Console</span>
                <span class="apple-section-meta">Real-Time Inference</span>
            </div>
            """
        )
        hud_placeholder = st.empty()
        hud_placeholder.html(build_hud_html(None, "", 0.0))

    # Supported Gestures Grid
    st.html("<div style='height: 28px;'></div>")
    st.html(
        """
        <div class="apple-section-header">
            <span class="apple-section-title">Supported Gestures</span>
            <span class="apple-section-meta">Core Vocabulary &bull; 8 Classes</span>
        </div>
        """
    )

    sign_keys = ["HELLO", "THANK YOU", "YES", "NO", "HELP", "LOVE", "PLEASE", "SORRY"]
    for row_start in range(0, len(sign_keys), 4):
        cols = st.columns(4, gap="medium")
        for idx, sk in enumerate(sign_keys[row_start : row_start + 4]):
            info = SIGN_GUIDE_DATA[sk]
            with cols[idx]:
                st.html(
                    f"""
                    <div class="apple-gesture-card">
                        <div>
                            <div style="font-size: 2rem; margin-bottom: 0.6rem;">{info['icon']}</div>
                            <div style="font-size: 1.15rem; font-weight: 700; color: #1D1D1F; margin-bottom: 0.4rem;">{info['label']}</div>
                            <div style="font-size: 0.85rem; color: #86868B; line-height: 1.45; margin-bottom: 1rem;">{info['instructions']}</div>
                        </div>
                        <div style="font-size: 0.72rem; font-weight: 600; text-transform: uppercase; color: #86868B; border-top: 1px solid #E5E5EA; padding-top: 0.6rem; margin-bottom: 0.8rem;">
                            {info['dataset_note']}
                        </div>
                    </div>
                    """
                )
                if st.button(f"Practice {info['label']}", key=f"prac_btn_{sk}", width="stretch"):
                    st.session_state.practice_sign = info['label']
                    st.rerun()

    # ============================================================
    # AUTOMATIC REAL-TIME WEBCAM STREAMING & INFERENCE LOOP
    # ============================================================
    rec = get_cached_recognizer()

    # Fast direct OpenCV capture (no buttons required)
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        cam_placeholder.error(
            "⚠️ Camera could not be opened. Please verify that your webcam is connected and not currently used by another application."
        )
    else:
        try:
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

            last_speech_time = 0.0
            last_spoken_sign = ""
            last_hud_time = 0.0

            while True:
                ret, frame = cap.read()
                if not ret:
                    time.sleep(0.02)
                    continue

                # 1. Full ML pipeline inference (258 features, 30 temporal frames, LSTM)
                res = rec.process_frame(frame, mirror_display=True)
                ann_bgr = res.get("annotated_frame", frame)

                # 2. Ultra-lightweight JPEG compression (~30KB per frame, prevents backend collapse)
                ret_enc, jpeg_buf = cv2.imencode('.jpg', ann_bgr, [cv2.IMWRITE_JPEG_QUALITY, 80])
                if ret_enc:
                    cam_placeholder.image(jpeg_buf.tobytes(), output_format="JPEG", width="stretch")

                # 3. Speech synthesis handling
                active_pred = res.get("display_prediction") or res.get("prediction", "Waiting...")
                active_conf = res.get("display_confidence", 0.0) if res.get("display_confidence", 0.0) > 0 else res.get("confidence", 0.0)
                curr_t = time.perf_counter()

                if active_pred in SPEECH_LABEL_MAP and active_conf >= 0.65:
                    if active_pred != last_spoken_sign or (curr_t - last_speech_time) >= 2.0:
                        speak_text(SPEECH_LABEL_MAP[active_pred])
                        last_spoken_sign = active_pred
                        last_speech_time = curr_t

                # 4. Neural Console HUD update (throttled to ~10 Hz for silky smooth UI)
                if curr_t - last_hud_time >= 0.09:
                    last_hud_time = curr_t
                    hud_placeholder.html(build_hud_html(res, last_spoken_sign, last_speech_time))

                # Yield slightly to OS and event loop
                time.sleep(0.015)
        finally:
            cap.release()


# ============================================================
# VIEW 2: GESTURE LIBRARY
# ============================================================

elif current_view == "Gesture Library":
    st.html(
        """
        <div class="apple-hero">
            <div class="apple-hero-eyebrow">Gesture Reference Guide</div>
            <h1 class="apple-hero-title">Core Vocabulary</h1>
            <p class="apple-hero-desc">
                Kinematics and execution guidelines for all gestures supported by our neural network.
            </p>
        </div>
        """
    )

    sign_items = list(SIGN_GUIDE_DATA.items())
    for chunk_start in range(0, len(sign_items), 2):
        g_cols = st.columns(2, gap="large")
        for col_idx, (sign_key, info) in enumerate(sign_items[chunk_start : chunk_start + 2]):
            with g_cols[col_idx]:
                st.html(
                    f"""
                    <div class="apple-card" style="margin-bottom: 1.5rem; min-height: 220px;">
                        <div>
                            <div style="font-size: 2.4rem; margin-bottom: 0.8rem;">{info['icon']}</div>
                            <div style="font-size: 1.35rem; font-weight: 700; color: #1D1D1F; margin-bottom: 0.5rem;">{info['label']}</div>
                            <div style="font-size: 0.92rem; color: #6E6E73; line-height: 1.5; margin-bottom: 1.2rem;">{info['instructions']}</div>
                        </div>
                        <div style="font-size: 0.74rem; font-weight: 600; text-transform: uppercase; color: #86868B; border-top: 1px solid #E5E5EA; padding-top: 0.6rem;">
                            {info['dataset_note']}
                        </div>
                    </div>
                    """
                )
                if st.button(f"Practice {info['label']} on Camera", key=f"lib_prac_{sign_key}", width="stretch"):
                    st.session_state.practice_sign = info['label']
                    st.session_state.current_nav = "Live Tracking"
                    st.rerun()


# ============================================================
# VIEW 3: NEURAL ARCHITECTURE
# ============================================================

elif current_view == "Neural Architecture":
    st.html(
        """
        <div class="apple-hero">
            <div class="apple-hero-eyebrow">Specifications & Benchmark</div>
            <h1 class="apple-hero-title">Neural Architecture</h1>
            <p class="apple-hero-desc">
                Spatial holistic landmark extraction, temporal tensor buffering, and LSTM classification metrics.
            </p>
        </div>
        """
    )

    arch_c1, arch_c2 = st.columns(2, gap="large")
    with arch_c1:
        st.html(
            """
            <div class="apple-card" style="height: 100%;">
                <div style="font-size: 1.25rem; font-weight: 700; color: #1D1D1F; margin-bottom: 0.8rem;">258-Feature Vector Breakdown</div>
                <div style="font-size: 0.92rem; color: #6E6E73; line-height: 1.65;">
                    &bull; <strong>Pose Landmarks</strong>: 33 keypoints &times; 4 values (x, y, z, visibility) = 132 features<br>
                    &bull; <strong>Left Hand Landmarks</strong>: 21 keypoints &times; 3 values (x, y, z) = 63 features<br>
                    &bull; <strong>Right Hand Landmarks</strong>: 21 keypoints &times; 3 values (x, y, z) = 63 features<br><br>
                    <strong>Total Feature Dimension</strong>: 132 + 63 + 63 = 258 features per frame.<br>
                    <strong>Input Tensor Shape</strong>: <code>(30, 258)</code> representing a 30-frame temporal window.
                </div>
                <div style="font-size: 0.74rem; font-weight: 600; text-transform: uppercase; color: #86868B; margin-top: 1.2rem; border-top: 1px solid #E5E5EA; padding-top: 0.6rem;">
                    MediaPipe Tasks HolisticLandmarker &bull; LIVE TRACKING Mode
                </div>
            </div>
            """
        )

    with arch_c2:
        st.html(
            """
            <div class="apple-card" style="height: 100%;">
                <div style="font-size: 1.25rem; font-weight: 700; color: #1D1D1F; margin-bottom: 0.8rem;">2-Layer LSTM Classification</div>
                <div style="font-size: 0.92rem; color: #6E6E73; line-height: 1.65;">
                    &bull; <strong>Layer 1</strong>: LSTM (128 units, return_sequences=True) + Dropout (0.3)<br>
                    &bull; <strong>Layer 2</strong>: LSTM (64 units, return_sequences=False) + Dropout (0.3)<br>
                    &bull; <strong>Dense Hidden</strong>: Dense (64 units, ReLU) + Dropout (0.3)<br>
                    &bull; <strong>Softmax Output</strong>: Dense (8 classes, Softmax)<br><br>
                    <strong>Decision Rules</strong>: Confidence &ge; 60%, 5 / 7 temporal voting filter.
                </div>
                <div style="font-size: 0.74rem; font-weight: 600; text-transform: uppercase; color: #86868B; margin-top: 1.2rem; border-top: 1px solid #E5E5EA; padding-top: 0.6rem;">
                    models/sign_language_lstm_best.keras &bull; TensorFlow 2.21
                </div>
            </div>
            """
        )

    st.html("<div style='height: 24px;'></div>")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.html(
            """
            <div class="apple-card" style="text-align: center; padding: 1.5rem;">
                <div style="font-size: 0.74rem; font-weight: 600; text-transform: uppercase; color: #86868B;">Test Samples</div>
                <div style="font-size: 2.2rem; font-weight: 800; color: #1D1D1F;">450</div>
            </div>
            """
        )
    with m2:
        st.html(
            """
            <div class="apple-card" style="text-align: center; padding: 1.5rem;">
                <div style="font-size: 0.74rem; font-weight: 600; text-transform: uppercase; color: #86868B;">Accuracy</div>
                <div style="font-size: 2.2rem; font-weight: 800; color: #1D1D1F;">98.44%</div>
            </div>
            """
        )
    with m3:
        st.html(
            """
            <div class="apple-card" style="text-align: center; padding: 1.5rem;">
                <div style="font-size: 0.74rem; font-weight: 600; text-transform: uppercase; color: #86868B;">Macro F1</div>
                <div style="font-size: 2.2rem; font-weight: 800; color: #1D1D1F;">98.32%</div>
            </div>
            """
        )
    with m4:
        st.html(
            """
            <div class="apple-card" style="text-align: center; padding: 1.5rem;">
                <div style="font-size: 0.74rem; font-weight: 600; text-transform: uppercase; color: #86868B;">Loss</div>
                <div style="font-size: 2.2rem; font-weight: 800; color: #1D1D1F;">0.0414</div>
            </div>
            """
        )


# ============================================================
# VIEW 4: ACCESSIBILITY
# ============================================================

elif current_view == "Accessibility":
    st.html(
        """
        <div class="apple-hero">
            <div class="apple-hero-eyebrow">Assistive Technology</div>
            <h1 class="apple-hero-title">Accessible by Design</h1>
            <p class="apple-hero-desc">
                Sign Language Recognition for Accessibility &bull; An open, browser-native assistive bridge
                connecting signers and non-signers without proprietary hardware.
            </p>
        </div>
        """
    )

    acc_c1, acc_c2 = st.columns(2, gap="large")
    with acc_c1:
        st.html(
            """
            <div class="apple-card">
                <div style="font-size: 1.25rem; font-weight: 700; color: #1D1D1F; margin-bottom: 0.8rem;">Zero Hardware Barrier</div>
                <div style="font-size: 0.92rem; color: #6E6E73; line-height: 1.65;">
                    SignFlow runs entirely through standard consumer webcams, eliminating the cost and constraint
                    of specialized gloves or depth cameras. Computer vision processes frames in real-time right in your browser.
                </div>
            </div>
            """
        )
    with acc_c2:
        st.html(
            """
            <div class="apple-card">
                <div style="font-size: 1.25rem; font-weight: 700; color: #1D1D1F; margin-bottom: 0.8rem;">Multi-Sensory Feedback</div>
                <div style="font-size: 0.92rem; color: #6E6E73; line-height: 1.65;">
                    Combines real-time visual landmark overlays, high-contrast dynamic recognition indicators, and asynchronous
                    vocal speech synthesis via pyttsx3, ensuring communication is bidirectional and accessible.
                </div>
            </div>
            """
        )

# ============================================================
# APPLE MINIMALIST FOOTER
# ============================================================

st.html(
    """
    <div style="text-align: center; padding: 3rem 1rem 1rem; border-top: 1px solid #E5E5EA; margin-top: 3.5rem;">
        <div style="font-size: 0.85rem; font-weight: 600; color: #1D1D1F; margin-bottom: 4px;">SignFlow &bull; Neural Accessibility</div>
        <div style="font-size: 0.78rem; color: #86868B;">Designed with Apple minimalist aesthetic &bull; MediaPipe Tasks &amp; LSTM Neural Network</div>
    </div>
    """
)
