---
name: setup-voice-mode
description: "Installs and configures VoiceMode MCP for voice interactions with Claude Code. Triggers on keywords: setup voice, voice mode, install voicemode, configure voice"
project-agnostic: true
allowed-tools:
  - Bash
  - Read
---

# Setup VoiceMode for Claude Code

Install and configure VoiceMode MCP for voice interactions with Claude Code.

## Steps

1. Install VoiceMode:
```bash
uvx voice-mode-install --yes
```

2. Add MCP server to Claude Code:
```bash
claude mcp add --scope user voicemode -- uvx --refresh voice-mode
```

3. Configure local endpoints (Kokoro TTS + Whisper STT):
```bash
voicemode config set VOICEMODE_TTS_BASE_URLS http://127.0.0.1:8880/v1
voicemode config set VOICEMODE_STT_BASE_URLS http://127.0.0.1:2022/v1
voicemode config set VOICEMODE_PREFER_LOCAL true
voicemode config set VOICEMODE_ALWAYS_TRY_LOCAL true
```

**This is critical.** Without explicit `_BASE_URLS`, the default includes `https://api.openai.com/v1` as fallback, which crashes with `OPENAI_API_KEY` errors even when local services are running.

4. Verify installation:
```bash
claude mcp list
```

5. Test voice mode:
- Restart Claude Code
- Use the `mcp__voicemode__converse` tool

## First Run Note

**Kokoro TTS may take 5+ minutes to load on first run** while it downloads and initializes the model (~111MB). Check status with:
```bash
voicemode service kokoro status
```

**Two MCP restarts required:**
1. After initial setup (step 5)
2. After Kokoro model finishes downloading

Without the second restart, you may get "OpenAI API key" errors even with local config.

## Configuration Options

Edit config with:
```bash
voicemode config edit
```

List all options:
```bash
voicemode config list
```

### Key Settings

| Setting | Description |
|---------|-------------|
| `VOICEMODE_PREFER_LOCAL` | Prefer local providers over cloud (true/false) |
| `VOICEMODE_ALWAYS_TRY_LOCAL` | Always attempt local providers first (true/false) |
| `VOICEMODE_SAVE_AUDIO` | Save audio files (true/false, default: false) |
| `VOICEMODE_WHISPER_MODEL` | Whisper model (tiny, base, small, medium, large-v2) |
| `VOICEMODE_KOKORO_DEFAULT_VOICE` | Default voice (e.g., af_sky) |
| `OPENAI_API_KEY` | Required only for cloud processing |

### Provider Options

- **Local-only** (default, recommended): Set `VOICEMODE_TTS_BASE_URLS=http://127.0.0.1:8880/v1` and `VOICEMODE_STT_BASE_URLS=http://127.0.0.1:2022/v1` (no API key needed)
- **Cloud-only**: Set `OPENAI_API_KEY` and set URLs to `https://api.openai.com/v1`
- **Hybrid** (local-first, cloud fallback): Set `OPENAI_API_KEY` and set URLs to `http://127.0.0.1:8880/v1,https://api.openai.com/v1` (TTS) and `http://127.0.0.1:2022/v1,https://api.openai.com/v1` (STT)

## Troubleshooting

- **OpenAI API key error**: Ensure `VOICEMODE_TTS_BASE_URLS` and `VOICEMODE_STT_BASE_URLS` point to local endpoints only (step 3). The `PREFER_LOCAL` flag alone is NOT sufficient — it does not remove OpenAI from the fallback chain
- **Kokoro stuck "starting up"**: Wait 5+ mins on first run, or check logs: `voicemode service kokoro logs`
- **macOS M3 crash**: Known issue with ggml_metal - use CPU mode
- **WSL audio issues**: Install PulseAudio packages
- **Slow transcription**: Use GPU acceleration or smaller Whisper model

## Improved Accuracy (Optional)

The default `tiny` model is fast but less accurate. For better transcription:

| Model | Size | Accuracy | Speed |
|-------|------|----------|-------|
| tiny | 75MB | ~70% | Fastest |
| small | 466MB | ~82% | Fast |
| medium | 1.4GB | ~88% | Moderate |

```bash
voicemode config set VOICEMODE_WHISPER_MODEL small
# or for best accuracy:
voicemode config set VOICEMODE_WHISPER_MODEL medium
```

Restart Whisper service after changing:
```bash
voicemode service whisper restart
```

## macOS Metal GPU Acceleration (Optional)

For significantly faster transcription on Apple Silicon, convert Whisper to Core ML:

### Prerequisites
```bash
# Install whisper.cpp via Homebrew
brew install whisper-cpp

# Set Whisper directory
WHISPER_DIR=~/.voicemode/services/whisper
```

### Steps

**1. Download model**
```bash
cd $WHISPER_DIR/models
./download-ggml-model.sh medium
```

**2. Install Python dependencies**
```bash
pip3 install torch coremltools openai-whisper ane_transformers
```

**3. Convert to Core ML**
```bash
cd $WHISPER_DIR
./models/generate-coreml-model.sh medium
```

**4. Update config**
```bash
voicemode config set VOICEMODE_WHISPER_MODEL medium
```

**5. Restart Whisper**
```bash
voicemode service whisper restart
```

### Verification
```bash
# Check Core ML model exists
ls -la $WHISPER_DIR/models/ggml-medium-encoder.mlmodelc
```

When running, logs should show: `GPU: Metal, Core ML: Enabled`

## Links
- GitHub: https://github.com/mbailey/voicemode
- Docs: https://voice-mode.readthedocs.io
- LiveKit Cloud: https://cloud.livekit.io
