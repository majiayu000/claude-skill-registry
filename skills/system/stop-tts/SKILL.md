---
name: stop-tts
description: Stop the TTS server
---

# Stop TTS Server

Stop the VibeVoice TTS server running on port 8002.

## Steps

1. Find and kill the TTS server process:

```bash
pkill -f "python server.py --http" || pkill -f "tts-mcp.*server.py"
```

2. Verify it's stopped:

```bash
curl -s http://localhost:8002/health 2>/dev/null || echo "TTS server stopped"
```

Should show "TTS server stopped" or connection refused.
