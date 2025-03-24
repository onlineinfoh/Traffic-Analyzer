import numpy as np 
import pandas as pd 
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import datetime
from tensorflow.keras import layers, Sequential
from tensorflow.keras.optimizers import Adam
from copy import deepcopy
from matplotlib.dates import DateFormatter

def str_to_datetime(s):
    if isinstance(s, (datetime.datetime, pd.Timestamp)):
        return s
    split = s.split('-')
    year, month, day = int(split[0]), int(split[1]), int((split[2].split(' '))[0])
    time = (split[2].split(' '))[1].split(':')
    hour = int(time[0])
    return datetime.datetime(year=year, month=month, day=day,hour=hour)

def get_junction_data(data_path):
    data = pd.read_csv(data_path)
    data["DateTime"] = data["DateTime"].apply(str_to_datetime)
    data.index = data.pop('DateTime')
    junction_data = {}
    available_junctions = data['Junction'].unique()
    for junction_num in available_junctions:
        tem = data[data['Junction']==junction_num]
        tem = tem.drop(columns=['Junction','ID'])
        junction_data[junction_num] = tem
    return junction_data

def create_lstm_data(dataframe, first, last, n):
    first = str_to_datetime(first)
    last  = str_to_datetime(last)
    target = first
    dates = []
    X, Y = [], []
    last_time = False
    while True:
        df_subset = dataframe.loc[:target].tail(n+1)
        if len(df_subset) != n+1:
            print(f'Error: Window of size {n} is too large for date {target}')
            return
        values = df_subset['Vehicles'].to_numpy()
        x, y = values[:-1], values[-1]
        dates.append(target)
        X.append(x)
        Y.append(y)
        next_week = dataframe.loc[target:target+datetime.timedelta(days=7)]
        next_datetime_str = str(next_week.head(2).tail(1).index.values[0])
        next_date_str = next_datetime_str.split('T')[0]
        year_month_day = next_date_str.split('-')
        year, month, day = year_month_day
        hour = (next_datetime_str.split('T')[1]).split(':')[0]
        next = datetime.datetime(hour = int(hour), day=int(day), month=int(month), year=int(year))
        if last_time:
            break
        target = next
        if target == last:
            last_time = True
    ret = pd.DataFrame({})
    ret['Target Date'] = dates
    X = np.array(X)
    for i in range(0, n):
        X[:, i]
        ret[f'Target-{n-i}'] = X[:, i]
    ret['Target'] = Y
    return ret

def lstm_data_split(lstm_data):
    df_as_np = lstm_data.to_numpy()
    dates = df_as_np[:, 0]
    middle_matrix = df_as_np[:, 1:-1]
    X = middle_matrix.reshape((len(dates), middle_matrix.shape[1], 1))
    Y = df_as_np[:, -1]
    return dates, X.astype(np.float32), Y.astype(np.float32)

# Predict future values
def predict_future_with_lstm_model(model, last_known_window, last_date, n_days_ahead):
    n_hours = int(n_days_ahead * 24) #int conversion for api calls, is float
    future_dates = []
    for i in range(n_hours):
        if i == 0:
            next_date = last_date + datetime.timedelta(hours=1)
        else:
            next_date = future_dates[-1] + datetime.timedelta(hours=1)
        future_dates.append(next_date)
    
    future_predictions = []
    prediction_window = deepcopy(last_known_window)
    for i in range(n_hours):
        next_prediction = model.predict(np.array([prediction_window]), verbose=0).flatten()[0]
        clean_prediction(next_prediction, future_dates, i)
        future_predictions.append(next_prediction)
        prediction_window = np.roll(prediction_window, -1, axis=0)
        prediction_window[-1] = next_prediction
    
    return np.array(future_predictions), future_dates

def visualize_traffic_predictions(model, X_train, y_train, X_val, y_val, X_test, y_test, 
                                 dates_train, dates_val, dates_test,
                                 train_predictions, val_predictions, test_predictions,
                                 n_days_ahead,output_path):
    last_date = dates_test[-1]
    last_window = X_test[-1]
    future_predictions, future_dates = predict_future_with_lstm_model(
        model=model,
        last_known_window=last_window,
        last_date=last_date,
        n_days_ahead=n_days_ahead
    )
    print(f"Last test date: {dates_test[-1]}")
    print(f"First future date: {future_dates[0]}")
    print(f"Last future date: {future_dates[-1]}")
    plt.figure(figsize=(20, 8))
    plt.plot(future_dates, future_predictions, 'm-', linewidth=1.5, label='Future Predictions')
    plt.title('Future Traffic Predictions')
    plt.xlabel('Date')
    plt.ylabel('Number of Vehicles')
    plt.grid(True, alpha=0.3)
    date_form = DateFormatter("%m-%d %H:%M")
    plt.gca().xaxis.set_major_formatter(date_form)
    plt.xticks(rotation=45)
    all_data = np.concatenate([y_train, y_val, y_test])
    y_min = max(0, min(np.min(all_data), np.min(future_predictions)) - 5)
    y_max = max(np.max(all_data), np.max(future_predictions)) + 5
    plt.ylim(y_min, y_max)
    plt.axvline(x=last_date, color='k', linestyle='--', alpha=0.5)
    plt.text(last_date, y_max*0.95, 'Forecast Start', horizontalalignment='right')
    plt.tight_layout()
    plt.savefig(f'{output_path}/future_traffic_prediction_with_lstm.png', dpi=300)
    return future_predictions, future_dates

