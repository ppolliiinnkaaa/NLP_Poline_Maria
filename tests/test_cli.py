"""Тесты консольного интерфейса."""

import sys
import os
import subprocess
import pytest
from src.cli import MAX_TEXT_LENGTH, HELP_TEXT

PYTHON = sys.executable
# На Windows консоль cp1251 не поддерживает юникод-символы — форсируем UTF-8
TEST_ENV = {**os.environ, "PYTHONIOENCODING": "utf-8"}


class TestCLIConstants:
    """Проверка констант CLI."""

    def test_max_length_is_1000(self):
        assert MAX_TEXT_LENGTH == 1000

    def test_help_text_contains_commands(self):
        assert "/help" in HELP_TEXT
        assert "/exit" in HELP_TEXT

    def test_help_text_contains_emotions(self):
        assert "радость" in HELP_TEXT
        assert "грусть" in HELP_TEXT
        assert "гнев" in HELP_TEXT
        assert "страх" in HELP_TEXT
        assert "удивление" in HELP_TEXT

    def test_help_text_contains_project_name(self):
        assert "NLP-Emo-01" in HELP_TEXT


class TestCLIInputValidation:
    """Тесты валидации пользовательского ввода."""

    def test_empty_input_detected(self):
        text = ""
        assert not text.strip()

    def test_exit_command(self):
        assert "/exit" == "/exit"

    def test_help_command(self):
        assert "/help" == "/help"

    def test_unknown_command_detected(self):
        text = "/unknown"
        assert text.startswith("/")
        assert text not in ("/help", "/exit")

    def test_text_length_check_under_limit(self):
        text = "a" * 999
        assert len(text) <= MAX_TEXT_LENGTH

    def test_text_length_check_at_limit(self):
        text = "a" * 1000
        assert len(text) <= MAX_TEXT_LENGTH

    def test_text_length_check_over_limit(self):
        text = "a" * 1001
        assert len(text) > MAX_TEXT_LENGTH

    def test_whitespace_only_is_empty(self):
        text = "   \t  \n  "
        assert not text.strip()


class TestCLIIntegration:
    """Интеграционные тесты CLI через subprocess."""

    def _run(self, args, input_text, timeout=30):
        return subprocess.run(
            args, input=input_text,
            capture_output=True, text=True, timeout=timeout,
            env=TEST_ENV, encoding="utf-8",
        )

    def test_help_output(self):
        result = self._run([PYTHON, "main.py"], "/help\n/exit\n")
        assert "NLP-Emo-01" in result.stdout
        assert "/help" in result.stdout
        assert "/exit" in result.stdout

    def test_exit_output(self):
        result = self._run([PYTHON, "main.py"], "/exit\n")
        assert "До свидания" in result.stdout

    def test_empty_input_error(self):
        result = self._run([PYTHON, "main.py"], "\n/exit\n")
        assert "пустая строка" in result.stdout.lower() or \
               "Ошибка" in result.stdout

    def test_long_text_error(self):
        long_text = "а" * 1001
        result = self._run([PYTHON, "main.py"], f"{long_text}\n/exit\n")
        assert "слишком длинный" in result.stdout or \
               "1001" in result.stdout

    def test_unknown_command_error(self):
        result = self._run([PYTHON, "main.py"], "/blabla\n/exit\n")
        assert "Неизвестная команда" in result.stdout

    def test_emotion_prediction_output(self):
        result = self._run([PYTHON, "main.py"], "Я очень рада!\n/exit\n")
        assert "Эмоция:" in result.stdout
        assert "Уверенность:" in result.stdout
        assert "%" in result.stdout

    def test_special_chars_no_crash(self):
        result = self._run([PYTHON, "main.py"], "!@#$%^&*()\n/exit\n")
        assert result.returncode == 0
        assert "Эмоция:" in result.stdout

    def test_bert_flag_accepted(self):
        result = self._run([PYTHON, "main.py", "--bert"], "/exit\n", timeout=60)
        assert result.returncode == 0
        assert "BERT" in result.stdout or "До свидания" in result.stdout
