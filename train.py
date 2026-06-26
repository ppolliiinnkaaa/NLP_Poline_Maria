"""Скрипт обучения: загрузка данных → предобработка → TF-IDF → модель → оценка."""

import sys
import numpy as np
from src.data_loader import load_data, get_labels_matrix, EMOTION_COLUMNS
from src.preprocessing import preprocess
from src.vectorizer import train_vectorizer
from src.model import train_model, save_model, RANDOM_SEED
from src.evaluate import evaluate_multilabel, evaluate_top1, compute_hit_rate

np.random.seed(RANDOM_SEED)


def main():
    model_type = sys.argv[1] if len(sys.argv) > 1 else "logreg"
    print(f"=== Обучение модели: {model_type} ===\n")

    # 1. Загрузка данных
    print("Загрузка данных...")
    df_train = load_data("train")
    df_test = load_data("test")
    print(f"  Train: {len(df_train)}, Test: {len(df_test)}")

    # 2. Предобработка
    print("Предобработка текстов...")
    train_texts = df_train["text"].apply(preprocess)
    test_texts = df_test["text"].apply(preprocess)

    # 3. Векторизация
    print("Обучение TF-IDF...")
    vectorizer, X_train = train_vectorizer(train_texts)
    X_test = vectorizer.transform(test_texts)

    # 4. Метки
    y_train = get_labels_matrix(df_train).values
    y_test = get_labels_matrix(df_test).values

    # 5. Обучение
    print(f"Обучение модели ({model_type})...")
    model = train_model(X_train, y_train, model_type=model_type)

    # 6. Оценка multi-label
    y_pred = model.predict(X_test)
    evaluate_multilabel(y_test, y_pred)

    # 7. Оценка top-1 + Confusion Matrix
    evaluate_top1(y_test, model, X_test)

    # 8. Hit Rate
    probas = model.predict_proba(X_test)
    if isinstance(probas, list):
        probas = np.column_stack([p[:, 1] for p in probas])
    hr = compute_hit_rate(y_test, probas)
    print(f"\nTop-1 Hit Rate: {hr:.4f} (предсказание попадает в любую из истинных меток)")

    # 9. Сохранение модели
    save_model(model)
    print("\nГотово!")


if __name__ == "__main__":
    main()
