import os
import requests
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# --- LangChain Imports ---
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.tools import tool

# --- SETUP ---
app = Flask(__name__, static_folder='../frontend', static_url_path='')
CORS(app)

# Ensure the GOOGLE_API_KEY is set. LangChain's library will use it automatically.
if "GOOGLE_API_KEY" not in os.environ:
    print("FATAL ERROR: GOOGLE_API_KEY environment variable not set.")
    exit()

# --- TOOL DEFINITION (LangChain Style) ---
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
        # Return the raw text; the LLM is smart enough to parse it.
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching weather data: {e}"

# --- LANGCHAIN AGENT SETUP ---
# 1. Initialize the LLM using the LangChain integration.
# As requested, using the latest flash model.
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# 2. Define the list of tools the agent can use.
tools = [get_weather_data]

# 3. Create the Prompt Template for the agent.
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful weather assistant."),
    ("user", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

# 4. Create the Agent itself by combining the LLM, tools, and prompt.
agent = create_tool_calling_agent(llm, tools, prompt)

# 5. Create the Agent Executor, which runs the agent's reasoning loop.
# verbose=True lets us see the agent's thoughts in the terminal.
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# --- API ENDPOINT ---
@app.route('/weather', methods=['GET'])
def get_weather_response():
    user_query = request.args.get('query') or request.args.get('city')
    if not user_query:
        return jsonify({"error": "Query or city parameter is required"}), 400
    try:
        # We invoke the agent executor, which handles the entire flow.
        response = agent_executor.invoke({"input": user_query})
        
        # The agent's final answer is in the 'output' key.
        final_response = response.get('output', "I could not process that request.")
        return jsonify({"response": final_response})
        
    except Exception as e:
        return jsonify({"error": f"An error occurred with the LangChain agent: {e}"}), 500

# --- SERVE FRONTEND ---
@app.route('/')
def serve_index():
    return send_from_directory('../frontend', 'index.html')

# --- RUN THE APP ---
if __name__ == '__main__':
    app.run(debug=True, port=5000)