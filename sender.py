import asyncio
import os
import requests
from datetime import datetime
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

REPORT_BOT_TOKEN = os.environ["REPORT_BOT_TOKEN"]
REPORT_CHAT_ID   = os.environ["REPORT_CHAT_ID"]

# ─── ОБЪЯВЛЕНИЯ ────────────────────────────────────────────────────────────────

MESSAGE_EXPERIENCED = """
🔥🔥🔥 НАБОР ОПЕРАТОРОВ/ПЕРЕВОДЧИКОВ DREAM SINGLES ⚡️⚡️⚡️

⌛️НАЛИЧИЕ ОПЫТА НЕОБЯЗАТЕЛЬНО
📚 ПОЛНОЕ ОБУЧЕНИЕ 
🤑 ОТ 42% ДО 50% ЗАРАБОТКА С АНКЕТЫ
🎁 25% ОТ СТОИМОСТИ ПОДАРКА ИДУТ ОПЕРАТОРУ
💻 УДАЛЕННАЯ РАБОТА С ПК/НОУТБУКА
🏖 ГРАФИК 6/1, 8 ЧАСОВ С ВОЗМОЖНОСТЬ РАЗДЕЛИТЬ СМЕНУ НА НЕСКОЛЬКО РАЗ
📈 КАРЪЕРНЫЙ РОСТ
🏆 ОТСУТСТВИЕ ШТРАФОВ ВНУТРИ КОМПАНИИ
💛 БОНУСЫ ДЛЯ ОПЫТНЫХ ОПЕРАТОРОВ + ТОПОВЫЕ АНКЕТЫ
🚀 ТРЕНИНГИ И ОБУЧЕНИЯ ОТ ОПЫТНЫХ ТИМЛИДЕРОВ
💥 СИСТЕМА БОНУСОВ 
💵 ВОЗМОЖНОСТЬ ПОЛУЧИТЬ ВЫПЛАТУ В КРИПТЕ
🔗 DREAM SINGLES

ИНТЕРЕСНО? ПИШИ TG - @max_dreamx 📩
"""

MESSAGE_BEGINNERS = """
💻 Оператор онлайн-чата (удалённо, без опыта)

Ищем человека для работы в переписке с клиентами. Без звонков, без продаж и без сложных задач - только чат 💬 

📌 Что нужно делать:
• Общаться с клиентами в чате по готовым инструкциям
• Отвечать на сообщения по готовым материалам
• Поддерживать диалог в переписке

📌 Условия:
• Полностью удалённая работа из дома
• График: 6/1, по 8 часов в день
• Доход: 39000 - 43000 грн + бонусы
• Стабильные выплаты без задержек
• Бесплатное обучение с нуля
• Поддержка куратора на каждом этапе

📌 Подходит тебе, если:
• Есть ПК или ноутбук
• Стабильный интернет
• Ты внимательный и ответственный
• Опыт не нужен - обучение с нуля

📩 Пиши в личные сообщения @max_dreamx
Расскажем детали и поможем быстро
"""

# ─── СПИСКИ ЧАТОВ ──────────────────────────────────────────────────────────────

CHATS_EXPERIENCED = [
    "OTC_ADULT",
    "OnlyBulletin",
    "MonkeyDesk",
    "PandaDesk",
    "freelance_chat_crimson",
    "DeskCrew",
    "board_onlyfans",
    "freelance_chatikk",
    "Market_Desk",
    "MoneyManiaGreen",
    "SugarDesk",
    "blud_adult",
    "onlyfans_legit",
    "kameliagroup",
    "diamond_networking",
    "freelancee_chati",
    "CuteAgencyDesk",
    "datingclubforum",
    "only_adult_chat",
    "datingworkplace",
    "of_x_hunters",
    "adult_18_board",
    "woompboard",
    "adultworkplace",
    "CardoCrewDesk",
    "black_only_desk",
    "adult_agency_industry",
    "onlyfans_mart",
    "adult_headhunt",
    "jobadult",
    "onlyfans_desk",
    "TopDatingForum",
    "OnyxOnlyfansDesk",
    "onlydesc",
    "adult_worker",
    "acaagawgfwa",
    "only_desk",
    "onlydeskadult",
    "camweboard",
    "virgin_grooup",
]

CHATS_BEGINNERS = [
    "WORKINGUA2",
    "uaallwork",
    "work_online_kiev",
    "work_chat_ua",
    "work_ukraine_kyiv",
    "jb_ua",
    "ua_ads",
    "RabotaFreelanceUa",
    "workingkyivwork",
    "rabota_ua8",
    "piarchattua1",
    "Mr_White_Business_Chat",
    "avito_chaatik",
    "udalenka_chat_ua",
    "odesa_robotaa",
    "robotaonllnechat",
    "robotachat2024",
    "ogoloshennyaU",
    "kupiprodayukra",
    "Kiev24chat",
    "kiev_vakanciya",
    "warsawa_work",
    "worker_odessa",
    "work_lviv2",
    "rabotaonlain48",
    "onlinerabota07",
    "rabota_onlliine",
    "freelance_chatik0",
    "rabotadneprzdes",
    "chatik1504",
    "chat_raboty",
    "rabota_ukraine_chat",
    "rabota_onlik",
    "rabota_chatt",
    "ishchu_rabotu_chat",
    "work_rabota_k",
    "doskaobyavleniyUK",
    "prorobotarv",
    "robota5500",
    "work_ua_01",
    "rabotavsumychat",
    "business_chat_ua",
    "Chat_rabota_ishchu_rabotu",
    "rabota_v_Dnepre_center",
    "g_7RDE0YS7dU5NmQy",
]

