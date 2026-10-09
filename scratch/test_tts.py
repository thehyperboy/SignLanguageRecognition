import sys
import os
sys.path.insert(0, os.path.abspath("."))

from src.speech import TTSEngineWorker
import traceback

class DebugTTSEngineWorker(TTSEngineWorker):
    def _worker_loop(self):
        try:
            import pyttsx3
            try:
                import pythoncom
                pythoncom.CoInitialize()
            except Exception:
                pass
            print("Initializing pyttsx3 engine in worker loop...")
            self.engine = pyttsx3.init()
            self.engine.setProperty("rate", self.rate)
            self.engine.setProperty("volume", self.volume)

            voices = self.engine.getProperty("voices")
            print("Voices found:", len(voices) if voices else 0)
            if voices and 0 <= self.voice_index < len(voices):
                self.engine.setProperty("voice", voices[self.voice_index].id)

            self.initialized_successfully = True
            print("Engine initialized successfully!")
        except Exception as exc:
            print("Exception in worker loop:")
            traceback.print_exc()
            self.initialized_successfully = False
            self.is_running = False
            return

w = DebugTTSEngineWorker()
import time
time.sleep(2)
print("Worker initialized_successfully:", w.initialized_successfully)
w.stop()
