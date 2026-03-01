import asyncio
import random
import time
from typing import Any

import requests
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.types import InputStickerSetShortName

# === НАСТРОЙКИ ===
MODE = "session"  # "session" или "bot_api"

# Для режима session (пользовательская сессия)
API_ID = 23695534
API_HASH = "08f5b069bb4fd8505b98a6b57f857868"
SESSION_NAME = "user_sender"
TARGET_CHAT: int | str = "@your_group_username"  # можно -100..., @username, t.me/username
STICKER_SET_SHORT_NAME = "TgEmoji"

# Для режима bot_api
BOT_TOKEN = "8779722671:AAHD1Dj5guQA3nRU504y4lTtqOsc7m4YYCA"
GROUP_LINK = "https://t.me/+vuft45R2wW1kNjFi"  # только для справки
GROUP_CHAT_ID: int | None = None

SEND_INTERVAL_SECONDS = 5
REQUEST_TIMEOUT_SECONDS = 30
# =================

# Bot API file_id (только для MODE="bot_api")
STICKERS = [
    "CAACAgIAAxkBAAEQpN5poyqxZEIu0ckIDNuBjXQhJx_HdAACVpcAAg5nGUkME8ZzJeb0CDoE",
    "CAACAgIAAxkBAAEQpOBpoyqzX4T9RbGlTs7bRHTmbJwFYgACPYsAAuRdGUkgLA-N4YfYdDoE",
    "CAACAgIAAxkBAAEQpOFpoyqzD1frms68wDUwg1tEtHmDhwACSJQAAuGJGEnTulOT2C5j8joE",
]


def _api_url(method: str) -> str:
    return f"https://api.telegram.org/bot{BOT_TOKEN}/{method}"


