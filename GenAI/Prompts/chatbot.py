
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

import os

load_dotenv()

message = [
    SystemMessage(content= "Hello ! You are a funny and witty chatbot. You are a helpful assistant that can answer questions, provide information, and engage in casual conversation. Your responses should be concise, informative, and friendly. If you don't know the answer to a question, respond with 'I'm not sure about that.'"),
]

model = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.3,
    max_retries=2
)

print("\n===== GROQ AI CHATBOT =====")
print("Type 'exit' or 'quit' to stop.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        print("Exiting the chatbot. Goodbye!")
        break

    message.append(HumanMessage(content=user_input))

    try:
        response = model.invoke(message)
        message.append(AIMessage(content=response.content))
        print(f"GROQ AI: {response.content}\n")
    except Exception as e:
        print(f"Error: {e}\n")

