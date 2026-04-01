# Doctor Assistant Chatbot

An AI-powered clinic receptionist chatbot built with Flask and LangChain. It helps patients book appointments by understanding their symptoms, finding the right specialist, and scheduling a slot — all through a natural conversation.

## Features

- Symptom-to-specialty mapping (e.g. "chest pain" → Cardiologist)
- Doctor lookup by specialty or name
- Real-time slot availability checking
- Appointment booking with patient details
- Persistent conversation memory per session

## Tech Stack

- **Backend:** Python, Flask
- **AI:** LangChain + OpenAI GPT-4o-mini
- **Database:** SQLite
- **Frontend:** HTML, JavaScript

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/gaurmukesh/doctor-assistant.git
   cd doctor-assistant
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Initialize the database**
   ```bash
   python db_setup.py
   ```

6. **Run the app**
   ```bash
   python app.py
   ```

   Open `http://localhost:5000` in your browser.

## Project Structure

```
doctor_chatbot/
├── app.py                  # Flask app and LangChain agent setup
├── db_setup.py             # Database initialization
├── verify_db.py            # Database verification script
├── requirements.txt
├── services/
│   ├── db.py               # Database query functions
│   └── langchain_tools.py  # LangChain tool wrappers
├── static/
│   └── script.js           # Frontend chat logic
└── templates/
    └── index.html          # Chat UI
```
