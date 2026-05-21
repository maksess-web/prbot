import asyncio
import os
import base64
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import (
    ChatWriteForbiddenError, UserBannedInChannelError,
    FloodWaitError, ChannelPrivateError, ChatAdminRequiredError,
    PeerFloodError, UserDeactivatedBanError
)

# ─── CONFIG ────────────────────────────────────────────────────────────────────
API_ID      = int(os.environ["TG_API_ID"])
API_HASH    = os.environ["TG_API_HASH"]
SESSION_STR = os.environ["TG_SESSION"]

# ─── ОБЪЯВЛЕНИЯ ────────────────────────────────────────────────────────────────

# Объявление для чатов С ОПЫТОМ
MESSAGE_EXPERIENCED = """
👔 Ищем опытных специалистов!

Здесь текст твоего объявления для людей с опытом.
Замени этот текст на свой.

📩 Писать: @твой_юзернейм
"""

# Объявление для чатов БЕЗ ОПЫТА
MESSAGE_BEGINNERS = """
🌟 Работа без опыта — обучаем с нуля!

Здесь текст твоего объявления для людей без опыта.
Замени этот текст на свой.

📩 Писать: @твой_юзернейм
"""

# ─── СПИСКИ ЧАТОВ ──────────────────────────────────────────────────────────────

# Чаты для людей С ОПЫТОМ (username или числовой ID)
CHATS_EXPERIENCED = [
    "username_чата_1",
    "username_чата_2",
    "username_чата_3",
    # добавляй сколько нужно
]

# Чаты для людей БЕЗ ОПЫТА
CHATS_BEGINNERS = [
    "username_чата_4",
    "username_чата_5",
    "username_чата_6",
    # добавляй сколько нужно
]

# ─── ОТПРАВКА ──────────────────────────────────────────────────────────────────

async def send_to_chat(client, chat, message):
    """Отправляем сообщение в один чат. При любой ошибке — пропускаем."""
    try:
        await client.send_message(chat, message, parse_mode='md')
        print(f"✅ Отправлено в {chat}")
        return True
    except FloodWaitError as e:
        print(f"⏳ FloodWait {chat}: ждём {e.seconds} сек...")
        await asyncio.sleep(e.seconds + 5)
        # Пробуем ещё раз после ожидания
        try:
            await client.send_message(chat, message, parse_mode='md')
            print(f"✅ Отправлено в {chat} (после ожидания)")
            return True
        except Exception as e2:
            print(f"❌ Не удалось после ожидания {chat}: {e2}")
            return False
    except (ChatWriteForbiddenError, UserBannedInChannelError,
            ChannelPrivateError, ChatAdminRequiredError) as e:
        print(f"🚫 Нет доступа к {chat}: {type(e).__name__}")
        return False
    except PeerFloodError:
        print(f"⚠️ PeerFlood — слишком много запросов. Ждём 5 минут...")
        await asyncio.sleep(300)
        return False
    except UserDeactivatedBanError:
        print(f"🔴 АККАУНТ ЗАБЛОКИРОВАН! Остановка.")
        raise  # критическая ошибка — останавливаем всё
    except Exception as e:
        print(f"❌ Ошибка {chat}: {type(e).__name__}: {e}")
        return False


async def main():
    print(f"Запуск рассылки...")

    async with TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH) as client:
        me = await client.get_me()
        print(f"Аккаунт: {me.first_name} (@{me.username})")

        sent = 0
        failed = 0

        # Рассылка в чаты С ОПЫТОМ
        print(f"\n--- Чаты с опытом ({len(CHATS_EXPERIENCED)}) ---")
        for chat in CHATS_EXPERIENCED:
            result = await send_to_chat(client, chat, MESSAGE_EXPERIENCED)
            if result:
                sent += 1
            else:
                failed += 1
            # Пауза между отправками (снижает риск бана)
            await asyncio.sleep(45)

        # Рассылка в чаты БЕЗ ОПЫТА
        print(f"\n--- Чаты без опыта ({len(CHATS_BEGINNERS)}) ---")
        for chat in CHATS_BEGINNERS:
            result = await send_to_chat(client, chat, MESSAGE_BEGINNERS)
            if result:
                sent += 1
            else:
                failed += 1
            await asyncio.sleep(45)

        print(f"\nГотово! Отправлено: {sent}, пропущено: {failed}")


if __name__ == "__main__":
    asyncio.run(main())
