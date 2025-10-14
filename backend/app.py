import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool

app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

if "GOOGLE_API_KEY" not in os.environ:
    print("FATAL ERROR: GOOGLE_API_KEY environment variable not set.")
    exit()

# --- TOOL DEFINITION ---
# We use the @tool decorator to make our function compatible with LangChain.
@tool
def get_weather_data(city: str) -> str:
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

# --- LANGCHAIN AGENT SETUP ---
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

tools = [get_weather_data]

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful weather assistant."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

agent = create_tool_calling_agent(llm, tools, prompt)

# Create the Agent Executor, which runs the agent's reasoning loop.
# verbose=True lets us see the agent's thoughts in the terminal.
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


@app.route('/weather', methods=['GET'])
def get_weather_response():
    user_query = request.args.get('query') or request.args.get('city')
    if not user_query:
        return jsonify({"error": "Query or city parameter is required"}), 400
    try:
        response = agent_executor.invoke({"input": user_query})
        
        final_response = response.get('output', "I could not process that request.")
        return jsonify({"response": final_response})
        
    except Exception as e:
        return jsonify({"error": f"An error occurred with the LangChain agent: {e}"}), 500

@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)