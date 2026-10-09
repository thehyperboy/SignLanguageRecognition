"""
Sign Language Recognition - LSTM Model Training Pipeline
--------------------------------------------------------
Stage: Step 5 - Model Training & Checkpoint Export

Loads preprocessed dataset tensors (X_train, y_train, X_val, y_val) from data/processed/,
imports the baseline 2-layer LSTM architecture from src.model, trains the model using
EarlyStopping, ModelCheckpoint, and ReduceLROnPlateau callbacks, exports training history JSON
and performance plots, and saves both the best checkpoint and final trained model.

Note: The test dataset (X_test, y_test) remains untouched for Step 6 formal evaluation.
"""

import json
import os
import sys
from pathlib import Path

# Add project root directory to sys.path to enable direct command execution: python src/train.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

from src.model import build_lstm_model, load_dataset_metadata

# ==============================================================================
# CONFIGURATION & REPRODUCIBILITY
# ==============================================================================

RANDOM_STATE = 42
tf.random.set_seed(RANDOM_STATE)
np.random.seed(RANDOM_STATE)

# Training hyperparameters
EPOCHS = 100
BATCH_SIZE = 32
LEARNING_RATE = 0.001


# ==============================================================================
# HELPER & VALIDATION FUNCTIONS
# ==============================================================================

def load_data(processed_dir: Path):
    """
    Load preprocessed data arrays using NumPy and convert types appropriately.
    Features: np.float32, Target labels: np.int64.
    """
    X_train, y_train, X_val, y_val, X_test, y_test, label_map = load_dataset_metadata(processed_dir)

    X_train = X_train.astype(np.float32)
    X_val = X_val.astype(np.float32)
    X_test = X_test.astype(np.float32)

    y_train = y_train.astype(np.int64)
    y_val = y_val.astype(np.int64)
    y_test = y_test.astype(np.int64)

    return X_train, y_train, X_val, y_val, X_test, y_test, label_map


def load_label_map(processed_dir: Path):
    """Load JSON class mapping dictionary from data/processed/label_map.json."""
    label_map_path = processed_dir / "label_map.json"
    with open(label_map_path, "r", encoding="utf-8") as f:
        label_map = json.load(f)
    return label_map


def validate_training_data(X_train, y_train, X_val, y_val, X_test, y_test, label_map):
    """
    Validate sequence shape consistency, sample counts, and label mapping integrity.
    """
    if X_train.ndim != 3 or X_val.ndim != 3 or X_test.ndim != 3:
        raise ValueError("Input feature arrays must be 3D (samples, sequence_length, feature_dimension).")

    seq_len = X_train.shape[1]
    feat_dim = X_train.shape[2]

    if X_val.shape[1] != seq_len or X_test.shape[1] != seq_len:
        raise ValueError(f"Sequence length mismatch across splits: Train={seq_len}, Val={X_val.shape[1]}, Test={X_test.shape[1]}.")

    if X_val.shape[2] != feat_dim or X_test.shape[2] != feat_dim:
        raise ValueError(f"Feature dimension mismatch across splits: Train={feat_dim}, Val={X_val.shape[2]}, Test={X_test.shape[2]}.")

    if len(y_train) != len(X_train) or len(y_val) != len(X_val) or len(y_test) != len(X_test):
        raise ValueError("Sample count mismatch between feature matrices and target label vectors.")

    num_classes = len(label_map)
    unique_labels = set(label_map.values())

    # Check label integrity in datasets
    for set_name, y_arr in [("train", y_train), ("validation", y_val), ("test", y_test)]:
        for lbl in np.unique(y_arr):
            if int(lbl) not in unique_labels:
                raise ValueError(f"Label '{lbl}' in {set_name} dataset is not present in label_map.json.")

    if num_classes < 2:
        print("\nERROR:")
        print("At least two classes are required for meaningful sign classification.")
        sys.exit(1)

    return seq_len, feat_dim, num_classes


def print_class_distribution(y_train, y_val, y_test, label_map):
    """Display sample counts per class across train, validation, and test splits."""
    inv_label_map = {idx: name for name, idx in label_map.items()}
    print("\nCLASS DISTRIBUTION")
    print("----------------------------------------")

    for idx in sorted(inv_label_map.keys()):
        class_name = inv_label_map[idx]
        train_c = int((y_train == idx).sum())
        val_c = int((y_val == idx).sum())
        test_c = int((y_test == idx).sum())
        print(f"Class {idx} - {class_name}")
        print(f"  Train: {train_c}")
        print(f"  Validation: {val_c}")
        print(f"  Test: {test_c}\n")
    print("----------------------------------------\n")


