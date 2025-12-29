import streamlit as st
from groq import Groq
import json
import time

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="Neural Core: Chaos vs Order", 
    page_icon="☢️", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ADVANCED STYLING (CYBERPUNK AESTHETIC) ---
st.markdown("""
<style>
    /* Background Setup */
    .stApp {
        background-color: #050505;
        color: #e0e0e0;
    }
    
    /* LEFT COLUMN: CHAOS TERMINAL */
    .chaos-terminal {
        background-color: #000000;
        border: 1px solid #1a1a1a;
        border-left: 2px solid #00ff41; /* Hacker Green */
        padding: 20px;
        font-family: 'Courier New', Courier, monospace;
        color: #00ff41; 
        font-size: 12px;
        line-height: 1.4;
        height: 650px;
        overflow-y: auto;
        white-space: pre-wrap;
        box-shadow: inset 0 0 30px rgba(0,0,0,0.9);
        opacity: 0.95;
    }
    
    /* SCROLLBAR CUSTOMIZATION (Chrome/Safari) */
    ::-webkit-scrollbar {
        width: 8px;
        background: #000;
    }
    ::-webkit-scrollbar-thumb {
        background: #333;
        border-radius: 4px;
    }

    /* RIGHT COLUMN: TACTICAL LIST */
    .tactical-container {
        height: 650px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        gap: 15px;
        padding: 10px;
    }

    .strategy-card {
        background: linear-gradient(90deg, #121212 0%, #1e1e1e 100%);
        border-left: 4px solid #00d2ff; /* Cyber Blue */
        padding: 15px 20px;
        border-radius: 4px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        transition: transform 0.2s;
    }
    
    .strategy-card:hover {
        transform: translateX(5px);
        border-left: 4px solid #fff;
    }

    .card-label {
        font-size: 10px;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }

    .card-content {
        font-size: 16px;
        font-weight: 600;
        color: #ffffff;
        font-family: 'Arial', sans-serif;
    }

    /* INPUT FIELD */
    .stTextInput > div > div > input {
        background-color: #0a0a0a;
        color: #00ff41;
        border: 1px solid #333;
        font-family: 'Courier New', monospace;
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

# --- 4. CORE LOGIC ---

def get_chaos_stream(user_input):
    """
    Generate raw, unfiltered neural noise.
    """
    system_prompt = """
    You are a raw AI neural network.
    
    INSTRUCTION:
    1. Dump your internal thought process about the user's request.
    2. NO FORMATTING. NO JSON. NO LISTS. Just a continuous paragraph of text.
    3. Mix languages (Indonesian/English) freely.
    4. Critique keywords, brainstorm synonyms, doubt your own logic.
    5. Be messy, be technical, be raw.
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"USER QUERY: {user_input}"}
        ],
        temperature=0.9, # High Chaos
        max_tokens=1500
    )
    return response.choices[0].message.content

def distill_strategy(raw_text):
    """
    Extract the top 3-5 best keywords from the chaos.
    """
    system_prompt = """
    You are a Strategic Filter.
    
    TASK: Read the raw thought stream provided.
    GOAL: Extract the top 3 to 5 most effective search queries/sentences based on that analysis.
    
    OUTPUT FORMAT: JSON Object containing a list called 'candidates'.
    Example:
    {
        "candidates": [
            "jasa arsitek murah di sukabumi",
            "biaya desain rumah minimalis sukabumi 2024",
            "daftar arsitek terbaik jawa barat portofolio"
        ]
    }
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_text}
        ],
        temperature=0.1, # Strict Logic
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

# --- 5. UI LAYOUT ---

st.title("☢️ KERNEL DUMP: CHAOS vs ORDER")

# Input Section
with st.container():
    col1, col2 = st.columns([5, 1])
    with col1:
        user_query = st.text_input("Injection Prompt:", placeholder="Input raw trigger...", label_visibility="collapsed")
    with col2:
        run_btn = st.button("⚡ EXECUTE", use_container_width=True)

if run_btn and user_query:
    
    # Progress Simulation
    progress = st.progress(0)
    status = st.empty()
    
    try:
        # STEP 1: CHAOS GENERATION
        status.code(">> ACCESSING NEURAL PATHWAYS...", language="bash")
        progress.progress(20)
        time.sleep(0.2)
        
        status.code(">> STREAMING RAW CONSCIOUSNESS...", language="bash")
        raw_stream = get_chaos_stream(user_query)
        progress.progress(60)
        
        # STEP 2: DISTILLATION
        status.code(">> REFINING STRATEGIC VECTORS...", language="bash")
        json_res = distill_strategy(raw_stream)
        refined_data = json.loads(json_res)
        candidates = refined_data.get("candidates", [])
        
        progress.progress(100)
        time.sleep(0.2)
        progress.empty()
        status.empty()

        # --- DUAL VIEW DISPLAY ---
        c_raw, c_refined = st.columns([1.2, 1])

        # LEFT: THE CHAOS
        with c_raw:
            st.markdown("### 🧬 UNFILTERED LOG")
            st.markdown(f"""
            <div class="chaos-terminal">
            > SYSTEM_START<br>
            > INPUT_RECEIVED: "{user_query}"<br>
            > ----------------------------------<br>
            {raw_stream}
            <br>> ----------------------------------<br>
            > STREAM_END
            </div>
            """, unsafe_allow_html=True)

        # RIGHT: THE ORDER
        with c_refined:
            st.markdown("### 🎯 OPTIMIZED VECTORS")
            
            # Container for the cards
            st.markdown('<div class="tactical-container">', unsafe_allow_html=True)
            
            # Loop to create cards dynamically
            for i, item in enumerate(candidates):
                st.markdown(f"""
                <div class="strategy-card">
                    <div class="card-label">VECTOR 0{i+1} // PRIORITY HIGH</div>
                    <div class="card-content">{item}</div>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)

    except Exception as e:
        st.error(f"System Failure: {e}")
