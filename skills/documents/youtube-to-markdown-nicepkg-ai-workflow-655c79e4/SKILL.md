---
name: youtube-to-markdown
description: Use when user asks YouTube video extraction, get, fetch, transcripts, subtitles, or captions. Writes video details and transcription into structured markdown file.
allowed-tools:
  - Bash
  - Read
  - Write
  - Task
  - AskUserQuestion
  - Skill
---

# YouTube to Markdown

Multiple videos: Process one video at a time, sequentially. Do not run parallel extractions.
Execute all steps sequentially without asking for user approval. Use TodoWrite to track progress.

## Step 0: Check extracted before

```bash
python3 ./check_existing.py "<YOUTUBE_URL>" "<output_directory>"
```

**Integrity check:**
- If `summary_valid: false`: Show issues to user, ask "Tiedosto epätäydellinen: [issues]. Prosessoidaanko uudelleen?" If yes, continue to Step 1.
- If `transcript_valid: false`: Ask user, if yes re-run Steps 2-3, 7-9.
- If `comments_valid: false`: Ask user, if yes re-run comment analysis.

If returns `exists: true` AND all valid fields are true: Read and follow UPDATE_MODE.md for update workflow.


## Step 1: Extract data (metadata, description, chapters)

```bash
python3 extract_data.py "<YOUTUBE_URL>" "<output_directory>"
```

Creates: youtube_{VIDEO_ID}_metadata.md, youtube_{VIDEO_ID}_description.md, youtube_{VIDEO_ID}_chapters.json

IMPORTANT: If you ask which language transcript to extract then do not translate that language to english and require that subagent do not translate either. Only if the user requests another language that the original then translate.

## Step 2: Extract transcript

### Primary method (if transcript available)

If video language is `en`, proceed directly. If non-English, ask user which language to download.

```bash
python3 extract_transcript.py "<YOUTUBE_URL>" "<output_directory>" "<LANG_CODE>"
```

Creates: youtube_{VIDEO_ID}_transcript.vtt

IMPORTANT: All file output must be in the same language as discovered in Step 2. If language is not English, explicitly instruct all subagents to preserve the original language.

The download may fail if a video is private, age-restricted, or geo-blocked.

### Fallback (only if transcript unavailable)

Ask user: "No transcript available. Proceed with Whisper transcription?
- Mac/Apple Silicon: Uses MLX Whisper if installed (faster, see SETUP_MLX_WHISPER.md)
- All platforms: Falls back to OpenAI Whisper (requires: brew install openai-whisper OR pip3 install openai-whisper)"

```bash
python3 extract_transcript_whisper.py "<YOUTUBE_URL>" "<output_directory>"
```

Script auto-detects MLX Whisper on Mac and uses it if available, otherwise uses OpenAI Whisper.

## Step 3: Deduplicate transcript

Set BASE_NAME from Step 1 output (youtube_{VIDEO_ID})

```bash
python3 ./deduplicate_vtt.py "<output_directory>/${BASE_NAME}_transcript.vtt" "<output_directory>/${BASE_NAME}_transcript_dedup.md" "<output_directory>/${BASE_NAME}_transcript_no_timestamps.txt"
```

## Step 4: Add natural paragraph breaks

Parallel with Step 5.

task_tool:
- subagent_type: "general-purpose"
- model: "sonnet"
- prompt:
```
INPUT: <output_directory>/${BASE_NAME}_transcript_no_timestamps.txt
CHAPTERS: <output_directory>/${BASE_NAME}_chapters.json
OUTPUT: <output_directory>/${BASE_NAME}_transcript_paragraphs.txt

Analyze INPUT and identify natural paragraph break line numbers.

Read CHAPTERS. If it contains chapters, use chapter timestamps as primary break points.

Target ~500 chars per paragraph. Find natural break points at topic shifts or sentence endings.

Write to OUTPUT in format:
15,42,78,103,...
```

