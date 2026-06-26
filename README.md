# NLP-Emo-01: Распознавание эмоций по тексту

Программа для автоматического определения эмоциональной окраски текста на русском языке.

## Распознаваемые эмоции (10 классов)

| Эмоция | English |
|--------|---------|
| Нейтральность | neutral |
| Радость | joy |
| Грусть | sadness |
| Гнев | anger |
| Воодушевление | enthusiasm |
| Удивление | surprise |
| Отвращение | disgust |
| Страх | fear |
| Вина | guilt |
| Стыд | shame |

## Установка

```bash
# Переход в директорию проекта
cd NLP_Emo

# Установка зависимостей
pip install -r requirements.txt
```

**Требования:** Python 3.8+

## Обучение модели

### Вариант 1: TF-IDF + LogisticRegression (baseline)

```bash
python3 train.py
```

### Вариант 2: BERT (rubert-tiny2) — рекомендуется

```bash
python3 train_bert.py
```

Опционально можно указать количество эпох:

```bash
python3 train_bert.py 10
```

### Сравнение моделей

| Метрика | TF-IDF + LogReg | BERT (rubert-tiny2) |
|---------|----------------|---------------------|
| Multi-label F1 (macro) | 0.29 | **0.49** |
| Top-1 Accuracy | 44.6% | **47.1%** |
| Recall (macro) | 0.20 | **0.43** |

## Запуск

```bash
# TF-IDF модель (по умолчанию)
python3 main.py

# BERT модель
python3 main.py --bert
```

### Пример работы

```
Введите текст: Меня это бесит, я в ярости!
  Эмоция: гнев
  Уверенность: 92%

Введите текст: Какой прекрасный день!
  Эмоция: радость
  Уверенность: 78%
```

### Команды

- `/help` — справка по использованию
- `/exit` — выход из программы

## Структура проекта

```
NLP_Emo/
├── src/
│   ├── data_loader.py     # Загрузка датасета
│   ├── preprocessing.py   # Предобработка текста (для TF-IDF)
│   ├── vectorizer.py      # TF-IDF векторизация
│   ├── model.py           # TF-IDF + LogReg модель
│   ├── bert_model.py      # BERT fine-tuning и инференс
│   ├── evaluate.py        # Метрики и Confusion Matrix
│   └── cli.py             # Консольный интерфейс
├── models/                # Сохранённые модели
│   ├── model.pkl          # TF-IDF модель
│   ├── tfidf_vectorizer.pkl
│   └── bert/              # BERT модель
├── train.py               # Обучение TF-IDF модели
├── train_bert.py          # Обучение BERT модели
├── main.py                # Точка входа
├── requirements.txt       # Зависимости
└── README.md
```

## Датасет

[ru-izard-emotions](https://huggingface.co/datasets/Djacon/ru-izard-emotions) — ~25 000 текстов, 10 классов эмоций по модели Изарда. Multi-label разметка.

## Технологии

- Python 3.8+
- **BERT**: transformers, torch (rubert-tiny2)
- **Baseline**: scikit-learn (TF-IDF, LogisticRegression, OneVsRestClassifier)
- NLTK, pymorphy2 (предобработка текста)
- matplotlib, seaborn (визуализация)
