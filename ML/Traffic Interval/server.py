# server.py 
from flask import Flask, jsonify, request, render_template
from functionalities import make_prediction

app = Flask(__name__) 

@app.route('/') 
def root(): 
    return render_template("index.html")
#/predict
@app.route('/predict', methods=['POST']) 
def predictions_endpoint(): 
   
    if request.method == 'POST': 
        
        file = request.data

        #make_predictions change to what file is, file is data from client
        predicted_class = make_prediction(file)
    
    return jsonify(predicted_class.item()) 


if __name__ == "__main__": 

    host = "127.0.0.1"
    port_number = 8080 

    app.run(host, port_number)




'''
server.py is expected to send date in this format to the make_prediction function:

***
{
    "start_date": "2023-01-01 00:00:00",
    "prediction_length": 24,
    "interval": "hours",
    "junction": INTEGER
}
***

'''