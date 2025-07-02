import sys
import os
import pytest
from app import app

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"LOAN STATUS" in response.data
    # assert response.json == {'message': 'Index page is rendered successfully.'}

def test_predict(client):
    test_data = {
        "Gender":1,
        "Married":1, 
        "Dependents":0,
        "Education":1,
        "Self_Employed":1,
        "ApplicantIncome":5000,
        "CoapplicantIncome":0,
        "LoanAmount":150,
        "Loan_Amount_Term":360,
        "Credit_History":1,
        "Property_Area":1
    }
    
    response = client.post('/predict_api', json={'data': test_data})
    assert response.status_code == 200
    assert response.json == {'prediction': 1}  # Assuming binary classification 
    