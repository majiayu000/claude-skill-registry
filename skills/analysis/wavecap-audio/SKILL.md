---
name: wavecap-audio
description: Analyze recorded audio files from WaveCap. Use when the user wants to inspect audio recordings, check audio quality, list available recordings, or get audio file metadata.
---

# WaveCap Audio Analysis Skill

Use this skill to analyze and inspect recorded audio files from WaveCap transcription sessions.

## Recordings Location

Audio recordings are stored in the state directory:
```bash
STATE_DIR="/Users/thw/Projects/WaveCap/state"
RECORDINGS_DIR="$STATE_DIR/recordings"
```

Recordings are also accessible via HTTP at `http://localhost:8000/recordings/`

## List Available Recordings

### List all recordings
```bash
ls -la "$STATE_DIR/recordings/" | head -50
```

### List recordings with sizes (sorted by date)
```bash
ls -lht "$STATE_DIR/recordings/" | head -30
```

### Count total recordings
```bash
ls "$STATE_DIR/recordings/" 2>/dev/null | wc -l
```

### Find recordings by date
```bash
# Today's recordings
find "$STATE_DIR/recordings" -name "*.wav" -mtime 0 -type f

# Last 7 days
find "$STATE_DIR/recordings" -name "*.wav" -mtime -7 -type f
```

## Get Audio File Metadata

### Basic file info
```bash
file "$STATE_DIR/recordings/FILENAME.wav"
```

### Detailed audio properties (requires ffprobe/sox)
```bash
# Using ffprobe (if available)
ffprobe -v quiet -show_format -show_streams "$STATE_DIR/recordings/FILENAME.wav" 2>/dev/null | grep -E "duration|sample_rate|channels|bit_rate"

# Using soxi (if sox installed)
soxi "$STATE_DIR/recordings/FILENAME.wav" 2>/dev/null
```

### Get duration of a recording
```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$STATE_DIR/recordings/FILENAME.wav" 2>/dev/null
```

## Find Recordings for a Transcription

### Get recording URL from transcription
```bash
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?limit=10" | \
  jq '.transcriptions[] | {id, timestamp, recordingUrl, text}'
```

### Check if recording file exists
```bash
RECORDING_URL="recordings/abc123.wav"
FILENAME=$(basename "$RECORDING_URL")
ls -la "$STATE_DIR/recordings/$FILENAME" 2>/dev/null || echo "Recording not found"
```

## Analyze Audio Quality

### Check for very short recordings (likely noise/errors)
```bash
find "$STATE_DIR/recordings" -name "*.wav" -size -10k -type f | head -20
```

### Check for large recordings (long transmissions)
```bash
find "$STATE_DIR/recordings" -name "*.wav" -size +500k -type f | head -20
```

### Get total disk usage
```bash
du -sh "$STATE_DIR/recordings/"
```

### List recordings without transcriptions
```bash
# Get all transcription recording URLs
TRANSCRIBED=$(curl -s http://localhost:8000/api/transcriptions/export | \
  jq -r '.[].recordingUrl // empty' | xargs -I{} basename {} | sort | uniq)

# Compare with files on disk
ls "$STATE_DIR/recordings/" | sort > /tmp/all_recordings.txt
echo "$TRANSCRIBED" | sort > /tmp/transcribed.txt
comm -23 /tmp/all_recordings.txt /tmp/transcribed.txt | head -20
```

## Stream Audio via API

### Access recording via HTTP
```bash
# Recordings are served at /recordings/
curl -s -I "http://localhost:8000/recordings/FILENAME.wav"

# Download a recording
curl -o local_copy.wav "http://localhost:8000/recordings/FILENAME.wav"
```

### Stream live audio (if stream supports it)
```bash
# Check if stream supports live audio
curl -s http://localhost:8000/api/streams | jq '.[] | select(.source == "audio" or .source == "remote") | {id, name, source}'
```

## Clean Up Old Recordings

### Find recordings older than 30 days
```bash
find "$STATE_DIR/recordings" -name "*.wav" -mtime +30 -type f | wc -l
```

### Calculate space used by old recordings
```bash
find "$STATE_DIR/recordings" -name "*.wav" -mtime +30 -type f -exec du -ch {} + 2>/dev/null | tail -1
```

## Tips

- Recording filenames typically include a UUID or timestamp
- Use `recordingUrl` from transcription API responses to link audio to transcripts
- The recordings directory may grow large over time - monitor disk usage
- Audio files are WAV format, typically 16kHz mono
- Very short recordings (< 1 second) may be noise or squelch breaks
