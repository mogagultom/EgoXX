from flask import Flask, request, jsonify
import openai
import requests

app = Flask(__name__)

# Ganti dengan API key kamu
OPENAI_API_KEY = 'your-openai-key'
TTS_API_KEY = 'your-tts-key'
DID_API_KEY = 'your-did-key'

@app.route('/generate-video', methods=['POST'])
def generate_video():
    data = request.json
    user_text = data.get('text', '')

    if not user_text:
        return jsonify({'error': 'Text tidak boleh kosong'}), 400

    # 1. Proses dengan ChatGPT
    openai.api_key = OPENAI_API_KEY
    chat_response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Kamu adalah asisten yang cerdas."},
            {"role": "user", "content": user_text}
        ]
    )
    reply_text = chat_response.choices[0].message.content.strip()

    # 2. Kirim ke TTS (ganti endpoint & header sesuai provider TTS kamu)
    tts_response = requests.post(
        'https://api.tts-provider.com/synthesize',
        headers={'Authorization': f'Bearer {TTS_API_KEY}'},
        json={'text': reply_text}
    )
    audio_url = tts_response.json().get('audio_url')

    # 3. Kirim ke D-ID
    did_response = requests.post(
        'https://api.d-id.com/talks',
        headers={
            'Authorization': f'Bearer {DID_API_KEY}',
            'Content-Type': 'application/json'
        },
        json={
            'script': {'type': 'audio', 'audio_url': audio_url},
            'source_url': 'https://example.com/photo.jpg'  # Ganti dengan URL fotomu
        }
    )

    return jsonify({
        'reply': reply_text,
        'audio_url': audio_url,
        'video_url': did_response.json().get('result_url')
    })

if __name__ == '__main__':
    app.run(debug=True)
