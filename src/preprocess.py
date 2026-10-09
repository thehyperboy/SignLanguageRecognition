"""
Sign Language Recognition - Dataset Preprocessing Pipeline
------------------------------------------------------------
Stage: Step 3B - Data Preprocessing & Sequence Formatting

Loads raw .npy landmark sequences from dataset/, validates shapes and numerical health,
creates a deterministic label map, splits dataset into Train (70%), Validation (15%), Test (15%),
fits StandardScaler strictly on training data (no data leakage), scales datasets, and exports
processed arrays and metadata to data/processed/.
"""

import json
import os
import sys
from pathlib import Path
import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Fixed seed for reproducibility
RANDOM_STATE = 42


def load_and_validate_sequence(file_path: Path, expected_shape: tuple = None):
    """
    Load a single .npy file and validate its dimensions and numeric integrity.

    Returns:
        (data_array, is_valid, error_message, shape_tuple)
    """
    try:
        data = np.load(file_path)
    except Exception as exc:
        return None, False, f"Failed to load file '{file_path.name}': {exc}", None

    if not isinstance(data, np.ndarray):
        return None, False, f"File '{file_path.name}' is not a NumPy array.", None

    if data.ndim != 2:
        return None, False, f"File '{file_path.name}' has invalid dimensions {data.ndim}D (expected 2D: frames x features).", data.shape

    if expected_shape is not None and data.shape != expected_shape:
        return None, False, f"File '{file_path.name}' shape mismatch {data.shape}, expected {expected_shape}.", data.shape

    if np.isnan(data).any():
        return None, False, f"File '{file_path.name}' contains NaN values.", data.shape

    if np.isinf(data).any():
        return None, False, f"File '{file_path.name}' contains Infinite values.", data.shape

    return data, True, "", data.shape


def mirror_sequence(seq: np.ndarray) -> np.ndarray:
    """Mirrors a 30x258 sequence horizontally and swaps Left and Right Hand landmarks."""
    mirrored = seq.copy()
    # 1. Mirror Pose x coordinates (indices 0, 4, 8, ... up to 132)
    for i in range(0, 132, 4):
        mask = mirrored[:, i] > 0
        mirrored[mask, i] = 1.0 - mirrored[mask, i]

    # Swap Pose Left/Right landmark pairs (shoulders 11-12, elbows 13-14, wrists 15-16, etc.)
    POSE_PAIRS = [(11, 12), (13, 14), (15, 16), (23, 24)]
    for left_idx, right_idx in POSE_PAIRS:
        l_start = left_idx * 4
        r_start = right_idx * 4
        temp = mirrored[:, l_start : l_start + 4].copy()
        mirrored[:, l_start : l_start + 4] = mirrored[:, r_start : r_start + 4]
        mirrored[:, r_start : r_start + 4] = temp

    # 2. Swap Left Hand (132:195) and Right Hand (195:258)
    lh = seq[:, 132:195].copy()
    rh = seq[:, 195:258].copy()

    # Mirror x coordinates for hands (indices 0, 3, 6, ... up to 63)
    for i in range(0, 63, 3):
        l_mask = lh[:, i] > 0
        lh[l_mask, i] = 1.0 - lh[l_mask, i]
        r_mask = rh[:, i] > 0
        rh[r_mask, i] = 1.0 - rh[r_mask, i]

    mirrored[:, 132:195] = rh
    mirrored[:, 195:258] = lh
    return mirrored


def resample_temporal_sequence(seq: np.ndarray, speed_factor: float) -> np.ndarray:
    """Temporally speeds up (< 1.0) or slows down (> 1.0) a sequence and resamples back to 30 frames."""
    n_frames = len(seq)
    eff_len = int(np.clip(n_frames * speed_factor, 15, 45))
    orig_indices = np.linspace(0, n_frames - 1, eff_len)

    sampled = np.zeros((eff_len, seq.shape[1]), dtype=np.float32)
    for feat_idx in range(seq.shape[1]):
        sampled[:, feat_idx] = np.interp(orig_indices, np.arange(n_frames), seq[:, feat_idx])

    resampled = np.zeros((30, seq.shape[1]), dtype=np.float32)
    final_indices = np.linspace(0, eff_len - 1, 30)
    for feat_idx in range(seq.shape[1]):
        resampled[:, feat_idx] = np.interp(final_indices, np.arange(eff_len), sampled[:, feat_idx])

    return resampled


