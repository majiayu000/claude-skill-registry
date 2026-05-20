---
description: Enable auto TTS for this session
allowed-tools: Bash
disable-model-invocation: true
---

Enable text-to-speech for this session by creating the session marker file:

```bash
touch "${TMPDIR:-/tmp}/tts-enabled-${CLAUDE_SESSION_ID}"
```

Confirm that TTS is now enabled. Future substantial responses will offer an audio summary.
