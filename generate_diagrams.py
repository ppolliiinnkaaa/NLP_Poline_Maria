"""Генерация PDF с диаграммами, схемами и подробным описанием слайдов."""

import os
from fpdf import FPDF

OUTPUT_PATH = os.path.join(os.path.dirname(__file__),
                           "Диаграммы_и_схемы_NLP_Emo.pdf")


class PDF(FPDF):
    def header(self):
        self.set_font("DejaVu", "B", 9)
        self.set_text_color(130, 130, 130)
        self.cell(0, 8, "NLP-Emo-01 — Диаграммы, схемы и описание слайдов",
                  align="R", new_x="LMARGIN", new_y="NEXT")
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "", 8)
        self.set_text_color(130, 130, 130)
        self.cell(0, 10, f"Страница {self.page_no()}/{{nb}}", align="C")

    def section_title(self, title):
        self.ln(3)
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

    def body(self, text):
        self.set_font("DejaVu", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text)
        self.ln(1)

    def bullet(self, text):
        self.set_font("DejaVu", "", 10)
        self.set_text_color(30, 30, 30)
        self.cell(10, 6, "  •", new_x="END")
        self.multi_cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")

    def bold_bullet(self, bold_part, rest):
        self.set_text_color(30, 30, 30)
        self.set_font("DejaVu", "", 10)
        self.cell(10, 6, "  •", new_x="END")
        self.set_font("DejaVu", "B", 10)
        w = self.get_string_width(bold_part)
        self.cell(w, 6, bold_part, new_x="END")
        self.set_font("DejaVu", "", 10)
        self.multi_cell(0, 6, rest, new_x="LMARGIN", new_y="NEXT")

    def num_bullet(self, num, text):
        self.set_font("DejaVu", "B", 10)
        self.set_text_color(30, 60, 120)
        self.cell(10, 6, f"  {num}.", new_x="END")
        self.set_font("DejaVu", "", 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text, new_x="LMARGIN", new_y="NEXT")

    def hint(self, text):
        self.set_font("DejaVu", "", 9)
        self.set_text_color(90, 90, 90)
        self.set_fill_color(245, 248, 255)
        self.set_x(14)
        self.multi_cell(182, 5.5, "Подсказка: " + text, fill=True,
                        new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

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
        for i, cell in enumerate(cells):
            self.cell(widths[i], 8, " " + cell, border=1, fill=True)
        self.ln(8)

    def slide_header(self, num, title):
        self.ln(3)
        self.set_fill_color(30, 60, 120)
        self.set_text_color(255, 255, 255)
        self.set_font("DejaVu", "B", 12)
        self.cell(0, 10, f"  СЛАЙД {num}: {title}", fill=True,
                  new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    # ===== РИСОВАНИЕ ДИАГРАММ =====

    def _box(self, x, y, w, h, text, fill_color=(220, 235, 255),
             border_color=(30, 60, 120), text_color=(30, 30, 30),
             font_size=9, bold=False):
        """Рисует прямоугольник с текстом."""
        self.set_fill_color(*fill_color)
        self.set_draw_color(*border_color)
        self.set_line_width(0.5)
        self.rect(x, y, w, h, "DF")
        self.set_font("DejaVu", "B" if bold else "", font_size)
        self.set_text_color(*text_color)
        self.set_xy(x, y)
        self.cell(w, h, text, align="C")

    def _rounded_box(self, x, y, w, h, text, fill_color=(220, 235, 255),
                     border_color=(30, 60, 120)):
        """Рисует скруглённый прямоугольник с текстом."""
        self.set_fill_color(*fill_color)
        self.set_draw_color(*border_color)
        self.set_line_width(0.5)
        self.rect(x, y, w, h, "DF")
        self.set_font("DejaVu", "", 9)
        self.set_text_color(30, 30, 30)
        self.set_xy(x, y)
        self.cell(w, h, text, align="C")

    def _ellipse(self, cx, cy, rx, ry, text, fill_color=(255, 240, 220),
                 border_color=(180, 100, 30)):
        """Рисует эллипс с текстом."""
        self.set_fill_color(*fill_color)
        self.set_draw_color(*border_color)
        self.set_line_width(0.5)
        self.ellipse(cx - rx, cy - ry, rx * 2, ry * 2, "DF")
        self.set_font("DejaVu", "", 8)
        self.set_text_color(30, 30, 30)
        self.set_xy(cx - rx, cy - 4)
        self.cell(rx * 2, 8, text, align="C")

    def _arrow_down(self, x, y1, y2):
        """Стрелка вниз."""
        self.set_draw_color(30, 60, 120)
        self.set_line_width(0.6)
        self.line(x, y1, x, y2)
        # наконечник
        self.line(x, y2, x - 2, y2 - 4)
        self.line(x, y2, x + 2, y2 - 4)

    def _arrow_right(self, x1, y, x2):
        """Стрелка вправо."""
        self.set_draw_color(30, 60, 120)
        self.set_line_width(0.6)
        self.line(x1, y, x2, y)
        self.line(x2, y, x2 - 4, y - 2)
        self.line(x2, y, x2 - 4, y + 2)

    def _arrow_left(self, x1, y, x2):
        """Стрелка влево."""
        self.set_draw_color(30, 60, 120)
        self.set_line_width(0.6)
        self.line(x1, y, x2, y)
        self.line(x2, y, x2 + 4, y - 2)
        self.line(x2, y, x2 + 4, y + 2)

    def _line_to(self, x1, y1, x2, y2):
        self.set_draw_color(100, 100, 100)
        self.set_line_width(0.4)
        self.line(x1, y1, x2, y2)

    def _dashed_line(self, x1, y1, x2, y2, dash=3, gap=2):
        """Пунктирная линия."""
        import math
        dx = x2 - x1
        dy = y2 - y1
        length = math.sqrt(dx * dx + dy * dy)
        if length == 0:
            return
        ux, uy = dx / length, dy / length
        self.set_draw_color(120, 120, 120)
        self.set_line_width(0.4)
        pos = 0
        while pos < length:
            sx = x1 + ux * pos
            sy = y1 + uy * pos
            end = min(pos + dash, length)
            ex = x1 + ux * end
            ey = y1 + uy * end
            self.line(sx, sy, ex, ey)
            pos += dash + gap

    def _label(self, x, y, text, font_size=8, color=(80, 80, 80)):
        self.set_font("DejaVu", "", font_size)
        self.set_text_color(*color)
        self.set_xy(x, y)
        self.cell(0, 5, text)


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
    fc = os.path.join(os.path.dirname(__file__), ".fonts")
    os.makedirs(fc, exist_ok=True)
    r = os.path.join(fc, "DejaVuSans.ttf")
    b = os.path.join(fc, "DejaVuSans-Bold.ttf")
    m = os.path.join(fc, "DejaVuSansMono.ttf")
    if not os.path.exists(r):
        url = ("https://github.com/dejavu-fonts/dejavu-fonts/releases/"
               "download/version_2_37/dejavu-fonts-ttf-2.37.zip")
        zp = os.path.join(fc, "dejavu.zip")
        print("Скачиваю шрифты DejaVu...")
        urllib.request.urlretrieve(url, zp)
        with zipfile.ZipFile(zp, "r") as zf:
            for name in zf.namelist():
                if name.endswith(".ttf"):
                    fn = os.path.basename(name)
                    with open(os.path.join(fc, fn), "wb") as f:
                        f.write(zf.read(name))
        os.remove(zp)
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
    pdf.cell(0, 8, "Диаграммы, схемы и описание слайдов", align="C",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("DejaVu", "", 10)
    pdf.set_text_color(100, 100, 100)
    for line in [
        "Этот документ содержит:",
        "• Диаграмму Use Case (варианты использования)",
        "• Диаграмму классов (Class Diagram)",
        "• Диаграмму объектов (Object Diagram)",
        "• Схему пайплайна обработки текста",
        "• Схему архитектуры проекта",
        "• Подробное описание каждого слайда с готовым текстом",
    ]:
        pdf.cell(0, 7, line, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 7, "МГТУ им. Н.Э. Баумана, кафедра ИУ10, группа ИУ10-44",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, "Осипова П.С., Селина М.А. | Преподаватель: Буркацкий К.А.",
             align="C", new_x="LMARGIN", new_y="NEXT")

    # ================================================================
    #                    1. USE CASE ДИАГРАММА
    # ================================================================
    pdf.add_page()
    pdf.section_title("1. Диаграмма Use Case (варианты использования)")
    pdf.body(
        "Показывает, что может делать пользователь с системой. "
        "Эту диаграмму можно вставить в отчёт и/или на отдельный слайд."
    )
    pdf.ln(2)

    # Рисуем Use Case
    # Актёр — слева
    actor_x, actor_y = 30, 105
    # Рисуем человечка
    pdf.set_draw_color(30, 60, 120)
    pdf.set_line_width(0.6)
    # голова
    pdf.ellipse(actor_x - 4, actor_y - 8, 8, 8, "D")
    # тело
    pdf.line(actor_x, actor_y, actor_x, actor_y + 15)
    # руки
    pdf.line(actor_x - 8, actor_y + 5, actor_x + 8, actor_y + 5)
    # ноги
    pdf.line(actor_x, actor_y + 15, actor_x - 6, actor_y + 23)
    pdf.line(actor_x, actor_y + 15, actor_x + 6, actor_y + 23)
    pdf._label(actor_x - 12, actor_y + 24, "Пользователь", 9, (30, 60, 120))

    # Системная рамка
    sys_x, sys_y, sys_w, sys_h = 65, 65, 125, 125
    pdf.set_draw_color(30, 60, 120)
    pdf.set_line_width(0.5)
    pdf.rect(sys_x, sys_y, sys_w, sys_h, "D")
    pdf.set_font("DejaVu", "B", 10)
    pdf.set_text_color(30, 60, 120)
    pdf.set_xy(sys_x, sys_y + 2)
    pdf.cell(sys_w, 8, "Система NLP-Emo-01", align="C")

    # Use Cases — эллипсы
    cases = [
        (130, 85, "Ввести текст"),
        (130, 105, "Получить эмоцию"),
        (130, 125, "Вызвать /help"),
        (130, 145, "Вызвать /exit"),
        (130, 165, "Обучить модель"),
    ]
    for cx, cy, label in cases:
        pdf._ellipse(cx, cy, 42, 8, label,
                     fill_color=(230, 240, 255), border_color=(30, 60, 120))
        # линия от актёра к use case
        pdf._line_to(actor_x + 8, actor_y + 5, cx - 42, cy)

    # «include» связь между "Ввести текст" и "Получить эмоцию"
    pdf._dashed_line(130, 93, 130, 97)
    pdf._label(132, 93, "«include»", 7, (100, 100, 100))

    pdf.set_y(200)
    pdf.ln(3)
    pdf.sub_title("Описание вариантов использования")
    pdf.bold_bullet("Ввести текст — ", "пользователь вводит произвольный текст "
                    "на русском языке (до 1000 символов)")
    pdf.bold_bullet("Получить эмоцию — ", "система возвращает метку эмоции "
                    "(одну из 10) и уверенность в процентах")
    pdf.bold_bullet("Вызвать /help — ", "система показывает справку: список "
                    "эмоций, доступные команды")
    pdf.bold_bullet("Вызвать /exit — ", "корректное завершение работы программы")
    pdf.bold_bullet("Обучить модель — ", "запуск обучения (train.py или "
                    "train_bert.py) перед первым использованием")

    # ================================================================
    #                    2. CLASS DIAGRAM
    # ================================================================
    pdf.add_page()
    pdf.section_title("2. Диаграмма классов (Class Diagram)")
    pdf.body(
        "Показывает основные классы и модули проекта и связи между ними."
    )
    pdf.ln(1)

    # ---- Классы ----
    box_h = 50
    # Ряд 1
    # DataLoader
    pdf._box(12, 60, 55, 12, "data_loader", (200, 220, 255), bold=True)
    pdf._box(12, 72, 55, 8, "load_data()", (240, 245, 255), font_size=7)
    pdf._box(12, 80, 55, 8, "split_data()", (240, 245, 255), font_size=7)
    pdf._box(12, 88, 55, 8, "load_local_file()", (240, 245, 255), font_size=7)

    # Preprocessing
    pdf._box(75, 60, 55, 12, "preprocessing", (200, 220, 255), bold=True)
    pdf._box(75, 72, 55, 8, "preprocess(text)", (240, 245, 255), font_size=7)
    pdf._box(75, 80, 55, 8, "_morph: MorphAnalyzer", (240, 245, 255), font_size=7)
    pdf._box(75, 88, 55, 8, "_stopwords: set", (240, 245, 255), font_size=7)

    # Vectorizer
    pdf._box(138, 60, 60, 12, "vectorizer", (200, 220, 255), bold=True)
    pdf._box(138, 72, 60, 8, "train_vectorizer()", (240, 245, 255), font_size=7)
    pdf._box(138, 80, 60, 8, "load_vectorizer()", (240, 245, 255), font_size=7)
    pdf._box(138, 88, 60, 8, "transform()", (240, 245, 255), font_size=7)

    # Ряд 2
    # Model (ML)
    pdf._box(12, 110, 55, 12, "model", (255, 230, 200), bold=True)
    pdf._box(12, 122, 55, 8, "train_model()", (255, 245, 230), font_size=7)
    pdf._box(12, 130, 55, 8, "predict_single()", (255, 245, 230), font_size=7)
    pdf._box(12, 138, 55, 8, "save/load_model()", (255, 245, 230), font_size=7)

    # BertModel
    pdf._box(75, 110, 55, 12, "bert_model", (255, 230, 200), bold=True)
    pdf._box(75, 122, 55, 8, "EmotionClassifier", (255, 245, 230), font_size=7)
    pdf._box(75, 130, 55, 8, "train_bert()", (255, 245, 230), font_size=7)
    pdf._box(75, 138, 55, 8, "predict_single_bert()", (255, 245, 230), font_size=7)
    pdf._box(75, 146, 55, 8, "save/load_bert()", (255, 245, 230), font_size=7)

    # Evaluate
    pdf._box(138, 110, 60, 12, "evaluate", (220, 255, 220), bold=True)
    pdf._box(138, 122, 60, 8, "evaluate_multilabel()", (240, 255, 240), font_size=7)
    pdf._box(138, 130, 60, 8, "evaluate_top1()", (240, 255, 240), font_size=7)
    pdf._box(138, 138, 60, 8, "compute_hit_rate()", (240, 255, 240), font_size=7)

    # Ряд 3 — CLI
    pdf._box(50, 168, 110, 12, "cli", (255, 220, 220), bold=True)
    pdf._box(50, 180, 110, 8, "run_cli(use_bert)", (255, 240, 240), font_size=7)
    pdf._box(50, 188, 110, 8, "HELP_TEXT, MAX_TEXT_LENGTH=1000", (255, 240, 240), font_size=7)

    # Стрелки связей
    # cli -> model
    pdf._line_to(50, 185, 40, 146)
    # cli -> bert_model
    pdf._line_to(105, 180, 102, 154)
    # cli -> preprocessing
    pdf._line_to(80, 168, 102, 96)
    # cli -> vectorizer
    pdf._line_to(140, 168, 168, 96)
    # model -> data_loader
    pdf._line_to(40, 110, 40, 96)
    # bert_model -> data_loader
    pdf._line_to(80, 110, 45, 96)

    # Легенда
    pdf.set_y(205)
    pdf.sub_title("Описание модулей")
    pdf.bold_bullet("data_loader — ", "загрузка данных из Hugging Face или "
                    "локального CSV/JSON, разбиение 80/20")
    pdf.bold_bullet("preprocessing — ", "предобработка текста: lowercase, "
                    "пунктуация, стоп-слова, лемматизация")
    pdf.bold_bullet("vectorizer — ", "TF-IDF векторизация, сохранение/загрузка "
                    "обученного векторизатора")
    pdf.bold_bullet("model — ", "классические ML-модели (LogReg, RandomForest), "
                    "обёрнуты в OneVsRest")
    pdf.bold_bullet("bert_model — ", "BERT-классификатор (EmotionClassifier), "
                    "обучение, сохранение, инференс")
    pdf.bold_bullet("evaluate — ", "расчёт метрик: Accuracy, Precision, Recall, "
                    "F1, Confusion Matrix")
    pdf.bold_bullet("cli — ", "консольный интерфейс: ввод текста, вывод эмоции, "
                    "обработка команд и ошибок")

    # ================================================================
    #               3. ДИАГРАММА ОБЪЕКТОВ
    # ================================================================
    pdf.add_page()
    pdf.section_title("3. Диаграмма объектов (Object Diagram)")
    pdf.body(
        "Показывает конкретные объекты в момент работы программы — "
        "когда пользователь вводит текст и получает результат."
    )
    pdf.ln(1)

    # Объекты
    y0 = 70
    # Входной текст
    pdf._box(12, y0, 85, 10, 'text : str', (255, 255, 200), (180, 160, 0), bold=True)
    pdf._box(12, y0+10, 85, 8, '= "Меня это бесит, я в ярости!"',
             (255, 255, 230), (180, 160, 0), font_size=7)

    # Preprocessed
    pdf._box(110, y0, 85, 10, 'processed : str', (255, 255, 200), (180, 160, 0), bold=True)
    pdf._box(110, y0+10, 85, 8, '= "бесить ярость"',
             (255, 255, 230), (180, 160, 0), font_size=7)
    pdf._arrow_right(97, y0+9, 110)

    # Vectorizer
    y1 = y0 + 30
    pdf._box(12, y1, 85, 10, 'vectorizer : TfidfVectorizer', (200, 220, 255), bold=True, font_size=8)
    pdf._box(12, y1+10, 85, 8, 'max_features=10000', (240, 245, 255), font_size=7)
    pdf._box(12, y1+18, 85, 8, 'ngram_range=(1, 2)', (240, 245, 255), font_size=7)

    # X vector
    pdf._box(110, y1, 85, 10, 'X : sparse matrix', (200, 220, 255), bold=True, font_size=8)
    pdf._box(110, y1+10, 85, 8, 'shape=(1, 10000)', (240, 245, 255), font_size=7)
    pdf._arrow_right(97, y1+9, 110)
    pdf._arrow_down(55, y0+18, y1)

    # Model
    y2 = y1 + 38
    pdf._box(12, y2, 85, 10, 'model : OneVsRestClassifier', (255, 230, 200), bold=True, font_size=8)
    pdf._box(12, y2+10, 85, 8, 'base: LogisticRegression', (255, 245, 230), font_size=7)
    pdf._box(12, y2+18, 85, 8, 'n_labels=10', (255, 245, 230), font_size=7)
    pdf._arrow_down(55, y1+26, y2)

    # Result
    pdf._box(110, y2, 85, 10, 'result', (220, 255, 220), (30, 130, 30), bold=True)
    pdf._box(110, y2+10, 85, 8, 'emotion_ru = "гнев"', (240, 255, 240), (30, 130, 30), font_size=7)
    pdf._box(110, y2+18, 85, 8, 'confidence = 92.0', (240, 255, 240), (30, 130, 30), font_size=7)
    pdf._arrow_right(97, y2+14, 110)

    pdf.set_y(y2 + 35)
    pdf.body(
        "Диаграмма показывает конкретный пример: текст «Меня это бесит, "
        "я в ярости!» проходит через предобработку, векторизуется в "
        "разреженную матрицу размером (1, 10000), подаётся в модель "
        "OneVsRestClassifier, которая возвращает результат: «гнев», 92%."
    )

    # ================================================================
    #               4. СХЕМА ПАЙПЛАЙНА (ДЕТАЛЬНАЯ)
    # ================================================================
    pdf.add_page()
    pdf.section_title("4. Схема пайплайна обработки текста (детальная)")
    pdf.body(
        "Подробная схема, показывающая оба пути обработки: "
        "через TF-IDF и через BERT."
    )
    pdf.ln(1)

    # Входной текст
    y = 70
    cx = 105
    bw = 80
    pdf._box(cx - bw//2, y, bw, 12, "Текст пользователя",
             (255, 240, 200), (200, 150, 50), bold=True)

    # Предобработка
    y += 20
    pdf._arrow_down(cx, y - 8, y)
    pdf._box(cx - bw//2, y, bw, 12, "Предобработка",
             (220, 235, 255), bold=True)
    # Детали справа
    pdf._label(cx + bw//2 + 5, y, "lowercase", 8)
    pdf._label(cx + bw//2 + 5, y + 5, "удаление пунктуации", 8)
    pdf._label(cx + bw//2 + 5, y + 10, "стоп-слова (NLTK)", 8)
    pdf._label(cx + bw//2 + 5, y + 15, "лемматизация (pymorphy2)", 8)

    # Развилка
    y += 22
    pdf._arrow_down(cx, y - 10, y)
    pdf._label(cx - 10, y, "Выбор метода", 8, (30, 60, 120))

    # Левая ветка — TF-IDF
    left_x = 50
    y_branch = y + 12

    pdf._line_to(cx, y + 5, left_x, y_branch)
    pdf._box(left_x - 35, y_branch, 70, 12, "TF-IDF Векторизация",
             (200, 220, 255), bold=True, font_size=8)

    y_model_l = y_branch + 20
    pdf._arrow_down(left_x, y_branch + 12, y_model_l)
    pdf._box(left_x - 35, y_model_l, 70, 12, "LogReg / RandomForest",
             (255, 230, 200), bold=True, font_size=8)

    # Правая ветка — BERT
    right_x = 160
    pdf._line_to(cx, y + 5, right_x, y_branch)
    pdf._box(right_x - 35, y_branch, 70, 12, "BERT Tokenizer",
             (200, 220, 255), bold=True, font_size=8)

    y_model_r = y_branch + 20
    pdf._arrow_down(right_x, y_branch + 12, y_model_r)
    pdf._box(right_x - 35, y_model_r, 70, 12, "BERT Classifier",
             (255, 230, 200), bold=True, font_size=8)

    # Объединение
    y_merge = y_model_l + 20
    pdf._arrow_down(left_x, y_model_l + 12, y_merge)
    pdf._arrow_down(right_x, y_model_r + 12, y_merge)
    pdf._line_to(left_x, y_merge, right_x, y_merge)
    pdf._arrow_down(cx, y_merge, y_merge + 8)

    y_result = y_merge + 8
    pdf._box(cx - bw//2, y_result, bw, 12, "Эмоция + Confidence (%)",
             (220, 255, 220), (30, 130, 30), bold=True, font_size=9)

    pdf.set_y(y_result + 20)
    pdf.body(
        "Оба пути ведут к одному результату: метка эмоции + уверенность. "
        "TF-IDF — быстрый, но менее точный путь. BERT — медленнее, "
        "но понимает контекст и даёт лучшие результаты."
    )

    # ================================================================
    #               5. АРХИТЕКТУРА ПРОЕКТА (ФАЙЛЫ)
    # ================================================================
    pdf.add_page()
    pdf.section_title("5. Схема архитектуры проекта (модули и файлы)")
    pdf.body(
        "Показывает, какие файлы за что отвечают и как связаны."
    )
    pdf.ln(1)

    # Три уровня
    # Уровень 1 — Точки входа
    pdf._box(15, 65, 40, 10, "main.py", (255, 220, 220), (180, 50, 50), bold=True, font_size=8)
    pdf._box(60, 65, 40, 10, "train.py", (255, 220, 220), (180, 50, 50), bold=True, font_size=8)
    pdf._box(105, 65, 46, 10, "train_bert.py", (255, 220, 220), (180, 50, 50), bold=True, font_size=8)
    pdf._box(156, 65, 42, 10, "train_bert_sl.py", (255, 220, 220), (180, 50, 50), bold=True, font_size=7)
    pdf._label(70, 56, "Точки входа (запуск)", 9, (180, 50, 50))

    # Уровень 2 — Модули src/
    pdf._label(75, 85, "Модули обработки (src/)", 9, (30, 60, 120))
    mods = [
        (15, 95, 38, "cli.py"),
        (57, 95, 38, "model.py"),
        (99, 95, 42, "bert_model.py"),
        (145, 95, 52, "preprocessing.py"),
    ]
    for mx, my, mw, ml in mods:
        pdf._box(mx, my, mw, 10, ml, (200, 220, 255), bold=True, font_size=7)

    mods2 = [
        (15, 110, 38, "evaluate.py"),
        (57, 110, 38, "vectorizer.py"),
        (99, 110, 42, "data_loader.py"),
    ]
    for mx, my, mw, ml in mods2:
        pdf._box(mx, my, mw, 10, ml, (200, 220, 255), bold=True, font_size=7)

    # Стрелки от точек входа к модулям
    pdf._arrow_down(35, 75, 95)   # main -> cli
    pdf._arrow_down(80, 75, 95)   # train -> model
    pdf._arrow_down(128, 75, 95)  # train_bert -> bert_model

    # Уровень 3 — Данные и модели
    pdf._label(65, 128, "Данные и сохранённые модели", 9, (30, 130, 30))
    pdf._box(15, 138, 55, 10, "models/*.pkl, *.pt", (220, 255, 220), (30, 130, 30), font_size=7, bold=True)
    pdf._box(75, 138, 55, 10, "data/ (CSV/JSON)", (220, 255, 220), (30, 130, 30), font_size=7, bold=True)
    pdf._box(135, 138, 60, 10, "HuggingFace (remote)", (220, 255, 220), (30, 130, 30), font_size=7, bold=True)

    pdf._arrow_down(76, 120, 138)  # vectorizer -> models
    pdf._arrow_down(120, 120, 138)  # data_loader -> data

    pdf.set_y(158)
    pdf.sub_title("Связи между модулями")
    pdf.bold_bullet("main.py → cli.py → ", "model.py или bert_model.py "
                    "(в зависимости от флага --bert)")
    pdf.bold_bullet("train.py → ", "data_loader → preprocessing → vectorizer "
                    "→ model → evaluate")
    pdf.bold_bullet("train_bert.py → ", "data_loader → bert_model → evaluate")
    pdf.bold_bullet("cli.py → ", "preprocessing + vectorizer + model (TF-IDF) "
                    "ИЛИ bert_model (BERT)")

    # ================================================================
    #           6. ПОДРОБНОЕ ОПИСАНИЕ КАЖДОГО СЛАЙДА
    # ================================================================
    pdf.add_page()
    pdf.section_title("6. Подробное описание каждого слайда")
    pdf.body(
        "Для каждого слайда: заголовок, содержание (можно копировать), "
        "какие картинки/диаграммы вставить, и что говорить при защите."
    )

    # ---- СЛАЙД 1 ----
    pdf.slide_header(1, "ТИТУЛЬНЫЙ")
    pdf.body("Заголовок: «Распознавание эмоций по тексту»")
    pdf.bullet("Шифр проекта: NLP-Emo-01")
    pdf.bullet("МГТУ им. Н.Э. Баумана, кафедра ИУ10, группа ИУ10-44")
    pdf.bullet("Исполнители: Осипова П.С., Селина М.А.")
    pdf.bullet("Преподаватель: Буркацкий К.А.")
    pdf.bullet("2025/2026 учебный год")
    pdf.hint("Стандартный титульный слайд. Никаких картинок.")

    # ---- СЛАЙД 2 ----
    pdf.slide_header(2, "ПОСТАНОВКА ЗАДАЧИ")
    pdf.body("Заголовок: «Постановка задачи»\n\nТекст на слайде:")
    pdf.body(
        "Цель: разработать программу для автоматического определения "
        "эмоциональной окраски текста на русском языке."
    )
    pdf.body("Принцип работы:")
    pdf.num_bullet(1, "Пользователь вводит текст на русском языке")
    pdf.num_bullet(2, "Программа выполняет предобработку и классификацию")
    pdf.num_bullet(3, "Выводит метку эмоции и уверенность (%)")
    pdf.body("Пример:")
    pdf.code_block(
        'Ввод:  «Меня это бесит, я в ярости!»\n'
        'Вывод: Эмоция: гнев, Уверенность: 92%')
    pdf.hint(
        "Говори: «Задача — классификация текста по эмоциям. "
        "10 классов эмоций, multi-label разметка.»")

    # ---- СЛАЙД 3 ----
    pdf.slide_header(3, "ОБЛАСТЬ ПРИМЕНЕНИЯ")
    pdf.body("Заголовок: «Область применения»\n\nТекст:")
    pdf.bullet("Анализ тональности в соцсетях и системах обратной связи")
    pdf.bullet("Поддержка чат-ботов и систем мониторинга тональности")
    pdf.bullet("Учебно-исследовательские цели (курсовые и дипломы по NLP)")

    # ---- СЛАЙД 4 ----
    pdf.add_page()
    pdf.slide_header(4, "ДАТАСЕТ")
    pdf.body("Заголовок: «Датасет: ru-izard-emotions»\n\nТекст:")
    pdf.bullet("Источник: Hugging Face (автор Djacon)")
    pdf.bullet("~25 000 текстов на русском языке")
    pdf.bullet("10 классов эмоций по модели Изарда")
    pdf.bullet("Multi-label: один текст может иметь несколько эмоций")
    pdf.bullet("Разбиение: 80/20, seed=42")
    pdf.ln(1)
    pdf.body("Таблица эмоций:")
    w = [50, 50]
    pdf.table_row(["Русский", "English"], w, header=True)
    for ru, en in [("Радость", "joy"), ("Грусть", "sadness"),
                   ("Гнев", "anger"), ("Страх", "fear"),
                   ("Удивление", "surprise"), ("Отвращение", "disgust"),
                   ("Воодушевление", "enthusiasm"), ("Вина", "guilt"),
                   ("Стыд", "shame"), ("Нейтральность", "neutral")]:
        pdf.table_row([ru, en], w)

    # ---- СЛАЙД 5 ----
    pdf.slide_header(5, "ПАЙПЛАЙН ОБРАБОТКИ")
    pdf.body(
        "Заголовок: «Архитектура: пайплайн обработки текста»\n\n"
        "Вставь сюда схему из раздела 4 этого документа (стр. 4) — "
        "блок-схема с двумя ветками (TF-IDF и BERT)."
    )
    pdf.body("Или упрощённая версия — 5 блоков со стрелками:")
    pdf.code_block(
        "[Текст] → [Предобработка] → [Векторизация] → "
        "[Классификация] → [Эмоция + %]")
    pdf.hint(
        "Это ключевой слайд. Говори: «Текст проходит 4 этапа обработки. "
        "Сначала чистим от шума, потом превращаем в числа, подаём "
        "на вход модели, получаем результат.»")

    # ---- СЛАЙД 6 ----
    pdf.slide_header(6, "ПРЕДОБРАБОТКА ТЕКСТА")
    pdf.body("Заголовок: «Предобработка текста»\n\n4 этапа:")
    pdf.num_bullet(1, "Lowercase — приведение к нижнему регистру")
    pdf.num_bullet(2, "Удаление знаков препинания и спецсимволов")
    pdf.num_bullet(3, "Удаление стоп-слов (NLTK, русский язык)")
    pdf.num_bullet(4, "Лемматизация (pymorphy2) — «бесит» → «бесить»")
    pdf.body("Пример трансформации:")
    pdf.code_block(
        '«Меня это бесит, я в ярости!»\n'
        '  → lowercase → без пунктуации → без стоп-слов\n'
        '  → лемматизация → «бесить ярость»')
    pdf.hint("«Предобработка убирает шум. Модели проще работать с леммами.»")

    # ---- СЛАЙД 7 ----
    pdf.add_page()
    pdf.slide_header(7, "МОДЕЛИ КЛАССИФИКАЦИИ")
    pdf.body("Заголовок: «Модели классификации»\n\nДва блока:")
    pdf.body("Baseline (простая модель):")
    pdf.bullet("TF-IDF → LogisticRegression (OneVsRest)")
    pdf.bullet("Быстро обучается, но невысокая точность")
    pdf.body("Основная (нейросеть):")
    pdf.bullet("BERT (rubert-tiny2) — трансформер для русского языка")
    pdf.bullet("Fine-tuning на наших данных")
    pdf.bullet("Понимает контекст → лучше по метрикам")
    pdf.hint("«BERT учитывает порядок и контекст слов, а TF-IDF — нет.»")

    # ---- СЛАЙД 8 ----
    pdf.slide_header(8, "РЕЗУЛЬТАТЫ")
    pdf.body("Заголовок: «Результаты: сравнение моделей»\n\nТаблица:")
    w3 = [55, 40, 50]
    pdf.table_row(["Метрика", "TF-IDF+LogReg", "BERT"], w3, header=True)
    pdf.table_row(["F1-score (macro)", "0.29", "0.49"], w3)
    pdf.table_row(["Top-1 Accuracy", "44.6%", "47.1%"], w3)
    pdf.table_row(["Recall (macro)", "0.20", "0.43"], w3)
    pdf.ln(1)
    pdf.body(
        "Вставь картинку: models/confusion_matrix_bert_single.png\n"
        "Вывод: BERT лучше baseline по всем метрикам.")
    pdf.hint(
        "«F1 у BERT 0.49 против 0.29 — почти вдвое лучше. "
        "Confusion Matrix показывает, какие эмоции путаются.»")

    # ---- СЛАЙД 9 ----
    pdf.slide_header(9, "ДЕМОНСТРАЦИЯ")
    pdf.body(
        "Заголовок: «Демонстрация работы»\n\n"
        "Вставь скриншот консоли (python3 main.py --bert).")
    pdf.code_block(
        'Введите текст: Меня это бесит, я в ярости!\n'
        '  Эмоция: гнев\n'
        '  Уверенность: 92%\n\n'
        'Введите текст: Какой прекрасный день!\n'
        '  Эмоция: радость\n'
        '  Уверенность: 78%')
    pdf.hint("Если можно — сделай живую демо на защите.")

    # ---- СЛАЙД 10 ----
    pdf.slide_header(10, "СТЕК ТЕХНОЛОГИЙ")
    pdf.body("Заголовок: «Стек технологий»\n\nТаблица из 3 колонок:")
    w3t = [40, 48, 95]
    pdf.table_row(["Назначение", "Технология", "Зачем"], w3t, header=True)
    rows = [
        ("Язык", "Python 3.8+", "Основной язык"),
        ("NLP", "NLTK", "Стоп-слова русского языка"),
        ("NLP", "pymorphy2", "Лемматизация"),
        ("NLP", "re (regex)", "Удаление пунктуации"),
        ("Векторизация", "scikit-learn", "TF-IDF: текст -> вектор"),
        ("Векторизация", "Transformers", "BERT-эмбеддинги (rubert-tiny2)"),
        ("ML-модели", "scikit-learn", "LogReg, RandomForest, метрики"),
        ("Нейросеть", "PyTorch", "Обучение BERT"),
        ("Данные", "pandas", "Таблицы данных"),
        ("Данные", "HF Datasets", "Загрузка датасета"),
        ("Графики", "matplotlib", "Confusion Matrix"),
        ("Сохранение", "joblib/torch", "Модели (.pkl, .pt)"),
    ]
    for r in rows:
        pdf.table_row(list(r), w3t)
    pdf.hint(
        "«Не просто набор библиотек — каждая решает конкретную задачу "
        "в пайплайне.»")

    # ---- СЛАЙД 11 ----
    pdf.add_page()
    pdf.slide_header(11, "ВЫВОДЫ")
    pdf.body("Заголовок: «Выводы»\n\nТекст (4 пункта):")
    pdf.num_bullet(1, "Разработана программа классификации эмоций на русском языке")
    pdf.num_bullet(2, "Реализованы два подхода: TF-IDF+LogReg и BERT (rubert-tiny2)")
    pdf.num_bullet(3, "BERT: F1=0.49, вдвое лучше baseline (0.29)")
    pdf.num_bullet(4, "Все требования ТЗ выполнены")
    pdf.hint(
        "«Трансформеры превосходят классику на задаче эмоций. "
        "Программа соответствует ТЗ и готова к эксплуатации.»")

    # ================================================================
    #           7. ДИАГРАММЫ ДЛЯ ОТЧЁТА — СВОДКА
    # ================================================================
    pdf.section_title("7. Какие диаграммы вставить в отчёт")
    pdf.body("В отчёт (пояснительную записку) нужно вставить:")
    pdf.ln(1)
    pdf.num_bullet(1,
        "Use Case диаграмма (стр. 2) — раздел «Функциональное назначение»")
    pdf.num_bullet(2,
        "Class Diagram (стр. 3) — раздел «Архитектура программы»")
    pdf.num_bullet(3,
        "Object Diagram (стр. 4) — раздел «Пример работы программы»")
    pdf.num_bullet(4,
        "Схема пайплайна (стр. 5) — раздел «Алгоритм обработки»")
    pdf.num_bullet(5,
        "Архитектура файлов (стр. 5) — раздел «Структура проекта»")
    pdf.num_bullet(6,
        "Confusion Matrix (файл models/confusion_matrix_bert_single.png) "
        "— раздел «Результаты»")
    pdf.ln(2)
    pdf.body(
        "Все диаграммы из этого документа можно использовать как есть — "
        "сделай скриншот нужной страницы и вставь в отчёт или презентацию."
    )

    # ===== Сохранение =====
    pdf.output(OUTPUT_PATH)
    print(f"PDF сохранён: {OUTPUT_PATH}")


if __name__ == "__main__":
    build_pdf()
