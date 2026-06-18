# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running

```bash
python main.py
```

Generates `.wav` audio chunks (`0.wav`, `1.wav`, …) and plays each one immediately via `afplay`.

## Known compatibility fixes

This project required patching to run on macOS with current pip packages:

- **`ESPEAK_DATA_PATH`** must be set before importing `kokoro` — the bundled `espeakng_loader` library has a CI build path baked in. `main.py` handles this with `os.environ.setdefault`.
- **`misaki/espeak.py` line 10** — `EspeakWrapper.set_data_path(...)` was commented out because `phonemizer 3.2+` removed that class method.
- **`pandas>=2.2`** required — pandas 2.1.x is binary-incompatible with numpy 2.x.

## Offline use

`main.py` sets `HF_HUB_OFFLINE=1` so huggingface_hub skips network checks and loads from cache. Works offline once the model and voice have been downloaded at least once (`~/.cache/huggingface/hub/models--hexgrad--Kokoro-82M/`). To fetch a new voice or update the model, run with `HF_HUB_OFFLINE=0 python main.py`.

First run also auto-downloads the spaCy model `en_core_web_sm` if missing.

## Dependencies

Key packages: `kokoro`, `misaki`, `soundfile`, `phonemizer`, `espeakng_loader`, `torch`.
