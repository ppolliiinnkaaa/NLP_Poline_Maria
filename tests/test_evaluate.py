"""Тесты модуля оценки качества."""

import pytest
import numpy as np
from src.evaluate import evaluate_multilabel, evaluate_top1, compute_hit_rate
from src.data_loader import EMOTION_COLUMNS


class TestComputeHitRate:
    """Тесты Hit Rate."""

    def test_perfect_predictions(self):
        y_true = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        probas = np.array([[0.9, 0.05, 0.05], [0.1, 0.8, 0.1], [0.1, 0.1, 0.8]])
        hr = compute_hit_rate(y_true, probas)
        assert hr == 1.0

    def test_all_wrong(self):
        y_true = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        probas = np.array([[0.1, 0.1, 0.9], [0.9, 0.05, 0.05], [0.8, 0.1, 0.1]])
        hr = compute_hit_rate(y_true, probas)
        assert hr == 0.0

    def test_multi_label_hit(self):
        """Если текст имеет несколько меток, попадание в любую — хит."""
        y_true = np.array([[1, 1, 0]])  # две метки
        probas = np.array([[0.3, 0.9, 0.1]])  # предсказана вторая
        hr = compute_hit_rate(y_true, probas)
        assert hr == 1.0

    def test_returns_float(self):
        y_true = np.array([[1, 0]])
        probas = np.array([[0.8, 0.2]])
        hr = compute_hit_rate(y_true, probas)
        assert isinstance(hr, float)

    def test_hit_rate_range(self):
        y_true = np.random.randint(0, 2, size=(100, 10))
        probas = np.random.rand(100, 10)
        hr = compute_hit_rate(y_true, probas)
        assert 0.0 <= hr <= 1.0


class TestMetricsOutput:
    """Тесты что метрики считаются без ошибок."""

    def test_evaluate_multilabel_no_error(self, capsys):
        y_true = np.random.randint(0, 2, size=(50, len(EMOTION_COLUMNS)))
        y_pred = np.random.randint(0, 2, size=(50, len(EMOTION_COLUMNS)))
        evaluate_multilabel(y_true, y_pred)
        captured = capsys.readouterr()
        assert "Accuracy" in captured.out
        assert "Precision" in captured.out
        assert "Recall" in captured.out
        assert "F1-score" in captured.out

    def test_evaluate_multilabel_perfect(self, capsys):
        y = np.eye(len(EMOTION_COLUMNS), dtype=int)
        evaluate_multilabel(y, y)
        captured = capsys.readouterr()
        assert "1.0000" in captured.out  # perfect accuracy
