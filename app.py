import streamlit as st
from groq import Groq
import json

# --- SETUP ---
st.set_page_config(page_title="Multi-Step Backend Inspector", page_icon="📡", layout="wide")

# --- AMBIL API KEY ---
try:
    if "GROQ_API_KEY" in st.secrets:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    else:
        st.error("⚠️ Masukkan API Key di Secrets.")
        st.stop()
except Exception:
    st.stop()

# --- FUNGSI GENERATOR JSON (MULTI-STEP LOGIC) ---
def get_backend_json_multi(user_input):
    # SYSTEM PROMPT: FORMAT STRICT JSON ARRAY
    # Kita perintahkan AI untuk memecah masalah menjadi BANYAK query (Unlimited/Sesuai kebutuhan).
    system_instruction = """
    You are a Deep Research AI Agent (Headless).
    
    YOUR GOAL: 
    Analyze the user prompt and generate a MULTI-STEP search strategy. 
    Do not limit yourself to one query. Break the problem down into as many queries as needed (prices, reviews, competitors, location, social proof, etc).
    
    RULES:
    1. Output MUST be a valid JSON object.
    2. The core data must be an ARRAY (List) of search steps.
    3. Use the user's language logic (if user implies local intent, use local language).
    
    JSON STRUCTURE:
    {
      "meta_analysis": {
        "user_intent": "...",
        "complexity_level": "..."
      },
      "search_pipeline": [
        {
          "step_id": 1,
          "strategy": "Broad/Specific/Price/Review",
          "query": "..."
        },
        {
          "step_id": 2,
          "strategy": "...",
          "query": "..."
        }
        ... (Add more steps as needed)
      ]
    }
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        temperature=0.2, # Sedikit kreatif agar bisa memecah masalah
        response_format={"type": "json_object"} 
    )
    return response.choices[0].message.content

# --- UI TAMPILAN INSPECT NETWORK ---
st.title("📡 AI Network Inspector (Multi-Step Payload)")
st.markdown("""
**Mode: Deep Decomposition**
Script ini menampilkan bagaimana AI memecah satu perintah menjadi **banyak permintaan server (Batch Request)**.
Lihat bagian `search_pipeline` untuk melihat daftar keyword yang ditembakkan secara bersamaan.
""")

user_prompt = st.text_input("User Prompt:", placeholder="Contoh: strategi jualan kopi kekinian biar laris")

if st.button("🔴 Inspect Network Payload"):
    if user_prompt:
        try:
            with st.spinner("Analyzing & Decomposing Request..."):
                # Ambil Raw JSON
                raw_json_str = get_backend_json_multi(user_prompt)
                
                # Ubah string jadi Object Python
                data_object = json.loads(raw_json_str)
                
                # 1. TAMPILKAN RAW JSON (UNTUK DEBUGGING)
                st.subheader("📡 Full Payload Data")
                st.caption("Ini adalah struktur data lengkap yang dikirim otak AI:")
                st.json(data_object)
                
                # 2. EKSTRAKSI KEYWORD (BIAR GAMPANG DIBACA)
                st.divider()
                st.subheader("🔑 Extracted Search Pipeline")
                st.write("AI memutuskan untuk melakukan pencarian berikut secara paralel:")
                
                # Kita loop array 'search_pipeline'
                pipeline = data_object.get("search_pipeline", [])
                
                if pipeline:
                    for item in pipeline:
                        # Tampilkan strategi dan query
                        st.markdown(f"**Langkah {item.get('step_id')}: {item.get('strategy')}**")
                        st.code(item.get('query'), language="text")
                else:
                    st.warning("JSON valid, tapi tidak ada pipeline yang ditemukan.")

        except Exception as e:
            st.error(f"Error: {e}")
