"""Генерация PDF-инструкции для создания презентации по проекту NLP-Emo-01."""

import os
from fpdf import FPDF

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "Инструкция_для_презентации_NLP_Emo.pdf")


class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 9)
        self.set_text_color(130, 130, 130)
        self.cell(0, 8, "NLP-Emo-01 — Подробная инструкция для презентации",
                  align="R", new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(130, 130, 130)
        self.cell(0, 10, f"Страница {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.ln(4)
        self.set_font("DejaVu", "B", 14)
        self.set_text_color(30, 60, 120)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(30, 60, 120)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(3)

    def sub_title(self, title):
        self.ln(2)
        self.set_font("DejaVu", "B", 11)
        self.set_text_color(50, 50, 50)
        self.cell(0, 8, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def small_title(self, title):
        self.ln(1)
        self.set_font("DejaVu", "B", 10)
        self.set_text_color(70, 70, 70)
        self.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT")

    def body(self, text):
        self.set_font("DejaVu", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def hint(self, text):
        """Серый курсивоподобный блок-подсказка."""
        self.set_font("DejaVu", "", 9)
        self.set_text_color(90, 90, 90)
        self.set_fill_color(245, 248, 255)
        y = self.get_y()
        self.rect(12, y, 186, 1, "F")  # тонкая полоска акцента
        self.set_fill_color(245, 248, 255)
        self.set_x(14)
        self.multi_cell(182, 5.5, "Подсказка: " + text, fill=True,
                        new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def bullet(self, text, indent=10):
        self.set_font("DejaVu", "", 10)
        self.set_text_color(30, 30, 30)
        self.cell(indent, 6, "  •", new_x="END")
        self.multi_cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")

    def bold_bullet(self, bold_part, rest, indent=10):
        self.set_text_color(30, 30, 30)
        self.set_font("DejaVu", "", 10)
        self.cell(indent, 6, "  •", new_x="END")
        self.set_font("DejaVu", "B", 10)
        w_bold = self.get_string_width(bold_part)
        self.cell(w_bold, 6, bold_part, new_x="END")
        self.set_font("DejaVu", "", 10)
        self.multi_cell(0, 6, rest, new_x="LMARGIN", new_y="NEXT")

    def num_bullet(self, num, text):
        self.set_font("DejaVu", "B", 10)
        self.set_text_color(30, 60, 120)
        self.cell(10, 6, f"  {num}.", new_x="END")
        self.set_font("DejaVu", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")

    def code_block(self, text):
        self.set_font("DejaVuMono", "", 9)
        self.set_fill_color(240, 240, 240)
        self.set_text_color(30, 30, 30)
        self.set_draw_color(200, 200, 200)
        lines = text.strip().split("\n")
        h = len(lines) * 5.5 + 6
        y = self.get_y()
        if y + h > 270:
            self.add_page()
            y = self.get_y()
        self.rect(12, y, 186, h, "DF")
        self.ln(3)
        for line in lines:
            self.cell(5)
            self.cell(0, 5.5, "  " + line, new_x="LMARGIN", new_y="NEXT")
        self.ln(4)

    def table_row(self, cells, widths, header=False):
        self.set_font("DejaVu", "B" if header else "", 9)
        if header:
            self.set_fill_color(30, 60, 120)
            self.set_text_color(255, 255, 255)
        else:
            self.set_fill_color(248, 248, 248)
            self.set_text_color(30, 30, 30)
        h = 8
        for i, cell in enumerate(cells):
            self.cell(widths[i], h, " " + cell, border=1, fill=True)
        self.ln(h)

    def slide_header(self, num, title):
        """Заголовок слайда — крупный, с номером."""
        self.ln(3)
        self.set_fill_color(30, 60, 120)
        self.set_text_color(255, 255, 255)
        self.set_font("DejaVu", "B", 12)
        self.cell(0, 10, f"  СЛАЙД {num}: {title}", fill=True,
                  new_x="LMARGIN", new_y="NEXT")
        self.ln(3)


def find_fonts():
    search_paths = [
        "/usr/share/fonts/truetype/dejavu",
        "/usr/share/fonts/dejavu",
        "/opt/homebrew/share/fonts",
        os.path.expanduser("~/.local/share/fonts"),
        "/System/Library/Fonts",
        "/Library/Fonts",
    ]
    for sp in search_paths:
        r = os.path.join(sp, "DejaVuSans.ttf")
        if os.path.exists(r):
            b = os.path.join(sp, "DejaVuSans-Bold.ttf")
            m = os.path.join(sp, "DejaVuSansMono.ttf")
            return r, b if os.path.exists(b) else r, m if os.path.exists(m) else r

    import urllib.request, zipfile
    font_cache = os.path.join(os.path.dirname(__file__), ".fonts")
    os.makedirs(font_cache, exist_ok=True)
    r = os.path.join(font_cache, "DejaVuSans.ttf")
    b = os.path.join(font_cache, "DejaVuSans-Bold.ttf")
    m = os.path.join(font_cache, "DejaVuSansMono.ttf")
    if not os.path.exists(r):
        url = "https://github.com/dejavu-fonts/dejavu-fonts/releases/download/version_2_37/dejavu-fonts-ttf-2.37.zip"
        zip_path = os.path.join(font_cache, "dejavu.zip")
        print("Скачиваю шрифты DejaVu...")
        urllib.request.urlretrieve(url, zip_path)
        with zipfile.ZipFile(zip_path, "r") as zf:
            for name in zf.namelist():
                if name.endswith(".ttf"):
                    fname = os.path.basename(name)
                    with open(os.path.join(font_cache, fname), "wb") as f:
                        f.write(zf.read(name))
        os.remove(zip_path)
    return r, b, m


def build_pdf():
    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    reg, bold, mono = find_fonts()
    pdf.add_font("DejaVu", "", reg)
    pdf.add_font("DejaVu", "B", bold)
    pdf.add_font("DejaVuMono", "", mono)

    # ================================================================
    #                      ТИТУЛЬНАЯ СТРАНИЦА
    # ================================================================
    pdf.add_page()
    pdf.ln(30)
    pdf.set_font("DejaVu", "B", 24)
    pdf.set_text_color(30, 60, 120)
    pdf.cell(0, 14, "NLP-Emo-01", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("DejaVu", "", 15)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 10, "Распознавание эмоций по тексту", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_draw_color(30, 60, 120)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(8)
    pdf.set_font("DejaVu", "B", 13)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, "Подробная инструкция для подготовки презентации",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 7,
             "Этот документ содержит всю информацию, необходимую для создания",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7,
             "презентации проекта. Для каждого слайда указано: заголовок, что написать,",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7,
             "какие картинки вставить и что можно сказать при защите.",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(25)
    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 7, "МГТУ им. Н.Э. Баумана, кафедра ИУ10", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Группа ИУ10-44", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Исполнители: Осипова П.С., Селина М.А.", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Преподаватель: Буркацкий К.А.", align="C",
             new_x="LMARGIN", new_y="NEXT")

    # ================================================================
    #               КРАТКОЕ ОПИСАНИЕ ПРОЕКТА (КОНТЕКСТ)
    # ================================================================
    pdf.add_page()
    pdf.section_title("Что это за проект (прочитай перед началом)")
    pdf.body(
        "Мы написали программу на Python, которая определяет эмоцию в тексте. "
        "Пользователь вводит фразу на русском языке (например «Меня это бесит!»), "
        "а программа отвечает: «Эмоция: гнев, Уверенность: 92%»."
    )
    pdf.body(
        "Программа умеет распознавать 10 эмоций: радость, грусть, гнев, страх, "
        "удивление, отвращение, воодушевление, вина, стыд и нейтральность."
    )
    pdf.body(
        "Мы сделали два подхода к решению задачи:\n"
        "1) Простой (baseline): текст превращается в числа через TF-IDF, "
        "потом классифицируется LogisticRegression.\n"
        "2) Продвинутый: используем нейросеть BERT (rubert-tiny2), "
        "которая понимает смысл текста. BERT работает лучше."
    )
    pdf.body(
        "Программа работает через консоль (терминал). Есть команды /help и /exit. "
        "Все ошибки обрабатываются, программа не падает."
    )
    pdf.ln(2)
    pdf.body(
        "Датасет — ru-izard-emotions с Hugging Face, ~25 000 текстов на русском "
        "языке. Каждый текст размечен по 10 эмоциям (один текст может иметь "
        "несколько эмоций — это называется multi-label)."
    )

    pdf.section_title("Словарь терминов (чтобы понимать о чём речь)")
    terms = [
        ("NLP", "Natural Language Processing — обработка естественного языка "
         "компьютером"),
        ("TF-IDF", "способ превратить текст в числа, чтобы подать на вход модели. "
         "Считает, какие слова важны в конкретном тексте"),
        ("BERT", "нейросеть-трансформер, которая «понимает» смысл слов в контексте. "
         "Мы используем rubert-tiny2 — версию для русского языка"),
        ("Fine-tuning", "дообучение — берём готовую модель BERT и доучиваем "
         "её на наших данных об эмоциях"),
        ("Лемматизация", "приведение слова к начальной форме: «бесит» → «бесить»"),
        ("Стоп-слова", "слова, которые не несут смысла и удаляются: «и», «в», «на»"),
        ("Accuracy", "доля правильных ответов (чем выше — тем лучше)"),
        ("Precision", "из того, что модель назвала «гнев» — сколько реально гнев"),
        ("Recall", "из всех текстов с гневом — сколько модель нашла"),
        ("F1-score", "среднее между Precision и Recall (одна метрика вместо двух)"),
        ("Confusion Matrix", "таблица-тепловая карта, показывающая какие эмоции "
         "модель путает между собой"),
        ("Confidence", "уверенность модели в ответе (0–100%)"),
        ("Multi-label", "один текст может иметь несколько эмоций одновременно"),
        ("OneVsRest", "способ решения multi-label: обучаем отдельный "
         "классификатор для каждой эмоции"),
    ]
    for term, desc in terms:
        pdf.bold_bullet(f"{term} — ", desc)

    # ================================================================
    #                     СЛАЙДЫ — ПОДРОБНО
    # ================================================================
    pdf.add_page()
    pdf.section_title("Детальное описание каждого слайда")
    pdf.body(
        "Ниже для каждого слайда написано: какой заголовок поставить, "
        "что именно написать в теле слайда (можно копировать текст), "
        "и подсказки — что можно сказать голосом при защите."
    )

    # ---- СЛАЙД 1 ----
    pdf.slide_header(1, "ТИТУЛЬНЫЙ")
    pdf.small_title("Заголовок слайда:")
    pdf.body("«Распознавание эмоций по тексту»")
    pdf.small_title("Что написать на слайде:")
    pdf.bullet("Шифр проекта: NLP-Emo-01")
    pdf.bullet("МГТУ им. Н.Э. Баумана, кафедра ИУ10")
    pdf.bullet("Группа: ИУ10-44")
    pdf.bullet("Исполнители: Осипова П.С., Селина М.А.")
    pdf.bullet("Преподаватель: Буркацкий К.А.")
    pdf.bullet("2025/2026 учебный год")
    pdf.hint("Этот слайд стандартный. Оформи как титульный лист курсовой.")

    # ---- СЛАЙД 2 ----
    pdf.slide_header(2, "ПОСТАНОВКА ЗАДАЧИ")
    pdf.small_title("Заголовок слайда:")
    pdf.body("«Постановка задачи»")
    pdf.small_title("Что написать на слайде:")
    pdf.body(
        "Цель: разработать программу для автоматического определения "
        "эмоциональной окраски текста на русском языке."
    )
    pdf.body("Принцип работы:")
    pdf.num_bullet(1, "Пользователь вводит текст на русском языке")
    pdf.num_bullet(2, "Программа выполняет предобработку и классификацию")
    pdf.num_bullet(3, "Выводит метку эмоции и уверенность модели (%)")
    pdf.ln(1)
    pdf.body("Пример:")
    pdf.code_block(
        'Ввод:  «Меня это бесит, я в ярости!»\n'
        'Вывод: Эмоция: гнев, Уверенность: 92%'
    )
    pdf.hint(
        "На защите скажи: «Задача — классификация текста по эмоциям. "
        "Пользователь вводит текст, программа говорит какая это эмоция "
        "и насколько она уверена.»"
    )

    # ---- СЛАЙД 3 ----
    pdf.slide_header(3, "ОБЛАСТЬ ПРИМЕНЕНИЯ")
    pdf.small_title("Заголовок слайда:")
    pdf.body("«Область применения»")
    pdf.small_title("Что написать (3 пункта, каждый с иконкой или буллетом):")
    pdf.bullet("Анализ тональности текстов в соцсетях и системах обратной связи")
    pdf.bullet("Поддержка чат-ботов и систем мониторинга тональности")
    pdf.bullet("Учебно-исследовательские цели (курсовые, дипломы по NLP)")
    pdf.hint(
        "На защите: «Программа может использоваться для автоматического "
        "анализа отзывов клиентов, мониторинга настроений в соцсетях, "
        "а также как учебный проект.»"
    )

    # ---- СЛАЙД 4 ----
    pdf.add_page()
    pdf.slide_header(4, "ДАТАСЕТ")
    pdf.small_title("Заголовок слайда:")
    pdf.body("«Датасет: ru-izard-emotions»")
    pdf.small_title("Что написать (список фактов):")
    pdf.bullet("Источник: Hugging Face (автор Djacon)")
    pdf.bullet("Объём: ~25 000 текстов на русском языке")
    pdf.bullet("10 классов эмоций (модель Изарда)")
    pdf.bullet("Разметка: multi-label — у текста может быть несколько эмоций")
    pdf.bullet("Формат: CSV/JSON, кодировка UTF-8")
    pdf.bullet("Разбиение: 80% обучение / 20% тест, seed=42")
    pdf.ln(1)
    pdf.small_title("Список 10 эмоций (можно в виде таблицы на слайде):")
    w = [50, 50]
    pdf.table_row(["Русский", "English"], w, header=True)
    for ru, en in [("Радость", "joy"), ("Грусть", "sadness"),
                   ("Гнев", "anger"), ("Страх", "fear"),
                   ("Удивление", "surprise"), ("Отвращение", "disgust"),
                   ("Воодушевление", "enthusiasm"), ("Вина", "guilt"),
                   ("Стыд", "shame"), ("Нейтральность", "neutral")]:
        pdf.table_row([ru, en], w)
    pdf.hint(
        "На защите: «Датасет содержит 25 тысяч текстов, размеченных по 10 эмоциям. "
        "Это multi-label задача — один текст может выражать и грусть, и страх "
        "одновременно.»"
    )

    # ---- СЛАЙД 5 ----
    pdf.slide_header(5, "ПАЙПЛАЙН ОБРАБОТКИ")
    pdf.small_title("Заголовок слайда:")
    pdf.body("«Архитектура: пайплайн обработки текста»")
    pdf.small_title("Что нарисовать — схема из 5 блоков со стрелками:")
    pdf.code_block(
        "[Текст пользователя]\n"
        "        |\n"
        "        v\n"
        "[Предобработка] - lowercase, удаление пунктуации,\n"
        "                  стоп-слов, лемматизация\n"
        "        |\n"
        "        v\n"
        "[Векторизация] - TF-IDF или BERT-эмбеддинги\n"
        "        |\n"
        "        v\n"
        "[Классификация] - LogReg / RandomForest / BERT\n"
        "        |\n"
        "        v\n"
        "[Результат] - Эмоция + Уверенность (%)"
    )
    pdf.hint(
        "Сделай красивую блок-схему из прямоугольников со стрелками. "
        "Каждый блок — этап обработки. Это ключевой слайд, он показывает "
        "как программа работает изнутри."
    )

    # ---- СЛАЙД 6 ----
    pdf.slide_header(6, "ПРЕДОБРАБОТКА ТЕКСТА")
    pdf.small_title("Заголовок слайда:")
    pdf.body("«Предобработка текста»")
    pdf.small_title("Что написать (4 этапа + пример):")
    pdf.num_bullet(1, "Приведение к нижнему регистру (lowercase)")
    pdf.num_bullet(2, "Удаление знаков препинания и спецсимволов")
    pdf.num_bullet(3, "Удаление стоп-слов (NLTK, русский язык)")
    pdf.num_bullet(4, "Лемматизация — слово → начальная форма (pymorphy2)")
    pdf.ln(2)
    pdf.small_title("Пример (покажи на слайде как трансформируется текст):")
    pdf.code_block(
        'Исходный:      «Меня это бесит, я в ярости!»\n'
        'Lowercase:      «меня это бесит, я в ярости!»\n'
        'Без пунктуации: «меня это бесит я в ярости»\n'
        'Без стоп-слов:  «бесит ярости»\n'
        'Лемматизация:   «бесить ярость»'
    )
    pdf.hint(
        "На защите: «Предобработка нужна, чтобы убрать шум из текста. "
        "Модели проще работать с чистыми леммами, чем с сырым текстом.»"
    )

    # ---- СЛАЙД 7 ----
    pdf.add_page()
    pdf.slide_header(7, "МОДЕЛИ КЛАССИФИКАЦИИ")
    pdf.small_title("Заголовок слайда:")
    pdf.body("«Модели классификации»")
    pdf.small_title("Что написать — два блока:")
    pdf.ln(1)
    pdf.body("Блок 1 — Baseline (простая модель):")
    pdf.bullet("TF-IDF — превращает текст в числовой вектор")
    pdf.bullet("LogisticRegression — классический алгоритм классификации")
    pdf.bullet("OneVsRest — отдельный классификатор на каждую эмоцию")
    pdf.bullet("Быстро обучается, но невысокая точность")
    pdf.ln(1)
    pdf.body("Блок 2 — Основная модель (нейросеть):")
    pdf.bullet("BERT (rubert-tiny2) — трансформер для русского языка")
    pdf.bullet("Fine-tuning — дообучили предобученную модель на наших данных")
    pdf.bullet("Понимает контекст слов (в отличие от TF-IDF)")
    pdf.bullet("Значительно лучше по метрикам")
    pdf.hint(
        "На защите: «Мы реализовали два подхода. Baseline — классический "
        "TF-IDF + логистическая регрессия, и BERT — нейросеть-трансформер. "
        "BERT показал результаты значительно лучше, потому что он "
        "учитывает контекст слов в предложении.»"
    )

    # ---- СЛАЙД 8 ----
    pdf.slide_header(8, "РЕЗУЛЬТАТЫ")
    pdf.small_title("Заголовок слайда:")
    pdf.body("«Результаты: сравнение моделей»")
    pdf.small_title("Что написать — таблица метрик:")
    pdf.ln(1)
    w3 = [55, 40, 50]
    pdf.table_row(["Метрика", "TF-IDF+LogReg", "BERT (rubert-tiny2)"], w3,
                  header=True)
    pdf.table_row(["F1-score (macro)", "0.29", "0.49"], w3)
    pdf.table_row(["Top-1 Accuracy", "44.6%", "47.1%"], w3)
    pdf.table_row(["Recall (macro)", "0.20", "0.43"], w3)
    pdf.ln(2)
    pdf.small_title("Также вставь картинку Confusion Matrix:")
    pdf.body(
        "Файл: models/confusion_matrix_bert.png (или confusion_matrix_bert_single.png)\n"
        "Это тепловая карта — показывает какие эмоции модель путает."
    )
    pdf.ln(1)
    pdf.small_title("Вывод (напиши внизу слайда):")
    pdf.body(
        "BERT превосходит baseline по всем метрикам. "
        "Трансформеры — более эффективный подход для классификации эмоций."
    )
    pdf.hint(
        "На защите объясни метрики: «F1-score — это баланс между точностью "
        "и полнотой. Accuracy — доля правильных ответов. BERT дал F1 = 0.49 "
        "против 0.29 у baseline — почти вдвое лучше.» "
        "Если спросят про Confusion Matrix — покажи, какие эмоции модель "
        "путает чаще всего."
    )

    # ---- СЛАЙД 9 ----
    pdf.slide_header(9, "ДЕМОНСТРАЦИЯ РАБОТЫ")
    pdf.small_title("Заголовок слайда:")
    pdf.body("«Демонстрация работы программы»")
    pdf.small_title("Что сделать:")
    pdf.body(
        "Вставь скриншот работы программы в консоли. "
        "Чтобы сделать скриншот, запусти:"
    )
    pdf.code_block(
        "python3 main.py --bert"
    )
    pdf.body("И введи несколько примеров:")
    pdf.code_block(
        'Введите текст: Меня это бесит, я в ярости!\n'
        '  Эмоция: гнев\n'
        '  Уверенность: 92%\n'
        '\n'
        'Введите текст: Какой прекрасный день сегодня!\n'
        '  Эмоция: радость\n'
        '  Уверенность: 78%\n'
        '\n'
        'Введите текст: Мне так страшно...\n'
        '  Эмоция: страх\n'
        '  Уверенность: 85%'
    )
    pdf.hint(
        "Если есть возможность — сделай живую демонстрацию на защите "
        "(запусти программу и введи текст прямо при комиссии). "
        "Если нет — хватит скриншота."
    )

    # ---- СЛАЙД 10 ----
    pdf.add_page()
    pdf.slide_header(10, "СТЕК ТЕХНОЛОГИЙ")
    pdf.small_title("Заголовок слайда:")
    pdf.body("«Стек технологий»")
    pdf.small_title("Что написать — таблица с пояснениями:")
    pdf.body(
        "Не просто перечисли библиотеки — покажи ЗАЧЕМ каждая нужна. "
        "Сделай таблицу из трёх колонок:"
    )
    pdf.ln(1)
    w3t = [40, 55, 90]
    pdf.table_row(["Назначение", "Технология", "Зачем используется"], w3t,
                  header=True)
    pdf.table_row(["Язык", "Python 3.8+",
                   "Основной язык разработки"], w3t)
    pdf.table_row(["NLP", "NLTK",
                   "Стоп-слова русского языка"], w3t)
    pdf.table_row(["NLP", "pymorphy2",
                   "Лемматизация (морфоанализ)"], w3t)
    pdf.table_row(["NLP", "re (regex)",
                   "Удаление пунктуации и спецсимволов"], w3t)
    pdf.table_row(["Векторизация", "scikit-learn",
                   "TF-IDF: текст -> числовой вектор"], w3t)
    pdf.table_row(["Векторизация", "Transformers",
                   "BERT-эмбеддинги (rubert-tiny2)"], w3t)
    pdf.table_row(["ML-модели", "scikit-learn",
                   "LogReg, RandomForest, метрики"], w3t)
    pdf.table_row(["Нейросеть", "PyTorch",
                   "Обучение и инференс BERT"], w3t)
    pdf.table_row(["Данные", "pandas",
                   "Работа с таблицами данных"], w3t)
    pdf.table_row(["Данные", "HF Datasets",
                   "Загрузка датасета"], w3t)
    pdf.table_row(["Графики", "matplotlib",
                   "Confusion Matrix"], w3t)
    pdf.table_row(["Графики", "seaborn",
                   "Тепловые карты"], w3t)
    pdf.table_row(["Сохранение", "joblib / torch",
                   "Сериализация моделей (.pkl, .pt)"], w3t)
    pdf.hint(
        "На защите: «Каждая технология в стеке решает конкретную задачу. "
        "Например, NLTK даёт нам стоп-слова русского языка, pymorphy2 "
        "приводит слова к начальной форме, а scikit-learn — это и "
        "векторизация через TF-IDF, и baseline-модели, и расчёт метрик.»"
    )

    # ---- СЛАЙД 11 ----
    pdf.slide_header(11, "ВЫВОДЫ")
    pdf.small_title("Заголовок слайда:")
    pdf.body("«Выводы»")
    pdf.small_title("Что написать (3-4 пункта):")
    pdf.num_bullet(1,
        "Разработана программа классификации эмоций в тексте на русском языке")
    pdf.num_bullet(2,
        "Реализованы два подхода: TF-IDF + LogReg (baseline) "
        "и BERT (rubert-tiny2)")
    pdf.num_bullet(3,
        "BERT показал F1-score 0.49 — почти вдвое лучше baseline (0.29)")
    pdf.num_bullet(4,
        "Все требования ТЗ выполнены: предобработка, векторизация, "
        "классификация, оценка качества, консольный интерфейс")
    pdf.hint(
        "На защите: «В результате работы мы убедились, что трансформеры "
        "значительно превосходят классические методы на задаче "
        "классификации эмоций. Программа полностью соответствует ТЗ "
        "и готова к эксплуатации.»"
    )

    # ================================================================
    #              ДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ
    # ================================================================
    pdf.add_page()
    pdf.section_title("Структура проекта (для справки)")
    pdf.code_block(
        "NLP_Emo/\n"
        "├── main.py                 # Точка входа (запуск CLI)\n"
        "├── train.py                # Обучение TF-IDF модели\n"
        "├── train_bert.py           # Обучение BERT (multi-label)\n"
        "├── train_bert_single.py    # Обучение BERT (single-label)\n"
        "├── src/\n"
        "│   ├── data_loader.py      # Загрузка датасета (HF / CSV / JSON)\n"
        "│   ├── preprocessing.py    # Предобработка текста\n"
        "│   ├── vectorizer.py       # TF-IDF векторизация\n"
        "│   ├── model.py            # Классическая ML-модель\n"
        "│   ├── bert_model.py       # BERT fine-tuning и инференс\n"
        "│   ├── evaluate.py         # Метрики и Confusion Matrix\n"
        "│   └── cli.py              # Консольный интерфейс\n"
        "├── models/                 # Сохранённые модели и графики\n"
        "├── requirements.txt        # Зависимости Python\n"
        "└── README.md               # Документация"
    )

    pdf.section_title("Как запустить программу (если нужен скриншот)")
    pdf.sub_title("Установка зависимостей")
    pdf.code_block("pip install -r requirements.txt")
    pdf.sub_title("Обучение модели")
    pdf.code_block(
        "python3 train.py              # TF-IDF + LogReg (быстро)\n"
        "python3 train_bert.py         # BERT multi-label (дольше)\n"
        "python3 train_bert_single.py  # BERT single-label"
    )
    pdf.sub_title("Запуск программы")
    pdf.code_block(
        "python3 main.py              # TF-IDF модель (по умолчанию)\n"
        "python3 main.py --bert       # BERT модель"
    )

    pdf.section_title("Файлы для вставки в презентацию")
    pdf.body("Готовые картинки Confusion Matrix (тепловые карты):")
    pdf.bullet("models/confusion_matrix.png — для TF-IDF модели")
    pdf.bullet("models/confusion_matrix_bert.png — для BERT multi-label")
    pdf.bullet("models/confusion_matrix_bert_single.png — для BERT single-label")
    pdf.ln(1)
    pdf.body(
        "Вставь одну из этих картинок на слайд 8 (Результаты). "
        "Лучше всего подойдёт confusion_matrix_bert_single.png — "
        "она проще для понимания."
    )

    # ===== Сохранение =====
    pdf.output(OUTPUT_PATH)
    print(f"PDF сохранён: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
