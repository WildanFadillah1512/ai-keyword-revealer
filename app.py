import streamlit as st
from groq import Groq

# --- SETUP ---
st.set_page_config(page_title="Raw AI Stream", page_icon="🧬", layout="wide")

# --- CSS BIAR SEPERTI NOTEPAD ---
st.markdown("""
<style>
    .stTextArea textarea {
        font-family: 'Courier New', Courier, monospace;
        background-color: #f0f2f6;
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)

try:
    if "GROQ_API_KEY" in st.secrets:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    else:
        st.error("⚠️ Masukkan API Key di Secrets.")
        st.stop()
except Exception:
    st.stop()

# --- FUNGSI MURNI TANPA FORMAT ---
def get_naked_ai_response(user_input):
    # SYSTEM PROMPT: SANGAT MINIMALIS
    # Kita hapus semua aturan JSON, hapus aturan kerapian.
    # Kita minta dia "Think Aloud" (Berpikir keras bersuara).
    system_instruction = """
    You are an AI Search Engine Brain.
    
    USER REQUEST: "{user_input}"
    
    INSTRUCTION:
    Do not be a chatbot. Do not be polite.
    Simply DUMP your raw internal thought process on how to find this information.
    Stream your consciousness:
    - Analyze the intent.
    - List every single keyword permutation you would try.
    - If you think of English keywords, write them.
    - If you think of Indonesian keywords, write them.
    - Critique your own keywords.
    
    OUTPUT FORMAT:
    Plain raw text. No Markdown. No Bold. No JSON. Just a wall of text showing your logic.
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_instruction.format(user_input=user_input)},
        ],
        temperature=0.7, # Sedikit tinggi biar dia "ngoceh" lebih natural/liar
        max_tokens=2000  # Biarkan dia bicara panjang
    )
    return response.choices[0].message.content

# --- UI SEDERHANA ---
st.title("🧬 The Naked AI Consciousness")
st.write("Ini adalah output teks mentah tanpa saya atur formatting-nya sama sekali.")

user_prompt = st.text_input("Ketik request Anda:", placeholder="jasa arsitek sukabumi")

if st.button("Buka Pikiran AI (Tanpa Filter)"):
    if user_prompt:
        with st.spinner("Mengambil data mentah..."):
            # Ambil respon
            raw_output = get_naked_ai_response(user_prompt)
            
            # Tampilkan mentah-mentah di Text Area
            st.subheader("RAW OUTPUT:")
            st.text_area("Isi Otak AI:", value=raw_output, height=600)
            
            st.success("☝️ Itu adalah teks asli yang dihasilkan AI. Tidak ada script saya yang mengubahnya.")
