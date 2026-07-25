import os
from typing import TypedDict, Annotated
import streamlit as st
from dotenv import load_dotenv

# LangChain & LangGraph imports
from langgraph.graph.message import add_messages 
from langgraph.graph import StateGraph, START, END 
from langchain_groq import ChatGroq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- Page Configuration ---
st.set_page_config(
    page_title="Campus Assistant",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Apple-Inspired Glassmorphic Styling ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "SF Pro Display", sans-serif !important;
        background-color: #050507 !important;
        color: #F5F5F7 !important;
    }

    .stApp {
        background-color: #050507 !important;
    }

    /* Top Nav Bar */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 28px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 999px;
        margin-bottom: 24px;
    }

    .nav-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .badge-active { background: rgba(48, 209, 88, 0.12); color: #30D158; border: 1px solid rgba(48, 209, 88, 0.25); }
    .badge-inactive { background: rgba(255, 69, 58, 0.12); color: #FF453A; border: 1px solid rgba(255, 69, 58, 0.25); }

    /* Routing Tag Badges */
    .route-pill {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .pill-academic { background: rgba(10, 132, 255, 0.15); color: #64D2FF; border: 1px solid rgba(10, 132, 255, 0.3); }
    .pill-fee { background: rgba(255, 159, 10, 0.15); color: #FFD60A; border: 1px solid rgba(255, 159, 10, 0.3); }
    .pill-general { background: rgba(175, 82, 222, 0.15); color: #BF5AF2; border: 1px solid rgba(175, 82, 222, 0.3); }

    /* Input Styling */
    .stChatInput input {
        background-color: #121318 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #FFFFFF !important;
        border-radius: 16px !important;
        padding: 14px !important;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0A0B0E !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- Helper: Dummy PDF Generator if documents are missing ---
def ensure_sample_pdfs():
    """Generates basic dummy PDFs if actual handbook/fee structure PDFs aren't present."""
    if not os.path.exists("academics_handbook.pdf"):
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        c = canvas.Canvas("academics_handbook.pdf", pagesize=letter)
        c.drawString(100, 750, "ACADEMIC HANDBOOK")
        c.drawString(100, 720, "Attendance Requirement: Students must maintain minimum 75% attendance.")
        c.drawString(100, 700, "Grading Policy: Passing score is 40% in each subject.")
        c.drawString(100, 680, "Degree Requirements: BCA requires 120 total credits. BBA requires 124 credits.")
        c.save()

    if not os.path.exists("fee_structure.pdf"):
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        c = canvas.Canvas("fee_structure.pdf", pagesize=letter)
        c.drawString(100, 750, "OFFICIAL FEE STRUCTURE")
        c.drawString(100, 720, "BCA Tuition Fee: $1,200 per semester. Lab fee: $150.")
        c.drawString(100, 700, "BBA Tuition Fee: $1,400 per semester.")
        c.drawString(100, 680, "B.Com (H) Tuition Fee: $1,100 per semester.")
        c.drawString(100, 660, "Late Payment Fee: $50 charge per week after due date.")
        c.save()

ensure_sample_pdfs()

# --- State Definition ---
class State(TypedDict):
    programme: str  
    messages: Annotated[list, add_messages]
    query_type: str 
    retrieved_context: str 

# --- Cached RAG Indexing ---
@st.cache_resource(show_spinner=False)
def load_rag_retrievers():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    def build_retriever(pdf_path: str):
        loader = PyPDFLoader(pdf_path)
        document = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
        chunks = splitter.split_documents(document)
        vectorstore = FAISS.from_documents(chunks, embeddings)
        return vectorstore.as_retriever(search_kwargs={"k": 4})

    academic = build_retriever("academics_handbook.pdf")
    fee = build_retriever("fee_structure.pdf")
    return academic, fee

# Load Retrievers
with st.spinner("Initializing campus document indexes..."):
    academic_retriever, fee_retriever = load_rag_retrievers()

# --- LangGraph Workflow Compiler ---
def build_graph(model_name: str):
    llm = ChatGroq(model=model_name, temperature=0.4, groq_api_key=GROQ_API_KEY)

    def classifier_node(state: State) -> dict:
        last_message = state['messages'][-1].content
        prompt = (
            "Classify the following student query into exactly one category: "
            "'academic', 'fee', or 'general'.\n\n"
            "Use 'academic' for questions about attendance, exams, grading, credits, "
            "promotion, course structure, summer training, or degree requirements.\n"
            "Use 'fee' for questions about tuition, payment, refund, late charges, "
            "scholarships, or any money-related topic.\n"
            "Use 'general' for greetings, casual talk, or anything not related to "
            "the college rules or fee.\n\n"
            f"Query: {last_message}\n\n"
            "Return only one word: academic, fee, or general."
        )
        response = llm.invoke(prompt)
        category = response.content.strip().lower()

        if "academic" in category:
            category = "academic"
        elif "fee" in category:
            category = "fee"
        else:
            category = "general"
        
        return {"query_type": category}

    def academic_rag_node(state: State) -> dict:
        query = state["messages"][-1].content
        docs = academic_retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in docs])
        return {"retrieved_context": context}

    def fee_rag_node(state: State) -> dict:
        query = state["messages"][-1].content
        docs = fee_retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in docs])
        return {"retrieved_context": context}

    def general_node(state: State) -> dict:
        return {"retrieved_context": "NO_RETRIEVAL_NEEDED"}

    def response_node(state: State) -> dict:
        query = state["messages"][-1].content
        programme = state.get("programme", "Unknown")
        context = state["retrieved_context"]

        if context == "NO_RETRIEVAL_NEEDED":
            prompt = (
                f"You are a friendly college assistant talking to a {programme} student. "
                f"Answer this question using your own general knowledge:\n\n{query}"
            )
        else:
            prompt = (
                f"You are a college assistant helping a {programme} student. "
                f"Use the following context from the official college documents to answer "
                f"the question accurately. If the context mentions specific figures for "
                f"different programmes, highlight the one relevant to {programme} if possible.\n\n"
                f"Context:\n{context}\n\n"
                f"Question: {query}\n\n"
                f"Give a clear, friendly, and precise answer."
            )

        response = llm.invoke(prompt)
        return {"messages": [("ai", response.content.strip())]}

    def route_query(state: State):
        if state['query_type'] == 'academic':
            return "academic_rag"
        elif state['query_type'] == "fee":
            return "fee_rag"
        else:
            return "general"

    graph = StateGraph(State)
    graph.add_node("classifier", classifier_node)
    graph.add_node("academic_rag", academic_rag_node)
    graph.add_node("fee_rag", fee_rag_node)
    graph.add_node("general", general_node)
    graph.add_node("response", response_node)

    graph.add_edge(START, "classifier")
    graph.add_conditional_edges("classifier", route_query)
    graph.add_edge("academic_rag", "response")
    graph.add_edge("fee_rag", "response")
    graph.add_edge("general", "response")
    graph.add_edge("response", END)

    return graph.compile()

# --- Sidebar Configuration ---
with st.sidebar:
    st.markdown("<h3 style='font-weight: 700; color: #F5F5F7;'>🎓 Student Profile</h3>", unsafe_allow_html=True)
    
    student_programme = st.selectbox(
        "Select Your Programme",
        ["BCA", "BBA", "B.Com (H)"],
        index=0
    )

    st.markdown("---")
    st.markdown("<h4 style='font-weight: 600; color: #A1A1A6; font-size: 0.9rem;'>INFERENCE ENGINE</h4>", unsafe_allow_html=True)
    model_name = st.selectbox(
        "LLM Model",
        ["llama-3.3-70b-versatile", "llama3-8b-8192"],
        index=0,
        label_visibility="collapsed"
    )

    st.markdown("---")
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Top Nav Bar ---
auth_status = """<span class="nav-badge badge-active">● API Connected</span>""" if GROQ_API_KEY else """<span class="nav-badge badge-inactive">● Key Missing</span>"""

st.markdown(f"""
    <div class="top-nav">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.2rem;">🎓</span>
            <span style="font-weight: 700; font-size: 1.05rem;">Campus Knowledge Assistant</span>
        </div>
        <div>
            {auth_status}
        </div>
    </div>
""", unsafe_allow_html=True)

# Session state chat initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Render Existing Chat Messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if "query_type" in msg:
            qtype = msg["query_type"]
            pill_class = f"pill-{qtype}"
            st.markdown(f'<span class="route-pill {pill_class}">Route: {qtype.upper()}</span>', unsafe_allow_html=True)
        st.markdown(msg["content"])

# --- Handle User Input ---
if user_query := st.chat_input("Ask about academics, fee structure, or general query..."):
    if not GROQ_API_KEY:
        st.error("🔑 GROQ_API_KEY missing from environment `.env` file.")
    else:
        # Append and display user prompt
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Process through LangGraph
        with st.chat_message("assistant"):
            with st.spinner("Classifying and querying knowledge base..."):
                try:
                    app = build_graph(model_name)
                    
                    # Graph execution
                    result = app.invoke({
                        "programme": student_programme,
                        "messages": [("human", user_query)]
                    })

                    qtype = result.get("query_type", "general")
                    ai_response = result['messages'][-1].content

                    # Display classification badge & response
                    pill_class = f"pill-{qtype}"
                    st.markdown(f'<span class="route-pill {pill_class}">Route: {qtype.upper()}</span>', unsafe_allow_html=True)
                    st.markdown(ai_response)

                    # Save to history
                    st.session_state.messages.append({
                        "role": "assistant",
                        "content": ai_response,
                        "query_type": qtype
                    })

                except Exception as e:
                    st.error(f"Error processing query: {str(e)}")