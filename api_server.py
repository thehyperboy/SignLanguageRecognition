"""
Sign Language Recognition - High-Performance Web Bridge Server
==============================================================
Module: api_server.py

Provides a high-throughput, low-latency Starlette/Uvicorn WebSocket and HTTP API
to connect the React + Vite frontend directly to the authoritative Python ML pipeline
WITHOUT altering any existing ML models, training files, or inference logic.

Exposes:
- GET  /api/health      : Status, device info, loaded classes
- GET  /api/vocabulary  : Supported gesture vocabulary metadata
- POST /api/predict     : Single-frame HTTP inference
- POST /api/reset       : Flushes the 30-frame temporal buffer
- WS   /ws/stream       : 30 FPS bidirectional real-time video inference stream
"""

import sys
import time
import base64
import json
import hashlib
import secrets
import uuid
from pathlib import Path

import cv2
import numpy as np
import uvicorn
from starlette.applications import Starlette
from starlette.responses import JSONResponse, Response
from starlette.routing import Route, WebSocketRoute
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocket, WebSocketDisconnect

# Ensure project root is in sys.path
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.inference import SignLanguageRecognizer, FRAME_WIDTH, FRAME_HEIGHT
from src.speech import speak_text

# Initialize cached inference engine
print("[API] Initializing authoritative SignLanguageRecognizer...")
recognizer = SignLanguageRecognizer()
print("[API] SignLanguageRecognizer ready with", len(recognizer.label_map), "classes.")

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

VOCABULARY = [
    {
        "id": "hello",
        "name": "HELLO",
        "icon": "👋",
        "description": "Raise dominant hand to shoulder height with open palm and wave naturally.",
        "difficulty": "Easy",
        "tag": "Greeting"
    },
    {
        "id": "thank_you",
        "name": "THANK YOU",
        "icon": "🙏",
        "description": "Touch fingertips to chin/lips and extend hand smoothly forward toward camera.",
        "difficulty": "Easy",
        "tag": "Courtesy"
    },
    {
        "id": "yes",
        "name": "YES",
        "icon": "🙆",
        "description": "Form a relaxed fist at chest level and nod your wrist up and down repeatedly.",
        "difficulty": "Easy",
        "tag": "Affirmation"
    },
    {
        "id": "no",
        "name": "NO",
        "icon": "🙅",
        "description": "Extend index and middle fingers together and snap them down onto the thumb.",
        "difficulty": "Medium",
        "tag": "Negation"
    },
    {
        "id": "help",
        "name": "HELP",
        "icon": "🆘",
        "description": "Place closed fist with upright thumb upon flat open palm and elevate slightly.",
        "difficulty": "Medium",
        "tag": "Assistance"
    },
    {
        "id": "love",
        "name": "LOVE",
        "icon": "🤟",
        "description": "Extend thumb, index, and pinky fingers while curling middle and ring down.",
        "difficulty": "Easy",
        "tag": "Emotion"
    },
    {
        "id": "please",
        "name": "PLEASE",
        "icon": "🤲",
        "description": "Place flat open palm over center of chest and rotate in a smooth circular motion.",
        "difficulty": "Easy",
        "tag": "Courtesy"
    },
    {
        "id": "sorry",
        "name": "SORRY",
        "icon": "✊",
        "description": "Form a fist against center of chest and rub in a gentle circular motion.",
        "difficulty": "Easy",
        "tag": "Courtesy"
    }
]

# Track speech timestamps
last_speech_time = 0.0
last_spoken_sign = ""


async def health(request):
    """Health check endpoint."""
    return JSONResponse({
        "status": "healthy",
        "model": "models/sign_language_lstm_best.keras",
        "classes": list(recognizer.label_map.values()),
        "sequence_length": recognizer.sequence_length,
        "feature_dimension": recognizer.expected_features
    })


async def get_vocabulary(request):
    """Returns supported gesture vocabulary."""
    return JSONResponse({
        "vocabulary": VOCABULARY,
        "count": len(VOCABULARY)
    })


async def reset_buffer(request):
    """Resets the sequence buffer in memory."""
    recognizer.reset()
    return JSONResponse({
        "status": "reset_successful",
        "frames": 0,
        "prediction": "Waiting..."
    })


