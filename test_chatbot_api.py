import pytest
import json
from app import app # Import the Flask app instance from your app.py file

# A pytest fixture to create a test client
@pytest.fixture
def client():
    # Configure the app for testing
    app.config['TESTING'] = True
    # Use a test client to make requests
    with app.test_client() as client:
        yield client # This makes the client available to test functions

# Test the homepage route (GET request)
def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    # Checks if the response contains the byte string for the index template
    assert b'<!DOCTYPE html>' in response.data 

# Test the API chat route with a valid "greeting" request (POST request)
def test_api_chat_greeting(client):
    # Data to send in the POST request (matches what the app expects)
    data = {"text": "Hello, how are you?"}
    
    # Send a POST request with JSON data to the /api/chat endpoint
    response = client.post(
        '/api/chat',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    # Check the JSON response data
    json_data = response.get_json()
    assert "Hello there!" in json_data['response']
    assert json_data['intent'] == 'greeting'

# Test the API chat route with an "order status" request
def test_api_chat_order_status(client):
    data = {"text": "Where is my package? Order number 12345."}
    
    response = client.post(
        '/api/chat',
        data=json.dumps(data),
        content_type='application/json'
    )
    
    assert response.status_code == 200
    json_data = response.get_json()
    assert "To check your order status, please provide your order ID." in json_data['response']
    assert json_data['intent'] == 'order_status'





#personal:test for "hello (name)"
import pytest
from nlp_utils import extract_name

def test_extract_name_simple():
    assert extract_name("Hello, my name is Alice") == "Alice"

def test_extract_name_full_name():
    assert extract_name("Please call me Dr. Jane Smith") == "Jane Smith"

def test_extract_name_not_present():
    assert extract_name("I need help with my account.") is None

def test_extract_name_complex_sentence():
    # NER can sometimes be tricky; this tests how well the base model does
    assert extract_name("My friend Sarah and I went to the store.") == "Sarah"

