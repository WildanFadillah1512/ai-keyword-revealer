import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI API KEY ---
API_KEY = "AIzaSyDOSXR9-WF-quua7OS5_Xa1S6sY8fYpOQk"
genai.configure(api_key=API_KEY)

# --- SETTING TAMPILAN ---
st.set_page_config(page_title="AI Search Tracker", page_icon="🕵️‍♂️")
st.title("🕵️‍♂️ AI Keyword Search Insight")

user_prompt = st.text_input("Masukkan Prompt untuk Riset SEO:", placeholder="Contoh: rekomendasi jasa desain arsitek")

if st.button("Bongkar Keyword Sekarang"):
    if user_prompt:
        with st.spinner("Sedang menghubungi Google AI..."):
            try:
                # Menggunakan format model name lengkap untuk menghindari error 404
                model = genai.GenerativeModel(
                    model_name='models/gemini-1.5-flash',
                    tools=[{ "google_search_retrieval": {} }]
                )

                response = model.generate_content(user_prompt)

                # Cek Metadata Pencarian
                keywords = []
                if hasattr(response.candidates[0], 'grounding_metadata'):
                    metadata = response.candidates[0].grounding_metadata
                    # Mengambil query pencarian jika ada
                    if hasattr(metadata, 'queries') and metadata.queries:
                        keywords = metadata.queries
                
                # Tampilkan Hasil
                st.subheader("🔑 Keyword yang dipakai AI:")
                if keywords:
                    for kw in keywords:
                        st.code(kw, language="text")
                    st.success("✅ Gunakan keyword di atas untuk judul artikel WordPress Anda!")
                else:
                    st.warning("⚠️ AI menjawab menggunakan database internal. Coba prompt yang lebih spesifik seperti 'cari jasa desain arsitek terbaru di sukabumi'.")

                st.divider()
                with st.expander("Lihat Jawaban AI"):
                    st.write(response.text)

            except Exception as e:
                # Menampilkan pesan error yang lebih rapi
                st.error(f"Terjadi kesalahan: {e}")
                st.info("Tips: Pastikan library 'google-generativeai' di requirements.txt sudah versi terbaru.")
    else:
        st.warning("Harap masukkan prompt.")
