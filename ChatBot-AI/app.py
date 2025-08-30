from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

# Configure API key
API_KEY = "AIzaSyBAq3x14nHOG-kZVWrnctGrTEON3bTomwU"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Initialize the generative model
model = genai.GenerativeModel('gemini-1.5-pro')

# Initialize Flask app
app = Flask(__name__)

# Serve the frontend page
@app.route('/')
def home():
    return render_template("index.html")  # Ensure you have an 'index.html' in a 'templates' folder

# Chatbot API Endpoint
@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()  # Expecting a single message

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Generate response from the Gemini model
        response = model.generate_content(user_message)

        # Extracting the response properly
        if hasattr(response, 'text'):
            chatbot_reply = response.text
        elif hasattr(response, 'candidates') and response.candidates:
            chatbot_reply = response.candidates[0].content
        else:
            chatbot_reply = "Sorry, I couldn't generate a response."

        # Format response for better UI rendering
        formatted_reply = chatbot_reply.replace("**", "<b>").replace("*", "<li>").replace("\n", "<br>").replace("\t", "&nbsp;&nbsp;&nbsp;&nbsp;")
        formatted_reply = formatted_reply.replace("```python", "<pre><code>").replace("```", "</code></pre>")

        return jsonify({"reply": formatted_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)
