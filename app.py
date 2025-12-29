import streamlit as st
import google.generativeai as genai

# --- CONFIG ---
# API Key Anda (Hardcoded sesuai permintaan)
API_KEY = "AIzaSyDOSXR9-WF-quua7OS5_Xa1S6sY8fYpOQk"
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="AI Keyword Insight", page_icon="🕵️‍♂️")

st.title("🕵️‍♂️ AI Search Keyword Revealer")
st.write("Versi Diagnosa Otomatis")

# --- FUNGSI PENCARIAN ---
def run_search(model_name_to_use, prompt):
    # Setup Model dengan Tools Google Search
    model = genai.GenerativeModel(
        model_name=model_name_to_use,
        tools=[{ "google_search_retrieval": {} }]
    )
    return model.generate_content(prompt)

# --- USER INPUT ---
user_prompt = st.text_input("Masukkan Prompt:", placeholder="Contoh: rekomendasi jasa desain arsitek")

if st.button("Bongkar Keyword"):
    if user_prompt:
        result_box = st.empty()
        
        # LIST NAMA MODEL YANG AKAN DICOBA (Urutan Prioritas)
        # Kita coba beberapa variasi nama model karena kadang beda akun beda nama
        model_candidates = [
            "gemini-1.5-flash",
            "models/gemini-1.5-flash",
            "gemini-1.5-flash-latest",
            "gemini-1.5-flash-001"
        ]

        success = False
        
        with st.spinner("Mencoba menghubungkan ke berbagai model AI..."):
            for model_name in model_candidates:
                try:
                    # Coba generate
                    response = run_search(model_name, user_prompt)
                    
                    # Jika berhasil sampai sini, berarti model ketemu!
                    success = True
                    st.success(f"Berhasil terhubung menggunakan model: **{model_name}**")
                    
                    # --- EKSTRAKSI KEYWORD ---
                    keywords = []
                    if hasattr(response.candidates[0], 'grounding_metadata'):
                        metadata = response.candidates[0].grounding_metadata
                        if hasattr(metadata, 'queries'):
                            keywords = metadata.queries

                    st.divider()
                    st.subheader("🔑 Keyword Pencarian AI:")
                    if keywords:
                        for kw in keywords:
                            st.code(kw, language="text")
                        st.info("Copy keyword di atas untuk judul artikel WordPress Anda.")
                    else:
                        st.warning("AI menjawab tanpa searching Google (menggunakan database internal).")

                    with st.expander("Lihat Jawaban Lengkap"):
                        st.write(response.text)
                    
                    # Stop looping jika sudah berhasil
                    break 
                
                except Exception as e:
                    # Jika gagal, lanjut ke model berikutnya di list
                    continue

        # --- JIKA SEMUA MODEL GAGAL (DIAGNOSA PENYEBAB) ---
        if not success:
            st.error("❌ Semua percobaan model GAGAL. Masalah ada pada Akun/Project Google Cloud Anda.")
            
            st.markdown("### 🛠️ Mode Diagnosa Otomatis")
            st.write("Sistem sekarang akan mengecek model apa yang SEBENARNYA tersedia untuk API Key Anda:")
            
            try:
                available_models = []
                for m in genai.list_models():
                    if 'generateContent' in m.supported_generation_methods:
                        available_models.append(m.name)
                
                if available_models:
                    st.warning("Daftar Model yang tersedia untuk akun Anda:")
                    st.json(available_models)
                    st.write("Silakan screenshot bagian ini dan kirim ke asisten AI Anda.")
                else:
                    st.error("Tidak ada model yang ditemukan. Kemungkinan API Key belum aktif atau Billing belum disetting.")
            except Exception as e:
                st.error(f"Gagal melakukan listing model: {e}")

    else:
        st.warning("Masukkan prompt dulu.")
