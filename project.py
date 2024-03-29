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
ikb3 = InlineKeyboardMarkup(row_width=2)
ikb4 = InlineKeyboardMarkup(row_width=2)
ikb5 = InlineKeyboardMarkup(row_width=3)
ikb6 = InlineKeyboardMarkup(row_width=3)
ikb7 = InlineKeyboardMarkup(row_width=2)
ikb8 = InlineKeyboardMarkup(row_width=2)
ikb9 = InlineKeyboardMarkup(row_width=3)
ikb10 = InlineKeyboardMarkup(row_width=2)
ikb11 = InlineKeyboardMarkup(row_width=3)

ikb.add(InlineKeyboardButton('Марка', callback_data='mark')).insert(InlineKeyboardButton('Модель', callback_data='model')).add(InlineKeyboardButton('Поколение', callback_data='generation')).insert(InlineKeyboardButton('Рестайлинг', callback_data='restyling')).add(InlineKeyboardButton('Кузов', callback_data='car_body')).insert(InlineKeyboardButton('Цена', callback_data='price')).add(InlineKeyboardButton('Год', callback_data='year')).insert(InlineKeyboardButton('Коробка передач', callback_data='shift_box')).add(InlineKeyboardButton('Топливо', callback_data='fuel')).insert(InlineKeyboardButton('Мощность', callback_data='power')).add(InlineKeyboardButton('Привод', callback_data='drive')).insert(InlineKeyboardButton('Цвет', callback_data='colour')).add(InlineKeyboardButton('Руль', callback_data='wheel')).insert(InlineKeyboardButton('Пробег', callback_data='mileage')).add(InlineKeyboardButton('Назад', callback_data='back2'))
ikb1.add(InlineKeyboardButton('Назад', callback_data='back1')).insert(InlineKeyboardButton('Выход', callback_data='back'))
ikb2.add(InlineKeyboardButton('Назад', callback_data='price')).insert(InlineKeyboardButton('Выход', callback_data='back'))
ikb3.add(InlineKeyboardButton('Назад', callback_data='mileage')).insert(InlineKeyboardButton('Выход', callback_data='back'))
ikb4.add(InlineKeyboardButton('Назад', callback_data='year')).insert(InlineKeyboardButton('Выход', callback_data='back'))
ikb5.add(InlineKeyboardButton('Передний', callback_data='front')).insert(InlineKeyboardButton('Задний', callback_data='rear')).insert(InlineKeyboardButton('Полный', callback_data='full')).add(InlineKeyboardButton('Назад', callback_data='back1')).insert(InlineKeyboardButton('Выход', callback_data='back'))
ikb6.add(InlineKeyboardButton('Белый', callback_data='white')).insert(InlineKeyboardButton('Чёрный', callback_data='black')).insert(InlineKeyboardButton('Коричневый', callback_data='brown')).add(InlineKeyboardButton('Фиолетовый', callback_data='violet')).insert(InlineKeyboardButton('Зелёный', callback_data='green')).insert(InlineKeyboardButton('Серый / Серебристый', callback_data='gray')).add(InlineKeyboardButton('Синий / Голубой', callback_data='blue')).insert(InlineKeyboardButton('Бежевый / Жёлтый / Золотистый', callback_data='yellow')).insert(InlineKeyboardButton('Красный / Бордовый / Оранжевый / Розовый', callback_data='red')).add(InlineKeyboardButton('Назад', callback_data='back3')).insert(InlineKeyboardButton('Выход', callback_data='back4'))
ikb7.add(InlineKeyboardButton('Левый', callback_data='left')).insert(InlineKeyboardButton('Правый', callback_data='right')).add(InlineKeyboardButton('Назад', callback_data='back1')).insert(InlineKeyboardButton('Выход', callback_data='back'))
ikb8.add(InlineKeyboardButton('Назад', callback_data='power')).insert(InlineKeyboardButton('Выход', callback_data='back'))
ikb9.add(InlineKeyboardButton('Бензин', callback_data='benzin')).insert(InlineKeyboardButton('Дизель', callback_data='dizel')).insert(InlineKeyboardButton('Электро', callback_data='electro')).add(InlineKeyboardButton('Гибрид', callback_data='gibrid')).insert(InlineKeyboardButton('ГБО', callback_data='gbo')).add(InlineKeyboardButton('Назад', callback_data='back1')).insert(InlineKeyboardButton('Выход', callback_data='back'))
ikb10.add(InlineKeyboardButton('Автомат', callback_data='auto')).insert(InlineKeyboardButton('Механика', callback_data='mech')).add(InlineKeyboardButton('Назад', callback_data='back1')).insert(InlineKeyboardButton('Выход', callback_data='back'))
ikb11.add(InlineKeyboardButton('Седан', callback_data='sedan')).insert(InlineKeyboardButton('Хэтчбек 5 дв.', callback_data='hatchback5')).insert(InlineKeyboardButton('Хэтчбек 3 дв.', callback_data='hatchback3')).add(InlineKeyboardButton('Лифтбек', callback_data='liftback')).insert(InlineKeyboardButton('Джип 5 дв.', callback_data='jeep5')).insert(InlineKeyboardButton('Джип 3 дв.', callback_data='jeep3')).add(InlineKeyboardButton('Универсал', callback_data='universal')).insert(InlineKeyboardButton('Минивэн', callback_data='miniwen')).insert(InlineKeyboardButton('Пикап', callback_data='pikap')).add(InlineKeyboardButton('Купе', callback_data='kupe')).insert(InlineKeyboardButton('Открытый', callback_data='open')).add(InlineKeyboardButton('Назад', callback_data='back1')).insert(InlineKeyboardButton('Выход', callback_data='back'))

