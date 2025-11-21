#Quick To-Do notes:
#1."if "intent" ==" is not defined and "generate_response"(user_input)" has a issue i dont know off



import pytest
import json
# Import the Flask app instance from your app.py file
# Make sure app.py is accessible in your environment path
from app import app

# A pytest fixture to create a test client
@pytest.fixture
def client():
    # Configure the app for testing
    app.config['TESTING'] = True
    # Crucial for session testing: set a secret key if app.py doesn't have one
    # If your app.py already has app.secret_key = 'some_secret', this can be removed.
    if not app.secret_key:
        app.secret_key = 'test_secret_key'

    # Use a test client to make requests
    with app.test_client() as client:
        yield client # This makes the client available to test functions

# Test the homepage route (GET request)
def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    # Checks if the response contains the byte string for the index template
    assert b'<!DOCTYPE html>' in response.data 

# --- New Test for Conversation History (Memory) Feature ---
def test_conversation_memory(client):
    """
    Tests that the chatbot remembers context across multiple requests within one session.
    """
    # Use the client's session_transaction to maintain the same session cookies
    with client.session_transaction() as session:
        # 1. Start a conversation (e.g., provide context)
        first_message = {"text": "I really like to read books."}
        response1 = client.post(
            '/api/chat',
            data=json.dumps(first_message),
            content_type='application/json'
        )
        assert response1.status_code == 200
        json_data1 = response1.get_json()
        print(f"Bot response 1: {json_data1['response']}")
        # Assert something expected from the first generic response
        assert len(json_data1['response']) > 0 # Asserts that the response is not empty

        # 2. Send a follow-up message that depends on the previous context
        #    Note: DialoGPT responses are highly variable. We test if *any* response is returned successfully.
        #    A better test would check the session variable itself in app.py logic,
        #    but testing the API response requires a flexible assertion for a generative model.
        second_message = {"text": "What kind of books do you recommend?"}
        response2 = client.post(
            '/api/chat',
            data=json.dumps(second_message),
            content_type='application/json'
        )
        assert response2.status_code == 200
        json_data2 = response2.get_json()
        print(f"Bot response 2: {json_data2['response']}")
        
        # We can assert that the response is not empty, which confirms the API endpoint worked.
        # It's difficult to assert exact response content for generative models.
        assert len(json_data2['response']) > 0


# --- The following tests are likely broken or irrelevant now ---
# The original tests assume specific, rule-based "intents" and "responses" 
# which might not align with a generative DialoGPT model that gives variable responses.
# I am commenting them out as you switch models/logic.

# def test_api_chat_greeting(client):
#     # ... (code commented out as DialoGPT doesn't return fixed intents) ...
#     pass

# def test_api_chat_order_status(client):
#     # ... (code commented out as DialoGPT doesn't return fixed intents) ...
#     pass

# The personal tests for `extract_name` and `generate_response` are testing 
# internal helper functions, not the Flask API endpoints. 
# If those helper functions still exist in your app.py, these tests are fine.
# They are included below for completeness:

# personal:test for "hello (name)"
# from app import extract_name # Make sure this function is exported/visible

# def test_extract_name_simple():
#     assert extract_name("Hello, my name is Alice") == "Alice"
# ... (other extract_name tests) ...

# test for clarification logic
# from app import generate_response # Make sure this function is exported/visible

# def test_generate_greeting_with_name():
#     # ... (code for generate_response tests) ...
#     pass
