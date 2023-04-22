# -*- coding: utf-8 -* 
from google.colab import drive 
import google.colab as colab
drive.mount('/content/gdrive')
#Для сохранения различных данных использую гуг диск
import cv2
import yfinance as yf
#import torch
#from tensorflow import keras
#import torchvision
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import Dense, LSTM
import matplotlib.pyplot as plt
import time
import numpy as np
import math
from imageai.Detection import ObjectDetection
import telebot
from telebot import types


             
TOKEN = "5197117880:AAHnkLJKCDqvmhoeIMEcT1W6kqL3o7be5Fg"
# Адрес телеграм-канала, начинается с @
# user_id = message.from_user.id
# user_first_name = message.from_user.first_name
# user_last_name = message.from_user.last_name
# user_username = message.from_user.username

# Создаем бота
bot = telebot.TeleBot(TOKEN)
CHANNEL_NAME = "-1001917819364"#"-1001922857608 bitcoincode"#'-816129217'


@bot.message_handler(commands=["start"])
def start(m, res=False):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_Hello = types.KeyboardButton("Привет")
        item_ehobot = types.KeyboardButton("Эхо бот")
        item_Refuse = types.KeyboardButton("Анализ рынка BTC/USD")

        markup.add(item_Refuse)
        markup.add(item_ehobot)
        markup.add(item_Hello)
        print([m.from_user.id, m.text])
        bot.send_message(CHANNEL_NAME, "Команды \n1) Привет \n2) Эхо бот \n3) Анализ рынка BTC/USD",reply_markup=markup)

