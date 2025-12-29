import streamlit as st
from groq import Groq
import json

# --- SETUP ---
st.set_page_config(page_title="Backend JSON Inspector", page_icon="👨‍💻", layout="wide")

# --- AMBIL API KEY ---
try:
    if "GROQ_API_KEY" in st.secrets:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    else:
        st.error("⚠️ Masukkan API Key di Secrets.")
        st.stop()
except Exception:
    st.stop()

# --- FUNGSI GENERATOR JSON (BACKEND LOGIC) ---
def get_backend_json(user_input):
    # SYSTEM PROMPT: FORMAT STRICT JSON
    # Kita menyuruh AI berhenti jadi chatbot, dan berubah jadi mesin pemroses data.
    # Output WAJIB format JSON, persis seperti data yang lalu lalang di Inspect Network.
    system_instruction = """
    You are a headless AI Search Agent.
    
    Your goal: Analyze the user prompt and construct a JSON object to trigger a search engine API.
    
    RULES:
    1. Do NOT speak to the user.
    2. OUTPUT ONLY VALID JSON.
    3. Determine the 'search_query' based on the most effective keyword (English or Local).
    4. Determine 'intent' (informational/transactional/navigational).
    
    JSON STRUCTURE:
    {
      "tool_used": "google_search_v2",
      "user_intent": "...",
      "detected_language": "...",
      "search_query_optimized": "..."
    }
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        temperature=0, # Logika Murni
        response_format={"type": "json_object"} # MEMAKSA OUTPUT JADI JSON MURNI
    )
    return response.choices[0].message.content

# --- UI TAMPILAN INSPECT NETWORK ---
st.title("👨‍💻 AI Network Inspector (JSON View)")
st.markdown("""
**Mode Debug:** Menampilkan *Raw Payload* yang dikirim otak AI ke Search Engine.
Ini adalah tampilan yang biasa dilihat developer saat membuka **Inspect Element -> Network**.
""")

user_prompt = st.text_input("User Prompt:", placeholder="jasa arsitek sukabumi")

if st.button("🔴 Inspect Network"):
    if user_prompt:
        try:
            with st.spinner("Intercepting Data Packets..."):
                # Ambil Raw JSON
                raw_json_str = get_backend_json(user_prompt)
                
                # Ubah string jadi Object Python biar rapi
                data_object = json.loads(raw_json_str)
                
                # TAMPILAN SEPERTI INSPECT ELEMENT
                st.subheader("📡 Payload Data (Request Body)")
                st.caption("Ini adalah data asli yang dipikirkan AI:")
                
                # Tampilkan JSON Mentah
                st.json(data_object)
                
                # Highlight Keywordnya saja
                st.divider()
                keyword = data_object.get("search_query_optimized", "Error")
                st.success(f"🔑 **Extracted Keyword:** {keyword}")
                st.info("👆 Gunakan keyword di atas untuk judul artikel Anda.")

        except Exception as e:
            st.error(f"Error: {e}")
