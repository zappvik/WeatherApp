import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai

# --- SETUP ---
# The static_folder path is now relative to this file's location (backend/).
# It needs to go one level up ('..') and then into the 'frontend' folder.
app = Flask(__name__, static_folder='../frontend', static_url_path='') # <-- THIS LINE IS CHANGED
CORS(app)

try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("FATAL ERROR: GOOGLE_API_KEY environment variable not set.")
    exit()

# --- TOOL DEFINITION ---
def get_weather_data(city: str):
    """Gets the current weather for a specified city using the wttr.in API."""
    if not isinstance(city, str):
        return "Error: City must be a string."
    weather_url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(weather_url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"

# --- GEMINI MODEL INITIALIZATION ---
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash', # Using your preferred model
    tools=[get_weather_data]
)

# --- API ENDPOINT ---
@app.route('/weather', methods=['GET'])
def get_weather_response():
    user_query = request.args.get('query') or request.args.get('city')
    if not user_query:
        return jsonify({"error": "Query or city parameter is required"}), 400
    try:
        chat = model.start_chat(enable_automatic_function_calling=True)
        response = chat.send_message(user_query)
        final_response = response.text
        return jsonify({"response": final_response})
    except Exception as e:
        return jsonify({"error": f"An error occurred with the Gemini API: {e}"}), 500

# --- SERVE FRONTEND ---
@app.route('/')
def serve_index():
    # We now tell send_from_directory to look in the correct relative path.
    return send_from_directory('../frontend', 'index.html') # <-- THIS LINE IS CHANGED

# --- RUN THE APP ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)