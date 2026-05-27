

Инструмент для кодирования и декодирования текста с 18 алгоритмами. Доступен в двух версиях — графический интерфейс (GUI) и интерфейс командной строки (CLI).

---

## Требования

- Python **3.8** и выше
- Библиотека `cryptography`

---

## Установка

**1. Клонировать репозиторий**

```bash
git clone https://github.com/your-username/encoderlab.git
cd encoderlab
```

**2. (Опционально) Создать виртуальное окружение**

```bash
python -m venv venv
```

Активировать:

- macOS / Linux:
```bash
source venv/bin/activate
```
- Windows:
```bash
venv\Scripts\activate
```

**3. Установить зависимости**

```bash
pip install cryptography
```

---

## Запуск

**GUI-версия**

```bash
python encoder_gui.py
```

**CLI-версия**

```bash
python encoder_cli.py
```

---

## Структура файлов

```
encoderlab/
├── encoder_engine.py   
├── encoder_gui.py      # Графический интерфейс (tkinter)
├── encoder_cli.py      # Интерфейс командной строки
└── README.md
```

---

