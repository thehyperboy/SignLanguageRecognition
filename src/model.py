"""
Sign Language Recognition - LSTM Model Architecture
---------------------------------------------------
Stage: Step 4 - Model Architecture Design & Initialization

Loads processed dataset metadata from data/processed/, automatically determines
sequence length, feature dimension, and number of sign classes, builds a 2-layer
LSTM neural network with Keras/TensorFlow, performs a forward-pass test on an untrained sample,
validates input/output shapes, and saves the initialized architecture to models/sign_language_lstm.keras.

Note: No model training (model.fit) is performed in this step.
"""

import json
import os
import sys
from pathlib import Path
import numpy as np
import tensorflow as tf

# ==============================================================================
# CONFIGURATION & REPRODUCIBILITY
# ==============================================================================

SEED = 42
tf.random.set_seed(SEED)
np.random.seed(SEED)

# Hyperparameters for baseline LSTM model architecture
LSTM_UNITS_1 = 128
LSTM_UNITS_2 = 64
DENSE_UNITS = 64
DROPOUT_RATE = 0.3
LEARNING_RATE = 0.001


# ==============================================================================
# METADATA & DATASET VALIDATION
# ==============================================================================

def load_dataset_metadata(processed_dir: Path):
    """
    Load preprocessed dataset tensors and label mapping from data/processed/.

    Returns:
        (X_train, y_train, X_val, y_val, X_test, y_test, label_map)
    """
    if not processed_dir.exists():
        raise FileNotFoundError(f"Processed dataset directory '{processed_dir}' does not exist.")

    required_files = [
        "X_train.npy", "y_train.npy",
        "X_val.npy", "y_val.npy",
        "X_test.npy", "y_test.npy",
        "label_map.json"
    ]

    for fname in required_files:
        fpath = processed_dir / fname
        if not fpath.exists():
            raise FileNotFoundError(f"Required processed file '{fname}' not found in '{processed_dir}'.")

    try:
        X_train = np.load(processed_dir / "X_train.npy")
        y_train = np.load(processed_dir / "y_train.npy")
        X_val = np.load(processed_dir / "X_val.npy")
        y_val = np.load(processed_dir / "y_val.npy")
        X_test = np.load(processed_dir / "X_test.npy")
        y_test = np.load(processed_dir / "y_test.npy")

        with open(processed_dir / "label_map.json", "r", encoding="utf-8") as f:
            label_map = json.load(f)

    except Exception as exc:
        raise RuntimeError(f"Error loading processed dataset files: {exc}")

    return X_train, y_train, X_val, y_val, X_test, y_test, label_map


def validate_dataset(X_train, y_train, X_val, y_val, X_test, y_test, label_map):
    """
    Validate sequence dimensions, channel consistency, and label counts.

    Returns:
        (sequence_length, feature_dimension, num_classes)
    """
    if X_train.ndim != 3 or X_val.ndim != 3 or X_test.ndim != 3:
        raise ValueError(f"Input feature arrays must be 3D (samples, sequence_length, feature_dimension). Got X_train.ndim={X_train.ndim}.")

    seq_len = X_train.shape[1]
    feat_dim = X_train.shape[2]

    if X_val.shape[1] != seq_len or X_test.shape[1] != seq_len:
        raise ValueError(f"Sequence length mismatch across splits: Train={seq_len}, Val={X_val.shape[1]}, Test={X_test.shape[1]}.")

    if X_val.shape[2] != feat_dim or X_test.shape[2] != feat_dim:
        raise ValueError(f"Feature dimension mismatch across splits: Train={feat_dim}, Val={X_val.shape[2]}, Test={X_test.shape[2]}.")

    if len(y_train) != len(X_train) or len(y_val) != len(X_val) or len(y_test) != len(X_test):
        raise ValueError("Sample count mismatch between feature matrices and label vectors.")

    num_classes = len(label_map)
    if num_classes < 2:
        print("\n" + "=" * 65)
        print("ERROR:")
        print("At least two sign classes are required to build a meaningful classification model.")
        print("=" * 65)
        sys.exit(1)

    return seq_len, feat_dim, num_classes


# ==============================================================================
# MODEL ARCHITECTURE & COMPILATION
# ==============================================================================

def build_lstm_model(sequence_length: int, feature_dimension: int, num_classes: int) -> tf.keras.Model:
    """
    Construct and compile a 2-layer Sequential LSTM architecture for gesture classification.

    Architecture:
      - LSTM (128 units, return_sequences=True)
      - Dropout (0.3)
      - LSTM (64 units, return_sequences=False)
      - Dropout (0.3)
      - Dense (64 units, ReLU)
      - Dropout (0.3)
      - Dense (num_classes, Softmax)

    Loss: sparse_categorical_crossentropy
    Optimizer: Adam (learning_rate=0.001)
    """
    # Architecture Explanation:
    # 1. The input sequence consists of 30 frames x 258 numerical landmarks per frame.
    # 2. Layer 1 LSTM processes full temporal trajectories and passes sequence outputs to Layer 2.
    # 3. Layer 2 LSTM compresses temporal sequence features into a fixed-length representation.
    # 4. Dense ReLU layer extracts higher-level non-linear feature combinations.
    # 5. Output Dense Softmax layer outputs probability distributions across sign gesture classes.

    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(shape=(sequence_length, feature_dimension), name="input_sequence"),
            tf.keras.layers.LSTM(
                LSTM_UNITS_1,
                return_sequences=True,
                name="lstm_layer_1",
            ),
            tf.keras.layers.Dropout(DROPOUT_RATE, name="dropout_1"),
            tf.keras.layers.LSTM(
                LSTM_UNITS_2,
                return_sequences=False,
                name="lstm_layer_2",
            ),
            tf.keras.layers.Dropout(DROPOUT_RATE, name="dropout_2"),
            tf.keras.layers.Dense(
                DENSE_UNITS,
                activation="relu",
                name="dense_hidden",
            ),
            tf.keras.layers.Dropout(DROPOUT_RATE, name="dropout_3"),
            tf.keras.layers.Dense(
                num_classes,
                activation="softmax",
                name="output_softmax",
            ),
        ],
        name="SignLanguageRecognition_LSTM",
    )

    optimizer = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)

    model.compile(
        optimizer=optimizer,
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )

    return model


