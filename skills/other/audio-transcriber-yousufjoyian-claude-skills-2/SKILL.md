---
name: audio-transcriber
description: Extracts audio from dashcam MP4 files and produces GPU-accelerated timestamped transcripts with optional speaker diarization. This skill should be used when users request audio transcription from video files, mention dashcam audio/transcribe MP4/extract speech, want to analyze conversations from video footage, need timestamped transcripts with speaker identification, or ask to process video folders with audio extraction.
---

# Audio Transcriber

**Skill Type:** Media Processing & Analysis
**Domain:** Audio Transcription, Speech Recognition, GPU Acceleration
**Version:** 2.0
**Last Updated:** 2025-10-26

---

## Description

Extracts audio from dashcam MP4 files and produces GPU-accelerated timestamped transcripts with optional speaker diarization. Uses faster-whisper with CUDA for efficient processing, organizing outputs by date with comprehensive metadata and quality metrics.

**When to Use This Skill:**
- User requests audio transcription from video files
- User mentions "dashcam audio", "transcribe MP4", or "extract speech"
- User wants to analyze conversations from video footage
- User needs timestamped transcripts with speaker identification
- User asks to process video folders with audio extraction

---

## Quick Start

### User Trigger Phrases
- "Transcribe audio from my dashcam videos"
- "Extract and transcribe speech from [folder/date]"
- "Generate transcripts for [MP4 files/date range]"
- "Process dashcam audio with speaker identification"
- "Create subtitles from video files"

### Expected Inputs
1. **Video Folder Path** (required) - Path to MP4 files or date-organized folders
2. **Date Range** (optional) - Single day, range, or "all available"
3. **Output Directory** (optional) - Default: parallel to input with `_transcripts` suffix
4. **Processing Options** (optional) - Model size, formats, diarization, GPU settings

### Expected Outputs
- Audio extracts (WAV files) organized by date
- Transcripts in multiple formats (TXT, JSON, SRT, VTT)
- Global INDEX.csv with searchable segment metadata
- Results JSON with GPU metrics and processing statistics
- Quality reports with confidence scores and coverage

---

## Core Capabilities

### 1. User Input Acquisition (Section 0 Protocol)

**CRITICAL: Always follow the Section 0 protocol before processing.**

#### Step 1: Parse User Request
```
User: "Transcribe my dashcam videos from September 3rd"

AI Detection:
✅ Date detected: 2025-09-03
❌ Folder path not specified → Try auto-discovery
```

#### Step 2: Auto-Discovery
Search these locations in order:
1. `C:\Users\[user]\Desktop\CARDV\Movie_F\YYYYMMDD\*.MP4`
2. `G:\My Drive\PROJECTS\INVESTIGATION\DASHCAM\Movie_F\YYYYMMDD\*.MP4`
3. Current working directory + `\*.mp4`
4. User-provided explicit path

#### Step 3: Validate Files
```python
def validate_video_folder(folder_path):
    # Check folder exists
    # Count MP4 files
    # Estimate total audio duration
    # Check disk space for outputs
    # Verify FFmpeg installation
```

#### Step 4: Prompt for Missing Inputs
If files not found:
```
🎥 I need video files to transcribe. I couldn't find MP4s in the expected location.

Please provide ONE of the following:
1. **Direct folder path**: e.g., `C:\Users\yousu\Desktop\CARDV\Movie_F\20250903`
2. **Parent directory**: I'll search for date subfolders
3. **Single video file**: Process just one MP4

💡 Tip: Dashcam folders are usually organized by date (YYYYMMDD)
```

