import os
from datetime import datetime
import numpy as np
import whisper
import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 16000

os.makedirs("input", exist_ok=True)
model = whisper.load_model("base")

SILENCE_THRESHOLD = 0.01  # ponytail: tune this if mic is too/not sensitive
SILENCE_SECONDS = 2
CHUNK_SIZE = int(SAMPLE_RATE * 0.1)  # 100ms chunks

print("Recording… stops after 2s silence or Ctrl+C")
chunks = []
silent_chunks = 0
max_silent = int(SILENCE_SECONDS / 0.1)

try:
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1) as stream:
        while True:
            data, _ = stream.read(CHUNK_SIZE)
            chunks.append(data)
            rms = np.sqrt(np.mean(data ** 2))
            if rms < SILENCE_THRESHOLD:
                silent_chunks += 1
                if silent_chunks >= max_silent:
                    break
            else:
                silent_chunks = 0
except KeyboardInterrupt:
    pass

audio = np.concatenate(chunks)
path = f"input/{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
sf.write(path, audio, SAMPLE_RATE)
result = model.transcribe(path)

text = result["text"].strip()
print(text)
with open("conversation.log", "a") as f:
    f.write(f"[IN][{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}\n")
