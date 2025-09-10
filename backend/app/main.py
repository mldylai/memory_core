from chat_engine import load_chat_engine
from text_to_speech import synthesize
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import base64
import os

app = FastAPI()

chat_engine = load_chat_engine()

def generate_response(user_input: str) -> str:
    # print(f"User input: {user_input}")
    response = chat_engine.chat(user_input).response
    print(f"Response: {response}")
    return synthesize(response)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace with your frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws/audio")
async def websocket_audio(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            # Receive text from frontend
            user_text = await ws.receive_text()
            print("Received:", user_text)

            # Generate audio using your TTS function
            audio_filepath = generate_response(user_text)

            # Read audio bytes and encode as base64
            with open(audio_filepath, "rb") as f:
                audio_bytes = f.read()
            audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")

            # Send audio back to frontend
            await ws.send_text(audio_b64)
            print("Audio sent back to client")

            # Delete the file to save disk space
            os.remove(audio_filepath)
    except WebSocketDisconnect:
        print("Client disconnected")