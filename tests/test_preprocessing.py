"""Тесты модуля предобработки текста."""

import pytest
from src.preprocessing import preprocess


class TestPreprocessBasic:
    """Базовая функциональность предобработки."""

    def test_lowercase(self):
        result = preprocess("ПРИВЕТ МИР")
        assert result == result.lower()

    def test_punctuation_removed(self):
        result = preprocess("Привет! Как дела???")
        assert "!" not in result
        assert "?" not in result

    def test_stopwords_removed(self):
        result = preprocess("я в на и с от")
        # после удаления стоп-слов должно быть пусто или почти пусто
        assert len(result.strip()) == 0 or all(
            w not in result.split() for w in ["я", "в", "на", "и", "с", "от"]
        )

    def test_lemmatization(self):
        result = preprocess("бесит")
        assert "бесить" in result

    def test_lemmatization_plural(self):
        result = preprocess("красивые цветы")
        assert "красивый" in result
        assert "цветок" in result


class TestPreprocessEdgeCases:
    """Крайние случаи предобработки."""

    def test_empty_string(self):
        result = preprocess("")
        assert result == ""

    def test_only_spaces(self):
        result = preprocess("     ")
        assert result.strip() == ""

    def test_only_punctuation(self):
        result = preprocess("!@#$%^&*().,;:")
        assert result.strip() == ""

    def test_only_numbers(self):
        result = preprocess("12345 67890")
        # числа не удаляются regex-ом, но и не ломают обработку
        assert isinstance(result, str)

    def test_mixed_cyrillic_latin(self):
        result = preprocess("Hello Привет world мир")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_emoji_and_special(self):
        """Спецсимволы и эмодзи не должны ломать обработку."""
        result = preprocess("🎉🎊 Ура!!! 🥳")
        assert isinstance(result, str)

    def test_very_long_text(self):
        """Длинный текст обрабатывается без ошибок."""
        long_text = "слово " * 5000
        result = preprocess(long_text)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_newlines_and_tabs(self):
        result = preprocess("привет\nмир\tземля")
        assert "\n" not in result
        assert "\t" not in result

    def test_multiple_spaces_collapsed(self):
        result = preprocess("привет    мир")
        assert "  " not in result

    def test_unicode_cyrillic(self):
        """Корректная обработка кириллицы в UTF-8."""
        result = preprocess("Ёжик в тумане")
        assert isinstance(result, str)
        assert len(result) > 0

    def test_returns_string(self):
        assert isinstance(preprocess("любой текст"), str)
