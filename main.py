import os
import subprocess
from datetime import datetime

import espeakng_loader

os.environ.setdefault("ESPEAK_DATA_PATH", str(espeakng_loader.get_data_path()))

import soundfile as sf
from kokoro import KPipeline

os.makedirs("output", exist_ok=True)

pipeline = KPipeline(lang_code="a")
text = """
[Kokoro](/kˈOkəɹO/) is an open-weight TTS model with 82 million parameters. Despite its lightweight architecture, it delivers comparable quality to larger models while being significantly faster and more cost-efficient. With Apache-licensed weights, [Kokoro](/kˈOkəɹO/) can be deployed anywhere from production environments to personal projects.
"""
with open("conversation.log", "a") as f:
    f.write(f"[OUT][{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {text.strip()}\n")
generator = pipeline(text, voice="af_heart")
for i, (gs, ps, audio) in enumerate(generator):
    print(i, gs, ps)
    path = f"output/{i}.wav"
    sf.write(path, audio, 24000)
    print(f"  → saved {path}")
    subprocess.run(["afplay", path])
