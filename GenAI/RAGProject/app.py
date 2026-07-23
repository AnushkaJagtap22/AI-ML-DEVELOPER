import os
import shutil
from dotenv import load_dotenv

import streamlit as st

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import (
    MistralAIEmbeddings,
    ChatMistralAI,
)
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

st.set_page_config(
    page_title="Book RAG Chatbot",
    page_icon="📚",
    layout="wide"
)

st.title("📚 Chat with Your Book")
st.write("Upload a PDF and ask questions about it.")

os.makedirs("uploads", exist_ok=True)
os.makedirs("vector_db", exist_ok=True)

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)

if uploaded_file:

    pdf_path = os.path.join(
        "uploads",
        uploaded_file.name
    )

    with open(pdf_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success("PDF Uploaded Successfully ✅")

    with st.spinner("Creating Vector Database..."):

        loader = PyPDFLoader(pdf_path)
        docs = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )

        chunks = splitter.split_documents(docs)

        embedding = MistralAIEmbeddings(
            model="mistral-embed"
        )

        vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=embedding,
            persist_directory="vector_db"
        )

        retriever = vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k":4,
                "fetch_k":10,
                "lambda_mult":0.5
            }
        )

    st.success("Vector Database Created 🎉")

    llm = ChatMistralAI(
        model="mistral-small-2506"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are a helpful AI assistant.

Use only the given context.

If the answer is not available,
say:
'I could not find the answer in the uploaded document.'
"""
            ),
            (
                "human",
                """
Context:
{context}

Question:
{question}
"""
            )
        ]
    )

    question = st.text_input(
        "Ask a Question"
    )

    if question:

        with st.spinner("Searching..."):

            docs = retriever.invoke(question)

            context = "\n\n".join(
                [d.page_content for d in docs]
            )

            final_prompt = prompt.invoke(
                {
                    "context":context,
                    "question":question
                }
            )

            response = llm.invoke(final_prompt)

        st.markdown("## 🤖 Answer")

        st.write(response.content)

        with st.expander("Retrieved Context"):

            for i, doc in enumerate(docs):

                st.markdown(f"### Chunk {i+1}")

                st.write(doc.page_content)