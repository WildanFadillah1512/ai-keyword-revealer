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
        border-radius: 0px; /* Sharp edges */
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
    
    /* METRIC BOXES */
    .metric-box {
        background: rgba(0, 20, 30, 0.5);
        border: 1px solid #1f293a;
        padding: 10px;
        text-align: center;
        border-radius: 0px;
        position: relative;
    }
    .metric-box::after {
        content: ''; position: absolute; bottom: 0; right: 0;
        width: 5px; height: 5px; background: #0088cc;
    }
    .metric-val { font-size: 20px; color: #fff; font-weight: bold; font-family: 'Orbitron'; }
    .metric-lbl { font-size: 10px; color: #557799; letter-spacing: 1px; }

    /* PANEL CONTAINERS */
    .panel-container {
        background: #050608;
        border: 1px solid #1f293a;
        height: 600px;
        position: relative;
        overflow-y: auto;
        margin-top: 10px;
        box-shadow: inset 0 0 50px rgba(0,0,0,0.8);
    }
    .panel-container::-webkit-scrollbar { width: 4px; }
    .panel-container::-webkit-scrollbar-track { background: #000; }
    .panel-container::-webkit-scrollbar-thumb { background: #004466; }
    
    .panel-header {
        background: linear-gradient(90deg, #0a111a, transparent);
        padding: 10px 15px;
        border-bottom: 1px solid #1f293a;
        font-size: 12px;
        color: #00eeff;
        display: flex;
        justify-content: space-between;
        font-family: 'Orbitron', sans-serif;
        letter-spacing: 1px;
        position: sticky;
        top: 0;
        z-index: 10;
        backdrop-filter: blur(5px);
    }

    /* CHAOS LOG (LEFT) */
    .chaos-log {
        padding: 20px;
        font-size: 11px;
        color: #00ffaa;
        line-height: 1.6;
        opacity: 0.9;
        font-family: 'Share Tech Mono', monospace;
    }

    /* --- NEW RESULT CARDS DESIGN (CYBERPUNK FILES) --- */
    .result-grid {
        padding: 20px;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .cyber-card {
        background: rgba(10, 20, 30, 0.4);
        border: 1px solid #334455;
        padding: 0;
        position: relative;
        transition: all 0.3s ease;
        /* Potongan sudut sci-fi */
        clip-path: polygon(
            0 0, 
            100% 0, 
            100% 85%, 
            95% 100%, 
            0 100%
        );
        margin-bottom: 5px;
    }

    .cyber-card:hover {
        background: rgba(0, 100, 200, 0.1);
        border-color: #00eeff;
        transform: translateX(5px);
        box-shadow: -5px 0 15px rgba(0, 238, 255, 0.1);
    }

    .cyber-card::before {
        /* Garis aksen kiri neon */
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 3px; height: 100%;
        background: #00eeff;
        opacity: 0.5;
        transition: 0.3s;
    }
    .cyber-card:hover::before {
        opacity: 1;
        box-shadow: 0 0 10px #00eeff;
    }

    .cc-header {
        background: rgba(0,0,0,0.3);
        padding: 8px 15px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid #223344;
    }

    .cc-id {
        font-family: 'Orbitron', sans-serif;
        font-size: 10px;
        color: #00eeff;
        letter-spacing: 2px;
    }

    .cc-conf {
        font-size: 9px;
        color: #557799;
        background: #0a0e14;
        padding: 2px 6px;
        border: 1px solid #223344;
    }

    .cc-body {
        padding: 15px;
        font-size: 13px;
        color: #ddeecc;
        line-height: 1.5;
    }
    
    .cc-footer {
        padding: 5px 15px 10px 15px;
        font-size: 9px;
        color: #446677;
        text-align: right;
        text-transform: uppercase;
        letter-spacing: 1px;
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
    # --- REQUESTING 3-5 SENTENCES ---
    system_prompt = """
    ROLE: Tactical Extractor.
    TASK: Extract exactly 3 to 5 highly specific, actionable search queries or strategic sentences.
    OUTPUT: JSON format {"candidates": ["sentence 1", "sentence 2", "sentence 3", "sentence 4", "sentence 5"]}
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

# 1. TOP METRICS ROW
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="metric-box"><div class="metric-val">{random.randint(12,25)}ms</div><div class="metric-lbl">LATENCY</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-box"><div class="metric-val">{random.randint(120,500)}TB</div><div class="metric-lbl">UPLINK</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-box"><div class="metric-val">SECURE</div><div class="metric-lbl">PROTOCOL</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-box"><div class="metric-val" style="color:#00ff41">ACTV</div><div class="metric-lbl">STATUS</div></div>', unsafe_allow_html=True)

# 2. MAIN SPLIT SCREEN
c_chaos, c_results = st.columns([1.2, 1])

if run_btn and user_query:
    with st.spinner("PROCESSING DATA STREAMS..."):
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
                <span>/// RAW_STREAM_LOG</span>
                <span>ID: {random.randint(1000,9999)}</span>
            </div>
            <div class="chaos-log">
                > INCOMING_TRANSMISSION...<br>
                > DECRYPTING NEURAL LAYERS...<br><br>
                {raw_stream}
                <br><br>> END_OF_STREAM
            </div>
        </div>
        """, unsafe_allow_html=True)

    # RIGHT PANEL: RESULTS (NEW DESIGN)
    with c_results:
        # Build the HTML for cards
        cards_html = ""
        for i, item in enumerate(candidates):
            conf = random.randint(92, 99)
            file_id = f"DAT_{random.randint(10,99)}_{random.randint(100,999)}"
            
            cards_html += f"""
            <div class="cyber-card">
                <div class="cc-header">
                    <span class="cc-id">VECTOR_0{i+1}</span>
                    <span class="cc-conf">CONFIDENCE: {conf}%</span>
                </div>
                <div class="cc-body">
                    {item}
                </div>
                <div class="cc-footer">
                    FILE_ID: {file_id} // READY
                </div>
            </div>
            """
            
        st.markdown(f"""
        <div class="panel-container">
            <div class="panel-header">
                <span>/// TARGET_ACQUISITION</span>
                <span style="color:#00ff41">LOCKED</span>
            </div>
            <div class="result-grid">
                {cards_html}
            </div>
             <div style="position: absolute; bottom: 10px; right: 10px; font-size: 120px; color: rgba(0, 238, 255, 0.03); pointer-events: none; font-family: 'Orbitron';">
                0{len(candidates)}
            </div>
        </div>
        """, unsafe_allow_html=True)

else:
    # IDLE STATE
    with c_chaos:
        st.markdown("""
        <div class="panel-container" style="display: flex; align-items: center; justify-content: center; opacity: 0.5;">
            <div style="text-align:center;">
                <div style="font-size: 40px;">⚠️</div>
                <div>AWAITING INPUT DATA</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with c_results:
         st.markdown("""
        <div class="panel-container" style="display: flex; align-items: center; justify-content: center; opacity: 0.5;">
            <div style="text-align:center;">
                <div style="font-size: 40px;">🚫</div>
                <div>NO TARGETS ACQUIRED</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
