"""
Sign Language Recognition - Dataset Inspection Script
------------------------------------------------------
Root alias script calling src/check_dataset.py.
"""

import sys
from pathlib import Path
from src.check_dataset import check_dataset

if __name__ == "__main__":
    valid = check_dataset(Path("dataset"))
    if not valid:
        sys.exit(1)
