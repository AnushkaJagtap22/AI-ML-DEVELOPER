from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("/Users/Anushka/OneDrive/Documents/ANUSHKA/AIML_DEVELOPER/GenAI/RAG/DocumentLoader/dl-curriculum.pdf")

documents = loader.load()

print(type(documents))

print(len(documents))

print(documents[0])

print(documents[1].metadata)