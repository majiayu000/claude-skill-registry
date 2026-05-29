---
name: xuezh
description: Teach Mandarin using the xuezh engine for review, speaking, and audits.
metadata: {"moltbot":{"nix":{"plugin":"github:joshp123/xuezh","systems":["aarch64-darwin","x86_64-linux"]},"config":{"requiredEnv":["XUEZH_AZURE_SPEECH_KEY_FILE","XUEZH_AZURE_SPEECH_REGION"],"stateDirs":[".config/xuezh"],"example":"config = { env = { XUEZH_AZURE_SPEECH_KEY_FILE = \"/run/agenix/xuezh-azure-speech-key\"; XUEZH_AZURE_SPEECH_REGION = \"westeurope\"; }; stateDirs = [ \".config/xuezh\" ]; };"},"cliHelp":"xuezh - Chinese learning engine\n\nUsage:\n  xuezh [command]\n\nAvailable Commands:\n  snapshot  Fetch learner state snapshot\n  review    Review due items\n  audio     Process speech audio\n  items     Manage learning items\n  events    Log learning events\n\nFlags:\n  -h, --help   help for xuezh\n  --json       Output JSON\n"}}
---

# Xuezh Skill

## Contract

Use the xuezh CLI exactly as specified. If a command is missing, ask for implementation instead of guessing.

## Default loop

1) Call `xuezh snapshot`.
2) Pick a tiny plan (1-2 bullets).
3) Run a short activity.
4) Log outcomes.

## CLI examples

```bash
xuezh snapshot --profile default
xuezh review next --limit 10
xuezh audio process-voice --file ./utterance.wav
```
