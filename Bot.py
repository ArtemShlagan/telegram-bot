from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
import asyncio

API_TOKEN = "7847861512:AAEShfuvEJrf-eXLk7-17PT9N-LVbdooA_8"
CHANNELS = ["@test13121488"]

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: Message):
    greeting_text = (
        "👋 Привет! Я — твой личный бот, который поможет найти задания, которые тебя интересуют, "
        "или предложить свои навыки. Выбирай возможность и начинай зарабатывать!"
    )
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Бесплатно", callback_data="free")],
        [InlineKeyboardButton(text="Оплатить", callback_data="pay")]
    ])
    await message.answer(greeting_text, reply_markup=keyboard)

@dp.callback_query(lambda callback: callback.data == "free")
async def free_option(callback: CallbackQuery):
    channels_text = "\n".join([f"👉 {channel}" for channel in CHANNELS])
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Подписан", callback_data="check_subs")]
    ])
    await callback.message.answer(f"Подпишитесь на каналы:\n{channels_text}", reply_markup=keyboard)

@dp.callback_query(lambda callback: callback.data == "check_subs")
async def check_subscriptions(callback: CallbackQuery):
    user_id = callback.from_user.id
    not_subscribed = []

    for channel in CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                not_subscribed.append(channel)
        except Exception:
            not_subscribed.append(channel)

    if not not_subscribed:
        await callback.message.answer("Принято. Ваша заявка будет обработана в течении 24х часов. Перед началом работы - прочтите инструкцию по эксплуатированию бота, найти можно в описании.")
    else:
        channels_text = "\n".join([f"👉 {channel}" for channel in not_subscribed])
        await callback.message.answer(f"Вы не подписаны на следующие каналы:\n{channels_text}")

@dp.callback_query(lambda callback: callback.data == "pay")
async def pay_option(callback: CallbackQuery):
    await callback.message.answer("Функция оплаты пока не настроена. Скоро она появится!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())