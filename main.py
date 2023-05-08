from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
import re
import datetime

pattern = r'^\d+[km]$'
pattern1 = r'^\d+[k]$'
pattern2 = r'^\d+[m]$'

storage = MemoryStorage()
bot = Bot("5830868688:AAGpyyeoZF9BWtO0oyVA-01wpAZi80UBsMw")
dp = Dispatcher(bot,
                storage=storage)

kb = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [KeyboardButton('/start')]
])
kb1 = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False, keyboard=[
    [KeyboardButton('Начать поиск'), KeyboardButton('Фильтр')]
])

ikb = InlineKeyboardMarkup(row_width=2)
ikb1 = InlineKeyboardMarkup(row_width=2)
ikb2 = InlineKeyboardMarkup(row_width=2)
ikb3= InlineKeyboardMarkup(row_width=2)
ikb4 = InlineKeyboardMarkup(row_width=2)

ikb.add(InlineKeyboardButton('Цена', callback_data='price')).insert(InlineKeyboardButton('Пробег', callback_data='mileage')).add(InlineKeyboardButton('Год', callback_data='year')).insert(InlineKeyboardButton('Назад', callback_data='back2'))
ikb1.add(InlineKeyboardButton('Назад', callback_data='back1')).insert(InlineKeyboardButton('Выход', callback_data='back'))
ikb2.add(InlineKeyboardButton('Назад', callback_data='price')).insert(InlineKeyboardButton('Выход', callback_data='back'))
ikb3.add(InlineKeyboardButton('Назад', callback_data='mileage')).insert(InlineKeyboardButton('Выход', callback_data='back'))
ikb4.add(InlineKeyboardButton('Назад', callback_data='year')).insert(InlineKeyboardButton('Выход', callback_data='back'))

START = """
Привет! Я могу быстрее всех уведомить Вас о новой машине. Я слежу за обновлениями с популярных сайтов!
Чтобы начать следить за обновлениями, вызовите команду <b>/search</b>. Вы можете следить либо за всеми объявлениями, либо за конкретным запросом.
Параметры запроса указываются через пробел, например: Lada привод задний бензин. Если будет совпадение, бот сразу пришлёт вам объявление и его источник.
Если нужно указать несколько запросов, то вызовите ещё раз команду <b>/start</b>. Удачи!"""

k, k1, k2, k3, k4, k5 = 0, 0, 0, 0, 0, 0

data_car = {
    'min_price': '',
    'max_price': '',
    'min_year': '',
    'max_year': '',
    'min_probeg': '',
    'max_probeg': '',
}

text = ''

class SetParamsForSearch(StatesGroup):
    waiting_for_filter = State()
    waiting_for_get_filter = State()
    waiting_for_get_filter1 = State()
    waiting_for_get_filter2 = State()
    waiting_for_get_filter3 = State()
    waiting_for_get_filter4 = State()
    waiting_for_get_filter5 = State()
    waiting_for_get_filter6 = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        'Привет! Я слежу за обновлениями с популярных сайтов по продажам машин! Введите фильтры поиска. Если не хотите вводить какой-либо фильтр, то пропустите его, после чего нажмите "начать поиск"',
        reply_markup=kb1)

@dp.message_handler(text='Фильтр')
async def filt(message: types.Message):
    await message.answer('Выберите фильтр',
                         reply_markup=ikb)
    await message.delete()
    await SetParamsForSearch.waiting_for_filter.set()

@dp.callback_query_handler(text='back', state='*')
async def callback(callback: types.CallbackQuery, state: FSMContext):
    global k, k1, k2, k3
    await callback.message.edit_text('Выберите фильтр',
                                     reply_markup=ikb)
    await state.finish()
    k, k1, k2, k3 = 0, 0, 0, 0

@dp.callback_query_handler(text='back1', state='*')
async def back1(callback: types.CallbackQuery, state: FSMContext):
    global k, k1, k2, k3
    await callback.message.edit_text('Выберите фильтр',
                                     reply_markup=ikb)
    k, k1, k2, k3 = 0, 0, 0, 0

