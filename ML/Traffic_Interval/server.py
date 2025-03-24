from flask import Flask, jsonify, request, render_template, send_from_directory
from functionalities import handle_web_request, get_training_option
import json
import os
import pandas as pd

app = Flask(__name__)

data_path = './Data/traffic.csv'
output_path = './Result'

@app.route('/')
def root():
    return render_template("index.html")

#/predict, endpoint works w/ get + post 
@app.route('/predict', methods=['GET', 'POST'])
def predictions_endpoint():
    try:
        #Json params via post or query string w/ get
        if request.method == 'POST':
            data = json.loads(request.data.decode('utf-8'))
        else:
            data = request.args

        
        junction_num = int(data.get('junction'))
        prediction_length = int(data.get('prediction_length', 24))
        interval = data.get('interval', 'hours')
        epoch = int(data.get('epoch', 50))

        if interval == 'hours':
            n_days_ahead = int(prediction_length / 24)
        elif interval == 'days':
            n_days_ahead = int(prediction_length)
        else:
            return jsonify({"error": f"Unsupported interval: {interval}. Use 'hours' or 'days'."})

        start_time, end_time = get_training_option(data_path, junction_num)

        handle_web_request(data_path, junction_num, n_days_ahead, start_time, end_time, epoch, output_path)

        future_csv = os.path.join(output_path, 'future_traffic_predictions.csv')
        df = pd.read_csv(future_csv)
        if df.empty:
            prediction_start = ""
            prediction_end = ""
        else:
            prediction_start = df['Time'].iloc[0]
            prediction_end = df['Time'].iloc[-1]

        response = {
            "success": True,
            "junction": junction_num,
            "prediction_start": prediction_start,
            "prediction_end": prediction_end,
            "plot_url": f"/results/future_traffic_prediction_with_lstm.png",
            "csv_url": f"/results/future_traffic_predictions.csv"
        }
        return jsonify(response)

    except Exception as e:
        return jsonify({"error": f"Failed to process request: {str(e)}"})

@app.route('/training_option', methods=['GET'])
def training_option():
    try:
        junction_num = int(request.args.get('junction'))
        start_time, end_time = get_training_option(data_path, junction_num)
        return jsonify({
            "junction": junction_num,
            "start_time": str(start_time),
            "end_time": str(end_time)
        })
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/results/<path:filename>')
def serve_result(filename):
    return send_from_directory(output_path, filename)

if __name__ == "__main__":
    host = "127.0.0.1"
    port_number = 8080
    print(f"Starting server at {host}:{port_number}")
    print(f"Data path: {data_path}, Output directory: {output_path}")
    app.run(host, port_number)
