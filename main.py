import logging
import enum
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text


class userState(enum.Enum):
    blank = 0
    registration = 1
    waiting_gender = 2
    waiting_companion_gender = 3
    waiting_name = 4
    waiting_photo = 5
    waiting_course = 6
    waiting_description = 7
    waiting_tags = 8
    viewing_forms = 9


class user:
    ID = 0  # INTEGER
    name = ""  # TEXT
    description = ""  # TEXT
    gender = 1  # 1-male 0-female 2-moderator # INTEGER
    companion_gender = 0  # 1-male 0-female 2-don't matter INTEGER
    course = 0  # INTEGER
    tag_list = []  # Список тегов ["Дружба" , "Музыка"]
    image = ""  # TEXT


max_tag_number = 5

allTagsList = ["Аниме культура", "Компьютерные игры", "Настольные игры", "Косплей/Ролеплей", "Сериалы",
               "Фильмы", "Книги", "Программирование", "Рисование", "Дизайн", "Политика", "Свидание вслепую",
               "Тусовки", "Музыка", "Спорт", "Проведение времени в душевной компании", "Поиск второй половинки",
               "Дружба", "Создание контента"]

user_data = {}

bot = Bot(token="5145205790:AAF3rNui4DLhSKMpq42LCpmqwfAmSbMzU44")

dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


def make_tag_buttons(usedTagList):
    ans = []
    for i in range(len(allTagsList)):
        if not allTagsList[i] in usedTagList:
            ans.append(InlineKeyboardButton(allTagsList[i], callback_data="btn" + str(i)))
    return ans


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ["Новая анкета"]
    keyboard.add(*buttons)
    await message.answer("Привет, я бот для знакомств РТУ МИРЭА\nСоздаем новую анкету ?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Новая анкета"))
async def new_form(message: types.Message):
    # TODO Имплементировать БД
    user_data[message.from_user.id] = user
    user_data[message.from_user.id].state = userState.waiting_gender
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*["Парень", "Девушка"])
    await message.answer("Кто ты ?", reply_markup=keyboard)


@dp.message_handler(Text(equals="Моя анкета"))
async def display_own_user_form(message: types.Message):
    # TODO Сделать более карасивый вывод анкеты и написать фукнцию генерации текста
    ans_text = user_data[message.from_user.id].name + " курс " + user_data[message.from_user.id].course + "\n"
    ans_text = ans_text + user_data[message.from_user.id].description

    await message.answer_photo(caption=ans_text, photo=user_data[message.from_user.id].image)


@dp.message_handler(Text(equals=["Парень", "Девушка"]))
async def get_gender(message: types.Message):
    if user_data[message.from_user.id].state == userState.waiting_gender:
        if message.text is "Парень":
            user_data[message.from_user.id].gender = 1
        else:
            user_data[message.from_user.id].gender = 0
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        keyboard.add(*["Парни", "Девушки", "Без разницы"])
        user_data[message.from_user.id].state = userState.waiting_companion_gender
        await message.answer("C кем хочешь общаться?", reply_markup=keyboard)


@dp.message_handler(Text(equals=["Парни", "Девушки", "Без разницы"]))
async def get_companion_gender(message: types.Message):
    if user_data[message.from_user.id].state == userState.waiting_companion_gender:
        if message.text is "Парни":
            user_data[message.from_user.id].gender = 1
        elif message.text is "Девушки":
            user_data[message.from_user.id].gender = 0
        else:
            user_data[message.from_user.id].gender = 2
        user_data[message.from_user.id].state = userState.waiting_name
        await message.answer("Как тебя зовут?")


@dp.message_handler(Text(equals=["1", "2", "3", "4"]))
async def get_course(message: types.Message):
    user_data[message.from_user.id].course = message.text
    user_data[message.from_user.id].state = userState.waiting_description
    await message.answer("Расскажи о себе")


@dp.message_handler(content_types=['photo'])
async def get_photo(message: types.Message):
    if user_data[message.from_user.id].state == userState.waiting_photo:
        user_data[message.from_user.id].image = message.photo[0].file_id
        user_data[message.from_user.id].state = userState.waiting_tags
        inline_keyboard = InlineKeyboardMarkup()
        inline_keyboard.add(*make_tag_buttons([]))
        await message.answer("Выбере интересные тебе темы общения", reply_markup=inline_keyboard)


@dp.message_handler(Text(equals=["Не хочу"]))
async def get_no_photo(message: types.Message):
    if user_data[message.from_user.id].state == userState.waiting_photo:
        user_data[message.from_user.id].image = ""
        user_data[message.from_user.id].state = userState.waiting_tags
        inline_keyboard = InlineKeyboardMarkup()
        inline_keyboard.add(*make_tag_buttons([]))
        await message.answer("Выбере интересные тебе темы общения", reply_markup=inline_keyboard)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('btn'))
async def process_button_callback(callback_query: types.CallbackQuery):
    code = int(callback_query.data[3:])
    user_data[callback_query.from_user.id].tag_list.append(str(allTagsList[code]))
    inline_keyboard = InlineKeyboardMarkup()
    inline_keyboard.add(*make_tag_buttons(user_data[callback_query.from_user.id].tag_list))
    inline_keyboard.add(InlineKeyboardButton("Я выбрал достаточо тем", callback_data="tagend"))
    await callback_query.message.edit_reply_markup(reply_markup=inline_keyboard)
    if len(user_data[callback_query.from_user.id].tag_list >= max_tag_number):
        user_data[callback_query.from_user.id].state = userState.viewing_forms
        # TODO Вывести рандомную анкету
        await callback_query.answer("")
    else:
        await callback_query.answer()


@dp.callback_query_handler(lambda c: c.data and c.data.startswith("tagend"))
async def process_button_callback(callback_query: types.CallbackQuery):
    user_data[callback_query.from_user.id].state = userState.viewing_forms
    # TODO Вывести рандомную анкету
    await callback_query.message.answer("Poggers")
    await callback_query.answer()

async def print_next_from():
    # TODO Получить анкету из БД
    pass

@dp.message_handler()
async def not_reserved(message: types.Message):
    # TODO Имплементировать БД
    if user_data[message.from_user.id].state == userState.waiting_name:
        user_data[message.from_user.id].name = message.text
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        buttons = ["1", "2"]
        keyboard.add(*buttons)
        buttons = ["3", "4"]
        keyboard.add(*buttons)
        user_data[message.from_user.id].state = userState.waiting_course
        await message.answer("С какого ты курса ?", reply_markup=keyboard)
    elif user_data[message.from_user.id].state == userState.waiting_description:
        user_data[message.from_user.id].description = message.text
        user_data[message.from_user.id].state = userState.waiting_photo
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        keyboard.add("Не хочу")
        await message.answer("Отправь свою фотографию",reply_markup=keyboard)
    else:
        await message.answer("Моя твоя не понимать :(\nИспользуй кнопки")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
