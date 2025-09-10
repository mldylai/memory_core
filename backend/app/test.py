from fastapi.testclient import TestClient
from main import app
import base64

client = TestClient(app)

with client.websocket_connect("/ws/audio") as ws:
    ws.send_text("你是誰？")
    audio_b64 = ws.receive_text()
    with open("test.wav", "wb") as f:
        f.write(base64.b64decode(audio_b64))
