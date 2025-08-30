# 🚀 **Flask Chatbot using Google Gemini API** 

This is a **Flask-based chatbot** that integrates with **Google Gemini API** (Generative AI) to generate responses based on user input. The chatbot is deployed on **Render**.  

---

## 🌟 Features  
✅ Chatbot powered by **Google Gemini API**  
✅ Uses **Flask** as a backend framework  
✅ **Deployed on Render**  
✅ API endpoint to communicate with the chatbot  

---

## 📂 Project Structure  

```
📁 flask-chatbot
│── 📂 templates          # HTML frontend
│   ├── index.html        # Main frontend file
│── app.py                # Main Flask application
│── requirements.txt      # Python dependencies
│── Procfile              # Deployment configuration (if needed)
│── README.md             # Documentation
```

---

## 🛠️ Installation & Setup

**1️⃣ Clone the Repository**

```
git clone https://github.com/yourusername/flask-chatbot.git
cd flask-chatbot
```

**2️⃣ Create a Virtual Environment (Optional but Recommended)**

```
python -m venv venv
source venv/bin/activate  # On Mac/Linux
venv\Scripts\activate     # On Windows
```

**3️⃣ Install Dependencies**

`pip install -r requirements.txt`

**4️⃣ Set Up Google Gemini API Key**

Replace **YOUR_GEMINI_API_KEY** in **app.py** with your actual API key.

**▶️ Running the App Locally**

`python app.py`

Then open **http://127.0.0.1:5000/** in your browser.

---

## 🚀 Deployment on Render

**1️⃣ Install gunicorn**

`pip install gunicorn`

**2️⃣ Update requirements.txt**

`pip freeze > requirements.txt`

**3️⃣ Deploying on Render**

- Push your project to GitHub.
- Go to Render → Create a new Web Service.
- Connect your GitHub repository.
- Set Start Command as: gunicorn app:app
- Click Deploy.

After deployment, your chatbot will be live at the provided URL.

---

## 🌐 Live Deployment

- **Chatbot AI** - [Live URL](https://chatbot-ai-j7mg.onrender.com)

---

## 🛠️ API Endpoint

```
POST /chat

Request

{
  "message": "Hello, how are you?"
}

Response

{
  "reply": "I'm good! How can I assist you today?"
}
```
---

## 🤝 Contributing

Pull requests are welcome. Please open an issue first to discuss any major changes.

---

## 📜 License

This project is open-source and free to use under the MIT License.
