# server.py 
from flask import Flask, jsonify, request, render_template
from functionalities import handle_web_request, get_training_option
import json
import os

app = Flask(__name__) 

data_path = './Data/traffic.csv'
output_path = './Result'

@app.route('/') 
def root(): 
    return render_template("index.html")

#/predict
@app.route('/predict', methods=['POST']) 
def predictions_endpoint(): 
   
    if request.method == 'POST':
        try:
            data = json.loads(request.data.decode('utf-8'))
            junction_num = int(data.get('junction'))
            
            prediction_length = int(data.get('prediction_length', 24))
            interval = data.get('interval', 'hours')
            
            if interval == 'hours':
                n_days_ahead = prediction_length / 24  # Convert hours to days
            elif interval == 'days':
                n_days_ahead = prediction_length
            else:
                return jsonify({"error": f"Unsupported interval: {interval}. Use 'hours' or 'days'."})
            
            result = handle_web_request(data_path, junction_num, output_path, n_days_ahead)
            if "error" in result:
                return jsonify({"error": result["error"]})
            response = {
                "success": True,
                "junction": junction_num,
                "prediction_start": result["prediction_start"],
                "prediction_end": result["prediction_end"],
                "plot_url": f"/results/{os.path.basename(result['plot_path'])}",
                "csv_url": f"/results/{os.path.basename(result['csv_path'])}"
            }
            return jsonify(response)
        except Exception as e:
            return jsonify({"error": f"Failed to process request: {str(e)}"})

if __name__ == "__main__":
    host = "127.0.0.1"
    port_number = 8080
    print(f"Starting server at {host}:{port_number}")
    print(f"Data path: {data_path}, Output directory: {output_path}")
    app.run(host, port_number)