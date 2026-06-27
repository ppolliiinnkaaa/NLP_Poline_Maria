"""Тесты модуля векторизации."""

import pytest
import os
import tempfile
import shutil
from sklearn.feature_extraction.text import TfidfVectorizer
from src.vectorizer import load_vectorizer, VECTORIZER_PATH


class TestVectorizerTraining:
    """Тесты обучения TF-IDF (без перезаписи рабочего файла)."""

    @pytest.fixture(scope="class")
    def trained(self):
        texts = [
            "привет мир",
            "как дела",
            "радость счастье",
            "грусть печаль",
            "гнев ярость злость",
        ]
        vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
        X = vectorizer.fit_transform(texts)
        return vectorizer, X

    def test_returns_vectorizer_and_matrix(self, trained):
        vectorizer, X = trained
        assert vectorizer is not None
        assert X is not None

    def test_matrix_shape(self, trained):
        _, X = trained
        assert X.shape[0] == 5  # 5 текстов
        assert X.shape[1] <= 100  # max_features

    def test_transform_new_text(self, trained):
        vectorizer, _ = trained
        X_new = vectorizer.transform(["новый текст"])
        assert X_new.shape[0] == 1

    def test_empty_text_transform(self, trained):
        vectorizer, _ = trained
        X = vectorizer.transform([""])
        assert X.shape[0] == 1
        assert X.nnz == 0


class TestVectorizerLoading:
    """Тесты загрузки сохранённого векторизатора (не перезаписывает)."""

    def test_vectorizer_file_exists(self):
        assert os.path.exists(VECTORIZER_PATH), \
            "Файл векторизатора не найден. Сначала обучите модель: python train.py"

    def test_load_vectorizer(self):
        vectorizer = load_vectorizer()
        assert vectorizer is not None

    def test_loaded_transform(self):
        vectorizer = load_vectorizer()
        X = vectorizer.transform(["тестовый текст"])
        assert X.shape[0] == 1
        assert X.shape[1] == 10000  # обученный на полном датасете
