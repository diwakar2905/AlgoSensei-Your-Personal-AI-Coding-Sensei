import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import Field

# --- AI & LangChain Imports ---
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# --- 1. Load Environment Variables ---
# This line now specifically looks for your "python.env" file.
load_dotenv(dotenv_path='python.env')

# --- Initialize your FastAPI app ---
app = FastAPI()

# --- Add CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Define Data Models ---
class CodeInput(BaseModel):
    problem: str
    code: str
    language: str


class AIResponse(BaseModel):
    model_config = {"populate_by_name": True}
    sender: str = Field(..., alias="from") # Use an alias to send "from" in JSON
    text: str

class ChatMessage(BaseModel): # New model to match Google's API structure
    role: str
    parts: list[dict]

class ChatInput(BaseModel):
    history: list[ChatMessage]
    problem: str
    code: str
    language: str

# --- The "Socratic" System Prompts ---
socratic_start_prompt = """
You are "AlgoSensei," an expert Socratic tutor for programming.
Your user is a student trying to solve a coding problem.

Your one and only goal is to **guide the user to the optimal solution by asking probing questions.**
You must **NEVER, EVER give the direct answer** or a full block of optimized code.

Here is the user's context:
- Language: {language}
- Problem: {problem}
- User's (possibly incorrect) Solution: {code}

Your task is to analyze their solution and start the Socratic dialogue.

1.  **Analyze:** Find the *single biggest bottleneck* or *most important error* in their solution (e.g., time complexity, wrong data structure, a logic error).
2.  **Formulate Question:** Ask **one single, clear question** that guides them to *think* about that bottleneck.
    -   **Good Question:** "I see you used a `nested loop`. What do you think the time complexity, `O(n^?)`, of this approach is?"
    -   **Bad (DO NOT DO):** "Your solution is O(n^2). You should use a hash map."

Start the conversation. Respond **only** with your first Socratic question.
"""

socratic_continue_prompt = """
You are "AlgoSensei," an expert Socratic tutor for programming.
Your user is trying to solve a coding problem.
Continue the conversation based on the history provided. Your goal is to guide them with questions.
NEVER give the final answer or a full block of optimized code. Ask the next logical question.

Here is the original context:
- Problem: {problem}
- User's Initial Code: {code}

--- CONVERSATION HISTORY ---
{history}
--- END HISTORY ---

Based on the last message from the user, what is your next guiding question?
"""

# --- 2. Initialize AI Model ---
# Because you loaded the .env file, this line will automatically find
# and use your GOOGLE_API_KEY.
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY not found. Make sure it's set in your python.env file.")

llm = ChatGoogleGenerativeAI(model="gemini-pro-latest", google_api_key=google_api_key, temperature=0.7)

# --- Create LangChain "Chains" ---
start_prompt_template = ChatPromptTemplate.from_template(socratic_start_prompt)
continue_prompt_template = ChatPromptTemplate.from_template(socratic_continue_prompt)
output_parser = StrOutputParser()

start_chain = start_prompt_template | llm | output_parser
continue_chain = continue_prompt_template | llm | output_parser

# --- API Endpoints ---
@app.post("/api/start_session", response_model=AIResponse)
async def start_session(user_input: CodeInput):
    ai_message = start_chain.invoke({
        "language": user_input.language,
        "problem": user_input.problem,
        "code": user_input.code
    })
    
    # Return the AI's first message
    return AIResponse(sender="ai", text=ai_message)

@app.post("/api/chat", response_model=AIResponse)
async def chat_session(chat_input: ChatInput):
    # Format the history for the prompt
    formatted_history = "\n".join([f"{msg.role}: {msg.parts[0]['text']}" for msg in chat_input.history])
    
    ai_message = continue_chain.invoke({
        "problem": chat_input.problem,
        "code": chat_input.code,
        "language": chat_input.language,
        "history": formatted_history,
    })
    
    return AIResponse(sender="ai", text=ai_message)

@app.get("/")
def read_root():
    return {"message": "AlgoSensei Backend is running!"}
