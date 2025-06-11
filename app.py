import streamlit as st
import openai
import requests

st.title("🧠 ChatGPT + TTS + D-ID Talking Head")

openai.api_key = st.secrets["OPENAI_API_KEY"]
D_ID_API_KEY = st.secrets["D_ID_API_KEY"]

prompt = st.text_input("Masukkan pertanyaan atau perintah:")

if prompt:
    # ChatGPT
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    reply = response.choices[0].message.content
    st.write("💬 ChatGPT:", reply)

    # TTS (Text to Speech)
    tts_response = openai.Audio.create(
        model="tts-1",
        voice="alloy",
        input=reply
    )
    audio_data = tts_response.read()

    # Upload suara ke D-ID
    headers = {
        "Authorization": f"Bearer {D_ID_API_KEY}"
    }
    files = {
        'script': (None, '{"type":"audio","provider":"microsoft","ssml":false}'),
        'audio': ('audio.mp3', audio_data)
    }
    did_res = requests.post("https://api.d-id.com/talks", headers=headers, files=files)

    if did_res.status_code == 200:
        result = did_res.json()
        video_url = result.get("result_url")
        st.video(video_url)
    else:
        st.error("Gagal membuat video dari D-ID")
