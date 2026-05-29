---
name: tts-skill
description: Multi-engine text-to-speech skill. Supports Qwen3-TTS local voice cloning, VoiceCraft online TTS, and OpenAI TTS.
---

# 🎙️ TTS-Skill — Multi-Engine Text-to-Speech

TTS-Skill provides a single entrypoint for generating speech using multiple backends, with consistent output naming and progress feedback for long-running jobs.

## Engines

- **qwen3-tts**: local voice cloning with a reference audio + transcript
- **edge-tts**: online voices with speed/pitch/style controls
- **openai-tts**: OpenAI speech generation via API

## Command Syntax

```text
/tts-skill [engine] [text] --voice [voice-keyword] [other options]
```

If you use the Python entrypoint:

```bash
python tts-skill.py [engine] [text] --voice [voice-keyword]
```

## Text Input

Pass text as a positional argument, or use `--text-file` / `-f` to read from a file.

Example:

```bash
python tts-skill.py qwen3-tts --text-file "input\\text.txt" --voice 寒冰射手
```

Notes:

- `--text-file` supports relative and absolute paths; relative paths are resolved from your current working directory
- If both positional text and `--text-file` are provided, `--text-file` takes priority
- UTF-8 is recommended (UTF-8 BOM is supported); on decode error it falls back to GBK

You can also call engine scripts directly:

```bash
python engines/qwen3-tts-cli.py --text-file "input\\text.txt" --voice 寒冰射手
python engines/edge-tts-cli.py --text-file "input\\text.txt" --voice xiaoxiao
python engines/openai-tts-cli.py --text-file "input\\text.txt" --voice alloy
```

## Local Voice Assets (Qwen3-TTS)

To add a clone voice, put a matching pair of files in `assets/`:

```text
assets/Lei.wav
assets/Lei.txt
```

Supported audio formats: `.wav`, `.mp3`, `.m4a`, `.flac`.

Then:

```bash
python tts-skill.py qwen3-tts "测试文本" --voice Lei
```

## Output

If `--output` is not provided:

- Output directory: `output/`
- Filename pattern: `YYYYMMDD_HHMMSS_<first-6-chars>.<ext>`

## Progress & Timing (Qwen3-TTS)

Qwen3-TTS jobs print a live progress bar with ETA. After completion, `tts-skill.py` prints:

- total runtime
- total chars and Chinese chars
- average seconds per Chinese character (or per char if no Chinese)

## Project Layout

```text
tts-skill/
├── .trae/
│   └── plans/
├── assets/
│   ├── Lei.txt
│   ├── 寒冰射手.txt
│   ├── 布里茨.txt
│   └── 赵信.txt
├── engines/
│   ├── edge-tts-cli.py
│   ├── edge-tts.config
│   ├── openai-tts-cli.py
│   ├── openai-tts.config
│   ├── qwen3-tts-cli.py
│   └── qwen3-tts.config
├── input/
│   └── text.txt
├── output/
├── tts-skill.py
├── INSTALL.md
├── INSTALL.zh-CN.md
├── README.md
├── README.zh-CN.md
├── SKILL.md
└── SKILL.zh-CN.md
```

## Chinese Spec

See [SKILL.zh-CN.md](SKILL.zh-CN.md).

