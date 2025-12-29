import streamlit as st
from groq import Groq
import json
import time

# --- 1. CONFIGURATION & PAGE SETUP ---
st.set_page_config(
    page_title="Neural Search Interface", 
    page_icon="💠", 
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. ADVANCED CSS STYLING (THE UI MAGIC) ---
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0e1117;
    }
    
    /* TERMINAL STYLE (Left Column) */
    .neural-terminal {
        background-color: #000000;
        border: 1px solid #333;
        border-left: 3px solid #00ff41;
        padding: 15px;
        border-radius: 5px;
        font-family: 'Courier New', Courier, monospace;
        color: #00ff41; /* Hacker Green */
        font-size: 13px;
        line-height: 1.4;
        height: 550px;
        overflow-y: auto;
        box-shadow: inset 0 0 10px #000;
    }
    
    /* CARD STYLE (Right Column) */
    .insight-card {
        background-color: #1e2530;
        border: 1px solid #2e3b4e;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    
    .insight-title {
        color: #a0aab5;
        font-size: 0.9em;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
        font-weight: 600;
    }
    
    .insight-value {
        color: #ffffff;
        font-size: 1.1em;
        font-weight: 500;
    }
    
    /* KEYWORD BADGES */
    .kw-badge {
        display: inline-block;
        background-color: #2b313e;
        color: #4fd1c5;
        padding: 5px 10px;
        border-radius: 15px;
        font-size: 0.85em;
        margin: 3px;
        border: 1px solid #4fd1c5;
    }

    /* INPUT FIELD STYLING */
    .stTextInput > div > div > input {
        background-color: #161b22;
        color: white;
        border: 1px solid #30363d;
        border-radius: 8px;
        padding: 10px;
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

# --- 4. CORE LOGIC FUNCTIONS ---

def get_raw_consciousness(user_input):
    """Mendapatkan aliran pikiran mentah tanpa filter"""
    system_prompt = """
    ROLE: You are the core search algorithm of a supercomputer.
    TASK: Analyze the user request. Stream your consciousness strictly.
    RULES: 
    1. NO polite intros. NO formatting.
    2. Dump raw logic about intent, language choice, synonyms, and query variations.
    3. Mix English/Indonesian freely as you process.
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"QUERY: {user_input}"}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    return response.choices[0].message.content

def synthesize_insight(raw_text):
    """Menerjemahkan pikiran mentah menjadi data terstruktur JSON"""
    system_prompt = """
    ROLE: Data Analyst.
    TASK: Extract structured insights from the provided Raw AI Thought Trace.
    OUTPUT FORMAT: JSON ONLY.
    {
        "user_intent": "Brief description of what user wants (e.g. Transactional, Informational)",
        "language_context": "Why did AI choose specific language?",
        "search_difficulty": "Easy/Medium/Hard",
        "primary_keywords": ["kw1", "kw2", "kw3", "kw4"],
        "strategy_note": "One sentence summary of the plan"
    }
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": raw_text}
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

# --- 5. UI LAYOUT ---

st.title("💠 Neural Search Engine")
st.markdown("Interface visualisasi proses berpikir AI: **Logika Mentah vs Analisis Terstruktur**.")

# Input Section (Centered and Clean)
with st.container():
    col_in1, col_in2 = st.columns([4, 1])
    with col_in1:
        user_query = st.text_input("Input Data / Keyword:", placeholder="contoh: rekomendasi laptop coding murah", label_visibility="collapsed")
    with col_in2:
        analyze_btn = st.button("🚀 PROCESS", use_container_width=True)

# Main Processing Area
if analyze_btn and user_query:
    
    # Progress Bar UI Effect
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # STEP 1: RAW THINKING
        status_text.caption("🔌 Connecting to Neural Core...")
        progress_bar.progress(20)
        time.sleep(0.5) # Efek dramatis sedikit
        
        status_text.caption("🧠 Streaming Consciousness...")
        raw_trace = get_raw_consciousness(user_query)
        progress_bar.progress(60)
        
        # STEP 2: SYNTHESIZING
        status_text.caption("📊 Synthesizing Logic Structure...")
        structured_data_str = synthesize_insight(raw_trace)
        structured_data = json.loads(structured_data_str)
        progress_bar.progress(100)
        time.sleep(0.3)
        progress_bar.empty()
        status_text.empty()

        # --- DUAL COLUMN RESULT ---
        c_left, c_right = st.columns([1, 1])

        # === KOLOM KIRI: RAW TERMINAL ===
        with c_left:
            st.subheader("📟 Raw Neural Trace")
            st.markdown(f"""
            <div class="neural-terminal">
            > INITIATING SEQUENCE...<br>
            > INPUT RECEIVED: "{user_query}"<br>
            > -------------------------<br>
            {raw_trace.replace(chr(10), '<br>')}
            <br>> -------------------------<br>
            > END OF STREAM.
            </div>
            """, unsafe_allow_html=True)

        # === KOLOM KANAN: HUMAN INSIGHTS ===
        with c_right:
            st.subheader("🛡️ Executive Summary")
            
            # Card 1: Intent & Difficulty
            st.markdown(f"""
            <div class="insight-card">
                <div style="display: flex; justify-content: space-between;">
                    <div>
                        <div class="insight-title">User Intent</div>
                        <div class="insight-value">🎯 {structured_data.get('user_intent', 'N/A')}</div>
                    </div>
                    <div>
                        <div class="insight-title">Complexity</div>
                        <div class="insight-value">⚡ {structured_data.get('search_difficulty', 'N/A')}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Card 2: Context
            st.markdown(f"""
            <div class="insight-card">
                <div class="insight-title">Language Logic</div>
                <div class="insight-value" style="font-size: 0.95em; color: #d1d5db;">
                    {structured_data.get('language_context', 'N/A')}
                </div>
                <hr style="border-color: #333; margin: 10px 0;">
                <div class="insight-title">Strategy</div>
                <div class="insight-value" style="font-size: 0.95em; color: #d1d5db; font-style: italic;">
                    "{structured_data.get('strategy_note', 'N/A')}"
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Card 3: Keywords
            st.markdown('<div class="insight-title" style="margin-left: 5px;">GENERATED OPTIMIZED KEYWORDS</div>', unsafe_allow_html=True)
            
            # Generate HTML Badges for Keywords
            keywords_html = ""
            for kw in structured_data.get('primary_keywords', []):
                keywords_html += f'<span class="kw-badge">{kw}</span>'
            
            st.markdown(f"""
            <div class="insight-card" style="border: 1px solid #4fd1c5;">
                {keywords_html}
            </div>
            """, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"System Malfunction: {e}")
