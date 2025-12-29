import streamlit as st
from openai import OpenAI
from duckduckgo_search import DDGS

# --- SETUP ---
st.set_page_config(page_title="Real GPT-4o Logic", page_icon="🧠")

# --- AMBIL API KEY (VERSI OPENAI) ---
try:
    if "OPENAI_API_KEY" in st.secrets:
        # Kita pakai kunci dari Secrets
        client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    else:
        st.error("⚠️ OpenAI API Key belum dimasukkan di Streamlit Secrets.")
        st.stop()
except Exception as e:
    st.error(f"Error Konfigurasi: {e}")
    st.stop()

# --- FUNGSI UTAMA (GPT-4o BRAIN) ---
def get_gpt_thought(user_input):
    # SYSTEM PROMPT: RAW LOGIC
    # Kita minta GPT-4o untuk jujur: Keyword apa yang dia butuhkan?
    system_instruction = """
    You are the search module of GPT-4o.
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

    response = client.chat.completions.create(
        model="gpt-4o", # MODEL ASLI CHATGPT (Paling Cerdas)
        messages=[
            {"role": "system", "content": system_instruction.format(user_input=user_input)},
        ],
        temperature=0, # Murni logika, nol kreativitas
    )
    return response.choices[0].message.content

# --- UI ---
st.title("🧠 Real GPT-4o Search Logic")
st.markdown("""
**Mesin:** OpenAI GPT-4o (Asli).
Ini adalah simulasi paling akurat karena menggunakan otak yang sama dengan ChatGPT Plus.
Lihat bagaimana dia memutuskan keyword pencariannya.
""")

user_prompt = st.text_input("Prompt User:", placeholder="Contoh: ide konten tiktok untuk jualan baju")

if st.button("🔴 Bongkar Pikiran ChatGPT"):
    if user_prompt:
        try:
            with st.spinner("Menghubungi Server OpenAI (GPT-4o)..."):
                # Ambil respon asli
                raw_response = get_gpt_thought(user_prompt)
                
                # Parsing
                lines = raw_response.split('\n')
                reasoning = "N/A"
                query = user_prompt
                
                for line in lines:
                    if "Reasoning:" in line:
                        reasoning = line.replace("Reasoning:", "").strip()
                    if "Query:" in line:
                        query = line.replace("Query:", "").strip().replace('"', '')

            # HASIL
            st.success("✅ Keputusan GPT-4o:")
            
            st.write("**Alasan (Reasoning):**")
            st.info(reasoning)
            
            st.write("**Keyword yang dicari (Query):**")
            st.code(query, language="text")
            
            # CEK GOOGLE (via DuckDuckGo)
            st.divider()
            st.caption(f"Hasil pencarian nyata untuk: {query}")
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
