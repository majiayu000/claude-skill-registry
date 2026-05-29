---
name: speak-tts
description: Local text-to-speech generation using Chatterbox TTS on Apple Silicon. Use this when users request converting text to audio, reading articles/documents aloud, generating speech from clipboard content, voice cloning, or creating audiobook-style narration. Runs entirely on-device via MLX for private TTS. Supports auto-chunking for long documents, batch processing, and resume capability.
---

# speak - Text to Speech for Agents

Convert text to natural speech audio using Chatterbox TTS on Apple Silicon.

## Prerequisites

| Requirement | Check | Install |
|-------------|-------|---------|
| Apple Silicon Mac | `uname -m` → arm64 | Intel not supported |
| macOS 12.0+ | `sw_vers` | - |
| sox | `which sox` | `brew install sox` |
| ffmpeg | `which ffmpeg` | `brew install ffmpeg` |
| poppler (PDF) | `which pdftotext` | `brew install poppler` |

## Input Sources

| Source | Example |
|--------|---------|
| Text file | `speak article.txt` |
| Markdown | `speak doc.md` |
| Direct string | `speak "Hello"` |
| Clipboard | `pbpaste \| speak` |
| Stdin | `cat file.txt \| speak` |

### Web Articles
```bash
lynx -dump -nolist "https://example.com/article" | speak --output article.wav
```

### Converting Formats

| Format | Convert Command |
|--------|-----------------|
| PDF | `pdftotext doc.pdf doc.txt` |
| DOCX | `textutil -convert txt doc.docx` |
| HTML | `pandoc -f html -t plain doc.html > doc.txt` |

## Output Modes

| Goal | Command |
|------|---------|
| Save for later | `speak text.txt --output file.wav` |
| Listen now (streaming) | `speak text.txt --stream` |
| Listen now (complete) | `speak text.txt --play` |
| Both | `speak text.txt --stream --output file.wav` |

### Default Behavior
```bash
speak article.txt          # → ~/Audio/speak/article.wav (no playback)
speak "Hello"              # → ~/Audio/speak/speak_<timestamp>.wav
```

## Directory Auto-Creation

| Directory | Auto-Created? |
|-----------|---------------|
| `~/Audio/speak/` | ✓ Yes |
| `~/.chatter/voices/` | ✗ No |
| Custom directories | ✗ No |

**Always create custom directories first:**
```bash
mkdir -p ~/.chatter/voices/
mkdir -p ~/Audio/custom/
```

## Voice Cloning

Voice cloning generates speech that matches your vocal characteristics (pitch, tone, cadence) from a short recording.

### Quality Expectations
- Output captures general voice characteristics but is **not a perfect replica**
- Quality depends heavily on sample quality
- 15-25 seconds is optimal (10s minimum, 30s maximum)

### Recording Your Voice

**Using QuickTime:**
1. Open QuickTime Player → File → New Audio Recording
2. Record 20 seconds of clear speech
3. File → Export As → Audio Only (.m4a)
4. Convert to WAV (see below)

**Using sox (command line):**
```bash
# -d = use default microphone
# Recording starts immediately and stops after 25 seconds
sox -d -r 24000 -c 1 ~/.chatter/voices/my_voice.wav trim 0 25
```

### Converting to Required Format

Voice samples **MUST** be: WAV, 24000 Hz, mono, 10-30 seconds.

```bash
# From MP3
ffmpeg -i voice.mp3 -ar 24000 -ac 1 voice.wav

# From M4A (QuickTime)
ffmpeg -i voice.m4a -ar 24000 -ac 1 voice.wav

# Trim to 25 seconds
ffmpeg -i long.wav -t 25 -ar 24000 -ac 1 trimmed.wav

# Check sample properties
ffprobe -i voice.wav 2>&1 | grep -E "Duration|Stream"
# Should show: Duration ~15-25s, 24000 Hz, mono
```

### Using Your Voice

```bash
# Create directory
mkdir -p ~/.chatter/voices/

# Move sample
mv voice.wav ~/.chatter/voices/my_voice.wav

# Test
speak "Testing my voice" --voice ~/.chatter/voices/my_voice.wav --stream

# Use for content
speak notes.txt --voice ~/.chatter/voices/my_voice.wav --output presentation.wav
```

