from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
import edge_tts
import io

app = FastAPI()

VOICES = {
    "ru": "ru-RU-DmitryNeural",
    "en": "en-US-JennyNeural",
    "ru_history": "ru-RU-SvetlanaNeural",
    "en_history": "en-US-AriaNeural",
    "ru_paranormal": "ru-RU-DmitryNeural",
    "en_paranormal": "en-US-GuyNeural",
}

@app.get("/tts")
async def tts(
    text: str = Query(...),
    lang: str = Query("ru"),
    category: str = Query("default")
):
    voice_key = f"{lang}_{category}" if f"{lang}_{category}" in VOICES else lang
    voice = VOICES.get(voice_key, VOICES.get(lang, "ru-RU-DmitryNeural"))
    communicate = edge_tts.Communicate(text, voice)
    audio_buffer = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio_buffer.write(chunk["data"])
    audio_buffer.seek(0)
    return StreamingResponse(
        audio_buffer,
        media_type="audio/mpeg",
        headers={"Content-Disposition": "attachment; filename=speech.mp3"}
    )

@app.get("/health")
def health():
    return {"status": "ok"}