def build_model(sequence_length: int, feature_dimension: int, num_classes: int) -> tf.keras.Model:
    """Build and compile the authoritative LSTM model architecture from src/model.py."""
    model = build_lstm_model(sequence_length, feature_dimension, num_classes)
    return model


def create_callbacks(best_model_path: Path):
    """
    Create training callbacks:
      1. EarlyStopping: Monitors val_loss with patience=10 and restores best weights.
      2. ModelCheckpoint: Saves best model to models/sign_language_lstm_best.keras based on val_loss.
      3. ReduceLROnPlateau: Reduces learning rate by factor 0.5 when val_loss plateaus.
    """
    best_model_path.parent.mkdir(parents=True, exist_ok=True)

    early_stopping = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=10,
        restore_best_weights=True,
        verbose=1,
    )

    model_checkpoint = tf.keras.callbacks.ModelCheckpoint(
        filepath=str(best_model_path),
        monitor="val_loss",
        save_best_only=True,
        verbose=1,
    )

    reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
        monitor="val_loss",
        factor=0.5,
        patience=5,
        min_lr=1e-6,
        verbose=1,
    )

    return [early_stopping, model_checkpoint, reduce_lr]


def train_model(model: tf.keras.Model, X_train, y_train, X_val, y_val, epochs: int, batch_size: int, callbacks: list):
    """Train the model using model.fit on training data and validation data."""
    history = model.fit(
        X_train,
        y_train,
        validation_data=(X_val, y_val),
        epochs=epochs,
        batch_size=batch_size,
        shuffle=True,
        callbacks=callbacks,
    )
    return history


def save_training_history(history, json_path: Path):
    """Save history metrics (loss, accuracy, val_loss, val_accuracy) to JSON file."""
    json_path.parent.mkdir(parents=True, exist_ok=True)
    history_dict = {}
    for key, val_list in history.history.items():
        history_dict[key] = [float(v) for v in val_list]

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(history_dict, f, indent=4)


