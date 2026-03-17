---
name: wavecap-config
description: View and edit WaveCap configuration. Use when the user asks about Whisper settings, LLM correction config, stream settings, or wants to modify the config.yaml file.
---

# WaveCap Configuration Skill

Use this skill to view and modify WaveCap configuration settings.

## Configuration File Location

The main configuration file is at:
```
/Users/thw/Projects/WaveCap/state/config.yaml
```

## View Current Configuration

### Full Config
```bash
cat /Users/thw/Projects/WaveCap/state/config.yaml
```

### Whisper Settings
```bash
cat /Users/thw/Projects/WaveCap/state/config.yaml | grep -A 30 "^whisper:"
```

### LLM Correction Settings
```bash
cat /Users/thw/Projects/WaveCap/state/config.yaml | grep -A 15 "^llm:"
```

### Stream Definitions
```bash
cat /Users/thw/Projects/WaveCap/state/config.yaml | grep -A 100 "^streams:"
```

## Key Configuration Sections

### Server Settings
```yaml
server:
  host: 0.0.0.0
  port: 8000
  corsOrigin: "*"
```

### Whisper Transcription Settings
```yaml
whisper:
  model: large-v3-turbo          # Model: base.en, small, medium, large-v3-turbo
  language: en                    # Language code
  chunkLength: 20                 # Seconds per chunk (15-120)
  minChunkDurationSeconds: 12     # Minimum chunk before flush
  contextSeconds: 0.5             # Overlap for context
  silenceThreshold: 0.02          # Audio energy threshold
  silenceHoldSeconds: 1.2         # Wait after silence
  maxConcurrentProcesses: 2       # Parallel transcriptions
  beamSize: 8                     # Decoder beam width
  decodeTemperature: 0.0          # 0.0 = deterministic
```

### LLM Correction Settings
```yaml
llm:
  enabled: true                   # Enable/disable LLM correction
  model: llama-3.2-3b             # Model name (see available models)
  temperature: 0.1                # Generation temperature
  maxTokens: 256                  # Max output tokens
  minTextLength: 10               # Skip short texts
  domainTerms:                    # Custom terminology
    - SITREP
    - SAPOL
```

### Available LLM Models
- `llama-3.2-1b` - Fast, small (Llama-3.2-1B-Instruct-4bit)
- `llama-3.2-3b` - Balanced (Llama-3.2-3B-Instruct-4bit)
- `qwen-2.5-1.5b` - Fast alternative (Qwen2.5-1.5B-Instruct-4bit)
- `qwen-2.5-3b` - Balanced alternative (Qwen2.5-3B-Instruct-4bit)
- `llama-3.2-8b` - Higher quality (Llama-3.2-8B-Instruct-4bit)
- `qwen-2.5-7b` - Higher quality alternative
- `deepseek-r1-8b` - DeepSeek R1 distilled

### UI Settings
```yaml
ui:
  themeMode: system               # system, light, dark
  colorCodingEnabled: false       # Color by confidence
  transcriptCorrectionEnabled: false
```

### Stream Configuration
```yaml
streams:
  - id: unique-stream-id
    name: "Display Name"
    url: https://stream-url       # For audio streams
    source: audio                 # audio, pager, remote, combined
    enabled: true
    pinned: false
    ignoreFirstSeconds: 30        # Skip initial audio
    recordingRetentionSeconds: 604800  # 7 days
```

## Common Configuration Changes

### Change Whisper Model
Edit config.yaml and change:
```yaml
whisper:
  model: small  # or base.en, medium, large-v3-turbo
```
Then restart the backend.

### Adjust Transcription Latency
For faster updates (shorter chunks):
```yaml
whisper:
  chunkLength: 15
  minChunkDurationSeconds: 8
```

For better sentence structure (longer chunks):
```yaml
whisper:
  chunkLength: 45
  minChunkDurationSeconds: 30
```

### Enable/Disable LLM Correction
```yaml
llm:
  enabled: false  # or true
```

### Add Domain Terms for LLM
```yaml
llm:
  domainTerms:
    - SITREP
    - SAPOL
    - YOUR_CUSTOM_TERM
```

### Add Silence Hallucination Phrases
Phrases to filter when detected during silence:
```yaml
whisper:
  silenceHallucinationPhrases:
    - "thank you"
    - "transcription by castingwords"
```

### Add a New Stream
Add to the streams array:
```yaml
streams:
  - id: my-new-stream
    name: "My New Stream"
    url: https://example.com/stream
    source: audio
    enabled: true
```

## After Configuration Changes

Most config changes require a backend restart:

```bash
# Kill existing backend
pkill -f "uvicorn.*wavecap"

# Restart
cd /Users/thw/Projects/WaveCap/backend
source .venv/bin/activate
uvicorn wavecap_backend.server:create_app --factory --host 0.0.0.0 --port 8000
```

## View Runtime Configuration via API

UI configuration (subset):
```bash
curl -s http://localhost:8000/api/ui-config | jq
```

Logging configuration:
```bash
curl -s http://localhost:8000/api/logging-config | jq
```

Access/auth configuration:
```bash
curl -s http://localhost:8000/api/access | jq
```
