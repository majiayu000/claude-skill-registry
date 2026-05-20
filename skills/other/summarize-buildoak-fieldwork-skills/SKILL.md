---
name: summarize
description: Content extraction skill for AI coding agents. YouTube transcripts, podcasts, PDFs, images (OCR), audio/video via the summarize CLI.
---

# Summarize

Extract clean text and media transcripts from URLs, files, and streams so your AI workflow can reason over reliable source content without hand-coding brittle scraper logic.

Use this skill when you need deterministic extraction for YouTube, podcast feeds, PDFs, scanned images, or local media files.

Terminology used in this file:
- **DOM:** Document Object Model, the page element structure used by browser-based extractors.
- **OCR:** Optical character recognition (extracting text from images/scans).
- **ANSI codes:** Terminal color/control sequences; `--plain` removes them for machine parsing.

## Setup

```bash
brew tap steipete/tap
brew install summarize
```

- **Claude Code:** copy this skill folder into `.claude/skills/summarize/`
- **Codex CLI:** append this SKILL.md content to your project's root `AGENTS.md`

For the full installation walkthrough (prerequisites, optional dependencies, verification, troubleshooting), see [references/installation-guide.md](references/installation-guide.md).

## Staying Updated

This skill ships with an `UPDATES.md` changelog and `UPDATE-GUIDE.md` for your AI agent.

After installing, tell your agent: "Check `UPDATES.md` in the summarize skill for any new features or changes."

When updating, tell your agent: "Read `UPDATE-GUIDE.md` and apply the latest changes from `UPDATES.md`."

Follow `UPDATE-GUIDE.md` so customized local files are diffed before any overwrite.

---

## Quick Start

Run one extraction flow end-to-end:

```bash
summarize --version
summarize --extract "https://www.youtube.com/watch?v=VIDEO_ID" --plain
summarize --extract "/path/to/document.pdf" --plain
```

Use `--extract --plain` as the default pattern for deterministic, non-ANSI output.

## Decision Tree: summarize vs Other Tools

```text
Need content from the web?
  |
  +-- Static web page (article, docs, blog)?
  |     --> WebFetch (built-in, zero deps, faster)
  |     --> Jina r.jina.ai (zero install alternative)
  |     --> summarize ONLY if above tools fail or return garbage
  |
  +-- JS-heavy SPA / dynamic content?
  |     --> Crawl4AI crwl (full browser rendering)
  |     --> summarize will NOT help here (no JS rendering)
  |
  +-- Anti-bot / paywalled / Cloudflare-protected?
  |     --> summarize --firecrawl always (requires FIRECRAWL_API_KEY)
  |     --> browser-based workflow as fallback
  |
  +-- YouTube video?
  |     --> summarize --extract (ONLY option for transcript)
  |     --> Add --youtube web for captions-only (faster)
  |     --> Add --slides for visual slide extraction
  |
  +-- Podcast / RSS feed?
  |     --> summarize --extract (ONLY option)
  |     --> Supports Apple Podcasts, Spotify, RSS feeds, Podbean, etc.
  |
  +-- PDF (URL or local file)?
  |     --> summarize --extract (ONLY CLI option)
  |     --> Requires: uvx/markitdown (brew install uv)
  |
  +-- Image (OCR)?
  |     --> summarize --extract (ONLY CLI option)
  |     --> Requires: tesseract
  |
  +-- Audio / video file?
        --> summarize --extract (ONLY CLI option)
        --> Requires: whisper-cli (local) or OPENAI_API_KEY (cloud)
```

**Rule of thumb:** summarize is the default for media extraction (YouTube, podcasts, audio, video, images). For web pages, prefer WebFetch/Jina/Crawl4AI depending on DOM complexity (how hard the page structure is to parse). Use summarize for web only when other tools fail.

## Extraction Mode (Primary)

`--extract` prints raw extracted content and exits. No LLM involved.
Use this first. You can handle any downstream synthesis in your own workflow.