def test_model_forward_pass(model: tf.keras.Model, X_sample: np.ndarray, label_map: dict):
    """
    Perform a single-sample forward pass test on untrained initialized model.
    Verifies output probability shape (1, num_classes) and finite predictions.
    """
    sample = X_sample[:1].astype(np.float32)
    prediction = model.predict(sample, verbose=0)

    pred_shape = prediction.shape
    predicted_class_idx = int(np.argmax(prediction[0]))

    # Invert label map: integer index -> class string name
    inv_label_map = {idx: name for name, idx in label_map.items()}
    predicted_sign_name = inv_label_map.get(predicted_class_idx, "Unknown")

    print("\nTesting forward pass...")
    print(f"Prediction shape: {pred_shape}")
    print(f"Initial predicted class: {predicted_class_idx}")
    print(f"Initial predicted sign: {predicted_sign_name}\n")
    print("NOTE:")
    print("This is an UNTRAINED model prediction.")
    print("It is NOT a recognition result.")

    return prediction, pred_shape


def validate_model(model: tf.keras.Model, sequence_length: int, feature_dimension: int, num_classes: int, prediction: np.ndarray):
    """Validate model architecture parameters, compilation status, and output shapes."""
    if model.optimizer is None:
        raise RuntimeError("Model compilation check failed: Optimizer is None.")

    if prediction.shape != (1, num_classes):
        raise ValueError(f"Output shape mismatch: Got {prediction.shape}, expected (1, {num_classes}).")

    if not np.isfinite(prediction).all():
        raise ValueError("Forward pass returned non-finite (NaN or Inf) predictions.")

    print("\n" + "=" * 40)
    print("MODEL VALIDATION PASSED")
    print("=" * 40)
    print("Input shape:")
    print(f"({sequence_length}, {feature_dimension})")
    print("\nOutput shape:")
    print(f"({num_classes})")
    print("\nForward pass:")
    print("SUCCESS")
    print("\nModel compilation:")
    print("SUCCESS")
    print("=" * 40)


def save_model(model: tf.keras.Model, save_path: Path):
    """Save initialized Keras model architecture to disk."""
    save_path.parent.mkdir(parents=True, exist_ok=True)
    model.save(save_path)

    if not save_path.exists():
        raise FileNotFoundError(f"Failed to verify saved model at '{save_path}'.")

    print(f"\nSaving model...")
    print(f"\nMODEL SAVED SUCCESSFULLY\n\n{save_path.as_posix()}")


# ==============================================================================
# MAIN PIPELINE
# ==============================================================================

def main():
    """Run Step 4 model setup, validation, forward pass test, and saving."""
    print("=" * 40)
    print("LSTM MODEL SETUP")
    print("=" * 40)
    print(f"TensorFlow version: {tf.__version__}\n")

    processed_dir = Path("data/processed")
    models_dir = Path("models")
    model_save_path = models_dir / "sign_language_lstm.keras"

    # 1. Load dataset metadata
    try:
        X_train, y_train, X_val, y_val, X_test, y_test, label_map = load_dataset_metadata(processed_dir)
    except Exception as exc:
        print(f"CRITICAL ERROR loading dataset metadata: {exc}")
        sys.exit(1)

    # 2. Validate shapes & determine model dimensions
    try:
        seq_length, feat_dim, num_classes = validate_dataset(X_train, y_train, X_val, y_val, X_test, y_test, label_map)
    except Exception as exc:
        print(f"CRITICAL ERROR during dataset validation: {exc}")
        sys.exit(1)

    print("Dataset:")
    print(f"X_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}\n")
    print(f"X_val shape: {X_val.shape}")
    print(f"y_val shape: {y_val.shape}\n")
    print(f"X_test shape: {X_test.shape}")
    print(f"y_test shape: {y_test.shape}\n")
    print(f"Sequence length: {seq_length}")
    print(f"Feature dimension: {feat_dim}")
    print(f"Number of classes: {num_classes}\n")

    print("Label mapping:")
    for name, idx in sorted(label_map.items(), key=lambda x: x[1]):
        print(f"{idx} -> {name}")

    # 3. Build & compile LSTM model
    print("\nBuilding LSTM model...\n")
    model = build_lstm_model(seq_length, feat_dim, num_classes)

    # Print Keras Model Summary
    print("Model summary:")
    model.summary()
    print("\nModel compiled successfully.")

    # 4. Perform forward pass test on 1 untrained sample
    prediction, _ = test_model_forward_pass(model, X_train, label_map)

    # 5. Validate model architecture & compilation
    validate_model(model, seq_length, feat_dim, num_classes, prediction)

    # 6. Save model architecture to models/sign_language_lstm.keras
    save_model(model, model_save_path)

    print("\n" + "=" * 40)
    print("STEP 4 COMPLETE")
    print("=" * 40)
    print("\nLSTM MODEL READY FOR TRAINING")
    print("=" * 40)


if __name__ == "__main__":
    main()
