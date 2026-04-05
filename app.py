import streamlit as st
import pickle
import pandas as pd
import numpy as np
import re

st.set_page_config(
    page_title="Job Intelligence System",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: #080c14 !important;
    color: #c8cdd8 !important;
    font-family: 'Syne', sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 0%, #0d1a2e 0%, #080c14 60%) !important;
}

[data-testid="stHeader"] { background: transparent !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #0b1120 !important;
    border-right: 1px solid #1a2540 !important;
}
[data-testid="stSidebar"] > div { padding: 2rem 1.2rem !important; }
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label {
    color: #7a8aaa !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.72rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
}
[data-testid="stSidebar"] .stCheckbox label {
    color: #a0aec0 !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.04em !important;
    text-transform: none !important;
}
[data-testid="stSidebar"] .stCheckbox > label > div {
    background: transparent !important;
    border-color: #2a3a5c !important;
}
[data-testid="stSidebar"] [data-testid="stCheckbox"] input:checked + div {
    background: #c9a84c !important;
    border-color: #c9a84c !important;
}
.sidebar-logo {
    font-family: 'Space Mono', monospace;
    font-size: 1rem;
    font-weight: 700;
    color: #c9a84c;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    padding-bottom: 1.5rem;
    border-bottom: 1px solid #1a2540;
    margin-bottom: 1.8rem;
}
.sidebar-section-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #3a4a6a;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin: 1.4rem 0 0.6rem 0;
}

/* ── HERO ── */
.hero-wrap {
    border: 1px solid #1a2540;
    border-radius: 16px;
    padding: 2.8rem 3rem;
    background: linear-gradient(135deg, #0d1a2e 0%, #080c14 100%);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 260px; height: 260px;
    background: radial-gradient(circle, rgba(201,168,76,0.1) 0%, transparent 70%);
    pointer-events: none;
}
.hero-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.22em;
    color: #c9a84c;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    color: #eef1f7;
    line-height: 1.1;
    letter-spacing: -0.02em;
    margin-bottom: 0.5rem;
}
.hero-title span { color: #c9a84c; }
.hero-sub {
    font-size: 0.85rem;
    color: #5a6a8a;
    letter-spacing: 0.02em;
    font-family: 'Space Mono', monospace;
    margin-bottom: 1.2rem;
}
.hero-owner {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    letter-spacing: 0.1em;
    color: #3a4a6a;
    text-transform: uppercase;
}
.hero-owner span { color: #c9a84c; opacity: 0.8; }

/* ── KPI CARDS ── */
.kpi-card {
    background: #0d1a2e;
    border: 1px solid #1a2540;
    border-radius: 14px;
    padding: 1.5rem 1.6rem;
    position: relative;
    overflow: hidden;
}
.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    background: #c9a84c;
    border-radius: 2px 0 0 2px;
}
.kpi-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.18em;
    color: #4a5a7a;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #eef1f7;
    line-height: 1;
}
.kpi-icon {
    position: absolute;
    top: 1.2rem; right: 1.4rem;
    font-size: 1.3rem;
    opacity: 0.2;
}

