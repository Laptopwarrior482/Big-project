#"help()" tool gives info on function when placed in ()
#"".\my_ai_env\Scripts\activate" paste at start of every new terminal for virtual environment(malan did this)
#Make a function that classifies intent of users text(Basic so no documentation)
#The 'def' keyword defines the function
#basic version should have 20-50 lines of python code and 30-55 lines using all of HTML,CSS,JavaScript)
#create a random variable to set equal to desired input,then "print(variable)" for it to work





from flask import Flask, render_template, request, jsonify
from transformers import pipeline # <-- ADD THIS IMPORT

# Create the Flask application instance
app = Flask(__name__)

# --- LOAD THE TRANSFORMER MODEL ONCE WHEN THE APP STARTS ---
# This loads a "zero-shot" classification model that can classify text
# based on labels you provide on the fly.
try:
    classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
except Exception as e:
    print(f"Error loading transformer model: {e}")
    classifier = None

# Define the default homepage route
@app.route('/')
def hello_world():
    return render_template('index.html')

# Define a new route for the chatbot API
@app.route('/api/chat', methods=['POST'])
def classify_user_text():
    data = request.get_json()
    user_message = data.get("text", "")

    if classifier and user_message:
        # Define potential intents (you customize these)
        candidate_labels = ["greeting", "order_status", "tech_support", "check_balance", "goodbye"]

        # Run the classification
        result = classifier(user_message, candidate_labels)
        detected_intent = result['labels'][0]
        confidence_score = result['scores'][0]

        bot_response = f"Detected intent: **{detected_intent}** with {confidence_score:.2f} confidence."
    else:
        bot_response = "Model not loaded or no message received."
        detected_intent = "none"

    return jsonify({
        "intent": detected_intent,
        "response": bot_response
    })


# Optional: Run the app directly if this script is executed
if __name__ == '__main__':
    app.run(debug=True)






#Dont touch this code unless asking gemini!!!
from flask import Flask, render_template # <-- ADD render_template here

# Create the Flask application instance
app = Flask(__name__)

# Define the default homepage route
@app.route('/')
def hello_world():
    # return 'Hello World! The AI Chatbot is starting up.' <-- DELETE THIS LINE
    return render_template('index.html') # <-- ADD THIS LINE INSTEAD

# Optional: Run the app directly if this script is executed
if __name__ == '__main__':
    app.run(debug=True)
