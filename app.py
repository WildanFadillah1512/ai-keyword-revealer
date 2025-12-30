import streamlit as st
from groq import Groq
import json
import time
import random

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="ORBITAL COMMAND V2.1",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ADVANCED NEURAL-ORBITAL HUD CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=JetBrains+Mono:wght@300;500&family=Orbitron:wght@400;900&display=swap');

    :root {
        --primary: #00ffaa;
        --secondary: #0088cc;
        --bg-dark: #020205;
        --glass: rgba(10, 15, 25, 0.8);
        --border: rgba(0, 255, 170, 0.15);
    }

    /* GLOBAL RESET */
    .stApp {
        background: radial-gradient(circle at 50% 50%, #0a1018 0%, #020205 100%);
        color: #aaccff;
        font-family: 'JetBrains Mono', monospace;
    }

    header, footer, .stDeployButton {display: none;}

    /* HUD TOP BAR */
    .hud-header {
        display: flex;
        justify-content: space-between;
        padding: 10px 20px;
        background: rgba(0,0,0,0.5);
        border-bottom: 1px solid var(--border);
        font-family: 'Syncopate', sans-serif;
        font-size: 9px;
        letter-spacing: 2px;
    }

    /* NEURAL PANEL (Kiri) */
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

    /* QUERY CARDS (Kanan) */
    .query-card {
        background: rgba(0, 136, 204, 0.05);
        border: 1px solid rgba(0, 136, 204, 0.2);
        border-left: 3px solid var(--secondary);
        padding: 15px;
        margin-bottom: 12px;
        transition: all 0.4s ease;
    }

    .query-card:hover {
        background: rgba(0, 255, 170, 0.1);
        border-left: 3px solid var(--primary);
        transform: translateX(10px);
    }

    /* COMMAND INPUT */
    .stTextInput input {
        background: rgba(0,0,0,0.3) !important;
        border: 1px solid var(--border) !important;
        border-radius: 0px !important;
        color: var(--primary) !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 20px !important;
        text-align: center;
        padding: 25px !important;
        transition: 0.5s;
    }
    
    .stTextInput input:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 20px rgba(0, 255, 170, 0.2) !important;
    }

    /* BUTTONS */
    .stButton button {
        background: transparent !important;
        border: 1px solid var(--primary) !important;
        color: var(--primary) !important;
        border-radius: 0px !important;
        font-family: 'Syncopate' !important;
        letter-spacing: 2px;
        transition: 0.4s;
    }

    .stButton button:hover {
        background: var(--primary) !important;
        color: #000 !important;
        box-shadow: 0 0 30px var(--primary);
    }

    /* TERMINAL TEXT */
    .chaos-text {
        color: var(--primary);
        font-size: 11px;
        line-height: 1.6;
        opacity: 0.8;
        white-space: pre-wrap;
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
        animation: scan 12s linear infinite;
        z-index: 10;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC (STRICTLY PRESERVED) ---
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

# --- 4. HUD LAYOUT ---

# TOP HUD BAR
st.markdown(f"""
<div class="hud-header">
    <div>STATUS: <span style="color:var(--primary)">UPLINK_ESTABLISHED</span></div>
    <div>CORE_LATENCY: {random.randint(8,15)}MS</div>
    <div>PROTOCOL: ORBITAL_V2</div>
    <div style="color:var(--secondary)">LOC: {random.randint(100,999)} // {random.randint(1000,9999)}</div>
</div>
""", unsafe_allow_html=True)

st.write("<br>", unsafe_allow_html=True)

# CENTRAL CONTROL AREA
c_main = st.columns([1, 2, 1])
with c_main[1]:
    st.markdown("<h1 style='text-align: center; font-size: 3.5rem; margin-bottom: 0; font-family:Syncopate;'>ORBITAL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: var(--secondary); letter-spacing: 12px; font-size: 10px; margin-top:-10px;'>COGNITIVE COMMAND CENTER</p>", unsafe_allow_html=True)
    user_query = st.text_input("..", placeholder="INJECT COMMAND SEQUENCE...", label_visibility="collapsed")
    run_btn = st.button("INITIALIZE SEQUENCE", use_container_width=True)

st.markdown("<div style='margin: 30px 0; border-bottom: 1px solid var(--border);'></div>", unsafe_allow_html=True)

# DATA DISPLAY ENGINE
if run_btn and user_query:
    with st.spinner("TRACE IN PROGRESS..."):
        raw_stream = get_chaos_stream(user_query)
        json_res = distill_strategy(raw_stream)
        try:
            candidates = json.loads(json_res).get("candidates", [])
        except:
            candidates = ["ERROR: DECODING_FAILED"]

    col_trace, col_shards = st.columns([1.3, 1])

    with col_trace:
        st.markdown("<div style='font-family:Syncopate; font-size:10px; color:var(--secondary); margin-bottom:10px;'>[01] DEEP_COGNITION_TRACE</div>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="neural-panel">
            <div class="scanner"></div>
            <div class="chaos-text">{raw_stream}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_shards:
        st.markdown("<div style='font-family:Syncopate; font-size:10px; color:var(--secondary); margin-bottom:10px;'>[02] TARGET_ACQUISITION_QUERIES</div>", unsafe_allow_html=True)
        with st.container():
            for i, item in enumerate(candidates):
                st.markdown(f"""
                <div class="query-card">
                    <div style="font-size: 9px; color: var(--secondary); margin-bottom:5px;">VECTOR_0{i+1}</div>
                    <code style="color:var(--primary); background:transparent; font-size:13px;">{item}</code>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"COPY_VECTOR_0{i+1}", key=f"btn_{i}", use_container_width=True):
                    st.toast(f"Vector 0{i+1} cached to system.")

else:
    # IDLE STATE
    st.markdown(f"""
    <div style="height: 40vh; display: flex; flex-direction: column; align-items: center; justify-content: center; opacity: 0.1;">
        <div style="font-family: 'Syncopate'; font-size: 6rem; margin:0;">IDLE</div>
        <div style="letter-spacing: 15px; font-size: 12px;">SYSTEM_STANDBY // AWAITING_INPUT</div>
    </div>
    """, unsafe_allow_html=True)

# FOOTER STATS
st.markdown(f"""
<div style="position: fixed; bottom: 15px; left: 20px; font-size: 9px; color: #445566; font-family: 'JetBrains Mono';">
    V.2.1_STABLE // NO_LIMITS_DEFINED // {time.strftime("%H:%M:%S")}
</div>
""", unsafe_allow_html=True)
