from flask import Flask, render_template, request, jsonify
#from openai import OpenAI # replaces for langchain 
from datetime import date
import os
import json
from dotenv import load_dotenv
from services.db import getDoctorAvailability, getAvailableSlots, bookAppointment, getDoctorsBySpecialty
#from services.tools import TOOLS  # replaces for langchain
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_tools_agent                                                                                                                                    
from langchain.memory import ConversationBufferMemory          
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder                                                                                                                             
from services.langchain_tools import check_specialty, check_slot, get_slots, book_appointment

app = Flask(__name__)
load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) 

@app.route("/")
def index():
    return render_template("index.html")

# --- LangChain Setup ---
llm = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))

langchain_tools = [check_specialty, check_slot, get_slots, book_appointment]

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a clinic receptionist for Super Clinic. Today's date is {today}.
Greet callers warmly and help them book appointments with doctors.
IMPORTANT RULES:
1. SYMPTOMS → SPECIALTY: When a caller describes symptoms, identify the required medical specialty and call check_specialty.
   - If no doctors of that specialty exist, apologize and ask if there is anything else you can help with.
   - If doctors exist, list all of them by name and ask which one the caller prefers.
2. DIRECT DOCTOR REQUEST: When a caller asks for a specific doctor by name, proceed to check availability.
3. CHECKING AVAILABILITY:
   - When the caller requests a specific date AND time, call check_slot to check that exact slot.
   - If the caller gives only a date (no time), call get_slots directly to get all free slots.
   - If NOT available, immediately call get_slots for that doctor and date. Do NOT ask the caller to suggest another time.
   - If the caller wants a doctor TODAY and no slots exist today, call get_slots for TOMORROW and suggest the earliest slot, clearly stating it is tomorrow.
   - If the caller switches to a different doctor, call get_slots for that doctor on the requested date.
4. PATIENT DETAILS: Before calling book_appointment, ensure you have the caller's name. If not provided, ask for it. Also ask for phone and email if not given.
5. BOOKING: Only call book_appointment once the caller confirms a slot and you have their name.
6. GOODBYE: When the caller says no or goodbye, thank them and wish them a good day."""),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

sessions = {}

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    session_id = request.json.get("session_id", "default")

    if session_id not in sessions:
        sessions[session_id] = ConversationBufferMemory(
            #memory_key="chat_history", return_messages=True
            memory_key="chat_history", return_messages=True, input_key="input"
        )

    memory = sessions[session_id]
    agent = create_openai_tools_agent(llm, langchain_tools, prompt)
    executor = AgentExecutor(agent=agent, tools=langchain_tools, memory=memory, verbose=True)

    result = executor.invoke({
        "input": user_message,
        "today": str(date.today())
    })
    return jsonify({"reply": result["output"]})

# --- Old OpenAI implementation for tool as implemented above for langchain ---
# @app.route("/chat", methods=["POST"])
# def chat():
#     user_message = request.json.get("message")
#     history = request.json.get("history", [])
#
#     system_prompt = {
#         "role": "system",
#         "content": f"""You are a clinic receptionist for Super Clinic. Today's date is {date.today()}.
#         ...
#         """
#     }
#     messages = [system_prompt] + history + [{"role": "user", "content": user_message}]
#     response = client.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=TOOLS)
#     choice = response.choices[0]
#     while choice.message.tool_calls:
#         ...
#     return jsonify({"reply": choice.message.content})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
