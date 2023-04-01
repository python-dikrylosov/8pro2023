# -*- coding: utf-8 -*-
import paasword
import random
import os
import math
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from tensorflow.keras.models import save_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
plt.style.use('bmh')
import matplotlib as mpl
mpl.rcParams['figure.max_open_warning'] = 0
import pandas as pd
import numpy as np
import yfinance as yf
import cv2
import time
from imageai.Detection import ObjectDetection
import telebot
from telebot import types
TOKEN = password.TOKEN
# Адрес телеграм-канала, начинается с @
# user_id = message.from_user.id
# user_first_name = message.from_user.first_name
# user_last_name = message.from_user.last_name
# user_username = message.from_user.username
# Создаем бота
bot = telebot.TeleBot(TOKEN) #Узнаем у botFather
CHANNEL_NAME = password.CHANNEL_NAME # смотрим в отдельном боте
import pandas as pd
start_time = time.time()

import yfinance as yf




@bot.message_handler(commands=["start"])
def start(m, res=False):
    # Добавляем две кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_agreement = types.KeyboardButton("Принять пользовательское соглашение")
    item_volue_exit = types.KeyboardButton("Отказаться")
    item_volue_btc_rub = types.KeyboardButton("биткоин к рублю")

    markup.add(item_volue_btc_rub)
    markup.add(item_agreement)
    markup.add(item_volue_exit)

    bot.send_message(CHANNEL_NAME, 'Принимая данное соглашение вы обязуетесь соблюдать все законы ', reply_markup=markup)
@bot.message_handler(content_types=["text"])
def handle_text(message):

        if message.text.strip() == 'Привет':
                answer =  "Ребята, привет из Open AI"
                # Отсылаем юзеру сообщение в его чат
                bot.send_message(CHANNEL_NAME, answer)
                print([message.from_user.id, message.text])
        elif message.text.strip() == 'Принять пользовательское соглашение':
                answer = "Пользовательское соглашение временно ограничено"
                # Отсылаем юзеру сообщение в его чат
                bot.send_message(CHANNEL_NAME, answer)
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



print("Запускаем бота")
bot.polling(none_stop=True, interval=0)