def _bot_api_request(method: str, *, data: dict[str, Any] | None = None) -> dict[str, Any]:
    response = requests.post(
        _api_url(method),
        data=data,
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    try:
        payload: dict[str, Any] = response.json()
    except ValueError:
        response.raise_for_status()
        raise RuntimeError(f"{method} вернул не-JSON ответ: {response.text[:300]}")

    if response.status_code >= 400 or not payload.get("ok"):
        description = payload.get("description", "unknown Telegram error")
        error_code = payload.get("error_code", response.status_code)
        raise RuntimeError(f"{method} error {error_code}: {description}")

    return payload


def _check_bot() -> None:
    payload = _bot_api_request("getMe")
    username = payload["result"].get("username", "<unknown>")
    print(f"[OK] Бот запущен: @{username}")


def _detect_group_chat_id_from_updates() -> int | None:
    payload = _bot_api_request("getUpdates", data={"limit": 100})
    updates = payload.get("result", [])

    for update in reversed(updates):
        for key in ("message", "channel_post", "edited_message", "edited_channel_post"):
            message = update.get(key)
            if not message:
                continue

            chat = message.get("chat", {})
            chat_type = chat.get("type")
            if chat_type in {"group", "supergroup"}:
                chat_id = chat.get("id")
                if isinstance(chat_id, int):
                    return chat_id

    return None


def _resolve_target_chat_id() -> int:
    if GROUP_CHAT_ID is not None:
        return GROUP_CHAT_ID

    detected_chat_id = _detect_group_chat_id_from_updates()
    if detected_chat_id is None:
        raise ValueError(
            "GROUP_CHAT_ID не задан и из getUpdates не удалось определить группу. "
            "Добавьте бота в группу, отправьте туда любое сообщение и запустите снова, "
            "или задайте GROUP_CHAT_ID вручную (обычно начинается с -100...)."
        )

    print(f"[OK] GROUP_CHAT_ID автоматически определён из getUpdates: {detected_chat_id}")
    return detected_chat_id


def _is_probably_sticker_file_id(value: str) -> bool:
    if not isinstance(value, str):
        return False
    if len(value) < 20:
        return False
    if value.isdigit() or value.startswith("temp_"):
        return False
    return value.startswith("CA")


def _prepare_stickers(stickers: list[str]) -> list[str]:
    valid: list[str] = []
    skipped = 0
    for sticker in stickers:
        if _is_probably_sticker_file_id(sticker):
            valid.append(sticker)
        else:
            skipped += 1

    if skipped:
        print(
            f"[WARN] Пропущено {skipped} невалидных id стикера "
            "(например числовые id или temp_* из другой системы)."
        )

    if not valid:
        raise ValueError(
            "В STICKERS не осталось валидных Bot API file_id. "
            "Нужны строки формата CAAC..."
        )

    return valid


def send_sticker(chat_id: int, sticker: str) -> None:
    _bot_api_request("sendSticker", data={"chat_id": chat_id, "sticker": sticker})


def run_bot_api_mode() -> None:
    _check_bot()
    chat_id = _resolve_target_chat_id()
    stickers = _prepare_stickers(STICKERS)

    print(f"[OK] Целевая группа: {chat_id}")

    while True:
        sticker = random.choice(stickers)
        try:
            send_sticker(chat_id, sticker)
            print(f"[SENT] {sticker}")
        except Exception as exc:
            print(f"[WARN] Ошибка отправки {sticker}: {exc}")

        time.sleep(SEND_INTERVAL_SECONDS)


def _normalize_target_chat(value: str) -> int | str:
    value = value.strip()
    if value.startswith("https://t.me/"):
        value = "@" + value.removeprefix("https://t.me/")
    if value.startswith("@"):
        return value
    try:
        return int(value)
    except ValueError:
        return value


async def connect_or_login_session() -> TelegramClient:
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.connect()

    if await client.is_user_authorized():
        me = await client.get_me()
        print(f"[OK] Сессия активна: {me.first_name or me.username or me.id}")
        return client

    phone = input("Введите номер телефона (например +79991234567): ").strip()
    await client.send_code_request(phone)
    code = input("Введите код из Telegram: ").strip()

    try:
        await client.sign_in(phone=phone, code=code)
    except SessionPasswordNeededError:
        password = input("Введите 2FA-пароль: ").strip()
        await client.sign_in(password=password)

    me = await client.get_me()
    print(f"[OK] Сессия подключена: {me.first_name or me.username or me.id}")
    return client


async def _load_stickers_from_set(client: TelegramClient) -> list[Any]:
    result = await client(GetStickerSetRequest(stickerset=InputStickerSetShortName(STICKER_SET_SHORT_NAME), hash=0))
    documents = list(result.documents or [])
    if not documents:
        raise ValueError(
            f"Стикерпак {STICKER_SET_SHORT_NAME} пуст или недоступен. "
            "Проверьте short_name у стикерпака."
        )
    return documents


async def run_session_mode() -> None:
    client = await connect_or_login_session()
    try:
        target_chat = _normalize_target_chat(str(TARGET_CHAT))
        entity = await client.get_entity(target_chat)
        stickers = await _load_stickers_from_set(client)
        print(f"[OK] Чат найден: {target_chat}")
        print(f"[OK] Загружено стикеров из пака {STICKER_SET_SHORT_NAME}: {len(stickers)}")

        while True:
            sticker_doc = random.choice(stickers)
            try:
                await client.send_file(entity, sticker_doc)
                print("[SENT] sticker(document)")
            except Exception as exc:
                print(f"[WARN] Ошибка отправки через сессию: {exc}")
            await asyncio.sleep(SEND_INTERVAL_SECONDS)
    finally:
        await client.disconnect()


async def main() -> None:
    print("1) Подключить/обновить сессию")
    print("2) Запустить отправку через сессию")
    print("3) Запустить отправку через bot api")
    choice = input("Выберите действие [1/2/3]: ").strip()

    if choice == "1":
        client = await connect_or_login_session()
        await client.disconnect()
        print("[OK] Сессия сохранена. Теперь можно запускать отправку.")
        return

    if choice == "2" or MODE == "session":
        await run_session_mode()
    else:
        run_bot_api_mode()


if __name__ == "__main__":
    asyncio.run(main())
