# -*- coding: utf-8 -*-
import password
import time
import random
import os
import math
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from tensorflow.keras.models import save_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('bmh')
import matplotlib as mpl
mpl.rcParams['figure.max_open_warning'] = 0
import numpy as np
import yfinance as yf
import cv2
import time
from imageai.Detection import ObjectDetection
import telebot
from telebot import types
import pandas as pd
import os.path
from block_io import BlockIo
import sqlite3
"""api_key_block_btc = password.api_key_block_btc
api_key_block_ltc = password.api_key_block_ltc
api_key_block_doge = password.api_key_block_doge
SECRET_PIN = password.SECRET_PIN
API_VERSION = 2
block_io_btc = BlockIo(api_key_block_btc, SECRET_PIN, API_VERSION)
block_io_ltc = BlockIo(api_key_block_ltc, SECRET_PIN, API_VERSION)
block_io_doge = BlockIo(api_key_block_doge, SECRET_PIN, API_VERSION)
print(block_io_btc)
print(block_io_ltc)
print(block_io_doge)"""
bot = telebot.TeleBot(password.TOKEN)
CHANNEL_NAME = password.CHANNEL_NAME
start_time = time.time()
@bot.message_handler(commands=["start"])
def start(m, res=False):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS login_id(id INTEGER)""")

    connect.commit()

    people_id = m.chat.id
    cursor.execute(f"SELECT id FROM login_id WHERE id = {people_id}")
    data = cursor.fetchone()

    if data is None:
        user_id = [m.chat.id]
        cursor.execute("INSERT INTO login_id VALUES(?);", user_id)
        connect.commit()
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_person = types.KeyboardButton("🌐 О пользователе 🌐")
        markup.add(item_person)
        bot.send_message(m.chat.id, "Такой пользователь существует", reply_markup=markup)
        bot.send_message(810299040, "Такой пользователь существует " + str(m.from_user.id))

    answer = 'Принимая данное соглашение вы согласны с соблюдением всех возможных законов'
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_Accept_user_agreement = types.KeyboardButton("Принять пользовательское соглашение")
    item_Accept_user_agreement_all = types.KeyboardButton("📚 Полный текст соглашения 📚")
    item_Refuse = types.KeyboardButton("Отказаться")
    markup.add(item_Accept_user_agreement)
    markup.add(item_Accept_user_agreement_all)
    markup.add(item_Refuse)
    bot.send_message(m.chat.id,answer , reply_markup=markup)
    bot.send_message(810299040, "Соглашение принято " + str(m.from_user.id))@bot.message_handler(content_types=["text"])


@bot.message_handler(commands=["delete"])
def delete(m, res=False):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    people_id = m.chat.id
    cursor.execute(f"DELETE FROM login_id WHERE id = {people_id}")
    connect.commit()


# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Принять пользовательское соглашение':
        print(str(time.strftime("%Y-%m-%d ")) + str(message.chat.id) + " " + message.from_user.first_name + " " + str(message.text))

        # проверка наличия пользователя в базе
        if os.path.isfile(str(message.from_user.id) + "_log.txt") == False:

            """btc_address = block_io_btc.get_address_balance(labels=str(message.from_user.id))
            data_btc = btc_address
            data_data_btc = data_btc["data"]
            balance_btc = data_data_btc["balances"]
            data_address_btc = pd.DataFrame(balance_btc)
            address_btc = data_address_btc['address']
            on_address_btc = address_btc[0]
            print(on_address_btc)
            ltc_address = block_io_ltc.get_address_balance(labels=str(message.from_user.id))
            doge_address = block_io_doge.get_address_balance(labels=str(message.from_user.id))
            """
            data_person = pd.DataFrame(["id", "Fname", "BTC", "DOGE", "LTC"])
            data_person.to_csv(str(message.from_user.id) + "_log.txt")

            print(str(time.strftime("%Y-%m-%d ")) + "пользователь в базе: " + str(message.from_user.id))
            print("Пользовательский id : " + str(message.from_user.id))

            print(str(time.strftime("%Y-%m-%d ")) + "Новый пользователь зарегистрирован в базе: " + str(
                message.from_user.id))

            bot.send_message(810299040, str(time.strftime("%Y-%m-%d ")) + "пользователь в базе: " + str(message.from_user.id))
        elif os.path.isfile(str(message.from_user.id) + "_log.txt") == True:
            """btc_address = block_io_btc.get_address_balance(labels=str(message.from_user.id))
            data_btc = btc_address
            data_data_btc = data_btc["data"]
            balance_btc = data_data_btc["balances"]
            data_address_btc = pd.DataFrame(balance_btc)
            address_btc = data_address_btc['address']
            on_address_btc = address_btc[0]
            print(on_address_btc)
            ltc_address = block_io_ltc.get_address_balance(labels=str(message.from_user.id))
            data_ltc = ltc_address
            data_data_ltc = data_ltc["data"]
            balance_ltc = data_data_ltc["balances"]
            data_address_ltc = pd.DataFrame(balance_ltc)
            address_ltc = data_address_ltc['address']
            on_address_ltc = address_ltc[0]
            print(on_address_ltc)
            doge_address = block_io_doge.get_address_balance(labels=str(message.from_user.id))"""

            data_person = pd.DataFrame(["id", "Fname", "BTC", "DOGE", "LTC"])
            data_person.to_csv(str(message.from_user.id) + "_log.txt")

            print(str(time.strftime("%Y-%m-%d ")) + "пользователь в базе: " + str(message.from_user.id))
            print("Пользовательский id : " + str(message.from_user.id))


        answer = "Спасибо за доверие " + str(message.from_user.first_name) + "\n" \
                 + " : " + str(message.from_user.id) + "\n"


        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

        item_volue_btc = types.KeyboardButton("📒 BTC кошелек")
        item_volue_doge = types.KeyboardButton("📙 DOGE кошелек")
        item_volue_ltc = types.KeyboardButton("📗LTC кошелек")

        item_volue = types.KeyboardButton("💼 Обмен на рубли")
        item_volue_remote = types.KeyboardButton("🚧 Разработка, обновления и новости")
        item_person = types.KeyboardButton("🌐 О пользователе 🌐")
        markup.add(item_volue)
        markup.add(item_volue_btc, item_volue_ltc, item_volue_doge)
        markup.add(item_volue_remote, item_person)

        bot.send_message(message.chat.id, answer, reply_markup=markup)
        bot.send_message(810299040, answer)
    elif message.text.strip() == 'биткоин к рублю':
                real_date = time.strftime("%Y-%m-%d")
                import numpy as np
                data = yf.download("BTC-RUB", start="2014-04-01", end=real_date, interval="1d")
                print(data)

                data_filter_open = data.filter(["Open"])
                data_filter_open.to_csv("logo.csv")

                print(data_filter_open)
                plt.plot(data_filter_open)
                plt.savefig("BTC-RUB.png")

                src = "BTC-RUB.png"
                answer = str(data_filter_open)
                # Отсылаем юзеру сообщение в его чат
                #bot.send_message(CHANNEL_NAME, answer)
                bot.send_photo(CHANNEL_NAME, open(src, 'rb'))

    elif message.text.strip() == 'биткоин к доллару':
                real_date = time.strftime("%Y-%m-%d")
                data = yf.download("BTC-USD", start="2014-01-01", end=real_date, interval="1d")
                data = pd.DataFrame(data)
                data_filter_open = data.filter(["Open"])
                data_filter_open.to_csv("BTC-USD.csv")
                print(data_filter_open.tail(1000))

                x = [i for i in range(len(data_filter_open.tail(1000)))]
                y = data_filter_open.tail(1000)
                plt.plot(x, y)
                plt.scatter(x, y)
                plt.show()
                plt.savefig("BTC-USD.png")

                src = "BTC-USD.png"
                answer = str(data_filter_open)
                # Отсылаем юзеру сообщение в его чат
                #bot.send_message(CHANNEL_NAME, answer)
                bot.send_photo(CHANNEL_NAME, open(src, 'rb'))

    elif message.text.strip() == 'Отказаться':
                answer = "ОТКАЗАТЬСЯ НЕВОЗМОЖНО"
                # Отсылаем юзеру сообщение в его чат
                bot.send_message(CHANNEL_NAME, answer)

    else:

            bot.send_message(CHANNEL_NAME, str(message.from_user.first_name + " : " + str(message.text) + "\n" + time.strftime("%Y-%m-%d")))
            #print([message.from_user.id, str(message.text)])

@bot.message_handler(content_types=["photo"])
def photo(message):
        idphoto = message.photo[0].file_id
        print([idphoto,message.photo[0].file_id])
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'files/' + file_info.file_path
        with open(src, 'wb') as new_file:
           new_file.write(downloaded_file)
        cap_read = cv2.imread(src)
        print(cap_read.shape)
        line = cv2.line(cap_read,(0,0),(cap_read.shape[1],cap_read.shape[0]),(0,0,255),thickness=2)
        detector = ObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath("yolov3.pt")
        detector.loadModel()
        detections = detector.detectObjectsFromImage(input_image=src,
                                                     output_image_path=src,
                                                     minimum_percentage_probability=30)
        for eachObject in detections:
            print(eachObject["name"], " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"])
            print("--------------------------------")
        bot.send_photo(CHANNEL_NAME, open(src, 'rb'))
        bot.send_photo(message, open(src, 'rb'))

end_time = time.time() - start_time
print("" + str(end_time))
bot.polling(none_stop=True, interval=0)

