document.addEventListener('DOMContentLoaded', () => {
    const chatbox = document.getElementById('chatbox');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function sendMessage() {
        const userMessage = userInput.value.trim();
        if (userMessage === '') return;

        // Display user message in the chatbox
        appendMessage(userMessage, 'user-message');
        userInput.value = ''; // Clear input field

        // Show a "typing..." indicator
        const typingIndicator = appendMessage("Bot is typing...", 'bot-message typing');
        
        // Send message to Flask API
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: userMessage })
        })
        .then(response => response.json())
        .then(data => {
            // Remove typing indicator
            chatbox.removeChild(typingIndicator); 
            // Display bot response
            appendMessage(data.response, 'bot-message');
        })
        .catch(error => {
            console.error('Error:', error);
            chatbox.removeChild(typingIndicator);
            appendMessage("Error: Could not reach the server.", 'bot-message error');
        });
    }

    function appendMessage(message, className) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', className);
        messageDiv.textContent = message;
        chatbox.appendChild(messageDiv);
        // Scroll to the bottom of the chatbox
        chatbox.scrollTop = chatbox.scrollHeight;
        return messageDiv; // Return the element for the typing indicator removal
    }
});
