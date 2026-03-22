---
name: speak
description: Text-to-speech using Kokoro local TTS. Use when the user wants to convert text to audio, read aloud, or generate speech.
---

# speak

Convert text to speech locally with [Kokoro TTS](https://github.com/nazdridoy/kokoro-tts).

## Quick start

```bash
# Text string → audio file
kokoro-tts <(echo "Hello world") hello.wav --voice af_sarah

# Text file → audio
kokoro-tts article.txt out.wav --voice af_heart

# Chinese
kokoro-tts story.txt out.wav --voice zf_xiaoni --lang cmn

# EPUB / PDF → chapter audio files
kokoro-tts book.epub --split-output ./chapters/ --format mp3 --voice bf_emma

# Voice blending (60-40 mix)
kokoro-tts input.txt out.wav --voice "af_sarah:60,am_adam:40"

# Adjust speed
kokoro-tts input.txt out.wav --voice am_adam --speed 1.2

# Stream playback (no file saved)
kokoro-tts input.txt --stream --voice af_nova
```

## Install

```bash
uv tool install kokoro-tts
```

Model files (`kokoro-v1.0.onnx`, `voices-v1.0.bin`) must be in the working directory. Download once:

```bash
wget https://github.com/nazdridoy/kokoro-tts/releases/download/v1.0.0/kokoro-v1.0.onnx
wget https://github.com/nazdridoy/kokoro-tts/releases/download/v1.0.0/voices-v1.0.bin
```

## Voices at a glance

| Region | Female | Male |
|--------|--------|------|
| 🇺🇸 en-us | af_alloy af_heart af_sarah af_nova ... | am_adam am_echo am_michael ... |
| 🇬🇧 en-gb | bf_alice bf_emma bf_lily ... | bm_daniel bm_george ... |
| 🇨🇳 cmn | zf_xiaoni zf_xiaoxiao zf_xiaoyi ... | zm_yunxi zm_yunyang ... |
| 🇯🇵 ja | jf_alpha jf_nezumi ... | jm_kumo |
| 🇫🇷 fr-fr | ff_siwis | — |
| 🇮🇹 it | if_sara | im_nicola |

For full voice list, options, and input format details, see [reference.md](reference.md).