@dp.callback_query_handler(text='back2', state='*')
async def callback(callback: types.CallbackQuery, state: FSMContext):
    global k, k1, k2, k3
    await callback.message.delete()
    await state.finish()
    k, k1, k2, k3 = 0, 0, 0, 0

@dp.callback_query_handler(text='mileage', state='*')
async def mileage(callback: types.CallbackQuery, state: FSMContext):
    message = await callback.message.edit_text('Напишите минимальный пробег. Можете использовать символы "k" и "m" для сокращения, например:'
                                               '\n\t100k = 100 тыс.\n\t1m = 1 млн.',
                                               reply_markup=ikb1)
    await state.update_data(message_id=message.message_id)
    await SetParamsForSearch.waiting_for_get_filter2.set()

@dp.callback_query_handler(text='price', state='*')
async def price(callback: types.CallbackQuery, state: FSMContext):
    message = await callback.message.edit_text('Напишите минимальную цену. Можете использовать символы "k" и "m" для сокращения, например:'
                                               '\n\t100k = 100 тыс.\n\t1m = 1 млн.',
                                               reply_markup=ikb1)
    await state.update_data(message_id = message.message_id)
    await SetParamsForSearch.waiting_for_get_filter.set()

@dp.callback_query_handler(text='year', state='*')
async def price(callback: types.CallbackQuery, state: FSMContext):
    global k4
    message = await callback.message.edit_text(
        'Напишите минимальный год выпуска (не меньше <b>1940-го</b> года).',
        reply_markup=ikb1,
        parse_mode='HTML')
    await state.update_data(message_id = message.message_id)
    await SetParamsForSearch.waiting_for_get_filter4.set()
    k4 = 0

@dp.message_handler(lambda message: not message.text.isdigit() and not re.match(pattern, message.text), state=SetParamsForSearch.waiting_for_get_filter)
async def check(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data['message_id']
        global k, k1
        if k == 0:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message_id,
                text='<b>Неправильный формат ввода!</b> Напишите минимальную цену. Можете использовать символы "k" и "m" для сокращения, например:'
                     '\n\t100k = 100 тыс.\n\t1m = 1 млн.',
                parse_mode='HTML',
                reply_markup=ikb1
            )
            await message.delete()
            k += 1
        else:
            await message.delete()
        k1 = 0

@dp.message_handler(lambda message: not message.text.isdigit() and not re.match(pattern, message.text), state=SetParamsForSearch.waiting_for_get_filter1)
async def check1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data['message_id']
        global k1
        if k1 == 0:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message_id,
                text='<b>Неправильный формат ввода!</b> Напишите максимальную цену. Можете использовать символы "k" и "m" для сокращения, например:'
                     '\n\t100k = 100 тыс.\n\t1m = 1 млн.',
                parse_mode='HTML',
                reply_markup=ikb2
            )
            await message.delete()
            k1 += 1
        else:
            await message.delete()

@dp.message_handler(lambda message: not message.text.isdigit() and not re.match(pattern, message.text), state=SetParamsForSearch.waiting_for_get_filter2)
async def check2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data['message_id']
        global k2, k3
        if k2 == 0:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message_id,
                text='<b>Неправильный формат ввода!</b> Напишите минимальный пробег. Можете использовать символы "k" и "m" для сокращения, например:'
                     '\n\t100k = 100 тыс.\n\t1m = 1 млн.',
                parse_mode='HTML',
                reply_markup=ikb1
            )
            await message.delete()
            k2 += 1
        else:
            await message.delete()
        k3 = 0

@dp.message_handler(lambda message: not message.text.isdigit() and not re.match(pattern, message.text), state=SetParamsForSearch.waiting_for_get_filter3)
async def check3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data['message_id']
        global k3
        if k3 == 0:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message_id,
                text='<b>Неправильный формат ввода!</b> Напишите максимальный пробег. Можете использовать символы "k" и "m" для сокращения, например:'
                     '\n\t100k = 100 тыс.\n\t1m = 1 млн.',
                parse_mode='HTML',
                reply_markup=ikb3
            )
            await message.delete()
            k3 += 1
        else:
            await message.delete()

