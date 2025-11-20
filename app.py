#"help()" tool gives info on function when placed in ()
#"".\my_ai_env\Scripts\activate" paste at start of every new terminal for virtual environment(malan did this)
#Document hashtag with "personal:" on top of code section whcih explains purpose so your not confused
#After a while make sure code is sectioned off correctly
#All main code goes here and all tests go in next file
#Run "pytest" to see if code is fine and only in test file
#Gemini doesnt trash memory if chat restarts

#NLP Logic/Model Code (PyTorch/ Transformers/SpaCy): ~300-600 line
#1.Goal=make robot say "hello (name)"
#2.Use spacy aka try
#3.Simple logic,like if sentence says "hello" in it then classify intent as greeting
#4.Transformers for model and pytorch to define input then run through model
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

# --- 4. Execution Block ---
if __name__ == '__main__':
    app.run(debug=True)

