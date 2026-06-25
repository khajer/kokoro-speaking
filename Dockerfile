FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    espeak-ng \
    libsndfile1 \
    portaudio19-dev \
    ffmpeg \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    openai-whisper sounddevice numpy

# Bake in small models; Kokoro (~300MB) should be mounted as a volume
RUN python -m spacy download en_core_web_sm && \
    python -c "import whisper; whisper.load_model('base')"

COPY . .

ENV HF_HUB_OFFLINE=1
ENV PYTHONUNBUFFERED=1

# afplay is macOS-only; wavs are written to output/ — mount it to retrieve them
# For STT mic access, run with: --device /dev/snd
CMD ["python", "main.py"]
