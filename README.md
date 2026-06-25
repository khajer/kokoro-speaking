# kokoro-speaking

Offline text-to-speech (TTS) and speech-to-text (STT) on macOS using [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) and [Whisper](https://github.com/openai/whisper).

## Requirements

- macOS (uses `afplay` for audio playback)
- Python 3.10+
- Microphone access granted to your terminal (System Settings → Privacy & Security → Microphone)

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Usage

**TTS** — generate and play speech from text:

```bash
python main.py
```

Outputs `.wav` chunks to `output/` and plays each one immediately.

**STT** — record from mic and transcribe:

```bash
python stt.py
```

Recording stops automatically after 2 seconds of silence, or on Ctrl+C. Saves the audio to `input/` and prints the transcript.

## First run

On first run, Kokoro and Whisper models are downloaded from Hugging Face (~300 MB). Subsequent runs work fully offline (`HF_HUB_OFFLINE=1` is set automatically).

To fetch a new voice or update the model:

```bash
HF_HUB_OFFLINE=0 python main.py
```

## Known fixes (macOS)

- `ESPEAK_DATA_PATH` is set at startup — the bundled `espeakng_loader` has a CI path baked in.
- `misaki/espeak.py` line 10: `set_data_path` commented out — removed in `phonemizer 3.2+`.
- `pandas>=2.2` required — 2.1.x is binary-incompatible with numpy 2.x.
