"""Обучение BERT на single-label версии датасета для сравнения с multi-label."""

import sys
import os
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModel, get_linear_schedule_with_warmup
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

from src.data_loader import load_data, EMOTION_COLUMNS, EMOTION_RU

BERT_MODEL_NAME = "cointegrated/rubert-tiny2"
MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")
BERT_SL_DIR = os.path.join(MODELS_DIR, "bert_single_label")
MAX_LENGTH = 128
RANDOM_SEED = 42

np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)


# --- Конвертация в single-label ---

def to_single_label(df):
    """Конвертирует multi-label датасет в single-label.

    Стратегия: для каждого текста берём первую (левую) эмоцию с меткой 1.
    Если все метки 0 — присваиваем 'neutral'.
    """
    labels = df[EMOTION_COLUMNS].values.astype(int)
    single_labels = []
    for row in labels:
        active = np.where(row == 1)[0]
        if len(active) == 0:
            single_labels.append(0)  # neutral
        else:
            single_labels.append(active[0])
    return np.array(single_labels)


# --- Dataset ---

class SingleLabelDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length=MAX_LENGTH):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        encoding = self.tokenizer(
            self.texts[idx],
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "label": torch.tensor(self.labels[idx], dtype=torch.long),
        }


# --- Model ---

class SingleLabelClassifier(nn.Module):
    def __init__(self, model_name=BERT_MODEL_NAME, num_labels=len(EMOTION_COLUMNS)):
        super().__init__()
        self.bert = AutoModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_labels)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled = outputs.last_hidden_state[:, 0, :]
        pooled = self.dropout(pooled)
        logits = self.classifier(pooled)
        return logits


# --- Training ---

def train(df_train, df_val, epochs=10, batch_size=32, lr=2e-5, device=None):
    if device is None:
        if torch.backends.mps.is_available():
            device = torch.device("mps")
        elif torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")
    print(f"Устройство: {device}")

    tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL_NAME)

    y_train = to_single_label(df_train)
    y_val = to_single_label(df_val)

    # Статистика
    print("\nРаспределение single-label (train):")
    for i, col in enumerate(EMOTION_COLUMNS):
        cnt = (y_train == i).sum()
        print(f"  {EMOTION_RU[col]:20s}: {cnt:5d} ({cnt/len(y_train)*100:.1f}%)")

    train_ds = SingleLabelDataset(df_train["text"].tolist(), y_train, tokenizer)
    val_ds = SingleLabelDataset(df_val["text"].tolist(), y_val, tokenizer)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size)

    model = SingleLabelClassifier().to(device)
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)
    total_steps = len(train_loader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=int(total_steps * 0.1), num_training_steps=total_steps,
    )

    best_val_acc = 0
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for batch in train_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["label"].to(device)

            optimizer.zero_grad()
            logits = model(input_ids, attention_mask)
            loss = criterion(logits, labels)
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()
            scheduler.step()
            total_loss += loss.item()

        avg_loss = total_loss / len(train_loader)

        # Валидация
        model.eval()
        all_preds, all_true = [], []
        with torch.no_grad():
            for batch in val_loader:
                logits = model(batch["input_ids"].to(device), batch["attention_mask"].to(device))
                preds = torch.argmax(logits, dim=1).cpu().numpy()
                all_preds.extend(preds)
                all_true.extend(batch["label"].numpy())

        val_acc = accuracy_score(all_true, all_preds)
        val_f1 = f1_score(all_true, all_preds, average="macro", zero_division=0)
        print(f"Epoch {epoch+1}/{epochs} | Loss: {avg_loss:.4f} | Val Acc: {val_acc:.4f} | Val F1: {val_f1:.4f}")

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            os.makedirs(BERT_SL_DIR, exist_ok=True)
            torch.save(model.state_dict(), os.path.join(BERT_SL_DIR, "model.pt"))
            tokenizer.save_pretrained(BERT_SL_DIR)
            print(f"  → Лучшая модель сохранена (Acc={val_acc:.4f})")

    print(f"\nЛучший Val Accuracy: {best_val_acc:.4f}")
    return model, tokenizer


def evaluate_on_test(df_test, device=None):
    if device is None:
        if torch.backends.mps.is_available():
            device = torch.device("mps")
        elif torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")

    tokenizer = AutoTokenizer.from_pretrained(BERT_SL_DIR)
    model = SingleLabelClassifier()
    model.load_state_dict(torch.load(os.path.join(BERT_SL_DIR, "model.pt"), map_location=device))
    model.to(device)
    model.eval()

    y_test = to_single_label(df_test)
    test_ds = SingleLabelDataset(df_test["text"].tolist(), y_test, tokenizer)
    test_loader = DataLoader(test_ds, batch_size=32)

    all_preds, all_true = [], []
    with torch.no_grad():
        for batch in test_loader:
            logits = model(batch["input_ids"].to(device), batch["attention_mask"].to(device))
            preds = torch.argmax(logits, dim=1).cpu().numpy()
            all_preds.extend(preds)
            all_true.extend(batch["label"].numpy())

    all_preds = np.array(all_preds)
    all_true = np.array(all_true)

    labels_ru = [EMOTION_RU[c] for c in EMOTION_COLUMNS]

    print(f"\n=== Метрики single-label BERT ===")
    print(f"Accuracy:            {accuracy_score(all_true, all_preds):.4f}")
    print(f"Precision (macro):   {precision_score(all_true, all_preds, average='macro', zero_division=0):.4f}")
    print(f"Recall (macro):      {recall_score(all_true, all_preds, average='macro', zero_division=0):.4f}")
    print(f"F1-score (macro):    {f1_score(all_true, all_preds, average='macro', zero_division=0):.4f}")
    print(f"F1-score (weighted): {f1_score(all_true, all_preds, average='weighted', zero_division=0):.4f}")

    print("\n=== Отчёт по каждой эмоции ===")
    present_labels = sorted(set(all_true) | set(all_preds))
    present_names = [labels_ru[i] for i in present_labels]
    print(classification_report(all_true, all_preds, labels=present_labels, target_names=present_names, zero_division=0))

    # Confusion Matrix
    cm = confusion_matrix(all_true, all_preds, labels=range(len(EMOTION_COLUMNS)))
    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues",
        xticklabels=labels_ru, yticklabels=labels_ru, ax=ax,
    )
    ax.set_xlabel("Предсказано")
    ax.set_ylabel("Истинное значение")
    ax.set_title("Confusion Matrix — BERT single-label")
    plt.tight_layout()
    path = os.path.join(MODELS_DIR, "confusion_matrix_bert_single.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    print(f"\nConfusion Matrix сохранена: {path}")


def main():
    epochs = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    print(f"=== Обучение BERT single-label, epochs={epochs} ===\n")

    df_train = load_data("train")
    df_val = load_data("validation")
    df_test = load_data("test")
    print(f"Train: {len(df_train)}, Val: {len(df_val)}, Test: {len(df_test)}")

    train(df_train, df_val, epochs=epochs)
    evaluate_on_test(df_test)
    print("\nГотово!")


if __name__ == "__main__":
    main()
