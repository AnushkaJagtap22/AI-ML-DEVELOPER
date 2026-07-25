import os
from typing import TypedDict, Annotated
import streamlit as st
from dotenv import load_dotenv

# LangGraph & LangChain imports
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_groq import ChatGroq
from langchain_tavily import TavilySearch
from langchain_core.tools import tool

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# --- Page Setup ---
st.set_page_config(
    page_title="LinkedIn Post Studio",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- High-End Apple macOS / visionOS Styling ---
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

    /* Glassmorphism Card Container */
    .apple-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        margin-bottom: 20px;
    }

    /* Top Navigation Bar */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 28px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 999px;
        margin-bottom: 28px;
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

    /* Verdict Badges */
    .verdict-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .badge-approved { background: rgba(48, 209, 88, 0.15); color: #30D158; border: 1px solid rgba(48, 209, 88, 0.3); }
    .badge-rejected { background: rgba(255, 69, 58, 0.15); color: #FF453A; border: 1px solid rgba(255, 69, 58, 0.3); }

    /* High-Visibility Text Area Styling */
    .stTextArea label {
        color: #A1A1A6 !important;
        font-weight: 600 !important;
    }

    .stTextArea textarea {
        background-color: #121318 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        color: #FFFFFF !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        padding: 16px !important;
        caret-color: #0A84FF !important;
    }

    .stTextArea textarea:focus {
        border-color: #0A84FF !important;
        box-shadow: 0 0 0 2px rgba(10, 132, 255, 0.3) !important;
    }

    /* Primary Action Button */
    div.stButton > button {
        background: linear-gradient(180deg, #0077ED 0%, #005BB5 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 999px !important;
        padding: 12px 32px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        box-shadow: 0 8px 20px rgba(0, 119, 237, 0.3) !important;
        transition: all 0.2s ease !important;
    }

    div.stButton > button:hover {
        transform: translateY(-1px) scale(1.02);
        box-shadow: 0 12px 28px rgba(0, 119, 237, 0.45) !important;
    }

    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: #0A0B0E !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    /* Selectbox Visibility Fix */
    div[data-baseweb="select"] {
        background-color: #121318 !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
    }

    div[data-baseweb="select"] * {
        color: #FFFFFF !important;
        background-color: transparent !important;
    }

    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- State Definition ---
class State(TypedDict):
    topic: str 
    messages: Annotated[list, add_messages]
    draft: str 
    review_feedback: str
    is_approved: bool 
    attempt: int

# --- Prompts ---
WRITER_SYSTEM_PROMPT = (
    "You are an expert LinkedIn content writer. Your job is to write "
    "engaging, professional LinkedIn posts about the given topic.\n\n"
    "If you need up-to-date information, call the `tavily_search` tool. "
    "IMPORTANT: Pass ONLY a simple string query (e.g. {\"query\": \"your topic\"}). "
    "Do NOT pass any extra fields like start_date, end_date, or domains.\n\n"
    "Rules for good LinkedIn posts:\n"
    "- Strong hook in the first line\n"
    "- 1 clear takeaway\n"
    "- Easy to skim (short paragraphs)\n"
    "- Around 150–200 words\n"
    "- Ends with a question or CTA\n"
    "- Do not use hashtags."
)

REVIEWER_SYSTEM_PROMPT = (
    "You are a strict LinkedIn content reviewer. You judge whether a "
    "post is publish-ready. Evaluate against these criteria:\n"
    "1. Strong hook in the first line\n"
    "2. One clear, valuable takeaway\n"
    "3. Easy to skim — uses short paragraphs\n"
    "4. Roughly 150-200 words\n"
    "5. Ends with an engaging question or CTA\n"
    "6. Professional but human tone (not corporate-robotic)\n"
    "7. No hashtags\n\n"
    "Respond in exactly this format:\n"
    "VERDICT: APPROVED or REJECTED\n"
    "FEEDBACK: <one short paragraph explaining why>\n\n"
    "Be strict but fair. Approve only if the post genuinely meets all "
    "criteria. Reject if even one criterion is clearly missing."
)

# --- Explicit Tool Definition (Prevents Groq 400 Schema Errors) ---
tavily_base_tool = TavilySearch(max_results=3)

@tool("tavily_search")
def search_tool(query: str) -> str:
    """Searches the web for up-to-date information on a given topic."""
    return tavily_base_tool.invoke({"query": query})

# --- Graph Compiler ---
def build_agent_graph(model_name: str, max_attempts: int):
    tools = [search_tool]

    # Lower temperature prevents hallucinating tool schema arguments
    writer_llm = ChatGroq(model=model_name, temperature=0.1, groq_api_key=GROQ_API_KEY)
    writer_llm_with_tools = writer_llm.bind_tools(tools)
    reviewer_llm = ChatGroq(model=model_name, temperature=0.2, groq_api_key=GROQ_API_KEY)

    def writer_node(state: State) -> dict:
        attempt = state.get("attempt", 0) + 1 
        topic = state["topic"]
        previous_feedback = state.get('review_feedback', '')

        if attempt == 1:
            user_message = (
                f"Write a LinkedIn post on this topic: {topic}. "
                f"If you need current information, search the web first."
            )
        else:
            user_message = (
                f"Your previous draft on '{topic}' was rejected. "
                f"Here is the reviewer's feedback:\n\n{previous_feedback}\n\n"
                f"Write a new, improved draft that fixes every issue mentioned. Do not repeat the same mistake."
            )
        
        # Preserve state context
        messages = [("system", WRITER_SYSTEM_PROMPT)] + state.get("messages", []) + [("human", user_message)]
        response = writer_llm_with_tools.invoke(messages)

        return {
            "messages": [response],
            "attempt": attempt
        }

    tool_node = ToolNode(tools)

    def extract_draft_node(state: State) -> dict:
        last_message = state['messages'][-1]
        draft = last_message.content 
        return {"draft": draft}

    def reviewer_node(state: State) -> dict:
        draft = state['draft']
        prompt = f"Review this LinkedIn post draft:\n{draft}\nGive your review."
        
        response = reviewer_llm.invoke(
            [("system", REVIEWER_SYSTEM_PROMPT), ("human", prompt)]
        )
        review_text = response.content.strip()
        
        is_approved = "APPROVED" in review_text.upper().split("FEEDBACK")[0]

        if "FEEDBACK:" in review_text:
            feedback = review_text.split("FEEDBACK:", 1)[1].strip()
        else:
            feedback = review_text

        return {
            "review_feedback": feedback,
            "is_approved": is_approved,
        }

    def should_use_tool(state: State):
        last_message = state['messages'][-1]
        if getattr(last_message, 'tool_calls', None):
            return "tools"
        return "extract_draft"

    def should_stop_looping(state: State):
        if state['is_approved']:
            return END
        if state['attempt'] >= max_attempts:
            return END 
        return "writer"

    graph = StateGraph(State)

    graph.add_node("writer", writer_node)
    graph.add_node("tools", tool_node)
    graph.add_node("extract_draft", extract_draft_node)
    graph.add_node("reviewer", reviewer_node)

    graph.add_edge(START, "writer")
    graph.add_conditional_edges("writer", should_use_tool)
    
    # Corrected Graph Edge: Search results route back to writer
    graph.add_edge("tools", "writer")
    graph.add_edge("extract_draft", "reviewer")
    
    graph.add_conditional_edges("reviewer", should_stop_looping)

    return graph.compile()

# --- Sidebar Controls ---
with st.sidebar:
    st.markdown("<h3 style='font-weight: 700; color: #F5F5F7;'>⚙️ Agent Config</h3>", unsafe_allow_html=True)
    
    model_name = st.selectbox(
        "LLM Inference Model",
        ["llama-3.3-70b-versatile", "llama3-8b-8192"],
        index=0
    )
    
    max_attempts = st.slider(
        "Max Iteration Attempts",
        min_value=1,
        max_value=5,
        value=3,
        help="Maximum times the writer will revise the post before stopping."
    )

    st.markdown("---")
    st.markdown("### 🔑 API Verification")
    if GROQ_API_KEY and TAVILY_API_KEY:
        st.success("Groq & Tavily Active")
    else:
        st.error("Missing Keys in `.env`")

# --- Header Navigation Bar ---
auth_status = """<span class="nav-badge badge-active">● Environment Ready</span>""" if (GROQ_API_KEY and TAVILY_API_KEY) else """<span class="nav-badge badge-inactive">● Key Missing</span>"""

st.markdown(f"""
    <div class="top-nav">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.2rem;">✍️</span>
            <span style="font-weight: 700; font-size: 1.05rem;">LinkedIn Post Agent Studio</span>
        </div>
        <div>
            {auth_status}
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("<h1 style='font-size: 2.2rem; font-weight: 800; letter-spacing: -0.02em;'>Autonomous Post Studio</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #86868B; margin-bottom: 28px;'>Self-evaluating multi-agent loop with active Tavily web search integration.</p>", unsafe_allow_html=True)

# --- Topic Input Form ---
topic_input = st.text_area(
    "TOPIC OR PROMPT",
    placeholder="e.g., Nvidia AIML Engineer role and responsibilities in 2026...",
    height=100
)

col_run, _ = st.columns([1, 4])
with col_run:
    generate_btn = st.button("🚀 Draft & Refine Post", use_container_width=True)

# --- Processing & Graph Streaming UI ---
if generate_btn:
    if not GROQ_API_KEY or not TAVILY_API_KEY:
        st.error("Please add `GROQ_API_KEY` and `TAVILY_API_KEY` to your `.env` file.")
    elif not topic_input.strip():
        st.warning("Please enter a topic to generate a post.")
    else:
        try:
            app = build_agent_graph(model_name, max_attempts)
            
            initial_state = {
                "topic": topic_input,
                "messages": [],
                "draft": "",
                "review_feedback": "",
                "is_approved": False,
                "attempt": 0,
            }

            status_container = st.status("Executing Writer-Reviewer Loop...", expanded=True)

            # Stream graph state steps
            for event in app.stream(initial_state):
                for node_name, state_update in event.items():
                    if node_name == "writer":
                        status_container.write(f"✍️ **Writer Node:** Drafted post (Attempt {state_update.get('attempt', 1)})...")
                    elif node_name == "tools":
                        status_container.write("🌐 **Search Tool:** Querying Tavily web search for fresh context...")
                    elif node_name == "reviewer":
                        is_appr = state_update.get("is_approved", False)
                        status_container.write(f"🧐 **Reviewer Node:** Evaluated draft. Approval Status: `{is_appr}`")

            status_container.update(label="Loop Completed Successfully!", state="complete", expanded=False)

            # Retrieve final state
            final_state = app.invoke(initial_state)

            st.markdown("<br>", unsafe_allow_html=True)
            
            # --- Executive Summary Banner ---
            if final_state["is_approved"]:
                st.markdown("""
                    <div style="background: rgba(48, 209, 88, 0.08); border: 1px solid rgba(48, 209, 88, 0.25); border-radius: 16px; padding: 20px;">
                        <span class="verdict-badge badge-approved">Approved for Publication</span>
                        <p style="color: #F5F5F7; margin-top: 8px; font-weight: 500;">Draft met all strict engagement and clarity criteria within allocated attempts.</p>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                    <div style="background: rgba(255, 69, 58, 0.08); border: 1px solid rgba(255, 69, 58, 0.25); border-radius: 16px; padding: 20px;">
                        <span class="verdict-badge badge-rejected">Max Iterations Reached</span>
                        <p style="color: #F5F5F7; margin-top: 8px; font-weight: 500;">Reached maximum revision attempts. Displaying best available draft below.</p>
                    </div>
                """, unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # --- Layout: Main Output Card & History Tabs ---
            col_left, col_right = st.columns([3, 2])

            with col_left:
                st.markdown("<h3 style='font-weight: 700; font-size: 1.2rem;'>📄 Final Generated Post</h3>", unsafe_allow_html=True)
                st.text_area(
                    "Publish Ready Output",
                    value=final_state["draft"],
                    height=280,
                    label_visibility="collapsed"
                )

            with col_right:
                st.markdown("<h3 style='font-weight: 700; font-size: 1.2rem;'>🔁 Revision Audit Trail</h3>", unsafe_allow_html=True)
                st.write(f"**Total Attempts Executed:** `{final_state['attempt']}`")
                
                if final_state.get("review_feedback"):
                    st.markdown("**Latest Reviewer Feedback:**")
                    st.info(final_state["review_feedback"])

        except Exception as e:
            st.error(f"Execution Error: {str(e)}")