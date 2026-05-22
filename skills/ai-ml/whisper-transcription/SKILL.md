---
name: Whisper-Transcription
description: Audio transcription using local whisper.cpp server with CUDA acceleration. HTTP API for speech-to-text conversion.
---

# Whisper Transcription Server

Local speech-to-text transcription using whisper.cpp with GPU acceleration. The server runs on port 5555 and accepts audio files via HTTP POST.

## Instructions

When helping users with audio transcription, follow these guidelines:

1. **Server Location**: The whisper-server runs at `http://localhost:5555` with the large-v3 model
2. **Audio Format**: Server accepts WAV, MP3, and other common formats. 16kHz mono WAV is optimal
3. **API Endpoint**: Use POST to `/inference` with multipart form data
4. **GPU Memory**: large-v3 uses ~6GB VRAM on the RTX 3090 (24GB total)
5. **VRAM Sharing**: If OOM errors occur, wait 30-60 seconds for other GPU services to unload (see Vram-GPU-OOM skill)

## Examples

### Example 1: Basic Transcription
```
User: Transcribe this audio file

Claude: I'll send the audio to the local Whisper server:

curl -X POST http://localhost:5555/inference \
  -F "file=@audio.wav"

The server returns JSON with the transcribed text.
```

### Example 2: Recording and Transcribing
```
User: Record my voice and transcribe it

Claude: I'll record audio then send it to Whisper:

1. Record 5 seconds of audio:
   arecord -d 5 -f S16_LE -r 16000 -c 1 recording.wav

2. Transcribe:
   curl -X POST http://localhost:5555/inference \
     -F "file=@recording.wav"
```

### Example 3: Python Integration
```
User: How do I use Whisper from Python?

Claude: Use requests to POST to the inference endpoint:

[Provides implementation using the Python pattern from reference material below]
```

---

# Reference Implementation Details

## Server Configuration

**Location**: `~/whisper.cpp/build/bin/whisper-server`
**Model**: `~/whisper.cpp/models/ggml-large-v3.bin`
**Port**: 5555

### Server Startup Command

```bash
~/whisper.cpp/build/bin/whisper-server \
  -m ~/whisper.cpp/models/ggml-large-v3.bin \
  -l en \
  --port 5555 \
  --host 0.0.0.0
```

### Systemd Service

**Location**: `/etc/systemd/system/whisper-server.service`

```ini
[Unit]
Description=Whisper.cpp Transcription Server
After=network.target

[Service]
Type=simple
User=matt
WorkingDirectory=/home/matt/whisper.cpp/build
ExecStart=/home/matt/whisper.cpp/build/bin/whisper-server \
  -m /home/matt/whisper.cpp/models/ggml-large-v3.bin \
  -l en \
  --port 5555 \
  --host 0.0.0.0 \
  --threads 4
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## API Reference

### POST /inference

Transcribe an audio file.

**Request:**
```bash
curl -X POST http://localhost:5555/inference \
  -F "file=@audio.wav" \
  -F "response_format=json"
```

**Response:**
```json
{
  "text": "transcribed text here"
}
```

### GET /

Health check endpoint.

## Python Integration

```python
import requests

def transcribe(audio_path: str, server_url: str = "http://localhost:5555") -> str:
    """Transcribe audio file using local Whisper server."""
    with open(audio_path, "rb") as f:
        response = requests.post(
            f"{server_url}/inference",
            files={"file": f},
            timeout=120
        )
    response.raise_for_status()
    return response.json().get("text", "")

# Usage
text = transcribe("recording.wav")
print(text)
```

## Shell Integration

```bash
#!/bin/bash
# transcribe.sh - Quick transcription helper

WHISPER_URL="${WHISPER_URL:-http://localhost:5555}"

if [ -z "$1" ]; then
    echo "Usage: transcribe.sh <audio_file>"
    exit 1
fi

curl -s -X POST "$WHISPER_URL/inference" \
    -F "file=@$1" | jq -r '.text'
```

## Troubleshooting

### Server Won't Start

**Cause:** Model file missing or CUDA unavailable

**Solution:**
```bash
# Check model exists
ls -lh ~/whisper.cpp/models/ggml-large-v3.bin

# Check CUDA
nvidia-smi
```

### OOM Error

**Cause:** Other GPU services using VRAM

**Solution:**
```bash
# Check GPU memory usage
nvidia-smi

# Wait for other services to unload, or manually stop them
# See Vram-GPU-OOM skill for retry patterns
```

### Slow Transcription

**Cause:** CPU fallback instead of GPU

**Solution:**
```bash
# Verify GPU is being used during transcription
watch -n 1 nvidia-smi
# Should show whisper-server using GPU memory
```

### Connection Refused

**Cause:** Server not running

**Solution:**
```bash
# Check service status
systemctl status whisper-server

# Start if stopped
sudo systemctl start whisper-server

# View logs
journalctl -u whisper-server -f
```

## Performance Notes

- **Speed**: ~2-4x real-time (1 second audio = 0.25-0.5 seconds processing)
- **VRAM Usage**: ~6GB for large-v3
- **Accuracy**: Excellent for English speech
- **Latency**: First request may be slower (model loading)
