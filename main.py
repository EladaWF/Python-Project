import telebot
import pyowm
import math
import requests
import random
from bs4 import BeautifulSoup
from googletrans import Translator

owm = pyowm.OWM('0f81e7f1a436b2ea18e7caded7d03a50')
keyboard_main = telebot.types.ReplyKeyboardMarkup(True)
keyboard_main.row('Камень ножницы бумага', 'Перевод', "Калькулятор")
keyboard_main.row("Погода", "Курс", "Covid")
keyboard_main.row("Новость с панорамы")
keyboard_main.row("Подбросить монетку")
keyboard_rock = telebot.types.ReplyKeyboardMarkup(True)
keyboard_rock.row('Камень', 'Ножницы', 'Бумага')
keyboard_calc = telebot.types.ReplyKeyboardMarkup(True)
keyboard_calc.row('-', '+', '*', '/')
calc_num1 = 0.0
calc_action = ""
keyboard_remove = telebot.types.ReplyKeyboardRemove()
bot = telebot.TeleBot('2120606905:AAHImKnKJ4BF-ySPAujfypN6Y-WnJz3-Cms')


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, "Привет! Я бот разработанный студентом третьего курса ИКБСП. Я могу поиграть с "
                                      "Вами в \"камень, ножницы, бумага\", перевести что-нибудь, предоставить Вам "
                                      "простенький калькулятор и показать погоду в Москве. Если возникнут трудности,"
                                      " напишите команду /help.", reply_markup=keyboard_main)


@bot.message_handler(commands=['help'])
def start_command(message):
    bot.send_message(message.chat.id, "Напишите \"Камень ножницы бумага\", чтобы поиграть. Чтобы я показал погоду "
                                      "напишите \"Погода\", чтобы открыть калькулятор напишите \"Калькулятор\", "
                                      "чтобы перевести что-нибудь напишите \"Перевод\"")


@bot.message_handler(content_types=['text'])
def get_start_message(message):
    if message.text == "Камень ножницы бумага":
        bot.send_message(message.chat.id, "Выберите камень, ножницы или бумагу", reply_markup=keyboard_rock)
        bot.register_next_step_handler(message, rock_paper)
    elif message.text == "Перевод":
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='RU', callback_data=1))
        markup.add(telebot.types.InlineKeyboardButton(text='EN ', callback_data=2))
        bot.send_message(message.chat.id, "Выбери язык на который хотите перевести текст.", reply_markup=markup)
    elif message.text == "Калькулятор":
        bot.send_message(message.chat.id, "Запускаю калькулятор", reply_markup=keyboard_remove)
        bot.send_message(message.chat.id, "Напишите первое число:")
        bot.register_next_step_handler(message, calc_start)
    elif message.text == "Погода":
        bot.send_message(message.chat.id, "Смотрю погоду")
        weather(message.chat.id)
    elif message.text == "Курс":
        currency_message(message.chat.id)
    elif message.text == "Covid":
        info_message(message.chat.id)
    elif message.text == "Новость с панорамы":
        panorama_message(message.chat.id)
    elif message.text == "Подбросить монетку":
        monetka(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Я вас не понял :(", reply_markup=keyboard_main)


def rock_paper(message):
    mes = message.text.lower()
    if mes != 'камень' and mes != 'ножницы' and mes != 'бумага':
        bot.send_message(message.chat.id, "Я вас не понял, повторите ввод правильно.")
        bot.register_next_step_handler(message, rock_paper)
        return
    bot_choice = random.randint(1, 3)
    if bot_choice == 1:
        bot_choice = "камень"
    elif bot_choice == 2:
        bot_choice = "ножницы"
    elif bot_choice == 3:
        bot_choice = "бумага"
    bot.send_message(message.chat.id, "Я выбрал - " + bot_choice + " , Вы выбрали - " + mes)
    if mes == "камень" and bot_choice == "камень":
        bot.send_message(message.chat.id, "У нас ничья :/", reply_markup=keyboard_main)
    elif mes == "ножницы" and bot_choice == "ножницы":
        bot.send_message(message.chat.id, "У нас ничья :/", reply_markup=keyboard_main)
    elif mes == "бумага" and bot_choice == "бумага":
        bot.send_message(message.chat.id, "У нас ничья :/", reply_markup=keyboard_main)
    elif mes == "камень" and bot_choice == "ножницы":
        bot.send_message(message.chat.id, "Увы! Я проиграл :( С победой!", reply_markup=keyboard_main)
    elif mes == "ножницы" and bot_choice == "камень":
        bot.send_message(message.chat.id, "Ура! Я победил :) Вы проиграли!", reply_markup=keyboard_main)
    elif mes == "камень" and bot_choice == "бумага":
        bot.send_message(message.chat.id, "Ура! Я победил :) Вы проиграли!", reply_markup=keyboard_main)
    elif mes == "бумага" and bot_choice == "камень":
        bot.send_message(message.chat.id, "Увы! Я проиграл :( С победой!", reply_markup=keyboard_main)
    elif mes == "бумага" and bot_choice == "ножницы":
        bot.send_message(message.chat.id, "Ура! Я победил :) Вы проиграли!", reply_markup=keyboard_main)
    elif mes == "ножницы" and bot_choice == "бумага":
        bot.send_message(message.chat.id, "Увы! Я проиграл :( С победой!", reply_markup=keyboard_main)


def calc_start(message):
    global calc_num1
    try:
        calc_num1 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Вы ввели что-то не понятное. Повторите ввод заново")
        bot.register_next_step_handler(message, calc_start)
        return
    bot.send_message(message.chat.id, "Введите операцию:", reply_markup=keyboard_calc)
    bot.register_next_step_handler(message, calc_op)


def calc_op(message):
    global calc_action
    calc_action = str(message.text)
    bot.send_message(message.chat.id, "Введите второе число:", reply_markup=keyboard_remove)
    bot.register_next_step_handler(message, calc_second)


def calc_second(message):
    try:
        calc_num2 = float(message.text)
    except ValueError:
        bot.send_message(message.chat.id, "Вы ввели что-то не понятное. Повторите ввод заново")
        bot.register_next_step_handler(message, calc_second)
        return
    if calc_action == '+':
        bot.send_message(message.chat.id, "Результат: " + str(calc_num1 + calc_num2), reply_markup=keyboard_main)
    elif calc_action == '-':
        bot.send_message(message.chat.id, "Результат: " + str(calc_num1 - calc_num2), reply_markup=keyboard_main)
    elif calc_action == '*':
        bot.send_message(message.chat.id, "Результат: " + str(calc_num1 * calc_num2), reply_markup=keyboard_main)
    elif calc_action == '/':
        if calc_num2 == 0:
            bot.send_message(message.chat.id, "На ноль делить нельзя!", reply_markup=keyboard_main)
            return
        bot.send_message(message.chat.id, "Результат: " + str(calc_num1 / calc_num2), reply_markup=keyboard_main)


translator = Translator()


def next_trans2(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text = message.text
        lang = 'ru'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)


def next_trans3(message):
    try:
        text = int(message.text)
        bot.send_message(message.chat.id, "Это не текст!")
    except:
        text = message.text
        lang = 'en'
        res = translator.translate(text, dest=lang)
        bot.send_message(message.chat.id, res.text)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id)
    answer = ''
    if call.data == '1':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data=4))
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Введите текст для перевода", reply_markup=markup)
        bot.register_next_step_handler(msg, next_trans2)
    elif call.data == '2':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Выбрать другой язык', callback_data=3))
        markup.add(telebot.types.InlineKeyboardButton(text='Отмена', callback_data=4))
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Введите текст для перевода", reply_markup=markup)
        bot.register_next_step_handler(msg, next_trans3)
    elif call.data == '3':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='RU', callback_data=1))
        markup.add(telebot.types.InlineKeyboardButton(text='EN ', callback_data=2))
        msg = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text="Выбери язык на который хотите перевести текст.", reply_markup=markup)
    elif call.data == '4':
        markup = telebot.types.InlineKeyboardMarkup()
        markup.add(telebot.types.InlineKeyboardButton(text='Перевод', callback_data=3))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Вы вернулись в главное меню!", reply_markup=markup)