m, m1, m2, m3, m4, m5, m6, m7, m8 = 0, 0, 0, 0, 0, 0, 0, 0, 0 # коэффициенты для добавления и удаления цветов
name = []
k, k1, k2, k3, k4, k5, k6, k7 = 0, 0, 0, 0, 0, 0, 0, 0 # коэффициенты для изменения сообщения о неправильном формате ввода

data_car = {
    'brand': '',
    'model': '',
    'generation': '',
    'restyling': '',
    'car_body': '',
    'min_price': '',
    'max_price': '',
    'min_year': '',
    'max_year': '',
    'shift_box': '',
    'fuel': '',
    'min_power': '',
    'max_power': '',
    'privod': '',
    'colour': '',
    'wheel': '',
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
    waiting_for_get_filter7 = State()
    waiting_for_get_filter8 = State()
    waiting_for_get_filter9 = State()
    waiting_for_get_filter10 = State()
    waiting_for_get_filter11 = State()
    waiting_for_get_filter12 = State()
    waiting_for_get_filter13 = State()
    waiting_for_get_filter14 = State()
    waiting_for_get_filter15 = State()
    waiting_for_get_filter16 = State()
    waiting_for_get_filter17 = State()

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        'Привет! Я слежу за обновлениями с популярных сайтов по продажам машин! Введите фильтры поиска. Если не хотите вводить какой-либо фильтр, то пропустите его, после чего нажмите "начать поиск"',
        reply_markup=kb1)

@dp.message_handler(text='Фильтр')
async def filt(message: types.Message):
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await message.answer("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                         parse_mode='HTML',
                         reply_markup=ikb)
    await message.delete()
    await SetParamsForSearch.waiting_for_filter.set()

@dp.callback_query_handler(text='mark', state='*')
async def mark(callback: types.CallbackQuery, state: FSMContext):
    message = await callback.message.edit_text("Введите название марки машины",
                                               reply_markup=ikb1)
    await state.update_data(message_id=message.message_id)
    await SetParamsForSearch.waiting_for_get_filter15.set()

@dp.callback_query_handler(text='model', state='*')
async def mark(callback: types.CallbackQuery, state: FSMContext):
    message = await callback.message.edit_text("Введите название модели машины",
                                               reply_markup=ikb1)
    await state.update_data(message_id=message.message_id)
    await SetParamsForSearch.waiting_for_get_filter16.set()

