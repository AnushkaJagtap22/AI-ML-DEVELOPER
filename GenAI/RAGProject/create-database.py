# Load PDF
# Split into chunks
# Create embeddings using Mistral AI
# Store in ChromaDB

from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_community.vectorstores import Chroma

# Step 1: Load PDF
loader = PyPDFLoader("RAGProject/DocumentLoaders/deeplearning.pdf")
docs = loader.load()

# Step 2: Split into chunks
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_documents(docs)

# Step 3: Create Mistral Embedding Model
embedding_model = MistralAIEmbeddings(
    model="mistral-embed"
)

# Step 4: Store in ChromaDB
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="RAGProject/VectorDB/chroma_db"
)

print("✅ PDF successfully stored in ChromaDB using Mistral Embeddings.")