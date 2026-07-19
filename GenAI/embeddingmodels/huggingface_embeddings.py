from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2")

texts = ["Hello This is Anushka Jagtap",
        "I am interested in AI and ML", 
        "I am learning about Generative AI"] 

vectors = embeddings.embed_documents(texts)

print(vectors)
