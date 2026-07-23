from langchain_community.document_loaders import WebBaseLoader

url = "https://www.apple.com/in/iphone-17-pro/"

data = WebBaseLoader(url).load()

print(data)