@dp.callback_query_handler(text='generation', state='*')
async def mark(callback: types.CallbackQuery, state: FSMContext):
    message = await callback.message.edit_text("Введите поколение машины",
                                               reply_markup=ikb1)
    await state.update_data(message_id=message.message_id)
    await SetParamsForSearch.waiting_for_get_filter17.set()

@dp.callback_query_handler(text='back', state='*')
async def callback(callback: types.CallbackQuery, state: FSMContext):
    global k, k1, k2, k3
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    await state.finish()
    k, k1, k2, k3 = 0, 0, 0, 0

@dp.callback_query_handler(text='back1', state='*')
async def back1(callback: types.CallbackQuery, state: FSMContext):
    global k, k1, k2, k3
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    k, k1, k2, k3 = 0, 0, 0, 0

@dp.callback_query_handler(text='back2', state='*')
async def callback(callback: types.CallbackQuery, state: FSMContext):
    global k, k1, k2, k3
    await callback.message.delete()
    await state.finish()
    k, k1, k2, k3 = 0, 0, 0, 0

@dp.callback_query_handler(text='back3', state='*')
async def callback(callback: types.CallbackQuery, state: FSMContext):
    data_car['colour'] = ', '.join(name)
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)

@dp.callback_query_handler(text='back4', state='*')
async def callback(callback: types.CallbackQuery, state: FSMContext):
    data_car['colour'] = ', '.join(name)
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    await state.finish()

@dp.callback_query_handler(text='mileage', state='*')
async def mileage(callback: types.CallbackQuery, state: FSMContext):
    message = await callback.message.edit_text('Напишите минимальный пробег (в километрах). Можете использовать символы "k" и "m" для сокращения, например:'
                                               '\n\t100k = 100 тыс.\n\t1m = 1 млн.',
                                               reply_markup=ikb1)
    await state.update_data(message_id=message.message_id)
    await SetParamsForSearch.waiting_for_get_filter2.set()

@dp.callback_query_handler(text='price', state='*')
async def price(callback: types.CallbackQuery, state: FSMContext):
    message = await callback.message.edit_text('Напишите минимальную цену (в рублях). Можете использовать символы "k" и "m" для сокращения, например:'
                                               '\n\t100k = 100 тыс.\n\t1m = 1 млн.',
                                               reply_markup=ikb1)
    await state.update_data(message_id = message.message_id)
    await SetParamsForSearch.waiting_for_get_filter.set()

@dp.callback_query_handler(text='year', state='*')
async def year(callback: types.CallbackQuery, state: FSMContext):
    global k4
    message = await callback.message.edit_text(
        'Напишите минимальный год выпуска (не меньше <b>1940-го</b> года).',
        reply_markup=ikb1,
        parse_mode='HTML')
    await state.update_data(message_id = message.message_id)
    await SetParamsForSearch.waiting_for_get_filter4.set()
    k4 = 0

@dp.callback_query_handler(text='drive', state='*')
async def drive(callback: types.Message, state: FSMContext):
    message = await callback.message.edit_text('Выберите нужный вам привод',
                                               reply_markup=ikb5)
    await state.update_data(message_id=message.message_id)
    await SetParamsForSearch.waiting_for_get_filter7.set()

@dp.callback_query_handler(text='colour', state='*')
async def colour(callback: types.Message, state: FSMContext):
    message = await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                               f"\n\t<b>Выбранные цвета:</b> {data_car['colour']}",
                                               parse_mode='HTML',
                                               reply_markup=ikb6)
    await state.update_data(message_id=message.message_id)
    await SetParamsForSearch.waiting_for_get_filter8.set()

@dp.callback_query_handler(text='wheel', state='*')
async def colour(callback: types.Message, state: FSMContext):
    message = await callback.message.edit_text('Выберите нужный вам руль',
                                               reply_markup=ikb7)
    await state.update_data(message_id=message.message_id)
    await SetParamsForSearch.waiting_for_get_filter9.set()

@dp.callback_query_handler(text='power', state='*')
async def power(callback: types.CallbackQuery, state: FSMContext):
    global k6
    message = await callback.message.edit_text(
        'Напишите минимальную мощность (в лошадиных силах).',
        reply_markup=ikb1,
        parse_mode='HTML')
    await state.update_data(message_id = message.message_id)
    await SetParamsForSearch.waiting_for_get_filter10.set()
    k6 = 0

