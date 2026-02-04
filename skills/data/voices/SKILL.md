---
name: voices
description: List, apply, or delete saved voice profiles. Use when user wants to see available voices or apply a saved voice to writing.
model: haiku
allowed-tools: Read
---

# Voice Library

Manage saved voice profiles for consistent writing style.

## Commands

| Command | Action |
|---------|--------|
| `/wordsmith:voices` | List all saved voice profiles |
| `/wordsmith:voices [name]` | Show details for specific voice |
| `/wordsmith:voices delete [name]` | Remove a voice profile |

## Voice Storage

Voices are stored in `~/.claude/voices/` as JSON files:

```
~/.claude/voices/
├── hemingway.json
├── technical-docs.json
└── brand-voice.json
```

## Voice Profile Schema

```json
{
  "name": "profile-name",
  "description": "Brief description of when to use",
  "extractedFrom": "Source material used for extraction",
  "characteristics": {
    "sentenceLength": "short/medium/long/varied",
    "vocabulary": "simple/technical/elevated/mixed",
    "tone": "formal/casual/authoritative/warm",
    "structure": "linear/nested/fragmented"
  },
  "patterns": [
    "Pattern 1 observed in source",
    "Pattern 2 observed in source"
  ],
  "avoids": [
    "Things this voice never does"
  ],
  "exampleTransform": {
    "before": "Generic sentence",
    "after": "Same idea in this voice"
  }
}
```

## Workflow

### List All Voices

1. Read all files in `~/.claude/voices/`
2. Display as table: Name | Description | Source

### Apply Voice

Use with `/wordsmith:writing` by specifying voice name:
- "edit this using hemingway voice"
- "write in brand-voice style"

### Create New Voice

Use `/wordsmith:writing` with sample text:
- "extract voice from this writing sample"

The writing skill handles extraction and saves to `~/.claude/voices/`.
