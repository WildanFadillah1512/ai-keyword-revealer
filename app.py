import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI API KEY ---
API_KEY = "AIzaSyDOSXR9-WF-quua7OS5_Xa1S6sY8fYpOQk"
genai.configure(api_key=API_KEY)

# --- SETTING HALAMAN ---
st.set_page_config(page_title="AI Search Revealer", page_icon="⚡")
st.title("⚡ AI Keyword Insight (Gemini 2.0 Flash)")
st.markdown("""
Menggunakan model **Gemini 2.0 Flash** - Model terbaru yang Cepat & Efisien.
Stabil untuk riset keyword tanpa takut kuota cepat habis.
""")

# --- INPUT ---
user_prompt = st.text_input("Masukkan Prompt:", placeholder="Contoh: Jasa kontraktor terbaik di Sukabumi")

if st.button("Bongkar Keyword"):
    if user_prompt:
        with st.spinner("Sedang melacak keyword via Gemini 2.0 Flash..."):
            try:
                # KITA GUNAKAN GEMINI 2.0 FLASH (Index No. 3 di list Anda)
                # Ini adalah pilihan terbaik: Lebih pintar dari 1.5, tapi kuota lega.
                target_model = "models/gemini-2.0-flash"
                
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
                    st.success(f"✅ SUKSES! Model berhasil menangkap keyword pencarian:")
                    st.divider()
                    st.subheader("🔑 Keyword Google Search:")
                    for kw in keywords:
                        st.code(kw, language="text")
                    st.info("💡 Tips: Copy keyword ini untuk Judul Artikel (H1) di WordPress.")
                else:
                    st.warning("⚠️ AI menjawab tanpa searching. Coba prompt yang lebih 'memancing', misal: 'Cari daftar harga jasa desain...'")

                # Tampilkan Jawaban Lengkap
                with st.expander("Lihat Jawaban Lengkap AI"):
                    st.write(response.text)

            except Exception as e:
                st.error(f"Error: {e}")
                st.write("Jika muncul error 429 lagi, tunggu 1-2 menit lalu coba lagi (limit per menit).")

    else:
        st.warning("Masukkan prompt dulu.")
