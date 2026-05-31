---
description: Stop any currently playing text-to-speech audio
allowed-tools: Bash
---

Stop any currently playing TTS audio:

```bash
killall say 2>/dev/null || true
```

Confirm the audio has been stopped.
