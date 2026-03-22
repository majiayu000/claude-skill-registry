---
name: testing-whisper
description: Transcribe WAV audio files using OpenAI Whisper for intelligibility testing. Use when transcribing audio, testing speech output quality, running whisper, or checking if generated audio is intelligible.
---

# Whisper Audio Intelligibility Test

Transcribe WAV audio files using OpenAI Whisper and report whether the speech
is intelligible. Optionally compare against expected text.

## Setup

Whisper is installed as a uv tool: `uv tool install openai-whisper`.

Since this machine may lack `ffmpeg`, always use the Python API approach that
loads WAV files with scipy (bypasses the ffmpeg requirement).

## Running Transcription

Use `uv run --no-project --with openai-whisper --with scipy --python 3.11` to
execute the transcription script:

```bash
uv run --no-project --with openai-whisper --with scipy --python 3.11 \
  python3 ~/.claude/skills/testing-whisper/transcribe.py \
  [--model tiny|base|small|medium|large-v3] \
  [--language en] \
  [--expected "expected text"] \
  [--json] \
  file1.wav [file2.wav ...]
```

### Arguments

- `--model`: Whisper model size (default: `large-v3`). See model selection guide below.
- `--language`: Language hint (default: `en`).
- `--expected`: Expected transcription text. When provided, calculates Word Error Rate (WER).
- `--json`: Output results as JSON instead of human-readable text.
- Positional: One or more WAV file paths.

### Model Selection

Use `large-v3` for TTS quality verification. Smaller models hallucinate or miss
words in synthesized speech, making them unreliable for judging output quality.

| Model      | VRAM   | When to use                                                     |
| ---------- | ------ | --------------------------------------------------------------- |
| `large-v3` | ~10 GB | **Default.** TTS evaluation, quality gating, regression testing |
| `medium`   | ~5 GB  | GPU memory constrained, still decent accuracy                   |
| `small`    | ~2 GB  | Quick smoke tests only                                          |
| `base`     | ~1 GB  | Not recommended for TTS — high hallucination rate               |
| `tiny`     | ~1 GB  | Not recommended for TTS — unreliable                            |

Observed with identical Qwen3-TTS 1.7B voice-cloned output:

- `large-v3`: "That's one tank. Flash attention pipeline." (key phrase captured)
- `base`: "That's one thing, flash attention pipeline." (close but hallucinated)

For poor-quality 0.6B output, `base` hallucinated "Charging Wheel" while
`large-v3` gave "Flat, splashes." — honest about the poor quality instead of
confabulating plausible words.

### Output Format

For each file, prints:

```text
filename.wav:
  transcription: "Hello world, this is a test."
  duration: 2.96s
  rms: 0.0866
  peak: 0.6832
  silence: 49.2%
  [wer: 0.0%]  (if --expected provided)
```

## Interpreting Results

| Transcription         | Meaning                                                                         |
| --------------------- | ------------------------------------------------------------------------------- |
| Matches expected text | Audio is intelligible and correct                                               |
| Partial match         | Audio has some speech but quality issues                                        |
| Empty string `""`     | Audio is unintelligible (noise, silence, or garbage)                            |
| Hallucinated text     | Model heard something in noise (common with Whisper, especially smaller models) |

### Audio Quality Indicators

- **RMS < 0.01**: Essentially silent
- **silence > 80%**: Mostly silence, likely no speech
- **peak < 0.05**: Very quiet, may not contain useful audio

### TTS-Specific Patterns

Voice-cloned TTS output often has these characteristics:

- **Garbled opening, clear ending**: Common with ICL voice cloning on short references. The model needs a few frames to "lock in" to the target voice.
- **Key phrases preserved**: Even when WER is high, domain-specific terms (e.g. "flash attention pipeline") often come through clearly.
- **Smaller models produce worse audio**: 0.6B models produce significantly less intelligible output than 1.7B — expect Whisper to reflect this.

## Batch Testing (TTS Variant Comparison)

When testing multiple TTS outputs against expected text:

```bash
uv run --no-project --with openai-whisper --with scipy --python 3.11 \
  python3 ~/.claude/skills/testing-whisper/transcribe.py \
  --expected "Hello world, this is a test." \
  variant1.wav variant2.wav variant3.wav
```

This produces a comparison table showing which variants produce intelligible speech.

## Docker / NGC Container Usage

When testing on a GPU box inside an NGC container (e.g. for CUDA flash-attn builds),
ffmpeg isn't available and apt can be slow. Two workarounds:

1. **Static ffmpeg binary** (fast, no apt):

   ```bash
   curl -sL https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-arm64-static.tar.xz \
     | tar xJ --strip-components=1 -C /usr/local/bin/ --wildcards "*/ffmpeg" "*/ffprobe"
   pip install openai-whisper
   ```

2. **Use scipy loader** (this script's default — no ffmpeg needed):

   ```bash
   pip install openai-whisper scipy
   python3 ~/.claude/skills/testing-whisper/transcribe.py --model large-v3 output.wav
   ```

The script loads WAV files directly via scipy, bypassing Whisper's ffmpeg
dependency entirely. This works for WAV files (the standard TTS output format).
