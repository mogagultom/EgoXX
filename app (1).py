import streamlit as st
import openai
import requests

# Ganti ini dengan API key kamu
OPENAI_API_KEY = 'your-openai-key'
TTS_API_KEY = 'your-tts-key'
DID_API_KEY = 'your-did-key'
PHOTO_URL = 'https://example.com/photo.jpg'  # Ganti dengan URL foto kamu

openai.api_key = OPENAI_API_KEY

st.title("EgoXX - Video Generator")

user_text = st.text_area("Masukkan teks kamu:")

if st.button("Generate Video"):
    if not user_text:
        st.warning("Teks tidak boleh kosong.")
    else:
        with st.spinner("Memproses dengan ChatGPT..."):
            chat_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Kamu adalah asisten yang cerdas."},
                    {"role": "user", "content": user_text}
                ]
            )
            reply_text = chat_response.choices[0].message.content.strip()
            st.success("Balasan dari GPT berhasil didapat!")

        st.markdown(f"**Balasan ChatGPT:** {reply_text}")

        with st.spinner("Mengubah ke suara (TTS)..."):
            tts_response = requests.post(
                "https://api.tts-provider.com/synthesize",  # ganti dengan endpoint TTS asli
                headers={"Authorization": f"Bearer {TTS_API_KEY}"},
                json={"text": reply_text}
            )
            audio_url = tts_response.json().get('audio_url')
            st.audio(audio_url)

        with st.spinner("Membuat video dengan D-ID..."):
            did_response = requests.post(
                "https://api.d-id.com/talks",
                headers={
                    "Authorization": f"Bearer {DID_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "script": {"type": "audio", "audio_url": audio_url},
                    "source_url": PHOTO_URL
                }
            )
            video_url = did_response.json().get('result_url')
            st.video(video_url)
