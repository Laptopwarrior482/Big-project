import requests
import json

# The URL of the chat API endpoint when your Flask server is running
API_URL = "http://127.0.0.1:5000/api/chat"

def test_send_message(message):
    # Data we are sending to the API
    payload = {"text": message}
    
    # Send a POST request with JSON data
    response = requests.post(API_URL, json=payload)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Get the JSON response from the bot
        bot_response = response.json()
        print(f"User Input: {message}")
        print(f"Bot Response: {bot_response['response']}")
        print(f"Detected Intent: {bot_response['intent']}")
        print("-" * 20)
    else:
        print(f"Error: API returned status code {response.status_code}")

if __name__ == "__main__":
    print("--- Testing Chatbot API ---")
    
    # Test a greeting with a name (should detect name and 'greeting' intent)
    test_send_message("Hi there, my name is Alex")
    
    # Test a different intent (e.g., tech support)
    test_send_message("My computer is broken and I need help")
    
    # Test an unknown intent
    test_send_message("Tell me about the history of the moon")