#### Step 5: Configuration Summary & Confirmation
```
📋 **Transcription Configuration Summary**

**Input:**
📁 Folder: C:\Users\yousu\Desktop\CARDV\Movie_F\20250903
📹 Videos found: 47 MP4 files
⏱️ Estimated audio: ~7.8 hours
💾 Estimated output size: ~450 MB (transcripts only)

**Processing:**
🖥️ GPU: NVIDIA GeForce RTX 4080 (detected)
🧠 Model: faster-whisper base (FP16, CUDA)
🎯 Segmentation: fixed 30s chunks
🗣️ Diarization: disabled (opt-in)
📝 Formats: txt, json, srt

**Output:**
💾 Audio extracts: C:\Users\yousu\Desktop\CARDV\Movie_F\20250903\audio\
📄 Transcripts: C:\Users\yousu\Desktop\CARDV\Movie_F\20250903\transcripts\
📊 INDEX.csv: C:\Users\yousu\Desktop\CARDV\Movie_F\20250903\transcripts\INDEX.csv

Ready to proceed? (Yes/No)
```

**NEVER begin processing without user confirmation.**

---

### 2. Audio Processing Pipeline

#### A. Audio Extraction (FFmpeg with Retry Matrix)

```python
# Primary extraction command
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav

# Retry sequence on failure:
# 1. Codec fallback: pcm_s16le → flac
# 2. Add demuxer args: -fflags +genpts -rw_timeout 30000000
# 3. Extended probe: -analyzeduration 100M -probesize 100M
```

**Quality Checks:**
- Verify audio stream exists (ffprobe preflight)
- Check duration matches video duration
- Detect silent/corrupted audio
- Log extraction errors to `_FAILED.json`

#### B. Segmentation (Two Modes)

**Fixed Mode (Default):**
- Split audio into 30-second chunks
- Predictable processing time
- No external VAD required
- Best for continuous speech

**VAD Mode (Advanced):**
- Use Silero VAD to detect speech regions
- Variable-length segments (2-60s)
- Skip long silences
- Best for sparse audio (parking mode)

**Mutual Exclusion:** Only one mode active at a time.

#### C. GPU Transcription (faster-whisper)

```python
# Load model with GPU optimization
model = WhisperModel(
    "base",
    device="cuda",
    compute_type="float16"
)

# Transcribe with word-level timestamps
segments, info = model.transcribe(
    audio_path,
    beam_size=5,
    word_timestamps=True,
    vad_filter=True
)
```

**GPU Metrics Captured:**
- Device name, VRAM, utilization
- CUDA version, driver version
- Average GPU % during run (sampled at 1-2 Hz)
- Memory usage peaks

#### D. Speaker Diarization (Optional)

**Backends:**
- **pyannote**: State-of-the-art (requires HF token + VRAM)
- **speechbrain**: Good performance (no auth required)

**Label Normalization:**
- Different backends → unified `spkA`, `spkB`, etc.
- Consistent across INDEX.csv and JSON outputs

**Fallback Behavior:**
- If HF token missing → skip diarization, log warning
- If OOM error → disable diarization, continue transcription

---

### 3. Output Generation

#### A. File Organization (Per-Day Structure)

```
C:\Users\yousu\Desktop\CARDV\Movie_F\
└── 20250903\
    ├── audio\
    │   ├── 20250903133516_059495B.wav
    │   ├── 20250903134120_059496B.wav
    │   └── ... (47 files)
    ├── transcripts\
    │   ├── 20250903133516_059495B.txt
    │   ├── 20250903133516_059495B.json
    │   ├── 20250903133516_059495B.srt
    │   └── ... (47 × 3 = 141 files)
    └── INDEX.csv
```

#### B. Format Details

**TXT (Plain Text):**
```
[00:00:15] Speaker A: Hey, where are we going?
[00:00:18] Speaker B: Just heading to the mall.
[00:00:22] Speaker A: Okay, sounds good.
```

**JSON (Complete Metadata):**
```json
{
  "video_file": "20250903133516_059495B.MP4",
  "audio_duration_sec": 60,
  "language": "en",
  "language_confidence": 0.95,
  "segments": [
    {
      "start": 15.2,
      "end": 17.8,
      "text": "Hey, where are we going?",
      "confidence": 0.89,
      "speaker": "spkA",
      "words": [
        {"word": "Hey", "start": 15.2, "end": 15.4, "confidence": 0.92},
        {"word": "where", "start": 15.5, "end": 15.8, "confidence": 0.88}
      ]
    }
  ]
}
```

