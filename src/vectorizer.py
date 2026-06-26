"""TF-IDF векторизация текста с сохранением/загрузкой."""

import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models")
VECTORIZER_PATH = os.path.join(MODELS_DIR, "tfidf_vectorizer.pkl")


def train_vectorizer(texts, max_features=10000, ngram_range=(1, 2)):
    """Обучает TF-IDF векторизатор и сохраняет его."""
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        sublinear_tf=True,
    )
    X = vectorizer.fit_transform(texts)
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(vectorizer, VECTORIZER_PATH)
    print(f"Векторизатор сохранён: {VECTORIZER_PATH}")
    print(f"Размер словаря: {len(vectorizer.vocabulary_)}")
    return vectorizer, X


def load_vectorizer():
    """Загружает обученный TF-IDF векторизатор."""
    return joblib.load(VECTORIZER_PATH)


def transform(vectorizer, texts):
    """Преобразует тексты в TF-IDF матрицу."""
    return vectorizer.transform(texts)
