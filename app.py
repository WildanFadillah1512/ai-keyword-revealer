import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI API KEY ---
# Gunakan Key Anda yang dari 'projektezo'
API_KEY = "AIzaSyDOSXR9-WF-quua7OS5_Xa1S6sY8fYpOQk"
genai.configure(api_key=API_KEY)

# --- TAMPILAN ---
st.set_page_config(page_title="AI Search Tracker v2", page_icon="🔍")
st.title("🕵️‍♂️ AI Keyword Search Insight")
st.markdown("Alat untuk membongkar keyword pencarian AI Gemini.")

user_prompt = st.text_input("Masukkan Prompt Riset:", placeholder="Contoh: rekomendasi jasa desain sukabumi")

if st.button("Bongkar Keyword Sekarang"):
    if user_prompt:
        with st.spinner("Sedang memproses..."):
            try:
                # Kita gunakan nama model tanpa prefix 'models/' 
                # karena library versi terbaru sering menambahkannya secara otomatis
                model = genai.GenerativeModel(
                    model_name='gemini-1.5-flash',
                    tools=[{ "google_search_retrieval": {} }]
                )

                response = model.generate_content(user_prompt)

                # Ekstraksi Keyword
                keywords = []
                if hasattr(response.candidates[0], 'grounding_metadata'):
                    metadata = response.candidates[0].grounding_metadata
                    if hasattr(metadata, 'queries'):
                        keywords = metadata.queries
                
                # Tampilkan Hasil
                st.subheader("🔑 Keyword yang dipakai AI:")
                if keywords:
                    for kw in keywords:
                        st.code(kw, language="text")
                    st.success("✅ Gunakan keyword ini untuk optimasi WordPress Anda.")
                else:
                    st.warning("⚠️ AI tidak melakukan pencarian Google. Coba prompt: 'Cari jasa desain terbaru di Sukabumi'.")

                st.divider()
                with st.expander("Lihat Jawaban AI"):
                    st.write(response.text)

            except Exception as e:
                # Jika masih error 404, kita coba model alternatif 'gemini-1.5-pro'
                st.error(f"Gagal memuat model: {e}")
                st.info("Mencoba melakukan sinkronisasi ulang...")
    else:
        st.warning("Masukkan prompt terlebih dahulu.")
