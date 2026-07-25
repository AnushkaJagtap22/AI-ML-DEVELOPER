import os
import streamlit as st
from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

# Load environment variables if available locally
load_dotenv()

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Script Localizer Pipeline",
    page_icon="🎬",
    layout="wide"
)

# --- State Definition ---
class PipelineState(TypedDict):
    raw_input: str 
    edited_text: str
    script_text: str
    final_output: str

# --- Sidebar Configuration ---
st.sidebar.title("⚙️ Configuration")

# Allow API Key entry via sidebar or load from environment
groq_api_key = st.sidebar.text_input(
    "Groq API Key", 
    value=os.getenv("GROQ_API_KEY", ""), 
    type="password",
    help="Enter your Groq API key here or keep it in a .env file."
)

model_name = st.sidebar.selectbox(
    "Select Model",
    ["llama-3.3-70b-versatile", "llama3-8b-8192", "mixtral-8x7b-32768"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Pipeline Stages:**\n1. Copyeditor (Grammar & Flow)\n2. ScriptWriter (YouTube Hook)\n3. Translator (Hinglish Localizer)")

# --- LangGraph Setup Function ---
def build_pipeline(api_key: str, model: str):
    llm = ChatGroq(model=model, temperature=0.7, groq_api_key=api_key)

    def editor_node(state: PipelineState) -> dict:
        prompt = (
            "You are an expert copyeditor. Clean up the following raw text. "
            "Fix any grammatical errors, spelling mistakes and smooth out the transition flow "
            "while keeping the core message intact. Return only the edited text.\n\n" 
            f"Text:\n{state['raw_input']}"
        )
        response = llm.invoke(prompt)
        return {"edited_text": response.content.strip()}

    def scriptwriter_node(state: PipelineState) -> dict:
        prompt = (
            "You are a charismatic YouTube content creator. Take this edited text and transform it "
            "into a highly engaging, punchy, conversational video script hook. Make it sound like "
            "a real person speaking passionately. Return only the script content.\n\n"
            f"Edited Text:\n{state['edited_text']}"
        )
        response = llm.invoke(prompt)
        return {"script_text": response.content.strip()}

    def translate_node(state: PipelineState) -> dict:
        prompt = (
            "You are an expert content localizer for the Indian market. Take the following script "
            "and convert it into natural, flowing 'Hinglish'. Do not simply translate it sentence by sentence "
            "or repeat information. Alternating comfortably between Hindi and English just like an intellectual tech "
            "educator would speak naturally on a live stream. Keep the energy high. "
            "Return only the final Hinglish text.\n\n"
            f"Script:\n{state['script_text']}"
        )
        response = llm.invoke(prompt)
        return {"final_output": response.content.strip()}

    # Graph construction
    graph = StateGraph(PipelineState)
    graph.add_node("Editor", editor_node)
    graph.add_node("ScriptWriter", scriptwriter_node)
    graph.add_node("Translator", translate_node)

    graph.add_edge(START, "Editor")
    graph.add_edge("Editor", "ScriptWriter")
    graph.add_edge("ScriptWriter", "Translator")
    graph.add_edge("Translator", END)

    return graph.compile()

# --- Main App Interface ---
st.title("🎬 AI Video Script Pipeline")
st.caption("Transform rough thoughts into punchy, stream-ready Hinglish scripts using LangGraph & Groq.")

# Default example text
default_text = "AI agents are the future of tech. They can think, plan, and act on their own. LangGraph helps you build these agents with proper control and memory."

raw_input = st.text_area(
    "Enter your raw text or idea:", 
    value=default_text, 
    height=140,
    placeholder="Type or paste your raw text here..."
)

col1, col2 = st.columns([1, 4])
with col1:
    run_button = st.button("🚀 Generate Script", type="primary", use_container_width=True)

# --- Execution Handling ---
if run_button:
    if not groq_api_key:
        st.error(" Please enter your Groq API Key in the sidebar or provide it via a `.env` file.")
    elif not raw_input.strip():
        st.warning(" Please enter some raw text before running the pipeline.")
    else:
        try:
            # Build and execute app
            app = build_pipeline(groq_api_key, model_name)
            
            # Status tracking UI
            with st.status("Processing Pipeline...", expanded=True) as status:
                st.write("🔄 **Stage 1:** Editing and refining text...")
                # Run the pipeline
                result = app.invoke({"raw_input": raw_input})
                st.write("✨ **Stage 2:** Formatting script hook...")
                st.write("🌐 **Stage 3:** Localizing to natural Hinglish...")
                status.update(label=" Pipeline Complete!", state="complete", expanded=False)

            st.markdown("---")
            st.subheader("🔥 Final Hinglish Script")
            st.success(result["final_output"])

            # --- Intermediate Results View ---
            st.markdown("---")
            st.subheader("🔍 Stage-by-Stage Breakdown")
            
            tab1, tab2, tab3 = st.tabs(["1. Cleaned Text", "2. Youtube Hook", "3. Final Hinglish"])
            
            with tab1:
                st.info("Grammar cleanup and refined tone:")
                st.write(result.get("edited_text", ""))
                
            with tab2:
                st.info("Conversational script structure:")
                st.write(result.get("script_text", ""))

            with tab3:
                st.info("Localized natural Hinglish presentation:")
                st.write(result.get("final_output", ""))

        except Exception as e:
            st.error(f"An error occurred during pipeline execution: {str(e)}")