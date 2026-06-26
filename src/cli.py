"""Консольный интерфейс для распознавания эмоций."""

MAX_TEXT_LENGTH = 1000

HELP_TEXT = """
╔══════════════════════════════════════════════════════╗
║      Распознавание эмоций по тексту (NLP-Emo-01)     ║
╠══════════════════════════════════════════════════════╣
║                                                      ║
║  Введите текст на русском языке, и программа         ║
║  определит его эмоциональную окраску.                ║
║                                                      ║
║  Доступные команды:                                  ║
║    /help  — показать эту справку                     ║
║    /exit  — завершить работу                         ║
║                                                      ║
║  Распознаваемые эмоции:                              ║
║    радость, грусть, гнев, страх, удивление,          ║
║    отвращение, воодушевление, вина, стыд,            ║
║    нейтральность                                     ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
"""


def run_cli(use_bert=False):
    """Запускает интерактивный консольный интерфейс.

    Args:
        use_bert: если True — использует BERT модель, иначе TF-IDF + LogReg.
    """
    if use_bert:
        print("Загрузка BERT модели...")
        try:
            from src.bert_model import load_bert, predict_single_bert
            model, tokenizer, device = load_bert()
            predict_fn = lambda text: predict_single_bert(model, tokenizer, device, text)
            model_name = "BERT (rubert-tiny2)"
        except (FileNotFoundError, OSError):
            print("Ошибка: BERT модель не найдена. "
                  "Сначала запустите обучение: python3 train_bert.py")
            return
        except Exception as e:
            print(f"Ошибка: не удалось загрузить BERT модель — файл повреждён "
                  f"или несовместим.\nПодробности: {e}\n"
                  "Попробуйте переобучить модель: python3 train_bert.py")
            return
    else:
        print("Загрузка модели TF-IDF + LogReg...")
        try:
            from src.model import load_model, predict_single
            from src.vectorizer import load_vectorizer
            from src.preprocessing import preprocess
            model = load_model()
            vectorizer = load_vectorizer()
            predict_fn = lambda text: predict_single(model, vectorizer, preprocess, text)
            model_name = "TF-IDF + LogisticRegression"
        except FileNotFoundError:
            print("Ошибка: файлы модели не найдены. "
                  "Сначала запустите обучение: python3 train.py")
            return
        except Exception as e:
            print(f"Ошибка: не удалось загрузить модель — файл повреждён "
                  f"или несовместим.\nПодробности: {e}\n"
                  "Попробуйте переобучить модель: python3 train.py")
            return

    print(f"Модель: {model_name}")
    print(HELP_TEXT)

    while True:
        try:
            text = input("\nВведите текст: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nДо свидания!")
            break

        if not text:
            print("Ошибка: введена пустая строка. Пожалуйста, введите текст.")
            continue

        if text == "/exit":
            print("До свидания!")
            break

        if text == "/help":
            print(HELP_TEXT)
            continue

        if text.startswith("/"):
            print(f"Неизвестная команда: {text}. Введите /help для справки.")
            continue

        if len(text) > MAX_TEXT_LENGTH:
            print(f"Ошибка: текст слишком длинный ({len(text)} символов). "
                  f"Максимум — {MAX_TEXT_LENGTH} символов.")
            continue

        try:
            emotion, confidence = predict_fn(text)
        except Exception as e:
            print(f"Ошибка при обработке текста: {e}")
            print("Попробуйте ввести другой текст.")
            continue
        print(f"  Эмоция: {emotion}")
        print(f"  Уверенность: {confidence}%")
