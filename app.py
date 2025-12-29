import streamlit as st
from groq import Groq
import json
import time
import random

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="ORBITAL COMMAND", 
    page_icon="🛰️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. THE "ORBITAL GRID" CSS ---
st.markdown("""
<style>
    /* IMPORTS */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

    /* BASE */
    .stApp {
        background-color: #020204;
        color: #aaccff;
        font-family: 'Share Tech Mono', monospace;
    }
    
    /* HIDE DEFAULT UI */
    header, footer, .stDeployButton {display: none;}
    div[data-testid="stDecoration"] {display: none;}

    /* --- SIDEBAR STYLING --- */
    section[data-testid="stSidebar"] {
        background-color: #050508;
        border-right: 1px solid #1f293a;
    }
    
    .sidebar-header {
        font-family: 'Orbitron', sans-serif;
        font-weight: 900;
        font-size: 24px;
        color: #fff;
        margin-bottom: 30px;
        text-shadow: 0 0 10px rgba(0, 150, 255, 0.5);
    }

    /* INPUT FIELD */
    .stTextInput > div > div {
        background-color: #0a0e14;
        border: 1px solid #334455;
        color: #00eeff;
        border-radius: 0px; 
    }
    .stTextInput input {
        color: #00eeff !important;
        font-family: 'Share Tech Mono', monospace;
    }

    /* BUTTON */
    .stButton > button {
        width: 100%;
        background: rgba(0, 85, 170, 0.2);
        border: 1px solid #0088cc;
        color: #00eeff;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 2px;
        padding: 15px;
        margin-top: 10px;
        transition: 0.3s;
        text-transform: uppercase;
    }
    .stButton > button:hover {
        background: #0088cc;
        color: #fff;
        box-shadow: 0 0 20px rgba(0, 136, 204, 0.6);
    }

    /* --- DASHBOARD GRID --- */
    .metric-box {
        background: rgba(0, 20, 30, 0.5);
        border: 1px solid #1f293a;
        padding: 10px;
        text-align: center;
        border-radius: 0px;
    }
    .metric-val { font-size: 20px; color: #fff; font-weight: bold; font-family: 'Orbitron'; }
    .metric-lbl { font-size: 10px; color: #557799; letter-spacing: 1px; }

    .chaos-text {
        color: #00ffaa;
        font-size: 11px;
        line-height: 1.6;
        opacity: 0.9;
        white-space: pre-wrap;
    }

    .query-card {
        background: rgba(0, 255, 170, 0.05);
        border: 1px solid #1f293a;
        padding: 10px;
        margin-bottom: 10px;
        border-left: 2px solid #00ffaa;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC ---
try:
    if "GROQ_API_KEY" in st.secrets:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    else:
        st.sidebar.error("⚠️ API Key Missing")
        st.stop()
except:
    st.stop()

def get_chaos_stream(user_input):
    # PROMPT LOGIKA MURNI (Kiri)
    system_prompt = """
    You are a hyper-analytical AI engine performing a Deep Layer Cognition Trace.
    Provide an exhaustive, step-by-step, unfiltered breakdown of your reasoning process.
    Structure:
    1. Semantic Deconstruction (tokens, intent).
    2. Knowledge Retrieval (related nodes/concepts).
    3. Multi-angle Hypothesis Formation.
    4. Dialectical Analysis (self-critique of hypotheses).
    5. Convergence Logic.
    
    STYLE: Clinical, verbose, and purely technical. Show all internal steps.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
        temperature=0.7,
        max_tokens=2048
    )
    return response.choices[0].message.content

def distill_strategy(raw_text):
    # PROMPT EKSTRAKSI SEARCH QUERY (Kanan)
    system_prompt = """
    ROLE: Intelligence Liaison.
    TASK: Based on the provided raw cognitive analysis, generate exactly 3 to 5 highly optimized "Search Model Queries".
    
    GUIDELINES for Queries:
    1. They must be designed for deep research (e.g., Google, Perplexity, or Academic search).
    2. Use advanced operators or specific terminology found in the analysis.
    3. Each query should target a different "blind spot" or "data need" identified in the reasoning.
    4. Format: Plain, direct search strings.
    
    OUTPUT: JSON format {"candidates": ["query 1", "query 2", "query 3", "query 4", "query 5"]}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": raw_text}],
        temperature=0.2, 
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

# --- 4. LAYOUT ---

# SIDEBAR
with st.sidebar:
    st.markdown('<div class="sidebar-header">/// ORBITAL</div>', unsafe_allow_html=True)
    user_query = st.text_input("..", placeholder="Inject Command...", label_visibility="collapsed")
    st.markdown("---")
    run_btn = st.button("INITIALIZE SEQUENCE")

# METRICS
m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="metric-box"><div class="metric-val">{random.randint(12,25)}ms</div><div class="metric-lbl">LATENCY</div></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-box"><div class="metric-val">{random.randint(120,500)}TB</div><div class="metric-lbl">UPLINK</div></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="metric-box"><div class="metric-val">SECURE</div><div class="metric-lbl">PROTOCOL</div></div>', unsafe_allow_html=True)
with m4: st.markdown(f'<div class="metric-box"><div class="metric-val" style="color:#00ff41">ACTV</div><div class="metric-lbl">STATUS</div></div>', unsafe_allow_html=True)

c_chaos, c_results = st.columns([1.2, 1])

if run_btn and user_query:
    with st.spinner("TRACE IN PROGRESS..."):
        raw_stream = get_chaos_stream(user_query)
        json_res = distill_strategy(raw_stream)
        try:
            candidates = json.loads(json_res).get("candidates", [])
        except:
            candidates = ["ERROR: DECODING_FAILED"]

    # KIRI: PROSES BERPIKIR MURNI
    with c_chaos:
        st.caption("/// RAW_COGNITIVE_LOG // DEEP_TRACE_ACTIVE")
        with st.container(height=600, border=True):
            st.markdown(f'<div class="chaos-text">{raw_stream}</div>', unsafe_allow_html=True)

    # KANAN: OPTIMIZED SEARCH QUERIES
    with c_results:
        st.caption("/// SEARCH_MODEL_QUERIES // TARGET_ACQUISITION")
        with st.container(height=600, border=True):
            for i, item in enumerate(candidates):
                with st.container():
                    st.markdown(f"""
                    <div class="query-card">
                        <small style="color:#557799;">SEARCH_VECTOR_0{i+1}</small><br>
                        <code style="color:#00eeff; background:transparent;">{item}</code>
                    </div>
                    """, unsafe_allow_html=True)
                    if st.button(f"COPY QUERY 0{i+1}", key=f"btn_{i}"):
                        st.write(f"Query 0{i+1} selected.")

else:
    with c_chaos:
        st.container(height=600, border=True).markdown("<br><br><center>SYSTEM_IDLE: AWAITING_INPUT</center>", unsafe_allow_html=True)
    with c_results:
        st.container(height=600, border=True).markdown("<br><br><center>NO_VECTORS_DEFINED</center>", unsafe_allow_html=True)
