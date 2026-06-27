"""Тесты модуля загрузки данных."""

import pytest
import pandas as pd
import os
import tempfile

from src.data_loader import (
    load_data, split_data, load_local_file,
    EMOTION_COLUMNS, EMOTION_RU, RANDOM_SEED,
)


class TestLoadData:
    """Загрузка датасета из Hugging Face."""

    @pytest.fixture(scope="class")
    def df_train(self):
        return load_data("train")

    def test_returns_dataframe(self, df_train):
        assert isinstance(df_train, pd.DataFrame)

    def test_has_text_column(self, df_train):
        assert "text" in df_train.columns

    def test_has_emotion_columns(self, df_train):
        for col in EMOTION_COLUMNS:
            assert col in df_train.columns, f"Отсутствует колонка {col}"

    def test_not_empty(self, df_train):
        assert len(df_train) > 0

    def test_text_is_string(self, df_train):
        assert df_train["text"].dtype == object or "string" in str(df_train["text"].dtype).lower()

    def test_labels_are_binary(self, df_train):
        for col in EMOTION_COLUMNS:
            unique_vals = set(df_train[col].unique())
            assert unique_vals.issubset({0, 1}), \
                f"Колонка {col} содержит значения {unique_vals}"


class TestSplitData:
    """Разбиение данных 80/20."""

    @pytest.fixture
    def sample_df(self):
        return pd.DataFrame({
            "text": [f"текст {i}" for i in range(100)],
            "neutral": [1] * 100,
            "joy": [0] * 100,
        })

    def test_split_ratio(self, sample_df):
        train, test = split_data(sample_df)
        assert len(train) == 80
        assert len(test) == 20

    def test_split_reproducible(self, sample_df):
        train1, test1 = split_data(sample_df)
        train2, test2 = split_data(sample_df)
        assert train1["text"].tolist() == train2["text"].tolist()
        assert test1["text"].tolist() == test2["text"].tolist()

    def test_no_overlap(self, sample_df):
        train, test = split_data(sample_df)
        train_texts = set(train["text"])
        test_texts = set(test["text"])
        assert len(train_texts & test_texts) == 0


class TestLoadLocalFile:
    """Загрузка из локального CSV/JSON."""

    def test_load_csv(self):
        with tempfile.NamedTemporaryFile(suffix=".csv", mode="w",
                                         delete=False, encoding="utf-8") as f:
            f.write("text,neutral,joy\n")
            f.write("привет,1,0\n")
            f.write("радость,0,1\n")
            path = f.name
        try:
            df = load_local_file(path)
            assert len(df) == 2
            assert "text" in df.columns
        finally:
            os.unlink(path)

    def test_load_json(self):
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w",
                                         delete=False, encoding="utf-8") as f:
            f.write('[{"text": "привет", "neutral": 1}]')
            path = f.name
        try:
            df = load_local_file(path)
            assert len(df) == 1
        finally:
            os.unlink(path)

    def test_unsupported_format(self):
        with pytest.raises(ValueError, match="Неподдерживаемый"):
            load_local_file("file.xml")


class TestEmotionMapping:
    """Проверка маппинга эмоций."""

    def test_all_emotions_have_russian_name(self):
        for col in EMOTION_COLUMNS:
            assert col in EMOTION_RU, f"Нет русского названия для {col}"

    def test_ten_emotions(self):
        assert len(EMOTION_COLUMNS) == 10

    def test_seed_is_42(self):
        assert RANDOM_SEED == 42
