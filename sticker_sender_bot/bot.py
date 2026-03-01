import random
import time
from typing import Any

import requests

# === НАСТРОЙКИ ===
BOT_TOKEN = "8779722671:AAHD1Dj5guQA3nRU504y4lTtqOsc7m4YYCA"
GROUP_LINK = "https://t.me/+vuft45R2wW1kNjFi"  # только для справки
# ОБЯЗАТЕЛЬНО: chat_id группы, например -1001234567890
GROUP_CHAT_ID = None
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


def _check_bot() -> None:
    response = requests.get(_api_url("getMe"), timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()
    payload: dict[str, Any] = response.json()
    if not payload.get("ok"):
        raise RuntimeError(f"Ошибка getMe: {payload}")


def send_sticker(chat_id: int, sticker: str) -> None:
    response = requests.post(
        _api_url("sendSticker"),
        data={"chat_id": chat_id, "sticker": sticker},
        timeout=REQUEST_TIMEOUT_SECONDS,
    )
    response.raise_for_status()
    payload: dict[str, Any] = response.json()
    if not payload.get("ok"):
        raise RuntimeError(f"sendSticker вернул ошибку: {payload}")


def main() -> None:
    if GROUP_CHAT_ID is None:
        raise ValueError(
            "Укажите GROUP_CHAT_ID (например -1001234567890). "
            "Для приватной ссылки t.me/+... chat_id обязателен."
        )

    _check_bot()
    print("[OK] Бот запущен.")
    print(f"[OK] Целевая группа: {GROUP_CHAT_ID}")

    while True:
        sticker = random.choice(STICKERS)
        try:
            send_sticker(GROUP_CHAT_ID, sticker)
            print(f"[SENT] {sticker}")
        except Exception as exc:
            print(f"[WARN] Ошибка отправки: {exc}")

        time.sleep(SEND_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
