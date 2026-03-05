# Sticker Sender Bot

Теперь проект поддерживает **два режима**:

1. `session` — отправка стикеров через пользовательскую сессию Telethon (вход: номер, код, 2FA-пароль).
2. `bot_api` — отправка стикеров через Bot API (`sendSticker`) по `file_id` вида `CAAC...`.

## Главное, что вы просили

В `bot.py` добавлено интерактивное меню:

- `1` — подключить/обновить сессию (ввод номера, кода, пароля 2FA)
- `2` — запуск отправки через сессию
- `3` — запуск отправки через bot api

Сессия сохраняется в файле `<SESSION_NAME>.session`.

## Настройка `session` режима

В `bot.py`:

- `API_ID`
- `API_HASH`
- `SESSION_NAME`
- `TARGET_CHAT` (`-100...`, `@username` или `https://t.me/username`)
- `STICKER_SET_SHORT_NAME` (short_name стикерпака, например из `https://t.me/addstickers/<short_name>`)

> Важно: в режиме сессии используются стикеры из `STICKER_SET_SHORT_NAME`.
> Bot API `file_id` (`CAAC...`) для Telethon-сессии не нужен.

## Настройка `bot_api` режима

- `BOT_TOKEN`
- `GROUP_CHAT_ID` (или `None` для автоопределения через `getUpdates`)
- `STICKERS` (только валидные `file_id` вида `CAAC...`)

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

## Типичные проблемы

- Пользователи не могут отправлять стикеры в группе:
  проверьте права группы/пользователей (обычно ограничено `can_send_other_messages`).
- Ошибка входа по сессии:
  убедитесь, что правильно введены номер, код и 2FA-пароль.
- Ошибка стикерпака:
  проверьте `STICKER_SET_SHORT_NAME`.
