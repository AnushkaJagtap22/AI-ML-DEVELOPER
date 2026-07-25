import os
from typing import TypedDict, Annotated
import streamlit as st
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph, START, END

# Load environment variables quietly
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- Page Configuration ---
st.set_page_config(
    page_title="Guardrails Studio",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- Ultra-High End Apple macOS/visionOS CSS with High Visibility Inputs ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "SF Pro Display", "SF Pro Text", sans-serif !important;
        background-color: #050507 !important;
        color: #F5F5F7 !important;
    }

    .stApp {
        background-color: #050507 !important;
    }

    /* Glass Container Styling */
    .vision-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .vision-card:hover {
        border-color: rgba(255, 255, 255, 0.16);
        box-shadow: 0 25px 60px rgba(0, 0, 0, 0.7);
    }

    /* Header Styling */
    .hero-title {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(135deg, #FFFFFF 0%, #8E8E93 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 4px;
    }

    .hero-subtitle {
        font-size: 1rem;
        color: #86868B;
        font-weight: 400;
        margin-bottom: 24px;
    }

    /* Top Navigation Bar */
    .top-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 24px;
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 999px;
        margin-bottom: 32px;
    }

    .nav-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 14px;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 600;
        letter-spacing: 0.02em;
    }
    .badge-active { background: rgba(48, 209, 88, 0.12); color: #30D158; border: 1px solid rgba(48, 209, 88, 0.25); }
    .badge-inactive { background: rgba(255, 69, 58, 0.12); color: #FF453A; border: 1px solid rgba(255, 69, 58, 0.25); }

    /* Score Cards */
    .metric-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }
    .metric-name {
        font-size: 0.85rem;
        font-weight: 600;
        color: #86868B;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-number {
        font-size: 2.8rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        line-height: 1;
        margin-bottom: 12px;
    }

    /* ========================================================= */
    /* HIGH-VISIBILITY INPUT & TEXT AREA STYLING                 */
    /* ========================================================= */
    .stTextArea label, .stSelectbox label {
        color: #A1A1A6 !important;
        font-weight: 600 !important;
    }

    .stTextArea textarea {
        background-color: #121318 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
        color: #FFFFFF !important;
        font-family: inherit !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        padding: 16px !important;
        caret-color: #0A84FF !important;
        transition: all 0.2s ease !important;
    }

    .stTextArea textarea::placeholder {
        color: #6E6E73 !important;
    }

    .stTextArea textarea:focus {
        background-color: #161820 !important;
        border-color: #0A84FF !important;
        box-shadow: 0 0 0 2px rgba(10, 132, 255, 0.3) !important;
        outline: none !important;
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
    /* ========================================================= */

    /* Action Button */
    div.stButton > button {
        background: linear-gradient(180deg, #0077ED 0%, #005BB5 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 999px !important;
        padding: 12px 32px !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: -0.01em !important;
        box-shadow: 0 8px 20px rgba(0, 119, 237, 0.3) !important;
        transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div.stButton > button:hover {
        transform: translateY(-1px) scale(1.02);
        box-shadow: 0 12px 28px rgba(0, 119, 237, 0.45) !important;
    }

    /* Hide Default UI Artifacts */
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# --- State Reducer & Definition ---
def merge_score_dicts(existing: dict, newupdate: dict) -> dict:
    if existing is None:
        return newupdate 
    return {**existing, **newupdate}

class AnalyzerState(TypedDict):
    raw_text: str
    safety_scores: Annotated[dict[str, int], merge_score_dicts]

# --- LangGraph Construction ---
def build_analyzer_graph(model_name: str):
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not defined in environment.")

    llm = ChatGroq(model=model_name, temperature=0.1, groq_api_key=GROQ_API_KEY)

    def toxicity_node(state: AnalyzerState) -> dict:
        prompt = (
            "Analyze the text for profanity, aggression, hate speech, or toxicity. "
            "Provide a score from 0 to 100, where 0 means safe and 100 means highly toxic. "
            "Return ONLY the plain integer number, nothing else.\n\n"
            f"Text:\n{state['raw_text']}"
        )
        res = llm.invoke(prompt)
        try:
            score = int(res.content.strip())
        except ValueError:
            score = 0
        return {"safety_scores": {"toxicity_level": score}}

    def copyright_node(state: AnalyzerState) -> dict:
        prompt = (
            "Analyze the text for copyright, plagiarism, or trademark risk. "
            "Provide a score from 0 to 100, where 0 means clean and 100 means severe risk. "
            "Return ONLY the plain integer number, nothing else.\n\n"
            f"Text:\n{state['raw_text']}"
        )
        res = llm.invoke(prompt)
        try:
            score = int(res.content.strip())
        except ValueError:
            score = 0
        return {"safety_scores": {"copyright_risk": score}}

    def culture_node(state: AnalyzerState) -> dict:
        prompt = (
            "Analyze the text for regional sensitivities, political landmines, or cultural offense. "
            "Provide a score from 0 to 100, where 0 means safe and 100 means highly offensive. "
            "Return ONLY the plain integer number, nothing else.\n\n"
            f"Text:\n{state['raw_text']}"
        )
        res = llm.invoke(prompt)
        try:
            score = int(res.content.strip())
        except ValueError:
            score = 0
        return {"safety_scores": {"cultural_insensitivity": score}}

    builder = StateGraph(AnalyzerState)

    builder.add_node("toxicity_node", toxicity_node)
    builder.add_node("copyright_check", copyright_node)
    builder.add_node("culture_node", culture_node)

    # Parallel fan-out
    builder.add_edge(START, "toxicity_node")
    builder.add_edge(START, "copyright_check")
    builder.add_edge(START, "culture_node")

    # Fan-in aggregation
    builder.add_edge("toxicity_node", END)
    builder.add_edge("copyright_check", END)
    builder.add_edge("culture_node", END)

    return builder.compile()

# --- Custom Score Card Renderer ---
def render_vision_metric(label: str, score: int, icon: str):
    if score >= 70:
        color = "#FF453A"
        bg_pill = "rgba(255, 69, 58, 0.12)"
        border_pill = "rgba(255, 69, 58, 0.25)"
        status_text = "High Risk"
    elif score >= 35:
        color = "#FFD60A"
        bg_pill = "rgba(255, 214, 10, 0.12)"
        border_pill = "rgba(255, 214, 10, 0.25)"
        status_text = "Moderate"
    else:
        color = "#30D158"
        bg_pill = "rgba(48, 209, 88, 0.12)"
        border_pill = "rgba(48, 209, 88, 0.25)"
        status_text = "Passed"

    st.markdown(f"""
        <div class="vision-card">
            <div class="metric-header">
                <span class="metric-name">{icon} {label}</span>
                <span style="background: {bg_pill}; color: {color}; border: 1px solid {border_pill}; padding: 3px 10px; border-radius: 999px; font-size: 0.72rem; font-weight: 600;">
                    {status_text}
                </span>
            </div>
            <div class="metric-number" style="color: {color};">{score}<span style="font-size: 1.1rem; color: #6E6E73; font-weight: 500;"> / 100</span></div>
        </div>
    """, unsafe_allow_html=True)
    st.progress(score / 100)

# --- Top Navigation Bar ---
auth_status = """<span class="nav-badge badge-active">● API Connected</span>""" if GROQ_API_KEY else """<span class="nav-badge badge-inactive">● Key Missing</span>"""

st.markdown(f"""
    <div class="top-nav">
        <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.2rem;">🛡️</span>
            <span style="font-weight: 700; font-size: 1.05rem; letter-spacing: -0.02em;">Guardrails Studio</span>
        </div>
        <div>
            {auth_status}
        </div>
    </div>
""", unsafe_allow_html=True)

# --- Hero Title Section ---
st.markdown('<div class="hero-title">Content Guardrails Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-subtitle">Parallel multi-branch evaluation powered by LangGraph state aggregation engines.</div>', unsafe_allow_html=True)

# --- Controls Grid ---
col_text, col_config = st.columns([3, 1])

sample_script = """Yo guys! Welcome back to the stream. Today I am going to show you how to hack into 
your friend's system using a script I copied directly from an online forum. 
Honestly, traditional security protocols are absolute garbage and anyone still using 
them is an absolute idiot. Let's dive into the code!"""

with col_text:
    st.markdown("<span style='font-size: 0.85rem; font-weight: 600; color: #A1A1A6; margin-bottom: 6px; display: block;'>INPUT CONTENT</span>", unsafe_allow_html=True)
    raw_text = st.text_area(
        "Input Content Area", 
        value=sample_script, 
        height=150,
        label_visibility="collapsed",
        placeholder="Type or paste content to evaluate..."
    )

with col_config:
    st.markdown("<span style='font-size: 0.85rem; font-weight: 600; color: #A1A1A6; margin-bottom: 6px; display: block;'>INFERENCE ENGINE</span>", unsafe_allow_html=True)
    model_name = st.selectbox(
        "Model Selection",
        ["llama-3.3-70b-versatile", "llama3-8b-8192", "mixtral-8x7b-32768"],
        index=0,
        label_visibility="collapsed"
    )
    st.markdown("<br>", unsafe_allow_html=True)
    run_btn = st.button("⚡ Execute Guardrails", use_container_width=True)

# --- Graph Execution ---
if run_btn:
    if not GROQ_API_KEY:
        st.error("🔑 GROQ_API_KEY missing from environment. Please create a `.env` file.")
    elif not raw_text.strip():
        st.warning("⚠️ Please provide input text to analyze.")
    else:
        try:
            with st.spinner("Processing graph branches in parallel..."):
                app = build_analyzer_graph(model_name)
                initial_state = {"raw_text": raw_text, "safety_scores": {}}
                final_state = app.invoke(initial_state)
                scores = final_state.get("safety_scores", {})

            st.markdown("<br><br>", unsafe_allow_html=True)
            st.markdown("<h3 style='font-weight: 700; font-size: 1.3rem; margin-bottom: 20px;'>Evaluation Breakdown</h3>", unsafe_allow_html=True)

            tox = scores.get("toxicity_level", 0)
            copy_risk = scores.get("copyright_risk", 0)
            cult = scores.get("cultural_insensitivity", 0)

            c1, c2, c3 = st.columns(3)
            with c1:
                render_vision_metric("Toxicity & Hate", tox, "🤬")
            with c2:
                render_vision_metric("Copyright & IP", copy_risk, "🔏")
            with c3:
                render_vision_metric("Cultural Risk", cult, "🌍")

            st.markdown("<br>", unsafe_allow_html=True)

            # Executive Verdict Banner
            max_score = max(tox, copy_risk, cult)
            if max_score >= 70:
                banner_bg = "rgba(255, 69, 58, 0.08)"
                banner_border = "rgba(255, 69, 58, 0.25)"
                title_color = "#FF453A"
                verdict_title = "Action Required: Content Flagged"
                verdict_desc = "One or more parallel nodes breached the safe threshold limit (≥70). Revision mandatory prior to publishing."
            elif max_score >= 35:
                banner_bg = "rgba(255, 214, 10, 0.08)"
                banner_border = "rgba(255, 214, 10, 0.25)"
                title_color = "#FFD60A"
                verdict_title = "Moderate Caution Advised"
                verdict_desc = "Content displays elevated risk scores in specific areas. Manual compliance verification recommended."
            else:
                banner_bg = "rgba(48, 209, 88, 0.08)"
                banner_border = "rgba(48, 209, 88, 0.25)"
                title_color = "#30D158"
                verdict_title = "Approved for Distribution"
                verdict_desc = "All parallel branches reported low risk metrics within standard safety boundaries."

            st.markdown(f"""
                <div style="background: {banner_bg}; border: 1px solid {banner_border}; border-radius: 20px; padding: 24px; margin-top: 10px;">
                    <div style="color: {title_color}; font-size: 1.15rem; font-weight: 700; margin-bottom: 4px;">{verdict_title}</div>
                    <div style="color: #A1A1A6; font-size: 0.92rem;">{verdict_desc}</div>
                </div>
            """, unsafe_allow_html=True)

            # Payload inspector
            with st.expander("🔍 Inspect Merged LangGraph State"):
                st.json(final_state)

        except Exception as e:
            st.error(f"Execution Error: {str(e)}")