@dp.callback_query_handler(text='fuel', state='*')
async def colour(callback: types.Message, state: FSMContext):
    message = await callback.message.edit_text('Выберите нужное вам топливо',
                                               reply_markup=ikb9)
    await state.update_data(message_id=message.message_id)
    await SetParamsForSearch.waiting_for_get_filter12.set()

@dp.callback_query_handler(text='shift_box', state='*')
async def colour(callback: types.Message, state: FSMContext):
    message = await callback.message.edit_text('Выберите коробку передач',
                                               reply_markup=ikb10)
    await state.update_data(message_id=message.message_id)
    await SetParamsForSearch.waiting_for_get_filter13.set()

@dp.callback_query_handler(text='car_body', state='*')
async def colour(callback: types.Message, state: FSMContext):
    message = await callback.message.edit_text('Выберите тип кузова',
                                               reply_markup=ikb11)
    await state.update_data(message_id=message.message_id)
    await SetParamsForSearch.waiting_for_get_filter14.set()

@dp.callback_query_handler(text='front', state=SetParamsForSearch.waiting_for_get_filter7)
async def drive(callback: types.Message, state: FSMContext):
    data_car['privod'] = 'Передний'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='rear', state=SetParamsForSearch.waiting_for_get_filter7)
async def drive(callback: types.Message, state: FSMContext):
    data_car['privod'] = 'Задний'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='full', state=SetParamsForSearch.waiting_for_get_filter7)
async def drive(callback: types.Message, state: FSMContext):
    data_car['privod'] = 'Полный'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='white', state=SetParamsForSearch.waiting_for_get_filter8)
async def white(callback: types.Message, state: FSMContext):
    global m
    if m == 1:
        name.remove('Белый')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m = 0
    else:
        name.append('Белый')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m += 1

@dp.callback_query_handler(text='black', state=SetParamsForSearch.waiting_for_get_filter8)
async def black(callback: types.Message, state: FSMContext):
    global m1
    if m1 == 1:
        name.remove('Чёрный')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m1 = 0
    else:
        name.append('Чёрный')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m1 += 1

@dp.callback_query_handler(text='brown', state=SetParamsForSearch.waiting_for_get_filter8)
async def brown(callback: types.Message, state: FSMContext):
    global m2
    if m2 == 1:
        name.remove('Коричневый')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m2 = 0
    else:
        name.append('Коричневый')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m2 += 1

@dp.callback_query_handler(text='violet', state=SetParamsForSearch.waiting_for_get_filter8)
async def violet(callback: types.Message, state: FSMContext):
    global m3
    if m3 == 1:
        name.remove('Фиолетовый')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m3 = 0
    else:
        name.append('Фиолетовый')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m3 += 1

@dp.callback_query_handler(text='green', state=SetParamsForSearch.waiting_for_get_filter8)
async def green(callback: types.Message, state: FSMContext):
    global m4
    if m4 == 1:
        name.remove('Зелёный')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m4 = 0
    else:
        name.append('Зелёный')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m4 += 1

@dp.callback_query_handler(text='gray', state=SetParamsForSearch.waiting_for_get_filter8)
async def gray(callback: types.Message, state: FSMContext):
    global m5
    if m5 == 1:
        name.remove('Серый / Серебристый')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m5 = 0
    else:
        name.append('Серый / Серебристый')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m5 += 1

@dp.callback_query_handler(text='blue', state=SetParamsForSearch.waiting_for_get_filter8)
async def blue(callback: types.Message, state: FSMContext):
    global m6
    if m6 == 1:
        name.remove('Синий / Голубой')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m6 = 0
    else:
        name.append('Синий / Голубой')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m6 += 1

@dp.callback_query_handler(text='yellow', state=SetParamsForSearch.waiting_for_get_filter8)
async def yellow(callback: types.Message, state: FSMContext):
    global m7
    if m7 == 1:
        name.remove('Бежевый / Желтый / Золотистый')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m7 = 0
    else:
        name.append('Бежевый / Желтый / Золотистый')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m7 += 1

