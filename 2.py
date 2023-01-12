# -*- coding: utf-8 -*-
import time
import pandas as pd
import password
from binance.client import Client
#from aiogram.dispatcher import Dispatcher
import telebot
from telebot import types
TOKEN = "5423197672:AAFPPlk1OgEomXa_F0kXclBdeLX7G_-zhaI"
# Адрес телеграм-канала, начинается с @
# user_id = message.from_user.id
# user_first_name = message.from_user.first_name
# user_last_name = message.from_user.last_name
# user_username = message.from_user.username

# Создаем бота
bot = telebot.TeleBot(TOKEN)
#dp = Dispatcher(bot)
CHANNEL_NAME = '-609825876'
# Команда start

def menu1():
    # Добавляем две кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itemnp = types.KeyboardButton("Навигационная панель")
    item1 = types.KeyboardButton("урок 1")
    item2 = types.KeyboardButton("урок 2")
    item3 = types.KeyboardButton("код")
    item4 = types.KeyboardButton("создание кошелька")

    markup.add(itemnp)
    markup.add(item1,item2)
    markup.add(item3,item4)
    bot.send_message(CHANNEL_NAME, '🦾 Навигационная панель 👁', reply_markup=markup)

def menu2():
    # Добавляем две кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    itemnp = types.KeyboardButton("Навигационная панель")
    itemsp = types.KeyboardButton("Синтаксис python")
    itemii = types.KeyboardButton("что такое искусственный интеллект")
    itemml = types.KeyboardButton("что такое машинное обучение")
    itemgl = types.KeyboardButton("что такое глубокое обучение")
    itemnd = types.KeyboardButton("что такое набор данных")
    itemds = types.KeyboardButton("что такое датасет")
    itemns = types.KeyboardButton("что такое нейросети")

    itemir = types.KeyboardButton("историю развития")
    itemssml = types.KeyboardButton("современное состояние сферы машинного обучения")
    itemspr = types.KeyboardButton("ссылки на полезные ресурсы")

    markup.add(itemsp)
    markup.add(itemnp)
    markup.add(itemii)
    markup.add(itemml,itemgl)
    markup.add(itemnd, itemds)
    markup.add(itemns)
    markup.add(itemir, itemssml)
    markup.add(itemspr)

    bot.send_message(CHANNEL_NAME, 'Урок 1', reply_markup=markup)
@bot.message_handler(commands=["start"])
def start(m, res=False):
        menu1()

        print([m.from_user.id, m.text])
# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    data_log = open("log.txt", "a")
    data_log.write(str(time.strftime("%y-%m-%d %H:%M:%S")))
    data_log.write(",")

    data_log.write(str(message.from_user.id))
    data_log.write(",")

    data_log.write(str(message.text))
    data_log.write(",")

    data_log.write("\n")
    data_log.close()
    # Если юзер прислал 1, выдаем ему случайный факт
    if message.text.strip() == 'Анализ рынков' :

        client = Client(password.api_key, password.api_secret)
        # info = client.get_symbol_info('AXSBTC')
        # print(info)
        prices = client.get_all_tickers()
        data_prices = pd.DataFrame(prices)
        print(data_prices.shape[0])
        for i in range(data_prices.shape[0]):
            time.sleep(2)
            price = prices[i]
            print([i, price['symbol'], price['price']])
            answer = str(i) + " " + str(price['symbol']) + " " + str(price['price'])
            bot.send_message(CHANNEL_NAME, answer)
            print([message.from_user.id,message.text])
    # Если юзер прислал 2, выдаем умную мысль

    elif message.text.strip() == 'урок 1':
        menu2()
        text_ans = "В этом интернет-уроке вы узнаете: \n" \
                   " - что такое искусственный интеллект \n" \
                   " - что такое машинное обучение, глубокое обучение, набор данных или датасет, нейросети \n" \
                   " - историю развития и современное состояние сферы машинного обучения \n" \
                   " - ссылки на полезные ресурсы, которые помогут быть в курсе новостей и технологических наработок \n\n" \
                   " Продолжение в источнике (штука) буду дописывать"

        bot.send_message(CHANNEL_NAME, text_ans)
        print([message.from_user.id, message.text])

    elif message.text.strip() == 'Навигационная панель':
        text_ans = "Навигационная панель"
        menu1()
        #bot.send_message(CHANNEL_NAME, text_ans)
        print([message.from_user.id, message.text])

    elif message.text.strip() == 'Синтаксис python':
        for i in range(100):
            a = "import os \n" + str(i)
            text_ans = "Синтаксис python : " + a
            menu2()
            bot.send_message(CHANNEL_NAME, text_ans)
            print([message.from_user.id, message.text])

    elif message.text.strip() == 'таймер':
        for i in range(1):
            time.sleep(1)
            text_ans = str(time.strftime("%y-%m-%d %H:%M:%S"))
            #menu1()
            bot.send_message(CHANNEL_NAME, text_ans)
            print([message.from_user.id, message.text])

    elif message.text.strip() == 'код':
            answer = "import telebot \n" \
                     "from telebot import types \n" \
                     "TOKEN = '...' \n" \
                     "bot = telebot.TeleBot(TOKEN) \n" \
                     "CHANNEL_NAME = '-609825876' \n" \
                     "@bot.message_handler(commands=['start']) \n" \
                     "def start(m, res=False): \n" \
                     "      bot.send_message(CHANNEL_NAME, 'Нажми:') \n" \
                     "@bot.message_handler(content_types=['text']) \n" \
                     "def handle_text(message): \n" \
                     "      if message.text.strip() == 'код': \n" \
                     "          answer = 'text' \n"\
                     "          bot.send_message(CHANNEL_NAME, answer) \n" \
                     "else: \n" \
                     "      bot.send_message(CHANNEL_NAME, message.text)"
            # Отсылаем юзеру сообщение в его чат
            bot.send_message(CHANNEL_NAME, answer)
            print([message.from_user.id, message.text])
    elif message.text.strip() == 'Привет':
            answer =  "Ребята, привет из Open AI"
            # Отсылаем юзеру сообщение в его чат
            bot.send_message(CHANNEL_NAME, answer)
            print([message.from_user.id, message.text])
    else:
            bot.send_message(CHANNEL_NAME, str(message.text))
            print([message.from_user.id, str(message.text)])

@bot.message_handler(content_types=["photo"])
def photo(message):
   idphoto = message.photo[0].file_id
   print([idphoto,message.photo[0].file_id])
   bot.send_photo(message.chat.id, idphoto )








# Запускаем бота
print("Запускаем бота")
bot.polling(none_stop=True, interval=0)




"""from block_io import BlockIo
api_key_block_btc = "cae3-e5ba-4e69-2ee9"
api_key_block_ltc = "1a2d-0feb-3608-582f"
api_key_block_doge = "6fef-650a-9bf7-f254"
SECRET_PIN = "mustberandomlygeneratedandunique" #kry2011gm
API_VERSION = 2
block_io_btc = BlockIo(api_key_block_btc, SECRET_PIN, API_VERSION)
block_io_ltc = BlockIo(api_key_block_ltc, SECRET_PIN, API_VERSION)
block_io_doge = BlockIo(api_key_block_doge, SECRET_PIN, API_VERSION)"""
