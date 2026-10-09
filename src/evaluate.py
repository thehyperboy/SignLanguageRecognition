"""
Sign Language Recognition - LSTM Model Evaluation Pipeline
-----------------------------------------------------------
Stage: Step 6 - Model Evaluation & Performance Analysis

Loads the best trained model (models/sign_language_lstm_best.keras) and the untouched
test dataset split (data/processed/X_test.npy, y_test.npy, label_map.json). Performs test set
loss and accuracy evaluation, generates predictions, calculates classification metrics
(precision, recall, F1-score), exports numerical and visual confusion matrices, per-class
metrics, prediction level details, and exports summary reports.

Note: Evaluation is strictly read-only. No model training or test data modification occurs.
"""

import json
import os
import sys
from pathlib import Path

# Add project root directory to sys.path to enable direct command execution: python src/evaluate.py
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.metrics import classification_report, confusion_matrix

# ==============================================================================
# HELPER & LOADING FUNCTIONS
# ==============================================================================

def load_model(model_path: Path) -> tf.keras.Model:
    """Load the best trained Keras LSTM model from disk."""
    if not model_path.exists():
        print("\nERROR:")
        print("Trained model not found.")
        print(f"Expected:\n{model_path.as_posix()}\n")
        print("Train the model in STEP 5 before performing evaluation.")
        sys.exit(1)

    try:
        model = tf.keras.models.load_model(model_path)
        return model
    except Exception as exc:
        print(f"\nCRITICAL ERROR loading trained model: {exc}")
        sys.exit(1)


def load_test_data(processed_dir: Path):
    """
    Load unprocessed test arrays (X_test, y_test) and label map from data/processed/.
    Features: np.float32, Target labels: np.int64.
    """
    x_test_path = processed_dir / "X_test.npy"
    y_test_path = processed_dir / "y_test.npy"
    label_map_path = processed_dir / "label_map.json"

    if not x_test_path.exists() or not y_test_path.exists():
        print("\nERROR:")
        print(f"Test dataset files not found in '{processed_dir.as_posix()}'.")
        sys.exit(1)

    if not label_map_path.exists():
        print("\nERROR:")
        print(f"Label map file 'label_map.json' not found in '{processed_dir.as_posix()}'.")
        sys.exit(1)

    try:
        X_test = np.load(x_test_path).astype(np.float32)
        y_test = np.load(y_test_path).astype(np.int64)
        with open(label_map_path, "r", encoding="utf-8") as f:
            label_map = json.load(f)

        return X_test, y_test, label_map
    except Exception as exc:
        print(f"\nCRITICAL ERROR loading test data: {exc}")
        sys.exit(1)


def load_label_map(processed_dir: Path):
    """Load JSON label map dictionary."""
    label_map_path = processed_dir / "label_map.json"
    with open(label_map_path, "r", encoding="utf-8") as f:
        label_map = json.load(f)
    return label_map


def validate_inputs(model: tf.keras.Model, X_test: np.ndarray, y_test: np.ndarray, label_map: dict):
    """
    Validate input feature shapes, sequence lengths, feature dimensions, and class count against model parameters.
    """
    if X_test.ndim != 3:
        print(f"\nERROR: X_test feature matrix must be 3D (samples, sequence_length, feature_dimension). Got ndim={X_test.ndim}.")
        sys.exit(1)

    if len(X_test) != len(y_test):
        print(f"\nERROR: Sample count mismatch between X_test ({len(X_test)}) and y_test ({len(y_test)}).")
        sys.exit(1)

    expected_seq_len = model.input_shape[1]
    expected_feat_dim = model.input_shape[2]
    expected_num_classes = model.output_shape[-1]

    actual_seq_len = X_test.shape[1]
    actual_feat_dim = X_test.shape[2]
    actual_num_classes = len(label_map)

    if actual_seq_len != expected_seq_len:
        print(f"\nERROR: Sequence length mismatch. Model expects {expected_seq_len}, but test dataset has {actual_seq_len}.")
        sys.exit(1)

    if actual_feat_dim != expected_feat_dim:
        print(f"\nERROR: Feature dimension mismatch. Model expects {expected_feat_dim}, but test dataset has {actual_feat_dim}.")
        sys.exit(1)

    if actual_num_classes != expected_num_classes:
        print(f"\nERROR: Class count mismatch. Model outputs {expected_num_classes} classes, but label_map contains {actual_num_classes}.")
        sys.exit(1)


def evaluate_loss_accuracy(model: tf.keras.Model, X_test: np.ndarray, y_test: np.ndarray):
    """Evaluate test loss and test accuracy using model.evaluate()."""
    test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
    return float(test_loss), float(test_acc)


def generate_predictions(model: tf.keras.Model, X_test: np.ndarray):
    """Generate probability predictions and extract argmax class predictions and confidence scores."""
    probabilities = model.predict(X_test, verbose=0)
    predicted_classes = np.argmax(probabilities, axis=1)
    confidences = np.max(probabilities, axis=1)
    return probabilities, predicted_classes, confidences


