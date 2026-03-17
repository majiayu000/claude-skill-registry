---
name: transcribe-and-analyze
description: Transcribe audio and video from URLs (YouTube, direct media links) using WhisperKit locally. Optionally analyze transcripts with AI when explicitly requested. Use when users provide URLs to media content and request transcription or speech-to-text conversion.
---

# Transcribe and Analyze

Local transcription of audio/video content using WhisperKit. Analysis is available on request using OpenAI or local Ollama.

## Capabilities

1. **Transcription** - Convert audio/video URLs to text using WhisperKit (runs locally, always available)
2. **Analysis** - Extract insights from transcripts (only when user asks for it, supports OpenAI or Ollama)

## Quick Start

### Transcribe Only
```bash
python3 scripts/transcribe.py "https://youtube.com/watch?v=..."
```

### Transcribe + Analyze (OpenAI)
```bash
python3 scripts/transcribe.py "https://youtube.com/watch?v=..."
python3 scripts/analyze_transcript.py whisper-transcriptions/video.md
```

### Transcribe + Analyze (Local)
```bash
python3 scripts/transcribe.py "https://youtube.com/watch?v=..."
python3 scripts/analyze_transcript.py whisper-transcriptions/video.md --local
```

---

## Transcription

### Script Options

```bash
# Basic
python3 scripts/transcribe.py "URL"

# Custom output directory
python3 scripts/transcribe.py "URL" --output-dir "/path/to/save"

# Higher accuracy (slower)
python3 scripts/transcribe.py "URL" --model medium

# Without timestamps
python3 scripts/transcribe.py "URL" --no-timestamps

# Custom filename
python3 scripts/transcribe.py "URL" --filename "my-transcription.md"
```

### Whisper Models

| Model | Speed | Accuracy | Use Case |
|-------|-------|----------|----------|
| `tiny` | Fastest | Lowest | Quick drafts, testing |
| `base` | Fast | Reasonable | Simple content |
| `small` | Balanced | Good | **Default - most use cases** |
| `medium` | Slower | High | Lectures, important content |
| `large` | Slowest | Highest | Critical accuracy needed |

### Dependencies

- **yt-dlp** - `pip install yt-dlp` or `brew install yt-dlp`
- **whisperkit-cli** - https://github.com/argmaxinc/WhisperKit

Script checks for these and provides install instructions if missing.

### Output

Transcriptions save to `./whisper-transcriptions/` as markdown:

```markdown
# Transcription

**Source:** https://youtube.com/watch?v=example
**Transcribed:** 2025-01-15 14:30:00
**Tool:** WhisperKit

---

[00:00:00.000 --> 00:00:05.000] Welcome to this video...
```

---

## Analysis

### Provider Options

**OpenAI API** (default):
```bash
python3 scripts/analyze_transcript.py transcript.md
python3 scripts/analyze_transcript.py transcript.md --model gpt-4o
```
Requires `OPENAI_API_KEY` environment variable.

**Local Ollama**:
```bash
python3 scripts/analyze_transcript.py transcript.md --local
python3 scripts/analyze_transcript.py transcript.md --local --model mistral
```
Requires Ollama running (`ollama serve`).

### Script Options

```bash
# Default comprehensive analysis (OpenAI)
python3 scripts/analyze_transcript.py transcript.md

# Use local Ollama
python3 scripts/analyze_transcript.py transcript.md --local

# Specify model
python3 scripts/analyze_transcript.py transcript.md --model gpt-4o
python3 scripts/analyze_transcript.py transcript.md --local --model llama3.2

# Custom analysis prompt
python3 scripts/analyze_transcript.py transcript.md --prompt "List all tools mentioned"

# Custom output location
python3 scripts/analyze_transcript.py transcript.md --output ~/Documents/analysis.md

# Print to stdout instead of saving
python3 scripts/analyze_transcript.py transcript.md --print
```

### Default Analysis Includes

- Executive summary (2-3 paragraphs)
- Key insights (5-7 bullet points)
- Topics discussed with summaries
- Notable quotes (3-5 memorable quotes)
- Action items and recommendations
- Additional observations

### Custom Prompt Examples

```bash
--prompt "List all technologies and tools mentioned"
--prompt "What are the main arguments presented?"
--prompt "Extract all statistics and data points"
--prompt "Summarize in 5 bullet points"
--prompt "What questions were asked and how were they answered?"
```

### Dependencies

- **openai** - `pip install openai` (used for both OpenAI and Ollama)
- **OPENAI_API_KEY** environment variable (for OpenAI only)
- **Ollama** running locally (for --local mode)

### Output

Analysis saves alongside transcript as `transcript_name_analysis.md`:

```markdown
# Transcript Analysis

**Source Transcript:** path/to/transcript.md
**Analysis Model:** gpt-4o-mini (OpenAI)
**Tokens Used:** 33,763

---

[Analysis content]
```

---

## Common Workflows

### Full Pipeline: URL to Insights (Cloud)

```bash
python3 scripts/transcribe.py "https://youtube.com/watch?v=abc123"
python3 scripts/analyze_transcript.py whisper-transcriptions/watch.md
```

### Full Pipeline: URL to Insights (Local)

```bash
python3 scripts/transcribe.py "https://youtube.com/watch?v=abc123"
python3 scripts/analyze_transcript.py whisper-transcriptions/watch.md --local
```

### Multiple Analyses on Same Transcript

```bash
python3 scripts/analyze_transcript.py transcript.md --output summary.md
python3 scripts/analyze_transcript.py transcript.md --prompt "List action items" --output actions.md
python3 scripts/analyze_transcript.py transcript.md --prompt "Extract quotes" --output quotes.md
```

### Batch Transcription

```bash
python3 scripts/transcribe.py "URL1"
python3 scripts/transcribe.py "URL2"
python3 scripts/transcribe.py "URL3"
```

---

## Reference Files

### Troubleshooting (`references/troubleshooting.md`)
- Download failures
- Transcription errors
- Dependency issues
- API errors

### Configuration (`references/configuration.md`)
- Output format details
- File naming behavior
- Model selection guidance

### Usage Patterns (`references/usage-patterns.md`)
- Common transcription scenarios
- Analysis patterns
- Batch processing tips

---

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/transcribe.py` | Download and transcribe audio/video from URLs (WhisperKit) |
| `scripts/analyze_transcript.py` | AI analysis of transcript files (OpenAI or Ollama) |
