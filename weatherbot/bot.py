from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import config
import bot_keyboard
import messages
from coordinates import Coordinates

bot = Bot(token=config.BOT_API_TOKEN)
dp = Dispatcher(bot)

users = dict()

# @dp.message_handler(commands=['start', 'help'])
# async def process_start_command(message: types.Message):
#     await message.reply("Привет! Напиши мне что-нибудь!")


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    text = "Hello! Please, share your current GEO."
    await message.answer(text=text, reply_markup=bot_keyboard.START)


@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await message.answer(text=messages.help(), reply_markup=bot_keyboard.HELP)


@dp.message_handler(commands=['weather'])
async def process_weather_command(message: types.Message):
    coordinates = users[message.from_user.id]
    await message.answer(text=messages.weather(coordinates), reply_markup=bot_keyboard.WEATHER)


@dp.message_handler(commands=['additional_info'])
async def process_weather_command(message: types.Message):
    coordinates = users[message.from_user.id]
    await message.answer(text=messages.additional_info(coordinates), reply_markup=bot_keyboard.ADDITIONAL_INFO)


@dp.message_handler(content_types=['location'])
async def handle_location(message: types.Message):
    lat = message.location.latitude
    lon = message.location.longitude
    data = Coordinates(lat, lon)
    users[message.from_user.id] = data
    await message.answer(text="Thank you! Now you can use these buttons bellow:", reply_markup=bot_keyboard.HELP)


@dp.callback_query_handler(text="weather")
async def process_callback_weather(callback_query: types.CallbackQuery):
    coordinates = users[callback_query.from_user.id]
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=messages.weather(coordinates), reply_markup=bot_keyboard.WEATHER)


@dp.callback_query_handler(text="additional_info")
async def process_callback_additional_info(callback_query: types.CallbackQuery):
    coordinates = users[callback_query.from_user.id]
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, text=messages.additional_info(coordinates), reply_markup=bot_keyboard.ADDITIONAL_INFO)


if __name__ == '__main__':
    print("Bot started...")
    executor.start_polling(dp)