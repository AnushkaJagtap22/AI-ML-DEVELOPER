from langchain_community.document_loaders import TextLoader

loader = TextLoader("/Users/Anushka/OneDrive/Documents/ANUSHKA/AIML_DEVELOPER/GenAI/RAG/DocumentLoader/cricket.txt" , encoding="utf-8")

documents = loader.load()

print(type(documents))

print(len(documents))

print(documents[0])