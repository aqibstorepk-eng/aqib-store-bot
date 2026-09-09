import os
import asyncio
import json
import html
import urllib.request
import urllib.error

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
QAMIFY_API_KEY = os.getenv("QAMIFY_API_KEY")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

if not QAMIFY_API_KEY:
    raise RuntimeError("QAMIFY_API_KEY is not set")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

QAMIFY_BASE_URL = "https://api.qamify.site"


# =========================
# MAIN MENU
# =========================

def main_menu():
    builder = InlineKeyboardBuilder()

    builder.button(text="🛍 SHOP", callback_data="shop")
    builder.button(text="💰 WALLET", callback_data="wallet")
    builder.button(text="🎁 FREEBIES", callback_data="freebies")
    builder.button(text="👤 PROFILE", callback_data="profile")
    builder.button(text="🎯 REFERRALS", callback_data="referrals")
    builder.button(text="📞 SUPPORT", callback_data="support")

    builder.adjust(2, 2, 2)
    return builder.as_markup()


# =========================
# QAMIFY API
# =========================

def qamify_get(endpoint):
    url = QAMIFY_BASE_URL + endpoint

    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {QAMIFY_API_KEY}",
            "Accept": "application/json",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)

    except urllib.error.HTTPError as e:
        try:
            error_body = e.read().decode("utf-8")
        except Exception:
            error_body = ""

        print(f"QAMIFY HTTP ERROR {e.code}: {error_body}")
        return None

    except Exception as e:
        print(f"QAMIFY ERROR: {e}")
        return None


async def get_products():
    return await asyncio.to_thread(qamify_get, "/v1/products")


# =========================
# START
# =========================

@dp.message(Command("start"))
async def start(message: Message):
    name = message.from_user.first_name or "Customer"

    text = (
        f"👋 Welcome, <b>{html.escape(name)}</b>!\n\n"
        "🛍 <b>Digital Aqib Store 🇵🇰</