def weather(id):
    try:
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place('Moscow, RU')
        w = observation.weather
        temp = w.temperature('celsius')["temp"]
        temp_max = w.temperature('celsius')["temp_max"]
        temp_min = w.temperature('celsius')["temp_min"]
        wind = w.wind()["speed"]
        status = w.detailed_status
        humidity = w.humidity

        t = round(temp)
        t_max = math.ceil(temp_max)
        t_min = math.floor(temp_min)

        lang = 'ru'
        res = translator.translate(str(status), dest=lang)
        answer = "В Москве сейчас {}\n".format(res.text)
        answer += "Температура ~ {}°C \n".format(str(t))
        answer += "Макс. {}°C \n".format(str(t_max))
        answer += "Мин. {}°C \n".format(str(t_min))
        answer += "Влажность {}% \n".format(str(humidity))
        answer += "Скорость ветра составляет {} м/с \n\n".format(str(wind))

        if t <= 10:
            answer += "На улице холодно, одевайся теплее!\n"
        elif t <= 18:
            answer += "На улице прохладно, захвати с собой кофту!\n"
        elif t <= 25:
            answer += "На улице тепло, иди гуляй!\n"
        else:
            answer += "На улице жара!\n"

        if str(status) == "дождь":
            answer += "Не забудь зонт, ты же не хочешь промокнуть?"
        elif str(status) == "легкий дождь":
            answer += "Зонт возьми, вдруг польет сильнее?"
        elif str(status) == "пасмурно" and (humidity > 50):
            answer += "Возможен дождь, но это не точно"

        bot.send_message(id, answer)
    except Exception:
        bot.send_message(id, "Произошла ошибка, попробуй еще раз")

def currency_message(id):
    response = requests.get('https://www.cbr-xml-daily.ru/latest.js').json()["rates"]
    formed_str = f'Текущий курс:\n' \
                 f'1 USD = {round(1/response["USD"], 2)}\n' \
                 f'1 EUR = {round(1/response["EUR"], 2)}'
    bot.send_message(id, formed_str)

def info_message(id):
    response = requests.get('https://yastat.net/s3/milab/2020/covid19-stat/data/v10/data-by-region/213.json').json()["info"]
    formed_str = f'Население Москвы: {response["population"]}\n' \
                f'Выявлено заражений: {response["cases"]}\n' \
                f'Заражений за пследние сутки: {response["cases_delta"]}\n' \
                f'Зарегестрировано смертей: {response["deaths"]}\n' \
                f'Смертей за пследние сутки: {response["deaths_delta"]}\n' \
                f'Актуально на {response["date"]}'
    bot.send_message(id, formed_str)

def panorama_message(id):
    main_page = requests.get("https://panorama.pub/")
    soup = BeautifulSoup(main_page.text, 'lxml')
    news = soup.select('.news .entry')
    selected_news = random.choice(news)
    news_header = selected_news.select('h3')[0].text.replace("</h3>", '').replace("<h3>", '')
    bot.send_message(id, news_header)

def monetka(id):
    coin_state = random.randint(0, 1)
    if coin_state == 0:
        coin_state = 'Орел'
    else:
        coin_state = 'Решка'
    bot.send_message(id, coin_state)

bot.polling(none_stop=True, interval=0)