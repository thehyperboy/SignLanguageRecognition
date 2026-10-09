"""
Sign Language Recognition - Dataset Inspection & Health Check
--------------------------------------------------------------
Stage: Step 3A - Data Validation Utility

Inspects the dataset directory, counts recorded sequences per sign, validates
array shapes, verifies feature dimension, checks for NaN/Infinite values, and reports
overall dataset validity.
"""

import sys
from pathlib import Path
import numpy as np


def check_dataset(dataset_path: Path = Path("dataset")) -> bool:
    """
    Find all .npy files in dataset folders, count sequences per sign,
    inspect shapes, verify numeric integrity (NaNs/Infs), and display summary.

    Returns:
        bool: True if dataset structure is VALID, False otherwise.
    """
    print("=" * 45)
    print("DATASET CHECK")
    print("=" * 45)

    if not dataset_path.exists():
        print(f"ERROR: Dataset directory '{dataset_path}' does not exist.")
        print("=" * 45)
        return False

    sign_folders = [d for d in dataset_path.iterdir() if d.is_dir()]
    if not sign_folders:
        print(f"WARNING: No sign folders found in '{dataset_path}'.")
        print("=" * 45)
        return False

    total_sequences = 0
    total_nan_count = 0
    total_inf_count = 0
    detected_feature_dim = None
    all_shapes = set()
    is_valid = True

    for sign_folder in sorted(sign_folders, key=lambda p: p.name):
        npy_files = sorted(list(sign_folder.glob("*.npy")))
        seq_count = len(npy_files)
        folder_shapes = set()

        for filepath in npy_files:
            try:
                data = np.load(filepath)
                folder_shapes.add(data.shape)
                all_shapes.add(data.shape)

                # Check for NaN and Infinite values
                nan_count = int(np.isnan(data).sum())
                inf_count = int(np.isinf(data).sum())

                total_nan_count += nan_count
                total_inf_count += inf_count

                if len(data.shape) == 2:
                    detected_feature_dim = data.shape[1]

            except Exception as exc:
                print(f"  ERROR loading '{filepath.name}': {exc}")
                is_valid = False

        total_sequences += seq_count

        if folder_shapes:
            shape_str = ", ".join(str(s) for s in sorted(folder_shapes))
        else:
            shape_str = "No .npy files found"

        print(f"\n{sign_folder.name}:")
        print(f"Sequences: {seq_count}")
        print(f"Shape: {shape_str}")

    print("\n" + "-" * 45)
    print(f"Total sequences: {total_sequences}")
    print(f"Feature dimension: {detected_feature_dim if detected_feature_dim is not None else 'N/A'}")
    print(f"\nNaN values: {total_nan_count}")
    print(f"Infinite values: {total_inf_count}")

    if total_sequences == 0:
        print("\nDATASET STRUCTURE: EMPTY (No sequences collected yet)")
        is_valid = False
    elif total_nan_count > 0 or total_inf_count > 0:
        print("\nDATASET STRUCTURE: INVALID (Contains NaN or Infinite values)")
        is_valid = False
    elif len(all_shapes) > 1:
        print("\nDATASET STRUCTURE: WARNING (Inconsistent sequence shapes detected)")
        is_valid = False
    else:
        print("\nDATASET STRUCTURE: VALID")

    print("=" * 45)
    return is_valid


if __name__ == "__main__":
    valid = check_dataset()
    if not valid:
        sys.exit(1)