**SRT (SubRip Subtitles):**
```
1
00:00:15,200 --> 00:00:17,800
[spkA] Hey, where are we going?

2
00:00:18,000 --> 00:00:20,500
[spkB] Just heading to the mall.
```

**VTT (WebVTT):**
```
WEBVTT

00:00:15.200 --> 00:00:17.800
<v spkA>Hey, where are we going?

00:00:18.000 --> 00:00:20.500
<v spkB>Just heading to the mall.
```

#### C. INDEX.csv (Global Search Index)

Composite key: `(video_rel, seg_idx)`

| Column | Description |
|--------|-------------|
| `dataset` | Movie_F / Movie_R / Park_F / Park_R |
| `date` | YYYYMMDD |
| `video_rel` | Relative path from root |
| `video_stem` | Filename without extension |
| `seg_idx` | 0-based segment index |
| `ts_start_ms` | Segment start milliseconds |
| `ts_end_ms` | Segment end milliseconds |
| `text` | Transcript text (truncated to 512 chars) |
| `text_len` | Full text length |
| `lang` | ISO language code |
| `lang_conf` | Language detection confidence |
| `conf_avg` | Average token confidence |
| `speaker` | Normalized speaker label |
| `format_mask` | Files generated (txt/json/srt/vtt) |
| `transcript_file` | Basename |
| `audio_file` | Basename |
| `engine` | e.g., `faster-whisper:base:fp16` |
| `cuda_version` | CUDA version |
| `driver_version` | Driver version |
| `created_utc` | ISO 8601 timestamp |

#### D. Results JSON (Single Source of Truth)

```json
{
  "status": "ok",
  "summary": {
    "videos_processed": 47,
    "segments": 1847,
    "hours_audio": 7.8,
    "gpu_detected": true,
    "device_count": 1,
    "devices": [
      {
        "index": 0,
        "name": "NVIDIA GeForce RTX 4080",
        "total_mem_mb": 16384,
        "free_mem_mb": 14200
      }
    ],
    "utilization": {
      "gpu_pct": 35,
      "mem_pct": 42,
      "sampling_hz": 2
    },
    "cuda_version": "12.1",
    "driver_version": "546.01",
    "torch_version": "2.2.0+cu121",
    "errors": 0,
    "failed_files": []
  },
  "artifacts": {
    "index_csv": "C:\\Users\\yousu\\Desktop\\CARDV\\Movie_F\\20250903\\INDEX.csv",
    "output_dir": "C:\\Users\\yousu\\Desktop\\CARDV\\Movie_F\\20250903\\transcripts"
  }
}
```

---

### 4. Quality & Error Handling

#### A. Resume Safety
- Skip existing transcripts unless `--force` flag
- Idempotent: re-running is safe
- Checkpoint support for long runs

#### B. Error Types & Recovery

**Per-Video Failures** (`{video_stem}_FAILED.json`):
```json
{
  "video_path": "C:\\...\\video.mp4",
  "error_type": "ffmpeg_err",
  "error_message": "Failed to decode audio stream",
  "ffprobe_metadata": {"duration": null, "codec": "h264"},
  "timestamp": "2025-09-03T14:30:00Z"
}
```

Error types:
- `ffmpeg_err`: Audio extraction failed
- `decode_err`: Whisper decode failed
- `OOM`: Out of GPU memory
- `corrupted`: Container/stream corrupted
- `no_audio`: No audio stream detected

#### C. SRT/VTT Validation
- Strictly monotonic timestamps
- No overlapping segments
- Clamp gaps <50ms
- Proper timecode formatting (comma vs period)

---

## Implementation Guide

