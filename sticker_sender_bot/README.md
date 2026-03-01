# Sticker Sender Bot

Простой Telegram-бот на `Telethon`, который бесконечно отправляет случайные стикеры в указанную группу.

## Что нужно

- Python 3.10+
- Доступ к Telegram API
- Бот добавлен в целевую группу

## Важно про ссылки `t.me/+...`

Бот-аккаунты **не могут** вступать в группы через приватные invite-ссылки (`https://t.me/+...`) через MTProto API.
Поэтому для приватной группы:

1. Добавьте бота в группу вручную.
2. Укажите `GROUP_CHAT_ID = -100...` в `bot.py`.

Для публичной группы можно использовать `@username` или `https://t.me/<username>`.

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
- `GROUP_CHAT_ID`
- `SEND_INTERVAL_SECONDS`
