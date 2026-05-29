---
name: regenerate-example
description: Use when asked to regenerate audio examples with shorthand like "L15 > P1 > E2" or "lesson 15 pattern 1 example 2" - runs regenerate_example.py with correct parameters
---

# Regenerate Audio Example

Regenerate a single demo audio example for EnglishConnect lessons.

## Syntax Parsing

Parse user requests into lesson, pattern, and example:

| User says | Lesson | Pattern | Example |
|-----------|--------|---------|---------|
| `L15 > P1 > E2` | 15 | 1 | 2 |
| `lesson 15 pattern 1 example 2` | 15 | 1 | 2 |
| `regenerate the 3rd example of pattern 2 in lesson 15` | 15 | 2 | 3 |

## Prerequisites

TTS server must be running. If not, run `/start-tts` first.

## Command

```bash
cd /home/smolen/dev/EnglishConnect/src/tools/demo-generator && \
  source /home/smolen/dev/EnglishConnect/src/backend/.venv/bin/activate && \
  python regenerate_example.py --lesson LESSON --pattern PATTERN --example EXAMPLE
```

Replace `LESSON`, `PATTERN`, `EXAMPLE` with parsed values.

## Output

Files are saved to `content/audio/ec1/demos/lesson-{NN}/` with deterministic names:

- `lesson{NN}-pattern{N}-ex{N}.wav` - audio file
- `lesson{NN}-pattern{N}-ex{N}.json` - metadata

Example: `lesson15-pattern1-ex3.wav`

Regenerating overwrites the existing file (no unique hashes).

## Optional: Change Voices

Add `--teacher-voice VOICE` or `--student-voice VOICE`:
- `speaker_a` - Aria (female)
- `speaker_b` - Emma (female, upbeat)
- `speaker_c` - Davis (male)
- `speaker_d` - Grace (female, default teacher)
- `speaker_e` - James (male)
- `speaker_f` - Lily (female)

## List Voices

```bash
cd /home/smolen/dev/EnglishConnect/src/tools/demo-generator && \
  source /home/smolen/dev/EnglishConnect/src/backend/.venv/bin/activate && \
  python regenerate_example.py --list-voices
```
