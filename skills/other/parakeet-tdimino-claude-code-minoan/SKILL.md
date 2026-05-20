---
name: parakeet
description: >
  Local speech-to-text via Handy app (push-to-talk) and NeMo CLI scripts.
  Parakeet V3: 25 languages, auto-detection, ~30x realtime on M4 Max, 6% WER.
  This skill should be used when transcribing audio files or dictating voice input.
argument-hint: [audio-file | "dictate" | "check"]
tools: [Bash, Read, Write]
---

# Parakeet Dictation Skill

Local speech-to-text powered by NVIDIA Parakeet TDT 0.6B V3 (~600MB model, 100% offline).

## Two Modes

### 1. Handy App (Primary — Push-to-Talk into Any Text Field)

[Handy](https://handy.computer/) is a free, open-source Tauri app (Rust + React) providing
push-to-talk dictation with Parakeet V3 built in. Inference via
[transcribe-rs](https://github.com/cjpais/transcribe-rs) (ONNX Runtime, int8 quantized).

```bash
brew install --cask handy
```

- **Default hotkey**: ⌥Space (Option-Space) on macOS, Ctrl-Space on Windows/Linux
- **Modes**: Push-to-talk (hold) or toggle (press to start/stop)
- Select **Parakeet V3** in Settings → Models (auto-downloads ~478MB)
- Grant microphone + accessibility permissions
- Includes VAD (Silero), model management UI
- **Additional models**: Whisper (Small/Medium/Turbo/Large), Moonshine, SenseVoice
- Models stored at `~/Library/Application Support/com.pais.handy/models/`

### 2. CLI Scripts (Claude Code File Transcription & Terminal Dictation)

CLI scripts remain for headless/terminal use within Claude Code. These use NeMo/PyTorch.

## Performance

| System | Speed | Engine |
|--------|-------|--------|
| **Handy (M4 Max)** | ~30x realtime | transcribe-rs / ONNX int8 |
| **Handy (Zen 3)** | ~20x realtime | transcribe-rs / ONNX int8 |
| **Handy (Skylake i5)** | ~5x realtime | transcribe-rs / ONNX int8 |
| **NeMo CLI (MPS)** | Varies | NeMo / PyTorch |

- **Accuracy**: 6.05% WER (Word Error Rate)
- **Languages**: 25 European languages with automatic detection (no prompting)
- **Privacy**: 100% local processing, no cloud API
- **License**: CC BY 4.0 (model), MIT (Handy app)

## Commands

### Transcribe Audio File

```bash
/parakeet path/to/audio.wav
/parakeet ~/recordings/interview.mp3
/parakeet meeting.m4a
```

Supported formats: `.wav`, `.mp3`, `.m4a`, `.flac`, `.ogg`, `.aac`

### Live Dictation (Terminal)

```bash
/parakeet
/parakeet dictate
```

Record from microphone until Enter is pressed, then transcribe.

### Check Installation

```bash
/parakeet check
```

Verify Parakeet is properly installed and model can load.

## Setup

### Handy (Push-to-Talk UI)

```bash
brew install --cask handy
```

Launch from Applications, select Parakeet V3 model, configure hotkey.

### CLI Scripts (Prerequisites)

1. **Parakeet Dictate repo** at `~/Programming/parakeet-dictate/` with Python venv
2. **Install dependencies**:
   ```bash
   cd ~/Programming/parakeet-dictate
   uv venv && uv pip install -r requirements.txt
   ```
3. **(Optional) Set custom path**: `export PARAKEET_HOME=/path/to/parakeet-dictate`

## Implementation

When this skill is invoked:

1. **For audio files**: Run the transcription script
   ```bash
   cd ~/.claude/skills/parakeet/scripts && \
   ${PARAKEET_HOME:-~/Programming/parakeet-dictate}/.venv/bin/python transcribe.py "<filepath>"
   ```

2. **For live dictation**: Run the dictation script
   ```bash
   cd ~/.claude/skills/parakeet/scripts && \
   ${PARAKEET_HOME:-~/Programming/parakeet-dictate}/.venv/bin/python dictate.py
   ```

3. **For checking setup**: Run the check script
   ```bash
   cd ~/.claude/skills/parakeet/scripts && \
   ${PARAKEET_HOME:-~/Programming/parakeet-dictate}/.venv/bin/python check_setup.py
   ```

## Model Caches

| System | Cache Location | Size | Engine |
|--------|---------------|------|--------|
| **Handy** | `~/Library/Application Support/com.pais.handy/models/` | ~478MB | transcribe-rs (ONNX int8) |
| **NeMo CLI** | `~/.cache/nemo/` | ~1.2GB | NeMo / PyTorch |

Model caches are separate. Handy's Parakeet V3 int8 model structure:
```
parakeet-tdt-0.6b-v3-int8/
├── encoder-model.int8.onnx
├── decoder_joint-model.int8.onnx
├── nemo128.onnx (audio preprocessor)
└── vocab.txt
```

## Troubleshooting

### "No module named nemo"
Use the Parakeet virtual environment. Scripts automatically use the correct Python.

### "MPS not available"
Apple Silicon Metal acceleration requires PyTorch 2.0+. Falls back to CPU automatically.

### "Permission denied: microphone"
Grant microphone access in System Preferences → Privacy & Security → Microphone.

### Model download slow
The Parakeet model downloads on first use (~478MB for Handy, ~1.2GB for NeMo). Subsequent runs use cache.

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `PARAKEET_HOME` | `~/Programming/parakeet-dictate` | Parakeet Dictate installation path |

## Dependencies

**Handy**: `brew install --cask handy` (standalone, no other deps)

**CLI scripts** require:
- **Parakeet Dictate repo** at `$PARAKEET_HOME` (default: `~/Programming/parakeet-dictate`)
- **Python virtual environment** at `$PARAKEET_HOME/.venv`
- **NeMo toolkit** with ASR support (`nemo_toolkit[asr]>=2.0.0`)
- **PyTorch 2.0+** (for MPS/CUDA acceleration)
- **soundfile** and **sounddevice** for audio handling
