import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Llama 3 SEO Hunter", page_icon="🦙")

# --- AMBIL API KEY DARI SECRETS (BRANKAS) ---
try:
    if "GROQ_API_KEY" in st.secrets:
        api_key = st.secrets["GROQ_API_KEY"]
    else:
        st.error("⚠️ API Key belum dimasukkan di Streamlit Secrets.")
        st.stop()
except Exception as e:
    st.error(f"Terjadi kesalahan saat membaca Secrets: {e}")
    st.stop()

# --- JUDUL & DESKRIPSI ---
st.title("🦙 Llama 3 Keyword Hunter")
st.markdown("""
**Mesin:** Llama 3 (via Groq) + DuckDuckGo.
**Status:** ✅ Aman, Cepat, Gratis, Tanpa Limit Google.
""")

# --- FUNGSI UTAMA ---
def get_keywords_from_groq(prompt, key):
    client = Groq(api_key=key)
    
    system_instruction = """
    Kamu adalah pakar SEO Keyword Research.
    Tugas: Berikan 5 ide keyword 'long-tail' yang spesifik dan volume tinggi untuk topik user.
    Format Output: HANYA daftar keyword dipisahkan koma. Tanpa teks lain.
    Contoh: jasa arsitek murah, desain rumah minimalis 2025, kontraktor terpercaya
    """

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6,
    )
    return completion.choices[0].message.content

# --- INPUT USER ---
user_prompt = st.text_input("Masukkan Topik Bisnis:", placeholder="Contoh: Jasa cuci sepatu di Jakarta Selatan")

if st.button("🚀 Cari Keyword & Data"):
    if user_prompt:
        try:
            # 1. TAHAP AI (GROQ)
            with st.spinner("🦙 Llama 3 sedang berpikir..."):
                keywords_raw = get_keywords_from_groq(user_prompt, api_key)
                keyword_list = [k.strip() for k in keywords_raw.split(',')]
            
            # Tampilkan Keyword
            st.success("✅ Keyword SEO Ditemukan!")
            cols = st.columns(len(keyword_list[:3]))
            for i, kw in enumerate(keyword_list[:3]):
                with cols[i]:
                    st.code(kw, language="text")
            
            if len(keyword_list) > 3:
                st.caption("Alternatif: " + ", ".join(keyword_list[3:]))

            # 2. TAHAP SEARCH (DUCKDUCKGO)
            st.divider()
            target_kw = keyword_list[0]
            st.subheader(f"🌐 Data Kompetitor: {target_kw}")
            
            with st.spinner("🔍 Sedang mencari data di internet..."):
                results = DDGS().text(target_kw, region="id-id", safesearch="off", max_results=4)
                
                if results:
                    for res in results:
                        with st.expander(res['title'], expanded=True):
                            st.write(res['body'])
                            st.markdown(f"[Kunjungi Website]({res['href']})")
                else:
                    st.warning("Data tidak ditemukan di pencarian.")

        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Masukkan topik dulu bosku.")
