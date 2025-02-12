import pandas as pd
import numpy as np
import torch
import torch.nn as nn
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from datetime import datetime, timedelta

# Same model as in model_v1.ipynb
class JunctionTrafficLSTM(nn.Module):
    def __init__(self, input_size=5, hidden_size=32, num_layers=5, output_size=1):
        super(JunctionTrafficLSTM, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.dropout = nn.Dropout(0.2)
        self.fc1 = nn.Linear(hidden_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()
    def forward(self, x, future_steps=1, teacher_forcing_ratio=0.5):
        batch_size = x.size(0)
        outputs = []
        lstm_out, (h, c) = self.lstm(x)
        decoder_input = x[:, -1:, :]
        for i in range(future_steps):
            out, (h, c) = self.lstm(decoder_input, (h, c))
            features = self.dropout(out[:, -1])
            features = self.relu(self.fc1(features))
            features = self.relu(self.fc2(features))
            prediction = self.fc3(features)
            outputs.append(prediction)
            next_input = decoder_input.clone()
            next_input[:, 0, 0] = prediction.squeeze()
            decoder_input = next_input
        
        return torch.stack(outputs, dim=1)

# Change the model_path to get different model
class TrafficPredictor:
    def __init__(self, model_path='best_saved_model.pth', data_path='./Data/traffic.csv'):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = JunctionTrafficLSTM().to(self.device)
        self.model.load_state_dict(torch.load(model_path, map_location=self.device))
        self.model.eval()
        # Load and process initial data for scalers and encoders
        self.df = pd.read_csv(data_path)
        self.df['DateTime'] = pd.to_datetime(self.df['DateTime'])
        self.setup_preprocessors()
    def setup_preprocessors(self):
        # Set up encoders and scalers
        self.junction_encoder = LabelEncoder()
        self.df['Junction_encoded'] = self.junction_encoder.fit_transform(self.df['Junction'])
        
        self.scalers = {}
        numerical_features = ['Vehicles', 'Hour', 'DayOfWeek', 'Month', 'Junction_encoded']
        for feature in numerical_features:
            scaler = MinMaxScaler()
            self.df[f'{feature}_normalized'] = scaler.fit_transform(self.df[[feature]])
            self.scalers[feature] = scaler

    def prepare_sequence(self, latest_time, junction, seq_length=10):
        # Filter data for specific junction
        junction_data = self.df[self.df['Junction'] == junction].copy()
        
        # Find closest time
        closest_time_idx = (junction_data['DateTime'] - latest_time).abs().argmin()
        
        # Get recent sequence
        feature_cols = [col for col in self.df.columns if '_normalized' in col]
        input_seq = junction_data.iloc[closest_time_idx:closest_time_idx+seq_length][feature_cols].values
        
        return torch.tensor(input_seq, dtype=torch.float32).unsqueeze(0).to(self.device)

    def predict(self, input_data):
        """
        Expects input_data as a dictionary with:
        - start_date: string in format "YYYY-MM-DD HH:MM:SS"
        - prediction_length: integer (number of steps to predict)
        - interval: string ('hours', 'days', or 'months')
        - junction: string or int (junction identifier)
        """
        try:
            start_date = pd.to_datetime(input_data['start_date'])
            prediction_length = int(input_data['prediction_length'])
            interval = input_data['interval']
            junction = input_data['junction']
            
            input_seq = self.prepare_sequence(start_date, junction)
            
            with torch.no_grad():
                predictions = self.model(input_seq, future_steps=prediction_length)
                predictions = predictions.squeeze().cpu().numpy()
            
            # Inverse transform predictions
            predictions = self.scalers['Vehicles'].inverse_transform(
                predictions.reshape(-1, 1)
            ).flatten()
            
            # Generate timestamps
            if interval == 'hours':
                timestamps = [start_date + timedelta(hours=i) for i in range(prediction_length)]
            elif interval == 'days':
                timestamps = [start_date + timedelta(days=i) for i in range(prediction_length)]
            elif interval == 'months':
                timestamps = [start_date + pd.DateOffset(months=i) for i in range(prediction_length)]
            
            # results
            results = {
                'timestamps': [ts.strftime("%Y-%m-%d %H:%M:%S") for ts in timestamps],
                'predictions': predictions.tolist(),
                'junction': junction
            }
            return results
        except Exception as e:
            return {'error': str(e)}

def make_prediction(input_data):
    predictor = TrafficPredictor()
    return predictor.predict(input_data)