###PERSONAL TIPS FOR CODING
#"".\my_ai_env\Scripts\activate" paste at start of every new terminal for virtual environment(malan did this)
#Document hashtag with "personal:" on top of code section whcih explains purpose so your not confused
#Make sure code # titles are correct
#Main code here and tests in next file
#Run this to test code"python test_chatbot_api.py"
#Ask extra questions b/c to master you need 10x info/keep short to make coding efficeint
#KEEP ALL MOST IMPORTANT CODING TIPS NEAR TOP:
#Tip:ALWAYS PASTE ENTIRE ERROR FEEDBACK TO AI SO IT CAN ACTUALLY HELP
#Tip:Debug every error even then tell ai what you did,highlighting/color coded stuff helps with errors
#Tip:"View" then ""Terminal"to open terminal without pasting anything and kill often to avoid bugs
#Tip:"enter" after pasting so code runs without glitches
#Tip:Press "ctrl"+"s" to save before running code every time
#Tip:Press "ctrl"+"c" as best way to kill infinite runnning code
#Tip:Highlight code then press "ctrl"+"/" to turn all lines to comments



    #DO DOCSTRINGS LIKE THIS B/C ITS"STANDARD GOOGLE STYLE"/"""MUST ALIGN W/ START OF FUNCTION
    #"""
    # 

    # After 1 line summary explain more detailed logic if needed (optional).

    # Args:
        # 

    # Returns:
        # 
    #"""




import spacy
import secrets
import json
import torch
from flask import Flask, render_template, request, jsonify, session
from transformers import AutoModelForCausalLM, AutoTokenizer
import os # Imported for potential future use or better error handling

# Create the Flask application instance and set a secret key for session management
app = Flask(__name__)
# Generate a secure random key for managing sessions (needed for history/memory)
app.secret_key = secrets.token_hex(16)

# --- 2. Model Loading (Load models once globally) ---

# Load the small English spaCy model for name extraction
try:
    nlp = spacy.load("en_core_web_sm")
    print("Loaded SpaCy model: en_core_web_sm")
except (OSError, ImportError):
    print("Downloading SpaCy model 'en_core_web_sm'. Please wait.")
    # Use the subprocess method to ensure download works reliably
    spacy.cli.download("en_core_web_sm") 
    nlp = spacy.load("en_core_web_sm")

# Load the DialoGPT Conversational Model
model_name = "microsoft/DialoGPT-small"
try:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    print(f"Loaded DialoGPT model: {model_name}")
except Exception as e:
    print(f"Error loading DialoGPT model: {e}")
    tokenizer = None
    model = None

# --- Helper Functions ---

def extract_name(user_input: str) -> str | None:
    """
    Extracts a potential person's name from a given user input string using spaCy.

    Args:
        user_input: The string provided by the user that needs to be analyzed for a name.

    Returns:
        str or None: The string name of the user, or None if no name is found.
    """

    if nlp:
        doc = nlp(user_input)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
    return None

def handle_specific_intents(user_message: str) -> str | None:
    """
    Checks user input against predefined rules to provide specific, non-AI responses.

    This function intercepts specific phrases (like "what is a sub?") and provides 
    a hardcoded, intelligent response to prevent the general AI model from generating 
    a quirky response based on its training data.

    Args:
        user_message: The current text input from the user.

    Returns:
        str or None: A predefined response string if a match is found, 
                     otherwise None to allow the AI model to handle the request.
    """
    message_lower = user_message.lower()

    if any(phrase in message_lower for phrase in ["what is a sub", "what is a 'sub'"]):
        return "A 'sub' in online communities often refers to a 'subreddit' on the platform Reddit, which is a dedicated forum for a specific topic."
    
    if any(phrase in message_lower for phrase in ["why are you talking about cats", "stop talking about cats"]):
        return "My training data included a lot of conversation about cats! I can try to focus on our current conversation topic if you prefer."

    # Add more specific handlers here as you identify problematic topics

    return None

