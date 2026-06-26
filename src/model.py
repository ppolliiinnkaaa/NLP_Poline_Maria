"""Обучение и инференс multi-label модели классификации эмоций."""

import os
import joblib
import numpy as np
from sklearn.multiclass import OneVsRestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from src.data_loader import EMOTION_COLUMNS, EMOTION_RU

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
MODEL_PATH = os.path.join(MODELS_DIR, "model.pkl")

RANDOM_SEED = 42


def train_model(X_train, y_train, model_type="logreg"):
    """Обучает multi-label модель. Возвращает обученную модель."""
    if model_type == "logreg":
        base = LogisticRegression(max_iter=1000, C=1.0, random_state=RANDOM_SEED)
    elif model_type == "rf":
        base = RandomForestClassifier(n_estimators=200, random_state=RANDOM_SEED, n_jobs=-1)
    else:
        raise ValueError(f"Неизвестный тип модели: {model_type}")

    model = OneVsRestClassifier(base, n_jobs=-1)
    model.fit(X_train, y_train)
    return model


def save_model(model, path=None):
    """Сохраняет модель на диск."""
    path = path or MODEL_PATH
    os.makedirs(os.path.dirname(path), exist_ok=True)
    joblib.dump(model, path)
    print(f"Модель сохранена: {path}")


def load_model(path=None):
    """Загружает модель с диска."""
    path = path or MODEL_PATH
    return joblib.load(path)


def predict_top_emotion(model, X):
    """Предсказывает топ-1 эмоцию и confidence для каждого текста.

    Возвращает списки (emotion_en, emotion_ru, confidence%).
    """
    probas = model.predict_proba(X)

    # OneVsRestClassifier с predict_proba возвращает матрицу [n_samples, n_labels]
    # Каждый столбец — вероятность для одного label
    if isinstance(probas, list):
        # Если вернулся список массивов (для некоторых base estimators)
        probas = np.column_stack([p[:, 1] for p in probas])

    top_indices = np.argmax(probas, axis=1)
    emotions_en = [EMOTION_COLUMNS[i] for i in top_indices]
    emotions_ru = [EMOTION_RU[e] for e in emotions_en]
    confidences = [round(probas[row, idx] * 100, 1) for row, idx in enumerate(top_indices)]

    return emotions_en, emotions_ru, confidences


def predict_single(model, vectorizer, preprocessor, text: str):
    """Предсказание для одного текста. Возвращает (emotion_ru, confidence%)."""
    processed = preprocessor(text)
    X = vectorizer.transform([processed])
    _, emotions_ru, confidences = predict_top_emotion(model, X)
    return emotions_ru[0], confidences[0]
