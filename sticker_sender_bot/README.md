# Sticker Sender Bot

Простой Telegram-бот на `Telethon`, который бесконечно отправляет случайные стикеры в указанную группу.

## Что нужно

- Python 3.10+
- Доступ к Telegram API
- Бот уже должен иметь доступ в целевую группу

## Установка

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Запуск

```bash
python bot.py
```

## Настройка

Параметры находятся в начале файла `bot.py`:

- `API_ID`
- `API_HASH`
- `BOT_TOKEN`
- `GROUP_LINK`
- `SEND_INTERVAL_SECONDS`

Если инвайт-ссылка недоступна для бота, замените `GROUP_LINK` на числовой `chat_id`/`@username`.