@dp.callback_query_handler(text='red', state=SetParamsForSearch.waiting_for_get_filter8)
async def red(callback: types.Message, state: FSMContext):
    global m8
    if m8 == 1:
        name.remove('Красный / Бордовый / Оранжевый / Розовый')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m8 = 0
    else:
        name.append('Красный / Бордовый / Оранжевый / Розовый')
        a = ', '.join(name)
        await callback.message.edit_text('Укажите нужные вам цвета, после чего выйдите из выбора цвета. Если хотите убрать выбранный цвет, нажмите на него ещё раз.'
                                         f'\n\t<b>Выбранные цвета:</b> {a} ',
                                         reply_markup=ikb6,
                                         parse_mode='HTML')
        m8 += 1

@dp.callback_query_handler(text='left', state=SetParamsForSearch.waiting_for_get_filter9)
async def left(callback: types.Message, state: FSMContext):
    data_car['wheel'] = 'Левый'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='right', state=SetParamsForSearch.waiting_for_get_filter9)
async def right(callback: types.Message, state: FSMContext):
    data_car['wheel'] = 'Правый'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='benzin', state=SetParamsForSearch.waiting_for_get_filter12)
async def benzin(callback: types.Message, state: FSMContext):
    data_car['fuel'] = 'Бензин'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='dizel', state=SetParamsForSearch.waiting_for_get_filter12)
async def dizel(callback: types.Message, state: FSMContext):
    data_car['fuel'] = 'Дизель'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='electro', state=SetParamsForSearch.waiting_for_get_filter12)
async def electro(callback: types.Message, state: FSMContext):
    data_car['fuel'] = 'Электро'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='gibrid', state=SetParamsForSearch.waiting_for_get_filter12)
async def gibrid(callback: types.Message, state: FSMContext):
    data_car['fuel'] = 'Гибрид'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='gbo', state=SetParamsForSearch.waiting_for_get_filter12)
async def gbo(callback: types.Message, state: FSMContext):
    data_car['fuel'] = 'ГБО'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='auto', state=SetParamsForSearch.waiting_for_get_filter13)
async def auto(callback: types.Message, state: FSMContext):
    data_car['shift_box'] = 'Автомат'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='mech', state=SetParamsForSearch.waiting_for_get_filter13)
async def mech(callback: types.Message, state: FSMContext):
    data_car['shift_box'] = 'Механика'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='sedan', state=SetParamsForSearch.waiting_for_get_filter14)
async def sedan(callback: types.Message, state: FSMContext):
    data_car['car_body'] = 'Седан'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='hatchback5', state=SetParamsForSearch.waiting_for_get_filter14)
async def hatchback5(callback: types.Message, state: FSMContext):
    data_car['car_body'] = 'Хэтчбек 5 дв.'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='hatchback3', state=SetParamsForSearch.waiting_for_get_filter14)
async def hatchback3(callback: types.Message, state: FSMContext):
    data_car['car_body'] = 'Хэтчбек 3 дв.'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='liftback', state=SetParamsForSearch.waiting_for_get_filter14)
async def liftback(callback: types.Message, state: FSMContext):
    data_car['car_body'] = 'Лифтбек'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='jeep5', state=SetParamsForSearch.waiting_for_get_filter14)
async def jeep5(callback: types.Message, state: FSMContext):
    data_car['car_body'] = 'Джип 5 дв.'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='jeep3', state=SetParamsForSearch.waiting_for_get_filter14)
async def jeep3(callback: types.Message, state: FSMContext):
    data_car['car_body'] = 'Джип 3 дв.'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='universal', state=SetParamsForSearch.waiting_for_get_filter14)
async def universal(callback: types.Message, state: FSMContext):
    data_car['car_body'] = 'Универсал'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='miniwen', state=SetParamsForSearch.waiting_for_get_filter14)
async def miniwen(callback: types.Message, state: FSMContext):
    data_car['car_body'] = 'Минивэн'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='pikap', state=SetParamsForSearch.waiting_for_get_filter14)
