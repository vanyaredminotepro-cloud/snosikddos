import asyncio
import random
from telethon import TelegramClient

# === НАСТРОЙКИ ===
API_ID = 23695534
API_HASH = "08f5b069bb4fd8505b98a6b57f857868"
BOT_TOKEN = "8779722671:AAHD1Dj5guQA3nRU504y4lTtqOsc7m4YYCA"
GROUP_LINK = "https://t.me/+vuft45R2wW1kNjFi"
# Для приватных групп укажите chat id вручную (например: -1001234567890)
GROUP_CHAT_ID = None
SEND_INTERVAL_SECONDS = 5
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


def _normalize_group_target(group_link: str):
    if group_link.startswith("https://t.me/"):
        slug = group_link.removeprefix("https://t.me/").strip("/")
        if slug.startswith("+"):
            return None
        return slug

    if group_link.startswith("@"):
        return group_link

    return group_link


async def resolve_group(client: TelegramClient):
    if GROUP_CHAT_ID is not None:
        return await client.get_entity(GROUP_CHAT_ID)

    normalized_target = _normalize_group_target(GROUP_LINK)
    if normalized_target is None:
        raise ValueError(
            "Для ботов Telegram приватные invite-ссылки (t.me/+...) недоступны через API. "
            "Добавьте бота в группу вручную и укажите GROUP_CHAT_ID (например -100...) "
            "или публичный @username/https://t.me/<username>."
        )

    return await client.get_entity(normalized_target)


async def main() -> None:
    client = TelegramClient("sticker_sender_bot", API_ID, API_HASH)
    await client.start(bot_token=BOT_TOKEN)
    print("[OK] Бот запущен.")

    chat = await resolve_group(client)
    print(f"[OK] Целевая группа определена: {chat.id}")

    while True:
        sticker = random.choice(STICKERS)
        await client.send_file(chat, sticker)
        print(f"[SENT] {sticker}")
        await asyncio.sleep(SEND_INTERVAL_SECONDS)


if __name__ == "__main__":
    asyncio.run(main())
