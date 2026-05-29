---
name: start-tts
description: Start the TTS server in HTTP mode for audio generation
---

# Start TTS Server

Start the VibeVoice TTS server in HTTP mode on port 8002.

## Steps

1. Run the TTS server in the background:

```bash
cd /home/smolen/dev/EnglishConnect/src/services/tts-mcp && source .venv/bin/activate && python server.py --http
```

Run this command in the background so it doesn't block the conversation.

2. Verify it's running:

```bash
curl -s http://localhost:8002/health
```

Should return `{"status":"ok"}`.

## Notes

- Server runs on port 8002
- Required for `generate_demos.py` and `regenerate_example.py` scripts
- Uses GPU for inference
