"""Скрипт обучения BERT модели для классификации эмоций."""

import sys
import numpy as np
import torch
from torch.utils.data import DataLoader
from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_score, recall_score, confusion_matrix

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from src.data_loader import load_data, EMOTION_COLUMNS, EMOTION_RU
from src.bert_model import (
    train_bert, load_bert, EmotionDataset,
    BERT_MODEL_NAME, BERT_DIR, MODELS_DIR, MAX_LENGTH,
)

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)


def full_evaluation(model, tokenizer, df_test, device):
    """Полная оценка модели на тестовой выборке."""
    from transformers import AutoTokenizer

    test_ds = EmotionDataset(
        df_test["text"].tolist(),
        df_test[EMOTION_COLUMNS].values.astype(int),
        tokenizer,
    )
    test_loader = DataLoader(test_ds, batch_size=32)

    model.eval()
    all_preds, all_labels, all_probas = [], [], []
    with torch.no_grad():
        for batch in test_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"]

            logits = model(input_ids, attention_mask)
            probas = torch.sigmoid(logits).cpu().numpy()
            preds = (probas > 0.5).astype(int)

            all_preds.append(preds)
            all_labels.append(labels.numpy().astype(int))
            all_probas.append(probas)

    all_preds = np.vstack(all_preds)
    all_labels = np.vstack(all_labels)
    all_probas = np.vstack(all_probas)

    # Multi-label метрики
    labels_ru = [EMOTION_RU[c] for c in EMOTION_COLUMNS]
    print("\n=== Метрики multi-label классификации (BERT) ===")
    print(f"Accuracy (subset):  {accuracy_score(all_labels, all_preds):.4f}")
    print(f"Precision (macro):  {precision_score(all_labels, all_preds, average='macro', zero_division=0):.4f}")
    print(f"Recall (macro):     {recall_score(all_labels, all_preds, average='macro', zero_division=0):.4f}")
    print(f"F1-score (macro):   {f1_score(all_labels, all_preds, average='macro', zero_division=0):.4f}")
    print(f"F1-score (weighted):{f1_score(all_labels, all_preds, average='weighted', zero_division=0):.4f}")

    print("\n=== Отчёт по каждой эмоции ===")
    print(classification_report(all_labels, all_preds, target_names=labels_ru, zero_division=0))

    # Top-1 метрики
    pred_top1 = np.argmax(all_probas, axis=1)
    true_top1 = np.argmax(all_labels, axis=1)

    top1_acc = accuracy_score(true_top1, pred_top1)
    top1_f1 = f1_score(true_top1, pred_top1, average="macro", zero_division=0)
    # Hit Rate
    from src.evaluate import compute_hit_rate
    hit_rate = compute_hit_rate(all_labels, all_probas)

    print(f"\n=== Top-1 метрики ===")
    print(f"Top-1 Accuracy: {top1_acc:.4f}")
    print(f"Top-1 F1 (macro): {top1_f1:.4f}")
    print(f"Top-1 Hit Rate:   {hit_rate:.4f} (предсказание попадает в любую из истинных меток)")

    # Confusion Matrix
    cm = confusion_matrix(true_top1, pred_top1, labels=range(len(EMOTION_COLUMNS)))
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=labels_ru, yticklabels=labels_ru, ax=ax,
    )
    ax.set_xlabel("Предсказано")
    ax.set_ylabel("Истинное значение")
    ax.set_title("Confusion Matrix — BERT (top-1 эмоция)")
    plt.tight_layout()
    import os
    path = os.path.join(MODELS_DIR, "confusion_matrix_bert.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"\nConfusion Matrix сохранена: {path}")


def main():
    epochs = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print(f"=== Обучение BERT ({BERT_MODEL_NAME}), epochs={epochs} ===\n")

    # Загрузка данных
    print("Загрузка данных...")
    df_train = load_data("train")
    df_val = load_data("validation")
    df_test = load_data("test")
    print(f"  Train: {len(df_train)}, Val: {len(df_val)}, Test: {len(df_test)}")

    # Обучение
    model, tokenizer = train_bert(df_train, df_val, epochs=epochs)

    # Загружаем лучшую модель
    print("\nЗагрузка лучшей модели для оценки...")
    model, tokenizer, device = load_bert()

    # Полная оценка на тесте
    full_evaluation(model, tokenizer, df_test, device)

    print("\nГотово!")


if __name__ == "__main__":
    main()
