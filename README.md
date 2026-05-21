# Telegram Auto Sender

Автоматическая рассылка объявлений в Telegram чаты каждые 4 часа.

---

## 📁 Файлы

- `sender.py` — основной скрипт рассылки
- `auth.py` — одноразовый скрипт для получения сессии
- `requirements.txt` — зависимости
- `.github/workflows/send.yml` — расписание

---

## 🚀 Пошаговая инструкция

### Шаг 1 — Получи API ключи Telegram

1. Зайди на **https://my.telegram.org**
2. Войди со своим номером телефона
3. Нажми **"API development tools"**
4. Заполни форму (App title: любое, Short name: любое)
5. Скопируй **App api_id** (число) и **App api_hash** (строка)

---

### Шаг 2 — Установи Python и получи строку сессии

**На Windows:**
1. Скачай Python с **python.org** → установи
2. Скачай файл `auth.py` на компьютер
3. Открой командную строку (Win+R → cmd)
4. Выполни команды:
```
pip install telethon
python auth.py
```
5. Введи API_ID и API_HASH когда попросит
6. Войди в Telegram (введи номер телефона и код из приложения)
7. Скопируй длинную строку сессии которую выдаст скрипт

---

### Шаг 3 — Создай GitHub репозиторий

1. Зайди на **github.com** → создай новый **приватный** репозиторий
2. Загрузи все файлы (кроме `auth.py` — он больше не нужен)
3. Убедись что `send.yml` лежит в папке `.github/workflows/`

---

### Шаг 4 — Добавь секреты

**Settings → Secrets and variables → Actions → New repository secret**

| Имя секрета  | Значение                        |
|--------------|---------------------------------|
| `TG_API_ID`  | числовой ID с my.telegram.org   |
| `TG_API_HASH`| хэш с my.telegram.org           |
| `TG_SESSION` | длинная строка из auth.py       |

---

### Шаг 5 — Настрой объявления и чаты

Открой `sender.py` и отредактируй:

**Объявления:**
```python
MESSAGE_EXPERIENCED = """твой текст для опытных"""
MESSAGE_BEGINNERS   = """твой текст для новичков"""
```

**Списки чатов** (username без @ или числовой ID):
```python
CHATS_EXPERIENCED = ["chat1", "chat2", "chat3"]
CHATS_BEGINNERS   = ["chat4", "chat5", "chat6"]
```

---

### Шаг 6 — Тест

**Actions → Telegram Sender → Run workflow**

---

## ⚠️ Важно

- Используй **отдельный аккаунт**, не основной
- Пауза между чатами — 45 секунд (не убирай!)
- Если аккаунт получит ограничения — создай новый и повтори Шаг 2