**Path requirements:**
- ✓ Works: `~/.chatter/voices/my_voice.wav` (tilde expanded by shell)
- ✓ Works: `/Users/name/.chatter/voices/my_voice.wav`
- ✗ Fails: `my_voice.wav` (relative path)
- ✗ Fails: `./voices/my_voice.wav` (relative path)

### Voice Sample Tips

| Good Sample | Bad Sample |
|-------------|------------|
| Quiet room | Background noise |
| Natural pace | Rushed or monotone |
| Clear diction | Mumbling |
| Varied content | Repetitive phrases |

## Default Voice

When `--voice` is omitted, a built-in default voice is used:
```bash
speak "Hello world" --stream  # Uses default voice
```

## Emotion Tags

Tags produce **audible effects** (actual sounds), not spoken words:

```bash
speak "[sigh] Monday again." --stream
# Output: (sigh sound) "Monday again."
```

| Tag | Effect |
|-----|--------|
| `[laugh]` | Laughter |
| `[chuckle]` | Light chuckle |
| `[sigh]` | Sighing |
| `[gasp]` | Gasping |
| `[groan]` | Groaning |
| `[clear throat]` | Throat clearing |
| `[cough]` | Coughing |
| `[crying]` | Crying |
| `[singing]` | Sung speech |

**NOT supported:** `[pause]`, `[whisper]` (ignored)

**For pauses:** Use punctuation: `"Wait... let me think."`

## Batch Processing

```bash
mkdir -p ~/Audio/book/
speak ch01.txt ch02.txt ch03.txt --output-dir ~/Audio/book/
# Creates: ch01.wav, ch02.wav, ch03.wav

# With auto-chunking (for long files)
speak chapters/*.txt --output-dir ~/Audio/book/ --auto-chunk

# Skip completed files
speak chapters/*.txt --output-dir ~/Audio/book/ --skip-existing
```

### Auto-Chunk Behavior

When using `--auto-chunk` with batch processing:
1. Each input file is chunked **independently**
2. Chunks are generated and **automatically concatenated** per file
3. Final output: one `.wav` per input file (e.g., `ch01.wav`)
4. Intermediate chunks deleted (unless `--keep-chunks`)

**You don't need to manually concatenate chunks** — only concatenate final chapter files.

## Concatenating Audio

```bash
# Explicit order (recommended)
speak concat ch01.wav ch02.wav ch03.wav --output book.wav

# Glob pattern (REQUIRES zero-padded filenames)
speak concat audiobook/*.wav --output book.wav
```

### Zero-Padding Rules

**Critical for correct concatenation order:**

| Files | Correct | Wrong |
|-------|---------|-------|
| 1-9 | `01`, `02`, ..., `09` | `1`, `2`, ..., `9` |
| 10-99 | `01`, `02`, ..., `99` | `1`, `10`, `2`, ... |
| 100+ | `001`, `002`, ..., `999` | `1`, `100`, `2`, ... |

**Why:** Shell glob expansion sorts alphabetically. `1, 10, 2` vs `01, 02, 10`.

## PDF to Audiobook (Complete Workflow)

### Step 1: Find Chapter Boundaries
```bash
# Preview table of contents
pdftotext -f 1 -l 5 textbook.pdf toc.txt
cat toc.txt  # Note chapter page numbers

# Or search for "Chapter" markers
pdftotext textbook.pdf - | grep -n "Chapter"
```

### Step 2: Extract Chapters (Zero-Padded!)
```bash
# For 100-page book with ~10 chapters
pdftotext -f 1 -l 12 -layout textbook.pdf ch01.txt
pdftotext -f 13 -l 25 -layout textbook.pdf ch02.txt
pdftotext -f 26 -l 38 -layout textbook.pdf ch03.txt
# ... continue for all chapters
```

### Step 3: Estimate Time
```bash
speak --estimate ch*.txt
# Shows: total audio duration, generation time, storage needed

# Quick estimates:
# 1 page ≈ 2 min audio ≈ 1 min generation
# 100 pages ≈ 200 min audio ≈ 100 min generation ≈ 500 MB
```

