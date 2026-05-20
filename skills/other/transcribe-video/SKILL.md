---
name: transcribe-video
description: Generate subtitles (SRT/VTT) and plain text transcripts from video or audio files using AWS Transcribe. Use when creating captions, extracting spoken content, generating transcripts for notes, or making video content searchable.
argument-hint: "[file] [language-code]"
allowed-tools: Bash(ffmpeg:*), Bash(aws:*), Bash(ls:*), Bash(rm:*), Bash(which:*)
---

# Video Transcription Skill

Generate subtitles and transcripts from `$ARGUMENTS` (a video or audio file path, optionally followed by a language code like `en-US` or `es-ES`) using AWS Transcribe.

Outputs `.srt`, `.vtt`, and `.txt` files next to the source file.

## Process

1. **Verify prerequisites** - check `ffmpeg` and `aws` CLI are installed and configured
2. **Extract audio** from the video as MP3 using ffmpeg
3. **Create temporary S3 bucket**, upload audio
4. **Run AWS Transcribe** job with SRT and VTT subtitle output
5. **Download results** and generate plain text transcript
6. **Clean up all AWS resources** - delete S3 bucket, Transcribe job, and temp files. No recurring costs.

## Prerequisites

- `ffmpeg` installed (`brew install ffmpeg`)
- `aws` CLI installed and configured with valid credentials (`brew install awscli && aws configure`)
- AWS credentials need permissions for: `s3:*` (create/delete buckets), `transcribe:*` (start/delete jobs)

## Step-by-Step

### Step 1: Extract audio

```bash
ffmpeg -i "input.mp4" -vn -acodec mp3 -q:a 2 "/tmp/transcribe-audio.mp3" -y
```

### Step 2: Create temp S3 bucket and upload

```bash
BUCKET="tmp-transcribe-$(date +%s)"
aws s3 mb "s3://$BUCKET" --region us-east-1
aws s3 cp "/tmp/transcribe-audio.mp3" "s3://$BUCKET/audio.mp3"
```

### Step 3: Start transcription job

```bash
JOB_NAME="tmp-job-$(date +%s)"
aws transcribe start-transcription-job \
  --transcription-job-name "$JOB_NAME" \
  --language-code en-US \
  --media-format mp3 \
  --media "MediaFileUri=s3://$BUCKET/audio.mp3" \
  --subtitles "Formats=srt,vtt" \
  --output-bucket-name "$BUCKET" \
  --region us-east-1
```

**Language codes:** `en-US`, `es-ES`, `fr-FR`, `de-DE`, `pt-BR`, `ja-JP`, `zh-CN`, `it-IT`, `ko-KR`, etc. Default to `en-US` if not specified.

### Step 4: Poll until complete

```bash
while true; do
  STATUS=$(aws transcribe get-transcription-job \
    --transcription-job-name "$JOB_NAME" \
    --region us-east-1 \
    --query 'TranscriptionJob.TranscriptionJobStatus' \
    --output text)
  if [ "$STATUS" = "COMPLETED" ] || [ "$STATUS" = "FAILED" ]; then break; fi
  sleep 5
done
```

### Step 5: Download subtitle files

Save `.srt` and `.vtt` next to the original file:

```bash
aws s3 cp "s3://$BUCKET/$JOB_NAME.srt" "/path/to/input.srt"
aws s3 cp "s3://$BUCKET/$JOB_NAME.vtt" "/path/to/input.vtt"
```

### Step 6: Generate plain text transcript

Download the JSON result and extract the full transcript text:

```bash
aws s3 cp "s3://$BUCKET/$JOB_NAME.json" "/tmp/transcribe-result.json"
```

Then use a tool to extract the `.results.transcripts[0].transcript` field from the JSON and save it as a `.txt` file next to the original.

### Step 7: Clean up everything

**IMPORTANT:** Always clean up to avoid recurring S3 storage costs.

```bash
# Delete S3 bucket and all contents
aws s3 rb "s3://$BUCKET" --force --region us-east-1

# Delete the transcription job
aws transcribe delete-transcription-job --transcription-job-name "$JOB_NAME" --region us-east-1

# Delete temp audio file
rm -f "/tmp/transcribe-audio.mp3" "/tmp/transcribe-result.json"
```

## Real-World Results (Reference)

From actual transcription runs:

| Video | Duration | Audio Size | Transcribe Time | Subtitle Segments |
|-------|----------|------------|-----------------|-------------------|
| X/Twitter clip | 2:40 | 2.5 MB | ~20 seconds | 83 |
| Screen recording | 18:45 | 11.4 MB | ~60 seconds | 500+ |

### Key Insights

1. **AWS Transcribe is fast** - even 19-minute videos complete in about a minute
2. **Short-form content** (tweets, reels) transcribes almost instantly
3. **Cost is negligible** - AWS Transcribe charges ~$0.024/min, so a 19-min video costs ~$0.46
4. **Cleanup is critical** - always delete the S3 bucket to avoid storage charges
5. **SRT is most compatible** - works with most video players and editors; VTT is better for web

## Output Files

```
original-video.mp4
original-video.srt          # Subtitles with timestamps (most compatible)
original-video.vtt          # Web-optimized subtitles (for HTML5 <track>)
original-video.txt          # Plain text transcript (no timestamps)
```

## After Transcription

1. **Verify all output files exist**: `ls -lh /path/to/original-video.{srt,vtt,txt}`
2. Report the number of subtitle segments and total duration
3. Confirm all AWS resources have been cleaned up (no S3 buckets, no Transcribe jobs remaining)
