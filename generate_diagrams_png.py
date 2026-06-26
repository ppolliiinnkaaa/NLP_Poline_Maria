"""Генерация высококачественных диаграмм в PNG (300 DPI) для печати."""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Ellipse
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "diagrams")
os.makedirs(OUT, exist_ok=True)

# Общий стиль
plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.linewidth": 0,
    "figure.facecolor": "white",
})

BLUE = "#1e3c78"
LIGHT_BLUE = "#d0ddf0"
MID_BLUE = "#a0bae0"
ORANGE = "#f5deb3"
DARK_ORANGE = "#c8a050"
GREEN = "#d4f0d4"
DARK_GREEN = "#2a8a2a"
RED_LIGHT = "#fde0e0"
DARK_RED = "#b03030"
GRAY = "#f0f0f0"
DARK_GRAY = "#888888"
WHITE = "#ffffff"


def _box(ax, x, y, w, h, text, fc=LIGHT_BLUE, ec=BLUE, fs=10,
         bold=False, ha="center", va="center", text_color="#1a1a1a"):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                         fc=fc, ec=ec, lw=1.5, zorder=2)
    ax.add_patch(box)
    weight = "bold" if bold else "normal"
    ax.text(x + w/2, y + h/2, text, ha=ha, va=va, fontsize=fs,
            fontweight=weight, color=text_color, zorder=3)


def _arrow(ax, x1, y1, x2, y2, color=BLUE, style="->", lw=1.5):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw),
                zorder=1)


def _line(ax, x1, y1, x2, y2, color=DARK_GRAY, lw=1.2, ls="-"):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, ls=ls, zorder=1)


def _ellipse(ax, cx, cy, w, h, text, fc=LIGHT_BLUE, ec=BLUE, fs=9):
    e = Ellipse((cx, cy), w, h, fc=fc, ec=ec, lw=1.5, zorder=2)
    ax.add_patch(e)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fs, zorder=3)


def _stickman(ax, x, y, scale=1.0):
    """Рисует человечка."""
    s = scale
    head = plt.Circle((x, y + 0.4*s), 0.12*s, fc=WHITE, ec=BLUE, lw=1.8, zorder=3)
    ax.add_patch(head)
    # тело
    ax.plot([x, x], [y + 0.28*s, y - 0.05*s], color=BLUE, lw=1.8, zorder=3)
    # руки
    ax.plot([x - 0.15*s, x + 0.15*s], [y + 0.18*s, y + 0.18*s],
            color=BLUE, lw=1.8, zorder=3)
    # ноги
    ax.plot([x, x - 0.12*s], [y - 0.05*s, y - 0.25*s], color=BLUE, lw=1.8, zorder=3)
    ax.plot([x, x + 0.12*s], [y - 0.05*s, y - 0.25*s], color=BLUE, lw=1.8, zorder=3)