def jitter_sequence(seq: np.ndarray, noise_std: float = 0.006, translation: float = 0.012) -> np.ndarray:
    """Adds small spatial noise and translation to active landmarks."""
    jittered = seq.copy()
    active_mask = np.abs(jittered) > 1e-4
    noise = np.random.normal(0, noise_std, seq.shape).astype(np.float32)
    tx = np.random.uniform(-translation, translation)
    ty = np.random.uniform(-translation, translation)

    jittered[active_mask] += noise[active_mask]
    for i in list(range(0, 132, 4)) + list(range(132, 195, 3)) + list(range(195, 258, 3)):
        m = jittered[:, i] > 0
        jittered[m, i] += tx
    for i in list(range(1, 132, 4)) + list(range(133, 195, 3)) + list(range(196, 258, 3)):
        m = jittered[:, i] > 0
        jittered[m, i] += ty

    return np.clip(jittered, 0.0, 1.0)


def augment_sequence(seq: np.ndarray, sign_name: str) -> list[np.ndarray]:
    """Generates 5 realistic augmentations for each input sequence."""
    variants = []
    # 1. Mirrored sequence (horizontal flip + LH <-> RH swap)
    mirrored = mirror_sequence(seq)
    variants.append(mirrored)

    # 2. Faster execution (0.85x speed)
    fast = resample_temporal_sequence(seq, 0.85)
    variants.append(fast)

    # 3. Slower execution (1.15x speed)
    slow = resample_temporal_sequence(seq, 1.15)
    variants.append(slow)

    # 4. Spatial jitter and slight translation
    jittered = jitter_sequence(seq)
    variants.append(jittered)

    # 5. Mirrored + jittered
    mirrored_jittered = jitter_sequence(mirrored)
    variants.append(mirrored_jittered)

    # 6. Single-hand isolation (if dominant hand gesture, zero out inactive hand)
    if sign_name in ("hello", "yes", "no", "love", "sorry", "thank_you"):
        isolated_rh = seq.copy()
        isolated_rh[:, 132:195] = 0.0  # Inactive LH is completely zero
        variants.append(isolated_rh)

        isolated_lh = mirrored.copy()
        isolated_lh[:, 195:258] = 0.0  # Inactive RH is completely zero
        variants.append(isolated_lh)

    return variants


def discover_and_load_dataset(dataset_path: Path):
    """
    Discover all sign directories, validate raw files, and apply data augmentation.
    """
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset directory '{dataset_path}' does not exist.")

    sign_folders = sorted([d for d in dataset_path.iterdir() if d.is_dir()], key=lambda p: p.name)
    if not sign_folders:
        raise ValueError(f"No sign subdirectories found in '{dataset_path}'.")

    # Auto-detect shape from the first valid file
    expected_shape = None
    first_valid_file = None

    for folder in sign_folders:
        for file in sorted(folder.glob("*.npy")):
            _, is_valid, _, shape = load_and_validate_sequence(file)
            if is_valid:
                expected_shape = shape
                first_valid_file = file
                break
        if expected_shape is not None:
            break

    if expected_shape is None:
        raise ValueError(f"No valid .npy sequence files found in '{dataset_path}'.")

    sequence_length, feature_dimension = expected_shape
    print(f"Auto-detected Sequence Shape : ({sequence_length} frames, {feature_dimension} features)")
    print(f"First valid sequence reference : {first_valid_file.relative_to(dataset_path.parent)}")

    X_list = []
    y_list = []
    class_names = [folder.name for folder in sign_folders]
    label_map = {name: idx for idx, name in enumerate(class_names)}

    valid_count = 0
    invalid_count = 0
    class_counts = {name: 0 for name in class_names}

    for folder in sign_folders:
        sign_name = folder.name
        label_idx = label_map[sign_name]
        files = sorted(list(folder.glob("*.npy")))

        for file in files:
            data, is_valid, err_msg, _ = load_and_validate_sequence(file, expected_shape=expected_shape)
            if is_valid:
                # Add original sequence
                X_list.append(data)
                y_list.append(label_idx)
                valid_count += 1
                class_counts[sign_name] += 1

                # Generate and add augmented sequences
                for aug in augment_sequence(data, sign_name):
                    X_list.append(aug)
                    y_list.append(label_idx)
                    class_counts[sign_name] += 1
            else:
                invalid_count += 1
                print(f"  [REJECTED] {err_msg}")

    if valid_count == 0:
        raise ValueError("No valid sequences passed validation checks.")

    X = np.array(X_list, dtype=np.float32)
    y = np.array(y_list, dtype=np.int64)

    return X, y, class_names, sequence_length, feature_dimension, valid_count, invalid_count, class_counts