def calculate_classification_metrics(y_test: np.ndarray, predicted_classes: np.ndarray, label_map: dict):
    """
    Generate classification report string and metrics dictionary using sklearn.metrics.classification_report.
    """
    inv_label_map = {idx: name for name, idx in label_map.items()}
    class_indices = list(range(len(label_map)))
    target_names = [inv_label_map[i] for i in class_indices]

    report_str = classification_report(
        y_test,
        predicted_classes,
        labels=class_indices,
        target_names=target_names,
        zero_division=0,
        digits=4,
    )

    report_dict = classification_report(
        y_test,
        predicted_classes,
        labels=class_indices,
        target_names=target_names,
        zero_division=0,
        output_dict=True,
    )

    return report_str, report_dict


def create_confusion_matrix_data(y_test: np.ndarray, predicted_classes: np.ndarray, label_map: dict):
    """Calculate numerical confusion matrix array."""
    class_indices = list(range(len(label_map)))
    cm = confusion_matrix(y_test, predicted_classes, labels=class_indices)
    return cm


def plot_confusion_matrix(cm: np.ndarray, class_names: list, output_path: Path):
    """
    Plot and save confusion matrix visualization using Matplotlib only (no Seaborn, no custom colors).
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 6))
    plt.imshow(cm, interpolation="nearest")
    plt.title("Sign Language Recognition - Confusion Matrix")
    plt.colorbar()

    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=45)
    plt.yticks(tick_marks, class_names)

    # Annotate matrix cells with numerical values
    thresh = cm.max() / 2.0 if cm.max() > 0 else 1.0
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(
                j, i, str(cm[i, j]),
                horizontalalignment="center",
                color="white" if cm[i, j] > thresh else "black"
            )

    plt.ylabel("True Label")
    plt.xlabel("Predicted Label")
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def plot_class_f1_scores(class_metrics_df: pd.DataFrame, output_path: Path):
    """
    Plot and save per-class F1-score bar chart using Matplotlib only (no Seaborn, no custom colors).
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.figure(figsize=(8, 5))
    plt.bar(class_metrics_df["class"], class_metrics_df["f1_score"])
    plt.title("Per-Class F1-Score Performance")
    plt.xlabel("Sign")
    plt.ylabel("F1-score")
    plt.ylim(0.0, 1.05)
    plt.xticks(rotation=45)
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def save_metrics(
    processed_dir: Path,
    test_samples: int,
    test_loss: float,
    test_acc: float,
    report_dict: dict,
    cm: np.ndarray,
    label_map: dict,
    y_test: np.ndarray,
    predicted_classes: np.ndarray,
    confidences: np.ndarray,
):
    """
    Export evaluation metrics, confusion matrix, predictions, and summary text files.
    """
    inv_label_map = {idx: name for name, idx in label_map.items()}
    class_names = [inv_label_map[i] for i in range(len(label_map))]

    # 1. Save numerical confusion matrix .npy and .csv
    np.save(processed_dir / "confusion_matrix.npy", cm)
    cm_df = pd.DataFrame(cm, index=class_names, columns=class_names)
    cm_df.to_csv(processed_dir / "confusion_matrix.csv", index_label="True Class")

    # 2. Save evaluation_metrics.json
    macro_precision = float(report_dict["macro avg"]["precision"])
    macro_recall = float(report_dict["macro avg"]["recall"])
    macro_f1 = float(report_dict["macro avg"]["f1-score"])

    weighted_precision = float(report_dict["weighted avg"]["precision"])
    weighted_recall = float(report_dict["weighted avg"]["recall"])
    weighted_f1 = float(report_dict["weighted avg"]["f1-score"])

    metrics_json = {
        "test_samples": int(test_samples),
        "test_loss": float(test_loss),
        "test_accuracy": float(test_acc),
        "macro_precision": macro_precision,
        "macro_recall": macro_recall,
        "macro_f1": macro_f1,
        "weighted_precision": weighted_precision,
        "weighted_recall": weighted_recall,
        "weighted_f1": weighted_f1,
    }

    with open(processed_dir / "evaluation_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics_json, f, indent=4)

    # 3. Save class_metrics.csv
    per_class_rows = []
    for idx, name in inv_label_map.items():
        key = name
        if key in report_dict:
            per_class_rows.append({
                "class": name,
                "precision": float(report_dict[key]["precision"]),
                "recall": float(report_dict[key]["recall"]),
                "f1_score": float(report_dict[key]["f1-score"]),
                "support": int(report_dict[key]["support"]),
            })
    class_metrics_df = pd.DataFrame(per_class_rows)
    class_metrics_df.to_csv(processed_dir / "class_metrics.csv", index=False)

    # Plot per-class F1 chart
    plot_class_f1_scores(class_metrics_df, processed_dir / "class_f1_scores.png")

    # 4. Save test_predictions.csv
    pred_rows = []
    for i in range(len(y_test)):
        t_id = int(y_test[i])
        p_id = int(predicted_classes[i])
        pred_rows.append({
            "sample_index": i,
            "true_class_id": t_id,
            "true_sign": inv_label_map.get(t_id, "Unknown"),
            "predicted_class_id": p_id,
            "predicted_sign": inv_label_map.get(p_id, "Unknown"),
            "confidence": float(confidences[i]),
        })
    predictions_df = pd.DataFrame(pred_rows)
    predictions_df.to_csv(processed_dir / "test_predictions.csv", index=False)

    # 5. Save evaluation_summary.txt
    correct_count = int(np.sum(y_test == predicted_classes))
    incorrect_count = int(test_samples - correct_count)
    error_rate = (incorrect_count / test_samples) * 100.0 if test_samples > 0 else 0.0

    summary_text = (
        "========================================\n"
        "SIGN LANGUAGE RECOGNITION\n"
        "MODEL EVALUATION\n"
        "========================================\n\n"
        "Model:\n"
        "models/sign_language_lstm_best.keras\n\n"
        f"Test samples:\n{test_samples}\n\n"
        f"Test loss:\n{test_loss:.4f}\n\n"
        f"Test accuracy:\n{test_acc * 100.0:.2f}%\n\n"
        f"Macro precision:\n{macro_precision * 100.0:.2f}%\n\n"
        f"Macro recall:\n{macro_recall * 100.0:.2f}%\n\n"
        f"Macro F1:\n{macro_f1 * 100.0:.2f}%\n\n"
        f"Weighted precision:\n{weighted_precision * 100.0:.2f}%\n\n"
        f"Weighted recall:\n{weighted_recall * 100.0:.2f}%\n\n"
        f"Weighted F1:\n{weighted_f1 * 100.0:.2f}%\n\n"
        f"Correct predictions:\n{correct_count}\n\n"
        f"Incorrect predictions:\n{incorrect_count}\n\n"
        f"Error rate:\n{error_rate:.2f}%\n"
        "========================================\n"
    )

    with open(processed_dir / "evaluation_summary.txt", "w", encoding="utf-8") as f:
        f.write(summary_text)

    return correct_count, incorrect_count, error_rate, class_names


# ==============================================================================
# MAIN EVALUATION PIPELINE
# ==============================================================================

def main():
    """Run full LSTM model evaluation workflow on test set."""
    print("========================================")
    print("MODEL EVALUATION")
    print("========================================\n")

    models_dir = Path("models")
    processed_dir = Path("data/processed")
    best_model_path = models_dir / "sign_language_lstm_best.keras"
    cm_plot_path = processed_dir / "confusion_matrix.png"

    # 1. Load trained best model
    model = load_model(best_model_path)
    print("Model loaded:")
    print(f"{best_model_path.as_posix()}\n")

    # 2. Load test set & label map
    X_test, y_test, label_map = load_test_data(processed_dir)

    # 3. Validate input shapes
    validate_inputs(model, X_test, y_test, label_map)

    # 4. Evaluate loss and accuracy
    test_loss, test_acc = evaluate_loss_accuracy(model, X_test, y_test)

    print(f"Test samples: {len(X_test)}\n")
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_acc * 100.0:.2f}%\n")

    # 5. Generate predictions
    print("Generating predictions...\n")
    probabilities, predicted_classes, confidences = generate_predictions(model, X_test)

    # 6. Calculate classification metrics
    report_str, report_dict = calculate_classification_metrics(y_test, predicted_classes, label_map)

    print("Classification Report:")
    print(report_str)

    # 7. Calculate & plot confusion matrix
    cm = create_confusion_matrix_data(y_test, predicted_classes, label_map)

    # 8. Save metrics, prediction table, matrices, and summary
    correct_count, incorrect_count, error_rate, class_names = save_metrics(
        processed_dir,
        len(X_test),
        test_loss,
        test_acc,
        report_dict,
        cm,
        label_map,
        y_test,
        predicted_classes,
        confidences,
    )

    plot_confusion_matrix(cm, class_names, cm_plot_path)

    # 9. Print prediction breakdown & confidence stats
    avg_conf = float(np.mean(confidences)) * 100.0
    min_conf = float(np.min(confidences)) * 100.0
    max_conf = float(np.max(confidences)) * 100.0

    print("========================================")
    print("PREDICTION ANALYSIS")
    print("========================================")
    print(f"Correct predictions: {correct_count}")
    print(f"Incorrect predictions: {incorrect_count}")
    print(f"Test Error Rate: {error_rate:.2f}%\n")
    print(f"Average prediction confidence: {avg_conf:.2f}%")
    print(f"Minimum prediction confidence: {min_conf:.2f}%")
    print(f"Maximum prediction confidence: {max_conf:.2f}%")
    print("========================================\n")

    print(f"Confusion matrix saved:\n{cm_plot_path.as_posix()}\n")
    print(f"Metrics saved:\n{(processed_dir / 'evaluation_metrics.json').as_posix()}\n")
    print(f"Predictions saved:\n{(processed_dir / 'test_predictions.csv').as_posix()}\n")

    print("========================================")
    print("EVALUATION COMPLETE")
    print("========================================\n")


if __name__ == "__main__":
    main()
