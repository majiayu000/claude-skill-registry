---
name: good-TTvideo2text
displayName: Good抖音短视频转文字Skills
description: "Extract audio from short videos (Douyin/TikTok) and transcribe to text with timestamps. Use when user provides video URL and needs audio transcription."
---

# good-TTvideo2text

Extract audio from Douyin/TikTok videos and transcribe to text using ASR service.

## Task Objective

Convert Douyin/TikTok video audio to text with timestamps, supporting both interactive UI and command-line workflow.

**Capabilities:** Video parsing, audio extraction, ASR transcription, timestamp generation

**Trigger:** User provides Douyin/TikTok URL and requests transcription

## Usage Modes

### Mode 1: Web UI (Recommended)

Visual interface for transcription management:

```bash
# Install dependencies
cd skills/good-TTvideo2text
pip install -r requirements.txt

# Start service (default port 8000)
python app/main.py

# Browser access
http://localhost:8000
```

**Features:**
- Paste video URL for instant transcription
- View results with timestamps
- Cookie management for restricted videos
- Real-time progress updates

### Mode 2: Script (Command Line)

Suitable for automation, AI workflow integration:

```bash
# Basic usage
python scripts/transcribe.py "https://v.douyin.com/xxx"

# Extract URL from share text
python scripts/transcribe.py "7.47 复制打开抖音，看看【用户名】的作品 https://v.douyin.com/xxx"

# JSON output
python scripts/transcribe.py "https://v.douyin.com/xxx" --output json

# Text output (default)
python scripts/transcribe.py "https://v.douyin.com/xxx" --output text
```

**Output Format (Text):**
```
=== Video Info ===
Title: Video title
Author: Author name
Duration: 30s

=== Transcription ===
Full Text:
Complete transcription text...

Sentences with Timestamps:
[00:00-00:03] First sentence
[00:03-00:06] Second sentence
```

**Output Format (JSON):**
```json
{
  "success": true,
  "video_info": {
    "title": "Video title",
    "author": "Author name",
    "duration": 30,
    "create_time": 1234567890
  },
  "transcription": {
    "text": "Complete transcription...",
    "sentences": [
      {
        "start_ms": 0,
        "end_ms": 3000,
        "text": "First sentence"
      }
    ]
  }
}
```

## Prerequisites

**Dependencies:**
- fastapi>=0.120.3, uvicorn>=0.35.0, httpx>=0.28.1
- TikTokDownloader dependencies (see requirements.txt)

**ASR Configuration:**
- Environment variables auto-injected by Goodable platform
- `GOODABLE_ASR_SUBMIT_URL` - ASR task submission endpoint
- `GOODABLE_ASR_QUERY_URL_TEMPLATE` - ASR result query endpoint (with {task_id} placeholder)

**Cookie Configuration (Optional):**
- Some videos require login cookies
- Configure via Web UI Settings or edit `TikTokDownloader/settings.json`
- Cookie format: Douyin web cookie string

## Standard Workflow (AI Usage)

### When User Provides URL

1. **Extract URL from input:**
   - User may provide raw URL or share text with URL
   - Use regex to extract actual video URL

2. **Call transcribe script:**
   ```bash
   python scripts/transcribe.py "USER_PROVIDED_TEXT"
   ```

3. **Handle results:**
   - Success: Present transcription text and timestamps
   - Error: Check error message for troubleshooting

### Common Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| Invalid video URL | URL format incorrect | Ask user to provide valid Douyin/TikTok URL |
| Video not found | Video deleted or requires login | Ask user to check video or provide cookies |
| No audio found | Video has no background music | Inform user this video has no audio track |
| ASR not configured | Environment variables missing | Run via Goodable platform (auto-injects vars) |
| ASR timeout | Long audio or service slow | Retry or use Web UI for monitoring |

## Resource Index

- `app/main.py` - FastAPI application entry
- `scripts/transcribe.py` - Command-line transcription script
- `TikTokDownloader/` - Video parsing library (source code)
- `TikTokDownloader/settings.json` - Cookie and configuration
- `static/index.html` - Web UI interface
- `requirements.txt` - Python dependencies
- `downloads/` - Temporary file directory

## Important Notes

1. **Cookie Requirement:** Public videos work without cookies, restricted videos need login cookies
2. **ASR Platform:** This skill requires Goodable platform's ASR service integration
3. **URL Formats Supported:**
   - Short URL: `https://v.douyin.com/xxx`
   - Full URL: `https://www.douyin.com/video/1234567890`
   - TikTok: `https://vm.tiktok.com/xxx`, `https://www.tiktok.com/@user/video/xxx`
4. **Audio Extraction:** Extracts background music URL directly (no download needed)
5. **ASR Processing Time:** Typically 5-30 seconds depending on audio length

## Example AI Usage

```markdown
User: "帮我转写这个抖音视频 7.47 复制打开抖音 https://v.douyin.com/abc123"

AI: Let me transcribe this video for you.

[Calls transcribe.py script with the provided text]

Based on the transcription:

Video: "视频标题"
Author: 作者名

Transcription:
[00:00-00:03] 第一句话内容
[00:03-00:08] 第二句话内容
...

Full text:
完整的转写文本内容...
```