### Phase 1: Input Acquisition
```python
# 1. Parse user request
inputs = parse_user_request(user_message)

# 2. Auto-discover video files
if not inputs['video_folder']:
    inputs['video_folder'] = auto_discover_videos()

# 3. Validate inputs
validate_video_folder(inputs['video_folder'])
check_ffmpeg_available()
check_gpu_available()

# 4. Estimate resource requirements
estimate_processing_time(inputs)
estimate_disk_space(inputs)

# 5. Present configuration summary
show_configuration_summary(inputs)

# 6. Wait for confirmation
if not user_confirms():
    return  # Do not proceed
```

### Phase 2: Audio Extraction
```python
for video_file in video_files:
    # FFprobe preflight check
    metadata = ffprobe(video_file)
    if not has_audio_stream(metadata):
        log_failed(video_file, "no_audio")
        continue

    # Extract audio with retry
    try:
        audio_path = extract_audio_ffmpeg(
            video_file,
            output_dir=audio_output_dir,
            sample_rate=16000,
            channels=1
        )
    except FFmpegError as e:
        # Retry with fallback codec
        audio_path = extract_audio_ffmpeg_retry(video_file)
```

### Phase 3: Transcription
```python
# Load model once (reuse for all files)
model = load_whisper_model(
    model_size="base",
    device="cuda",
    compute_type="float16"
)

for audio_file in audio_files:
    # Segment audio
    if segmentation_mode == "fixed":
        chunks = segment_fixed(audio_file, chunk_size=30)
    else:
        chunks = segment_vad(audio_file, vad_model)

    # Transcribe each chunk
    all_segments = []
    for chunk in chunks:
        segments = model.transcribe(chunk)
        all_segments.extend(segments)

    # Optional: Diarization
    if diarization_enabled:
        all_segments = apply_diarization(audio_file, all_segments)
```

### Phase 4: Output Generation
```python
# Generate all formats
for video_file, segments in results.items():
    # TXT
    write_txt(segments, output_dir)

    # JSON
    write_json(segments, metadata, output_dir)

    # SRT
    srt_content = generate_srt(segments)
    validate_srt_monotonic(srt_content)
    write_srt(srt_content, output_dir)

    # VTT (optional)
    write_vtt(segments, output_dir)

    # Update INDEX.csv
    append_to_index(segments, index_csv_path)
```

### Phase 5: Completion Report
```python
# Generate results JSON
results_json = {
    "status": "ok",
    "summary": collect_statistics(),
    "artifacts": list_output_files(),
    "gpu_metrics": get_gpu_metrics()
}

# Save to file
save_results_json(results_json, output_dir)

# Report to user
print(f"✅ Complete! Processed {video_count} videos")
print(f"   Transcripts: {output_dir}")
print(f"   INDEX: {index_csv_path}")
print(f"   GPU Util: {avg_gpu_pct}%")
```

---

## Reference Materials

### In This Skill

- **SKILL_MANIFEST.md** - Complete technical specification (v2.0)
- **references/TECHNICAL_SPECIFICATION.md** - Detailed implementation rules
- **scripts/batch_transcriber.py** - Main batch processing script
- **scripts/audio_extractor.py** - FFmpeg wrapper with retry logic
- **scripts/transcriber.py** - Whisper transcription engine
- **scripts/diarizer.py** - Speaker diarization integration
- **scripts/format_writers.py** - TXT/JSON/SRT/VTT generators
- **scripts/gpu_monitor.py** - GPU metrics collection
- **scripts/validation.py** - Input validation and checks
- **assets/config_template.json** - Default configuration
- **assets/params.json** - Tunable parameters

### External Documentation

- faster-whisper documentation
- FFmpeg audio processing guide
- pyannote.audio diarization guide
- SRT/VTT subtitle format specifications

---

## Tunable Parameters

