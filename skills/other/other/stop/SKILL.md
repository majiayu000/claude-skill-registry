---
description: Disable auto TTS for this session
allowed-tools: Bash
disable-model-invocation: true
---

Disable text-to-speech for this session by removing the session marker file:

```bash
rm -f "${TMPDIR:-/tmp}/tts-enabled-${CLAUDE_SESSION_ID}"
```

Confirm that TTS is now disabled.
