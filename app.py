import joblib
import os
from flask import Flask, request, render_template, jsonify, url_for, redirect
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np

from src.logging.logger import logger 
app = Flask(__name__)
CORS(app) 

# Load the model
model = joblib.load(os.path.join('models', 'loan_status_predict'))
scaler = joblib.load(os.path.join('models', 'scaler'))

logger.info("ML Model is loaded successfully.")

@app.route('/')
def home():
    logger.info("Index page is rendered successfully.")
    return {
        "Info":"Index page is rendered successfully."
    }
    
@app.route('/predict_api', methods=['POST'])
def predict_api():
    try:
        # Get the form data
        data = request.json['data']
        logger.info(f"Form data received: {data}")
        print (f"Form data received: {data}")

        # Convert the form data to a numpy array
        input_data = np.array(list(data.values())).reshape(1, -1)
        logger.info(f"Input data for prediction: {input_data}")

        # Scale the input data
        input_data = scaler.transform(input_data)

        # Make the prediction
        prediction = model.predict(input_data)
        logger.info(f"Prediction result: {prediction}")

        # Return the prediction result
        return jsonify({'prediction': int(prediction[0])})
    
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return jsonify({'error': str(e)})
    
from flask import request, jsonify

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get JSON data
        data = request.get_json()
        logger.info(f"Form data received: {data}")

        # Convert dict to list in correct feature order
        input_features = [
            data['Gender'],
            data['Married'],
            data['Dependents'],
            data['Education'],
            data['Self_Employed'],
            data['ApplicantIncome'],
            data['CoapplicantIncome'],
            data['LoanAmount'],
            data['Loan_Amount_Term'],
            data['Credit_History'],
            data['Property_Area']
        ]

        logger.info(f"Input features list: {input_features}")

        # Scale the input data
        input_array = np.array(input_features).reshape(1, -1)
        logger.info(f"Numpy array for scaling: {input_array}")

        scaled_input = scaler.transform(input_array)
        logger.info(f"Scaled input: {scaled_input}")

        # Make the prediction
        prediction = model.predict(scaled_input)
        logger.info(f"Prediction result: {prediction}")

        # Return JSON response
        prediction_text = 'Approved' if prediction[0] == 1 else 'Rejected'
        return jsonify({
            "status": prediction_text
        })

    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return jsonify({"error": str(e)}), 500
    
if __name__ == '__main__':
    logger.info("Starting Flask app...")
    app.run(debug=True, host='127.0.0.1', port=5000)

