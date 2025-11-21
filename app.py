#"".\my_ai_env\Scripts\activate" paste at start of every new terminal for virtual environment(malan did this)
#Document hashtag with "personal:" on top of code section whcih explains purpose so your not confused
#Make sure code # titles are correct
#Main code here and tests in next file
#Run this to test code"python test_chatbot_api.py"
#Always ask extra questions b/c to master something you need 10x knowledge
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





#personal:"hello(name)"goal 
import spacy

# Load the small English model. Ensure you have installed it via:
# python -m spacy download en_core_web_sm
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print("Downloading SpaCy model 'en_core_web_sm'. Please wait.")
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

def extract_name(user_input: str) -> str | None:
    """
    Attempts to extract a person's name from a given string using SpaCy NER.
    """
    doc = nlp(user_input)
    # Iterate over the entities recognized by SpaCy
    for ent in doc.ents:
        # 'PERSON' label indicates a name
        if ent.label_ == "PERSON":
            return ent.text
    return None

# Example usage:
# name = extract_name("Hello, my name is John Doe.")
# print(name) # Output: John Doe

#personal:a classify function that belongs below here
def generate_response(user_input: str) -> str:
    """
    Generates a greeting response using intent and name extraction.
    """
    classify_user_text
    if intent == "greeting":
        name = extract_name(user_input)
        if name:
            return f"Hello, {name}!"
        else:
            return "Hello there!"
    else:
        return "I am not sure how to respond to that."








#personal:chatbot done
# --- 1. Imports ---
from flask import Flask, render_template, request, jsonify
from transformers import pipeline
import spacy # Import spacy

# Create the Flask application instance
app = Flask(__name__)

# --- 2. Model Loading (Load models once globally) ---
try:
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
except Exception as e:
    print(f"Error loading transformer model: {e}")
    classifier = None

try:
    # Load the English spaCy model
    nlp_spacy = spacy.load("en_core_web_sm")
except Exception as e:
    print(f"Error loading spaCy model: {e}")
    nlp_spacy = None

# --- 3. Routes and Logic (The API endpoint) ---

# Define the default homepage route
@app.route('/')
def hello_world():
    return render_template('index.html')

# Define a new route for the chatbot API
@app.route('/api/chat', methods=['POST'])
def classify_user_text():
    data = request.get_json()
    user_message = data.get("text", "")

    # Add the responses dictionary here
    responses = {
        "greeting": "Hello there! How can I assist you today?",
        "order_status": "To check your order status, please provide your order ID.",
        "tech_support": "I can help with tech support. Please describe your issue in detail.",
        "check_balance": "You can check your balance in your account settings online.",
        "goodbye": "Goodbye! Have a great day.",
        "default": "I'm not sure how to respond to that intent."
    }

    # --- Integrate SpaCy processing here, before classification ---
    if nlp_spacy and user_message:
        doc = nlp_spacy(user_message)
        # The lemmatized words are now accessible via 'token.lemma_' if you need them
        print([token.lemma_ for token in doc]) # Example of accessing the base forms
    # --- End SpaCy integration ---
    

    if classifier and user_message:
        # Define potential intents based on the dictionary keys
        candidate_labels = list(responses.keys())
        candidate_labels.remove("default") # Don't classify as 'default'

        # Run the classification
        result = classifier(user_message, candidate_labels)
        detected_intent = result['labels'][0] # Use [0] to get the top result
        confidence_score = result['scores'][0]

        # Get the specific response based on the detected intent
        bot_response = responses.get(detected_intent, responses["default"])
        bot_response += f" (Intent: {detected_intent}, Confidence: {confidence_score:.2f})"

    else:
        # Handles cases where the model failed to load or no message was sent
        bot_response = responses["default"]
        detected_intent = "none"

    return jsonify({
        "intent": detected_intent,
        "response": bot_response
    })



#personal:tests the clarification logic and should stay at bottom
if __name__ == "__main__":
    test_input_1 = "Hi, my name is Alex"
    response_1 = generate_response(test_input_1)
    print(f"Input: '{test_input_1}' -> Response: '{response_1}'")

    test_input_2 = "How are you doing today?"
    response_2 = generate_response(test_input_2)
    print(f"Input: '{test_input_2}' -> Response: '{response_2}'")

