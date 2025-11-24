Advanced Python AI Chatbot:

This project is an Advanced Python AI Chatbot, implemented as a Flask web application that leverages sophisticated Natural Language Processing (NLP) models to facilitate engaging and context-aware conversations.The core of the application is a Flask API that manages conversation state using session cookies. It integrates specialized libraries for enhanced functionality:

*transformers (DialoGPT): Generates human-like, contextually relevant conversational responses.

*spaCy: Used for named entity recognition (NER), specifically to extract and manage user information like names.

*Intent Handling: The application combines generative AI with rule-based logic to handle specific, predefined user queries accurately and consistently.


Installation:
To set up the environment, it is highly recommended to use a Python virtual environment.
1.Create and Activate a Virtual Environment:

"python -m venv my_ai_env"
# On Windows:
".\my_ai_env\Scripts\activate"
# On macOS/Linux:
"source my_ai_env/bin/activate"
2.Install Dependencies: Install the required libraries listed in your requirements.txt file (or install them directly):

"pip install numpy torch transformers flask pytest black flake8 spacy"
# After installing spacy, download the necessary model data:
"python -m spacy download en_core_web_sm"


Usage:
The chatbot runs as a local Flask web server.
1.Run the Flask App: Ensure you are in your activated virtual environment and execute the following command:

"flask --app app run"

2.Access the Interface: Open your web browser and navigate to the provided local address, typically http://127.0.0.1:5000, to interact with the chatbot interface (index.html).


Testing:
Testing ensures code integrity, functionality, and consistent adherence to standards.
Run Unit/Integration Tests: The project uses pytest for testing the API endpoints and helper functions. Run this command in a new, separate terminal (while the Flask app is running in the first one):

"pytest"

1.Green output indicates all tests passed successfully; Red output indicates a failure in one or more test cases.
2.Run a Conversation Test Script: The provided test_chatbot_api.py script simulates a multi-turn conversation via HTTP requests to verify session management and memory capabilities.

"python test_chatbot_api.py"


Code Standards:
The project maintains high code quality using automatic tools:
Black: An uncompromising code formatter used to ensure consistent, clean Python syntax across the project.
Flake8: A static analysis tool used as a linter, enforcing style guides and highlighting potential errors or standards boundaries crossed within the codebase.
