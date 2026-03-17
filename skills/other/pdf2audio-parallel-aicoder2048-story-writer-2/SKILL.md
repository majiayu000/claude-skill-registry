---
name: pdf2audio-parallel
description: "Parallel PDF to MP3 conversion using MiniMax. Convert multiple PDF chapters to audio simultaneously using parallel subagents. Use when: (1) User says 'generate mp3 for the story of [STORY_NAME]', (2) User says '为故事[STORY_NAME]生成mp3', (3) User says '为故事[STORY_NAME]第[X]章生成mp3', (4) User says 'generate mp3 for story of [STORY_NAME], chapter [X]', (5) Converting a range of PDFs like 'story-[01-05].pdf' to MP3, (6) Batch audiobook creation from PDF chapters."
---

# Parallel PDF to Audio Converter

Convert multiple PDF chapters to MP3 audio in parallel by delegating to `/pdf2audio-minimax`.

## Trigger Phrases

This skill triggers on natural language requests:

| User Says | Action |
|-----------|--------|
| "generate mp3 for the story of 我的故事" | Convert all chapters |
| "为故事我的故事生成mp3" | Convert all chapters |
| "为故事我的故事第[01, 03-04]章生成mp3" | Convert specified chapters |
| "generate mp3 for story of 我的故事, chapter [01-05]" | Convert specified chapters |

## Input Format

**Direct command:**
```
/pdf2audio-parallel "<story_dir>/chapters/<story_name>-[chapter_pattern].pdf" [voice_id]
```

**Examples:**
- `/pdf2audio-parallel "重写时间的源代码/chapters/重写时间的源代码-[01-05].pdf"`
- `/pdf2audio-parallel "我的故事/chapters/我的故事-[01, 03-04].pdf" "Chinese (Mandarin)_Gentleman"`

## Workflow

### 1. Parse Input Parameters

**From natural language:** Extract story name, then discover chapters:
```bash
# Find story directory
ls -d <STORY_NAME>/

# List available PDF chapters
ls <STORY_NAME>/chapters/<STORY_NAME>-*.pdf
```

**From direct command:** Extract from path pattern:
- `story_dir`: Story directory name (e.g., `重写时间的源代码`)
- `story_name`: Story name from filename pattern (usually same as directory)
- `chapter_pattern`: Chapter numbers (e.g., `01-05` or `[01, 03-04]`)
- `voice_id`: Voice ID for TTS (optional, passed to pdf2audio-minimax)

### 2. Generate Chapter List

Parse the chapter pattern and expand into individual files.

**Supported Patterns:**

| Pattern | Expands To |
|---------|------------|
| `[01-05]` | 01, 02, 03, 04, 05 |
| `[03]` | 03 |
| `[01, 03-04]` | 01, 03, 04 |
| `[01-02, 05-07]` | 01, 02, 05, 06, 07 |
| `[01, 03, 05]` | 01, 03, 05 |

**Example:** `我的故事/chapters/我的故事-[01, 03-04].pdf` expands to:
- `我的故事/chapters/我的故事-01.pdf`
- `我的故事/chapters/我的故事-03.pdf`
- `我的故事/chapters/我的故事-04.pdf`

### 3. Launch Parallel Agents

Use Task tool to spawn N agents simultaneously, each calling `/pdf2audio-minimax` for one PDF.

**Agent Prompt Template:**

```
Convert this PDF to MP3 using the pdf2audio-minimax skill:

/pdf2audio-minimax <story_dir>/chapters/<story_name>-XX.pdf [voice_id]

Example:
/pdf2audio-minimax 我的故事/chapters/我的故事-01.pdf Chinese (Mandarin)_Gentleman
```

**IMPORTANT:**
- Each agent delegates to `/pdf2audio-minimax` which handles:
  - Reading PDF content
  - Extracting chapter title from content
  - Voice selection (auto or specified)
  - Audio conversion via MiniMax
  - File naming: `<故事名>_<章节号>_<章节标题>.mp3`
- This skill only handles parallel orchestration

### 4. Collect Results

Gather outputs from all agents and report:
- Successfully converted files with final paths
- Any errors encountered

## Quick Examples

### Example 1: Simple Range

**User Input:**
```
/pdf2audio-parallel "我的故事/chapters/我的故事-[01-03].pdf"
```

**Parallel Agent Tasks:**
1. Agent 1: `/pdf2audio-minimax 我的故事/chapters/我的故事-01.pdf` → `我的故事_01_<标题>.mp3`
2. Agent 2: `/pdf2audio-minimax 我的故事/chapters/我的故事-02.pdf` → `我的故事_02_<标题>.mp3`
3. Agent 3: `/pdf2audio-minimax 我的故事/chapters/我的故事-03.pdf` → `我的故事_03_<标题>.mp3`

### Example 2: With Voice ID

**User Input:**
```
/pdf2audio-parallel "星际迷航/chapters/星际迷航-[01, 03-04].pdf" "Chinese (Mandarin)_Gentleman"
```

**Parallel Agent Tasks:**
1. Agent 1: `/pdf2audio-minimax 星际迷航/chapters/星际迷航-01.pdf Chinese (Mandarin)_Gentleman`
2. Agent 2: `/pdf2audio-minimax 星际迷航/chapters/星际迷航-03.pdf Chinese (Mandarin)_Gentleman`
3. Agent 3: `/pdf2audio-minimax 星际迷航/chapters/星际迷航-04.pdf Chinese (Mandarin)_Gentleman`

## Notes

- Voice selection and file naming are handled by `pdf2audio-minimax`
- See `pdf2audio-minimax` skill for voice options and naming convention
- Output files are saved to `<story_dir>/audiobook/` directory
