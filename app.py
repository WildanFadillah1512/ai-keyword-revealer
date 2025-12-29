import streamlit as st
import google.generativeai as genai

# --- KONFIGURASI API KEY ---
API_KEY = "AIzaSyDOSXR9-WF-quua7OS5_Xa1S6sY8fYpOQk"
genai.configure(api_key=API_KEY)

# --- SETTING HALAMAN ---
st.set_page_config(page_title="AI Search Revealer", page_icon="💎")
st.title("💎 AI Keyword Insight (Gemini 2.5 Pro)")
st.markdown("""
Menggunakan model **Gemini 2.5 Pro** - Model tercanggih di akun Anda.
Alat ini akan memaksa AI mencari data di Google dan membocorkan keyword-nya.
""")

# --- INPUT ---
user_prompt = st.text_input("Masukkan Prompt:", placeholder="Contoh: Jasa kontraktor terbaik di Sukabumi")

if st.button("Bongkar Keyword"):
    if user_prompt:
        with st.spinner("Sedang memerintahkan Gemini 2.5 Pro untuk riset..."):
            try:
                # KITA GUNAKAN MODEL TERCANGGIH DARI LIST (NOMOR 1)
                target_model = "models/gemini-2.5-pro"
                
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
                    st.success(f"✅ SUKSES! {target_model} menggunakan keyword ini:")
                    st.divider()
                    st.subheader("🔑 Keyword Google Search:")
                    for kw in keywords:
                        st.code(kw, language="text")
                    st.info("💡 Copy keyword di atas untuk judul artikel WordPress Anda.")
                else:
                    st.warning("⚠️ AI menjawab tanpa searching. Coba tambahkan kata 'Terbaru' atau 'Data 2025' agar AI terpaksa searching.")

                # Tampilkan Jawaban Lengkap
                with st.expander("Lihat Jawaban Lengkap AI"):
                    st.write(response.text)

            except Exception as e:
                st.error(f"Error pada model {target_model}: {e}")
                st.markdown("---")
                st.info("Jika error berlanjut, kemungkinan model 2.5 Pro belum support 'Search Tool'. Ganti kode 'target_model' menjadi 'models/gemini-2.0-flash'.")

    else:
        st.warning("Masukkan prompt dulu.")
