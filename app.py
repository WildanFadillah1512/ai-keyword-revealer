import streamlit as st
from groq import Groq
import json

# --- SETUP ---
st.set_page_config(page_title="Raw vs Human AI", page_icon="🧠", layout="wide")

# --- CSS: RAW TEXT (BIAR SEPERTI TERMINAL) ---
st.markdown("""
<style>
    .raw-text textarea {
        font-family: 'Courier New', Courier, monospace !important;
        background-color: #1e1e1e !important;
        color: #00ff41 !important; /* Warna Hijau Hacker */
        font-size: 14px;
    }
    .stAlert {
        background-color: #f0f2f6;
        border: 1px solid #dcdcdc;
    }
</style>
""", unsafe_allow_html=True)

# --- API CLIENT ---
try:
    if "GROQ_API_KEY" in st.secrets:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    else:
        st.error("⚠️ Masukkan API Key di Secrets.")
        st.stop()
except Exception:
    st.stop()

# --- FUNGSI 1: GENERATE PIKIRAN MENTAH (RAW STREAM) ---
def get_naked_ai_response(user_input):
    # Prompt ini MEMAKSA AI untuk berantakan (Stream of Consciousness)
    system_instruction = """
    You are an AI Search Brain. 
    User Input: "{user_input}"
    
    INSTRUCTION:
    Dump your raw internal monologue. No formatting. No bullet points. No JSON.
    Just a continuous stream of text analyzing keywords, languages (English/Indonesian), synonyms, and user intent. 
    Critique your own ideas as you type.
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system_instruction.format(user_input=user_input)}],
        temperature=0.7, 
        max_tokens=1500
    )
    return response.choices[0].message.content

# --- FUNGSI 2: TERJEMAHKAN KE BAHASA MANUSIA (TRANSLATOR) ---
def interpret_chaos(raw_text):
    # Prompt ini mengambil teks berantakan tadi, dan merapikannya jadi JSON
    system_instruction = """
    You are an Analyst. I will give you a RAW AI THOUGHT STREAM.
    Your job is to extract the structured data from that chaos.
    
    OUTPUT JSON FORMAT:
    {
        "core_intent": "What is the user actually looking for?",
        "primary_language_logic": "Why did the AI choose Indo/English?",
        "final_keywords": ["keyword1", "keyword2", "keyword3"],
        "strategy_summary": "1 sentence summary of the plan."
    }
    """
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": raw_text} # Kita kirim teks mentah tadi ke sini
        ],
        temperature=0,
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content

# --- UI VISUALISASI ---
st.title("🧠 AI Consciousness: Raw vs Human View")
st.caption("Melihat bagaimana AI berpikir (kiri) dan kesimpulan akhirnya (kanan).")

user_prompt = st.text_input("Masukkan Request:", placeholder="jasa gambar desain")

if st.button("🔍 Mulai Deep Thinking"):
    if user_prompt:
        # STEP 1: DAPATKAN RAW STREAM
        with st.spinner("AI sedang berpikir keras (Generating Raw Stream)..."):
            raw_output = get_naked_ai_response(user_prompt)
        
        # STEP 2: TERJEMAHKAN RAW STREAM
        with st.spinner("Menerjemahkan logika untuk manusia..."):
            human_output_str = interpret_chaos(raw_output)
            human_data = json.loads(human_output_str)

        # --- TAMPILAN DUAL COLUMN ---
        col1, col2 = st.columns(2)

        # KOLOM KIRI: RAW (MENTAH)
        with col1:
            st.subheader("🧬 Raw Stream (Isi Otak)")
            st.markdown("Ini adalah proses berpikir asli tanpa filter:")
            # Class raw-text agar warnanya hitam-hijau
            st.markdown('<div class="raw-text">', unsafe_allow_html=True)
            st.text_area("Log", value=raw_output, height=500, label_visibility="collapsed")
            st.markdown('</div>', unsafe_allow_html=True)

        # KOLOM KANAN: HUMAN READABLE (HASIL OLAHAN)
        with col2:
            st.subheader("👤 Human Readable (Kesimpulan)")
            st.markdown("Ini adalah intisari dari teks panjang di sebelah kiri:")
            
            # Kartu Visual
            with st.container(border=True):
                st.markdown(f"**🎯 Tujuan User (Intent):**")
                st.info(human_data['core_intent'])
                
                st.markdown(f"**🗣️ Logika Bahasa:**")
                st.write(human_data['primary_language_logic'])
                
                st.divider()
                
                st.markdown(f"**🔑 Keyword Final Pilihan AI:**")
                # Tampilkan keyword sebagai tags/code
                for kw in human_data['final_keywords']:
                    st.code(kw, language="text")
                
                st.divider()
                st.caption(f"**Strategi:** {human_data['strategy_summary']}")

        st.success("✅ Proses Selesai. Kiri adalah proses mental, Kanan adalah keputusan eksekutif.")
