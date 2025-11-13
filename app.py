#"help()" tool gives info on function when placed in ()
#"".\my_ai_env\Scripts\activate" paste at start of every new terminal for virtual environment(malan did this)


#Make a function that classifies intent of users text(Basic so no documentation)
#The 'def' keyword defines the function
#basic version should have 20-50 lines of python code and 30-55 lines using all of HTML,CSS,JavaScript)
#create a random variable to set equal to desired input,then "print(variable)" for it to work


def user_intent(info):
    message = f"Write: {info}!"
    print(message)
    # The 'return' keyword provides an output
    return message
user_intent("My text input")










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
