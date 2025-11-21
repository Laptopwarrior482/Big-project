#Quick To-Do notes:
#1."if "intent" ==" is not defined and "generate_response"(user_input)" has a issue i dont know off




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
from app import extract_name

def test_extract_name_simple():
    assert extract_name("Hello, my name is Alice") == "Alice"

def test_extract_name_full_name():
    assert extract_name("Please call me Dr. Jane Smith") == "Jane Smith"

def test_extract_name_not_present():
    assert extract_name("I need help with my account.") is None

def test_extract_name_complex_sentence():
    # NER can sometimes be tricky; this tests how well the base model does
    assert extract_name("My friend Sarah and I went to the store.") == "Sarah"




#test for clarifcation logic
from app import generate_response

def test_generate_greeting_with_name():
    """
    Tests that the bot correctly generates a personalized greeting.
    """
    user_input = "Hi, my name is Bob"
    expected_response = "Hello, Bob!"
    actual_response = generate_response(user_input)
    assert actual_response == expected_response

def test_generate_generic_greeting():
    """
    Tests that the bot generates a generic greeting when no name is found.
    """
    user_input = "Hello there! How are you?"
    expected_response = "Hello there!"
    actual_response = generate_response(user_input)
    assert actual_response == expected_response

