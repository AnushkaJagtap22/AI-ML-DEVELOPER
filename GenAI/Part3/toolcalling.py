from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.tools import tool

# -----------------------------
# Create Tool
# -----------------------------
@tool
def calculator(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

# -----------------------------
# Load Mistral Model
# -----------------------------
llm = ChatMistralAI(
    model="mistral-small-2506"
)

# -----------------------------
# Bind Tool
# -----------------------------
llm_with_tools = llm.bind_tools([calculator])

# -----------------------------
# Ask Question
# -----------------------------
query = "What is 25 + 75?"

response = llm_with_tools.invoke(query)

print(response)