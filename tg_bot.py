import telebot
from telebot import types
import psycopg2
import datetime

def data(day1, symbol):
    conn = psycopg2.connect(database="mtuci_timetable",
                            user="postgres",
                            password="Hfnfneq2005",
                            host = "localhost",
                            port = "5432")
    cursor = conn.cursor()

    query = "SELECT timetable.id, timetable.day, subjects.name, timetable.room_numb, TO_CHAR(timetable.start_time,'HH24:MI'), teacher.full_name FROM timetable JOIN subjects ON timetable.subject = subjects.name JOIN teacher ON timetable.subject = teacher.subject WHERE day=%s AND timetable.id {} 12 ORDER BY id".format(symbol)

    cursor.execute(query, (day1,))
    result = cursor.fetchall()

    output = ""
    output1 = ""

    for row in result:
        output += f"{row[2]} {row[3]} {row[4]} {row[5]}" + "\n\n"
        output1 = row[1] + "\n" + "______________\n" + output + "______________\n\n\n"
    return output1

def date():
    now = datetime.date.today()
    a = datetime.date(2023,2,6)
    b = now-a
    c = str(b)
    d = c.split()[0]
    e = int(d)//7
    if e % 2 == 0:
        return True
    else:
        return False

token = "6036268745:AAFJ0U40JmPH9Dqj7fIDgRPkQfNtIRqXyIw"

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Понедельник","Вторник","Среда","Четверг","Пятница","Расписание на текущую неделю","Расписание на следующую неделю", "/week", "/mtuci", "/help")
    bot.send_message(message.chat.id, 'Привет! На какой день вы хотите узнать расписание?', reply_markup=keyboard)


@bot.message_handler(commands=['mtuci'])
def mtuci(message):
    bot.send_message(message.chat.id, 'Здесь ты можешь узнать свежую информацию о МТУСИ - https://mtuci.ru/')


@bot.message_handler(commands=['week'])
def week(message):
    if date():
        bot.send_message(message.chat.id, 'Сейчас чётная неделя')
    if not date():
        bot.send_message(message.chat.id, 'Сейчас нечётная неделя')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Я бот, показывающий расписание для вашей группы. Выберите нужный вам день или неделю из предоставленных ниже кнопок, чтобы узнать нужную вам информацию.\nТакже у меня есть несколько команд, которыми вы можете воспользоваться:\n/week - Узнать какая сейчас неделя (чётная или нечётная)\n/mtuci - Узнать свежую информацию о МТУСИ')


@bot.message_handler(content_types=['text'])
def answer(message):
    if date():
        symbol = '<='
        if message.text.lower() == "понедельник":
            day1 = 'Понедельник'
            output1 = data(day1,symbol)
            bot.send_message(message.chat.id, output1)
        if message.text.lower() == "вторник":
            bot.send_message(message.chat.id, "Вторник" + "\n" + "______________\n" + "Нет пар\n" + "______________\n")
        if message.text.lower() == "среда":
            day1 = 'Среда'
            output1 = data(day1,symbol)
            bot.send_message(message.chat.id, output1)
        if message.text.lower() == "четверг":
            day1 = 'Четверг'
            output1 = data(day1,symbol)
            bot.send_message(message.chat.id, output1)
        if message.text.lower() == "пятница":
            day1 = 'Пятница'
            output1 = data(day1,symbol)
            bot.send_message(message.chat.id, output1)
    if not date():
        symbol = ">="
        if message.text.lower() == "понедельник":
            day1 = 'Понедельник'
            output1 = data(day1,symbol)
            bot.send_message(message.chat.id, output1)
        if message.text.lower() == "вторник":
            day1 = 'Вторник'
            output1 = data(day1,symbol)
            bot.send_message(message.chat.id, output1)
        if message.text.lower() == "среда":
            day1 = 'Среда'
            output1 = data(day1,symbol)
            bot.send_message(message.chat.id, output1)
        if message.text.lower() == "четверг":
            bot.send_message(message.chat.id, "Четверг" + "\n" + "______________\n" + "Нет пар" + "______________\n")
        if message.text.lower() == "пятница":
            day1 = 'Пятница'
            output1 = data(day1,symbol)
            bot.send_message(message.chat.id, output1)
    if message.text.lower() == 'расписание на текущую неделю':
        if date():
            output1 = ''
            symbol = '<='
            day1 = 'Понедельник'
            output1 += data(day1, symbol)
            output1 += "Вторник" + "\n" + "______________\n" + "Нет пар\n" + "______________\n\n\n"
            day1 = 'Среда'
            output1 += data(day1, symbol)
            day1 = 'Четверг'
            output1 += data(day1, symbol)
            day1 = 'Пятница'
            output1 += data(day1, symbol)
            bot.send_message(message.chat.id, output1)
        if not date():
            symbol = ">="
            output1 = ''
            day1 = 'Понедельник'
            output1 += data(day1, symbol)
            day1 = 'Вторник'
            output1 += data(day1, symbol)
            day1 = 'Среда'
            output1 += data(day1, symbol)
            output1 += ("Четверг" + "\n" + "______________\n" + "Нет пар" + "______________\n\n\n")
            day1 = 'Пятница'
            output1 += data(day1, symbol)
            bot.send_message(message.chat.id, output1)
    if message.text.lower() == 'расписание на следующую неделю':
        if not date():
            output1 = ''
            symbol = '<='
            day1 = 'Понедельник'
            output1 += data(day1, symbol)
            output1 += "Вторник" + "\n" + "______________\n" + "Нет пар\n" + "______________\n\n\n"
            day1 = 'Среда'
            output1 += data(day1, symbol)
            day1 = 'Четверг'
            output1 += data(day1, symbol)
            day1 = 'Пятница'
            output1 += data(day1, symbol)
            bot.send_message(message.chat.id, output1)
        if date():
            symbol = ">="
            output1 = ''
            day1 = 'Понедельник'
            output1 += data(day1, symbol)
            day1 = 'Вторник'
            output1 += data(day1, symbol)
            day1 = 'Среда'
            output1 += data(day1, symbol)
            output1 += ("Четверг" + "\n" + "______________\n" + "Нет пар\n" + "______________\n\n\n")
            day1 = 'Пятница'
            output1 += data(day1, symbol)
            bot.send_message(message.chat.id, output1)
    if message.text.lower() != "понедельник" and message.text.lower() != "вторник" and message.text.lower() != "среда" and message.text.lower() != "четверг" and message.text.lower() != "пятница" and message.text.lower() != "расписание на текущую неделю" and message.text.lower() != "расписание на следующую неделю":
        bot.send_message(message.chat.id, 'Извините, я Вас не понял')

bot.infinity_polling()