def process_b64_image(b64_str: str) -> dict:
    """Helper to decode base64, process with inference engine, and return payload."""
    global last_speech_time, last_spoken_sign

    if "," in b64_str:
        b64_str = b64_str.split(",", 1)[1]

    img_bytes = base64.b64decode(b64_str)
    nparr = np.frombuffer(img_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if frame is None:
        return {"error": "Invalid image data"}

    res = recognizer.process_frame(frame, mirror_display=False)
    ann_bgr = res.get("annotated_frame", frame)

    # Compress annotated frame to lightweight high-speed JPEG base64 (quality 55 for sub-millisecond encoding)
    ret_enc, jpeg_buf = cv2.imencode('.jpg', ann_bgr, [cv2.IMWRITE_JPEG_QUALITY, 55])
    ann_b64 = ""
    if ret_enc:
        ann_b64 = "data:image/jpeg;base64," + base64.b64encode(jpeg_buf).decode("utf-8")

    # Speech synthesis handling
    pred = res.get("display_prediction") or res.get("prediction", "Waiting...")
    conf = res.get("display_confidence", 0.0)
    now = time.perf_counter()
    spoken = False

    if pred in SPEECH_LABEL_MAP and conf >= 0.48:
        if pred != last_spoken_sign or (now - last_speech_time) >= 2.0:
            speak_text(SPEECH_LABEL_MAP[pred])
            last_spoken_sign = pred
            last_speech_time = now
            spoken = True

    return {
        "prediction": res.get("prediction", "Waiting..."),
        "confidence": float(res.get("confidence", 0.0)),
        "display_prediction": res.get("display_prediction", "Waiting..."),
        "display_confidence": float(res.get("display_confidence", 0.0)),
        "is_latched": bool(res.get("is_latched", False)),
        "ready": bool(res.get("ready", False)),
        "frames": int(res.get("frames", 0)),
        "hand_detected": bool(res.get("hand_detected", False)),
        "left_hand_detected": bool(res.get("left_hand_detected", False)),
        "right_hand_detected": bool(res.get("right_hand_detected", False)),
        "pose_detected": bool(res.get("pose_detected", False)),
        "spoken": spoken,
        "last_spoken": last_spoken_sign,
        "annotated_frame": ann_b64,
        "error": None
    }


async def predict_http(request):
    """POST endpoint for single-frame inference."""
    try:
        body = await request.json()
        image_data = body.get("image", "")
        if not image_data:
            return JSONResponse({"error": "No image provided"}, status_code=400)

        payload = process_b64_image(image_data)
        return JSONResponse(payload)
    except Exception as exc:
        return JSONResponse({"error": str(exc)}, status_code=500)


async def websocket_stream(websocket: WebSocket):
    """High-throughput WebSocket for live continuous gesture streaming."""
    await websocket.accept()
    print("[API] WebSocket client connected.")
    try:
        while True:
            data = await websocket.receive_text()
            if not data:
                continue

            # Command or Frame
            if data == "RESET":
                recognizer.reset()
                await websocket.send_text(json.dumps({"type": "reset", "frames": 0}))
                continue

            try:
                payload = process_b64_image(data)
                payload["type"] = "inference"
                await websocket.send_text(json.dumps(payload))
            except (WebSocketDisconnect, RuntimeError):
                break
            except Exception as e:
                try:
                    await websocket.send_text(json.dumps({"type": "error", "message": str(e)}))
                except Exception:
                    break

    except WebSocketDisconnect:
        pass
    except Exception as exc:
        pass
    finally:
        print("[API] WebSocket client session closed.")


# ============================================================
# USER AUTHENTICATION & SESSION PERSISTENCE
# ============================================================

USERS_DB_PATH = Path(ROOT) / "data" / "users.json"
ACTIVE_SESSIONS = {}  # token -> email

def hash_password(password: str, salt: str = None) -> tuple[str, str]:
    if not salt:
        salt = secrets.token_hex(16)
    hashed = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return hashed, salt

def verify_password(password: str, hashed: str, salt: str) -> bool:
    calc_hash, _ = hash_password(password, salt)
    return secrets.compare_digest(calc_hash, hashed)

def load_users() -> dict:
    if not USERS_DB_PATH.exists():
        USERS_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        demo_hashed, demo_salt = hash_password("password123")
        initial_users = {
            "demo@signflow.ai": {
                "id": "usr_demo_001",
                "name": "Alex Morgan",
                "email": "demo@signflow.ai",
                "password_hash": demo_hashed,
                "salt": demo_salt,
                "role": "ASL Learner",
                "createdAt": "2026-10-30T12:00:00Z"
            }
        }
        with open(USERS_DB_PATH, "w", encoding="utf-8") as f:
            json.dump(initial_users, f, indent=2)
        return initial_users
    try:
        with open(USERS_DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def save_users(users: dict):
    USERS_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(USERS_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2)

async def auth_signup(request):
    """POST /api/auth/signup - Register new account"""
    try:
        body = await request.json()
        email = body.get("email", "").strip().lower()
        password = body.get("password", "")
        name = body.get("name", "").strip()
        role = body.get("role", "ASL Learner")

        if not email or "@" not in email:
            return JSONResponse({"error": "A valid email address is required"}, status_code=400)
        if not password or len(password) < 6:
            return JSONResponse({"error": "Password must be at least 6 characters long"}, status_code=400)
        if not name:
            name = email.split("@")[0].title()

        users = load_users()
        if email in users:
            return JSONResponse({"error": "An account with this email already exists"}, status_code=409)

        pwd_hash, salt = hash_password(password)
        user_id = f"usr_{uuid.uuid4().hex[:10]}"
        now_iso = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        new_user = {
            "id": user_id,
            "name": name,
            "email": email,
            "password_hash": pwd_hash,
            "salt": salt,
            "role": role,
            "createdAt": now_iso
        }
        users[email] = new_user
        save_users(users)

        token = f"sftk_{secrets.token_urlsafe(32)}"
        ACTIVE_SESSIONS[token] = email

        return JSONResponse({
            "success": True,
            "message": "Account created successfully",
            "token": token,
            "user": {
                "id": user_id,
                "name": name,
                "email": email,
                "role": role,
                "createdAt": now_iso
            }
        })
    except Exception as exc:
        return JSONResponse({"error": f"Registration failed: {str(exc)}"}, status_code=500)

async def auth_login(request):
    """POST /api/auth/login - Authenticate user"""
    try:
        body = await request.json()
        email = body.get("email", "").strip().lower()
        password = body.get("password", "")

        if not email or not password:
            return JSONResponse({"error": "Email and password are required"}, status_code=400)

        users = load_users()
        user = users.get(email)
        if not user or not verify_password(password, user["password_hash"], user["salt"]):
            return JSONResponse({"error": "Invalid email or password"}, status_code=401)

        token = f"sftk_{secrets.token_urlsafe(32)}"
        ACTIVE_SESSIONS[token] = email

        return JSONResponse({
            "success": True,
            "message": f"Welcome back, {user['name']}!",
            "token": token,
            "user": {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user.get("role", "ASL Learner"),
                "createdAt": user.get("createdAt")
            }
        })
    except Exception as exc:
        return JSONResponse({"error": f"Login failed: {str(exc)}"}, status_code=500)

async def auth_me(request):
    """GET /api/auth/me - Get current logged-in user profile"""
    auth_header = request.headers.get("Authorization", "")
    token = auth_header.replace("Bearer ", "").strip()
    if not token or token not in ACTIVE_SESSIONS:
        return JSONResponse({"error": "Not authenticated"}, status_code=401)
    
    email = ACTIVE_SESSIONS[token]
    users = load_users()
    user = users.get(email)
    if not user:
        return JSONResponse({"error": "User not found"}, status_code=404)

    return JSONResponse({
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user.get("role", "ASL Learner"),
            "createdAt": user.get("createdAt")
        }
    })

async def auth_forgot_password(request):
    """POST /api/auth/forgot-password - Simulated password reset request"""
    try:
        body = await request.json()
        email = body.get("email", "").strip().lower()
        if not email:
            return JSONResponse({"error": "Email is required"}, status_code=400)
        return JSONResponse({
            "success": True,
            "message": f"If an account with {email} exists, password reset instructions have been dispatched."
        })
    except Exception as exc:
        return JSONResponse({"error": str(exc)}, status_code=500)


routes = [
    Route("/api/health", health, methods=["GET"]),
    Route("/api/vocabulary", get_vocabulary, methods=["GET"]),
    Route("/api/reset", reset_buffer, methods=["POST"]),
    Route("/api/predict", predict_http, methods=["POST"]),
    Route("/api/auth/signup", auth_signup, methods=["POST"]),
    Route("/api/auth/login", auth_login, methods=["POST"]),
    Route("/api/auth/me", auth_me, methods=["GET"]),
    Route("/api/auth/forgot-password", auth_forgot_password, methods=["POST"]),
    WebSocketRoute("/ws/stream", websocket_stream),
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )
]

app = Starlette(debug=False, routes=routes, middleware=middleware)

if __name__ == "__main__":
    print("[API] Starting Uvicorn API server on http://localhost:8000 ...")
    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=False, workers=1)
