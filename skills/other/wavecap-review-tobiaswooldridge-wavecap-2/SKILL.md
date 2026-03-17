---
name: wavecap-review
description: Review and correct WaveCap transcriptions. Use when the user wants to mark transcriptions as verified, add corrections, or manage the review workflow.
---

# WaveCap Review Skill

Use this skill to manage the transcription review workflow in WaveCap.

## Authentication Required

Review operations require editor authentication:

```bash
# Get auth token
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"password": "YOUR_EDITOR_PASSWORD"}' | jq -r '.token')
```

## Review Status Values

- `pending` - Not yet reviewed (default)
- `corrected` - Reviewed and corrected
- `verified` - Reviewed and confirmed accurate

## Update Transcription Review

### Mark as Verified (transcript is accurate)

```bash
curl -s -X PATCH "http://localhost:8000/api/transcriptions/{TRANSCRIPTION_ID}/review" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "reviewStatus": "verified",
    "reviewer": "your_name"
  }' | jq
```

### Mark as Corrected (provide corrected text)

```bash
curl -s -X PATCH "http://localhost:8000/api/transcriptions/{TRANSCRIPTION_ID}/review" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "correctedText": "The corrected transcription text here",
    "reviewStatus": "corrected",
    "reviewer": "your_name"
  }' | jq
```

### Clear Review (reset to pending)

```bash
curl -s -X PATCH "http://localhost:8000/api/transcriptions/{TRANSCRIPTION_ID}/review" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "correctedText": null,
    "reviewStatus": "pending",
    "reviewer": null
  }' | jq
```

## Find Transcriptions to Review

### Get pending transcriptions (unreviewed)

```bash
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?limit=50" | \
  jq '[.transcriptions[] | select(.reviewStatus == "pending")] | .[:10]'
```

### Get low-confidence transcriptions (likely need review)

```bash
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?limit=100" | \
  jq '[.transcriptions[] | select(.confidence < 0.7 and .reviewStatus == "pending")] | sort_by(.confidence) | .[:10] | .[] | {id, text, confidence}'
```

### Count by review status

```bash
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?limit=500" | \
  jq '.transcriptions | group_by(.reviewStatus) | map({status: .[0].reviewStatus, count: length})'
```

## Review Response Format

After updating a review, the response contains the updated transcription:

```json
{
  "id": "transcription-uuid",
  "streamId": "stream-id",
  "text": "original transcription",
  "correctedText": "corrected transcription",
  "reviewStatus": "corrected",
  "reviewedAt": "2025-01-15T12:30:00Z",
  "reviewedBy": "reviewer_name",
  ...
}
```

## Batch Review Workflow

For reviewing multiple transcriptions:

```bash
# 1. Get pending transcriptions with low confidence
PENDING=$(curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?limit=100" | \
  jq -r '[.transcriptions[] | select(.confidence < 0.8 and .reviewStatus == "pending")] | .[].id')

# 2. Loop through and review each
for ID in $PENDING; do
  echo "Reviewing: $ID"
  # Get the transcription
  curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?limit=500" | \
    jq --arg id "$ID" '.transcriptions[] | select(.id == $id) | {text, confidence, recordingUrl}'

  # Mark as verified (or prompt for correction)
  # curl -s -X PATCH "http://localhost:8000/api/transcriptions/$ID/review" ...
done
```

## Tips

- Always include a `reviewer` name for audit trail
- Use `correctedText: null` to clear a previous correction
- Low confidence scores (< 0.7) often indicate transcription errors
- The `reviewedAt` timestamp is set automatically by the server
