
from langchain_mistralai import ChatMistralAI
from dotenv import load_dotenv
import streamlit as st
from langchain_core.prompts import load_prompt

load_dotenv()

model = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0.3
)

st.header("Research Tool")

paper_input = st.selectbox(
    "Select Research Paper Name",
    [
        "Attention Is All You Need",
        "BERT: Pre-training of Deep Bidirectional Transformers",
        "GPT-3: Language Models are Few-Shot Learners",
        "Diffusion Models Beat GANs on Image Synthesis"
    ]
)

style_input = st.selectbox(
    "Select Explanation Style",
    [
        "Beginner-Friendly",
        "Technical",
        "Code-Oriented",
        "Mathematical"
    ]
)

length_input = st.selectbox(
    "Select Explanation Length",
    [
        "Short (1-2 paragraphs)",
        "Medium (3-5 paragraphs)",
        "Long (detailed explanation)"
    ]
)

template = load_prompt("template.json")

if st.button("Summarize"):
    with st.spinner("Summarizing research paper..."):
        try:
            chain = template | model

            result = chain.invoke({
                "paper_input": paper_input,
                "style_input": style_input,
                "length_input": length_input
            })

            st.subheader("Research Paper Summary")
            st.write(result.content)

        except Exception as e:
            st.error(f"An error occurred: {e}")