# Получение сообщений от юзера
@bot.message_handler(content_types=["text"])
def handle_text(message):
    data_log = open("/content/gdrive/MyDrive/8pro2023/tele_bot/log.txt", "a")
    data_log.write(str(time.strftime("%y-%m-%d %H:%M:%S")))
    data_log.write(",")

    data_log.write(str(message.from_user.id))
    data_log.write(",")

    data_log.write(str(message.text))
    data_log.write(",")

    data_log.write("\n")
    data_log.close()


    if message.text.strip() == 'Привет':
            answer =  "Ребята, привет из Open AI" 
            # Отсылаем юзеру сообщение в его чат
            bot.send_message(CHANNEL_NAME, answer)
            print([message.from_user.id, message.text])
    elif message.text.strip() == 'Эхо бот':
            for i in range(10):
              answer =  "Тестовый решил эха :" + str(time.time())
              # Отсылаем юзеру сообщение в его чат
              bot.send_message(CHANNEL_NAME, answer)
              print([message.from_user.id, message.text])

    elif message.text.strip() == 'Анализ рынка BTC/USD':

              import requests  # Модуль для обработки URL
              from bs4 import BeautifulSoup  # Модуль для работы с HTML

              # Ссылка на нужную страницу
              url_btc_usd = "https://www.google.com/search?channel=fs&client=ubuntu&q=btc+usd"  # "https://www.investing.com/crypto/bitcoin/btc-usd"
              # Заголовки для передачи вместе с URL
              headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'}
              full_page = requests.get(url_btc_usd, headers=headers)
              # Разбираем через BeautifulSoup
              soup = BeautifulSoup(full_page.content, 'html.parser')
              # Получаем нужное для нас значение и возвращаем его
              convert = soup.findAll("span", {"class": "pclqee"})
              # print(str(convert[0].text))
              mattr = convert[0].text
              data_pay = [mattr[0] + mattr[1] + mattr[3] + mattr[4] + mattr[5] + "." + mattr[7] + mattr[8]]
              print(data_pay)



              real_date = str(time.strftime("%Y-%m-%d"))
              bot.send_message(CHANNEL_NAME, "Запрос обрабатывается, реальный курс BTC/USD " + str(data_pay))
              data_btc_usd = yf.download("BTC-USD", start="2014-01-01", end=real_date, interval='1d') 
              print(data_btc_usd)
              #bot.send_message(CHANNEL_NAME, data_btc_usd)
              


              #creat  e dATEFRAME CLOSE
              data = data_btc_usd.filter(['Close'])
              print(data)
              #bot.send_message(CHANNEL_NAME, data)  
              #Из урока 6.2 Визаулизирую график
              for i in range(0):
                x = [i for i in range(len(data))]
                y = data
                plt.plot(x, y)
                plt.scatter(x, y)

                plt.savefig("/content/gdrive/MyDrive/8pro2023/Диплом/data_btc_usd.png")
                bot.send_photo(CHANNEL_NAME, "/content/gdrive/MyDrive/8pro2023/Диплом/data_btc_usd.png") 

              #Конвертирование данных
              dataset = data.values

              #bot.send_message(CHANNEL_NAME, dataset)  
              #print(dataset)


              #получение цифровых строк для обучения модели
              training_data_len = math.ceil(len(dataset) * .8 )
              #bot.send_message(CHANNEL_NAME, training_data_len) 
              #print(training_data_len)


              #масштабирование данных
              scaler = MinMaxScaler(feature_range=(0,1))
              #bot.send_message(CHANNEL_NAME, scaler)
              scaled_data = scaler.fit_transform(dataset)
              #bot.send_message(CHANNEL_NAME, scaled_data)
              #print(scaled_data)


              #создание обучающего набора данных
              train_data = scaled_data[0:training_data_len , :]
              #bot.send_message(CHANNEL_NAME, train_data)


              #разделение данных на наборы данных x_train и y_train
              x_train = []
              y_train = []
              for i in range(60, len(train_data)):
                  x_train.append(train_data[i-60:i, 0])
                  y_train.append(train_data[i, 0])
                  if i <= 61:
                    #print(x_train)
                    #print(y_train)
                    print()


              #преобразование x_train и y_train в массивы numpy
              x_train, y_train = np.array(x_train),np.array(y_train)
              #bot.send_message(CHANNEL_NAME, (x_train, y_train))


              #reshape the data
              x_train = np.reshape(x_train, (x_train.shape[0],x_train.shape[1],1))
              x_train.shape

              #biuld to LSTM model
              model = Sequential()
              model.add(LSTM(50, return_sequences=True, input_shape = (x_train.shape[1],1)))
              model.add(LSTM(101, return_sequences=False))
              model.add(Dense(50))
              model.add(Dense(25))
              model.add(Dense(1))

              #compale the model
              model.compile(optimizer='adam',loss='mean_squared_error')

              #train_the_model
              from tensorflow import keras
              model = keras.models.load_model("/content/gdrive/MyDrive/8pro2023/Диплом/BTC-USD.h5")
              #model.load("/content/gdrive/MyDrive/8pro2023/Диплом/BTC-USD.h5")
              model.fit(x_train, y_train, batch_size=2,epochs=1)
              model.save("/content/gdrive/MyDrive/8pro2023/Диплом/BTC-USD.h5")


              #create the testing data set
              #create a new array containing scaled values from index 1713 to 2216
              test_data = scaled_data[training_data_len - 60: , : ]

              
              #create the fata sets x_test and y_test
              x_test = []
              y_test = dataset[training_data_len:, :]
              for i in range(60, len(test_data)):
                  x_test.append(test_data[i-60:i,0])

              #conert the data to numpy array
              x_test = np.array(x_test)

              #reshape the data
              X_test = np.reshape(x_test, (x_test.shape[0],x_test.shape[1],1))

              #get the model predicted price values
              predictions = model.predict(X_test)
              predictions = scaler.inverse_transform(predictions)

              #get the root squared error (RMSE)
              rmse = np.sqrt(np.mean(predictions - y_test ) ** 2 )
              #rmse

              #show the valid and pridicted prices
              #valid

              #get the quate 
              btc_quote = data_btc_usd
              #create a new dataframe

              new_df = btc_quote.filter(['Close'])

              #get teh last 60 days closing price values and convert the dataframe to an array
              last_60_days = new_df[-1:].values
              #scale the data to be values beatwet 0 and 1

              last_60_days_scaled = scaler.transform(last_60_days)

              #creAte an enemy list
              X_test = []
              #Append past 60 days
              X_test.append(last_60_days_scaled)

              #convert the x tesst dataset to numpy
              X_test = np.array(X_test)

              #Reshape the dataframe
              X_test = np.reshape(X_test, (X_test.shape[0],X_test.shape[1],1))
              #get predict scaled

              pred_price = model.predict(X_test)
              #undo the scaling
              pred_price = scaler.inverse_transform(pred_price)
              print(pred_price)
              pred_price = np.array(pred_price)
              pred_price = pred_price[0]
              pred_price = pred_price[0]
              # Отсылаем юзеру сообщение в его чат
              print(pred_price)
              answer =  "Прогнозируемый результат BTC-USD " + str(pred_price)
              bot.send_message(CHANNEL_NAME, answer)
              src = "/content/gdrive/MyDrive/8pro2023/Диплом/data_btc_usd.png"
              bot.send_photo(CHANNEL_NAME,open(src, 'rb')) 
              #bot.send_message(message.from_user.id, answer)
              #print([message.from_user.id, message.text])
              #time.sleep(15)

    elif message.text.strip() == 'а что нибудь разумное можешь?':
            status = ["Пока не могу","Более менее"]
            import random
            answer =  status[random.randint(0,1)]
            # Отсылаем юзеру сообщение в его чат
            bot.send_message(CHANNEL_NAME, answer)
            print([message.from_user.id, message.text])
    else:
            #bot.send_message(CHANNEL_NAME, str(message.from_user.first_name + " : " + message.text))
            bot.send_message(message.from_user.id, "Я вас не понимаю /help")
            bot.send_message(CHANNEL_NAME, "Я вас не понимаю")
            print([message.from_user.id, str("Я вас не понимаю /help")])

"""@bot.message_handler(content_types=["photo"])
def photo(message):
        idphoto = message.photo[0].file_id
        print([idphoto,message.photo[0].file_id])

        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src2 = 'files/' + file_info.file_path
        with open(src2, 'wb') as new_file:
                new_file.write(downloaded_file)
        cap_read = cv2.imread(src2)
        print(cap_read.shape)
        line = cv2.line(cap_read,(0,0),(cap_read.shape[1],cap_read.shape[0]),(0,0,255),thickness=2)
        detector = ObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath("/content/gdrive/MyDrive/8pro2023/Диплом/yolov3.pt")
        detector.loadModel()
        detections = detector.detectObjectsFromImage(input_image=src2,
        output_image_path=src2,
        minimum_percentage_probability=30)
        for eachObject in detections:
                print(eachObject["name"], " : ", eachObject["percentage_probability"], " : ", eachObject["box_points"])
                print("--------------------------------")

        bot.send_photo(CHANNEL_NAME, open(src2, 'rb'))
        bot.send_photo(message, open(src2, 'rb'))"""



print("Запускаем бота")
bot.polling(none_stop=True, interval=0)
