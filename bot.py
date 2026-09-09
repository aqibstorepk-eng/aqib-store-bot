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


# =========================
# CONFIG
# =========================

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
QAMIFY_API_KEY = os.getenv("QAMIFY_API_KEY")

QAMIFY_BASE_URL = "https://api.qamify.site"


if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


# =========================
# MAIN MENU
# =========================

def main_menu():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🛍 SHOP",
        callback_data="shop"
    )

    builder.button(
        text="💰 WALLET",
        callback_data="wallet"
    )

    builder.button(
        text="🎁 FREEBIES",
        callback_data="freebies"
    )

    builder.button(
        text="👤 PROFILE",
        callback_data="profile"
    )

    builder.button(
        text="🎯 REFERRALS",
        callback_data="referrals"
    )

    builder.button(
        text="📞 SUPPORT",
        callback_data="support"
    )

    builder.adjust(2, 2, 2)

    return builder.as_markup()


# =========================
# BACK BUTTONS
# =========================

def back_to_menu_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🔙 Back to Menu",
        callback_data="back_menu"
    )

    return builder.as_markup()


def product_back_keyboard():
    builder = InlineKeyboardBuilder()

    builder.button(
        text="🔙 Back to Shop",
        callback_data="shop"
    )

    builder.button(
        text="🏠 Main Menu",
        callback_data="back_menu"
    )

    builder.adjust(1)

    return builder.as_markup()


# =========================
# QAMIFY API
# =========================

def qamify_request(endpoint):
    if not QAMIFY_API_KEY:
        print("ERROR: QAMIFY_API_KEY is not set")
        return None

    url = QAMIFY_BASE_URL + endpoint

    request = urllib.request.Request(
        url,
        headers={
            "Authorization": f"Bearer {QAMIFY_API_KEY}",
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read().decode("utf-8")
            return json.loads(body)

    except urllib.error.HTTPError as error:
        try:
            body = error.read().decode("utf-8")
        except Exception:
            body = ""

        print(
            f"QAMIFY HTTP ERROR: {error.code} | {body}"
        )

        return None

    except Exception as error:
        print(f"QAMIFY ERROR: {error}")

        return None


async def get_products():
    return await asyncio.to_thread(
        qamify_request,
        "/v1/products"
    )


async def get_product(product_id):
    return await asyncio.to_thread(
        qamify_request,
        f"/v1/products/{product_id}"
    )


# =========================
# PRODUCT DATA HELPERS
# =========================

def get_product_id(product):
    return (
        product.get("id")
        or product.get("product_id")
    )


def get_product_name(product):
    return (
        product.get("name")
        or product.get("title")
        or product.get("product_name")
        or "Unnamed Product"
    )


def get_product_price(product):
    return (
        product.get("price")
        or product.get("reseller_price")
        or product.get("price_usd")
        or product.get("amount")
        or "N/A"
    )


def get_product_stock(product):
    stock = (
        product.get("stock")
        if product.get("stock") is not None
        else product.get("stock_count", 0)
    )

    try:
        return int(stock)
    except (ValueError, TypeError):
        return 0


def get_product_description(product):
    return (
        product.get("description")
        or product.get("details")
        or ""
    )


def extract_products(data):
    if isinstance(data, list):
        return data

    if not isinstance(data, dict):
        return []

    possible_keys = [
        "products",
        "data",
        "items",
        "results"
    ]

    for key in possible_keys:
        value = data.get(key)

        if isinstance(value, list):
            return value

        if isinstance(value, dict):
            for nested_key in possible_keys:
                nested_value = value.get(nested_key)

                if isinstance(nested_value, list):
                    return nested_value

    return []


def extract_single_product(data):
    if not isinstance(data, dict):
        return {}

    if isinstance(data.get("product"), dict):
        return data["product"]

    if isinstance(data.get("data"), dict):
        return data["data"]

    return data


# =========================
# START
# =========================

@dp.message(Command("start"))
async def start(message: Message):

    name = message.from_user.first
