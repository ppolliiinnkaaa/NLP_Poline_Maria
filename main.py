"""Точка входа: запуск консольного интерфейса распознавания эмоций."""

import sys
from src.cli import run_cli

if __name__ == "__main__":
    use_bert = "--bert" in sys.argv or "-b" in sys.argv
    run_cli(use_bert=use_bert)
