"""Загрузка и разведка датасета ru-izard-emotions."""

import os
import pandas as pd
from sklearn.model_selection import train_test_split
from datasets import load_dataset

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

RANDOM_SEED = 42

EMOTION_COLUMNS = [
    "neutral", "joy", "sadness", "anger", "enthusiasm",
    "surprise", "disgust", "fear", "guilt", "shame",
]

EMOTION_RU = {
    "neutral": "нейтральность",
    "joy": "радость",
    "sadness": "грусть",
    "anger": "гнев",
    "enthusiasm": "воодушевление",
    "surprise": "удивление",
    "disgust": "отвращение",
    "fear": "страх",
    "guilt": "вина",
    "shame": "стыд",
}


def load_local_csv(path):
    """Загружает датасет из локального CSV файла (UTF-8)."""
    return pd.read_csv(path, encoding="utf-8")


def load_local_json(path):
    """Загружает датасет из локального JSON файла (UTF-8)."""
    return pd.read_json(path, encoding="utf-8")


def load_local_file(path):
    """Загружает датасет из локального файла CSV или JSON."""
    if path.endswith(".csv"):
        return load_local_csv(path)
    elif path.endswith(".json") or path.endswith(".jsonl"):
        return load_local_json(path)
    else:
        raise ValueError(f"Неподдерживаемый формат файла: {path}. "
                         "Используйте CSV или JSON.")


def split_data(df, test_size=0.2, random_state=RANDOM_SEED):
    """Разбивает данные на обучающую и тестовую выборки (80/20) с фиксацией seed."""
    df_train, df_test = train_test_split(
        df, test_size=test_size, random_state=random_state,
    )
    return df_train.reset_index(drop=True), df_test.reset_index(drop=True)


def load_data(split="train", local_path=None):
    """Загружает датасет и возвращает DataFrame с колонками text + emotion labels.

    Если local_path указан — загружает из локального CSV/JSON файла
    и разбивает 80/20 с фиксацией seed.
    Иначе — загружает из Hugging Face (Djacon/ru-izard-emotions).
    """
    if local_path is not None:
        df = load_local_file(local_path)
        df_train, df_test = split_data(df)
        if split == "train":
            return df_train
        elif split in ("test", "validation"):
            return df_test
        else:
            raise ValueError(f"Неизвестный split: {split}")

    ds = load_dataset("Djacon/ru-izard-emotions", split=split)
    df = ds.to_pandas()
    return df


def get_labels_matrix(df):
    """Возвращает матрицу меток (DataFrame) из колонок эмоций."""
    return df[EMOTION_COLUMNS].astype(int)


def print_stats(df, split_name=""):
    """Выводит статистику по датасету."""
    prefix = f"[{split_name}] " if split_name else ""
    print(f"\n{prefix}Размер: {len(df)} текстов")
    print(f"{prefix}Длина текста: min={df['text'].str.len().min()}, "
          f"max={df['text'].str.len().max()}, "
          f"median={df['text'].str.len().median():.0f}")

    print(f"\n{prefix}Распределение эмоций:")
    labels = get_labels_matrix(df)
    counts = labels.sum().sort_values(ascending=False)
    for emo, cnt in counts.items():
        ru = EMOTION_RU[emo]
        pct = cnt / len(df) * 100
        print(f"  {ru:20s} ({emo:12s}): {cnt:5d} ({pct:5.1f}%)")

    multi_label_count = (labels.sum(axis=1) > 1).sum()
    print(f"\n{prefix}Текстов с несколькими эмоциями: {multi_label_count} "
          f"({multi_label_count / len(df) * 100:.1f}%)")

    print(f"\n{prefix}Примеры текстов:")
    for _, row in df.head(5).iterrows():
        active = [EMOTION_RU[c] for c in EMOTION_COLUMNS if row[c] == 1]
        print(f"  [{', '.join(active)}] {row['text'][:100]}")


if __name__ == "__main__":
    for split in ["train", "validation", "test"]:
        df = load_data(split)
        print_stats(df, split)
