---
name: wavecap-transcripts
description: Check and analyze WaveCap transcriptions. Use when the user wants to inspect transcript quality, find problematic transcriptions, compare original vs corrected text, or audit transcription accuracy.
---

# WaveCap Transcripts Analysis Skill

Use this skill to inspect, analyze, and audit transcription quality in WaveCap.

## Get Transcriptions

### List recent transcriptions for a stream
```bash
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?limit=20" | \
  jq '.transcriptions[] | {id, timestamp, text, confidence, reviewStatus}'
```

### Get all transcriptions across streams
```bash
curl -s http://localhost:8000/api/transcriptions/export | jq 'length'
```

### Get transcription with full details
```bash
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?limit=100" | \
  jq '.transcriptions[] | select(.id == "TRANSCRIPTION_ID")'
```

## Quality Analysis

### Find low-confidence transcriptions
```bash
# Very low confidence (< 0.5) - likely errors
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.confidence != null and .confidence < 0.5)] | sort_by(.confidence) | .[:20] | .[] | {id, streamId, confidence, text}'

# Medium-low confidence (0.5 - 0.7) - may need review
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.confidence != null and .confidence >= 0.5 and .confidence < 0.7)] | length'
```

### Find very short transcriptions (might be noise)
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select((.text | length) < 10)] | .[:20] | .[] | {id, text, duration, confidence}'
```

### Find transcriptions with common error patterns
```bash
# Find transcriptions with repeated words (stuttering artifact)
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.text | test("\\b(\\w+)\\s+\\1\\b"))] | .[:10] | .[] | {id, text}'

# Find transcriptions with "[inaudible]" or similar markers
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.text | test("inaudible|unclear|unintelligible"; "i"))] | length'
```

### Analyze confidence distribution
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq 'group_by(.confidence | . * 10 | floor / 10) | map({confidence_bucket: .[0].confidence | . * 10 | floor / 10, count: length}) | sort_by(.confidence_bucket)'
```

## Compare Original vs Corrected

### List corrected transcriptions
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.reviewStatus == "corrected")] | .[] | {id, original: .text, corrected: .correctedText, reviewer: .reviewedBy}'
```

### Show diff between original and corrected
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.reviewStatus == "corrected")] | .[:5] | .[] | "--- Original ---\n" + .text + "\n--- Corrected ---\n" + .correctedText + "\n"'
```

### Calculate correction rate
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '{
    total: length,
    corrected: [.[] | select(.reviewStatus == "corrected")] | length,
    verified: [.[] | select(.reviewStatus == "verified")] | length,
    pending: [.[] | select(.reviewStatus == "pending" or .reviewStatus == null)] | length
  } | . + {correction_rate: (.corrected / .total * 100 | . * 100 | round / 100)}'
```

## Review Status Audit

### Count by review status
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq 'group_by(.reviewStatus // "pending") | map({status: .[0].reviewStatus // "pending", count: length})'
```

### List transcriptions needing review (low confidence, unreviewed)
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select((.reviewStatus == "pending" or .reviewStatus == null) and .confidence != null and .confidence < 0.7)] | sort_by(.confidence) | .[:20] | .[] | {id, streamId, confidence, text}'
```

### Find recently reviewed transcriptions
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.reviewedAt != null)] | sort_by(.reviewedAt) | reverse | .[:10] | .[] | {id, reviewStatus, reviewedAt, reviewedBy}'
```

## Stream-by-Stream Analysis

### Transcription count per stream
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq 'group_by(.streamId) | map({stream: .[0].streamId, count: length}) | sort_by(.count) | reverse'
```

### Average confidence per stream
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq 'group_by(.streamId) | map({
    stream: .[0].streamId,
    count: length,
    avg_confidence: ([.[] | .confidence // 0] | add / length | . * 100 | round / 100)
  }) | sort_by(.avg_confidence)'
```

### Find streams with quality issues
```bash
# Streams with many low-confidence transcriptions
curl -s http://localhost:8000/api/transcriptions/export | \
  jq 'group_by(.streamId) | map({
    stream: .[0].streamId,
    total: length,
    low_confidence: [.[] | select(.confidence != null and .confidence < 0.6)] | length
  }) | map(. + {pct_low: (.low_confidence / .total * 100 | round)}) | sort_by(.pct_low) | reverse | .[:10]'
```

## Segment Analysis

### Inspect transcription segments (word-level timing)
```bash
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?limit=5" | \
  jq '.transcriptions[0].segments'
```

### Find segments with low confidence (within a transcription)
```bash
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?limit=10" | \
  jq '.transcriptions[] | {id, low_conf_segments: [.segments[]? | select(.no_speech_prob > 0.5 or .avg_logprob < -1)] | length}'
```

## Time-Based Analysis

### Transcriptions in the last hour
```bash
SINCE=$(date -u -v-1H +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -d "1 hour ago" +"%Y-%m-%dT%H:%M:%SZ")
curl -s http://localhost:8000/api/transcriptions/export | \
  jq --arg since "$SINCE" '[.[] | select(.timestamp >= $since)] | length'
```

### Activity over time
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq 'group_by(.timestamp | split("T")[0]) | map({date: .[0].timestamp | split("T")[0], count: length}) | sort_by(.date) | .[-14:]'
```

## Text Search

### Search transcriptions for keywords
```bash
curl -s "http://localhost:8000/api/transcriptions/search?q=fire&limit=20" | \
  jq '.results[] | {id, streamId, timestamp, text, matchCount}'
```

### Find transcriptions mentioning addresses
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.text | test("\\d+\\s+\\w+\\s+(street|st|avenue|ave|road|rd|drive|dr|lane|ln)"; "i"))] | .[:10] | .[] | {id, text}'
```

## Tips

- Use `.confidence` to prioritize which transcriptions need review
- The `reviewStatus` field can be: `pending`, `corrected`, or `verified`
- `correctedText` contains human-corrected version when `reviewStatus == "corrected"`
- Segments provide word-level timing and confidence via `no_speech_prob` and `avg_logprob`
- Very short transcriptions with low confidence are often noise, not real speech
- Use the search API for keyword queries rather than filtering exports client-side
