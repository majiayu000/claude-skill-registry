---
name: video-transcript
description: "Extract video transcripts: yt-dlp subtitles to clean paragraphs."
user_invocable: false  # default -- router-dispatched, not user-typed
agent: python-general-engineer
allowed-tools:
  - Bash
  - Read
routing:
  triggers:
    - "video transcript"
    - "youtube transcript"
    - "extract transcript"
    - "download subtitles"
    - "what does this video say"
  category: research
  pairs_with:
    - research-pipeline
    - wrestlejoy-external-research
---

# Video Transcript

Pull a video's transcript as readable paragraphs. Two paths, in order:

**Path 1 — uploader subtitles** (accurate, prefer when present):

```bash
yt-dlp --skip-download --write-subs --sub-langs en --sub-format vtt \
  -o '<work-dir>/%(id)s' '<URL>'
```

**Path 2 — auto-generated captions** (fallback when path 1 writes no file):

```bash
yt-dlp --skip-download --write-auto-subs --sub-langs en --sub-format vtt \
  -o '<work-dir>/%(id)s' '<URL>'
```

Then clean the VTT into paragraphs:

```bash
python3 skills/research/video-transcript/scripts/vtt_to_paragraph.py <work-dir>/<id>.en.vtt
```

Default output is plain paragraph text with `[Music]`-style cues stripped and the rolling duplicates of auto-captions deduplicated. Use `--timestamps` for `[mm:ss]` markers, `--keep-brackets` to keep cue tags, `-o FILE` to write to a file.

For other languages, change `--sub-langs` (e.g. `de`, `en.*`). List what a video offers with `yt-dlp --list-subs '<URL>'`.

## Error handling

### Both paths write no .vtt file
Cause: video has no subtitles or captions in the requested language.
Solution: run `yt-dlp --list-subs '<URL>'` and pick an available language; if none exist, report that and offer audio transcription via the `markdown-converter` skill on a downloaded audio file.

### HTTP 429 / "Sign in to confirm"
Cause: platform rate-limiting the host.
Solution: wait and retry with `--sleep-requests 2`; keep request volume low.

### Cleaner output repeats lines
Cause: VTT came from a third path (e.g. translated captions) with cue formats the dedupe misses.
Solution: rerun the cleaner; if repeats remain, file the sample VTT alongside a fix to `vtt_to_paragraph.py`.