async def pikap(callback: types.Message, state: FSMContext):
    data_car['car_body'] = 'Пикап'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='kupe', state=SetParamsForSearch.waiting_for_get_filter14)
async def kupe(callback: types.Message, state: FSMContext):
    data_car['car_body'] = 'Купе'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.callback_query_handler(text='open', state=SetParamsForSearch.waiting_for_get_filter14)
async def open(callback: types.Message, state: FSMContext):
    data_car['car_body'] = 'Открытый'
    mi = []
    mi.append(data_car['min_probeg'])
    mi.append(data_car['max_probeg'])
    mileage = ' - '.join(mi)
    pr = []
    pr.append(data_car['min_price'])
    pr.append(data_car['max_price'])
    price = ' - '.join(pr)
    ye = []
    ye.append(data_car['min_year'])
    ye.append(data_car['max_year'])
    year = ' - '.join(ye)
    po = []
    po.append(data_car['min_power'])
    po.append(data_car['max_power'])
    power = ' - '.join(po)
    if price == ' - ': price = ''
    else: price = price
    if mileage == ' - ': mileage = ''
    else: mileage = mileage
    if year == ' - ': year = ''
    else: year = year
    if power == ' - ': power = ''
    else: power = power
    await callback.message.edit_text("Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
                                     parse_mode='HTML',
                                     reply_markup=ikb)
    print(data_car)

