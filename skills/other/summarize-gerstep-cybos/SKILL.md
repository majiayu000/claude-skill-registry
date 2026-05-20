---
name: summarize
description: Summarize various content types (therapy sessions, meetings, documents) into structured notes. Use when processing transcripts or long-form content.
---

# Summarize Skill

Transform transcripts and long-form content into structured, actionable summaries.

## Capabilities

- **Therapy Sessions**: Summarize therapy transcripts in Russian with structured insights
- **Meetings**: (future) Meeting transcript summaries
- **Documents**: (future) Long document summarization

## Workflows

- `workflows/therapy.md`: **PRIMARY** - Therapy session transcript summarization

## Output Location

- Therapy: `~/CybosVault/private/context/my-life/therapy/YYYY-MM-DD-summary.md`

## Usage

```
/cyber-summarize therapy @path/to/transcript.md
/cyber-summarize therapy @path/to/transcript.txt
```
