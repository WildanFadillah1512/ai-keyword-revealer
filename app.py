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

    /* --- SIDEBAR STYLING (THE CONTROLLER) --- */
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
        border-radius: 4px;
    }
    .stTextInput input {
        color: #00eeff !important;
        font-family: 'Share Tech Mono', monospace;
    }

    /* BUTTON */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #0055aa, #0088cc);
        border: none;
        color: white;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 2px;
        padding: 12px;
        margin-top: 10px;
        transition: 0.3s;
    }
    .stButton > button:hover {
        box-shadow: 0 0 15px #0088cc;
        transform: scale(1.02);
    }

    /* --- DASHBOARD GRID --- */
    
    /* METRIC BOXES (TOP ROW) */
    .metric-box {
        background: rgba(0, 20, 40, 0.5);
        border: 1px solid #112233;
        padding: 15px;
        text-align: center;
        border-radius: 4px;
    }
    .metric-val { font-size: 24px; color: #fff; font-weight: bold; }
    .metric-lbl { font-size: 10px; color: #557799; letter-spacing: 1px; }

    /* PANEL CONTAINERS */
    .panel-container {
        background: #030405;
        border: 1px solid #1f293a;
        height: 600px; /* Fixed Height */
        position: relative;
        overflow: hidden;
        margin-top: 10px;
    }
    
    .panel-header {
        background: #0a0e14;
        padding: 8px 15px;
        border-bottom: 1px solid #1f293a;
        font-size: 12px;
        color: #446688;
        display: flex;
        justify-content: space-between;
        font-family: 'Orbitron', sans-serif;
    }

    /* CHAOS LOG (LEFT) */
    .chaos-log {
        padding: 20px;
        height: 550px;
        overflow-y: auto;
        font-size: 11px;
        color: #00ffaa;
        line-height: 1.6;
        opacity: 0.8;
    }

    /* RESULT CARDS (RIGHT) */
    .result-grid {
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .data-card {
        background: linear-gradient(90deg, rgba(0,0,0,0), rgba(0,100,255,0.05));
        border-left: 3px solid #0088cc;
        padding: 15px;
        position: relative;
    }
    .data-card:hover {
        background: rgba(0,100,255,0.1);
        border-left: 3px solid #fff;
    }
    .data-title { font-size: 10px; color: #0088cc; margin-bottom: 5px; text-transform: uppercase;}
    .data-content { font-size: 14px; color: #fff; }

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
    system_prompt = """
    ROLE: Orbital AI Core.
    TASK: Analyze input. Output raw, messy, technical thought process.
    LANG: Mix English (Technical) and Indonesian (Reasoning). "Jaksel" Cyberpunk style.
    OUTPUT: Continuous text block.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
        temperature=0.8, max_tokens=1000
    )
    return response.choices[0].message.content

def distill_strategy(raw_text):
    system_prompt = """
    ROLE: Tactical Extractor.
    TASK: Get 3 top search queries.
    OUTPUT: JSON {"candidates": ["q1", "q2", "q3"]}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": raw_text}],
        temperature=0.1, response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

# --- 4. LAYOUT CONSTRUCTION ---

# === SIDEBAR (CONTROLLER) ===
with st.sidebar:
    st.markdown('<div class="sidebar-header">/// ORBITAL</div>', unsafe_allow_html=True)
    
    st.markdown("PARAMETER INPUT")
    user_query = st.text_input("..", placeholder="Inject Command...", label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("SYSTEM SETTINGS")
    temp = st.slider("Chaos Level", 0.0, 1.0, 0.8)
    
    st.markdown("---")
    run_btn = st.button("INITIALIZE SEQUENCE")
    
    if not run_btn:
        st.markdown("""
        <div style='margin-top: 50px; font-size: 10px; color: #445566;'>
        STATUS: STANDBY<br>
        UPLINK: SECURE<br>
        V.3.1.0
        </div>
        """, unsafe_allow_html=True)

# === MAIN DASHBOARD ===

# 1. TOP METRICS ROW (Visual Candy)
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-box"><div class="metric-val">{random.randint(20,40)}ms</div><div class="metric-lbl">LATENCY</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-box"><div class="metric-val">{random.randint(800,999)}TB</div><div class="metric-lbl">BANDWIDTH</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-box"><div class="metric-val">{random.randint(95,100)}%</div><div class="metric-lbl">INTEGRITY</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-box"><div class="metric-val">ACTV</div><div class="metric-lbl">CORE STATUS</div></div>', unsafe_allow_html=True)

# 2. MAIN SPLIT SCREEN
c_chaos, c_results = st.columns([1.2, 1])

if run_btn and user_query:
    with st.spinner("PROCESSING..."):
        # Logic
        raw_stream = get_chaos_stream(user_query)
        json_res = distill_strategy(raw_stream)
        try:
            candidates = json.loads(json_res).get("candidates", [])
        except:
            candidates = ["DATA CORRUPTED", "RETRY"]
            
    # LEFT PANEL: CHAOS
    with c_chaos:
        st.markdown(f"""
        <div class="panel-container">
            <div class="panel-header">
                <span>RAW_STREAM_LOG</span>
                <span>ID: {random.randint(1000,9999)}</span>
            </div>
            <div class="chaos-log">
                > INCOMING_TRANSMISSION...<br>
                > DECODING...<br><br>
                {raw_stream}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # RIGHT PANEL: RESULTS
    with c_results:
        # Build the HTML for cards
        cards_html = ""
        for i, item in enumerate(candidates):
            cards_html += f"""
            <div class="data-card">
                <div class="data-title">VECTOR 0{i+1} // CONFIDENCE {random.randint(90,99)}%</div>
                <div class="data-content">{item}</div>
            </div>
            """
            
        st.markdown(f"""
        <div class="panel-container">
            <div class="panel-header">
                <span>TARGET_ACQUISITION</span>
                <span>COUNT: {len(candidates)}</span>
            </div>
            <div class="result-grid">
                {cards_html}
            </div>
             <div style="position: absolute; bottom: 10px; right: 10px; font-size: 90px; color: rgba(255,255,255,0.02); pointer-events: none;">
                0{len(candidates)}
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    # IDLE STATE (Empty Dashboard)
    with c_chaos:
        st.markdown("""
        <div class="panel-container" style="display: flex; align-items: center; justify-content: center; opacity: 0.5;">
            <div>AWAITING INPUT DATA...</div>
        </div>
        """, unsafe_allow_html=True)
    with c_results:
         st.markdown("""
        <div class="panel-container" style="display: flex; align-items: center; justify-content: center; opacity: 0.5;">
            <div>NO TARGETS</div>
        </div>
        """, unsafe_allow_html=True)