# ================================================================
#                    1. USE CASE DIAGRAM
# ================================================================
def draw_use_case():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(-0.5, 10)
    ax.set_ylim(-0.5, 8)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.suptitle("Диаграмма Use Case — NLP-Emo-01", fontsize=16,
                 fontweight="bold", color=BLUE, y=0.96)

    # Системная рамка
    sys_rect = FancyBboxPatch((2.8, 0.3), 6.5, 7.0,
                               boxstyle="round,pad=0.1",
                               fc="#f8faff", ec=BLUE, lw=2, zorder=0)
    ax.add_patch(sys_rect)
    ax.text(6.05, 7.05, "Система NLP-Emo-01", ha="center", va="bottom",
            fontsize=13, fontweight="bold", color=BLUE)

    # Актёр — Пользователь
    _stickman(ax, 1.2, 4.5, scale=1.8)
    ax.text(1.2, 3.3, "Пользователь", ha="center", fontsize=11,
            fontweight="bold", color=BLUE)

    # Use Cases
    cases = [
        (6.0, 6.2, "Ввести текст\n(до 1000 символов)"),
        (6.0, 5.0, "Получить эмоцию\n+ уверенность (%)"),
        (6.0, 3.8, "Вызвать /help\n(справка)"),
        (6.0, 2.6, "Вызвать /exit\n(выход)"),
        (6.0, 1.4, "Обучить модель\n(train.py / train_bert.py)"),
    ]
    for cx, cy, label in cases:
        _ellipse(ax, cx, cy, 3.8, 0.85, label, fc="#e8f0ff", ec=BLUE, fs=10)
        _line(ax, 1.7, 4.5, cx - 1.9, cy, color=MID_BLUE, lw=1.3)

    # include связь
    ax.annotate("«include»", xy=(6.0, 5.45), xytext=(6.0, 5.75),
                ha="center", fontsize=8, color=DARK_GRAY,
                arrowprops=dict(arrowstyle="->", color=DARK_GRAY,
                                lw=1, ls="--"))

    fig.savefig(os.path.join(OUT, "1_use_case.png"), dpi=300,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  1_use_case.png")


# ================================================================
#                    2. CLASS DIAGRAM
# ================================================================
def draw_class_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 12)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.suptitle("Диаграмма классов — NLP-Emo-01", fontsize=16,
                 fontweight="bold", color=BLUE, y=0.97)

    bw, bh_title, bh_row = 4.2, 0.5, 0.38

    def class_box(x, y, name, attrs, methods, color=LIGHT_BLUE):
        total_h = bh_title + bh_row * (len(attrs) + len(methods))
        # Рамка
        rect = FancyBboxPatch((x, y - total_h), bw, total_h,
                               boxstyle="round,pad=0.02",
                               fc=WHITE, ec=BLUE, lw=1.5, zorder=2)
        ax.add_patch(rect)
        # Заголовок
        head = FancyBboxPatch((x, y - bh_title), bw, bh_title,
                               boxstyle="round,pad=0.02",
                               fc=color, ec=BLUE, lw=1.5, zorder=3)
        ax.add_patch(head)
        ax.text(x + bw/2, y - bh_title/2, name, ha="center", va="center",
                fontsize=10, fontweight="bold", zorder=4)

        # Атрибуты
        cy = y - bh_title
        for attr in attrs:
            cy -= bh_row
            ax.text(x + 0.15, cy + bh_row/2, attr, ha="left", va="center",
                    fontsize=8, color="#333", zorder=4)
        # Линия
        if attrs and methods:
            ax.plot([x, x + bw], [cy, cy], color=BLUE, lw=0.8, zorder=3)
        # Методы
        for meth in methods:
            cy -= bh_row
            ax.text(x + 0.15, cy + bh_row/2, meth, ha="left", va="center",
                    fontsize=8, color="#333", zorder=4)
        return x + bw/2, y - total_h  # bottom center

    # Ряд 1 — Данные и предобработка
    class_box(0.5, 11,
              "data_loader",
              ["EMOTION_COLUMNS: list", "EMOTION_RU: dict", "RANDOM_SEED = 42"],
              ["load_data(split, local_path)", "split_data(df, test_size)",
               "load_local_file(path)", "get_labels_matrix(df)"],
              color="#c8daf8")

    class_box(5.8, 11,
              "preprocessing",
              ["_morph: MorphAnalyzer", "_stopwords: set"],
              ["preprocess(text) -> str"],
              color="#c8daf8")

    class_box(10.8, 11,
              "vectorizer",
              ["VECTORIZER_PATH: str"],
              ["train_vectorizer(texts)", "load_vectorizer()",
               "transform(vectorizer, texts)"],
              color="#c8daf8")

    # Ряд 2 — Модели
    class_box(0.5, 7.5,
              "model",
              ["MODEL_PATH: str", "RANDOM_SEED = 42"],
              ["train_model(X, y, model_type)", "save_model(model)",
               "load_model()", "predict_single(model, vec, prep, text)",
               "predict_top_emotion(model, X)"],
              color="#f5deb3")

    class_box(5.8, 7.5,
              "bert_model",
              ["EmotionClassifier(nn.Module)", "BERT_MODEL_NAME",
               "MAX_LENGTH = 128"],
              ["train_bert(df_train, df_val)", "save_bert(model, tok)",
               "load_bert(device)", "predict_single_bert(m, t, d, text)"],
              color="#f5deb3")

    class_box(10.8, 7.5,
              "evaluate",
              ["MODELS_DIR: str"],
              ["evaluate_multilabel(y_true, y_pred)",
               "evaluate_top1(y_true, model, X)",
               "compute_hit_rate(y_true, probas)"],
              color="#d4f0d4")

    # Ряд 3 — CLI
    class_box(5.8, 4.0,
              "cli",
              ["MAX_TEXT_LENGTH = 1000", "HELP_TEXT: str"],
              ["run_cli(use_bert=False)"],
              color="#fde0e0")

    # Стрелки зависимостей
    _arrow(ax, 7.9, 3.2, 2.6, 5.15, color=MID_BLUE)      # cli -> model
    _arrow(ax, 7.9, 3.2, 7.9, 5.0, color=MID_BLUE)        # cli -> bert_model
    _arrow(ax, 7.9, 3.5, 12.9, 8.8, color=MID_BLUE)       # cli -> vectorizer
    _arrow(ax, 7.9, 3.5, 7.9, 9.1, color=MID_BLUE)        # cli -> preprocessing
    _arrow(ax, 2.6, 7.5, 2.6, 8.3, color=DARK_GRAY)       # model -> data_loader
    _arrow(ax, 7.9, 7.5, 2.6, 8.6, color=DARK_GRAY)       # bert -> data_loader
    _arrow(ax, 2.6, 5.15, 12.9, 5.9, color=DARK_GRAY)     # model -> evaluate
    _arrow(ax, 7.9, 5.0, 12.9, 5.7, color=DARK_GRAY)      # bert -> evaluate

    # Легенда
    ax.text(0.5, 0.8, "Цвета:", fontsize=9, fontweight="bold", color="#555")
    for i, (c, label) in enumerate([
        ("#c8daf8", "Данные и предобработка"),
        ("#f5deb3", "Модели классификации"),
        ("#d4f0d4", "Оценка качества"),
        ("#fde0e0", "Пользовательский интерфейс"),
    ]):
        rect = FancyBboxPatch((2.0 + i*3.3, 0.55), 0.4, 0.35,
                               boxstyle="round,pad=0.02", fc=c, ec=BLUE, lw=1)
        ax.add_patch(rect)
        ax.text(2.5 + i*3.3, 0.72, label, fontsize=8, va="center")

    fig.savefig(os.path.join(OUT, "2_class_diagram.png"), dpi=300,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  2_class_diagram.png")


# ================================================================
#                    3. OBJECT DIAGRAM
# ================================================================
def draw_object_diagram():
    fig, ax = plt.subplots(1, 1, figsize=(14, 9))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 9)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.suptitle("Диаграмма объектов — пример классификации текста",
                 fontsize=15, fontweight="bold", color=BLUE, y=0.97)

    bw = 5.5

    def obj_box(x, y, name, attrs, color=LIGHT_BLUE, ec=BLUE):
        h = 0.45 + 0.35 * len(attrs)
        rect = FancyBboxPatch((x, y), bw, h, boxstyle="round,pad=0.02",
                               fc=WHITE, ec=ec, lw=1.5, zorder=2)
        ax.add_patch(rect)
        head = FancyBboxPatch((x, y + h - 0.45), bw, 0.45,
                               boxstyle="round,pad=0.02",
                               fc=color, ec=ec, lw=1.5, zorder=3)
        ax.add_patch(head)
        ax.text(x + bw/2, y + h - 0.22, name, ha="center", va="center",
                fontsize=10, fontweight="bold", zorder=4,
                style="italic" if ":" in name else "normal")
        for i, attr in enumerate(attrs):
            ax.text(x + 0.2, y + h - 0.45 - 0.35*(i+1) + 0.17,
                    attr, fontsize=9, va="center", zorder=4)
        return x + bw/2, y + h, y  # center_x, top, bottom

    # Входной текст
    cx1, t1, b1 = obj_box(0.5, 7.2, "text : str",
        ['= "Меня это бесит, я в ярости!"'],
        color="#fff8d0", ec="#c8a030")

    # Preprocessed
    cx2, t2, b2 = obj_box(7.8, 7.2, "processed : str",
        ['= "бесить ярость"'],
        color="#fff8d0", ec="#c8a030")

    _arrow(ax, cx1 + bw/2 + 0.1, 7.6, 7.8, 7.6, color="#c8a030")
    ax.text(6.6, 7.75, "preprocess()", fontsize=8, ha="center",
            color=DARK_GRAY, style="italic")

    # Vectorizer
    cx3, t3, b3 = obj_box(0.5, 5.0, "vectorizer : TfidfVectorizer",
        ["max_features = 10000", "ngram_range = (1, 2)",
         "sublinear_tf = True"],
        color=LIGHT_BLUE)

    # X vector
    cx4, t4, b4 = obj_box(7.8, 5.3, "X : sparse matrix",
        ["shape = (1, 10000)", "nnz = 2  (два ненулевых)"],
        color=LIGHT_BLUE)

    _arrow(ax, cx1, b1, cx1, t3, color=BLUE)
    _arrow(ax, cx3 + bw/2 + 0.1, 5.7, 7.8, 5.7, color=BLUE)
    ax.text(6.6, 5.85, "transform()", fontsize=8, ha="center",
            color=DARK_GRAY, style="italic")

    # Model
    cx5, t5, b5 = obj_box(0.5, 2.8, "model : OneVsRestClassifier",
        ["base = LogisticRegression", "n_estimators = 10 (по числу эмоций)",
         "random_state = 42"],
        color="#f5deb3", ec=DARK_ORANGE)

    _arrow(ax, cx3, b3, cx3, t5, color=BLUE)

    # Result
    cx6, t6, b6 = obj_box(7.8, 2.8, "result",
        ['emotion_ru = "гнев"', "confidence = 68.7",
         'emotion_en = "anger"'],
        color=GREEN, ec=DARK_GREEN)

    _arrow(ax, cx5 + bw/2 + 0.1, 3.5, 7.8, 3.5, color=DARK_GREEN)
    ax.text(6.6, 3.65, "predict_proba() → argmax",
            fontsize=8, ha="center", color=DARK_GRAY, style="italic")

    # CLI output
    out_box = FancyBboxPatch((3.5, 0.3), 7.0, 1.8, boxstyle="round,pad=0.05",
                              fc="#f0f8f0", ec=DARK_GREEN, lw=2, zorder=2)
    ax.add_patch(out_box)
    ax.text(7.0, 1.75, "Вывод в консоль:", fontsize=10,
            fontweight="bold", color=DARK_GREEN, ha="center")
    ax.text(7.0, 1.25, "Эмоция: гнев", fontsize=12, ha="center",
            fontfamily="monospace", color="#1a1a1a")
    ax.text(7.0, 0.75, "Уверенность: 68.7%", fontsize=12, ha="center",
            fontfamily="monospace", color="#1a1a1a")

    _arrow(ax, cx6, b6, 7.0, 2.1, color=DARK_GREEN)

    fig.savefig(os.path.join(OUT, "3_object_diagram.png"), dpi=300,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  3_object_diagram.png")


# ================================================================
#                    4. PIPELINE DIAGRAM
# ================================================================
def draw_pipeline():
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.suptitle("Схема пайплайна обработки текста", fontsize=16,
                 fontweight="bold", color=BLUE, y=0.97)

    bw, bh = 5.0, 0.8
    cx = 7.0

    # Входной текст
    _box(ax, cx - bw/2, 9.0, bw, bh, "Текст пользователя",
         fc="#fff5e0", ec="#d0a030", fs=12, bold=True)

    # Стрелка
    _arrow(ax, cx, 9.0, cx, 8.5)

    # Предобработка
    _box(ax, cx - bw/2, 7.6, bw, bh, "Предобработка",
         fc=LIGHT_BLUE, ec=BLUE, fs=12, bold=True)
    # Детали справа
    details = ["1. Lowercase", "2. Удаление пунктуации (regex)",
               "3. Стоп-слова (NLTK)", "4. Лемматизация (pymorphy2)"]
    for i, d in enumerate(details):
        ax.text(cx + bw/2 + 0.3, 8.2 - i*0.3, d, fontsize=9,
                color="#555", va="center")

    _arrow(ax, cx, 7.6, cx, 7.1)

    # Развилка
    ax.text(cx, 6.9, "Выбор метода", ha="center", fontsize=10,
            fontweight="bold", color=BLUE)

    # Левая ветка — TF-IDF
    lx = 3.5
    _line(ax, cx, 6.7, lx, 6.3, color=BLUE, lw=1.5)

    _box(ax, lx - bw/2 + 0.3, 5.5, bw - 0.6, bh, "TF-IDF\nВекторизация",
         fc="#d8e8ff", ec=BLUE, fs=11, bold=True)
    _arrow(ax, lx, 5.5, lx, 4.9)
    ax.text(lx - bw/2 + 0.3 - 0.1, 5.5, "sklearn", fontsize=8,
            color=DARK_GRAY, ha="right")

    _box(ax, lx - bw/2 + 0.3, 4.1, bw - 0.6, bh, "LogReg /\nRandomForest",
         fc="#f5deb3", ec=DARK_ORANGE, fs=11, bold=True)
    _arrow(ax, lx, 4.1, lx, 3.5)
    ax.text(lx - bw/2 + 0.3 - 0.1, 4.1, "sklearn", fontsize=8,
            color=DARK_GRAY, ha="right")

    # Правая ветка — BERT
    rx = 10.5
    _line(ax, cx, 6.7, rx, 6.3, color=BLUE, lw=1.5)

    _box(ax, rx - bw/2 + 0.3, 5.5, bw - 0.6, bh, "BERT Tokenizer\n(rubert-tiny2)",
         fc="#d8e8ff", ec=BLUE, fs=11, bold=True)
    _arrow(ax, rx, 5.5, rx, 4.9)
    ax.text(rx + bw/2 - 0.3 + 0.1, 5.5, "transformers", fontsize=8,
            color=DARK_GRAY, ha="left")

    _box(ax, rx - bw/2 + 0.3, 4.1, bw - 0.6, bh, "BERT Classifier\n(EmotionClassifier)",
         fc="#f5deb3", ec=DARK_ORANGE, fs=11, bold=True)
    _arrow(ax, rx, 4.1, rx, 3.5)
    ax.text(rx + bw/2 - 0.3 + 0.1, 4.1, "PyTorch", fontsize=8,
            color=DARK_GRAY, ha="left")

    # Объединение
    _line(ax, lx, 3.5, rx, 3.5, color=BLUE, lw=1.5)
    _arrow(ax, cx, 3.5, cx, 3.0)

    # Результат
    _box(ax, cx - bw/2 - 0.5, 2.0, bw + 1.0, bh + 0.2,
         "Эмоция + Уверенность (%)",
         fc="#d4f0d4", ec=DARK_GREEN, fs=13, bold=True)

    # Пример внизу
    example_box = FancyBboxPatch((2.5, 0.2), 9.0, 1.3,
                                  boxstyle="round,pad=0.05",
                                  fc="#f8faf8", ec=DARK_GREEN, lw=1.5, zorder=2)
    ax.add_patch(example_box)
    ax.text(7.0, 1.2, "Пример:", fontsize=10, fontweight="bold",
            ha="center", color=DARK_GREEN)
    ax.text(7.0, 0.8, '"Меня это бесит, я в ярости!"  →  гнев, 68.7%',
            fontsize=11, ha="center", fontfamily="monospace")

    fig.savefig(os.path.join(OUT, "4_pipeline.png"), dpi=300,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  4_pipeline.png")


# ================================================================
#                 5. ARCHITECTURE DIAGRAM
# ================================================================
def draw_architecture():
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    ax.set_xlim(0, 15)
    ax.set_ylim(0, 10)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.suptitle("Архитектура проекта — модули и файлы", fontsize=16,
                 fontweight="bold", color=BLUE, y=0.97)

    bw, bh = 3.0, 0.7

    # Уровень 1 — Точки входа
    ax.text(7.5, 9.3, "Точки входа (запуск)", ha="center", fontsize=12,
            fontweight="bold", color=DARK_RED)
    entries = [
        (1.5, "main.py", "Запуск CLI"),
        (4.8, "train.py", "Обучение TF-IDF"),
        (8.1, "train_bert.py", "Обучение BERT"),
        (11.4, "train_bert_single.py", "BERT single-label"),
    ]
    for x, name, desc in entries:
        _box(ax, x, 8.4, bw, bh, name, fc=RED_LIGHT, ec=DARK_RED, fs=10, bold=True)
        ax.text(x + bw/2, 8.35, desc, ha="center", va="top", fontsize=7,
                color=DARK_GRAY)

    # Уровень 2 — Модули src/
    ax.text(7.5, 7.3, "Модули обработки (src/)", ha="center", fontsize=12,
            fontweight="bold", color=BLUE)
    modules = [
        (0.5, "cli.py", "Интерфейс"),
        (3.3, "model.py", "ML-модели"),
        (6.1, "bert_model.py", "BERT"),
        (8.9, "preprocessing.py", "Предобработка"),
        (11.7, "vectorizer.py", "TF-IDF"),
    ]
    for x, name, desc in modules:
        _box(ax, x, 6.4, bw - 0.2, bh, name, fc=LIGHT_BLUE, ec=BLUE, fs=10, bold=True)
        ax.text(x + (bw - 0.2)/2, 6.35, desc, ha="center", va="top",
                fontsize=7, color=DARK_GRAY)

    modules2 = [
        (2.0, "evaluate.py", "Метрики"),
        (5.5, "data_loader.py", "Загрузка данных"),
    ]
    for x, name, desc in modules2:
        _box(ax, x, 5.0, bw, bh, name, fc=LIGHT_BLUE, ec=BLUE, fs=10, bold=True)
        ax.text(x + bw/2, 4.95, desc, ha="center", va="top",
                fontsize=7, color=DARK_GRAY)

    # Стрелки входные точки -> модули
    _arrow(ax, 3.0, 8.4, 1.9, 7.1, color=DARK_GRAY)   # main -> cli
    _arrow(ax, 6.3, 8.4, 4.7, 7.1, color=DARK_GRAY)   # train -> model
    _arrow(ax, 9.6, 8.4, 7.5, 7.1, color=DARK_GRAY)   # train_bert -> bert

    # cli -> model, bert
    _arrow(ax, 1.9, 6.4, 4.3, 7.1, color=MID_BLUE, style="-|>")
    _arrow(ax, 1.9, 6.4, 7.1, 7.1, color=MID_BLUE, style="-|>")

    # Уровень 3 — Данные
    ax.text(7.5, 3.9, "Данные и сохранённые модели", ha="center",
            fontsize=12, fontweight="bold", color=DARK_GREEN)
    data_items = [
        (1.0, "models/\n*.pkl, *.pt", "Обученные модели"),
        (5.0, "data/\nCSV / JSON", "Локальный датасет"),
        (9.0, "Hugging Face\n(remote)", "Облачный датасет"),
        (12.0, "models/\n*.png", "Confusion Matrix"),
    ]
    for x, name, desc in data_items:
        _box(ax, x, 2.5, bw + 0.3, bh + 0.2, name,
             fc=GREEN, ec=DARK_GREEN, fs=9, bold=True)
        ax.text(x + (bw + 0.3)/2, 2.45, desc, ha="center", va="top",
                fontsize=7, color=DARK_GRAY)

    # Стрелки модули -> данные
    _arrow(ax, 4.7, 6.4, 2.5, 3.4, color=DARK_GREEN)  # model -> models/
    _arrow(ax, 7.0, 5.0, 6.5, 3.4, color=DARK_GREEN)  # data_loader -> data/
    _arrow(ax, 7.0, 5.0, 10.5, 3.4, color=DARK_GREEN)  # data_loader -> HF
    _arrow(ax, 3.5, 5.0, 2.5, 3.4, color=DARK_GREEN)  # evaluate -> png

    # Тесты
    ax.text(7.5, 1.5, "Автоматические тесты (pytest)", ha="center",
            fontsize=12, fontweight="bold", color="#8B4513")
    test_items = [
        (1.0, "test_preprocessing", "16 тестов"),
        (4.0, "test_model", "17 тестов"),
        (7.0, "test_cli", "20 тестов"),
        (10.0, "test_evaluate", "7 тестов"),
    ]
    for x, name, desc in test_items:
        _box(ax, x, 0.5, bw + 0.3, 0.55, name,
             fc="#fff0e0", ec="#8B4513", fs=8, bold=True)
        ax.text(x + (bw + 0.3)/2, 0.45, desc, ha="center", va="top",
                fontsize=7, color=DARK_GRAY)

    fig.savefig(os.path.join(OUT, "5_architecture.png"), dpi=300,
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  5_architecture.png")


# ================================================================
if __name__ == "__main__":
    print("Генерация диаграмм (300 DPI)...")
    draw_use_case()
    draw_class_diagram()
    draw_object_diagram()
    draw_pipeline()
    draw_architecture()
    print(f"\nГотово! Файлы в папке: {OUT}/")
