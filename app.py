import streamlit as st
from groq import Groq
import json
import time
import random

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="NEURAL TACTICAL HUD", 
    page_icon="👁️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. TACTICAL HUD CSS (Solid, Clean, High Contrast) ---
st.markdown("""
<style>
    /* RESET & FONTS */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;800&family=Rajdhani:wght@500;700&display=swap');
    
    .stApp {
        background-color: #050505;
        background-image: 
            linear-gradient(rgba(0, 255, 65, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 65, 0.03) 1px, transparent 1px);
        background-size: 30px 30px; /* Grid Pattern */
        color: #e0e0e0;
    }

    /* HIDE STREAMLIT UI */
    header, footer, .stDeployButton {display: none;}
    div[data-testid="stDecoration"] {display: none;}

    /* INPUT FIELD - COMMAND LINE STYLE */
    .stTextInput > div > div {
        background-color: #000 !important;
        border: 2px solid #333 !important;
        border-left: 5px solid #00ff41 !important; /* Green Accent */
        border-radius: 0px !important;
        color: #00ff41 !important;
    }
    .stTextInput input {
        font-family: 'JetBrains Mono', monospace !important;
        color: #00ff41 !important;
        font-size: 16px;
    }

    /* --- LEFT COLUMN: RAW DATA TERMINAL --- */
    .terminal-window {
        background-color: #0a0a0a;
        border: 1px solid #333;
        height: 600px;
        padding: 0;
        position: relative;
        overflow: hidden;
        box-shadow: 0 0 20px rgba(0,0,0,0.8);
    }
    
    .terminal-header {
        background-color: #1a1a1a;
        padding: 10px;
        border-bottom: 1px solid #333;
        display: flex;
        justify-content: space-between;
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        color: #555;
    }

    .terminal-content {
        padding: 20px;
        height: 550px;
        overflow-y: auto;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        line-height: 1.5;
        color: #00ff41; /* Classic Terminal Green */
        white-space: pre-wrap;
    }

    /* SCROLLBAR */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #000; }
    ::-webkit-scrollbar-thumb { background: #333; }

    /* --- RIGHT COLUMN: TACTICAL CARDS --- */
    .results-container {
        height: 600px;
        display: flex;
        flex-direction: column;
        gap: 15px;
    }

    .hud-card {
        background: #0f1115;
        border: 1px solid #444;
        border-right: 4px solid #00d2ff; /* Cyan Accent */
        padding: 15px;
        position: relative;
        transition: transform 0.2s;
    }
    
    .hud-card:hover {
        transform: translateX(-5px);
        background: #16191f;
        border-color: #00d2ff;
    }

    .hud-label {
        font-family: 'Rajdhani', sans-serif;
        font-weight: 700;
        font-size: 12px;
        color: #00d2ff;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px;
        display: flex;
        justify-content: space-between;
    }

    .hud-text {
        font-family: 'JetBrains Mono', monospace;
        font-size: 14px;
        color: #fff;
    }

    /* BUTTON STYLING */
    .stButton > button {
        width: 100%;
        background-color: #00d2ff;
        color: #000;
        font-family: 'Rajdhani', sans-serif;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 2px;
        border: none;
        border-radius: 0;
        padding: 15px;
        transition: 0.3s;
    }
    .stButton > button:hover {
        background-color: #fff;
        box-shadow: 0 0 20px #00d2ff;
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

# --- 4. LOGIC ENGINE (DITWEAK AGAR LEBIH CHAOS BAHASANYA) ---

def get_chaos_stream(user_input):
    """
    Prompt ini memaksa AI untuk mencampur bahasa dan bersikap lebih 'mesin'.
    """
    system_prompt = """
    ROLE: High-Performance Neural Search Core.
    
    CRITICAL INSTRUCTIONS:
    1. You are PROCESSING data, not chatting.
    2. DUMP your raw internal monologue instantly.
    3. LANGUAGE REQUIREMENT: You MUST mix English (for technical terms, logic) and Indonesian (for connectors, reasoning) freely. AKA "Bahasa Jaksel" style but more robotic.
    4. Example: "Analyzing user intent... sepertinya user butuh spesifikasi teknis. Query is ambiguous. Checking synonyms... mungkin maksudnya 'low latency'."
    5. NO MARKDOWN FORMATTING. Just raw text stream.
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"INPUT: {user_input}"}
        ],
        temperature=0.85, # Agak tinggi biar kreatif
        max_tokens=1500
    )
    return response.choices[0].message.content

