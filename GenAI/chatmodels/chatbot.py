from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

model = init_chat_model(
    "mistral-small-latest",
    temperature=0.9
)

print("------------WELCOME TO BASIC CHAT BOT---------------")
print("----------------PRESS 0 TO EXIT--------------------")

print("You are now connected to the AI chatbot.")
print("Choose Your AI Mood:")
print("1. Funny")
print("2. Angry")
print("3. Neutral")
choice = input("Enter your choice (1, 2, or 3): ")
if choice == "1":
    messages = [
        SystemMessage(content="You are a very funny AI agent."),
    ]
elif choice == "2":
    messages = [
        SystemMessage(content="You are a very angry AI agent."),
    ]
elif choice == "3":
    messages = [
        SystemMessage(content="You are a very neutral AI agent."),
    ]
else:
    print("Invalid choice. Defaulting to neutral mood.")
    messages = [
        SystemMessage(content="You are a very neutral AI agent."),
    ]


while True:
    prompt = input("You: ")

    messages.append(HumanMessage(content=prompt))
    if prompt == "0":
            break

    response = model.invoke(messages)

    print("Bot:", response.content)

    messages.append(AIMessage(content=response.content))