```bash
# Web page extraction (plain text, default)
summarize --extract "https://example.com" --plain

# Web page extraction (markdown format)
summarize --extract "https://example.com" --format md --plain

# YouTube transcript
summarize --extract "https://www.youtube.com/watch?v=VIDEO_ID" --plain

# YouTube transcript with timestamps
summarize --extract "https://www.youtube.com/watch?v=VIDEO_ID" --timestamps --plain

# YouTube transcript formatted as markdown (requires LLM -- uses API key)
summarize --extract "https://www.youtube.com/watch?v=VIDEO_ID" --format md --markdown-mode llm --plain

# YouTube slides + transcript
summarize --extract "https://www.youtube.com/watch?v=VIDEO_ID" --slides --plain

# Podcast (RSS feed)
summarize --extract "https://feeds.example.com/podcast.xml" --plain

# Apple Podcasts episode
summarize --extract "https://podcasts.apple.com/us/podcast/EPISODE_ID" --plain

# PDF from URL
summarize --extract "https://example.com/document.pdf" --plain

# PDF from local file
summarize --extract "/path/to/document.pdf" --plain

# Image OCR
summarize --extract "/path/to/image.png" --plain

# Audio transcription
summarize --extract "/path/to/audio.mp3" --plain

# Video transcription
summarize --extract "/path/to/video.mp4" --plain

# Stdin (pipe content)
pbpaste | summarize --extract - --plain
cat document.pdf | summarize --extract - --plain
```

**Always use `--plain`** when extracting for agent consumption. It suppresses ANSI/OSC rendering.

**Extraction defaults:**
- URLs default to `--format md` in extract mode
- Files default to `--format text`
- PDF requires uvx/markitdown (`--preprocess auto`, which is default)

## LLM Summarization Mode (Secondary)

Use this mode only when you explicitly want summarize to perform synthesis itself.

```bash
# Summarize a URL (requires API key for the chosen model)
summarize "https://example.com" --model anthropic/claude-sonnet-4-5 --length long

# Summarize with a custom prompt
summarize "https://example.com" --prompt "Extract key technical decisions and their rationale"

# Summarize YouTube video
summarize "https://www.youtube.com/watch?v=VIDEO_ID" --length xl

# JSON output with metrics
summarize "https://example.com" --json --model openai/gpt-5-mini
```

**API keys for LLM mode** (set in `~/.summarize/config.json` or env vars):
- `ANTHROPIC_API_KEY` -- for anthropic/ models
- `OPENAI_API_KEY` -- for openai/ models
- `GEMINI_API_KEY` -- for google/ models
- `XAI_API_KEY` -- for xai/ models

## Dependency Matrix

| Feature | Required Deps |
|---------|--------------|
| Web page extraction | None |
| YouTube transcript (captions) | None (web mode) |
| YouTube transcript (no captions) | yt-dlp + whisper or API key |
| YouTube slides | yt-dlp + ffmpeg |
| Podcast transcription | yt-dlp + whisper or API key |
| PDF extraction | uvx/markitdown |
| Image OCR | tesseract |
| Audio/video transcription | whisper-cli (local) or OPENAI_API_KEY |
| Anti-bot sites (Firecrawl) | FIRECRAWL_API_KEY |
| Slide OCR | tesseract |

**What is not installed (by design):**
- `whisper-cli` / whisper.cpp -- heavy binary, install when audio transcription is needed
- Firecrawl API key -- paid service, configure when anti-bot extraction is needed
- LLM API keys in summarize config -- only add if you use LLM Summarization Mode

## Key Flags Quick Reference

| Flag | Purpose | Example |
|------|---------|---------|
| `--extract` | Raw content extraction, no LLM | `summarize --extract URL` |
| `--plain` | No ANSI rendering (agent-safe output) | Always use for agents |
| `--format md\|text` | Output format (md default for URLs in extract) | `--format md` |
| `--youtube auto\|web\|yt-dlp` | YouTube transcript source | `--youtube web` (captions only) |
| `--slides` | Extract video slides with ffmpeg | `--slides --slides-ocr` |
| `--timestamps` | Include timestamps in transcripts | `--timestamps` |
| `--firecrawl off\|auto\|always` | Firecrawl for anti-bot sites | `--firecrawl always` |
| `--preprocess off\|auto\|always` | Preprocessing (markitdown for PDFs) | Default `auto` |
| `--markdown-mode` | HTML-to-MD conversion mode | `--markdown-mode readability` |
| `--timeout` | Fetch/LLM timeout | `--timeout 2m` |
| `--verbose` | Debug output to stderr | Troubleshooting |
| `--json` | Structured JSON output with metrics | `--json` |
| `--length` | Summary length (LLM mode only) | `--length xl` |
| `--model` | LLM model (LLM mode only) | `--model anthropic/claude-sonnet-4-5` |
| `--max-extract-characters` | Limit extract output length | `--max-extract-characters 50000` |
| `--language\|--lang` | Output language | `--lang en` |
| `--video-mode` | Video handling mode | `--video-mode transcript` |
| `--transcriber` | Audio backend | `--transcriber whisper` |

## Verified Services (YouTube/Podcasts)

**YouTube:** All public videos with captions. Falls back to yt-dlp audio download + transcription for videos without captions.

