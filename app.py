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
    
    /* METRIC BOXES */
    .metric-box {
        background: rgba(0, 20, 30, 0.5);
        border: 1px solid #1f293a;
        padding: 10px;
        text-align: center;
        border-radius: 0px;
        position: relative;
    }
    .metric-val { font-size: 20px; color: #fff; font-weight: bold; font-family: 'Orbitron'; }
    .metric-lbl { font-size: 10px; color: #557799; letter-spacing: 1px; }

    /* PANEL CONTAINERS */
    .custom-container {
        background: #050608;
        border: 1px solid #1f293a;
        height: 600px;
        overflow-y: auto;
        padding: 20px;
        margin-top: 10px;
        position: relative;
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar { width: 5px; }
    ::-webkit-scrollbar-track { background: #020204; }
    ::-webkit-scrollbar-thumb { background: #1f293a; }

    /* CHAOS LOG STYLE */
    .chaos-text {
        color: #00ffaa;
        font-size: 11px;
        line-height: 1.6;
        opacity: 0.9;
        white-space: pre-wrap; /* Agar format teks terjaga */
    }

    /* --- RESULT CARD STYLING FOR ST.CONTAINER --- */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        gap: 1rem; /* Spacing antar card */
    }
    
    .stMarkdown h3 {
        font-family: 'Orbitron', sans-serif !important;
        font-size: 14px !important;
        color: #00eeff !important;
        margin: 0;
        padding: 0;
        letter-spacing: 1px;
    }
    
    .stMarkdown p {
        font-size: 13px !important;
        color: #ddeecc !important;
    }

    /* Styling container khusus hasil */
    .result-card-container {
        border: 1px solid #334455;
        background: rgba(10, 20, 30, 0.4);
        padding: 15px;
        border-left: 3px solid #0088cc;
        transition: 0.3s;
    }
    .result-card-container:hover {
        border-left: 3px solid #00eeff;
        background: rgba(0, 100, 200, 0.1);
        transform: translateX(5px);
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
    # --- PROMPT DIPERBARUI UNTUK MEMBUKA SELURUH PROSES BERPIKIR ---
    system_prompt = """
    You are a hyper-analytical AI engine performing a Deep Layer Cognition Trace.
    
    OBJECTIVE:
    Provide an exhaustive, step-by-step, unfiltered breakdown of your reasoning process regarding the user's input. Do NOT summarize. Do NOT simplify.
    
    MANDATORY OUTPUT STRUCTURE (Stream of Consciousness):
    1. **Semantic Deconstruction**: Break the input down into tokens, intent, and hidden implications.
    2. **Knowledge Retrieval**: List all related concepts, database nodes, and theoretical frameworks you are accessing.
    3. **Hypothesis Formation**: Generate multiple possible interpretations or answers (Hypothesis A, B, C).
    4. **Dialectical Analysis**: Argue against yourself. Find flaws in Hypothesis A. Strengthen Hypothesis B.
    5. **Synthesis & Convergence**: Merging the strongest points into a final logic path.
    6. **Final Output Generation**: The actual answer derived from the process.
    
    STYLE:
    - Use technical, clinical, and precise language.
    - Show the "messy" work: intermediate calculations, corrections, and reconsiderations.
    - Output MUST be verbose and detailed.
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
        temperature=0.7, 
        max_tokens=2048 # Max token dinaikkan agar output tidak terpotong
    )
    return response.choices[0].message.content

def distill_strategy(raw_text):
    system_prompt = """
    ROLE: Tactical Extractor.
    TASK: Based on the raw analysis provided, extract exactly 3 to 5 highly specific, actionable conclusions or strategic points.
    OUTPUT: JSON format {"candidates": ["point 1", "point 2", "point 3", "point 4", "point 5"]}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": raw_text}],
        temperature=0.1, response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

# --- 4. LAYOUT CONSTRUCTION ---

# === SIDEBAR ===
with st.sidebar:
    st.markdown('<div class="sidebar-header">/// ORBITAL</div>', unsafe_allow_html=True)
    user_query = st.text_input("..", placeholder="Inject Command...", label_visibility="collapsed")
    st.markdown("---")
    st.markdown("SYSTEM SETTINGS")
    temp = st.slider("Chaos Level", 0.0, 1.0, 0.8)
    st.markdown("---")
    run_btn = st.button("INITIALIZE SEQUENCE")
    
    if not run_btn:
        st.info("STATUS: STANDBY // UPLINK: SECURE")

# === MAIN DASHBOARD ===

# Metrics Row
m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="metric-box"><div class="metric-val">{random.randint(12,25)}ms</div><div class="metric-lbl">LATENCY</div></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-box"><div class="metric-val">{random.randint(120,500)}TB</div><div class="metric-lbl">UPLINK</div></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="metric-box"><div class="metric-val">SECURE</div><div class="metric-lbl">PROTOCOL</div></div>', unsafe_allow_html=True)
with m4: st.markdown(f'<div class="metric-box"><div class="metric-val" style="color:#00ff41">ACTV</div><div class="metric-lbl">STATUS</div></div>', unsafe_allow_html=True)

# Main Split
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
            
    # LEFT PANEL: CHAOS (Raw Logika AI)
    with c_chaos:
        st.caption(f"/// RAW_COGNITIVE_LOG // ID: {random.randint(1000,9999)}")
        with st.container(height=600, border=True):
            st.markdown(f'<div class="chaos-text">{raw_stream}</div>', unsafe_allow_html=True)

    # RIGHT PANEL: RESULTS (NATIVE STREAMLIT COMPONENT)
    with c_results:
        st.caption("/// TARGET_ACQUISITION // STATUS: LOCKED")
        
        # Container utama dengan scroll
        with st.container(height=600, border=True):
            
            # Loop menggunakan komponen native Streamlit
            for i, item in enumerate(candidates):
                conf = random.randint(92, 99)
                
                with st.container():
                    st.markdown("---") # Pembatas tipis
                    c_head, c_conf = st.columns([3, 1])
                    with c_head:
                        st.markdown(f"**VECTOR 0{i+1}**")
                    with c_conf:
                        st.caption(f"{conf}%")
                    
                    st.write(item) 
                    st.caption(f"FILE_ID: DAT_{random.randint(10,99)} // READY")

else:
    # IDLE STATE
    with c_chaos:
        st.container(height=600, border=True).markdown("<br><br><center>AWAITING INPUT...</center>", unsafe_allow_html=True)
    with c_results:
        st.container(height=600, border=True).markdown("<br><br><center>NO TARGETS</center>", unsafe_allow_html=True)
