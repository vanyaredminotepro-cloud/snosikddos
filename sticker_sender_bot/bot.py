import random
import time
from typing import Any

import requests

# === НАСТРОЙКИ ===
BOT_TOKEN = "8779722671:AAHD1Dj5guQA3nRU504y4lTtqOsc7m4YYCA"
GROUP_LINK = "https://t.me/+vuft45R2wW1kNjFi"  # только для справки
# Если None, бот попробует взять chat_id из последних getUpdates
GROUP_CHAT_ID: int | None = None
SEND_INTERVAL_SECONDS = 5
REQUEST_TIMEOUT_SECONDS = 30
# =================

STICKERS = [
    "CAACAgIAAxkBAAEQpN5poyqxZEIu0ckIDNuBjXQhJx_HdAACVpcAAg5nGUkME8ZzJeb0CDoE",
    "CAACAgIAAxkBAAEQpOBpoyqzX4T9RbGlTs7bRHTmbJwFYgACPYsAAuRdGUkgLA-N4YfYdDoE",
    "CAACAgIAAxkBAAEQpOFpoyqzD1frms68wDUwg1tEtHmDhwACSJQAAuGJGEnTulOT2C5j8joE",
    "CAACAgIAAxkBAAEQpORpoyq1EZV8Fsxo0uLmjt3xy84lVgAC_JIAAknfGUldvbWxv9kAAbI6BA",
    "CAACAgIAAxkBAAEQpOVpoyq2gJdDtrwPHzXwqCW4vuOingACsZwAAobuGUnwuJ2bcy6RGjoE",
    "CAACAgIAAxkBAAEQpOdpoyq3LPSJYlch-ablDAPEzNqRLgACaJkAAo4YGUkDlrZtEoqKBToE",
    "CAACAgIAAxkBAAEQpOlpoyq31gVAYiEyDDEUHRJHeAABkfEAAn2TAAIzchlJX9dYGmkLJuk6BA",
    "CAACAgIAAxkBAAEQpOppoyq44gABS6hm0zToZ6kCEpXiW2wAAvKVAAJD0RhJb62ix8LfkEk6BA",
    "CAACAgIAAxkBAAEQpO5poyq8PLg5jimuluOhcC8juls72wACA44AAshzGUmQND1EN1iYkToE",
    "CAACAgIAAxkBAAEQpPBpoyq-ZJKfU8LvMjNrP8TT-4nZ9QACJJsAAiMUEUkQXFu4GQWIlDoE",
    "CAACAgIAAxkBAAEQpPJpoyrA3_K8SGVeRsBn0l_F_vuY5wACuqMAArDVGEm-cA_CwWqJEzoE",
    "CAACAgIAAxkBAAEQpPRpoyrCttuKVpiyYChrIwWRq9QvHwACqpsAAraoGUktcd9Nf6BafDoE",
    "CAACAgIAAxkBAAEQpPZpoyrEVkOZClGyCZCSbqiadkEN4gAC1IUAArxPGEkrWoqWcU3kmjoE",
    "CAACAgIAAxkBAAEQpPhpoyrGtEGmOrmbtdBbQBAyxM8rlAACGooAAp5NGEkly7oI9QXg-DoE",
    "CAACAgIAAxkBAAEQpPppoyrHFQVB_17H5XjodxHEtYJfggACaZQAAq0xEUkE1vTgRLaCuDoE",
    "CAACAgIAAxkBAAEQpPxpoyrJ8Iy1PelVoRTFrKfJd12puQACmY4AAj6AGEmnrdRkLcSOhjoE",
    "CAACAgIAAxkBAAEQpP5poyrL6hdkzzSVYHYdgPiyxGBDIgAC3JQAAgjpGUkC2UQiIqI1xDoE",
    "CAACAgIAAxkBAAEQpQABaaMqze5xm_PQ0lCQtJ4jrTi8AnAAAgGVAAJMmhlJ8IYS6bgXQy86BA",
    "CAACAgIAAxkBAAEQpQJpoyrOrfwuwIAyetSLLtPleHSsgwACd5AAAm8rGUmf91_vj4gZcjoE",
    "CAACAgIAAxkBAAEQpQRpoyrQ7bQXPBJjT2Eo9zQ5XOlb9AAC85wAAo_KEEmNhFLeQmWRNjoE",
    "CAACAgIAAxkBAAEQpQhpoyrnsJ__IBOLJRr6BFQ_VioAAVQAArOVAAK_xxhJEqYeGBvf1zs6BA",
    "CAACAgIAAxkBAAEQpQppoyrpFbl76Yra8YH8ITHkan97YQACfJkAAl44GElU-DAPZAS2FDoE",
    "CAACAgIAAxkBAAEQpQxpoyrs6A6WUKLqNuV7el6n690LPwAC05wAAu0gGElwj3cXVT0U6zoE",
    "CAACAgIAAxkBAAEQpQ5poyrttnJkKyRfmlTXpi8J0sSh1wACVZMAAod7GUlQUb6lMhsdGzoE",
    "CAACAgIAAxkBAAEQpRBpoyrvbrvecpErJhv9XZXewYroMQACA5MAAoHeGEm8tLlVyFZJgDoE",
    "CAACAgIAAxkBAAEQpRJpoyrxG6tZ9nToky6iKXKsw294sAACFokAAlLOGEkTgp6ysblaMDoE",
    "CAACAgIAAxkBAAEQpRRpoyryj3Oo90ePZ8AvGsd0EckH9AACNJwAAj2oGUmqRelGihFpvDoE",
    "CAACAgIAAxkBAAEQpRZpoyr0ws3tSv85JdafXnZUVk0lhgACiZUAAl6HGUnEM4QqTr6K7ToE",
    "CAACAgIAAxkBAAEQpRhpoyr1qqhmYkOwHqX0VqzyC-oImQACfY0AAjHIGEn1pmuvN4z9QjoE",
    "CAACAgIAAxkBAAEQpRppoyr3c58ifW8eDjlXkGIhiNQcYQACMZ0AArOlGEnSuBSKlPt3TzoE",
    "CAACAgIAAxkBAAEQpRxpoyr5fb3gqkfCP_7hExHMj5b9GgAC1pAAApjQGEkfaa-mw_mxZzoE",
    "CAACAgIAAxkBAAEQpR5poyr6zq13Qxu7_rUbJxj9WBWl3wACwpcAAsScGUkIvnOUS8nnoToE",
    "CAACAgIAAxkBAAEQpSNpoytfOizdITYqMfpBp8nJgg7B7gACkKIAAqVUGUloH6bbGynL3DoE",
    "CAACAgIAAxkBAAEQpSVpoyth9LszFXuQtyGTNFb8MvarfwACjo8AAss8GUmcpKlwsEZY9DoE",
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
    """
    Быстрая фильтрация невалидных значений для sendSticker.
    Ожидаем Bot API file_id (обычно начинается с CAAC...).
    """
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


def main() -> None:
    _check_bot()
    chat_id = _resolve_target_chat_id()
    stickers = _prepare_stickers(STICKERS)

    if chat_id > 0:
        print(
            "[WARN] chat_id положительный. Для групп обычно используется отрицательный id "
            "(например -100...). Проверьте, что это точно id группы, а не пользователя/бота."
        )

    print(f"[OK] Целевая группа: {chat_id}")

    while True:
        sticker = random.choice(stickers)
        try:
            send_sticker(chat_id, sticker)
            print(f"[SENT] {sticker}")
        except Exception as exc:
            print(f"[WARN] Ошибка отправки {sticker}: {exc}")
            if "chat not found" in str(exc).lower() or "not enough rights" in str(exc).lower():
                print(
                    "[HINT] Проверьте, что bot добавлен в группу, chat_id верный (-100...), "
                    "и у бота есть права отправки сообщений/стикеров."
                )

        time.sleep(SEND_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
