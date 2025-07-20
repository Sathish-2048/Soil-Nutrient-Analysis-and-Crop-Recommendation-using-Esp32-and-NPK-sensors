from flask import Flask, request, jsonify
import os
import joblib
import numpy as np
from datetime import datetime
app = Flask(__name__)
MODEL_PATH = "C:\\Users\\Sathish\\Downloads\\model_nb.pkl"
model = joblib.load(MODEL_PATH)
label_encoder = joblib.load("C:\\Users\\Sathish\\Downloads\\label_encoder.pkl")
CSV_FILE = 'npk_sensor_data.csv'
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, 'w') as f:
        f.write("Moisture,Temperature,pH,Nitrogen,Phosphorus,Pottasium,Timestamp,Prediction\n ")

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    if data:
        required_fields = ['Moisture', 'Temperature', 'pH','Nitrogen','Phosphorus','Pottasium']
        try:
            mois = float(data.get("Moisture"))/10
            temp = float(data.get("Temperature"))/10
            ph = float(data.get("pH"))/100
            nit = float(data.get("Nitrogen"))/10
            pho = float(data.get("Phosphorus"))/10
            pot = float(data.get("Pottasium"))/10
            rf = 64
            input_features = np.array([[nit,pho,pot,temp,mois,ph,rf]])
            prediction = model.predict(input_features)[0]
            class_name = label_encoder.inverse_transform([prediction])[0]
            with open(CSV_FILE, 'a') as f:
                f.write(f'{mois},{temp},{ph},{nit},{pho},{pot},{datetime. now().strftime("%Y-%m-%d %H:%M:%S")},{class_name}\n')
            return jsonify(message='Data received', data=data), 200
        except Exception as e:
            return jsonify(message=e, error=str(e)), 500
    return jsonify(message='No data received'), 400
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)  
