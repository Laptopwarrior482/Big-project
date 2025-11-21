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
    # ... (function remains the same) ...
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

    # Define the maximum length the model can handle (DialoGPT small is often 512)
    MAX_HISTORY_LENGTH = 512 

    # Truncate history if it's getting too long *before* adding the new input
    if chat_history_ids is not None and chat_history_ids.shape[1] >= MAX_HISTORY_LENGTH:
        # Keep only the most recent tokens that fit within the max length
        chat_history_ids = chat_history_ids[:, -MAX_HISTORY_LENGTH + 50:] # Keep recent history + some buffer

    # Encode the new user input
    new_input_ids = tokenizer.encode(user_message + tokenizer.eos_token, return_tensors='pt')

    # Concatenate new input with truncated chat history
    bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1) if chat_history_ids is not None else new_input_ids

    # Generate a response
    chat_history_ids = model.generate(
        bot_input_ids, 
        max_length=bot_input_ids.shape[-1] + 50, # Set max generation length dynamically
        pad_token_id=tokenizer.eos_token_id,
        no_repeat_ngram_size=3,
        do_sample=True,
        top_k=50,
        top_p=0.9,
        temperature=0.7
    )

    # Decode the last response from the bot
    bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:], skip_special_tokens=True)
    
    return bot_response, chat_history_ids


# --- 3. Routes and Logic (The API endpoint) ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def handle_chat_api():
    data = request.get_json()
    user_message = data.get("text", "")
    
    chat_history_ids = None

    # Retrieve history from the Flask session
    if 'chat_history' in session:
        # Convert the list of integers back to a PyTorch tensor
        # CRITICAL FIX: Ensure we reconstruct the tensor in the correct 2D shape (batch_size=1)
        history_list = session['chat_history']
        if history_list and isinstance(history_list, list) and isinstance(history_list[0], list):
             # Handle the nested list structure correctly for the tensor constructor
            chat_history_ids = torch.tensor(history_list, dtype=torch.long)
        elif history_list and isinstance(history_list, list) and isinstance(history_list[0], int):
            # Handle a flat list if your implementation changes later
            chat_history_ids = torch.tensor([history_list], dtype=torch.long)


    # Get AI response and updated history
    bot_response, updated_chat_history_ids = generate_ai_response(user_message, chat_history_ids)
    
    # Save the updated history back to the session for the next request
    if updated_chat_history_ids is not None:
        # Convert tensor back to a standard Python list of lists for session storage
        session['chat_history'] = updated_chat_history_ids.tolist()
    
    # Integrate name extraction for a better greeting
    name = extract_name(user_message)
    if name and "hello" in bot_response.lower():
         bot_response = f"Hello, {name}! {bot_response.split('!', 1)[-1].strip()}"

    return jsonify({
        "intent": "AI_Response_Generated",
        "response": bot_response
    })
