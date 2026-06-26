"""Предобработка текста: lowercase, удаление пунктуации, стоп-слов, лемматизация."""

import re
import nltk
try:
    from pymorphy3 import MorphAnalyzer
except ImportError:
    from pymorphy2 import MorphAnalyzer

nltk.download("stopwords", quiet=True)

_morph = MorphAnalyzer()
_stopwords = set(nltk.corpus.stopwords.words("russian"))


def preprocess(text: str) -> str:
    """Полный пайплайн предобработки текста."""
    text = text.lower()
    text = re.sub(r"[^а-яёa-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    tokens = text.split()
    tokens = [t for t in tokens if t not in _stopwords]
    tokens = [_morph.parse(t)[0].normal_form for t in tokens]
    return " ".join(tokens)


if __name__ == "__main__":
    examples = [
        "Меня это бесит, я в ярости!",
        "Какой прекрасный день сегодня!!!",
        "Мне грустно и одиноко...",
        "",
        "Ты дебил",
    ]
    for ex in examples:
        print(f"  '{ex}' -> '{preprocess(ex)}'")