@dp.message_handler(lambda message: not message.text.isdigit() and not re.match(pattern, message.text), state=SetParamsForSearch.waiting_for_get_filter)
async def check(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data['message_id']
        global k, k1
        if k == 0:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message_id,
                text='<b>Неправильный формат ввода!</b> Напишите минимальную цену (в рублях). Можете использовать символы "k" и "m" для сокращения, например:'
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
                text='<b>Неправильный формат ввода!</b> Напишите максимальную цену (в рублях). Можете использовать символы "k" и "m" для сокращения, например:'
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
                text='<b>Неправильный формат ввода!</b> Напишите минимальный пробег (в километрах). Можете использовать символы "k" и "m" для сокращения, например:'
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
                text='<b>Неправильный формат ввода!</b> Напишите максимальный пробег (в километрах). Можете использовать символы "k" и "m" для сокращения, например:'
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

@dp.message_handler(lambda message: not message.text.isdigit(), state=SetParamsForSearch.waiting_for_get_filter10)
async def check6(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data['message_id']
        global k6, k7
        if k6 == 0:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message_id,
                text='<b>Неправильный формат ввода!</b> Напишите минимальную мощность (в лошадиных силах)',
                parse_mode='HTML',
                reply_markup=ikb1
            )
            await message.delete()
            k6 += 1
        else:
            await message.delete()
        k7 = 0

@dp.message_handler(lambda message: not message.text.isdigit(), state=SetParamsForSearch.waiting_for_get_filter11)
async def check5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data['message_id']
        global k7
        if k7 == 0:
            await bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=message_id,
                text='<b>Неправильный формат ввода!</b> Напишите максимальную мощность (в лошадиных силах)',
                parse_mode='HTML',
                reply_markup=ikb4
            )
            await message.delete()
            k7 += 1
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
        await message.delete()
        text = message.text
        if re.match(pattern1, text):
            text = str(int(text[:text.find('k')]) * 10 ** 3)
        elif re.match(pattern2, text):
            text = str(int(text[:text.find('m')]) * 10 ** 6)
        data['max_price'] = text
        data_car['max_price'] = data['max_price']
        mi = []
        mi.append(data_car['min_probeg'])
        mi.append(data_car['max_probeg'])
        mileage = ' - '.join(mi)
        pr = []
        pr.append(data_car['min_price'])
        pr.append(data_car['max_price'])
        price = ' - '.join(pr)
        ye = []
        ye.append(data_car['min_year'])
        ye.append(data_car['max_year'])
        year = ' - '.join(ye)
        po = []
        po.append(data_car['min_power'])
        po.append(data_car['max_power'])
        power = ' - '.join(po)
        if price == ' - ': price = ''
        else: price = price
        if mileage == ' - ': mileage = ''
        else: mileage = mileage
        if year == ' - ': year = ''
        else: year = year
        if power == ' - ': power = ''
        else: power = power
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text="Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
            parse_mode='HTML',
            reply_markup=ikb)
        print(data_car['max_price'])
        k1 = 0
        await SetParamsForSearch.waiting_for_get_filter2.set()

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
        await message.delete()
        text = message.text
        if re.match(pattern1, text):
            text = str(int(text[:text.find('k')]) * 10 ** 3)
        elif re.match(pattern2, text):
            text = str(int(text[:text.find('m')]) * 10 ** 6)
        data['max_probeg'] = text
        data_car['max_probeg'] = data['max_probeg']
        mi = []
        mi.append(data_car['min_probeg'])
        mi.append(data_car['max_probeg'])
        mileage = ' - '.join(mi)
        pr = []
        pr.append(data_car['min_price'])
        pr.append(data_car['max_price'])
        price = ' - '.join(pr)
        ye = []
        ye.append(data_car['min_year'])
        ye.append(data_car['max_year'])
        year = ' - '.join(ye)
        po = []
        po.append(data_car['min_power'])
        po.append(data_car['max_power'])
        power = ' - '.join(po)
        if price == ' - ': price = ''
        else: price = price
        if mileage == ' - ': mileage = ''
        else: mileage = mileage
        if year == ' - ': year = ''
        else: year = year
        if power == ' - ': power = ''
        else: power = power
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text="Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
            parse_mode='HTML',
            reply_markup=ikb)
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
        data['max_year'] = message.text
        data_car['max_year'] = data['max_year']
        mi = []
        mi.append(data_car['min_probeg'])
        mi.append(data_car['max_probeg'])
        mileage = ' - '.join(mi)
        pr = []
        pr.append(data_car['min_price'])
        pr.append(data_car['max_price'])
        price = ' - '.join(pr)
        ye = []
        ye.append(data_car['min_year'])
        ye.append(data_car['max_year'])
        year = ' - '.join(ye)
        po = []
        po.append(data_car['min_power'])
        po.append(data_car['max_power'])
        power = ' - '.join(po)
        if price == ' - ': price = ''
        else: price = price
        if mileage == ' - ': mileage = ''
        else: mileage = mileage
        if year == ' - ': year = ''
        else: year = year
        if power == ' - ': power = ''
        else: power = power
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text="Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
            parse_mode='HTML',
            reply_markup=ikb)
        await message.delete()
        print(data_car)

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter10)
async def add_filter10(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data['message_id']
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text='Теперь введите максимальную мощность (в лошадиных силах)',
            reply_markup=ikb8
        )
        await message.delete()
        text = message.text
        data['min_power'] = text
        data_car['min_power'] = data['min_power']
        await SetParamsForSearch.waiting_for_get_filter11.set()
        print(data_car)

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter11)
async def add_filter11(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data['message_id']
        text = message.text
        data['max_power'] = text
        data_car['max_power'] = data['max_power']
        mi = []
        mi.append(data_car['min_probeg'])
        mi.append(data_car['max_probeg'])
        mileage = ' - '.join(mi)
        pr = []
        pr.append(data_car['min_price'])
        pr.append(data_car['max_price'])
        price = ' - '.join(pr)
        ye = []
        ye.append(data_car['min_year'])
        ye.append(data_car['max_year'])
        year = ' - '.join(ye)
        po = []
        po.append(data_car['min_power'])
        po.append(data_car['max_power'])
        power = ' - '.join(po)
        if price == ' - ': price = ''
        else: price = price
        if mileage == ' - ': mileage = ''
        else: mileage = mileage
        if year == ' - ': year = ''
        else: year = year
        if power == ' - ': power = ''
        else: power = power
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text="Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
            parse_mode='HTML',
            reply_markup=ikb)
        await message.delete()
        print(data_car)

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter15)
async def add_filter15(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data['message_id']
        text = message.text
        data['brand'] = text
        data_car['brand'] = data['brand']
        mi = []
        mi.append(data_car['min_probeg'])
        mi.append(data_car['max_probeg'])
        mileage = ' - '.join(mi)
        pr = []
        pr.append(data_car['min_price'])
        pr.append(data_car['max_price'])
        price = ' - '.join(pr)
        ye = []
        ye.append(data_car['min_year'])
        ye.append(data_car['max_year'])
        year = ' - '.join(ye)
        po = []
        po.append(data_car['min_power'])
        po.append(data_car['max_power'])
        power = ' - '.join(po)
        if price == ' - ': price = ''
        else: price = price
        if mileage == ' - ': mileage = ''
        else: mileage = mileage
        if year == ' - ': year = ''
        else: year = year
        if power == ' - ': power = ''
        else: power = power
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text="Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
            parse_mode='HTML',
            reply_markup=ikb)
        await message.delete()
        print(data_car)

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter16)
async def add_filter16(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data['message_id']
        text = message.text
        data['model'] = text
        data_car['model'] = data['model']
        mi = []
        mi.append(data_car['min_probeg'])
        mi.append(data_car['max_probeg'])
        mileage = ' - '.join(mi)
        pr = []
        pr.append(data_car['min_price'])
        pr.append(data_car['max_price'])
        price = ' - '.join(pr)
        ye = []
        ye.append(data_car['min_year'])
        ye.append(data_car['max_year'])
        year = ' - '.join(ye)
        po = []
        po.append(data_car['min_power'])
        po.append(data_car['max_power'])
        power = ' - '.join(po)
        if price == ' - ': price = ''
        else: price = price
        if mileage == ' - ': mileage = ''
        else: mileage = mileage
        if year == ' - ': year = ''
        else: year = year
        if power == ' - ': power = ''
        else: power = power
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text="Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
            parse_mode='HTML',
            reply_markup=ikb)
        await message.delete()
        print(data_car)

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter17)
async def add_filter17(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        message_id = data['message_id']
        text = message.text
        data['generation'] = text
        data_car['generation'] = data['generation']
        mi = []
        mi.append(data_car['min_probeg'])
        mi.append(data_car['max_probeg'])
        mileage = ' - '.join(mi)
        pr = []
        pr.append(data_car['min_price'])
        pr.append(data_car['max_price'])
        price = ' - '.join(pr)
        ye = []
        ye.append(data_car['min_year'])
        ye.append(data_car['max_year'])
        year = ' - '.join(ye)
        po = []
        po.append(data_car['min_power'])
        po.append(data_car['max_power'])
        power = ' - '.join(po)
        if price == ' - ': price = ''
        else: price = price
        if mileage == ' - ': mileage = ''
        else: mileage = mileage
        if year == ' - ': year = ''
        else: year = year
        if power == ' - ': power = ''
        else: power = power
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=message_id,
            text="Выберите фильтр""\n""\n<b>Выбранные фильтры:</b>"f"\nМарка: {data_car['brand']}"f"\nМодель: {data_car['model']}"f"\nПоколение: {data_car['generation']}"f"\nРестайлинг: {data_car['restyling']}"f"\nКузов: {data_car['car_body']}"f"\nЦена: {price}"f"\nГод: {year}"f"\nКоробка передач: {data_car['shift_box']}"f"\nТопливо: {data_car['fuel']}"f"\nЛошадиные силы: {power}"f"\nПривод: {data_car['privod']}"f"\nЦвет: {data_car['colour']}"f"\nРуль: {data_car['wheel']}"f"\nПробег: {mileage}",
            parse_mode='HTML',
            reply_markup=ikb)
        await message.delete()
        print(data_car)

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter7)
async def add_filter7(message: types.Message, state: FSMContext):
    await message.delete()

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter8)
async def add_filter8(message: types.Message, state: FSMContext):
    await message.delete()

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter9)
async def add_filter9(message: types.Message, state: FSMContext):
    await message.delete()

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter12)
async def add_filter9(message: types.Message, state: FSMContext):
    await message.delete()

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter13)
async def add_filter9(message: types.Message, state: FSMContext):
    await message.delete()

@dp.message_handler(state=SetParamsForSearch.waiting_for_get_filter14)
async def add_filter9(message: types.Message, state: FSMContext):
    await message.delete()

if __name__ == '__main__':
    executor.start_polling(dp)
