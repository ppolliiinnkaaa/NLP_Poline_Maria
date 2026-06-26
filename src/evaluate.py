"""Оценка качества модели: метрики и Confusion Matrix."""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix,
)

from src.data_loader import EMOTION_COLUMNS, EMOTION_RU

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")


def evaluate_multilabel(y_true, y_pred):
    """Выводит метрики для multi-label классификации."""
    print("\n=== Метрики multi-label классификации ===")
    print(f"Accuracy (subset):  {accuracy_score(y_true, y_pred):.4f}")
    print(f"Precision (macro):  {precision_score(y_true, y_pred, average='macro', zero_division=0):.4f}")
    print(f"Recall (macro):     {recall_score(y_true, y_pred, average='macro', zero_division=0):.4f}")
    print(f"F1-score (macro):   {f1_score(y_true, y_pred, average='macro', zero_division=0):.4f}")
    print(f"F1-score (weighted):{f1_score(y_true, y_pred, average='weighted', zero_division=0):.4f}")

    labels_ru = [EMOTION_RU[c] for c in EMOTION_COLUMNS]
    print("\n=== Отчёт по каждой эмоции ===")
    print(classification_report(y_true, y_pred, target_names=labels_ru, zero_division=0))


def evaluate_top1(y_true_matrix, model, X):
    """Оценка top-1 предсказаний + Confusion Matrix."""
    probas = model.predict_proba(X)
    if isinstance(probas, list):
        probas = np.column_stack([p[:, 1] for p in probas])

    pred_indices = np.argmax(probas, axis=1)

    # Для true — берём эмоцию с максимальным весом (первую из multi-label)
    true_matrix = np.array(y_true_matrix)
    true_indices = np.argmax(true_matrix, axis=1)

    labels_ru = [EMOTION_RU[c] for c in EMOTION_COLUMNS]

    print("\n=== Метрики top-1 классификации ===")
    print(f"Top-1 Accuracy: {accuracy_score(true_indices, pred_indices):.4f}")
    print(f"Top-1 F1 (macro): {f1_score(true_indices, pred_indices, average='macro', zero_division=0):.4f}")
    print(f"Top-1 F1 (weighted): {f1_score(true_indices, pred_indices, average='weighted', zero_division=0):.4f}")

    cm = confusion_matrix(true_indices, pred_indices, labels=range(len(EMOTION_COLUMNS)))

    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=labels_ru, yticklabels=labels_ru, ax=ax,
    )
    ax.set_xlabel("Предсказано")
    ax.set_ylabel("Истинное значение")
    ax.set_title("Confusion Matrix (top-1 эмоция)")
    plt.tight_layout()

    path = os.path.join(MODELS_DIR, "confusion_matrix.png")
    os.makedirs(MODELS_DIR, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"\nConfusion Matrix сохранена: {path}")


def compute_hit_rate(y_true_matrix, probas):
    """Top-1 Hit Rate: предсказание верно, если попадает в любую из истинных меток.

    Args:
        y_true_matrix: бинарная матрица [n_samples, n_labels]
        probas: вероятности [n_samples, n_labels]
    Returns:
        hit_rate (float)
    """
    true_matrix = np.array(y_true_matrix)
    pred_indices = np.argmax(probas, axis=1)
    hits = 0
    for i, pred_idx in enumerate(pred_indices):
        if true_matrix[i, pred_idx] == 1:
            hits += 1
    hit_rate = hits / len(pred_indices)
    return hit_rate
