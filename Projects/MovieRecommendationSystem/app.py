import requests
import streamlit as st

# =========================================================
# CONFIG
# =========================================================
API_BASE = "https://movie-rec-466x.onrender.com"
TMDB_IMG = "https://image.tmdb.org/t/p/w500"

st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide",
)

# =========================================================
# MODERN NETFLIX STYLE UI
# =========================================================
st.markdown("""
<style>

/* Entire App */
.stApp{
    background-color:#0f1117;
    color:white;
}

/* Hide Streamlit Header */
header{
    visibility:hidden;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#151821;
    border-right:1px solid #222;
}

/* Inputs */
.stTextInput input{
    background:#1a1d26;
    color:white;
    border-radius:14px;
    border:1px solid #333;
    padding:12px;
}

/* Selectbox */
.stSelectbox div[data-baseweb="select"]{
    background:#1a1d26;
    border-radius:12px;
}

/* Buttons */
.stButton button{
    width:100%;
    border:none;
    border-radius:12px;
    background:#e50914;
    color:white;
    font-weight:600;
    padding:10px;
    transition:0.3s;
}

.stButton button:hover{
    background:#ff1f2d;
    transform:scale(1.02);
}

/* Cards */
.movie-card{
    background:#181c24;
    border-radius:18px;
    padding:12px;
    transition:0.3s;
    border:1px solid rgba(255,255,255,0.05);
    height:100%;
}

.movie-card:hover{
    transform:translateY(-6px);
    box-shadow:0 10px 25px rgba(255,255,255,0.08);
}

/* Poster */
.movie-card img{
    border-radius:14px;
}

/* Title */
.movie-title{
    color:white;
    font-size:15px;
    font-weight:600;
    text-align:center;
    margin-top:10px;
    min-height:40px;
}

/* Muted text */
.small-muted{
    color:#9ca3af;
}

/* Hero */
.hero{
    background:linear-gradient(to right,#111,#1f1f1f);
    padding:40px;
    border-radius:24px;
    margin-bottom:25px;
}

/* Genre Chips */
.genre-chip{
    display:inline-block;
    background:#222;
    padding:6px 12px;
    border-radius:20px;
    margin-right:6px;
    margin-bottom:6px;
    font-size:13px;
}

/* Rating Badge */
.rating{
    background:#e50914;
    padding:5px 10px;
    border-radius:12px;
    width:fit-content;
    font-size:13px;
    margin:auto;
    margin-top:8px;
}

/* Remove white space */
.block-container{
    padding-top:1rem;
    padding-bottom:2rem;
    max-width:1450px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# SESSION STATE
# =========================================================
if "view" not in st.session_state:
    st.session_state.view = "home"

if "selected_tmdb_id" not in st.session_state:
    st.session_state.selected_tmdb_id = None

# =========================================================
# ROUTING
# =========================================================
def goto_home():
    st.session_state.view = "home"
    st.rerun()

def goto_details(tmdb_id):
    st.session_state.view = "details"
    st.session_state.selected_tmdb_id = tmdb_id
    st.rerun()

# =========================================================
# API HELPERS
# =========================================================
@st.cache_data(ttl=60)
def api_get_json(path, params=None):

    try:
        r = requests.get(
            f"{API_BASE}{path}",
            params=params,
            timeout=25
        )

        if r.status_code >= 400:
            return None, f"HTTP {r.status_code}"

        return r.json(), None

    except Exception as e:
        return None, str(e)

# =========================================================
# CARD GRID
# =========================================================
def poster_grid(cards, cols=5, key_prefix="grid"):

    if not cards:
        st.info("No movies found.")
        return

    rows = (len(cards) + cols - 1) // cols

    idx = 0

    for r in range(rows):

        colset = st.columns(cols)

        for c in range(cols):

            if idx >= len(cards):
                break

            movie = cards[idx]
            idx += 1

            with colset[c]:

                st.markdown(
                    '<div class="movie-card">',
                    unsafe_allow_html=True
                )

                if movie.get("poster_url"):
                    st.image(
                        movie["poster_url"],
                        
                    )

                st.markdown(
                    f"""
                    <div class="movie-title">
                        {movie.get("title")}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                rating = movie.get("vote_average")

                if rating:
                    st.markdown(
                        f"""
                        <div class="rating">
                            ⭐ {rating}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                if st.button(
                    "View Details",
                    key=f"{key_prefix}_{idx}"
                ):
                    goto_details(movie["tmdb_id"])

                st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3418/3418886.png",
        width=90
    )

    st.markdown("# CineMatch AI")

    st.markdown("---")

    if st.button("🏠 Home"):
        goto_home()

    st.markdown("### Categories")

    home_category = st.selectbox(
        "Browse",
        [
            "trending",
            "popular",
            "top_rated",
            "now_playing",
            "upcoming"
        ]
    )

    grid_cols = st.slider(
        "Grid Columns",
        4,
        8,
        5
    )

# =========================================================
# HERO SECTION
# =========================================================
st.markdown("""
<div class="hero">

<h1 style="font-size:52px;color:white;">
🎬 CineMatch AI
</h1>

<p style="font-size:18px;color:#b3b3b3;">
Discover movies powered by Machine Learning,
TF-IDF similarity & TMDB recommendations.
</p>

</div>
""", unsafe_allow_html=True)

# =========================================================
# HOME VIEW
# =========================================================
if st.session_state.view == "home":

    typed = st.text_input(
        "Search Movies",
        placeholder="Search: Interstellar, Batman, Avengers..."
    )

    st.divider()

    # =====================================================
    # SEARCH RESULTS
    # =====================================================
    if typed.strip():

        with st.spinner("Searching movies..."):

            data, err = api_get_json(
                "/tmdb/search",
                {"query": typed}
            )

        if err:
            st.error(err)

        elif isinstance(data, dict):

            results = data.get("results", [])

            cards = []

            for m in results:

                poster = None

                if m.get("poster_path"):
                    poster = f"{TMDB_IMG}{m['poster_path']}"

                cards.append({
                    "tmdb_id": m.get("id"),
                    "title": m.get("title"),
                    "poster_url": poster,
                    "vote_average": m.get("vote_average")
                })

            st.markdown("## 🔍 Search Results")

            poster_grid(
                cards,
                cols=grid_cols,
                key_prefix="search"
            )

    # =====================================================
    # HOME FEED
    # =====================================================
    else:

        st.markdown(
            f"## 🔥 {home_category.replace('_',' ').title()}"
        )

        with st.spinner("Loading movies..."):

            home_cards, err = api_get_json(
                "/home",
                {
                    "category": home_category,
                    "limit": 24
                }
            )

        if err:
            st.error(err)

        else:
            poster_grid(
                home_cards,
                cols=grid_cols,
                key_prefix="home"
            )

# =========================================================
# DETAILS VIEW
# =========================================================
elif st.session_state.view == "details":

    tmdb_id = st.session_state.selected_tmdb_id

    if not tmdb_id:
        st.warning("No movie selected.")
        st.stop()

    if st.button("⬅ Back"):
        goto_home()

    # =====================================================
    # MOVIE DETAILS
    # =====================================================
    with st.spinner("Loading details..."):

        data, err = api_get_json(
            f"/movie/id/{tmdb_id}"
        )

    if err or not data:
        st.error("Could not load movie.")
        st.stop()

    # =====================================================
    # BACKDROP HERO
    # =====================================================
    if data.get("backdrop_url"):

        st.markdown(
            f"""
            <div style="
            background-image:url('{data['backdrop_url']}');
            height:420px;
            background-size:cover;
            border-radius:24px;
            position:relative;
            overflow:hidden;
            ">

            <div style="
            position:absolute;
            bottom:0;
            width:100%;
            padding:30px;
            background:linear-gradient(
                transparent,
                rgba(0,0,0,0.95)
            );
            ">

            <h1 style="color:white;font-size:52px;">
            {data.get('title')}
            </h1>

            </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    left, right = st.columns([1, 2])

    # =====================================================
    # POSTER
    # =====================================================
    with left:

        if data.get("poster_url"):
            st.image(
                data["poster_url"],
                
            )

    # =====================================================
    # INFO
    # =====================================================
    with right:

        st.markdown(f"# {data.get('title')}")

        st.markdown(
            f"""
            <div class="small-muted">
            Release Date: {data.get('release_date')}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        # Genres
        genres_html = ""

        for g in data.get("genres", []):

            genres_html += f"""
            <span class="genre-chip">
                {g['name']}
            </span>
            """

        st.markdown(
            genres_html,
            unsafe_allow_html=True
        )

        st.write("")

        rating = data.get("vote_average")

        if rating:
            st.markdown(
                f"""
                <div class="rating">
                    ⭐ {rating}
                </div>
                """,
                unsafe_allow_html=True
            )

        st.write("")

        st.markdown("## Overview")

        st.write(
            data.get("overview")
            or "No overview available."
        )

    st.divider()

    # =====================================================
    # RECOMMENDATIONS
    # =====================================================
    st.markdown("## ✅ Recommendations")

    with st.spinner("Generating recommendations..."):

        bundle, err = api_get_json(
            "/movie/search",
            {
                "query": data.get("title"),
                "tfidf_top_n": 12,
                "genre_limit": 12
            }
        )

    if bundle:

        tab1, tab2 = st.tabs([
            "🔎 Similar Movies",
            "🎭 Genre Based"
        ])

        # =================================================
        # TFIDF
        # =================================================
        with tab1:

            cards = []

            for x in bundle.get(
                "tfidf_recommendations",
                []
            ):

                tmdb = x.get("tmdb") or {}

                cards.append({
                    "tmdb_id": tmdb.get("tmdb_id"),
                    "title": tmdb.get("title"),
                    "poster_url": tmdb.get("poster_url"),
                    "vote_average": tmdb.get("vote_average")
                })

            poster_grid(
                cards,
                cols=grid_cols,
                key_prefix="tfidf"
            )

        # =================================================
        # GENRE
        # =================================================
        with tab2:

            poster_grid(
                bundle.get(
                    "genre_recommendations",
                    []
                ),
                cols=grid_cols,
                key_prefix="genre"
            )

    else:
        st.warning("No recommendations available.")

# =========================================================
# FOOTER
# =========================================================
st.divider()

st.markdown("""
<center>

<p style='color:gray;'>

Built with ❤️ using
FastAPI • Streamlit • TMDB • Machine Learning

</p>

</center>
""", unsafe_allow_html=True)