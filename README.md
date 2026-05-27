# ⬡ EncoderLab

Инструмент для кодирования и декодирования текста с 18 алгоритмами. Доступен в двух версиях — графический интерфейс (GUI) и интерфейс командной строки (CLI).

---

## Алгоритмы

| Категория | Алгоритмы |
|---|---|
| Кодировки символов | UTF-8 Hex, UTF-16 Hex, UTF-32 Hex, ASCII Hex, CP1251 Hex |
| Base-кодирование | Base64, Base64 URL, Base32, Base16 (HEX) |
| Числовые представления | Binary, Octal, Unicode Escape |
| Веб-кодирование | URL Encoding, HTML Entities |
| Классические шифры | ROT13, Morse, Caesar (shift 13), Atbash |

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
├── encoder_engine.py   # Ядро — все 18 алгоритмов
├── encoder_gui.py      # Графический интерфейс (tkinter)
├── encoder_cli.py      # Интерфейс командной строки
└── README.md
```

---

