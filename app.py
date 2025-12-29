import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# --- SETUP ---
st.set_page_config(page_title="Raw AI Logic (Free)", page_icon="🧠")

# --- AMBIL API KEY (GROQ) ---
try:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
        client = Groq(api_key=api_key)
    else:
        st.error("⚠️ GROQ API Key belum dimasukkan di Streamlit Secrets.")
        st.stop()
except Exception as e:
    st.error(f"Error Konfigurasi: {e}")
    st.stop()

# --- FUNGSI UTAMA (LLAMA 3.3 RAW LOGIC) ---
def get_ai_thought(user_input):
    # SYSTEM PROMPT: RAW LOGIC (Sama persis dengan versi GPT-4o tadi)
    system_instruction = """
    You are the search module of a Super Intelligent AI.
    User Input: "{user_input}"
    
    Task: 
    To answer this user strictly and accurately, determine the BEST Google Search Query.
    
    Constraints:
    1. Do not try to be helpful to the user yet. focus on retrieving data.
    2. Choose the language (English vs Indonesian) based on where the best data resides.
    
    Output Format:
    Reasoning: [Short reason why you chose this query]
    Query: [The exact search string]
    """

    # Kita pakai Llama 3.3 70B (Model paling pintar di Groq, setara GPT-4)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile", 
        messages=[
            {"role": "system", "content": system_instruction.format(user_input=user_input)},
        ],
        temperature=0, # Logika Murni (Robot)
    )
    return response.choices[0].message.content

# --- UI ---
st.title("🧠 AI Search Logic (Raw Llama 3.3)")
st.markdown("""
**Mesin:** Llama 3.3 70B (via Groq).
Model ini memiliki kecerdasan setara GPT-4.
Settingan ini menggunakan **Temperature 0** (Logika Murni) tanpa rekayasa prompt bahasa.
""")

user_prompt = st.text_input("Prompt User:", placeholder="Contoh: jasa arsitek sukabumi")

if st.button("🔴 Bongkar Pikiran AI"):
    if user_prompt:
        try:
            with st.spinner("Mengakses Neural Network..."):
                # Ambil respon asli
                raw_response = get_ai_thought(user_prompt)
                
                # Parsing Manual
                lines = raw_response.split('\n')
                reasoning = "N/A"
                query = user_prompt
                
                for line in lines:
                    if "Reasoning:" in line:
                        reasoning = line.replace("Reasoning:", "").strip()
                    if "Query:" in line:
                        query = line.replace("Query:", "").strip().replace('"', '')

            # HASIL
            st.success("✅ Keputusan Algoritma:")
            
            st.write("**Alasan (Reasoning):**")
            st.info(reasoning)
            
            st.write("**Keyword yang dicari (Query):**")
            st.code(query, language="text")
            
            # CEK SEARCH ENGINE
            st.divider()
            st.caption(f"Hasil pencarian nyata untuk: {query}")
            # Region kita set 'wt-wt' (World) biar adil kalau keyword inggris
            results = DDGS().text(query, region="wt-wt", safesearch="off", max_results=3)
            
            if results:
                for res in results:
                    st.markdown(f"**[{res['title']}]({res['href']})**")
                    st.write(res['body'])
                    st.markdown("---")
            else:
                st.warning("Tidak ada hasil search.")

        except Exception as e:
            st.error(f"Error: {e}")
