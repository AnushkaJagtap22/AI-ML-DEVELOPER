from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

from langchain.chat_models import init_chat_model

model = init_chat_model('mistral-small-latest', temperature=0.9,max_tokens=20)  # Initialize the chat model

response = model.invoke('Write a poem on AI')  # Invoke the model with a prompt   
print(response.content)  # Print the response from the model