---
name: transcription
description: Transcribes audio and video files through case.dev with speaker diarization. Supports MP3, WAV, M4A, FLAC, OGG, WEBM, MP4 up to 5GB. Use when the user mentions "transcribe", "transcription", "deposition recording", "hearing audio", "speaker labels", or needs to convert audio/video to text.
---

# case.dev Transcription

Audio and video transcription with speaker diarization, ideal for depositions, hearings, and recorded proceedings. Supports MP3, WAV, M4A, FLAC, OGG, WEBM, and MP4 up to 5GB.

Requires the `casedev` CLI. See `setup` skill for installation and auth.

## Start a Transcription

The source file must be in a vault:

```bash
casedev transcribe run --vault VAULT_ID --object OBJECT_ID --json
```

The object must be an audio or video file. Non-media files are rejected.

Flags:
- `--speaker-labels` — enable speaker diarization
- `--speakers-expected N` — hint for number of speakers
- `--language` — language code (e.g., `en`, `es`)
- `--format` — output format
- `--auto-highlights` — extract key phrases

Uses focused vault if set via `casedev focus set --vault`.

## Check Status

```bash
casedev transcribe status TRANSCRIPTION_ID --json
```

Returns: ID, status, vault, source/result object IDs, audio duration, word count, confidence.

Statuses: `queued` -> `processing` -> `completed` or `failed`.

## Get Result

```bash
casedev transcribe result TRANSCRIPTION_ID --json
```

Returns the transcript text. If the result is stored as a vault object, it fetches the text automatically. Fails if the job is not yet completed.

## Watch Until Complete

```bash
casedev transcribe watch TRANSCRIPTION_ID --json
```

Polls until done, then prints the result. Flags:
- `--interval` / `-i` — poll interval in seconds (default: 3)
- `--timeout` / `-t` — max wait in seconds (default: 900)

## Common Workflow

### Transcribe a deposition recording

```bash
# 1. Upload to vault
casedev vault object upload ./deposition-2024-01-15.mp3 --vault VAULT_ID --json

# 2. Start transcription with speaker labels
casedev transcribe run --vault VAULT_ID --object OBJECT_ID --speaker-labels --speakers-expected 4 --json

# 3. Watch until complete
casedev transcribe watch TRANSCRIPTION_ID --json

# 4. Or check status + get result separately
casedev transcribe status TRANSCRIPTION_ID --json
casedev transcribe result TRANSCRIPTION_ID --json
```

### Using the job tracker

```bash
# Transcription jobs are auto-tracked
casedev jobs list --type transcribe --json
casedev jobs watch JOB_ID --type transcribe --json
```

## Troubleshooting

**"Invalid file type for transcribe"**: Only audio/video MIME types are accepted. Check the object with `casedev vault object list --vault VAULT_ID`. Upload audio files, not PDFs.

**"Invalid object ID for this vault"**: Run `casedev vault object list --vault VAULT_ID` to see valid IDs.

**"Transcription is not complete yet"**: Wait for the job to finish. Use `casedev transcribe watch` or `casedev jobs watch`.

**Transcription failed**: Check `casedev transcribe status TRANSCRIPTION_ID --json` for the error message. Common causes: corrupted file, unsupported codec, file too large.

**Long audio (2+ hours)**: Increase timeout with `--timeout 3600`. Large files take proportionally longer.
