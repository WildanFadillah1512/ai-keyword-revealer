import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
import re

# --- SETUP ---
st.set_page_config(page_title="Raw AI Consciousness", page_icon="🧠", layout="wide")

try:
    if "GROQ_API_KEY" in st.secrets:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
    else:
        st.error("⚠️ Masukkan API Key di Secrets.")
        st.stop()
except Exception:
    st.stop()

# --- FUNGSI PIKIRAN MENTAH (UNFILTERED) ---
def get_raw_stream(user_input):
    # SYSTEM PROMPT: BEBAS TANPA BATAS
    # Kita menyuruh AI untuk melakukan "Deep Research Planning".
    # Tidak ada batasan jumlah query. Biarkan dia membanjiri kita dengan data.
    system_instruction = """
    You are an AI Research Engine performing a deep dive analysis.
    
    USER PROMPT: "{user_input}"
    
    YOUR GOAL:
    You need to gather ALL possible information to answer this request perfectly.
    Don't just look for one thing. Look for prices, reviews, competitors, locations, social proof, Reddit discussions, everything.
    
    INSTRUCTION:
    Dump your raw internal search plan. 
    List EVERY SINGLE keyword string you would type into Google. 
    If you need 10 queries, generate 10. If you need 20, generate 20.
    
    FORMAT (STRICTLY ONE PER LINE):
    >> QUERY: [Your Search String Here]
    >> QUERY: [Your Search String Here]
    ...
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_instruction.format(user_input=user_input)},
        ],
        temperature=0.6, # Sedikit dinaikkan agar AI lebih liar/eksploratif dalam mencari ide
        max_tokens=1000  # Kita beri ruang luas agar dia tidak terpotong
    )
    return response.choices[0].message.content

# --- UI ---
st.title("🧠 AI Unfiltered Consciousness")
st.markdown("""
**Ini adalah Logika Tanpa Filter.**
Script ini tidak membatasi AI. Jika AI merasa perlu mencari 15 hal berbeda untuk menjawab Anda, dia akan melakukannya.
Inilah representasi paling akurat dari "Multi-Step Reasoning" yang dilakukan AI canggih.
""")

user_prompt = st.text_input("Prompt User:", placeholder="Misal: strategi marketing untuk jualan basreng pedas")

if st.button("🔴 Buka Pikiran AI"):
    if user_prompt:
        try:
            with st.spinner("AI sedang melakukan Deep Thinking..."):
                # 1. DAPATKAN RAW TEXT
                raw_text = get_raw_stream(user_prompt)
                
                # 2. TAMPILKAN MENTAHNYA (SEPERTI LOG SERVER)
                st.subheader("📝 Raw Internal Log")
                st.text_area("Apa yang ada di otak AI:", value=raw_text, height=300)
                
                # 3. EKSTRAKSI QUERY (Untuk pembuktian)
                # Kita cari semua baris yang diawali ">> QUERY:"
                queries = re.findall(r">> QUERY: (.*)", raw_text)
                
                if queries:
                    st.success(f"✅ AI Memutuskan untuk melakukan {len(queries)} pencarian sekaligus!")
                    
                    # Tampilkan list bersih
                    st.write("Daftar Keyword yang dipakai:")
                    for q in queries:
                        st.code(q.strip(), language="text")
                    
                    # 4. SIMULASI PENCARIAN (Ambil 3 Teratas saja biar tidak berat)
                    st.divider()
                    st.write(f"🔎 Mengambil sampel data untuk 3 query pertama...")
                    
                    for i, q in enumerate(queries[:3]):
                        clean_q = q.strip()
                        st.markdown(f"**Mencari: `{clean_q}`**")
                        results = DDGS().text(clean_q, region="wt-wt", safesearch="off", max_results=2)
                        for res in results:
                            with st.expander(f"Hasil: {res['title']}"):
                                st.caption(res['href'])
                                st.write(res['body'])
                else:
                    st.warning("AI memberikan respon naratif, bukan list query. Coba prompt yang lebih spesifik.")

        except Exception as e:
            st.error(f"Error: {e}")