def generate_ai_response(user_message, chat_history_ids=None):
    """
    Generates a conversational AI response using DialoGPT and manages history tensors.

    Args:
        user_message: The current text input from the user (a string).
        chat_history_ids: A PyTorch tensor or list containing previous conversation 
                      history tokens, or None if starting a new chat session.

    Returns:
    tuple[str, torch.Tensor or None]: A tuple containing the bot response text 
                                      (string) and the full updated history tensor 
                                      (torch.Tensor), or None if the model failed to load.
    """

    if not tokenizer or not model:
        return "Sorry, the AI model is not available.", None

    MAX_HISTORY_LENGTH = 512 

    if chat_history_ids is not None:
        # Ensure it's a tensor
        if isinstance(chat_history_ids, list):
             chat_history_ids = torch.tensor(chat_history_ids, dtype=torch.long)
             
        if chat_history_ids.shape[-1] >= MAX_HISTORY_LENGTH:
            # Truncate old history if it gets too long
            chat_history_ids = chat_history_ids[:, -MAX_HISTORY_LENGTH + 50:]

    # Encode the new user input
    new_input_ids = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors='pt')

    # Concatenate new input with history to form the full input sequence for generation
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids

    # Generate a response with adjusted parameters for coherence
    updated_chat_history_ids = model.generate(
        bot_input_ids, 
        max_length=bot_input_ids.shape[-1] + 50,
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=4,  # Increased from 3 to 4 for slightly more coherence
        do_sample=True,
        top_k=50,
        top_p=0.9,
        temperature=0.6 # Lowered from 0.7 to 0.6 (less random/creative)
    )
    
    # Decode only the *new* part of the tensor that the bot just generated
    bot_response = tokenizer.decode(updated_chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    
    # Return the response text AND the full updated history tensor
    return bot_response, updated_chat_history_ids


# --- Routes ---

@app.route('/')
def index():
    """
    Renders the main chatbot interface HTML page.
        str: The rendered HTML content of the 'index.html' template.
    """
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def handle_chat_api():
    """
    Handles the main API logic for the chatbot.

    Processes incoming user messages, checks for specific intents, manages 
    conversation history via Flask sessions, generates an AI response, and 
    returns a structured JSON object.

    Returns:
        jsonify: A JSON response containing the chatbot's reply and the intent type.
    """
    data = request.get_json()
    user_message = data.get("text", "")
    
    # 1. Check for specific, rule-based responses FIRST (New Logic)
    specific_response = handle_specific_intents(user_message)
    if specific_response:
        return jsonify({
            "intent": "Rule_Based_Response",
            "response": specific_response
        })

    # 2. Handle your existing color logic (Specific Override)
    if any(phrase in user_message.lower() for phrase in ["my favorite color", "favorite color is", "do you know my color", "what is my color"]):
        bot_response = "I remember you mentioned your favorite color is blue!"
        return jsonify({
            "intent": "Fact_Retrieval",
            "response": bot_response
        })
    
    # 3. If no specific rules triggered, proceed to the general AI model
    chat_history_ids = None

    # Retrieve history from the Flask session safely
    if 'chat_history' in session:
        try:
            history_list = json.loads(session['chat_history'])
            if history_list:
                chat_history_ids = torch.tensor(history_list, dtype=torch.long)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error restoring session history: {e}. Starting fresh session.")
            session.pop('chat_history', None)


    # Get AI response and updated history
    bot_response, updated_chat_history_ids = generate_ai_response(user_message, chat_history_ids)
    
    # Save the updated history back to the session *as a JSON string*
    if updated_chat_history_ids is not None:
        # Convert tensor to a list first, then to a JSON string for storage
        session['chat_history'] = json.dumps(updated_chat_history_ids.tolist())
    
    # Integrate name extraction for a better greeting/response structure
    name = extract_name(user_message)
    if name and "hello" in bot_response.lower():
         # Modify the response if a name was found in the greeting
         bot_response = f"Hello, {name}! How can I help you?"
         

    return jsonify({
        "intent": "AI_Response_Generated",
        "response": bot_response
    })
