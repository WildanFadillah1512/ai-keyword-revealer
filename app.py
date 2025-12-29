import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI API KEY (SESUAI KEY ANDA) ---
API_KEY = "AIzaSyDOSXR9-WF-quua7OS5_Xa1S6sY8fYpOQk"
genai.configure(api_key=API_KEY)

# --- SETTING TAMPILAN HALAMAN ---
st.set_page_config(
    page_title="AI Search Keyword Tracker", 
    page_icon="🕵️‍♂️", 
    layout="centered"
)

# --- HEADER APLIKASI ---
st.title("🕵️‍♂️ AI Search Keyword Revealer")
st.markdown("""
Aplikasi ini membantu Anda **membongkar cara berpikir AI**. 
Lihat keyword apa yang dipakai AI saat mencari referensi di Google, lalu gunakan keyword tersebut untuk postingan WordPress Anda.
""")

st.divider()

# --- INPUT PROMPT ---
user_prompt = st.text_input(
    "Masukkan Prompt untuk Riset SEO:", 
    placeholder="Contoh: 10 jasa desain grafis terbaik di sukabumi"
)

# --- PROSES ANALISA ---
if st.button("Bongkar Keyword Sekarang"):
    if user_prompt:
        with st.spinner("Sedang menganalisa jejak pencarian AI..."):
            try:
                # Menggunakan model Gemini 1.5 Flash dengan fitur Google Search
                model = genai.GenerativeModel(
                    model_name='gemini-1.5-flash',
                    tools=[{ "google_search_retrieval": {} }]
                )

                # Meminta AI menjawab prompt
                response = model.generate_content(user_prompt)

                # Ekstraksi Keyword dari Grounding Metadata
                keywords = []
                if hasattr(response.candidates[0], 'grounding_metadata'):
                    metadata = response.candidates[0].grounding_metadata
                    if hasattr(metadata, 'queries'):
                        keywords = metadata.queries
                
                # --- MENAMPILKAN HASIL ---
                st.subheader("🔑 Keyword yang Digunakan AI:")
                
                if keywords:
                    st.write("AI mencari informasi menggunakan kata kunci berikut:")
                    for kw in keywords:
                        # Menampilkan keyword dengan kotak kode agar mudah di-copy
                        st.code(kw, language="text")
                    
                    st.success("✅ **Saran Strategi:** Buatlah artikel di WordPress Anda dengan Judul (H1) yang mengandung keyword di atas.")
                else:
                    st.warning("⚠️ AI memberikan jawaban berdasarkan database internal tanpa melakukan pencarian Google. Coba gunakan prompt yang mencari 'Rekomendasi' atau 'Terbaru'.")

                st.divider()

                # Menampilkan Jawaban Final AI
                with st.expander("Lihat Jawaban Lengkap AI"):
                    st.write(response.text)

            except Exception as e:
                st.error(f"Terjadi kesalahan teknis: {e}")
    else:
        st.warning("Harap masukkan prompt terlebih dahulu.")

# --- FOOTER ---
st.markdown("---")
st.caption("Alat Riset AEO (AI Engine Optimization) - Khusus untuk Jasa Desain Sukabumi")
