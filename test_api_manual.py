import requests
import json

# The URL of the chat API endpoint when your Flask server is running
API_URL = "http://127.0.0.1:5000/api/chat"

def chat_session_test():
    # Use a requests.Session to persist cookies across requests
    with requests.Session() as session:
        def send_message(message):
            # Data we are sending to the API
            payload = {"text": message}
            
            # Send a POST request with JSON data using the session
            response = session.post(API_URL, json=payload)
            
            # Check if the request was successful
            if response.status_code == 200:
                # Get the JSON response from the bot
                bot_response = response.json()
                print(f"User Input: {message}")
                print(f"Bot Response: {bot_response['response']}")
                # The intent key might not be present if your app.py only handles simple text
                # response from DialoGPT, you may need to adjust this line.
                # print(f"Detected Intent: {bot_response.get('intent', 'N/A')}") 
                print("-" * 20)
            else:
                print(f"Error: API returned status code {response.status_code}")

        print("--- Testing Chatbot API with Conversation History ---")
        
        # 1. Start with a greeting. The model should remember this context.
        send_message("Hello there!")
        
        # 2. Ask a follow-up question. The bot's response should be contextual.
        #    For example, if your bot is about general chat, the context helps
        #    guide the follow-up response.
        send_message("How are you doing today?")

        # 3. Add a specific context point (e.g., a hobby).
        send_message("I really enjoy hiking on the weekends.")

        # 4. A general follow-up. The bot might use the hobby in its response
        #    if memory is working correctly.
        send_message("What do you think about that?")

        print("--- End of Test ---")

if __name__ == "__main__":
    chat_session_test()

