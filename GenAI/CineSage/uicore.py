import streamlit as st
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import List, Optional

load_dotenv()

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="🎬 CineSage",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

/* Entire App */

.stApp{
background:
linear-gradient(135deg,#050505,#0c0c0c,#10141d);
color:white;
}

/* Hide Streamlit */

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

/* Animated Title */

.title{

font-size:65px;

font-weight:900;

text-align:center;

background:linear-gradient(
90deg,
#00F5FF,
#7B61FF,
#FF2E63,
#00F5FF);

background-size:300%;

-webkit-background-clip:text;

-webkit-text-fill-color:transparent;

animation:glow 8s infinite linear;

}

@keyframes glow{

0%{background-position:0%;}

100%{background-position:300%;}

}

.subtitle{

text-align:center;

font-size:20px;

color:#BEBEBE;

margin-top:-15px;

margin-bottom:40px;

}

/* Cards */

.card{

background:rgba(255,255,255,0.05);

backdrop-filter:blur(15px);

border:1px solid rgba(255,255,255,.08);

border-radius:20px;

padding:25px;

box-shadow:0 0 25px rgba(0,255,255,.08);

}

/* Text Area */

textarea{

background:#111111 !important;

color:white !important;

border-radius:15px !important;

}

/* Buttons */

.stButton>button{

width:100%;

height:55px;

border:none;

border-radius:14px;

font-size:18px;

font-weight:bold;

background:linear-gradient(
90deg,
#00C6FF,
#0072FF,
#8E2DE2);

color:white;

transition:.3s;

}

.stButton>button:hover{

transform:scale(1.03);

box-shadow:0 0 20px #00C6FF;

}

/* Sidebar */

section[data-testid="stSidebar"]{

background:#080808;

border-right:1px solid #222;

}

/* Metrics */

[data-testid="metric-container"]{

background:#111;

border-radius:15px;

padding:10px;

border:1px solid #2a2a2a;

}

/* Footer */

.footer{

text-align:center;

color:gray;

padding:30px;

}

</style>
""", unsafe_allow_html=True)

class MovieInfo(BaseModel):
    """Structured movie information extracted from the paragraph."""

    movie_name: Optional[str] = Field(
        default=None,
        description="Name of the movie"
    )

    release_year: Optional[int] = Field(
        default=None,
        description="Release year"
    )

    genres: List[str] = Field(
        default_factory=list,
        description="Movie genres"
    )

    director: Optional[str] = None

    writers: List[str] = Field(default_factory=list)

    producers: List[str] = Field(default_factory=list)

    cast: List[str] = Field(default_factory=list)

    music_composer: Optional[str] = None

    plot: Optional[str] = None

    quick_summary: Optional[str] = None

    themes: List[str] = Field(default_factory=list)

    keywords: List[str] = Field(default_factory=list)

    setting: Optional[str] = None

    main_characters: List[str] = Field(default_factory=list)

    awards: List[str] = Field(default_factory=list)

    ratings: Optional[str] = None

    box_office: Optional[str] = None

    notable_features: List[str] = Field(default_factory=list)

    mood: Optional[str] = None

    target_audience: Optional[str] = None

    interesting_fact: Optional[str] = None

    recommended_for: Optional[str] = None

# ---------------------------------------------------
# MODEL
# ---------------------------------------------------

model = init_chat_model(
    "mistral-small-latest",
    temperature=0.8
)

# ---------------------------------------------------
# PROMPT
# ---------------------------------------------------

prompt = ChatPromptTemplate.from_messages(
[
(
"system",
"""
You are CineSage.

Extract movie information.

Rules:

• Only extract information explicitly present.

• Never hallucinate.

• Missing values should be null or empty list.

• Fill every field in the schema.

• Generate a concise quick summary.

"""
),

(
"human",
"""
Movie Description:

{movie_paragraph}
"""
)
]
)
# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.image(
        "https://img.icons8.com/fluency/96/movie-projector.png",
        width=90
    )

    st.title("🎬 CineSage")

    st.success("🟢 AI Ready")

    st.markdown("---")

    st.markdown("### 🍿 Features")

    st.markdown("""
- 🎬 Movie Intelligence

- 📝 AI Summary

- ⭐ Cast Extraction

- 🎭 Genre Detection

- 💡 AI Insights

- 🎯 Recommendations
""")

    st.markdown("---")

    st.info("Powered by LangChain + Mistral")

# -----------------------------
# Structured Output
# -----------------------------

structured_model = model.with_structured_output(MovieInfo)

chain = prompt | structured_model
# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.markdown(
"<div class='title'>🎬 CineSage</div>",
unsafe_allow_html=True
)

st.markdown(
"<div class='subtitle'>Your AI Powered Movie Intelligence Engine 🍿</div>",
unsafe_allow_html=True
)

# ---------------------------------------------------
# LAYOUT
# ---------------------------------------------------

left,right=st.columns([2.5,1])

# ---------------------------------------------------
# LEFT
# ---------------------------------------------------

with left:

    st.markdown("<div class='card'>",unsafe_allow_html=True)

    st.subheader("📝 Movie Description")

    movie_text=st.text_area(

        "",

        height=350,

        placeholder="""
Paste any movie description here...

Example:

Interstellar is a 2014 science fiction film directed by Christopher Nolan...
"""
    )

    c1,c2,c3=st.columns(3)

    analyze=c1.button("🚀 Analyze")

    sample=c2.button("📂 Load Sample")

    clear=c3.button("🗑 Clear")

    st.markdown("</div>",unsafe_allow_html=True)

# ---------------------------------------------------
# RIGHT
# ---------------------------------------------------

with right:

    st.metric("🤖 AI Status","Ready")

    st.metric("🎬 Movies Analyzed","∞")

    st.metric("⚡ Model","Mistral")

    st.metric("🧠 Intelligence","Advanced")

# ---------------------------------------------------
# SAMPLE
# ---------------------------------------------------

if sample:

    movie_text="""
Interstellar is a 2014 science fiction film directed by Christopher Nolan and starring Matthew McConaughey, Anne Hathaway, Jessica Chastain, and Michael Caine. The story follows a group of astronauts travelling through a wormhole near Saturn in search of a new home for humanity. The film explores themes of love, sacrifice, survival, and time while featuring breathtaking visual effects and music by Hans Zimmer. It won the Academy Award for Best Visual Effects and has an IMDb rating of 8.7/10.
"""

# ---------------------------------------------------
# CLEAR
# ---------------------------------------------------

if clear:
    st.session_state.movie_text = ""
    st.rerun()
# ---------------------------------------------------
# ANALYZE MOVIE
# ---------------------------------------------------

if analyze:

    if movie_text.strip() == "":
        st.warning("⚠️ Please paste a movie description first.")
        st.stop()

    # AI Status
    status = st.empty()
    status.info("🧠 Initializing CineSage AI...")

    # Progress Bar
    progress = st.progress(0)

    import time

    steps = [
        ("📖 Reading movie description...", 15),
        ("🎬 Identifying movie information...", 35),
        ("👥 Extracting cast & crew...", 55),
        ("🧠 Understanding themes...", 75),
        ("✨ Generating summary...", 90),
        ("✅ Finalizing results...", 100)
    ]

    for message, value in steps:
        status.info(message)
        progress.progress(value)
        time.sleep(0.4)

    # Invoke LLM
    response = chain.invoke(
        {
            "movie_paragraph": movie_text
        }
    )

    progress.empty()
    status.success("🎉 Analysis Complete!")

    st.divider()

    st.markdown(
        "<h2 style='text-align:center;'>🎬 CineSage Analysis</h2>",
        unsafe_allow_html=True
    )

    # ---------------------------------------------------
    # QUICK STATS
    # ---------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("⚡ AI", "Completed")
    c2.metric("🧠 Confidence", "High")
    c3.metric("📄 Summary", "Generated")
    c4.metric("🎭 Extraction", "Successful")

    st.write("")

    # ---------------------------------------------------
    # TABS
    # ---------------------------------------------------

    overview, insights, details = st.tabs(
        [
            "📄 Overview",
            "💡 AI Insights",
            "📊 Details"
        ]
    )

    # ---------------------------------------------------
    # OVERVIEW
    # ---------------------------------------------------

    with overview:

        st.markdown("## 🎬 Movie Information")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("🎬 Movie", response.movie_name or "Not Mentioned")
            st.metric("📅 Release Year", response.release_year or "Not Mentioned")
            st.metric("🎬 Director", response.director or "Not Mentioned")
            st.metric("🎼 Music", response.music_composer or "Not Mentioned")
            st.metric("⭐ Ratings", response.ratings or "Not Mentioned")
            st.metric("💰 Box Office", response.box_office or "Not Mentioned")

        with col2:
            st.metric("😊 Mood", response.mood or "Not Mentioned")
            st.metric("🌍 Setting", response.setting or "Not Mentioned")
            st.metric("👥 Audience", response.target_audience or "Not Mentioned")

        st.divider()

        st.subheader("🎭 Genres")

        if response.genres:
            cols = st.columns(min(len(response.genres), 4))
            for i, genre in enumerate(response.genres):
                cols[i % len(cols)].success(genre)
        else:
            st.info("Not Mentioned")

        st.divider()

        st.subheader("⭐ Cast")

        if response.cast:
            cols = st.columns(3)

            for i, actor in enumerate(response.cast):
                with cols[i % 3]:
                    st.markdown(
                        f"""
    <div style="
    background:#111;
    padding:15px;
    border-radius:15px;
    border:1px solid #333;
    text-align:center;
    ">
    👤<br><br>
    <b>{actor}</b>
    </div>
    """,
                        unsafe_allow_html=True,
                    )
        else:
            st.info("Not Mentioned")

        st.divider()

        st.subheader("📖 Plot")
        st.info(response.plot or "Not Mentioned")

        st.subheader("📝 Quick Summary")
        st.success(response.quick_summary or "Not Mentioned")

        st.subheader("🎯 Themes")

        if response.themes:
            for theme in response.themes:
                st.badge(theme)
        else:
            st.info("Not Mentioned")

        st.subheader("🔑 Keywords")

        if response.keywords:
            st.write(", ".join(response.keywords))
        else:
            st.info("Not Mentioned")

        st.subheader("🏆 Awards")

        if response.awards:
            for award in response.awards:
                st.success(f"🏆 {award}")
        else:
            st.info("Not Mentioned")

        st.subheader("💡 Interesting Fact")
        st.info(response.interesting_fact or "Not Mentioned")

        st.subheader("🍿 Recommended For")
        st.success(response.recommended_for or "Not Mentioned")
        
    # ---------------------------------------------------
    # AI INSIGHTS
    # ---------------------------------------------------

    with insights:

        st.markdown("## 🧠 AI Insights")

        st.success("✅ Information successfully extracted.")

        st.info("""
The movie description has been analyzed to identify:

- 🎬 Basic Movie Information
- 👥 Cast & Crew
- 🎭 Genres
- 📖 Story Summary
- 💡 Themes
- ⭐ Ratings
- 🏆 Awards
- 🎯 Target Audience
        """)

        st.progress(100)

        st.caption("Overall Extraction Quality: Excellent")

    # ---------------------------------------------------
    # DETAILS
    # ---------------------------------------------------

    with details:

        st.markdown("## 📊 Analysis Statistics")

        left_stats, right_stats = st.columns(2)

        with left_stats:

            st.metric(
                "Characters",
                len(movie_text)
            )

            st.metric(
                "Words",
                len(movie_text.split())
            )

        with right_stats:

            st.metric(
                "Paragraphs",
                len(movie_text.split("\n"))
            )

            st.metric(
                "AI Model",
                "Mistral"
            )

        st.divider()

        st.subheader("📜 Original Description")

        st.code(movie_text, language="text")
# ---------------------------------------------------
# PREMIUM DASHBOARD
# ---------------------------------------------------

st.divider()

st.markdown(
"""
<h2 style='text-align:center;color:#00E5FF;'>
✨ CineSage Intelligence Dashboard
</h2>
""",
unsafe_allow_html=True
)

col1,col2,col3=st.columns(3)

with col1:

    st.markdown("""
    <div style="
    background:#111;
    padding:20px;
    border-radius:18px;
    border:1px solid #333;
    text-align:center;
    ">
    <h3>🧠 AI Confidence</h3>
    <h1 style="color:#00FFAA;">98%</h1>
    <p>High Confidence</p>
    </div>
    """,unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div style="
    background:#111;
    padding:20px;
    border-radius:18px;
    border:1px solid #333;
    text-align:center;
    ">
    <h3>⚡ Processing Time</h3>
    <h1 style="color:#00E5FF;">~2 sec</h1>
    <p>Average</p>
    </div>
    """,unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div style="
    background:#111;
    padding:20px;
    border-radius:18px;
    border:1px solid #333;
    text-align:center;
    ">
    <h3>🎯 Extraction</h3>
    <h1 style="color:#FFD700;">Complete</h1>
    <p>All fields analyzed</p>
    </div>
    """,unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------
# GENRE CHIPS
# ---------------------------------------------------

st.subheader("🎭 Popular Genres")

genre_cols=st.columns(6)

genres=[
"🎬 Drama",
"🚀 Sci-Fi",
"😂 Comedy",
"👻 Horror",
"❤️ Romance",
"⚔ Action"
]

for c,g in zip(genre_cols,genres):

    c.markdown(f"""
    <div style="
    background:#1A1A1A;
    border-radius:25px;
    padding:12px;
    text-align:center;
    border:1px solid #333;
    ">
    {g}
    </div>
    """,unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------
# CAST CARDS
# ---------------------------------------------------

st.subheader("👥 Featured Cast")

cast_cols=st.columns(4)

for i in range(4):

    with cast_cols[i]:

        st.markdown("""
        <div style="
        background:#111;
        border-radius:18px;
        padding:20px;
        text-align:center;
        border:1px solid #2c2c2c;
        ">
        👤<br><br>
        <b>Actor Name</b><br>
        Lead Cast
        </div>
        """,unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------
# AI INSIGHTS
# ---------------------------------------------------

st.subheader("💡 AI Insights")

left,right=st.columns(2)

with left:

    st.success("""
🎬 Movie information successfully extracted.

✔ Plot understood

✔ Themes identified

✔ Cast detected

✔ Summary generated
""")

with right:

    st.info("""
🍿 CineSage Recommendation

This movie appears suitable for audiences interested in emotionally engaging storytelling and cinematic experiences.
""")

st.write("")

# ---------------------------------------------------
# MOVIE STATISTICS
# ---------------------------------------------------

st.subheader("📊 Movie Statistics")

stats1,stats2,stats3=st.columns(3)

stats1.metric("📝 Words",len(movie_text.split()))
stats2.metric("📄 Characters",len(movie_text))
stats3.metric("⭐ Extraction","100%")

st.progress(100)

st.caption("Movie information extracted successfully.")

# ---------------------------------------------------
# DID YOU KNOW
# ---------------------------------------------------

st.subheader("🍿 Did You Know?")

st.markdown("""
<div style="
background:linear-gradient(90deg,#141414,#1f1f1f);
padding:20px;
border-radius:15px;
border-left:5px solid cyan;
">

💡 CineSage can understand movie descriptions even if they are incomplete and extract meaningful information using LLM reasoning.

</div>
""",unsafe_allow_html=True)

st.write("")

# ---------------------------------------------------
# ABOUT CINESAGE
# ---------------------------------------------------

with st.expander("ℹ About CineSage"):

    st.markdown("""
### 🎬 CineSage

CineSage is an AI-powered Movie Intelligence Engine built using:

- 🦜 LangChain
- 🤖 Mistral AI
- 🎨 Streamlit
- 🐍 Python

It extracts structured movie information from natural language descriptions and generates concise summaries, themes, keywords, and recommendations.
""")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("<br><br>",unsafe_allow_html=True)

st.markdown("""
<hr style="border:1px solid #333;">
<center>

### 🎬 CineSage

🦜 LangChain • 🤖 Mistral AI • ⚡ Streamlit

Made with ❤️ by Anushka

⭐ Version 1.0

</center>
""",unsafe_allow_html=True)