# ─── ОТЧЁТЫ ────────────────────────────────────────────────────────────────────

def send_report(text):
    try:
        url = f"https://api.telegram.org/bot{REPORT_BOT_TOKEN}/sendMessage"
        r = requests.post(url, json={
            "chat_id": REPORT_CHAT_ID,
            "text": text,
            "parse_mode": "Markdown"
        }, timeout=10)
        print(f"Report sent: {r.status_code}")
    except Exception as e:
        print(f"[WARN] Report failed: {e}")

# ─── ОТПРАВКА ──────────────────────────────────────────────────────────────────

async def send_to_chat(client, chat, message, account_name):
    try:
        print(f"Trying to send to {chat}...")
        await client.send_message(chat, message, parse_mode='md')
        now = datetime.now().strftime("%H:%M")
        print(f"✅ Отправлено в @{chat}")
        send_report(f"✅ *{account_name}* отправила сообщение в *{now}* в чат @{chat}")
        return True

    except FloodWaitError as e:
        print(f"⏳ FloodWait {chat}: ждём {e.seconds} сек...")
        send_report(f"⏳ FloodWait — ждём {e.seconds} сек перед @{chat}")
        await asyncio.sleep(e.seconds + 5)
        try:
            await client.send_message(chat, message, parse_mode='md')
            now = datetime.now().strftime("%H:%M")
            send_report(f"✅ *{account_name}* отправила сообщение в *{now}* в чат @{chat} (после ожидания)")
            return True
        except Exception as e2:
            print(f"❌ После FloodWait: {e2}")
            send_report(f"❌ Не удалось отправить в @{chat}: {type(e2).__name__}")
            return False

    except (ChatWriteForbiddenError, UserBannedInChannelError,
            ChannelPrivateError, ChatAdminRequiredError) as e:
        print(f"🚫 Нет доступа к @{chat}: {type(e).__name__}")
        send_report(f"🚫 Нет доступа к @{chat} — пропускаем")
        return False

    except PeerFloodError:
        print(f"⚠️ PeerFlood — ждём 5 минут...")
        send_report(f"⚠️ PeerFlood — слишком много запросов, ждём 5 минут")
        await asyncio.sleep(300)
        return False

    except UserDeactivatedBanError:
        print(f"🔴 АККАУНТ ЗАБЛОКИРОВАН!")
        send_report(f"🔴 АККАУНТ ЗАБЛОКИРОВАН! Рассылка остановлена.")
        raise

    except Exception as e:
        print(f"❌ Ошибка @{chat}: {type(e).__name__}: {e}")
        send_report(f"❌ Ошибка в @{chat}: {type(e).__name__}: {e}")
        return False


async def main():
    print(f"API_ID: {API_ID}")
    print(f"SESSION длина: {len(SESSION_STR)}")
    print("Подключаемся к Telegram...")

    async with TelegramClient(StringSession(SESSION_STR), API_ID, API_HASH) as client:
        print("Подключились! Получаем данные аккаунта...")
        me = await client.get_me()
        account_name = me.first_name or me.username or "Бот"
        print(f"Аккаунт: {account_name} (@{me.username})")

        now = datetime.now().strftime("%d.%m.%Y %H:%M")
        send_report(f"🚀 Начинаю рассылку | {now}\nАккаунт: *{account_name}*")

        sent = 0
        failed = 0

        print(f"\n--- Чаты с опытом ({len(CHATS_EXPERIENCED)}) ---")
        for chat in CHATS_EXPERIENCED:
            result = await send_to_chat(client, chat, MESSAGE_EXPERIENCED, account_name)
            if result:
                sent += 1
            else:
                failed += 1
            await asyncio.sleep(8)

        print(f"\n--- Чаты без опыта ({len(CHATS_BEGINNERS)}) ---")
        for chat in CHATS_BEGINNERS:
            result = await send_to_chat(client, chat, MESSAGE_BEGINNERS, account_name)
            if result:
                sent += 1
            else:
                failed += 1
            await asyncio.sleep(20)

        summary = (
            f"📊 *Рассылка завершена*\n"
            f"✅ Отправлено: {sent}\n"
            f"❌ Пропущено: {failed}\n"
            f"📋 Всего чатов: {sent + failed}"
        )
        print(summary)
        send_report(summary)


if __name__ == "__main__":
    asyncio.run(main())