def create_label_mapping(class_names: list) -> dict:
    """Create a deterministic alphabetical mapping from class names to integer labels."""
    return {name: idx for idx, name in enumerate(sorted(class_names))}


def split_dataset(X: np.ndarray, y: np.ndarray):
    """
    Split dataset into 70% Train, 15% Validation, 15% Test.
    Uses reproducible random_state=42.
    Falls back gracefully if sample size is too small for stratification (e.g. test mode).
    """
    total_samples = len(X)
    unique_classes, counts = np.unique(y, return_counts=True)
    min_samples_per_class = min(counts) if len(counts) > 0 else 0

    # Determine if stratified splitting is possible
    can_stratify = len(unique_classes) > 1 and min_samples_per_class >= 3 and total_samples >= 10

    if not can_stratify:
        print("\n" + "!" * 65)
        print("WARNING: Dataset contains insufficient samples or single class for stratified split.")
        print("This dataset is only for pipeline testing.")
        print("Collect the full dataset before LSTM training.")
        print("!" * 65)

    if total_samples <= 3:
        # Extreme small test mode fallback (e.g., 2 samples)
        # Assign samples directly for pipeline verification without throwing split error
        print(" [TEST MODE] Assigning samples to splits for test mode pipeline verification.")
        X_train, y_train = X, y
        X_val, y_val = X, y
        X_test, y_test = X, y
        return X_train, y_train, X_val, y_val, X_test, y_test

    stratify_first = y if can_stratify else None
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.30, random_state=RANDOM_STATE, stratify=stratify_first
    )

    stratify_second = y_temp if can_stratify else None
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.50, random_state=RANDOM_STATE, stratify=stratify_second
    )

    return X_train, y_train, X_val, y_val, X_test, y_test


def fit_and_transform_scaler(X_train: np.ndarray, X_val: np.ndarray, X_test: np.ndarray):
    """
    Fit StandardScaler strictly on training data (preventing data leakage),
    then transform train, val, and test sequences.

    Maintains 3D sequence shape (samples, sequence_length, feature_dimension).
    """
    n_train, seq_len, feat_dim = X_train.shape
    n_val = X_val.shape[0]
    n_test = X_test.shape[0]

    # 1. Flatten 3D arrays to 2D for scaler fitting: (samples * sequence_length, feature_dimension)
    X_train_flat = X_train.reshape(-1, feat_dim)
    X_val_flat = X_val.reshape(-1, feat_dim)
    X_test_flat = X_test.reshape(-1, feat_dim)

    # 2. Fit StandardScaler ONLY on training data
    scaler = StandardScaler()
    scaler.fit(X_train_flat)

    # 3. Transform all splits using training scaler
    X_train_scaled_flat = scaler.transform(X_train_flat)
    X_val_scaled_flat = scaler.transform(X_val_flat)
    X_test_scaled_flat = scaler.transform(X_test_flat)

    # 4. Reshape back to 3D tensors: (samples, sequence_length, feature_dimension)
    X_train_scaled = X_train_scaled_flat.reshape(n_train, seq_len, feat_dim)
    X_val_scaled = X_val_scaled_flat.reshape(n_val, seq_len, feat_dim)
    X_test_scaled = X_test_scaled_flat.reshape(n_test, seq_len, feat_dim)

    return X_train_scaled, X_val_scaled, X_test_scaled, scaler


def plot_class_distribution(class_counts: dict, output_path: Path):
    """Generate and save class distribution bar chart using Matplotlib."""
    plt.figure(figsize=(10, 5))
    classes = list(class_counts.keys())
    counts = list(class_counts.values())

    colors = ["#1f77b4" for _ in classes]
    plt.bar(classes, counts, color=colors, edgecolor="black", alpha=0.8)
    plt.title("Sign Language Dataset Class Distribution", fontsize=14, fontweight="bold")
    plt.xlabel("Sign Class Name", fontsize=12)
    plt.ylabel("Number of Sequences", fontsize=12)
    plt.xticks(rotation=45, ha="right")
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()

    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()