**Podcasts (verified):**
- Apple Podcasts
- Spotify (best-effort; may fail for exclusives)
- Amazon Music / Audible podcast pages
- Podbean
- Podchaser
- RSS feeds (Podcasting 2.0 transcripts when available)
- Embedded YouTube podcast pages

## Common Patterns

### 1. YouTube Transcript for Analysis

```bash
# Quick: captions only (fastest, no deps beyond summarize)
summarize --extract "https://www.youtube.com/watch?v=VIDEO_ID" --youtube web --plain

# Full: with timestamps
summarize --extract "https://www.youtube.com/watch?v=VIDEO_ID" --timestamps --plain

# Formatted as clean markdown (requires LLM API key)
summarize --extract "https://www.youtube.com/watch?v=VIDEO_ID" --format md --markdown-mode llm --plain
```

### 2. Podcast Episode Transcript

```bash
# From RSS feed (transcribes latest episode)
summarize --extract "https://feeds.example.com/podcast.xml" --plain

# From Apple Podcasts link
summarize --extract "https://podcasts.apple.com/us/podcast/SHOW/EPISODE" --plain
```

### 3. PDF Content Extraction

```bash
# From URL
summarize --extract "https://example.com/report.pdf" --plain

# From local file
summarize --extract "/path/to/file.pdf" --plain

# Limit output length
summarize --extract "/path/to/huge.pdf" --max-extract-characters 50000 --plain
```

### 4. Image OCR

```bash
summarize --extract "/path/to/screenshot.png" --plain
summarize --extract "/path/to/scanned-doc.jpg" --plain
```

### 5. Anti-Bot Website (Firecrawl Fallback)

```bash
# Requires FIRECRAWL_API_KEY in env or config
summarize --extract "https://paywalled-site.com/article" --firecrawl always --plain
```

### 6. Batch Extraction (Shell Loop)

```bash
# Extract multiple YouTube videos
for url in "URL1" "URL2" "URL3"; do
  echo "=== $url ==="
  summarize --extract "$url" --plain
done
```

## Error Handling

| Symptom | Cause | Fix |
|---------|-------|-----|
| `Missing uvx/markitdown` | PDF preprocessing not available | `brew install uv` |
| `does not support extracting binary files` | Preprocessing disabled for PDF | Use `--preprocess auto` (default) with uvx installed |
| YouTube returns empty transcript | No captions available, no yt-dlp/whisper | Install yt-dlp; for whisper fallback, install whisper-cli or set OPENAI_API_KEY |
| `FIRECRAWL_API_KEY not set` | Anti-bot mode requires Firecrawl | Set key in env or `~/.summarize/config.json` |
| Timeout on large content | Default 2m timeout too short | Use `--timeout 5m` |
| Audio transcription fails | No whisper backend available | Install whisper-cli locally or set OPENAI_API_KEY/FAL_KEY |
| Podcast extraction fails | Audio download failed | Check yt-dlp is installed and updated: `brew upgrade yt-dlp` |
| Garbled web extraction | JS-rendered content | summarize has no JS engine; use Crawl4AI instead |

## Configuration

Config file: `~/.summarize/config.json`

```json
{
  "model": "auto",
  "env": {
    "FIRECRAWL_API_KEY": "fc-..."
  },
  "ui": {
    "theme": "mono"
  }
}
```

Configure only what your workflow needs. If you use LLM Summarization Mode, add the required API keys.

## Anti-Patterns

| Do NOT | Do Instead |
|--------|------------|
| Use summarize for static web pages | WebFetch or Jina (faster, zero deps) |
| Use summarize for JS-heavy SPAs | Crawl4AI crwl (has browser rendering) |
| Use summarize's LLM mode as default | Use `--extract` and run synthesis in your own workflow unless explicitly required |
| Skip `--plain` for any non-interactive run | Always use `--plain` to avoid ANSI escape codes |
| Install whisper.cpp preemptively | Install only when audio transcription use case arises |
| Forget `--timeout` for large media | Podcasts/videos can take minutes; set `--timeout 5m` |
| Use summarize when WebFetch works | summarize is heavier; reserve for media and fallback |
| Use summarize for local repo/codebase search | Use your local knowledge search tools |

## Bundled Resources Index

| Path | What | When to Load |
|------|------|-------------|
| `./UPDATES.md` | Structured changelog for AI agents | When checking for new features or updates |
| `./UPDATE-GUIDE.md` | Instructions for AI agents performing updates | When updating this skill |
| `./references/installation-guide.md` | Detailed install walkthrough for Claude Code and Codex CLI | First-time setup or environment repair |
| `./references/commands.md` | Full CLI flag reference with all options | When you need exact flag syntax or env var names |
