from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path='/Users/Anushka/OneDrive/Documents/ANUSHKA/AIML_DEVELOPER/GenAI/RAG/DocumentLoader/Social_Network_Ads.csv')

documents = loader.load()

print(type(documents))

print(len(documents))