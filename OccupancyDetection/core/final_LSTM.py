from model.rnn import LSTM
from model.hidden_markov_model import HMM
# from model.nn import NN
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sklearn.metrics as skm
model = 'timegan'
X_train = np.load(r'/tmp/pycharm_project_236/training/X_{}.npy'.format(model))
y_train = np.load(r'/tmp/pycharm_project_236/training/y_{}.npy'.format(model))
X_test = np.load("/tmp/pycharm_project_236/training/X_test.npy")
y_test = np.load("/tmp/pycharm_project_236/training/y_test.npy")
# X_train = np.load(r'C:\Users\ASUS\Desktop\最后一战\profile/X_{}.npy'.format(model))
# y_train = np.load(r'C:\Users\ASUS\Desktop\最后一战\profile/y_{}.npy'.format(model))
# X_test = np.load(r"C:\Users\ASUS\Desktop\最后一战\profile/X_test.npy")
# y_test = np.load(r"C:\Users\ASUS\Desktop\最后一战\profile/y_test.npy")
lag = 30
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_train = scaler.fit_transform(X_train)
data = []
electricity_data = X_train[:,0]
time_features = X_train[:,[1,2]]
for i in range(len(electricity_data)-lag):
    data.append(electricity_data[i:i+lag])
data = np.array(data)
X_train = np.concatenate((data, time_features[:-lag]), axis=1) #23031,12
# X_train = X_train.reshape(X_train.shape[0],-1,X_train.shape[1])
y_train=y_train[:-lag].reshape(-1,1)

from sklearn.preprocessing import MinMaxScaler
# scaler = MinMaxScaler()
X_test = scaler.fit_transform(X_test)
data = []
electricity_data = X_test[:,0]
time_features = X_test[:,[1,2]]
for i in range(len(electricity_data)-lag):
    data.append(electricity_data[i:i+lag])
data=np.array(data)
X_test = np.concatenate((data, time_features[:-lag]), axis=1)
y_test=y_test[:-lag].reshape(-1,1)
y_test_reserved = y_test.copy()
np.save('y_ground_truth.npy',y_test_reserved)
from sklearn.preprocessing import OneHotEncoder
y_train = OneHotEncoder().fit_transform(y_train).toarray()

y_test = OneHotEncoder().fit_transform(y_test).toarray()
class Dataset:
    def __init__(self, occupancy, electricity_dat):
        self.occupancy = occupancy
        self.data = electricity_dat

train_dataset = Dataset(y_train,X_train)
test_dataset = Dataset(y_test,X_test)
lstm = LSTM(train_dataset, test_dataset, epoch=30)
prediction1 = lstm.run()
np.save(r"lstm_{}".format(model), prediction1)
from sklearn.metrics import f1_score,accuracy_score
print(f1_score(y_test.astype(int),prediction1.astype(int),average="macro"))
print(accuracy_score(y_test_reserved.reshape(-1).astype(int),prediction1.reshape(-1).astype(int)))