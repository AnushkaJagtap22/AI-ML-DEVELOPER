from langchain_openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

llm = OpenAI(model_name="gpt-4", temperature=0.9)

result = llm.invoke("Write a poem about the beauty of nature.")

print(result)
