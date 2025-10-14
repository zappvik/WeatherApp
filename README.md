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

## Technology Stack

-   **Backend:** Python, Flask, LangChain
-   **Frontend:** HTML, Tailwind CSS, vanilla JavaScript
-   **APIs:** Google Gemini API, [wttr.in](https://wttr.in) (for weather data)

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

### 1. Clone & Set Up the Backend

Navigate to the backend directory and set up the environment.

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/zappvik/WeatherApp
cd WeatherApp

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

-----

## How It Works: Tool Calling

This project is built around the concept of tool calling, where the LLM acts as a reasoning engine:

1.  A user asks, "What's the weather in Chennai?".
2.  The Flask server sends this query to the LangChain agent.
3.  The agent's LLM (Gemini) recognizes that it needs external data. It sees the `get_weather_data` tool that was provided to it.
4.  Instead of answering, the model returns a command: "Call the `get_weather_data` tool with the argument `city='Chennai'`".
5.  The LangChain Agent Executor runs the actual Python function, which calls the `wttr.in` API and gets back raw weather data.
6.  This data is sent back to the LLM with the instruction: "Here is the result from the tool, now formulate a final answer."
7.  Gemini uses this new information to generate a user-friendly response, like "The weather in Chennai is currently 30°C and partly cloudy."