@dp.message_handler(lambda message: not message.text.isdigit() or int(message.text) < 1940 or int(message.text) > datetime.date.today().year, state=SetParamsForSearch.waiting_for_get_filter4)
async def check4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data['message_id']
        global k4, k5
        if k4 == 0:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message_id,
                text='<b>Неправильный формат ввода!</b> Напишите минимальный год выпуска (не меньше <b>1940-го</b> года).',
                parse_mode='HTML',
                reply_markup=ikb1
            )
            await message.delete()
            k4 += 1
        else:
            await message.delete()
        k5 = 0

@dp.message_handler(lambda message: not message.text.isdigit() or int(message.text) < 1940 or int(message.text) > datetime.date.today().year, state=SetParamsForSearch.waiting_for_get_filter5)
async def check5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data['message_id']
        global k5
        if k5 == 0:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message_id,
                text='<b>Неправильный формат ввода!</b> Напишите максимальный год выпуска',
                parse_mode='HTML',
                reply_markup=ikb4
            )
            await message.delete()
            k5 += 1
        else:
            await message.delete()

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter)
async def add_filter(message: types.Message, state: FSMContext):
    global text, k
    async with state.proxy() as data:
        message_id = data['message_id']
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text='Теперь введите максимальную цену',
            reply_markup=ikb2
        )
        await message.delete()
        text = message.text
        if re.match(pattern1, text):
            text = str(int(text[:text.find('k')]) * 10 ** 3)
        elif re.match(pattern2, text):
            text = str(int(text[:text.find('m')]) * 10 ** 6)
        data['min_price'] = text
        data_car['min_price'] = data['min_price']
        print(data_car['min_price'])
        await SetParamsForSearch.waiting_for_get_filter1.set()
        k = 0

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter1)
async def add_filter1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        global k1
        message_id = data['message_id']
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text='Выберите фильтр',
            reply_markup=ikb)
        await message.delete()
        text = message.text
        if re.match(pattern1, text):
            text = str(int(text[:text.find('k')]) * 10 ** 3)
        elif re.match(pattern2, text):
            text = str(int(text[:text.find('m')]) * 10 ** 6)
        data['max_price'] = text
        data_car['max_price'] = data['max_price']
        print(data_car['max_price'])
        k1 = 0

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter2)
async def add_filter2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        global k2
        message_id = data['message_id']
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text='Теперь введите максимальный пробег',
            reply_markup=ikb3
        )
        await message.delete()
        text = message.text
        if re.match(pattern1, text):
            text = str(int(text[:text.find('k')]) * 10 ** 3)
        elif re.match(pattern2, text):
            text = str(int(text[:text.find('m')]) * 10 ** 6)
        data['min_probeg'] = text
        data_car['min_probeg'] = data['min_probeg']
        print(data_car['min_probeg'])
        await SetParamsForSearch.waiting_for_get_filter3.set()
        k2 = 0

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter3)
async def add_filter3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        global k3
        message_id = data['message_id']
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text='Выберите фильтр',
            reply_markup=ikb)
        await message.delete()
        text = message.text
        if re.match(pattern1, text):
            text = str(int(text[:text.find('k')]) * 10 ** 3)
        elif re.match(pattern2, text):
            text = str(int(text[:text.find('m')]) * 10 ** 6)
        data['max_probeg'] = text
        data_car['max_probeg'] = data['max_probeg']
        print(data_car)
        k3 = 0

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter4)
async def add_filter4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data['message_id']
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text='Теперь введите максимальный год выпуска',
            reply_markup=ikb4
        )
        await message.delete()
        text = message.text
        data['min_year'] = text
        data_car['min_year'] = data['min_year']
        await SetParamsForSearch.waiting_for_get_filter5.set()
        print(data_car)

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter5)
async def add_filter5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data['message_id']
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text='Выберите фильтр',
            reply_markup=ikb)
        await message.delete()
        text = message.text
        data['max_year'] = text
        data_car['max_year'] = data['max_year']
        print(data_car)



if __name__ == '__main__':
    executor.start_polling(dp)