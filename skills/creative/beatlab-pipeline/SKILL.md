---
name: beatlab-pipeline
description: Deterministic BeatLab pipeline utilities (validate, render grid, export MIDI/WAV). Use for running scripts instead of reasoning about validation/rendering.
user-invocable: false
allowed-tools: Read, Write, Bash(uv:*), Bash(mkdir:*), Bash(which:*), Bash(ffmpeg:*)
---

# BeatLab Pipeline

Prefer running these scripts (do NOT read them into context):

## Validate (and normalize) a beat JSON
uv run python .claude/skills/beatlab-pipeline/scripts/validate.py <beat.json> --inplace

## Render 16-step ASCII grid
uv run python .claude/skills/beatlab-pipeline/scripts/render_grid.py <beat.json>

## Export MIDI
uv run python .claude/skills/beatlab-pipeline/scripts/export_midi.py <beat.json> <out.mid>

## Render WAV
uv run python .claude/skills/beatlab-pipeline/scripts/render_wav.py <beat.json> <out.wav>

## Optional MP3 (if ffmpeg exists)
ffmpeg -y -i <out.wav> <out.mp3>
