import streamlit as st
from groq import Groq
import json
import time
import random

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="ORBITAL COMMAND V2.1",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ADVANCED NEURAL HUD CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=JetBrains+Mono:wght@300;500&family=Orbitron:wght@400;900&display=swap');

    :root {
        --primary: #00ffaa;
        --secondary: #0088cc;
        --warning: #ff3300;
        --bg-dark: #020205;
        --glass: rgba(10, 15, 25, 0.8);
        --border: rgba(0, 255, 170, 0.15);
    }

    /* GLOBAL CANVAS */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0a1018 0%, #020205 100%);
        color: #aaccff;
        font-family: 'JetBrains Mono', monospace;
    }

    header, footer, .stDeployButton {display: none;}

    /* HUD METRIC BAR */
    .hud-metric-container {
        display: flex;
        justify-content: space-between;
        padding: 10px 20px;
        background: rgba(0,0,0,0.5);
        border-bottom: 1px solid var(--border);
        font-family: 'Syncopate', sans-serif;
        font-size: 9px;
        letter-spacing: 2px;
    }

    /* NEURAL CONTAINER (Kiri) */
    .neural-panel {
        background: var(--glass);
        backdrop-filter: blur(15px);
        border: 1px solid var(--border);
        padding: 20px;
        height: 600px;
        overflow-y: auto;
        position: relative;
    }
    
    .neural-panel::after {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 100%;
        background: linear-gradient(rgba(0,255,170,0.03) 50%, transparent 50%);
        background-size: 100% 4px;
        pointer-events: none;
    }

    /* VECTOR SHARDS (Kanan) */
    .vector-shard {
        background: rgba(0, 136, 204, 0.05);
        border: 1px solid rgba(0, 136, 204, 0.2);
        border-left: 3px solid var(--secondary);
        padding: 15px;
        margin-bottom: 12px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .vector-shard:hover {
        background: rgba(0, 255, 170, 0.1);
        border-left: 3px solid var(--primary);
        transform: translateX(10px);
        box-shadow: -10px 0 20px rgba(0, 255, 170, 0.1);
    }

    /* COMMAND INPUT */
    .stTextInput input {
        background: rgba(0,0,0,0.3) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0px !important;
        color: var(--primary) !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 18px !important;
        text-align: center;
        padding: 20px !important;
    }

    /* TERMINAL TEXT */
    .chaos-text {
        color: var(--primary);
        font-size: 11px;
        line-height: 1.6;
        opacity: 0.8;
        white-space: pre-wrap;
    }

    .section-label {
        font-family: 'Syncopate', sans-serif;
        font-size: 10px;
        color: var(--secondary);
        margin-bottom: 10px;
        display: block;
        letter-spacing: 3px;
    }

    /* SCANLINE ANIMATION */
    @keyframes scan {
        0% { transform: translateY(-100%); }
        100% { transform: translateY(1000%); }
    }
    .scanner {
        position: absolute;
        width: 100%;
        height: 2px;
        background: var(--primary);
        opacity: 0.1;
        animation: scan 10s linear infinite;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CORE INTELLIGENCE (GROQ) ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("UPLINK FAILED: API_KEY_NOT_FOUND")
    st.stop()

def get_deep_trace(user_input):
    """Fungsi Logika Kiri: Analisis Mendalam"""
    system_prompt = """
    You are a hyper-analytical AI engine performing a Deep Layer Cognition Trace.
    MANDATORY OUTPUT STRUCTURE:
    1. Semantic Deconstruction: (tokens, hidden intent)
    2. Knowledge Retrieval: (theoretical frameworks, related nodes)
    3. Hypothesis Formation: (interpretations A, B, C)
    4. Dialectical Analysis: (finding flaws in your own logic)
    5. Convergence Logic: (synthesis of the final path)
    
    STYLE: Clinical, technical, verbose. Show the messy work.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
        temperature=0.75, max_tokens=2500
    )
    return response.choices[0].message.content

def distill_shards(trace_text):
    """Fungsi Logika Kanan: Ekstraksi Kueri Pencarian"""
    system_prompt = """
    ROLE: Intelligence Liaison.
    TASK: Generate exactly 4 highly optimized "Search Model Queries" for deep research based on the provided trace.
    OUTPUT: JSON format {"shards": ["query 1", "query 2", "query 3", "query 4"]}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": trace_text}],
        temperature=0.2, response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content).get("shards", [])

# --- 4. ORBITAL INTERFACE ---

# TOP HUD
st.markdown(f"""
<div class="hud-metric-container">
    <div>SYS_STATUS: <span style="color:var(--primary)">ACTIVE</span></div>
    <div>UPLINK_STRENGTH: {random.randint(85,99)}%</div>
    <div>NEURAL_LOAD: {random.randint(10,40)}%</div>
    <div style="color:var(--warning)">COORDINATES: {random.randint(100,999)}LX / {random.randint(100,999)}YT</div>
</div>
""", unsafe_allow_html=True)

# HEADER
st.write("<br>", unsafe_allow_html=True)
c_header = st.columns([1, 2, 1])
with c_header[1]:
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-bottom: 0; font-family:Syncopate;'>ORBITAL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: var(--secondary); letter-spacing: 12px; font-size: 10px;'>DEEP COGNITION COMMAND</p>", unsafe_allow_html=True)
    query = st.text_input("CMD", placeholder="INJECT COMMAND SEQUENCE...", label_visibility="collapsed")
    execute = st.button("INITIALIZE TRACE")

st.markdown("<div style='margin: 20px 0; border-bottom: 1px solid var(--border);'></div>", unsafe_allow_html=True)

# MAIN DISPLAY
if execute and query:
    with st.spinner("PENETRATING NEURAL LAYERS..."):
        # Processing
        raw_trace = get_deep_trace(query)
        shards = distill_shards(raw_trace)
    
    col_left, col_right = st.columns([1.4, 1])
    
    with col_left:
        st.markdown("<span class='section-label'>[01] COGNITIVE_RAW_TRACE</span>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="neural-panel">
            <div class="scanner"></div>
            <div class="chaos-text">{raw_trace}</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col_right:
        st.markdown("<span class='section-label'>[02] OPTIMIZED_SEARCH_SHARDS</span>", unsafe_allow_html=True)
        with st.container():
            for i, s in enumerate(shards):
                st.markdown(f"""
                <div class="vector-shard">
                    <div style="font-size: 9px; color: var(--secondary);">VECTOR_ID: 0x00{i+1}</div>
                    <div style="font-size: 14px; margin-top: 5px; color: #fff;">{s}</div>
                    <div style="text-align: right; font-size: 8px; margin-top: 8px; color: var(--primary); opacity: 0.5;">READY FOR UPLINK</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"EXECUTE SEARCH 0{i+1}", key=f"btn_{i}"):
                    st.toast(f"Broadcasting Vector 0{i+1} to Research Engine...")

else:
    # IDLE STATE
    st.markdown(f"""
    <div style="height: 50vh; display: flex; flex-direction: column; align-items: center; justify-content: center; opacity: 0.15;">
        <div style="font-family: 'Syncopate'; font-size: 8rem; margin:0;">IDLE</div>
        <div style="letter-spacing: 15px; font-size: 12px;">AWAITING COMMAND INJECTION</div>
    </div>
    """, unsafe_allow_html=True)

# FOOTER
st.markdown(f"""
<div style="position: fixed; bottom: 15px; right: 20px; font-size: 9px; color: #445566; font-family: 'JetBrains Mono';">
    V.2.1_STABLE // GROQ_LLAMA_3.3_70B // {time.strftime("%H:%M:%S")}
</div>
""", unsafe_allow_html=True)
