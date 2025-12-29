import streamlit as st
from groq import Groq
import json
import time
import random

# --- 1. CONFIGURATION ---
st.set_page_config(
    page_title="ORBITAL COMMAND V2",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. THE "NEURAL-ORBITAL HUD" CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syncopate:wght@400;700&family=JetBrains+Mono:wght@300;500&display=swap');

    :root {
        --primary: #00ffaa;
        --bg-dark: #050505;
        --glass: rgba(15, 15, 20, 0.7);
        --border-color: rgba(0, 255, 170, 0.2);
    }

    /* GLOBAL RESET */
    .stApp {
        background: radial-gradient(circle at center, #101520 0%, #050505 100%);
        color: #e0e0e0;
        font-family: 'JetBrains+Mono', monospace;
    }

    /* HIDE STREAMLIT GARBAGE */
    header, footer, .stDeployButton {display: none;}
    
    /* GLASS CONTAINER */
    .neural-container {
        background: var(--glass);
        backdrop-filter: blur(20px);
        border: 1px solid var(--border-color);
        border-radius: 2px;
        padding: 25px;
        position: relative;
        overflow: hidden;
    }

    .neural-container::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, var(--primary), transparent);
        animation: scan 3s linear infinite;
    }

    @keyframes scan {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }

    /* TYPOGRAPHY */
    h1, h2, h3 {
        font-family: 'Syncopate', sans-serif !important;
        letter-spacing: 4px !important;
        text-transform: uppercase;
    }

    .status-text {
        font-size: 10px;
        color: var(--primary);
        text-shadow: 0 0 10px var(--primary);
        letter-spacing: 2px;
    }

    /* INPUT FIELD OVERHAUL */
    .stTextInput input {
        background: transparent !important;
        border: none !important;
        border-bottom: 2px solid var(--border-color) !important;
        color: var(--primary) !important;
        font-size: 24px !important;
        text-align: center;
        transition: 0.5s;
    }

    .stTextInput input:focus {
        border-bottom: 2px solid var(--primary) !important;
        box-shadow: 0 10px 20px -10px var(--primary) !important;
    }

    /* BUTTON ACTION */
    .stButton button {
        background: transparent !important;
        border: 1px solid var(--primary) !important;
        color: var(--primary) !important;
        border-radius: 0px !important;
        padding: 10px 40px !important;
        font-family: 'Syncopate' !important;
        transition: 0.4s !important;
        width: auto !important;
        margin: 0 auto;
        display: block;
    }

    .stButton button:hover {
        background: var(--primary) !important;
        color: black !important;
        box-shadow: 0 0 30px var(--primary);
    }

    /* VECTOR CARD */
    .vector-shard {
        background: rgba(255, 255, 255, 0.03);
        border-left: 4px solid var(--primary);
        padding: 15px;
        margin-bottom: 15px;
        transition: 0.3s;
        cursor: crosshair;
    }

    .vector-shard:hover {
        background: rgba(0, 255, 170, 0.1);
        transform: scale(1.02) translateX(10px);
    }

    /* SCROLLBAR */
    ::-webkit-scrollbar { width: 3px; }
    ::-webkit-scrollbar-thumb { background: var(--primary); }

</style>
""", unsafe_allow_html=True)

# --- 3. LOGIC (GROQ) ---
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except:
    st.error("GROQ_API_KEY NOT DETECTED IN SECRETS")
    st.stop()

def get_cognitive_trace(user_input):
    system_prompt = "You are a Neural Engine. Perform an exhaustive Deep Layer Cognition Trace. Break down semantics, retrieval nodes, and dialectical contradictions. Output raw analytical thoughts."
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_input}],
        temperature=0.8, max_tokens=2500
    )
    return response.choices[0].message.content

def distill_queries(raw_text):
    system_prompt = 'Extract exactly 4 highly optimized search queries for deep research based on this trace. Output JSON: {"queries": ["q1", "q2", "q3", "q4"]}'
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": raw_text}],
        temperature=0.1, response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content).get("queries", [])

# --- 4. HUD LAYOUT ---

# TOP BAR
st.markdown(f"""
<div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
    <div class="status-text">SYSTEM: ONLINE | KERNEL: V2.0.4</div>
    <div class="status-text" style="color: #ff3300;">LATENCY: {random.randint(5,15)}MS | THREAT_LEVEL: NULL</div>
    <div class="status-text">COORDINATES: 40.7128° N, 74.0060° W</div>
</div>
""", unsafe_allow_html=True)

st.write("<br>", unsafe_allow_html=True)

# CENTRAL CONTROL
c_head = st.columns([1, 2, 1])
with c_head[1]:
    st.markdown("<h1 style='text-align: center; font-size: 3rem; margin-bottom: 0;'>ORBITAL</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #555; letter-spacing: 10px; margin-top: -10px;'>COGNITIVE COMMAND CENTER</p>", unsafe_allow_html=True)
    query = st.text_input("QUERY", placeholder=">>> TYPE COMMAND HERE", label_visibility="collapsed")
    run = st.button("EXECUTE TRACE")

st.write("---")

# DATA HUD
if run and query:
    with st.spinner("SYNAPSES FIRING..."):
        trace = get_cognitive_trace(query)
        queries = distill_queries(trace)

    col_trace, col_shards = st.columns([1.5, 1])

    with col_trace:
        st.markdown("<div class='status-text' style='margin-bottom: 10px;'>[01] DEEP_COGNITION_TRACE</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown(f"""
            <div class="neural-container" style="height: 600px; overflow-y: auto;">
                <div style="font-size: 12px; color: #8899aa; line-height: 1.8;">
                    {trace}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with col_shards:
        st.markdown("<div class='status-text' style='margin-bottom: 10px;'>[02] SEARCH_VECTOR_SHARDS</div>", unsafe_allow_html=True)
        for i, q in enumerate(queries):
            st.markdown(f"""
            <div class="vector-shard">
                <div style="font-size: 10px; color: var(--primary); opacity: 0.6;">SHARD_0{i+1}</div>
                <div style="font-size: 14px; font-weight: bold; margin-top: 5px;">{q}</div>
                <div style="text-align: right; font-size: 9px; margin-top: 10px; color: #555;">READY_FOR_EXTRACTION</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button(f"EXTRACT SHARD 0{i+1}", key=f"q_{i}"):
                st.toast(f"Shard {i+1} data cached to clipboard.")

else:
    # EMPTY STATE - RADIAL DECORATION
    st.markdown("""
    <div style="height: 50vh; display: flex; align-items: center; justify-content: center; opacity: 0.2;">
        <div style="text-align: center;">
            <h2 style="font-size: 5rem; margin: 0;">00</h2>
            <p>IDLE_STATE_ACTIVE</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# FOOTER STATS
st.markdown("""
<div style="position: fixed; bottom: 20px; left: 20px; font-size: 10px; color: #444;">
    // ORBITAL_TRACE_ENGINE // POWERED_BY_LLAMA_3.3_70B // NO_LIMITS_DEFINED
</div>
""", unsafe_allow_html=True)