```bash
python3 ./apply_paragraph_breaks.py "<output_directory>/${BASE_NAME}_transcript_dedup.md" "<output_directory>/${BASE_NAME}_transcript_paragraphs.txt" "<output_directory>/${BASE_NAME}_transcript_paragraphs.md"
```

## Step 5: Summarize transcript

Parallel with Step 4.

task_tool:
- subagent_type: "general-purpose"
- model: "sonnet"
- prompt:
```
INPUT: <output_directory>/${BASE_NAME}_transcript_no_timestamps.txt
OUTPUT: <output_directory>/${BASE_NAME}_summary.md
FORMATS: ./summary_formats.md

1. Classify content type:
   - TIPS: gear reviews, rankings, "X ways to...", practical advice lists
   - INTERVIEW: podcasts, conversations, Q&A, multiple perspectives
   - EDUCATIONAL: concept explanations, analysis, "how X works"
   - TUTORIAL: step-by-step instructions, coding, recipes

2. Analyze content structure:
   - Identify meaningful content units (topic shifts, argument structure, narrative breaks)
   - If single continuous topic, omit content unit headers
   - Skip ads, sponsors, self-promotion ("like and subscribe", merch, etc.)
   - Merge content spanning ad breaks if thematically connected

3. Read FORMATS file and use format for detected content type. Target <10% of transcript bytes.


ACTION REQUIRED: Use the Write tool NOW to save output to OUTPUT file. Do not ask for confirmation.
```

## Step 6: Review and tighten summary

task_tool:
- subagent_type: "general-purpose"
- model: "sonnet"
- prompt:
```
INPUT: <output_directory>/${BASE_NAME}_summary.md
OUTPUT: <output_directory>/${BASE_NAME}_summary_tight.md
FORMATS: ./summary_formats.md

You are an adversarial copy editor. Cut fluff, enforce quality.

Rules:
- Read FORMATS - the format has been selected based on the content type - preserve format and do not count a reason to squeeze more from budget.
- Byte budget: <10% of transcript bytes
- Hidden Gems: Remove if duplicates main content
- Tightness: Cut filler words, compress verbose explanations, prefer lists over prose

Preserve original language - do not translate.

ACTION REQUIRED: Use the Write tool NOW to save output to OUTPUT file. Do not ask for confirmation.
```

## Step 7: Clean speech artifacts

task_tool:
- subagent_type: "general-purpose"
- model: "haiku"
- prompt:
```
Read <output_directory>/${BASE_NAME}_transcript_paragraphs.md and clean speech artifacts.

Tasks:
- Remove fillers (um, uh, like, you know)
- Fix transcription errors
- Add proper punctuation
- Reduce or add implicit words to improve flow
- Preserve natural voice and tone
- Keep timestamps at end of paragraphs

ACTION REQUIRED: Use the Write tool NOW to save output to <output_directory>/${BASE_NAME}_transcript_cleaned.md. Do not ask for confirmation.
```

## Step 8: Add topic headings

task_tool:
- subagent_type: "general-purpose"
- model: "sonnet"
- prompt:
```
INPUT: <output_directory>/${BASE_NAME}_transcript_cleaned.md
OUTPUT: <output_directory>/${BASE_NAME}_transcript.md

Read the INPUT file. Add markdown headings.

Read <output_directory>/${BASE_NAME}_chapters.json:
- If contains chapters: Use chapter names as ### headings at chapter timestamps, add #### headings for subtopics
- If empty: Add ### headings where major topics change

ACTION REQUIRED: Use the Write tool NOW to save output to OUTPUT file. Do not ask for confirmation.
```

## Step 9: Create output files

```bash
python3 finalize.py "${BASE_NAME}" "<output_directory>"
```

Script uses templates to create two final files: summary file with metadata and summary, and transcript file with description and transcript. Removes intermediate work files.

Outputs:
- `youtube - {title} ({video_id}).md` - Main summary
- `youtube - {title} - transcript ({video_id}).md` - Description and transcript

Use `--debug` flag to keep intermediate work files for inspection.

## Step 10: Comment analysis

If youtube-comment-analysis skill is available, run it with the same YouTube URL and output directory.
