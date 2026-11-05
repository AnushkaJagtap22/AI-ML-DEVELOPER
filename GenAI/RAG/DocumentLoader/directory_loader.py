from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader

loader = DirectoryLoader(
    path='/Users/Anushka/OneDrive/Documents/ANUSHKA/AIML_DEVELOPER/GenAI/RAG/DocumentLoader/books',
    glob='*.pdf',
    loader_cls=PyPDFLoader
)

docs = loader.lazy_load()

for document in docs:
    print(document.metadata)