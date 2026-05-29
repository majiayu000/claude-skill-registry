---
name: gemini-caption-parse
description: Parse and write Gemini/YouTube markdown transcript format with timestamps
---

# Gemini Format Parser Skill

Use this skill to parse and write Gemini-style markdown transcripts.

## Installation

```bash
# Using uv (recommended)
uv pip install gemini-caption-skills

# Or using pip
pip install gemini-caption-skills
```

## Reading Transcripts

### Parse All Segments

```python
from gemini_caption import GeminiReader

# From file
segments = GeminiReader.read("transcript.md", include_events=True, include_sections=True)

# From string content
segments = GeminiReader.read(markdown_content, include_events=True)

for seg in segments:
    print(f"[{seg.start:.1f}s] {seg.speaker}: {seg.text}")
```

### Extract Dialogue Only

```python
from gemini_caption import GeminiReader

# Returns list of dicts with: text, start, end, speaker, section
dialogue = GeminiReader.extract_dialogue("transcript.md")

for seg in dialogue:
    print(f"{seg['start']:.2f} - {seg['end']:.2f}: {seg['text']}")
```

## GeminiSegment Fields

Each segment has these fields:
- `text`: The spoken/event text
- `timestamp`: Start time in seconds (or None)
- `end_timestamp`: End time in seconds (or None)
- `speaker`: Speaker name (e.g., "Mira Murati:")
- `section`: Current section title
- `segment_type`: "dialogue", "event", or "section_header"
- `line_number`: Source line number

## Writing Transcripts

### Write to File

```python
from gemini_caption import GeminiWriter

segments = [
    {"text": "Welcome everyone.", "start": 0, "end": 2, "speaker": "Host"},
    {"text": "Thank you for having me.", "start": 2, "end": 5, "speaker": "Guest"},
]

GeminiWriter.write_transcript(
    segments,
    "output.md",
    title="My Podcast Episode",
    include_toc=True,
)
```

### Convert to Markdown String

```python
from gemini_caption import GeminiWriter

md = GeminiWriter.to_markdown(segments, title="Episode 1")
print(md)
```

## Supported Formats

### Standard Gemini Format
```markdown
## [00:00:00] Introduction

**Host:** Welcome back to the show. [00:00:01]

**Guest:** Thank you for having me. [00:00:05]

[Applause] [00:00:08]
```

### YouTube Link Format
```markdown
## [[00:12](http://www.youtube.com/watch?v=xxx&t=12)] Introduction

**Speaker:** Hello everyone [[00:21](http://www.youtube.com/watch?v=xxx&t=21)]
```

## Timestamp Utilities

```python
from gemini_caption import GeminiReader, GeminiWriter

# Parse timestamp to seconds
seconds = GeminiReader.parse_timestamp("01", "30", "45")  # 5445.0

# Format seconds to timestamp
ts = GeminiWriter.format_timestamp(5445.0)  # "[01:30:45]"
```
