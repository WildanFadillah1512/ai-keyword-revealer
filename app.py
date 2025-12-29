import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# --- CONFIG ---
st.set_page_config(page_title="Deep AI Search Logic", page_icon="🧬")

# --- SECRETS ---
try:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        st.error("⚠️ API Key hilang.")
        st.stop()
except Exception:
    st.stop()

# --- FUNGSI OTAK (DECOMPOSITION LOGIC) ---
def get_real_backend_queries(user_input, key):
    client = Groq(api_key=key)
    
    # SYSTEM PROMPT LEVEL DEWA
    # Kita menyuruh AI bertindak sebagai "Query Understanding Module"
    # Bukan sekadar penerjemah, tapi pemecah masalah.
    system_instruction = """
    ROLE: You are the 'Multi-Hop Query Generator' for a Search Engine.
    
    TASK: 
    The user asks a question. You need to break it down into 3 DISTINCT search types to get a complete answer.
    Do NOT just translate. Think about WHERE the data lives.
    
    GENERATE 3 QUERIES (Comma Separated):
    1. **Broad Authority Search (English):** Search for "Best/Top" lists or general knowledge. Usually in English for better data.
    2. **Specific Local Search (Local Language):** Search for specific price, location, or local intent. Keep it in the user's language.
    3. **Footprint/Platform Search:** Search specifically on platforms like 'site:instagram.com', 'site:linkedin.com', or 'reviews'.
    
    EXAMPLE INPUT: "Jasa desain rumah di Sukabumi"
    EXAMPLE OUTPUT: best architecture firms sukabumi indonesia, biaya jasa arsitek sukabumi 2025, site:instagram.com arsitek sukabumi project
    
    OUTPUT FORMAT: Just the 3 query strings separated by comma. No labels.
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_input}
        ],
        temperature=0.4, # Sedikit kreatif untuk memikirkan variasi
    )
    return completion.choices[0].message.content

# --- UI ---
st.title("🧬 Deep AI Search Logic (Decomposition)")
st.markdown("""
**Ini adalah simulasi yang lebih Real.**
AI asli tidak hanya mencari 1 kata kunci. Mereka memecah pencarian menjadi 3 jenis data:
1. **Otoritas Global** (Biasanya Inggris)
2. **Intent Lokal** (Bahasa Lokal/Harga)
3. **Jejak Digital** (Instagram/Review/Forum)
""")

user_prompt = st.text_input("Prompt User:", placeholder="Misal: rekomendasi catering diet di jakarta selatan")

if st.button("🧬 Bongkar Logika AI"):
    if user_prompt:
        with st.spinner("Mengurai logika pencarian..."):
            queries_raw = get_real_backend_queries(user_prompt, api_key)
            query_list = [q.strip() for q in queries_raw.split(',')]
            
            st.success("✅ AI Memecah Strategi Menjadi 3 Arah:")
            
            # Kita mapping manual agar user paham maksudnya
            labels = ["🌍 1. Pencarian Otoritas (Global/Inggris)", "🇮🇩 2. Pencarian Spesifik (Lokal)", "👣 3. Pencarian Jejak (Platform/Review)"]
            
            for i, q in enumerate(query_list):
                if i < 3:
                    st.markdown(f"**{labels[i]}**")
                    st.code(q, language="text")
            
            # Tes salah satu
            st.divider()
            target_kw = query_list[0] # Kita ambil yang Global/Inggris biasanya paling relevan buat AI
            st.write(f"Mari kita lihat hasil untuk query otoritas: **{target_kw}**")
            
            results = DDGS().text(target_kw, region="wt-wt", safesearch="off", max_results=3)
            for res in results:
                with st.expander(res['title'], expanded=True):
                    st.caption(res['href'])
                    st.write(res['body'])
