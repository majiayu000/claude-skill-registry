---
name: tubeify
category: media
description: AI video editor for YouTube — removes pauses, filler words, and dead air from raw recordings via API
---

# Tubeify

AI-powered video editing for YouTube creators. Submit a raw recording URL, get back a polished, trimmed video automatically — no manual editing required.

## When to Use This Skill

- User wants to remove dead air or pauses from a video recording
- User wants to clean up filler words (um, uh, etc.) from a video
- User wants to automate post-recording video editing for YouTube

## What This Skill Does

1. Authenticates to Tubeify with a wallet address
2. Submits the raw video URL with processing options
3. Polls for completion and returns a download link

## Usage

```bash
# Authenticate
curl -c session.txt -X POST https://tubeify.xyz/index.php \
  -d "wallet=<YOUR_WALLET>"

# Submit video
curl -b session.txt -X POST https://tubeify.xyz/process.php \
  -d "video_url=<URL>" \
  -d "remove_pauses=true" \
  -d "remove_fillers=true"

# Check status
curl -b session.txt https://tubeify.xyz/status.php
```

## Links

- Website: https://tubeify.xyz
- ClawHub: https://clawhub.ai/esokullu/tubeify
- Full docs: https://tubeify.xyz/skills.md
