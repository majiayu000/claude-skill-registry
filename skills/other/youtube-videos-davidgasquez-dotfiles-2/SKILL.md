---
name: youtube-videos
description: Transcribe and analyze YouTube videos
---

# YouTube Videos

Use this skill to transcribe YouTube videos and ask questions about their content.

## Tools

- **yt-dlp** — extract auto-generated subtitles
- **llm (Gemini)** — answer questions using the video and its metadata

Run `yt-dlp --help` once before first use.

## Usage

### Transcribe

```bash
yt-dlp -q --skip-download --write-auto-subs --sub-format vtt -o /tmp/$VIDEO_SLUG.vtt "VIDEO_URL"
```

### Question

```bash
llm -m gemini-3-pro-preview -a "VIDEO_URL" "QUERY"
```

## Workflow

1. Start a new tmux session with the `llm` command query to the video.
2. Generate the transcript with `yt-dlp`.
3. Wait for the `llm` response, meanwhile, read the transcription.
4. Get back to the user.
