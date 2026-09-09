import os
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


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


@dp.message(Command("start"))
async def start(message: Message):
    name = message.from_user.first_name or "Customer"

    text = (
        f"👋 Welcome, <b>{name}</b>!\n\n"
        "🛍 <b>Digital Aqib Store 🇵🇰</b>\n"
        "Quality products at affordable prices.\n\n"
        "Choose an option below:"
    )

    await message.answer(
        text,
        reply_markup=main_menu(),
        parse_mode="HTML"
    )


@dp.callback_query(F.data == "shop")
async def shop(callback: CallbackQuery):
    await callback.message.edit_text(
        "🛍 <b>SHOP</b>\n\n"
        "📦 Products will appear here.\n\n"
        "🔌 Supplier API will be connected in the next step.",
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(F.data == "wallet")
async def wallet(callback: CallbackQuery):
    await callback.message.edit_text(
        "💰 <b>WALLET</b>\n\n"
        "Balance: <b>$0.00</b>\n\n"
        "Payment system will be added later.",
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(F.data == "profile")
async def profile(callback: CallbackQuery):
    user = callback.from_user

    await callback.message.edit_text(
        f"👤 <b>PROFILE</b>\n\n"
        f"Name: {user.full_name}\n"
        f"Username: @{user.username or 'Not set'}\n"
        f"User ID: <code>{user.id}</code>",
        parse_mode="HTML"
    )
    await callback.answer()


@dp.callback_query(F.data == "freebies")
async def freebies(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🎁 <b>FREEBIES</b>\n\n"
        "Free products and offers will appear here.",
        parse_mode="HTML"
    )


@dp.callback_query(F.data == "referrals")
async def referrals(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "🎯 <b>REFERRALS</b>\n\n"
        "Your referral system will be added later.",
        parse_mode="HTML"
    )


@dp.callback_query(F.data == "support")
async def support(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "📞 <b>SUPPORT</b>\n\n"
        "Contact support here.",
        parse_mode="HTML"
    )


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
