"""
Sign Language Recognition - Text-to-Speech (TTS) Module
--------------------------------------------------------
Stage: Step 8 - Text-to-Speech Integration

Provides an asynchronous, thread-safe speech synthesis interface using pyttsx3.
Uses a persistent background worker thread and thread-safe queue to ensure real-time
webcam frame processing is never frozen or delayed by audio output.

Includes safety checks and graceful exception handling for headless or unsupported environments.
"""

import queue
import threading
import time
from typing import Optional

try:
    import pyttsx3
    PYTTSX3_AVAILABLE = True
except ImportError:
    PYTTSX3_AVAILABLE = False


class TTSEngineWorker:
    """
    Persistent background worker managing a pyttsx3 text-to-speech engine loop.
    Communicates via a thread-safe Queue to perform asynchronous non-blocking speech.
    """

    def __init__(self, rate: int = 150, volume: float = 1.0, voice_index: int = 0):
        self.rate = rate
        self.volume = volume
        self.voice_index = voice_index
        self.speech_queue = queue.Queue()
        self.is_running = False
        self.thread: Optional[threading.Thread] = None
        self.engine = None
        self.initialized_successfully = False

        if PYTTSX3_AVAILABLE:
            self._start_worker_thread()

    def _start_worker_thread(self):
        """Start persistent background speech worker thread."""
        self.is_running = True
        self.thread = threading.Thread(target=self._worker_loop, daemon=True, name="TTSWorkerThread")
        self.thread.start()

    def _worker_loop(self):
        """Worker thread entry point. Initializes pyttsx3 in thread context and processes queue."""
        try:
            try:
                import pythoncom
                pythoncom.CoInitialize()
            except Exception:
                pass
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", self.rate)
            self.engine.setProperty("volume", self.volume)

            voices = self.engine.getProperty("voices")
            if voices and 0 <= self.voice_index < len(voices):
                self.engine.setProperty("voice", voices[self.voice_index].id)

            self.initialized_successfully = True
        except Exception as exc:
            print(f"[TTS WARNING] Speech engine failed to initialize: {exc}")
            self.initialized_successfully = False
            self.is_running = False
            return

        while self.is_running:
            try:
                # Wait for text item with timeout to check running flag
                text = self.speech_queue.get(timeout=0.2)
                if text is None:
                    # Termination sentinel
                    self.speech_queue.task_done()
                    break

                if isinstance(text, str) and text.strip():
                    cleaned_text = text.strip()
                    try:
                        self.engine.say(cleaned_text)
                        self.engine.runAndWait()
                    except Exception as speech_exc:
                        print(f"[TTS ERROR] Exception during speech output: {speech_exc}")

                self.speech_queue.task_done()
            except queue.Empty:
                continue
            except Exception as exc:
                print(f"[TTS ERROR] Unexpected queue error: {exc}")

        # Clean shutdown of pyttsx3 engine
        if self.engine:
            try:
                self.engine.stop()
            except Exception:
                pass

    def speak(self, text: str):
        """
        Enqueue text for background speech synthesis. Non-blocking.
        """
        if not PYTTSX3_AVAILABLE or not self.initialized_successfully:
            return

        if not text or not isinstance(text, str) or not text.strip():
            return

        # Avoid backlog buildup: if queue already has items waiting, clear older items
        while not self.speech_queue.empty():
            try:
                self.speech_queue.get_nowait()
                self.speech_queue.task_done()
            except queue.Empty:
                break

        self.speech_queue.put(text.strip())

    def set_rate(self, rate: int):
        """Update speech rate (words per minute)."""
        self.rate = rate
        if self.engine and self.initialized_successfully:
            try:
                self.engine.setProperty("rate", rate)
            except Exception:
                pass

    def set_volume(self, volume: float):
        """Update speech volume (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        if self.engine and self.initialized_successfully:
            try:
                self.engine.setProperty("volume", self.volume)
            except Exception:
                pass

    def set_voice(self, voice_index: int):
        """Set voice index."""
        self.voice_index = voice_index
        if self.engine and self.initialized_successfully:
            try:
                voices = self.engine.getProperty("voices")
                if voices and 0 <= voice_index < len(voices):
                    self.engine.setProperty("voice", voices[voice_index].id)
            except Exception:
                pass

    def stop(self):
        """Signal background worker thread to stop and flush queue."""
        if not self.is_running:
            return

        self.is_running = False
        try:
            self.speech_queue.put(None)
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=1.0)
        except Exception:
            pass


# Global module-level worker instance
_GLOBAL_TTS_WORKER: Optional[TTSEngineWorker] = None


def get_speech_worker() -> TTSEngineWorker:
    """Retrieve or initialize singleton TTS worker instance."""
    global _GLOBAL_TTS_WORKER
    if _GLOBAL_TTS_WORKER is None:
        _GLOBAL_TTS_WORKER = TTSEngineWorker()
    return _GLOBAL_TTS_WORKER


def speak_text(text: str):
    """
    Public utility function to synthesize speech for provided text string.
    Executes asynchronously in background without blocking calling thread.

    Args:
        text (str): Text phrase to speak.
    """
    worker = get_speech_worker()
    worker.speak(text)


def set_voice(voice_index: int):
    """Set voice index for speech engine."""
    worker = get_speech_worker()
    worker.set_voice(voice_index)


def set_rate(rate: int):
    """Set words per minute rate for speech engine."""
    worker = get_speech_worker()
    worker.set_rate(rate)


def set_volume(volume: float):
    """Set volume level (0.0 to 1.0) for speech engine."""
    worker = get_speech_worker()
    worker.set_volume(volume)


def shutdown_speech():
    """Cleanly shut down background speech engine and worker thread."""
    global _GLOBAL_TTS_WORKER
    if _GLOBAL_TTS_WORKER is not None:
        _GLOBAL_TTS_WORKER.stop()
        _GLOBAL_TTS_WORKER = None