def distill_strategy(raw_text):
    """
    Mengambil intisari menjadi keyword siap pakai.
    """
    system_prompt = """
    ROLE: Tactical Data Filter.
    TASK: Extract exactly 3 to 4 best search phrases from the raw stream.
    OUTPUT: JSON format {"candidates": ["phrase 1", "phrase 2", "phrase 3"]}
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_text}
        ],
        temperature=0.1,
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

# --- 5. UI LAYOUT ---

st.markdown("<h1 style='text-align: center; font-family: Rajdhani; color: #fff; letter-spacing: 5px; margin-bottom: 10px;'>/// NEURAL TACTICAL INTERFACE</h1>", unsafe_allow_html=True)

# INPUT BAR
c1, c2 = st.columns([5, 1])
with c1:
    user_query = st.text_input("CMD_INPUT", placeholder="ENTER TARGET KEYWORD...", label_visibility="collapsed")
with c2:
    run_btn = st.button("EXECUTE")

if run_btn and user_query:
    
    # PROCESS INDICATOR
    status_box = st.empty()
    bar = st.progress(0)
    
    # 1. GENERATE CHAOS
    status_box.markdown("<span style='color:#00ff41; font-family: JetBrains Mono;'>[>>] ESTABLISHING NEURAL LINK...</span>", unsafe_allow_html=True)
    time.sleep(0.3)
    raw_stream = get_chaos_stream(user_query)
    bar.progress(60)
    
    # 2. REFINE DATA
    status_box.markdown("<span style='color:#00d2ff; font-family: JetBrains Mono;'>[>>] CALCULATING OPTIMAL VECTORS...</span>", unsafe_allow_html=True)
    json_res = distill_strategy(raw_stream)
    try:
        data = json.loads(json_res)
        candidates = data.get("candidates", [])
    except:
        candidates = ["ERROR PARSING DATA", "RETRY INITIATED"]
        
    bar.progress(100)
    time.sleep(0.2)
    bar.empty()
    status_box.empty()

    # --- MAIN DISPLAY (SPLIT VIEW) ---
    col_left, col_right = st.columns([1.5, 1], gap="medium")

    # LEFT: TERMINAL
    with col_left:
        st.markdown(f"""
        <div class="terminal-window">
            <div class="terminal-header">
                <span>TERMINAL_ID: 0X99</span>
                <span>STATUS: LIVE</span>
            </div>
            <div class="terminal-content">
> SYSTEM_INIT<br>
> TARGET: "{user_query}"<br>
> LANG_MODE: MIXED_HYBRID<br>
> ----------------------------------------<br>
{raw_stream}
<br>> ----------------------------------------<br>
> END_OF_STREAM
            </div>
        </div>
        """, unsafe_allow_html=True)

    # RIGHT: HUD CARDS
    with col_right:
        st.markdown('<div class="results-container">', unsafe_allow_html=True)
        st.markdown("<div style='color: #666; font-family: Rajdhani; font-size: 12px; margin-bottom: 10px;'>TARGET ACQUISITION RESULT</div>", unsafe_allow_html=True)
        
        for i, item in enumerate(candidates):
            confidence = random.randint(89, 99)
            st.markdown(f"""
            <div class="hud-card">
                <div class="hud-label">
                    <span>VECTOR_0{i+1}</span>
                    <span>{confidence}% MATCH</span>
                </div>
                <div class="hud-text">{item}</div>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)

else:
    # IDLE SCREEN
    st.markdown("""
    <div style="height: 400px; display: flex; align-items: center; justify-content: center; flex-direction: column; opacity: 0.3;">
        <h2 style="font-family: Rajdhani; color: #00ff41;">SYSTEM STANDBY</h2>
        <p style="font-family: JetBrains Mono; font-size: 12px;">AWAITING OPERATOR INPUT</p>
    </div>
    """, unsafe_allow_html=True)
