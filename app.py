import joblib
import os
from flask import Flask, request, render_template, jsonify, app, url_for, redirect

import numpy as np

from src.logging import logger 

app = Flask(__name__)

# Load the model
model = joblib.load(os.path.join('models', 'loan_status_predict'))
scaler = joblib.load(os.path.join('models', 'scaler'))

logger.logging.info("ML Model is loaded successfully.")

@app.route('/')
def home():
    return render_template('index.html')
    logger.logging.info("Index page is rendered successfully.")

@app.route('/predict_api', methods=['POST'])
def predict_api():
    try:
        # Get the form data
        data = request.json['data']
        logger.logging.info(f"Form data received: {data}")
        print (f"Form data received: {data}")

        # Convert the form data to a numpy array
        input_data = np.array(list(data.values())).reshape(1, -1)
        logger.logging.info(f"Input data for prediction: {input_data}")

        # Scale the input data
        input_data = scaler.transform(input_data)

        # Make the prediction
        prediction = model.predict(input_data)
        logger.logging.info(f"Prediction result: {prediction}")

        # Return the prediction result
        return jsonify({'prediction': int(prediction[0])})
    
    except Exception as e:
        logger.logging.error(f"Error during prediction: {e}")
        return jsonify({'error': str(e)})
    
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the form data
        data = [float(x) for x in request.form.values()]
        logger.logging.info(f"Form data received: {data}")

        # Scale the input data
        logger.logging.info(f"Scaling Started: {data}")
        input_data = scaler.transform(np.array(data).reshape(1, -1))
        logger.logging.info(f"Scaling Completed: {input_data}")

        # Make the prediction
        prediction = model.predict(input_data)
        logger.logging.info(f"Prediction result: {prediction}")

        # Return the prediction result
        return render_template('result.html', prediction_text=f'{"Approved" if prediction[0] == 1 else "Rejected"}')
    
    except Exception as e:
        logger.logging.error(f"Error during prediction: {e}")
        return render_template('result.html', error=str(e))
    
if __name__ == '__main__':
    app.run(debug=True)

