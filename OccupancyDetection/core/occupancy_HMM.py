from model.rnn import LSTM
from model.hidden_markov_model import HMM
# from model.nn import NN
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def run(lag):
    print(lag)
    occupancy = pd.read_csv(r'C:\Users\ASUS\Desktop\activity inference\data\eco\home1\01_occupancy_csv\01_summer.csv',index_col=0)
    # timestamps = pd.date_range(start=occupancy.index[0], end=pd.to_datetime(occupancy.index[-1])+pd.Timedelta(days=1), freq='S')
    occupancy_state = []
    for i in range(len(occupancy)):
        date = occupancy.index[i]
        timestamps = pd.date_range(start=date,end=pd.to_datetime(date)+pd.Timedelta(days=1)-pd.Timedelta(seconds=1),freq='s')
        data = occupancy.iloc[i,:]
        series = pd.DataFrame(index=timestamps, data=data.values,columns=["occupancy"]).resample('1min').max()
        occupancy_state.append(series)
    occupancy_state = pd.concat(occupancy_state)
    timestamps = occupancy_state.index
    # prepare electricity
    hdf = pd.HDFStore(r'C:\Users\ASUS\Desktop\activity inference\data\eco\eco.h5')
    power_info = hdf.get('/building1/elec/meter1')
    power_info.index.name = 'Date'
    power_info.reset_index(inplace=True)
    power_info['Date'] = pd.to_datetime(power_info['Date']).dt.tz_localize(None)
    #转化时间戳
    power_info.set_index('Date', drop=True, inplace=True)
    power_info=power_info.fillna(0)
    power_info = power_info["power"]["active"].to_frame()
    power_info=power_info.resample("1min").mean()
    power_info=power_info.fillna(0)
    date = power_info.index
    electricity_data = power_info.loc[np.intersect1d(pd.to_datetime(date), pd.to_datetime(timestamps))]
    class Dataset:
        def __init__(self, occupancy, electricity_dat):
            self.occupancy = occupancy
            self.data = electricity_dat
    occupancy_state = occupancy_state.loc[np.intersect1d(pd.to_datetime(date), pd.to_datetime(timestamps))]

    sliding_window = []
    lag = lag
    for i in range(len(electricity_data)-lag):
        sliding_window.append(electricity_data[i:i+lag].values)
    power_sliding = np.array(sliding_window).reshape(-1,lag)

    num_indices = 24
    sin_encoding = np.sin(2 * np.pi * electricity_data.index.hour / num_indices)
    cos_encoding = np.cos(2 * np.pi * electricity_data.index.hour / num_indices)

    # 将编码后的索引作为新列添加到DataFrame
    electricity_data['sin_index'] = sin_encoding
    electricity_data['cos_index'] = cos_encoding
    time_info = electricity_data[:-lag].iloc[:,[1,2]]
    electricity_data = np.concatenate([power_sliding,time_info],axis=1)
    occupancy_state_reserve = occupancy_state.values[:-lag]
    occupancy_state = occupancy_state.values[:-lag]
    # from sklearn.preprocessing import OneHotEncoder
    # occupancy_state = OneHotEncoder().fit_transform(occupancy_state.values).toarray()[:-lag]

    from sklearn.preprocessing import MinMaxScaler
    electricity_data = MinMaxScaler().fit_transform(electricity_data)
    training = 0.6
    validation = 0.2
    test = 0.2
    validation_end = int(len(electricity_data)*validation)
    training_end = validation_end + int(len(electricity_data)*training)
    test_start = int(len(electricity_data)*test)
    validation_dataset = Dataset(occupancy_state[:validation_end], electricity_data[:validation_end])
    train_dataset = Dataset(occupancy_state[validation_end:training_end], electricity_data[validation_end:training_end])
    test_dataset = Dataset(occupancy_state[-test_start:], electricity_data[-test_start:])
    model = HMM(train_dataset, test_dataset,number_of_hidden_states=3)
    prediction1 = model.run()
    np.save(r"same_winter_prediction{}".format(lag) ,prediction1)
    np.save(r"same_winter_ground_truth{}".format(lag),
            occupancy_state_reserve[-test_start:])
    print("save into",r"ground_truth_lag{}".format(lag))

run(60)