def save_processed_data(
    output_dir: Path,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
    label_map: dict,
    scaler: StandardScaler,
    summary: dict,
):
    """Save all processed NumPy tensors, label mapping JSON, scaler pickle, and metadata summary."""
    output_dir.mkdir(parents=True, exist_ok=True)

    np.save(output_dir / "X_train.npy", X_train)
    np.save(output_dir / "y_train.npy", y_train)

    np.save(output_dir / "X_val.npy", X_val)
    np.save(output_dir / "y_val.npy", y_val)

    np.save(output_dir / "X_test.npy", X_test)
    np.save(output_dir / "y_test.npy", y_test)

    # Save Label Map JSON
    with open(output_dir / "label_map.json", "w", encoding="utf-8") as f:
        json.dump(label_map, f, indent=4)

    # Save Fitted Scaler Pickle
    joblib.dump(scaler, output_dir / "scaler.pkl")

    # Save Dataset Metadata Summary JSON
    with open(output_dir / "dataset_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=4)


def main():
    """Run full dataset preprocessing workflow."""
    print("=" * 65)
    print("SIGN LANGUAGE RECOGNITION - DATASET PREPROCESSING")
    print("=" * 65)

    raw_data_dir = Path("dataset")
    processed_dir = Path("data/processed")

    # 1. Discover and load raw dataset
    try:
        X, y, class_names, seq_length, feat_dim, valid_count, invalid_count, class_counts = discover_and_load_dataset(raw_data_dir)
    except Exception as exc:
        print(f"CRITICAL ERROR loading dataset: {exc}")
        sys.exit(1)

    print("\n--- CLASS BALANCE SUMMARY ---")
    for sign, count in class_counts.items():
        print(f"  {sign:<14} : {count} sequences")

    # 2. Create label map
    label_map = create_label_mapping(class_names)

    # 3. Train / Validation / Test Split (70% / 15% / 15%)
    X_train, y_train, X_val, y_val, X_test, y_test = split_dataset(X, y)

    # 4. Fit StandardScaler strictly on training set and transform all sets
    X_train_scaled, X_val_scaled, X_test_scaled, scaler = fit_and_transform_scaler(X_train, X_val, X_test)

    # 5. Plot class distribution
    dist_plot_path = processed_dir / "class_distribution.png"
    plot_class_distribution(class_counts, dist_plot_path)

    # 6. Prepare dataset summary dictionary
    summary = {
        "num_classes": len(class_names),
        "class_labels": label_map,
        "total_sequences": len(X),
        "valid_sequences": valid_count,
        "invalid_sequences": invalid_count,
        "sequence_length": seq_length,
        "feature_dimension": feat_dim,
        "train_samples": len(X_train_scaled),
        "validation_samples": len(X_val_scaled),
        "test_samples": len(X_test_scaled),
        "random_state": RANDOM_STATE,
    }

    # 7. Save outputs to data/processed/
    save_processed_data(
        processed_dir,
        X_train_scaled,
        y_train,
        X_val_scaled,
        y_val,
        X_test_scaled,
        y_test,
        label_map,
        scaler,
        summary,
    )

    # 8. Output Validation Checks
    nan_in_train = int(np.isnan(X_train_scaled).sum())
    inf_in_train = int(np.isinf(X_train_scaled).sum())
    nan_in_val = int(np.isnan(X_val_scaled).sum())
    inf_in_val = int(np.isinf(X_val_scaled).sum())
    nan_in_test = int(np.isnan(X_test_scaled).sum())
    inf_in_test = int(np.isinf(X_test_scaled).sum())
    total_nans = nan_in_train + nan_in_val + nan_in_test
    total_infs = inf_in_train + inf_in_val + inf_in_test

    print("\n" + "=" * 50)
    print("DATASET PREPROCESSING COMPLETE")
    print("=" * 50)
    print(f"Classes: {len(class_names)}")
    print(f"Total sequences: {len(X)}")
    print(f"Valid sequences: {valid_count}")
    print(f"Invalid sequences: {invalid_count}\n")
    print(f"Sequence length: {seq_length}")
    print(f"Feature dimension: {feat_dim}\n")
    print(f"Training samples: {len(X_train_scaled)}")
    print(f"Validation samples: {len(X_val_scaled)}")
    print(f"Testing samples: {len(X_test_scaled)}\n")
    print(f"Training shape: {X_train_scaled.shape}")
    print(f"Validation shape: {X_val_scaled.shape}")
    print(f"Testing shape: {X_test_scaled.shape}\n")
    print(f"NaN values: {total_nans}")
    print(f"Infinite values: {total_infs}\n")
    print(f"Label mapping saved:\n  {processed_dir / 'label_map.json'}\n")
    print(f"Scaler saved:\n  {processed_dir / 'scaler.pkl'}\n")
    print(f"Metadata summary saved:\n  {processed_dir / 'dataset_summary.json'}\n")
    print(f"Class distribution chart saved:\n  {processed_dir / 'class_distribution.png'}")
    print("=" * 50)
    print("\nDATASET READY FOR LSTM")
    print("=" * 50)


if __name__ == "__main__":
    main()
