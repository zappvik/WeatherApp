# Gemini Weather Assistant

Gemini Weather Assistant is a simple web application that uses Google's Gemini API to provide conversational weather forecasts. This project was created as a learning exercise to understand key concepts in building modern AI applications, specifically **LLM tool calling** (also known as function calling), which is a core feature in advanced AI frameworks like LangChain.

The user can ask natural language questions, and the AI-powered backend will fetch the weather data and formulate a human-friendly response.

---

## Features

-   **Natural Language Queries:** Ask for the weather in plain English (e.g., "what's it like in London right now?").
-   **AI-Powered Responses:** Utilizes the **Gemini model** to understand the query, use a weather tool, and generate a conversational answer.
-   **Clean, Modern UI:** A simple and responsive user interface built with Tailwind CSS.
-   **Separated Frontend & Backend:** Structured with a distinct Flask backend and a static HTML/JS frontend, a common pattern for web applications.

---

## Project Structure

```

.
├── backend/
│   ├── app.py            \# The Flask server and Gemini logic
│   └── requirements.txt  \# Python dependencies
├── frontend/
│   └── index.html        \# The HTML, CSS, and JavaScript for the UI
├── .gitignore            \# Specifies files for Git to ignore
└── README.md             \# This file

````

---

## How to Run

### Prerequisites

-   Python 3.7+
-   A Google Gemini API Key

### 1. Set Up the Backend

Navigate to the backend directory and set up the environment.

```bash
# Move into the backend folder
cd backend

# Create and activate a virtual environment (recommended)
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install the required Python packages
pip install -r requirements.txt

# Set your Gemini API key
# On Windows (PowerShell):
$env:GOOGLE_API_KEY="YOUR_API_KEY_HERE"
# On macOS/Linux:
export GOOGLE_API_KEY="YOUR_API_KEY_HERE"

# Run the Flask server
python app.py
````

The backend server will start on `http://127.0.0.1:5000`. **Leave this terminal running.**

### 2\. Launch the Frontend

Once the backend server is running, you must access the application through it.

**Important:** Do **NOT** open the `frontend/index.html` file directly in your browser, as this will cause an error.

  - Open your web browser and navigate to the following address:

    [**http://127.0.0.1:5000**](http://127.0.0.1:5000)

You can now interact with the application.