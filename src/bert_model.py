"""Fine-tuning rubert-tiny2 для multi-label классификации эмоций."""

import os
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer, AutoModel, get_linear_schedule_with_warmup

from src.data_loader import EMOTION_COLUMNS, EMOTION_RU

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
BERT_DIR = os.path.join(MODELS_DIR, "bert")
BERT_MODEL_NAME = "cointegrated/rubert-tiny2"

NUM_LABELS = len(EMOTION_COLUMNS)
MAX_LENGTH = 128
RANDOM_SEED = 42


# --- Dataset ---

class EmotionDataset(Dataset):
    """PyTorch Dataset для multi-label эмоций."""

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
            "labels": torch.tensor(self.labels[idx], dtype=torch.float),
        }


# --- Model ---

class EmotionClassifier(nn.Module):
    """BERT encoder + linear head для multi-label классификации."""

    def __init__(self, model_name=BERT_MODEL_NAME, num_labels=NUM_LABELS):
        super().__init__()
        self.bert = AutoModel.from_pretrained(model_name)
        self.dropout = nn.Dropout(0.3)
        self.classifier = nn.Linear(self.bert.config.hidden_size, num_labels)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
        pooled = outputs.last_hidden_state[:, 0, :]  # [CLS] token
        pooled = self.dropout(pooled)
        logits = self.classifier(pooled)
        return logits


# --- Training ---

def train_bert(
    df_train, df_val,
    epochs=5, batch_size=32, lr=2e-5, device=None,
):
    """Дообучает rubert-tiny2 на данных эмоций. Возвращает модель и токенизатор."""
    if device is None:
        if torch.backends.mps.is_available():
            device = torch.device("mps")
        elif torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")
    print(f"Устройство: {device}")

    # Токенизатор
    tokenizer = AutoTokenizer.from_pretrained(BERT_MODEL_NAME)

    # Датасеты
    train_ds = EmotionDataset(
        df_train["text"].tolist(),
        df_train[EMOTION_COLUMNS].values.astype(int),
        tokenizer,
    )
    val_ds = EmotionDataset(
        df_val["text"].tolist(),
        df_val[EMOTION_COLUMNS].values.astype(int),
        tokenizer,
    )
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=batch_size)

    # Модель
    model = EmotionClassifier().to(device)
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr, weight_decay=0.01)

    total_steps = len(train_loader) * epochs
    scheduler = get_linear_schedule_with_warmup(
        optimizer,
        num_warmup_steps=int(total_steps * 0.1),
        num_training_steps=total_steps,
    )

    # Обучение
    best_val_f1 = 0
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        for batch in train_loader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"].to(device)

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
        val_f1 = evaluate_bert(model, val_loader, device)
        print(f"Epoch {epoch+1}/{epochs} | Loss: {avg_loss:.4f} | Val F1 (macro): {val_f1:.4f}")

        if val_f1 > best_val_f1:
            best_val_f1 = val_f1
            save_bert(model, tokenizer)
            print(f"  → Лучшая модель сохранена (F1={val_f1:.4f})")

    print(f"\nЛучший Val F1 (macro): {best_val_f1:.4f}")
    return model, tokenizer


def evaluate_bert(model, dataloader, device):
    """Считает macro F1 на валидации."""
    from sklearn.metrics import f1_score
    model.eval()
    all_preds, all_labels = [], []
    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = batch["labels"]

            logits = model(input_ids, attention_mask)
            preds = (torch.sigmoid(logits).cpu().numpy() > 0.5).astype(int)
            all_preds.append(preds)
            all_labels.append(labels.numpy().astype(int))

    all_preds = np.vstack(all_preds)
    all_labels = np.vstack(all_labels)
    return f1_score(all_labels, all_preds, average="macro", zero_division=0)


# --- Save / Load ---

def save_bert(model, tokenizer):
    """Сохраняет модель и токенизатор."""
    os.makedirs(BERT_DIR, exist_ok=True)
    torch.save(model.state_dict(), os.path.join(BERT_DIR, "model.pt"))
    tokenizer.save_pretrained(BERT_DIR)
    print(f"BERT модель сохранена: {BERT_DIR}")


def load_bert(device=None):
    """Загружает модель и токенизатор."""
    if device is None:
        if torch.backends.mps.is_available():
            device = torch.device("mps")
        elif torch.cuda.is_available():
            device = torch.device("cuda")
        else:
            device = torch.device("cpu")

    tokenizer = AutoTokenizer.from_pretrained(BERT_DIR)
    model = EmotionClassifier()
    model.load_state_dict(torch.load(os.path.join(BERT_DIR, "model.pt"), map_location=device))
    model.to(device)
    model.eval()
    return model, tokenizer, device


# --- Inference ---

def predict_single_bert(model, tokenizer, device, text):
    """Предсказание для одного текста. Возвращает (emotion_ru, confidence%)."""
    encoding = tokenizer(
        text,
        max_length=MAX_LENGTH,
        padding="max_length",
        truncation=True,
        return_tensors="pt",
    )
    input_ids = encoding["input_ids"].to(device)
    attention_mask = encoding["attention_mask"].to(device)

    model.eval()
    with torch.no_grad():
        logits = model(input_ids, attention_mask)
        probas = torch.sigmoid(logits).cpu().numpy()[0]

    top_idx = np.argmax(probas)
    emotion_en = EMOTION_COLUMNS[top_idx]
    emotion_ru = EMOTION_RU[emotion_en]
    confidence = round(float(probas[top_idx]) * 100, 1)
    return emotion_ru, confidence
