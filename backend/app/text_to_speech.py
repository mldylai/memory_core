import uuid
import os
import utils 
import torch
import torchaudio
from boson_multimodal.serve.serve_engine import HiggsAudioServeEngine, HiggsAudioResponse
from boson_multimodal.data_types import ChatMLSample, Message, AudioContent

# Generate audio from text and save to a file.

MODEL_PATH = "bosonai/higgs-audio-v2-generation-3B-base"
AUDIO_TOKENIZER_PATH = "bosonai/higgs-audio-v2-tokenizer"
REF_AUDIO = "ref_audio/mel.wav"

system_prompt = ("Generate audio following instruction.\n\n<|scene_desc_start|>\nAudio is recorded from a spacious room with echoes.\n<|scene_desc_end|>")

device = "cuda" if torch.cuda.is_available() else "cpu"

reference_audio = utils.encode_base64_content_from_file(REF_AUDIO)

serve_engine = HiggsAudioServeEngine(MODEL_PATH, AUDIO_TOKENIZER_PATH, device=device)


def synthesize(text: str):
    # Generate unique filename to avoid conflicts
    audio_filepath = f"{uuid.uuid4()}.wav"

    # Run the TTS model
    text = utils.clean_punctuation(text)
    text = utils.convert_traditional_to_simplified(text)
    messages = [
        Message(role="system", content=system_prompt),
        Message(role="assistant", content=AudioContent(raw_audio=reference_audio, audio_url="placeholder")),
        Message(role="user", content=text),
    ]

    output: HiggsAudioResponse = serve_engine.generate(
        chat_ml_sample=ChatMLSample(messages=messages),
        max_new_tokens=1024,
        temperature=0.3,
        top_p=0.95,
        top_k=50,
        stop_strings=["<|end_of_text|>", "<|eot_id|>"],
        seed=2025,
    )
    torchaudio.save(audio_filepath, torch.from_numpy(output.audio)[None, :], output.sampling_rate)
    utils.add_reverb(audio_filepath)
    print(f"Saved: {audio_filepath}")
    return audio_filepath
