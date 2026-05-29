---
name: register-twilio-test-audio
description: Use when adding new test audio files for Twilio voice calls, uploading audio to S3, or updating the twilio_place_call.py script with new audio options.
---

# Register Twilio Test Audio

Upload audio files to S3 and register them for use with `twilio_place_call.py`.

## Prerequisites

- SSH access to `server-local` with AWS CLI configured
- Audio file must be in **mulaw format** (8kHz, mono) for Twilio compatibility

## Quick Reference

| Item | Value |
|------|-------|
| S3 Bucket | `codel-development-tts-audio` |
| S3 Prefix | `test-audio/` |
| URL Pattern | `https://codel-development-tts-audio.s3.amazonaws.com/test-audio/{filename}` |
| Script | `api/src/scripts/twilio_place_call.py` |
| Dict | `AUDIO_FILES` |

## Steps

### 1. Convert audio to mulaw format (if needed)

```bash
ffmpeg -i input.wav -ar 8000 -ac 1 -acodec pcm_mulaw output_mulaw.wav
```

### 2. Upload to S3 and make public

From `server-local` (uses `--profile codel`):

```bash
# Upload single file
aws s3 cp /path/to/audio_mulaw.wav s3://codel-development-tts-audio/test-audio/ --profile codel

# Make it publicly readable (required for Twilio to access)
aws s3api put-object-acl --bucket codel-development-tts-audio --key test-audio/audio_mulaw.wav --acl public-read --profile codel

# Verify upload and public access
curl -sI "https://codel-development-tts-audio.s3.amazonaws.com/test-audio/audio_mulaw.wav" | head -1
# Should return: HTTP/1.1 200 OK
```

### 3. Update twilio_place_call.py

Add entry to `AUDIO_FILES` dict:

```python
AUDIO_FILES = {
    # ... existing entries ...
    "newname": "https://codel-development-tts-audio.s3.amazonaws.com/test-audio/audio_mulaw.wav",
}
```

### 4. Test the audio

```bash
# Verify URL is accessible
curl -sI "https://codel-development-tts-audio.s3.amazonaws.com/test-audio/audio_mulaw.wav" | head -1
# Should return: HTTP/1.1 200 OK

# Test with a call
docker compose exec api python src/scripts/twilio_place_call.py --audio newname --to '+1234567890' --duration-minutes 1
```

## Common Issues

| Issue | Solution |
|-------|----------|
| 403 Forbidden | Check S3 bucket permissions, file may not be public |
| Audio doesn't play | Ensure mulaw format (8kHz mono) |
| Call gets error | Verify URL returns 200, not 503 |

## Naming Convention

Use descriptive names with `_mulaw` suffix:
- `fight_mulaw.wav` - Conflict/argument audio
- `neutral_mulaw.wav` - Normal conversation
- `healthyfight_mulaw.wav` - Healthy disagreement
