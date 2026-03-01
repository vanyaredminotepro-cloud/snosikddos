# Sticker Sender Bot

Простой Telegram-бот, который бесконечно отправляет случайные стикеры в группу.

## Почему прошлый вариант падал

Ваши строки `CAACAg...` — это Bot API `file_id`. Telethon (MTProto-клиент) не обязан принимать такие идентификаторы как `send_file`, поэтому и возникала ошибка `Not ... a valid bot-API-like file ID`.

В этом проекте отправка сделана через **Telegram Bot API** (`sendSticker`), где эти `file_id` работают корректно.

## Что нужно

- Python 3.10+
- Бот уже добавлен в группу
- В `bot.py` задан `GROUP_CHAT_ID` (например `-1001234567890`)

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

## Настройка (`bot.py`)

- `BOT_TOKEN`
- `GROUP_CHAT_ID` (**обязательно**)
- `SEND_INTERVAL_SECONDS`
- `REQUEST_TIMEOUT_SECONDS`

`GROUP_LINK` оставлен как справочное поле и не используется для резолва чата.
