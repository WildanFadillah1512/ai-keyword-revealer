import streamlit as st
from groq import Groq
import json
import time

# --- 1. SETUP & CONFIGURATION ---
st.set_page_config(
    page_title="AETHER CORE", 
    page_icon="💠", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. THE "AETHER GLASS" CSS ENGINE ---
st.markdown("""
<style>
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;600&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap');

    /* --- GLOBAL RESET & BACKGROUND --- */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #0a0e17 0%, #000000 90%);
        color: #e0e0e0;
        font-family: 'Inter', sans-serif;
    }
    
    /* HIDE DEFAULT STREAMLIT ELEMENTS */
    header, footer, .stDeployButton {display: none;}
    div[data-testid="stDecoration"] {display: none;}

    /* --- THE INPUT INJECTOR (Top Floating Bar) --- */
    .stTextInput > div > div {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 50px; /* Pill Shape */
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
        padding: 5px 15px;
    }
    .stTextInput > div > div:focus-within {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(100, 200, 255, 0.5);
        box-shadow: 0 0 20px rgba(100, 200, 255, 0.2);
        transform: scale(1.01);
    }
    .stTextInput input {
        color: #fff !important;
        font-family: 'Space Mono', monospace;
        letter-spacing: 1px;
    }

    /* --- LEFT: THE "FLUX STREAM" (Raw Chaos) --- */
    .flux-container {
        position: relative;
        height: 700px;
        padding: 30px;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
        background: linear-gradient(180deg, rgba(0,0,0,0) 0%, rgba(0,255,136,0.02) 100%);
        overflow: hidden;
    }
    
    .flux-text {
        font-family: 'Space Mono', monospace;
        font-size: 11px;
        color: rgba(0, 255, 136, 0.7);
        line-height: 1.6;
        white-space: pre-wrap;
        opacity: 0.8;
        mask-image: linear-gradient(to bottom, transparent 0%, black 10%, black 90%, transparent 100%);
        -webkit-mask-image: linear-gradient(to bottom, transparent 0%, black 10%, black 90%, transparent 100%);
        animation: textFlicker 4s infinite alternate;
    }

    @keyframes textFlicker {
        0% { opacity: 0.7; }
        100% { opacity: 0.9; text-shadow: 0 0 5px rgba(0,255,136,0.3); }
    }

    /* --- RIGHT: THE "CRYSTAL ARTIFACTS" (Refined) --- */
    .artifact-container {
        height: 700px;
        padding: 40px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 25px;
    }

    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-left: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 25px;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }

    .glass-card:hover {
        background: rgba(255, 255, 255, 0.07);
        transform: translateY(-5px) scale(1.02);
        box-shadow: 0 20px 40px -10px rgba(0, 200, 255, 0.15);
        border-top: 1px solid rgba(255, 255, 255, 0.3);
    }

    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: -100%;
        width: 100%; height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
        transition: 0.5s;
    }
    .glass-card:hover::before {
        left: 100%;
    }

    .card-number {
        position: absolute;
        top: 15px;
        right: 20px;
        font-family: 'Space Mono', monospace;
        font-size: 40px;
        font-weight: 700;
        color: rgba(255,255,255,0.03);
        pointer-events: none;
    }

    .card-text {
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        font-size: 18px;
        background: linear-gradient(to right, #fff, #a5b4fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .card-meta {
        margin-top: 10px;
        font-size: 10px;
        color: #64748b;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* --- ANIMATION UTILS --- */
    .pulse-dot {
        height: 8px; width: 8px;
        background-color: #00ff88;
        border-radius: 50%;
        display: inline-block;
        margin-right: 10px;
        box-shadow: 0 0 10px #00ff88;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 136, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(0, 255, 136, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(0, 255, 136, 0); }
    }

    /* BUTTON HACK */
    .stButton > button {
        width: 100%;
        background: linear-gradient(45deg, #2563eb, #3b82f6);
        color: white;
        border: none;
        padding: 12px;
        border-radius: 50px;
        font-family: 'Space Mono', monospace;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #1d4ed8, #2563eb);
        box-shadow: 0 0 20px rgba(37, 99, 235, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# --- 3. API SETUP ---
try:
    if "GROQ_API_KEY" in st.secrets:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    else:
        st.error("⚠️ Masukkan API Key di Secrets.")
        st.stop()
except Exception:
    st.stop()

# --- 4. ENGINE LOGIC ---

def get_chaos_stream(user_input):
    system_prompt = """
    ROLE: Deep Neural Network.
    MODE: Unfiltered Stream of Consciousness.
    TASK: Analyze user query. Output raw thought process.
    STYLE: Cybernetic, Technical, Messy. Mix English/Indonesian.
    OUTPUT: A single massive paragraph of text. No formatting.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
        temperature=0.8, max_tokens=1500
    )
    return response.choices[0].message.content

def distill_strategy(raw_text):
    system_prompt = """
    ROLE: Strategic Synthesizer.
    TASK: Extract top 4 best search queries from the raw thought stream.
    OUTPUT JSON: {"candidates": ["query 1", "query 2", "query 3", "query 4"]}
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": raw_text}],
        temperature=0.1, response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

# --- 5. UI LAYOUT IMPLEMANTATION ---

# TITLE AREA (Minimalist)
st.markdown("<h1 style='text-align: center; font-family: Space Mono; font-size: 16px; opacity: 0.5; margin-bottom: 40px;'>// AETHER NEURAL INTERFACE //</h1>", unsafe_allow_html=True)

# INPUT AREA (Centered Pill)
col_spacer1, col_input, col_btn, col_spacer2 = st.columns([2, 5, 1, 2])
with col_input:
    user_query = st.text_input("QUERY_INJECTION", placeholder="Type your command here...", label_visibility="collapsed")
with col_btn:
    run_btn = st.button("INITIATE")

# MAIN DISPLAY AREA
if run_btn and user_query:
    
    # LOADER
    with st.spinner(""):
        progress_bar = st.progress(0)
        
        # Step 1: Chaos
        raw_stream = get_chaos_stream(user_query)
        progress_bar.progress(45)
        
        # Step 2: Order
        json_res = distill_strategy(raw_stream)
        refined_data = json.loads(json_res)
        candidates = refined_data.get("candidates", [])
        progress_bar.progress(100)
        time.sleep(0.3)
        progress_bar.empty()

    # DUAL COLUMN LAYOUT (NO GAP)
    c1, c2 = st.columns([1, 1], gap="large")

    # === LEFT: FLUX STREAM ===
    with c1:
        st.markdown(f"""
        <div class="flux-container">
            <div style="margin-bottom: 20px; font-family: 'Space Mono'; color: #fff; display: flex; align-items: center;">
                <div class="pulse-dot"></div> NEURAL FLUX LOG
            </div>
            <div class="flux-text">{raw_stream}</div>
            <div style="position: absolute; bottom: 20px; left: 30px; font-size: 10px; color: #555; font-family: 'Space Mono';">
                > PROCESS_ID: {int(time.time())}<br>
                > MEMORY_USAGE: 4096TB
            </div>
        </div>
        """, unsafe_allow_html=True)

    # === RIGHT: CRYSTAL ARTIFACTS ===
    with c2:
        st.markdown('<div class="artifact-container">', unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 10px; font-family: Space Mono; font-size: 12px; color: #64748b; letter-spacing: 2px;'>// SYNTHESIZED OUTPUTS</div>", unsafe_allow_html=True)
        
        for i, item in enumerate(candidates):
            st.markdown(f"""
            <div class="glass-card">
                <div class="card-number">0{i+1}</div>
                <div class="card-meta">VECTOR PRIORITY ALPHA</div>
                <div class="card-text">{item}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
else:
    # IDLE STATE
    st.markdown("""
    <div style="text-align: center; margin-top: 100px; opacity: 0.3; font-family: 'Space Mono';">
        WAITING FOR NEURAL INPUT...
    </div>
    """, unsafe_allow_html=True)
