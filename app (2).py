import streamlit as st
import openai

# Inisialisasi klien OpenAI (pastikan API key disetel via secret atau environment variable)
client = openai.OpenAI()

# Judul aplikasi
st.title("Tanya Asisten AI")

# Input dari pengguna
user_input = st.text_input("Apa yang ingin kamu tanyakan?")

if st.button("Tanya"):
    if not user_input.strip():
        st.warning("Teks tidak boleh kosong.")
    else:
        with st.spinner("Memproses dengan ChatGPT..."):
            try:
                # Kirim ke model GPT-4
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Kamu adalah asisten yang membantu menjawab pertanyaan dengan jelas dan sopan."},
                        {"role": "user", "content": user_input}
                    ]
                )

                # Ambil hasilnya
                result = response.choices[0].message.content
                st.success("Jawaban dari AI:")
                st.write(result)

            except Exception as e:
                st.error(f"Terjadi kesalahan: {str(e)}")
