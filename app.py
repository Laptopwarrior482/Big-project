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
from flask import Flask, render_template, request, jsonify
from transformers import pipeline

# Create the Flask application instance
app = Flask(__name__)

# --- 2. Model Loading (Load models once globally) ---

# Load the small English spaCy model. Ensure you have installed it via:
# python -m spacy download en_core_web_sm
try:
    nlp = spacy.load("en_core_web_sm")
except (OSError, ImportError):
    print("Downloading SpaCy model 'en_core_web_sm'. Please wait.")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

try:
    # This model classifies intents
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
except Exception as e:
    print(f"Error loading transformer model: {e}")
    classifier = None

# --- Helper Function ---

def extract_name(user_input: str) -> str | None:
    """
    Attempts to extract a person's name from a given string using SpaCy NER.
    Runs only if nlp model is loaded correctly.
    """
    if nlp:
        doc = nlp(user_input)
        for ent in doc.ents:
            if ent.label_ == "PERSON":
                return ent.text
    return None

# --- 3. Routes and Logic (The API endpoint) ---

# Define the default homepage route
@app.route('/')
def hello_world():
    # You need an 'index.html' file in a 'templates' folder for this to work
    return render_template('index.html')

# Define a new route for the chatbot API
@app.route('/api/chat', methods=['POST'])
def handle_chat_api():
    data = request.get_json()
    user_message = data.get("text", "")

    responses = {
        "order_status": "To check your order status, please provide your order ID.",
        "tech_support": "I can help with tech support. Please describe your issue in detail.",
        "check_balance": "You can check your balance in your account settings online.",
        "goodbye": "Goodbye! Have a great day.",
        "default": "I'm not sure how to respond to that intent."
    }
    
    bot_response = responses["default"]
    detected_intent = "none"

    if classifier and user_message:
        candidate_labels = list(responses.keys())
        candidate_labels.remove("default")

        result = classifier(user_message, candidate_labels)
        detected_intent = result['labels'][0]
        confidence_score = result['scores'][0]
        
        # New Logic: Integrate name extraction if the intent is a greeting
        if detected_intent == "greeting":
            name = extract_name(user_message)
            if name:
                bot_response = f"Hello, {name}! How can I assist you today?"
            else:
                bot_response = "Hello there! How can I assist you today?"
        else:
            bot_response = responses.get(detected_intent, responses["default"])
            
        bot_response += f" (Intent: {detected_intent}, Confidence: {confidence_score:.2f})"
        
    return jsonify({
        "intent": detected_intent,
        "response": bot_response
    })


# Note: The manual tests at the bottom were removed as generate_response was deleted.
# We will use the 'pytest' file for testing going forward.


