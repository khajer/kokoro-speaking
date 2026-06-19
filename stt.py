import os
from datetime import datetime
import numpy as np
import whisper
import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 16000

os.makedirs("input", exist_ok=True)
model = whisper.load_model("base")

print("Recording… Ctrl+C to stop and transcribe")
chunks = []
try:
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1) as stream:
        while True:
            data, _ = stream.read(SAMPLE_RATE)
            chunks.append(data)
except KeyboardInterrupt:
    pass

audio = np.concatenate(chunks)
path = f"input/{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
sf.write(path, audio, SAMPLE_RATE)
result = model.transcribe(path)

print(result["text"])
