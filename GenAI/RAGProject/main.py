from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import TextLoader
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()

# Load document
loader = TextLoader("GenAI/RAGProject/notes.txt")
docs = loader.load()

# Prompt
template = ChatPromptTemplate.from_messages(
    [
        ("system", "You are an AI assistant that summarizes text in a clear and concise manner."),
        ("human", "Please summarize the following text:\n\n{data}")
    ]
)

# Initialize model
model = init_chat_model(
    "mistral-small-latest",
    temperature=0.3
)

# Format prompt
messages = template.format_messages(
    data=docs[0].page_content
)

# Invoke model
response = model.invoke(messages)

# Print summary
print("\n========== SUMMARY ==========\n")
print(response.content)