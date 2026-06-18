import tempfile
import numpy as np
import whisper
import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 16000

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
with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
    sf.write(f.name, audio, SAMPLE_RATE)
    result = model.transcribe(f.name)

print(result["text"])
