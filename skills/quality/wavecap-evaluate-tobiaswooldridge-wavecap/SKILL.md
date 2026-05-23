---
name: wavecap-evaluate
description: Evaluate WaveCap audio analysis and transcription accuracy. Use when the user wants to run regression tests, compare transcriptions against ground truth, calculate WER/CER metrics, or assess overall system quality.
---

# WaveCap Evaluation Skill

Use this skill to evaluate transcription accuracy and run regression tests against known ground truth.

## Overview

WaveCap includes a regression testing framework that:
- Compares transcriptions against expected (human-corrected) text
- Calculates Word Error Rate (WER) and Character Error Rate (CER)
- Uses reviewed transcriptions as ground truth for evaluation

## Export Regression Test Data

### Export reviewed transcriptions for regression testing
```bash
# Export as regression bundle (includes audio + expected transcripts)
curl -s -o regression_bundle.zip "http://localhost:8000/api/transcriptions/export-reviewed?format=regression"

# Extract the bundle
unzip -o regression_bundle.zip -d regression_data/
```

### Regression bundle contents
```
regression_data/
├── metadata.json          # Export info
├── cases.jsonl            # Regression case definitions
└── audio/                 # Audio files
    ├── case-name-1.wav
    └── case-name-2.wav
```

### View regression cases
```bash
cat regression_data/cases.jsonl | jq -s '.'
# Or line by line
head -5 regression_data/cases.jsonl
```

## Calculate Accuracy Metrics

### Word Error Rate (WER) Analysis

WER = (Substitutions + Insertions + Deletions) / Total Reference Words

```bash
# Get transcriptions with corrections to calculate implied WER
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.reviewStatus == "corrected" and .correctedText != null)] | .[] | {
    id,
    original: .text,
    expected: .correctedText,
    original_words: (.text | split(" ") | length),
    expected_words: (.correctedText | split(" ") | length)
  }' | head -50
```

### Approximate Error Analysis
```bash
# Rough word-level difference (not true WER, but indicative)
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.reviewStatus == "corrected" and .correctedText != null)] |
  map({
    id,
    orig_len: (.text | split(" ") | length),
    corr_len: (.correctedText | split(" ") | length),
    diff: ((.text | split(" ") | length) - (.correctedText | split(" ") | length) | if . < 0 then . * -1 else . end)
  }) |
  {
    cases: length,
    avg_word_diff: (map(.diff) | add / length | . * 10 | round / 10),
    total_orig_words: (map(.orig_len) | add),
    total_corr_words: (map(.corr_len) | add)
  }'
```

## Review-Based Quality Assessment

### Overall accuracy from reviews
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '{
    total: length,
    verified_accurate: [.[] | select(.reviewStatus == "verified")] | length,
    needed_correction: [.[] | select(.reviewStatus == "corrected")] | length,
    unreviewed: [.[] | select(.reviewStatus == "pending" or .reviewStatus == null)] | length
  } | . + {
    accuracy_rate: (if (.verified_accurate + .needed_correction) > 0 then (.verified_accurate / (.verified_accurate + .needed_correction) * 100 | . * 10 | round / 10) else null end)
  }'
```

### Accuracy by stream
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq 'group_by(.streamId) | map({
    stream: .[0].streamId,
    total: length,
    verified: [.[] | select(.reviewStatus == "verified")] | length,
    corrected: [.[] | select(.reviewStatus == "corrected")] | length
  }) | map(. + {
    reviewed: (.verified + .corrected),
    accuracy_pct: (if (.verified + .corrected) > 0 then (.verified / (.verified + .corrected) * 100 | round) else null end)
  }) | sort_by(.accuracy_pct // 100) | reverse'
```

## Confidence vs Accuracy Correlation

### Check if confidence predicts accuracy
```bash
# High confidence transcriptions - how many were verified vs corrected?
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '{
    high_conf: {
      range: "0.8-1.0",
      verified: [.[] | select(.confidence >= 0.8 and .reviewStatus == "verified")] | length,
      corrected: [.[] | select(.confidence >= 0.8 and .reviewStatus == "corrected")] | length
    },
    medium_conf: {
      range: "0.6-0.8",
      verified: [.[] | select(.confidence >= 0.6 and .confidence < 0.8 and .reviewStatus == "verified")] | length,
      corrected: [.[] | select(.confidence >= 0.6 and .confidence < 0.8 and .reviewStatus == "corrected")] | length
    },
    low_conf: {
      range: "0.0-0.6",
      verified: [.[] | select(.confidence < 0.6 and .reviewStatus == "verified")] | length,
      corrected: [.[] | select(.confidence < 0.6 and .reviewStatus == "corrected")] | length
    }
  }'
```

