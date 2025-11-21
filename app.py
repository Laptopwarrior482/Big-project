#"".\my_ai_env\Scripts\activate" paste at start of every new terminal for virtual environment(malan did this)
#Document hashtag with "personal:" on top of code section whcih explains purpose so your not confused
#Make sure code # titles are correct
#Main code here and tests in next file
#Run this to test code"python test_chatbot_api.py"
#Ask extra questions b/c to master you need 10x info/keep short to make coding efficeint
#KEEP ALL MOST IMPORTANT CODING TIPS NEAR TOP:
#Tip:Debug every error even then tell ai what you did,highlighting/color coded stuff helps with errors
#Tip:"View" then ""Terminal"to open terminal without pasting anything and kill often to avoid bugs
#Tip:"enter" after pasting so code runs without glitches
#Tip:Press "ctrl"+"s" to save before running code every time
#Tip:Press "ctrl"+"c" as best way to kill infinite runnning code
#Tip:Highlight code then press "ctrl"+"/" to turn all lines to comments


#NLP Logic/Model Code (PyTorch/ Transformers/SpaCy): ~300-600 line
#1(Done).Goal=make robot say "hello (name)"
#2(Done).Use spacy
#(Done)3.Simple logic,like if sentence says "hello" in it then classify intent as greeting
#4().Transformers for model and pytorch to define input then run through model
#5.Write a pytest for each corresponding function



import spacy
from flask import Flask, render_template, request, jsonify, session
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import secrets

# Create the Flask application instance and set a secret key for session management
app = Flask(__name__)
# Generate a secure random key for managing sessions (needed for history/memory)
app.secret_key = secrets.token_hex(16)


# --- 2. Model Loading (Load models once globally) ---

# Load the small English spaCy model for name extraction
try:
    nlp = spacy.load("en_core_web_sm")
except (OSError, ImportError):
    print("Downloading SpaCy model 'en_core_web_sm'. Please wait.")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

# Load the DialoGPT Conversational Model
try:
    model_name = "microsoft/DialoGPT-small"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)
    print(f"Loaded DialoGPT model: {model_name}")
except Exception as e:
    print(f"Error loading DialoGPT model: {e}")
    tokenizer = None
    model = None

# --- Helper Function ---

def extract_name(user_input: str) -> str | None:
    """
    Attempts to extract a person's name from a given string using SpaCy NER.
    """
    if nlp:
        doc = nlp(user_input)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
    return None

def generate_ai_response(user_message, chat_history_ids=None):
    """
    Generates a conversational AI response using DialoGPT and manages history tensors.
    """
    if not tokenizer or not model:
        return "Sorry, the AI model is not available.", None

    # Encode the new user input
    new_input_ids = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors='pt')

    # Concatenate new input with chat history
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids

    # Generate a response
    chat_history_ids = model.generate(
        bot_input_ids, 
        max_length=100, 
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        do_sample=True,
        top_k=50,
        top_p=0.9,
        temperature=0.7 # Adjust temperature to make responses less repetitive
    )

    # Decode the last response from the bot
    bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:], skip_special_tokens=True)
    
    return bot_response, chat_history_ids


# --- 3. Routes and Logic (The API endpoint) ---

@app.route('/')
def home():
    # You need an 'index.html' file in a 'templates' folder for this to work
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def handle_chat_api():
    data = request.get_json()
    user_message = data.get("text", "")
    
    # Get chat history from the Flask session, if it exists
    # History is stored as a list of numbers (bytes), so we convert back to a PyTorch tensor
    chat_history_bytes = session.get('chat_history', None)
    chat_history_ids = torch.tensor(chat_history_bytes) if chat_history_bytes else None

    # Get AI response and updated history
    bot_response, chat_history_ids = generate_ai_response(user_message, chat_history_ids)
    
    # Save the updated history back to the session for the next request
    # Convert tensor back to a list/bytes that Flask can save in the session
    if chat_history_ids is not None:
        session['chat_history'] = chat_history_ids.tolist()
    
    # Integrate name extraction for a better greeting
    name = extract_name(user_message)
    if name and "hello" in bot_response.lower():
         bot_response = f"Hello, {name}! {bot_response.split('!', 1)[-1].strip()}"

    return jsonify({
        "intent": "AI_Response_Generated",
        "response": bot_response
    })

# Note: Remember to run with `flask --app app run`
