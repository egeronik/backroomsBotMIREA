import logging
import enum
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text


class BotState(enum.Enum):
    blank = 0
    registration = 1
    waiting_name = 2
    waiting_course = 3
    waiting_description = 4
    waiting_photo = 5


user_data = {}

bot = Bot(token="5145205790:AAF3rNui4DLhSKMpq42LCpmqwfAmSbMzU44")

dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = ["Новая анкета", "Я уже смешарик"]
    keyboard.add(*buttons)
    await message.answer("Привет, я бот для знакомств РТУ МИРЭА\nСоздаем новую анкету ?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Новая анкета"))
async def new_form(message: types.Message):
    # TODO Имплементировать БД
    user_data[message.from_user.id] = {}
    user_data[message.from_user.id]["state"] = BotState.waiting_name
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("Напиши своё имя", reply_markup=keyboard)


@dp.message_handler(Text(equals="Я уже смешарик"))
async def new_form(message: types.Message):
    await message.answer(user_data[message.from_user.id]["name"])


@dp.message_handler(Text(equals=["1", "2", "3", "4"]))
async def set_course(message: types.Message):
    user_data[message.from_user.id]["course"] = message.text
    user_data[message.from_user.id]["state"] = BotState.waiting_description
    keyboard = types.ReplyKeyboardRemove()
    await message.answer("Расскажи о себе", reply_markup=keyboard)


@dp.message_handler()
async def not_reserved(message: types.Message):
    # TODO Имплементировать БД
    if user_data[message.from_user.id]["state"] == BotState.waiting_name:
        user_data[message.from_user.id]["name"] = message.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = ["1", "2"]
        keyboard.add(*buttons)
        buttons = ["3", "4"]
        keyboard.add(*buttons)
        user_data[message.from_user.id]["state"] = BotState.waiting_course
        await message.answer("С какого ты курса ?", reply_markup=keyboard)
    elif user_data[message.from_user.id]["state"] == BotState.waiting_description:
        user_data[message.from_user.id]["description"] = message.text
        user_data[message.from_user.id]["state"] = BotState.waiting_photo
        keyboard = types.ReplyKeyboardRemove()
        await message.answer("Отправь свою фотографию", reply_markup=keyboard)
    else:
        await message.answer("Моя твоя не понимать :(\nИспользуй кнопки")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
