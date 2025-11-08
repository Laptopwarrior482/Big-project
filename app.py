#"help()" tool gives info on function when placed in ()
#"".\my_ai_env\Scripts\activate" paste at start of every new terminal for virtual environment(malan did this)
#Leave the flask code below as is


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



