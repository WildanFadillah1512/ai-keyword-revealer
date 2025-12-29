import streamlit as st
from groq import Groq
import json

# --- SETUP TAMPILAN ---
st.set_page_config(page_title="KERNEL LEVEL INSPECTOR", page_icon="☢️", layout="wide")

# --- CSS HACK UNTUK TAMPILAN SEPERTI TERMINAL HACKER ---
st.markdown("""
<style>
    .stApp {background-color: #0e1117;}
    .stJson {background-color: #1e1e1e; color: #00ff41; font-family: 'Courier New', monospace;}
    div[data-testid="stMarkdownContainer"] {color: #e6e6e6;}
</style>
""", unsafe_allow_html=True)

# --- AMBIL API KEY ---
try:
    if "GROQ_API_KEY" in st.secrets:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    else:
        st.error("⚠️ Masukkan API Key di Secrets.")
        st.stop()
except Exception:
    st.stop()

# --- FUNGSI 'BRAIN DUMP' ---
def get_kernel_dump(user_input):
    # SYSTEM PROMPT: MEMAKSA MODE 'DEBUG KERNEL'
    # Kita perintahkan AI untuk tidak menjadi asisten, tapi menjadi mesin pemroses data.
    # Output WAJIB JSON kompleks yang menunjukkan 'Neural Activation'.
    system_instruction = """
    ACT AS: Neural Search Engine Backend (Kernel Level).
    
    TASK: Process the user input and output the RAW INTERNAL EXECUTION LOG in JSON format.
    
    CONSTRAINTS:
    1. NO polite text. NO markdown explanation. ONLY JSON.
    2. Reveal your internal "confidence_score" (0.0 to 1.0).
    3. Reveal your "raw_thought_trace" (The unfiltered logic flow).
    4. Break down the query into "search_vectors".
    
    JSON SCHEMA STRUCTURE:
    {
      "timestamp_simulation": "UnixEpoch",
      "input_processing": {
        "detected_language": "...",
        "complexity_assessment": "Low/Medium/High",
        "ambiguity_check": "..."
      },
      "neural_reasoning": {
        "raw_thought_trace": "String of consciousness. Explain exactly why you choose specific keywords without filtering.",
        "confidence_score": 0.95
      },
      "execution_plan": {
        "primary_strategy": "...",
        "search_vectors": [
            {"priority": 1, "type": "navigational/transactional", "query_string": "..."},
            {"priority": 2, "type": "...", "query_string": "..."}
        ]
      }
    }
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        temperature=0.1, # Hampir beku, logika murni
        response_format={"type": "json_object"} # FORCE JSON
    )
    return response.choices[0].message.content

# --- UI UTAMA ---
st.title("☢️ AI KERNEL DUMP (Raw Data)")
st.caption("Melihat langsung struktur data JSON yang dikirim oleh otak AI ke server.")

user_prompt = st.text_input("Input Data:", placeholder="jasa arsitek sukabumi", value="jasa desain arsitek di sukabumi")

if st.button("EXECUTE KERNEL TRACE"):
    if user_prompt:
        try:
            with st.spinner("Decrypting Neural Pathways..."):
                # Ambil data mentah
                raw_data = get_kernel_dump(user_prompt)
                json_data = json.loads(raw_data)
                
                # TAMPILKAN JSON MENTAH (Ini yang dilihat developer)
                st.subheader("📡 Backend Payload")
                st.json(json_data)
                
                # EKSTRAKSI UNTUK MANUSIA
                st.divider()
                st.markdown("### 🧠 Analisis Pikiran (Extracted)")
                
                trace = json_data['neural_reasoning']['raw_thought_trace']
                vectors = json_data['execution_plan']['search_vectors']
                
                st.write("**Logika Mentah:**")
                st.code(trace, language="text")
                
                st.write("**Keputusan Query Akhir:**")
                for v in vectors:
                    st.success(f"Priority {v['priority']} ({v['type']}): {v['query_string']}")

        except Exception as e:
            st.error(f"System Error: {e}")
