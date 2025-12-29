import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI API KEY ---
API_KEY = "AIzaSyDOSXR9-WF-quua7OS5_Xa1S6sY8fYpOQk"
genai.configure(api_key=API_KEY)

# --- SETTING HALAMAN ---
st.set_page_config(page_title="AI Search Lite", page_icon="🍃")
st.title("🍃 AI Keyword Insight (Versi Hemat)")
st.markdown("Menggunakan **Gemini 2.0 Flash Lite**. Versi paling ringan, cepat, dan anti-limit.")

# --- INPUT ---
user_prompt = st.text_input("Masukkan Prompt:", placeholder="Contoh: Jasa kontraktor terbaik di Sukabumi")

if st.button("Bongkar Keyword"):
    if user_prompt:
        with st.spinner("Sedang mencari data dengan mode hemat..."):
            try:
                # KITA GUNAKAN VERSI LITE (Sesuai List No. 8 di Screenshot Anda)
                target_model = "models/gemini-2.0-flash-lite-preview-02-05"
                
                model = genai.GenerativeModel(
                    model_name=target_model,
                    tools=[{ "google_search_retrieval": {} }]
                )

                response = model.generate_content(user_prompt)

                # --- EKSTRAKSI KEYWORD ---
                keywords = []
                if hasattr(response.candidates[0], 'grounding_metadata'):
                    metadata = response.candidates[0].grounding_metadata
                    if hasattr(metadata, 'queries'):
                        keywords = metadata.queries
                
                # --- TAMPILAN HASIL ---
                if keywords:
                    st.success("✅ BERHASIL! Keyword ditemukan:")
                    for kw in keywords:
                        st.code(kw, language="text")
                    st.caption("Copy keyword di atas untuk SEO WordPress Anda.")
                else:
                    st.warning("⚠️ AI menjawab tanpa searching. Coba prompt: 'Carikan berita terbaru tentang...'")

                with st.expander("Lihat Jawaban AI"):
                    st.write(response.text)

            except Exception as e:
                st.error(f"Error: {e}")
                st.markdown("---")
                st.error("JIKA MASIH ERROR 429: Berarti kuota Akun Google Anda benar-benar habis total hari ini. Solusi: Buat API Key baru di Akun Google (Gmail) yang berbeda.")

    else:
        st.warning("Prompt masih kosong.")
