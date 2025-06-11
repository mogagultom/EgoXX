   
import streamlit as st
import openai
import requests
from openai import OpenAI

st.title("🧠 ChatGPT + TTS + D-ID Talking Head")

# Ambil API key dari secret
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
D_ID_API_KEY = st.secrets["D_ID_API_KEY"]

# Input dari user
prompt = st.text_input("Masukkan pertanyaan atau perintah:")

if prompt:
    # Kirim ke GPT
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    jawaban = response.choices[0].message.content
    st.write("💬 Jawaban:", jawaban)

    # Text to Speech (TTS) pakai ElevenLabs (bisa diganti)
    voice_id = "EXAVITQu4vr4xnSDxMaL"
    tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": st.secrets["ELEVENLABS_API_KEY"],
        "Content-Type": "application/json"
    }

    data = {
        "text": jawaban,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75}
    }

    audio_response = requests.post(tts_url, headers=headers, json=data)

    if audio_response.status_code == 200:
        with open("jawaban.mp3", "wb") as f:
            f.write(audio_response.content)
        audio_file = open("jawaban.mp3", "rb")
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format="audio/mp3")
    else:
        st.error("Gagal mengubah teks jadi suara 😢")

    # Kirim ke D-ID (Talking Head Video)
    image_url = "https://i.imgur.com/2RXPc2d.png"  # Gambar default, bisa diganti
    headers = {
        "Authorization": f"Bearer {D_ID_API_KEY}",
        "Content-Type": "application/json"
    }

    did_data = {
        "script": {
            "type": "text",
            "provider": {"type": "elevenlabs", "voice_id": voice_id},
            "ssml": False,
            "input": jawaban
        },
        "source_url": image_url
    }

    res = requests.post("https://api.d-id.com/talks", headers=headers, json=did_data)

    if res.status_code == 200:
        video_url = res.json()["result_url"]
        st.video(video_url)
    else:
        st.error("Gagal membuat video talking head 😢")
