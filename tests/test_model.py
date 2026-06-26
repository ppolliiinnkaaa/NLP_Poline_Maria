"""Тесты модуля классической ML-модели."""

import pytest
import numpy as np
from src.model import (
    train_model, save_model, load_model, predict_single,
    predict_top_emotion, RANDOM_SEED, MODEL_PATH,
)
from src.vectorizer import load_vectorizer
from src.preprocessing import preprocess
from src.data_loader import EMOTION_COLUMNS, EMOTION_RU


class TestModelTraining:
    """Тесты обучения модели."""

    @pytest.fixture(scope="class")
    def dummy_data(self):
        np.random.seed(RANDOM_SEED)
        X = np.random.rand(50, 20)
        y = np.random.randint(0, 2, size=(50, len(EMOTION_COLUMNS)))
        return X, y

    def test_train_logreg(self, dummy_data):
        X, y = dummy_data
        model = train_model(X, y, model_type="logreg")
        assert model is not None

    def test_train_rf(self, dummy_data):
        X, y = dummy_data
        model = train_model(X, y, model_type="rf")
        assert model is not None

    def test_train_unknown_type_raises(self, dummy_data):
        X, y = dummy_data
        with pytest.raises(ValueError, match="Неизвестный"):
            train_model(X, y, model_type="unknown")

    def test_predict_returns_correct_shape(self, dummy_data):
        X, y = dummy_data
        model = train_model(X, y, model_type="logreg")
        preds = model.predict(X)
        assert preds.shape == y.shape

    def test_seed_reproducibility(self, dummy_data):
        X, y = dummy_data
        model1 = train_model(X, y, model_type="logreg")
        model2 = train_model(X, y, model_type="logreg")
        preds1 = model1.predict(X)
        preds2 = model2.predict(X)
        np.testing.assert_array_equal(preds1, preds2)


class TestModelInference:
    """Тесты инференса (предсказания)."""

    @pytest.fixture(scope="class")
    def loaded_model(self):
        return load_model()

    @pytest.fixture(scope="class")
    def loaded_vectorizer(self):
        return load_vectorizer()

    def test_predict_single_returns_tuple(self, loaded_model, loaded_vectorizer):
        emo, conf = predict_single(
            loaded_model, loaded_vectorizer, preprocess,
            "Меня это бесит!"
        )
        assert isinstance(emo, str)
        assert isinstance(conf, float)

    def test_confidence_range(self, loaded_model, loaded_vectorizer):
        _, conf = predict_single(
            loaded_model, loaded_vectorizer, preprocess,
            "Я очень рада!"
        )
        assert 0.0 <= conf <= 100.0

    def test_emotion_is_russian(self, loaded_model, loaded_vectorizer):
        emo, _ = predict_single(
            loaded_model, loaded_vectorizer, preprocess,
            "Мне страшно"
        )
        assert emo in EMOTION_RU.values()

    def test_predict_top_emotion_shapes(self, loaded_model, loaded_vectorizer):
        X = loaded_vectorizer.transform(["текст один", "текст два"])
        en, ru, conf = predict_top_emotion(loaded_model, X)
        assert len(en) == 2
        assert len(ru) == 2
        assert len(conf) == 2

    def test_predict_empty_after_preprocess(self, loaded_model, loaded_vectorizer):
        """Текст из одних стоп-слов — не должен упасть."""
        emo, conf = predict_single(
            loaded_model, loaded_vectorizer, preprocess,
            "я в на и с от"
        )
        assert isinstance(emo, str)
        assert 0.0 <= conf <= 100.0

    def test_predict_special_chars(self, loaded_model, loaded_vectorizer):
        """Спецсимволы не ломают предсказание."""
        emo, conf = predict_single(
            loaded_model, loaded_vectorizer, preprocess,
            "!@#$%^&*()"
        )
        assert isinstance(emo, str)
        assert 0.0 <= conf <= 100.0

    def test_anger_detected(self, loaded_model, loaded_vectorizer):
        emo, _ = predict_single(
            loaded_model, loaded_vectorizer, preprocess,
            "Меня это бесит, я в ярости!"
        )
        assert emo == "гнев"

    def test_joy_detected(self, loaded_model, loaded_vectorizer):
        emo, _ = predict_single(
            loaded_model, loaded_vectorizer, preprocess,
            "Какой прекрасный день сегодня!"
        )
        assert emo == "радость"

    def test_sadness_detected(self, loaded_model, loaded_vectorizer):
        emo, _ = predict_single(
            loaded_model, loaded_vectorizer, preprocess,
            "Мне так грустно и одиноко..."
        )
        assert emo == "грусть"

    def test_fear_detected(self, loaded_model, loaded_vectorizer):
        emo, _ = predict_single(
            loaded_model, loaded_vectorizer, preprocess,
            "Я боюсь, что всё пойдёт не так"
        )
        assert emo == "страх"

    def test_surprise_detected(self, loaded_model, loaded_vectorizer):
        emo, _ = predict_single(
            loaded_model, loaded_vectorizer, preprocess,
            "Ого, вот это неожиданность!"
        )
        assert emo == "удивление"