### Step 4: Generate Audio
```bash
mkdir -p audiobook/
speak ch01.txt ch02.txt ch03.txt --output-dir audiobook/ --auto-chunk
# Creates: audiobook/ch01.wav, audiobook/ch02.wav, audiobook/ch03.wav
```

### Step 5: Concatenate
```bash
speak concat audiobook/ch01.wav audiobook/ch02.wav audiobook/ch03.wav --output complete_audiobook.wav
# Or with glob (only if zero-padded):
speak concat audiobook/ch*.wav --output complete_audiobook.wav
```

### PDF Troubleshooting

| Issue | Solution |
|-------|----------|
| Empty/garbled text | Scanned PDF — use OCR: `brew install tesseract` |
| Wrong encoding | Try: `pdftotext -enc UTF-8 doc.pdf` |
| Check word count | `pdftotext doc.pdf - \| wc -w` (should be >100) |

## Multi-Voice Content

```bash
mkdir -p podcast/scripts podcast/wav

echo "Welcome to the show." > podcast/scripts/01_host.txt
echo "Thanks for having me." > podcast/scripts/02_guest.txt

speak podcast/scripts/01_host.txt --voice ~/.chatter/voices/host.wav --output podcast/wav/01.wav
speak podcast/scripts/02_guest.txt --voice ~/.chatter/voices/guest.wav --output podcast/wav/02.wav

speak concat podcast/wav/01.wav podcast/wav/02.wav --output podcast.wav
```

## Options Reference

| Option | Description | Default |
|--------|-------------|---------|
| `--stream` | Stream as it generates | false |
| `--play` | Play after complete | false |
| `--output <path>` | Output file | ~/Audio/speak/ |
| `--output-dir <dir>` | Batch output directory | - |
| `--voice <path>` | Voice sample (full path) | default |
| `--timeout <sec>` | Timeout per file | 300 |
| `--auto-chunk` | Split long documents | false |
| `--chunk-size <n>` | Chars per chunk | 6000 |
| `--resume <file>` | Resume from manifest | - |
| `--keep-chunks` | Keep intermediate files | false |
| `--skip-existing` | Skip if output exists | false |
| `--estimate` | Show duration estimate | false |
| `--dry-run` | Preview only | false |
| `--quiet` | Suppress output | false |

## Commands

| Command | Description |
|---------|-------------|
| `speak setup` | Set up environment |
| `speak health` | Check system status |
| `speak models` | List TTS models |
| `speak concat` | Concatenate audio |
| `speak daemon kill` | Stop TTS server |
| `speak config` | Show configuration |

## Performance

| Metric | Value |
|--------|-------|
| Cold start | ~4-8s |
| Warm start | ~3-8s |
| Speed | 0.3-0.5x RTF (faster than real-time) |
| Storage | ~2.5 MB/min, ~150 MB/hour |

## Resume Capability

For interrupted long generations:

```bash
# Single file with auto-chunk — use --resume
speak long.txt --auto-chunk --output book.wav
# If interrupted, manifest saved at ~/Audio/speak/manifest.json
speak --resume ~/Audio/speak/manifest.json

# Batch processing — use --skip-existing
speak ch*.txt --output-dir audiobook/ --auto-chunk
# If interrupted, re-run same command:
speak ch*.txt --output-dir audiobook/ --auto-chunk --skip-existing
```

## Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| "Voice file not found" | Relative path | Use full path: `~/.chatter/voices/x.wav` |
| "Invalid WAV format" | Wrong specs | Convert: `ffmpeg -i in.wav -ar 24000 -ac 1 out.wav` |
| "Voice sample too short" | <10 seconds | Record 15-25 seconds |
| "Output directory doesn't exist" | Not created | `mkdir -p dirname/` |
| "sox not found" | Not installed | `brew install sox` |
| Scrambled concat order | Non-zero-padded | Use `01`, `02`, not `1`, `2` |
| Timeout | >5 min generation | Use `--auto-chunk` or `--timeout 600` |
| "Server not running" | Stale daemon | `speak daemon kill && speak health` |

## Setup

```bash
speak "test"     # Auto-setup on first run (downloads model ~500MB)
speak setup      # Or manual setup
speak health     # Verify everything works
```

## Server Management

Server auto-starts and shuts down after 1 hour idle.

```bash
speak health        # Check status
speak daemon kill   # Stop manually
```
