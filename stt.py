import os
import sys
import tty
import termios
import threading
from datetime import datetime
import numpy as np
import whisper
import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 16000
CHUNK_SIZE = int(SAMPLE_RATE * 0.1)  # 100ms chunks

os.makedirs("input", exist_ok=True)
model = whisper.load_model("base")

print("Recording… press Space to stop")
chunks = []
stop_flag = threading.Event()

fd = sys.stdin.fileno()
old_settings = termios.tcgetattr(fd)

def wait_for_space():
    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch == " ":
                stop_flag.set()
                break
    except Exception:
        stop_flag.set()

threading.Thread(target=wait_for_space, daemon=True).start()

try:
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1) as stream:
        while not stop_flag.is_set():
            data, _ = stream.read(CHUNK_SIZE)
            chunks.append(data)
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

audio = np.concatenate(chunks)
path = f"input/{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
sf.write(path, audio, SAMPLE_RATE)
result = model.transcribe(path)

text = result["text"].strip()
print(text)
with open("conversation.log", "a") as f:
    f.write(f"[IN][{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text}\n")
