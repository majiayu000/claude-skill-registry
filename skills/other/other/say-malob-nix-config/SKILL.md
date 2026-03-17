---
description: Speak the last response aloud using text-to-speech
allowed-tools: Bash
argument-hint: "[rate]"
arguments:
  - name: rate
    description: Speaking rate in words per minute (default: 300)
    required: false
---

Run the TTS script to speak the last response aloud:

```bash
${CLAUDE_PLUGIN_ROOT}/skills/say/scripts/speak.sh ${CLAUDE_SESSION_ID} $1
```
