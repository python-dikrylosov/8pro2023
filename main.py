import yfinance as yf
import time
import math
import numpy as np
import math
import numpy as np
import tensorflow as tf
from termcolor import colored
from tensorflow.keras.models import load_model
from tensorflow.keras.models import save_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt
epochs = 1
plt.style.use('fivethirtyeight')

start_time = time.time()
real_time = str(time.strftime("%Y-%m-%d"))

dfuid = yf.download("AXS-BTC",start="2014-01-01",end=real_time,interval="1d")

print(dfuid)

data_filter_AXSBTC_Close = dfuid.filter(["Close"])

print(data_filter_AXSBTC_Close)

data_values = data_filter_AXSBTC_Close.values

print(data_values)

data = dfuid.filter(['Close'])
# data_df_pandas_filter = data_df_pandas.filter(["Well"])
print(data)

# convert dataframe
dataset = data.values

# dataset  = data_df_pandas_filter.values
print(dataset)

# get the number rows to train the model
training_data_len = math.ceil(len(dataset) * .8)
print(training_data_len)

# scale the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(dataset)
print(scaled_data)

# create the training dataset
train_data = scaled_data[0:training_data_len, :]
# split the data into x_train and y_train data sets
x_train = []
y_train = []
for rar in range(60, len(train_data)):
    x_train.append(train_data[rar - 60:rar, 0])
    y_train.append(train_data[rar, 0])
    if rar <= 61:
        print(x_train)
        print(y_train)
        print()

# conver the x_train and y_train to numpy arrays
x_train, y_train = np.array(x_train), np.array(y_train)

# reshape the data
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
print(x_train.shape)


# biuld to LST model

model = Sequential()
model.add(LSTM(50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(LSTM(101, return_sequences=False))
model.add(Dense(50))
model.add(Dense(25))
model.add(Dense(1))

# cmopale th emodel
model.compile(optimizer='adam', loss='mean_squared_error')
# train_the_model
model.summary()
print("Fit model on training data")

# Evaluate the model on the test data using `evaluate`
print("Evaluate on test data")

results = model.evaluate(x_train, y_train, batch_size=1)
print("test loss, test acc:", results)

model = tf.keras.models.load_model(os.path.join("./dnn/", "AXS-BTC_model.h5"))
model.fit(x_train, y_train, batch_size=1, epochs=2)

model.save(os.path.join("./dnn/", "AXS-BTC_model.h5"))
reconstructed_model = tf.keras.models.load_model(os.path.join("./dnn/", "AXS-BTC_model.h5"))

np.testing.assert_allclose(model.predict(x_train), reconstructed_model.predict(x_train))
reconstructed_model.fit(x_train, y_train)

# create the testing data set
# create a new array containing scaled values from index 1713 to 2216
test_data = scaled_data[training_data_len - 60:, :]
# create the fata sets x_test and y_test
x_test = []
y_test = dataset[training_data_len:, :]
for resr in range(60, len(test_data)):
    x_test.append(test_data[resr - 60:resr, 0])

# conert the data to numpy array
x_test = np.array(x_test)

# reshape the data
x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

# get the model predicted price values
predictions = model.predict(x_test)
predictions = scaler.inverse_transform(predictions)

# get the root squared error (RMSE)
rmse = np.sqrt(np.mean(predictions - y_test) ** 2)
print(rmse)
if int(rmse) >= 1000:
    print(colored("Высокий уровень ошибки", "red"))

# get the quate
btc_quote = dfuid
# btc_quote = pd.read_csv(str(balance_btc["asset"]) + ".csv", delimiter=",")

new_df = btc_quote.filter(['Close'])

# get teh last 60 days closing price values and convert the dataframe to an array
last_60_days = new_df[-60:].values

# scale the data to be values beatwet 0 and 1
last_60_days_scaled = scaler.transform(last_60_days)

# creAte an enemy list
X_test = []
# Append past 60 days
X_test.append(last_60_days_scaled)

# convert the x tesst dataset to numpy
X_test = np.array(X_test)

# Reshape the dataframe
X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
# get predict scaled

pred_price = model.predict(X_test)
# undo the scaling
pred_price = scaler.inverse_transform(pred_price)
print(pred_price)

pred_price_a = pred_price[0]
pred_price_aa = pred_price_a[0]
preset_pred_price = float(pred_price_aa)
print(pred_price)
print(preset_pred_price)
old_time = time.time() - start_time
print(old_time)
