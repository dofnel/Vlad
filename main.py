from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from aiogram.types import Message
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram import F

users = {}
info = {}

months = ['январь', 'февраль', 'март', 'апрель', 'май',
          'июнь', 'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']


BOT_TOKEN = '6266926855:AAH6HlpggZp3oSOrTUWkKEC_6g1TsQZgSKs'

bot: Bot = Bot(BOT_TOKEN)
dp: Dispatcher = Dispatcher()

button_1: KeyboardButton = KeyboardButton(text='Анализы')
button_2: KeyboardButton = KeyboardButton(text='Анкета')

keyboard: ReplyKeyboardMarkup = ReplyKeyboardMarkup(keyboard=[[button_1, button_2]], resize_keyboard=True,
                                                    one_time_keyboard=True)


def isfloat(num: str) -> bool:
    try:
        float(num)
        return True
    except ValueError:
        return False


@dp.message(Command(commands='start'))
async def process_start(message: Message):
    first_name_tg = message.from_user.first_name
    await message.answer(f"Здравствуйте, {first_name_tg}, рады вас видеть!\n\nВам надо заполнить начальную анкету:"
                         f"\n\nДля этого нажмите кнопку Анкета ",
                         reply_markup=keyboard)


@dp.message(Command(commands='menu'))
async def menu_handler(message: Message):
    first_name_tg = message.from_user.first_name

    await message.answer(f"{first_name_tg}, now u are in menu", reply_markup=keyboard)


@dp.message(Text(text='Анализы'))
async def analysis_handler(message: Message):
    first_name = message.from_user.first_name

    await message.answer(f"{first_name}, нам нужен снимок ваших анализов, пришлите его.")


# Сохраняет фото в папку, где находится main.py
@dp.message(F.photo)
async def analysis(message):
    photo_id = message.photo[-1].file_id
    file = await bot.get_file(photo_id)
    photo_path = file.file_path

    await bot.download_file(photo_path, 'photo.jpg')


@dp.message(Text(text='Анкета'))
async def form_handler(message: Message):
    if message.from_user.id not in users:
        users[message.from_user.id] = {}
    else:
        users.pop(message.from_user.id)
        users[message.from_user.id] = {}

    await message.answer('Укажите ваш год рождения в формате 2022')


@dp.message(lambda x: x.text and x.text.isdigit() and 1900 <= int(x.text) <= 2023)
async def year_of_birth(message: Message):
    users[message.from_user.id]['year'] = message.text

    await message.answer('Укажите месяц рождения в формате: Январь, Февраль и тд')


@dp.message(Text(text=months, ignore_case=True))
async def month_of_birth(message: Message):
    users[message.from_user.id]['month'] = message.text

    await message.answer('Укажите день рождения (1-31)')


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 31)
async def day_of_birth(message: Message):
    users[message.from_user.id]['day'] = message.text

    await message.answer('Укажите ваш рост в см (целое число)')


@dp.message(lambda x: x.text and x.text.isdigit() and 140 <= int(x.text) <= 220)
async def tall_of_user(message: Message):
    users[message.from_user.id]['tall'] = message.text

    await message.answer('Укажите ваш вес в кг (целое число)')


@dp.message(lambda x: x.text and x.text.isdigit() and 32 <= int(x.text) <= 139)
async def weight_of_user(message: Message):
    users[message.from_user.id]['weight'] = message.text

    await message.answer('Укажите ваше артериальное давление. В формате(120/80)')


@dp.message(F.text.contains('/'))
async def pressure_of_user(message: Message):
    users[message.from_user.id]['pressure'] = message.text

    await message.answer('Укажите температуру тела в данный момент. В формате(XX.X)\n\n'
                         'Если температура - целое число, то пишите 36.0, 37.0')


@dp.message(lambda x: x.text and isfloat(x.text) and float(x.text) < 55)
async def temp_of_user(message: Message):
    users[message.from_user.id]['temp'] = message.text

    await message.answer('Укажите ваше имя и фамилию')


@dp.message(lambda x: x.text and not x.text.isdigit() and len(x.text) > 6)
async def name_and_surname(message: Message):
    users[message.from_user.id]['name'] = message.text.split()[0]
    users[message.from_user.id]['surname'] = message.text.split()[1]

    await message.answer('Укажите ваш номер без +')

    print(len(message.text))


@dp.message(lambda x: x.text and x.text.isdigit() and int(x.text) > 2500)
async def telephone_number_of_user(message: Message):
    users[message.from_user.id]['number'] = message.text

    await message.answer('Спасибо за ответы!\nЕсли вы хотите вернуться на главный экран, используйте кнопку /menu')

    print(users)


@dp.message()
async def react_to_any_message(message: Message):
    await message.answer('Что-то не работает')


if __name__ == '__main__':
    dp.run_polling(bot)