/* ── SECTION HEADER ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-bottom: 1.4rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #111e33;
}
.section-icon {
    width: 34px; height: 34px;
    background: rgba(201,168,76,0.08);
    border: 1px solid rgba(201,168,76,0.2);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.95rem;
    flex-shrink: 0;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.05rem;
    font-weight: 700;
    color: #dde3f0;
    letter-spacing: 0.01em;
}
.section-badge {
    margin-left: auto;
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.12em;
    color: #c9a84c;
    background: rgba(201,168,76,0.07);
    border: 1px solid rgba(201,168,76,0.18);
    border-radius: 20px;
    padding: 0.2rem 0.65rem;
    text-transform: uppercase;
    white-space: nowrap;
}

/* ── INPUTS ── */
[data-testid="stTextInput"] input {
    background: #060a10 !important;
    border: 1px solid #1a2540 !important;
    border-radius: 10px !important;
    color: #c8cdd8 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
    padding: 0.7rem 1rem !important;
    transition: border-color 0.2s, box-shadow 0.2s;
}
[data-testid="stTextInput"] input:focus {
    border-color: #c9a84c !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.08) !important;
}
[data-testid="stTextInput"] input::placeholder { color: #2a3a5a !important; }
[data-testid="stTextInput"] label {
    color: #5a6a8a !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* ── SELECT ── */
[data-testid="stSelectbox"] > div > div {
    background: #060a10 !important;
    border: 1px solid #1a2540 !important;
    border-radius: 10px !important;
    color: #c8cdd8 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.82rem !important;
}
[data-testid="stSelectbox"] label {
    color: #5a6a8a !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* ── BUTTON ── */
[data-testid="stButton"] > button {
    background: #c9a84c !important;
    color: #060a10 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.88rem !important;
    letter-spacing: 0.06em !important;
    padding: 0.75rem 2rem !important;
    height: auto !important;
    transition: all 0.2s !important;
    text-transform: uppercase !important;
}
[data-testid="stButton"] > button:hover {
    background: #dbb85a !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 22px rgba(201,168,76,0.28) !important;
}

/* ── ALERTS ── */
[data-testid="stSuccess"] {
    background: rgba(52,211,153,0.05) !important;
    border: 1px solid rgba(52,211,153,0.15) !important;
    border-radius: 10px !important;
    color: #6ee7b7 !important;
}
[data-testid="stError"] {
    background: rgba(239,68,68,0.05) !important;
    border: 1px solid rgba(239,68,68,0.15) !important;
    border-radius: 10px !important;
    color: #fca5a5 !important;
}
[data-testid="stWarning"] {
    background: rgba(251,191,36,0.05) !important;
    border: 1px solid rgba(251,191,36,0.15) !important;
    border-radius: 10px !important;
}

/* ── ROLE RESULT CARD ── */
.role-result-card {
    background: #060a10;
    border: 1px solid #1a2540;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.8rem;
    position: relative;
    overflow: hidden;
}
.role-result-card.top-pick {
    border-color: rgba(201,168,76,0.38);
    background: linear-gradient(135deg, #0d1a2e 0%, #060a10 100%);
}
.role-result-card.top-pick::before {
    content: 'BEST MATCH';
    position: absolute;
    top: 0.55rem; right: 0.8rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.12em;
    color: #c9a84c;
    background: rgba(201,168,76,0.1);
    border: 1px solid rgba(201,168,76,0.25);
    border-radius: 20px;
    padding: 0.12rem 0.5rem;
}
.role-rank {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #3a4a6a;
    letter-spacing: 0.1em;
    margin-bottom: 0.3rem;
}
.role-name {
    font-family: 'Syne', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    color: #dde3f0;
    margin-bottom: 0.65rem;
}
.role-bar-track {
    width: 100%;
    height: 6px;
    background: #111e33;
    border-radius: 3px;
    margin-bottom: 0.45rem;
    overflow: hidden;
}
.role-bar-fill {
    height: 6px;
    border-radius: 3px;
}
.role-pct-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.role-pct {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #c9a84c;
}
.role-confidence {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #3a4a6a;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── SKILL CHIPS ── */
.skill-chip-wrap { display: flex; flex-wrap: wrap; gap: 0.45rem; margin-top: 0.3rem; }
.skill-chip {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #7a8aaa;
    background: #060a10;
    border: 1px solid #1a2540;
    border-radius: 20px;
    padding: 0.28rem 0.8rem;
}
.skill-chip-missing {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    color: #c9a84c;
    background: rgba(201,168,76,0.05);
    border: 1px solid rgba(201,168,76,0.22);
    border-radius: 20px;
    padding: 0.28rem 0.8rem;
}

/* ── LEARNING CUSTOM BARS ── */
.learn-row {
    display: flex;
    align-items: center;
    gap: 0.8rem;
    padding: 0.65rem 0;
    border-bottom: 1px solid #0d1626;
}
.learn-row:last-child { border-bottom: none; }
.learn-rank {
    font-family: 'Space Mono', monospace;
    font-size: 0.6rem;
    color: #2a3a5a;
    width: 1.4rem;
    flex-shrink: 0;
    text-align: right;
}
.learn-name {
    font-family: 'Syne', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    color: #c8cdd8;
    width: 130px;
    flex-shrink: 0;
}
.learn-bar-track {
    flex: 1;
    height: 7px;
    background: #0d1626;
    border-radius: 4px;
    overflow: hidden;
}
.learn-bar-fill {
    height: 7px;
    border-radius: 4px;
}
.learn-count {
    font-family: 'Space Mono', monospace;
    font-size: 0.62rem;
    color: #4a5a7a;
    width: 3.2rem;
    text-align: right;
    flex-shrink: 0;
}

/* ── TIP ITEMS ── */
.tip-item {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    padding: 0.75rem 0;
    border-bottom: 1px solid #111e33;
    font-size: 0.88rem;
    color: #8a9ab8;
    font-family: 'Syne', sans-serif;
}
.tip-item:last-child { border-bottom: none; }
.tip-dot {
    width: 6px; height: 6px;
    background: #c9a84c;
    border-radius: 50%;
    margin-top: 0.42rem;
    flex-shrink: 0;
}

/* ── SUB LABEL ── */
.sub-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.14em;
    color: #4a5a7a;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* ── HINT BOX ── */
.hint-box {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #4a5a7a;
    margin-bottom: 1rem;
    padding: 0.75rem 1rem;
    background: #060a10;
    border: 1px solid #1a2540;
    border-radius: 10px;
    letter-spacing: 0.04em;
    line-height: 1.8;
}

/* ── FOOTER ── */
.footer-strip {
    margin-top: 3rem;
    padding: 1.2rem 0;
    border-top: 1px solid #111e33;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.footer-left {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.12em;
    color: #2a3a5a;
    text-transform: uppercase;
}
.footer-right {
    font-family: 'Space Mono', monospace;
    font-size: 0.65rem;
    color: #c9a84c;
    opacity: 0.5;
}

#MainMenu, footer, header { visibility: hidden !important; }
[data-testid="stDecoration"] { display: none !important; }
.stDeployButton { display: none !important; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD MODEL
# -----------------------------
@st.cache_resource
def load_model():
    with open("career_role_model.pkl", "rb") as f:
        model = pickle.load(f)

    with open("tfidf_vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)

    return model, vectorizer

model, vectorizer = load_model()

# -----------------------------
# LOAD DATA
# -----------------------------
@st.cache_data
def load_data():
    role_skill_df = pd.read_csv("data/role_wise_skills.csv")
    skills_df = pd.read_csv("data/top_skills_frequency.csv")
    fresher_df = pd.read_csv("data/fresher_jobs_dataset.csv")
    job_df = pd.read_csv("data/naukri_jobs_dataset.csv")
    return role_skill_df, skills_df, fresher_df, job_df

role_skill_df, skills_df, fresher_df, job_df = load_data()

# -----------------------------
# CLEAN COLUMN NAMES
# -----------------------------
role_skill_df.columns = role_skill_df.columns.str.strip().str.lower()
skills_df.columns = skills_df.columns.str.strip().str.lower()
fresher_df.columns = fresher_df.columns.str.strip().str.lower()
job_df.columns = job_df.columns.str.strip().str.lower()

# -----------------------------
# BUILD ROLE -> SKILLS MAP
# -----------------------------
top_skills_per_role = {}

for role in role_skill_df["search_role"].dropna().unique():
    top_skills = (
        role_skill_df[role_skill_df["search_role"] == role]["skill"]
        .dropna()
        .astype(str)
        .str.lower()
        .value_counts()
        .head(15)
        .index
        .tolist()
    )
    top_skills_per_role[role] = top_skills

# -----------------------------
# BUILD VALID SKILLS LIST
# -----------------------------
VALID_SKILLS = set(role_skill_df["skill"].dropna().astype(str).str.lower().str.strip().unique())

# -----------------------------
# FUNCTIONS
# -----------------------------
def clean_and_validate_skills(user_input):
    if not user_input or user_input.strip() == "":
        return False, " Please enter at least one skill."

    cleaned = user_input.lower().strip()
    skills = [s.strip() for s in cleaned.split(",") if s.strip()]

    if len(skills) == 0:
        return False, "Please enter valid skills separated by commas."

    # reject meaningless symbols/numbers only
    valid_text_skills = []
    for s in skills:
        if re.search(r"[a-zA-Z]", s):
            valid_text_skills.append(s)

    if len(valid_text_skills) == 0:
        return False, " Please enter meaningful skill names."

    matched_skills = [s for s in valid_text_skills if s in VALID_SKILLS]

    if len(matched_skills) == 0:
        return False, "No valid matching skills found in dataset. Try python, sql, machine learning."

    return True, matched_skills


def predict_top_roles(skills_input, top_n=3):
    skills_vector = vectorizer.transform([skills_input])
    probs = model.predict_proba(skills_vector)[0]
    top_indices = np.argsort(probs)[::-1][:top_n]
    return [(model.classes_[i], probs[i]) for i in top_indices]


def recommend_missing_skills(user_skills, role):
    user_skills = [s.strip().lower() for s in user_skills.split(",")]
    role_skills = top_skills_per_role.get(role, [])
    return [s for s in role_skills if s not in user_skills][:10]


def extract_top_items(df, column_name, top_n=15):
    if column_name not in df.columns:
        return pd.Series(dtype=int)
    return df[column_name].dropna().astype(str).value_counts().head(top_n)


# -----------------------------
# HEADER
# -----------------------------
st.markdown("""
<div class="hero-wrap">
    <div class="hero-label">◈ Intelligence Platform · v1.0</div>
    <div class="hero-title">Job<br><span>Intelligence System</span></div>
    <div class="hero-sub">Predict roles · Identify skill gaps · Explore market signals</div>
    <div class="hero-owner">Crafted by &nbsp;<span>Katheeja</span></div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("Insights Panel")

show_prediction = st.sidebar.checkbox("Career Prediction", value=True, key="career_prediction")
show_skills = st.sidebar.checkbox("Top Skills", key="top_skills")
show_roles = st.sidebar.checkbox("Top Roles", key="top_roles")
show_companies = st.sidebar.checkbox("Top Companies", key="top_companies")
show_locations = st.sidebar.checkbox("Top Locations", key="top_locations")
show_fresher = st.sidebar.checkbox("Fresher Opportunities", key="fresher_opportunities")
show_role_skills = st.sidebar.checkbox("Skills by Role", key="skills_by_role")
show_learning = st.sidebar.checkbox("Learning Suggestions", key="learning_suggestions")
show_tips = st.sidebar.checkbox("Career Tips", key="career_tips")

# -----------------------------
# TOP METRICS
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Unique Roles", role_skill_df["search_role"].nunique())

with col2:
    st.metric("Unique Skills", role_skill_df["skill"].nunique())

with col3:
    st.metric("Fresher Jobs", len(fresher_df))

# -----------------------------
# CAREER PREDICTION SECTION
# -----------------------------
if show_prediction:
    st.markdown("---")
    st.subheader("Career Role Predictor")

    user_input = st.text_input(
        "Enter your skills (comma separated)",
        placeholder="Example: python, sql, machine learning"
    )

    if st.button("Predict Career Path"):
        is_valid, result = clean_and_validate_skills(user_input)

        if not is_valid:
            st.error(result)
        else:
            cleaned_skills = ", ".join(result)
            results = predict_top_roles(cleaned_skills)

            # st.success(f"✅ Valid skills detected: {cleaned_skills}")

            st.subheader(" Recommended Roles")
            for role, score in results:
                st.write(f"**{role}** → {round(score * 100, 2)}%")

            best_role = results[0][0]

            st.subheader(f" Skills to Improve for {best_role}")
            missing = recommend_missing_skills(cleaned_skills, best_role)

            if missing:
                for skill in missing:
                    st.write(f"- {skill}")
            else:
                st.success("You already have most of the important skills for this role.")

# -----------------------------
# TOP SKILLS
# -----------------------------
if show_skills:
    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="section-title">Top 20 In-Demand Skills</div>
    </div>""", unsafe_allow_html=True)
    if "skill" in skills_df.columns:
        st.bar_chart(skills_df.head(20).set_index("skill"), color="#544cc9")
    else:
        st.warning("No 'skill' column found in top_skills_frequency.csv")


# -----------------------------
# TOP ROLES
# -----------------------------
if show_roles:
    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="section-title">Top 15 Job Roles</div>
    </div>""", unsafe_allow_html=True)
    st.bar_chart(role_skill_df["search_role"].value_counts().head(15), color="#c94c4c")
# -----------------------------
# TOP COMPANIES
# -----------------------------
if show_companies:
    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="section-icon"></div>
        <div class="section-title">Top Hiring Companies</div>
        <div class="section-badge">Fresher Market</div>
    </div>""", unsafe_allow_html=True)
    company_counts = extract_top_items(job_df, "company_name", 15)
    if not company_counts.empty:
        st.bar_chart(company_counts, color="#4cc94c")
    else:
        st.warning("No 'company' column found in fresher_jobs_dataset.csv")
# -----------------------------
# TOP LOCATIONS

if show_locations:
    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="section-icon"></div>
        <div class="section-title">Top Hiring Locations</div>
        <div class="section-badge">Geo Distribution</div>
    </div>""", unsafe_allow_html=True)
    location_counts = extract_top_items(fresher_df, "location", 15)
    if not location_counts.empty:
        st.bar_chart(location_counts, color="#a34cc9")
    else:
        st.warning("No 'location' column found in fresher_jobs_dataset.csv")

# -----------------------------
# FRESHER OPPORTUNITIES
# -----------------------------
if show_fresher:
    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="section-icon">🎓</div>
        <div class="section-title">Fresher Market Opportunities</div>
        <div class="section-badge">Entry Level</div>
    </div>""", unsafe_allow_html=True)
    fc1, fc2 = st.columns(2)
    with fc1:
        if "search_role" in fresher_df.columns:
            st.markdown('<div class="sub-label">Top Roles</div>', unsafe_allow_html=True)
            st.bar_chart(fresher_df["search_role"].value_counts().head(10), color="#544cc9")
    with fc2:
        if "skills" in fresher_df.columns:
            st.markdown('<div class="sub-label">Top Skills</div>', unsafe_allow_html=True)
            fresher_skills = fresher_df["skills"].dropna().astype(str).str.lower().str.split(",")
            flat = [s.strip() for sub in fresher_skills for s in sub if s.strip()]
            st.bar_chart(pd.Series(flat).value_counts().head(15), color="#4c6bc9")


# -----------------------------
# SKILLS BY ROLE
# -----------------------------
if show_role_skills:
    st.markdown("---")
    st.subheader(" Skills Required per Role")

    selected_role = st.selectbox(
        "Select a role",
        sorted(role_skill_df["search_role"].dropna().unique())
    )

    role_skills = (
        role_skill_df[role_skill_df["search_role"] == selected_role]["skill"]
        .dropna()
        .astype(str)
        .str.lower()
        .value_counts()
        .head(15)
    )

    st.write(f"### Top Skills for {selected_role}")
    st.bar_chart(role_skills)

# -----------------------------
# LEARNING SUGGESTIONS
# -----------------------------
if show_learning:
    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    # st.markdown("""
    # <div class="section-header">
    #     <div class="section-icon"></div>
    #     <div class="section-title">Market Trending Skills to Learn</div>
    #     <div class="section-badge">Growth Map</div>
    # </div>""", unsafe_allow_html=True)

    trending_skills = role_skill_df["skill"].dropna().astype(str).str.lower().value_counts().head(15)
    max_val = trending_skills.max()

    bar_palette = [
        "#c9a84c","#d4b05e","#deb870","#e8c080","#f0c878",
        "#4a8ac4","#5a9ad4","#3a7ab4","#6aaae4","#2a6aa4",
        "#7a5ac4","#9a7ae4","#5a7a9a","#8a9aba","#aabada",
    ]
    st.markdown('<div class="sub-label">Frequency Chart</div>', unsafe_allow_html=True)
    st.bar_chart(trending_skills, color="#4cc95b")

# -----------------------------
# CAREER TIPS
# -----------------------------
if show_tips:
    st.markdown("<div style='height:0.6rem'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="section-header">
        <div class="section-icon"></div>
        <div class="section-title">Career Growth Playbook</div>
        <div class="section-badge">Strategy</div>
    </div>""", unsafe_allow_html=True)

    tips = [
        ("Foundation", "Master SQL + Python + Excel as your non-negotiable core stack."),
        ("Portfolio", "Build 2–3 end-to-end projects that solve real-world problems."),
        ("Visualization", "Add Power BI or Tableau to stand out in analytics roles."),
        ("ML Depth", "Learn Machine Learning fundamentals for data science tracks."),
        ("Resume", "Tailor your resume per job description — keywords matter a lot."),
        ("Entry Points", "Target internships and fresher openings aggressively early."),
        ("Presence", "Optimize your GitHub and LinkedIn — recruiters check both."),
    ]
    tips_html = "".join([
        f'<div class="tip-item"><div class="tip-dot"></div>'
        f'<div><strong style="color:#c9a84c;font-size:0.78rem">{t}</strong>&nbsp;&nbsp;{d}</div></div>'
        for t, d in tips
    ])
    st.markdown(tips_html, unsafe_allow_html=True)

# -----------------------------
# FOOTER
# -----------------------------
st.markdown("""
<style>
.footer-strip {
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    width: 100%;
}
</style>

<div class="footer-strip">
    Job Intelligence System · Katheeja Builds · Built with Streamlit <br>
            ◈ JIS v1.0<br>
</div>
""", unsafe_allow_html=True)