def clean_prediction(next_prediction,future_dates, current_hour):
    hour_of_day = future_dates[current_hour].hour
    if hour_of_day >= 22 or hour_of_day < 6:
        next_prediction = next_prediction * 0.4
    elif 7 <= hour_of_day <= 9:
        next_prediction = next_prediction * 2.5
    elif 16 <= hour_of_day <= 19:
        next_prediction = next_prediction * 2.5
    day_of_week = future_dates[current_hour].weekday()
    if day_of_week >= 5:
        next_prediction = next_prediction * 0.8 
    next_prediction = next_prediction + np.random.normal(0, next_prediction * 0.1)

def handle_web_request(data_path,junction_num,n_days_ahead,start_time,end_time,epoch,output_path):
    output_path = output_path
    junction_data = get_junction_data(data_path)
    joc = junction_data[junction_num]
    lstm_data = create_lstm_data(joc, start_time, end_time, n=168)
    dates, X, y = lstm_data_split(lstm_data)
    dates.shape, X.shape, y.shape
    dates_train,X_train,y_train = dates[:int(len(dates)*0.8)],X[:int(len(dates)*0.8)],y[:int(len(dates)*0.8)]
    dates_test,X_test,y_test = dates[int(len(dates)*0.9):],X[int(len(dates)*0.9):],y[int(len(dates)*0.9):]
    dates_val,X_val,y_val = dates[int(len(dates)*0.8):int(len(dates)*0.9)], X[int(len(dates)*0.8):int(len(dates)*0.9)], y[int(len(dates)*0.8):int(len(dates)*0.9)]

    model = Sequential([
        layers.Input((168, 1)),
        layers.LSTM(64),
        layers.Dense(32, activation='relu'),
        layers.Dense(32, activation='relu'),
        layers.Dense(1)
    ])
    model.compile(loss='mse', 
                optimizer=Adam(learning_rate=0.001),
                metrics=['mean_squared_error'])
    model.fit(X_train,y_train,validation_data=(X_val,y_val),epochs=epoch)

    train_predictions = model.predict(X_train).flatten()
    plt.figure(figsize=(20,5))
    plt.plot(dates_train, train_predictions)
    plt.plot(dates_train, y_train)
    plt.legend(['Training Predictions', 'Truth Values'])
    plt.savefig(f'{output_path}/training_predictions_vs_actual_values.png', dpi=300)

    val_predictions = model.predict(X_val).flatten()
    plt.figure(figsize=(20,5))
    plt.plot(dates_val, val_predictions)
    plt.plot(dates_val, y_val)
    plt.legend(['Validation Predictions', 'Truth Values'])
    plt.savefig(f'{output_path}/validation_predictions_vs_actual_values.png', dpi=300)

    test_predictions = model.predict(X_test).flatten()
    plt.figure(figsize=(20,5))
    plt.plot(dates_test, test_predictions)
    plt.plot(dates_test, y_test)
    plt.legend(['Testing Predictions', 'Truth Values'])
    plt.savefig(f'{output_path}/testing_predictions_vs_actual_values.png', dpi=300)

    future_predictions, future_dates = visualize_traffic_predictions(
        model=model,
        X_train=X_train, y_train=y_train,
        X_val=X_val, y_val=y_val,
        X_test=X_test, y_test=y_test,
        dates_train=dates_train,
        dates_val=dates_val,
        dates_test=dates_test,
        train_predictions=train_predictions,
        val_predictions=val_predictions,
        test_predictions=test_predictions,
        n_days_ahead=n_days_ahead,
        output_path=output_path
    )

    df = pd.DataFrame({'Time': future_dates, 'Predicted vehicle count': np.round(future_predictions).astype(int)})
    df.to_csv(f'{output_path}/future_traffic_predictions.csv', index=False)

def get_training_option(data_path, junction_number):
    junction_data = get_junction_data(data_path)
    joc = junction_data[junction_number]
    first_time = joc.index.min()
    last_time = joc.index.max()
    start_time = first_time + datetime.timedelta(hours=168)
    print(f"\nUser requested the analysis of junction {junction_number}, which has start time at {first_time}, and end start at {last_time}\n")
    print(f"To account for the interval shift during the LSTM model training process, the new start time is {start_time}\n")
    print(f"{start_time} and {last_time} will be used for model  training")
    return start_time,last_time

################################################################################################
# END OF FUNCTIONS
################################################################################################

# Sample usage, these variables need to be adjusted.
data_path = './Data/traffic.csv'
junction_number = 1
start_time, end_time = get_training_option(data_path,junction_number)
prediction_days_ahead = 3
output_path = './Result'

num_epochs = 50 # Keep this the same
handle_web_request(data_path=data_path,
                   junction_num=junction_number,
                   n_days_ahead=prediction_days_ahead,
                   start_time=start_time,
                   end_time=end_time, 
                   epoch=num_epochs,
                   output_path=output_path)

################################################################################################
# END OF EXAMPLE USAGE
################################################################################################