"""Тесты модуля векторизации."""

import pytest
import os
from src.vectorizer import train_vectorizer, load_vectorizer, VECTORIZER_PATH


class TestVectorizer:
    """Тесты TF-IDF векторизатора."""

    @pytest.fixture(scope="class")
    def trained(self):
        texts = [
            "привет мир",
            "как дела",
            "радость счастье",
            "грусть печаль",
            "гнев ярость злость",
        ]
        vectorizer, X = train_vectorizer(texts, max_features=100)
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

    def test_vectorizer_saved(self, trained):
        assert os.path.exists(VECTORIZER_PATH)

    def test_load_vectorizer(self):
        vectorizer = load_vectorizer()
        assert vectorizer is not None
        X = vectorizer.transform(["тестовый текст"])
        assert X.shape[0] == 1

    def test_empty_text_transform(self, trained):
        vectorizer, _ = trained
        X = vectorizer.transform([""])
        assert X.shape[0] == 1
        # пустой текст даёт нулевой вектор
        assert X.nnz == 0