```json
{
  "whisper": {
    "model_size": "base",
    "device": "cuda",
    "compute_type": "float16",
    "batch_size": 8,
    "beam_size": 5,
    "language": "en",
    "detect_language": false
  },
  "audio": {
    "sample_rate": 16000,
    "channels": 1,
    "format": "wav",
    "keep_intermediate": false
  },
  "segmentation": {
    "mode": "fixed",
    "chunk_length_sec": 30,
    "vad_min_len_sec": 2,
    "vad_max_len_sec": 60
  },
  "diarization": {
    "enabled": false,
    "backend": "pyannote",
    "min_speakers": 1,
    "max_speakers": 10
  },
  "output": {
    "formats": ["txt", "json", "srt"],
    "text_truncate_csv": 512
  },
  "parallel": {
    "max_workers": 3
  }
}
```

---

## Common Issues & Solutions

### Issue 1: "GPU not detected"
**Cause:** CUDA not installed or incompatible driver
**Solution:**
1. Check: `python -c "import torch; print(torch.cuda.is_available())"`
2. Install/update CUDA toolkit
3. Fallback to CPU: `--device cpu`

### Issue 2: "FFmpeg command failed"
**Cause:** FFmpeg not in PATH or unsupported codec
**Solution:**
1. Verify: `ffmpeg -version`
2. Install from ffmpeg.org
3. Use retry matrix with codec fallback

### Issue 3: "Out of memory (OOM)"
**Cause:** GPU VRAM insufficient for model + batch size
**Solution:**
1. Use smaller model: `tiny` or `small`
2. Reduce batch size: `--batch 4`
3. Process fewer files in parallel

### Issue 4: "Diarization failed"
**Cause:** HF token missing or network error
**Solution:**
1. Set token: `export HF_TOKEN=hf_...`
2. Accept pyannote license on HuggingFace
3. Disable diarization: `--no-diarize`

### Issue 5: "SRT validation errors"
**Cause:** Overlapping timestamps or malformed timecodes
**Solution:**
1. Enable timestamp clamping: `--clamp-gaps`
2. Check for negative durations
3. Validate with subtitle validator tool

---

## Security & Privacy Notes

### Data Sensitivity
Dashcam audio may contain:
- Personal conversations
- Addresses and locations
- Phone numbers and names
- Private information

### Processing Guidelines
1. **Local Processing Only** - Never upload audio to external services
2. **Secure Storage** - Encrypt transcripts if sharing devices
3. **Redaction** - Use `--redact` flag for PII patterns (phone, email)
4. **Retention** - Delete audio extracts after transcription if not needed

### Investigation Use
- Designed for legitimate personal data analysis
- NOT an anti-forensics tool
- All conclusions require independent corroboration

---

## Skill Invocation

This skill is invoked when the model detects:
1. User mentions "transcribe audio", "dashcam transcription", or "extract speech"
2. User requests processing of video/MP4 files for audio content
3. User provides paths to video folders
4. User asks for subtitles or timestamped transcripts

---

## Success Criteria

A successful audio transcription must:

✅ Obtain all required inputs from user (video folder, output preferences)
✅ Validate all inputs before processing (files exist, FFmpeg available, GPU detected)
✅ Present configuration summary and get confirmation
✅ Extract audio successfully (or log failures)
✅ Transcribe with GPU acceleration (or CPU fallback)
✅ Generate all requested formats (TXT, JSON, SRT, VTT)
✅ Create INDEX.csv with searchable metadata
✅ Include GPU metrics in results JSON
✅ Report output locations to user

**Key Principle:** Never guess critical inputs. Always validate, confirm, and provide clear feedback.

---

## Version History

- **v2.0** (2025-10-26) - Production-ready skill with GPU-first architecture
- **v1.5** (2025-10-25) - Added diarization support and retry matrix
- **v1.0** (2025-10-20) - Initial release with basic transcription

---

**Last Updated:** 2025-10-26
**Status:** Production Ready
**Maintained By:** Audio Transcription Pipeline Project