def plot_training_history(history, output_path: Path):
    """
    Generate and save training history plots using Matplotlib only (no Seaborn, no subplots, no custom colors).
    Creates two separate plots and saves training_history.png.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    hist = history.history
    epochs_range = range(1, len(hist["loss"]) + 1)

    # 1. Training vs Validation Loss (Separate Plot)
    plt.figure(figsize=(8, 5))
    plt.plot(epochs_range, hist["loss"], label="Training Loss")
    plt.plot(epochs_range, hist["val_loss"], label="Validation Loss")
    plt.title("Training vs Validation Loss")
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    loss_plot_path = output_path.parent / "training_loss.png"
    plt.savefig(loss_plot_path, dpi=300)
    plt.close()

    # 2. Training vs Validation Accuracy (Separate Plot)
    plt.figure(figsize=(8, 5))
    plt.plot(epochs_range, hist["accuracy"], label="Training Accuracy")
    plt.plot(epochs_range, hist["val_accuracy"], label="Validation Accuracy")
    plt.title("Training vs Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    acc_plot_path = output_path.parent / "training_accuracy.png"
    plt.savefig(acc_plot_path, dpi=300)
    plt.close()

    # Main plot file required by spec: data/processed/training_history.png
    # Saved as loss plot (or accuracy plot), maintaining individual separate plot generation
    plt.figure(figsize=(8, 5))
    plt.plot(epochs_range, hist["loss"], label="Training Loss")
    plt.plot(epochs_range, hist["val_loss"], label="Validation Loss")
    plt.plot(epochs_range, hist["accuracy"], label="Training Accuracy")
    plt.plot(epochs_range, hist["val_accuracy"], label="Validation Accuracy")
    plt.title("Training History Metrics")
    plt.xlabel("Epoch")
    plt.ylabel("Metric Value")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


# ==============================================================================
# MAIN TRAINING PIPELINE
# ==============================================================================

def main():
    """Run full LSTM model training workflow."""
    print("========================================")
    print("LSTM TRAINING")
    print("========================================")
    print(f"TensorFlow version: {tf.__version__}\n")

    processed_dir = Path("data/processed")
    models_dir = Path("models")

    best_model_path = models_dir / "sign_language_lstm_best.keras"
    final_model_path = models_dir / "sign_language_lstm_final.keras"
    history_json_path = models_dir / "training_history.json"
    history_plot_path = processed_dir / "training_history.png"

    # 1. Load dataset metadata & arrays
    try:
        X_train, y_train, X_val, y_val, X_test, y_test, label_map = load_data(processed_dir)
    except Exception as exc:
        print(f"CRITICAL ERROR loading dataset files: {exc}")
        sys.exit(1)

    # 2. Validate shapes & dimensions
    try:
        seq_length, feat_dim, num_classes = validate_training_data(
            X_train, y_train, X_val, y_val, X_test, y_test, label_map
        )
    except Exception as exc:
        print(f"CRITICAL ERROR validating training data: {exc}")
        sys.exit(1)

    print(f"Training samples: {len(X_train)}")
    print(f"Validation samples: {len(X_val)}")
    print(f"Testing samples: {len(X_test)}\n")

    print(f"Sequence length: {seq_length}")
    print(f"Feature dimension: {feat_dim}")
    print(f"Classes: {num_classes}\n")

    print("========================================")
    print("TRAINING DATA")
    print("========================================")
    print(f"X_train shape: {X_train.shape}")
    print(f"y_train shape: {y_train.shape}\n")
    print(f"X_val shape: {X_val.shape}")
    print(f"y_val shape: {y_val.shape}\n")
    print(f"X_test shape: {X_test.shape}\n")
    print(f"Number of classes: {num_classes}")
    print("========================================\n")

    # 3. Print Class Distribution
    print_class_distribution(y_train, y_val, y_test, label_map)

    if len(X_train) < BATCH_SIZE:
        effective_batch_size = max(1, len(X_train))
        print(f"[NOTE] Dataset training split has {len(X_train)} samples. Reducing BATCH_SIZE from {BATCH_SIZE} to {effective_batch_size}.\n")
    else:
        effective_batch_size = BATCH_SIZE

    # Small dataset warning check
    if len(X_train) < 20:
        print("WARNING:")
        print("The dataset is small and may result in overfitting.\n")

    # 4. Build & Compile LSTM Model
    print("Building model...\n")
    model = build_model(seq_length, feat_dim, num_classes)

    print("Model summary:")
    model.summary()
    print()

    # 5. Create Callbacks
    callbacks = create_callbacks(best_model_path)

    # 6. Train Model (model.fit)
    print("Starting training...\n")
    history = train_model(
        model,
        X_train,
        y_train,
        X_val,
        y_val,
        epochs=EPOCHS,
        batch_size=effective_batch_size,
        callbacks=callbacks,
    )

    # 7. Save Training History & Plots
    save_training_history(history, history_json_path)
    plot_training_history(history, history_plot_path)

    # 8. Save Final Model
    # EarlyStopping(restore_best_weights=True) restored the weights from the epoch
    # with the lowest validation loss to the model instance. Saving this model creates
    # models/sign_language_lstm_final.keras.
    model.save(final_model_path)

    # 9. Verify Model Files & Run Validation Forward Pass
    if not best_model_path.exists() or not final_model_path.exists():
        raise FileNotFoundError("Model file verification failed after training.")

    loaded_final_model = tf.keras.models.load_model(final_model_path)
    sample_pred = loaded_final_model.predict(X_val[:1], verbose=0)
    print(f"\nValidation sample prediction shape: {sample_pred.shape}")

    # Calculate statistics from training history
    epochs_trained = len(history.history["loss"])
    best_val_loss_idx = int(np.argmin(history.history["val_loss"]))
    best_val_loss = history.history["val_loss"][best_val_loss_idx]
    best_val_acc = history.history["val_accuracy"][best_val_loss_idx] * 100.0

    final_train_loss = history.history["loss"][-1]
    final_train_acc = history.history["accuracy"][-1] * 100.0
    final_val_loss = history.history["val_loss"][-1]
    final_val_acc = history.history["val_accuracy"][-1] * 100.0

    # 10. Print Final Training Summary
    print("\n========================================")
    print("TRAINING COMPLETE")
    print("========================================")
    print(f"Epochs configured: {EPOCHS}")
    print(f"Epochs actually trained: {epochs_trained}\n")
    print(f"Best validation loss: {best_val_loss:.4f}")
    print(f"Best validation accuracy: {best_val_acc:.2f}%\n")
    print(f"Final training loss: {final_train_loss:.4f}")
    print(f"Final training accuracy: {final_train_acc:.2f}%\n")
    print(f"Final validation loss: {final_val_loss:.4f}")
    print(f"Final validation accuracy: {final_val_acc:.2f}%\n")
    print("Best model:")
    print("models/sign_language_lstm_best.keras\n")
    print("Final model:")
    print("models/sign_language_lstm_final.keras\n")
    print("Training history:")
    print("models/training_history.json\n")
    print("Training plots:")
    print("data/processed/training_history.png")
    print("========================================\n")


if __name__ == "__main__":
    main()
