---
name: wavecap-export
description: Export WaveCap transcriptions and pager data. Use when the user wants to export transcriptions as JSON, download reviewed transcriptions with audio, or export pager feed data.
---

# WaveCap Export Skill

Use this skill to export transcription data from WaveCap.

## Export All Transcriptions (JSON)

Export all transcriptions across all streams as a JSON array:

```bash
curl -s http://localhost:8000/api/transcriptions/export > transcriptions.json
```

### Filter with jq

```bash
# Export just text and timestamps
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | {streamId, timestamp, text}]' > transcriptions_simple.json

# Export only transcriptions from a specific stream
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.streamId == "STREAM_ID")]' > stream_transcriptions.json

# Export with corrections where available
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | {timestamp, text: (.correctedText // .text), reviewStatus}]' > transcriptions_corrected.json
```

## Export Reviewed Transcriptions (ZIP)

Download reviewed transcriptions with audio recordings as a ZIP file:

```bash
curl -s -o reviewed_export.zip http://localhost:8000/api/transcriptions/export-reviewed
```

### Filter by Review Status

```bash
# Only corrected transcriptions
curl -s -o corrected.zip "http://localhost:8000/api/transcriptions/export-reviewed?status=corrected"

# Only verified transcriptions
curl -s -o verified.zip "http://localhost:8000/api/transcriptions/export-reviewed?status=verified"

# Both corrected and verified (default)
curl -s -o reviewed.zip "http://localhost:8000/api/transcriptions/export-reviewed?status=corrected&status=verified"
```

### Export for Regression Testing

Export in a format suitable for audio regression tests:

```bash
curl -s -o regression_bundle.zip "http://localhost:8000/api/transcriptions/export-reviewed?format=regression"
```

### ZIP Contents

The exported ZIP contains:

```
reviewed_export.zip
├── metadata.json          # Export timestamp, filter info
├── transcriptions.jsonl   # One JSON object per line
└── recordings/            # Audio files (if available)
    ├── abc123.wav
    └── def456.wav
```

## Export Pager Feed Data

Export all pager messages for a specific stream:

```bash
# Requires editor auth
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"password": "YOUR_EDITOR_PASSWORD"}' | jq -r '.token')

curl -s -o pager_export.zip \
  -H "Authorization: Bearer $TOKEN" \
  "http://localhost:8000/api/pager-feeds/{STREAM_ID}/export"
```

### Pager Export Contents

```
pager_export.zip
├── metadata.json    # Export metadata
└── messages.jsonl   # One pager message per line
```

## Working with JSONL Files

JSONL (JSON Lines) files have one JSON object per line:

```bash
# Read JSONL and convert to array
cat transcriptions.jsonl | jq -s '.'

# Filter JSONL
cat transcriptions.jsonl | jq 'select(.confidence > 0.8)'

# Count entries
wc -l transcriptions.jsonl

# Get first 10 entries
head -10 transcriptions.jsonl | jq -s '.'
```

## Export Statistics

Get summary statistics from exported data:

```bash
# Count by stream
curl -s http://localhost:8000/api/transcriptions/export | \
  jq 'group_by(.streamId) | map({stream: .[0].streamId, count: length})'

# Count by review status
curl -s http://localhost:8000/api/transcriptions/export | \
  jq 'group_by(.reviewStatus) | map({status: .[0].reviewStatus, count: length})'

# Average confidence by stream
curl -s http://localhost:8000/api/transcriptions/export | \
  jq 'group_by(.streamId) | map({stream: .[0].streamId, avgConfidence: ([.[].confidence] | add / length)})'

# Total duration of all recordings
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[].duration // 0] | add'
```

## Export for Analysis

### CSV Export

```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq -r '["timestamp","streamId","text","confidence"], (.[] | [.timestamp, .streamId, .text, .confidence]) | @csv' > transcriptions.csv
```

### Export with Pager Incident Details

```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.pagerIncident != null) | {
    timestamp,
    incidentId: .pagerIncident.incidentId,
    callType: .pagerIncident.callType,
    address: .pagerIncident.address,
    alarmLevel: .pagerIncident.alarmLevel
  }]' > incidents.json
```

## Tips

- Large exports may take time - use `-o` to save directly to file
- JSONL format is more memory-efficient for processing large datasets
- The ZIP export includes audio files which can be large
- Use `jq -c` for compact output when piping to files
- For incremental exports, use the search API with date filters instead
