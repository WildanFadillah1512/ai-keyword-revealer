import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Real AI Search Log", page_icon="⚙️")

# --- AMBIL API KEY ---
try:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        st.error("⚠️ API Key belum dimasukkan di Streamlit Secrets.")
        st.stop()
except Exception as e:
    st.error(f"Error Secrets: {e}")
    st.stop()

# --- HEADER ---
st.title("⚙️ AI Backend Search Log")
st.markdown("""
**Status:** Mode "Raw Intelligence".
Script ini meniru perilaku asli LLM Besar (Gemini/GPT). 
Meskipun Prompt Anda **Bahasa Indonesia**, AI seringkali melakukan searching dalam **Bahasa Inggris** karena database global jauh lebih lengkap. Inilah keyword "rahasia" yang mereka pakai.
""")

# --- FUNGSI UTAMA (LOGIKA AI ASLI) ---
def get_ai_search_queries(user_input, key):
    client = Groq(api_key=key)
    
    # SYSTEM PROMPT: MEMAKSA AI MENGGUNAKAN LOGIKA DATABASE GLOBAL
    system_instruction = """
    ROLE: You are the internal "Search Retrieval System" of a Super-Intelligent AI.
    
    CONTEXT: 
    The user gives a prompt in their local language (e.g., Indonesian).
    However, as an AI, you know that the BEST and MOST COMPLETE information is usually found in ENGLISH sources.
    
    YOUR TASK:
    Generate 3-5 Google Search Queries to answer the user's prompt.
    
    CRITICAL RULE (THE "REAL" AI BEHAVIOR):
    Even if the user asks in INDONESIAN, you should usually convert the search queries into ENGLISH to get the best global results. 
    (Or use a mix of English and Local Language if it's a very specific local location).
    
    OUTPUT FORMAT:
    Just the keywords/queries separated by comma. No other text.
    """

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"User Prompt: '{user_input}'. Generate English/Global search queries for this."}
        ],
        temperature=0.3, 
    )
    return completion.choices[0].message.content

# --- INPUT USER ---
user_prompt = st.text_input("Masukkan Prompt Bahasa Indonesia:", placeholder="Contoh: cara mengobati sakit gigi alami")

if st.button("🔓 Bongkar Query Asli AI"):
    if user_prompt:
        try:
            # 1. TAHAP AI BERPIKIR (LOGIKA GLOBAL)
            with st.spinner("⚙️ Mengakses otak AI (Translating to Global Context)..."):
                queries_raw = get_ai_search_queries(user_prompt, api_key)
                
                clean_queries = queries_raw.replace('"', '').replace("'", "").split(',')
                query_list = [q.strip() for q in clean_queries if q.strip()]
            
            # 2. TAMPILKAN HASIL
            st.success("✅ Keyword Internal AI (Biasanya Bahasa Inggris):")
            st.write("Ternyata untuk menjawab pertanyaan Anda, AI mencari ini di Google:")
            
            for kw in query_list:
                st.code(kw, language="text")

            # 3. CEK SEARCH ENGINE
            st.divider()
            primary_query = query_list[0]
            st.info(f"🌐 Bukti Pencarian untuk: **'{primary_query}'**")
            
            with st.spinner("Sedang mencari..."):
                # Kita cari tanpa batasan wilayah (wt-wt) karena keywordnya Inggris
                results = DDGS().text(primary_query, region="wt-wt", safesearch="off", max_results=3)
                
                if results:
                    for res in results:
                        with st.container():
                            st.markdown(f"**[{res['title']}]({res['href']})**")
                            st.caption(res['body'])
                            st.markdown("---")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Masukkan prompt dulu.")