## Manual Evaluation Workflow

### Step 1: Select samples for evaluation
```bash
# Random sample of 20 transcriptions
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.recordingUrl != null)] | .[0:20] | .[] | {id, streamId, text, recordingUrl}'
```

### Step 2: Listen to audio and compare
```bash
# Get a specific transcription with its audio URL
TRANSCRIPTION_ID="your-transcription-id"
curl -s http://localhost:8000/api/transcriptions/export | \
  jq --arg id "$TRANSCRIPTION_ID" '.[] | select(.id == $id) | {id, text, recordingUrl, confidence}'

# Audio is accessible at:
# http://localhost:8000/recordings/FILENAME.wav
```

### Step 3: Mark evaluation results
```bash
# After listening, mark as verified or provide correction
TOKEN="your-auth-token"

# If accurate:
curl -s -X PATCH "http://localhost:8000/api/transcriptions/$TRANSCRIPTION_ID/review" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reviewStatus": "verified", "reviewer": "evaluator"}'

# If needs correction:
curl -s -X PATCH "http://localhost:8000/api/transcriptions/$TRANSCRIPTION_ID/review" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"reviewStatus": "corrected", "correctedText": "actual transcript here", "reviewer": "evaluator"}'
```

## Segment-Level Analysis

### Analyze no-speech probability
```bash
# High no_speech_prob segments may indicate incorrect transcription
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?limit=20" | \
  jq '.transcriptions[] | {
    id,
    text,
    high_no_speech_segments: [.segments[]? | select(.no_speech_prob > 0.5)] | length,
    total_segments: [.segments[]?] | length
  }'
```

### Analyze log probability (transcription confidence per segment)
```bash
# Very negative avg_logprob indicates low confidence
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?limit=20" | \
  jq '.transcriptions[] | {
    id,
    text: (.text | .[0:50]),
    avg_segment_logprob: ([.segments[]?.avg_logprob] | if length > 0 then add / length else null end),
    min_segment_logprob: ([.segments[]?.avg_logprob] | min)
  }'
```

## Duration-Based Analysis

### Check transcription rate (words per second)
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.duration != null and .duration > 0)] |
  map({
    id,
    duration: .duration,
    word_count: (.text | split(" ") | length),
    words_per_sec: ((.text | split(" ") | length) / .duration | . * 10 | round / 10)
  }) |
  {
    avg_words_per_sec: (map(.words_per_sec) | add / length | . * 10 | round / 10),
    min_words_per_sec: (map(.words_per_sec) | min),
    max_words_per_sec: (map(.words_per_sec) | max)
  }'
```

### Find unusually fast/slow transcriptions
```bash
# Very fast (> 5 words/sec) or very slow (< 1 word/sec) might indicate issues
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '[.[] | select(.duration != null and .duration > 1)] |
  map(. + {wps: ((.text | split(" ") | length) / .duration)}) |
  [.[] | select(.wps > 5 or .wps < 0.5)] |
  .[:10] | .[] | {id, text: (.text | .[0:50]), duration, wps: (.wps | . * 10 | round / 10)}'
```

## Summary Report

### Generate evaluation summary
```bash
curl -s http://localhost:8000/api/transcriptions/export | \
  jq '{
    total_transcriptions: length,
    with_recordings: [.[] | select(.recordingUrl != null)] | length,
    review_status: (group_by(.reviewStatus // "pending") | map({status: .[0].reviewStatus // "pending", count: length})),
    confidence_distribution: {
      high: [.[] | select(.confidence >= 0.8)] | length,
      medium: [.[] | select(.confidence >= 0.6 and .confidence < 0.8)] | length,
      low: [.[] | select(.confidence < 0.6)] | length,
      unknown: [.[] | select(.confidence == null)] | length
    },
    accuracy_from_reviews: (
      ([.[] | select(.reviewStatus == "verified")] | length) as $verified |
      ([.[] | select(.reviewStatus == "corrected")] | length) as $corrected |
      if ($verified + $corrected) > 0
      then {verified: $verified, corrected: $corrected, accuracy_pct: ($verified / ($verified + $corrected) * 100 | round)}
      else {verified: $verified, corrected: $corrected, accuracy_pct: null}
      end
    )
  }'
```

## Tips

- WER < 10% is generally considered good for speech recognition
- Confidence scores correlate with but don't guarantee accuracy
- Use reviewed transcriptions (verified + corrected) as ground truth
- Export regression bundles periodically to track accuracy over time
- Focus review efforts on low-confidence transcriptions first
- The `no_speech_prob` segment field helps identify hallucinations
