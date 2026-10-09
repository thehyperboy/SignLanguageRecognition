import sys
import os
sys.path.insert(0, os.path.abspath("."))

import mediapipe as mp
import inspect

print("Inspect HolisticLandmarkerResult:")
from mediapipe.tasks.python.vision import HolisticLandmarkerResult
print("HolisticLandmarkerResult annotations / fields:")
if hasattr(HolisticLandmarkerResult, '__annotations__'):
    print(HolisticLandmarkerResult.__annotations__)
