---
name: youtube-transcript
description: "YouTube transcript extraction and content reformatting: given a YouTube video URL, opens the video's transcript panel, extracts all timestamped segments, and transforms the raw transcript into summaries, chapter outlines, Twitter/X threads, blog posts, or notable quotes. Use when the user shares a YouTube URL or video link, asks to summarize a video, get a transcript, extract content from a YouTube video, get YouTube captions, extract YouTube captions, download YouTube captions, transcribe YouTube video, YouTube video to text, make a thread from YouTube, YouTube to blog post, YouTube to article, pull transcript from YouTube, YouTube content extraction, convert YouTube to text, video to transcript. Also applies when user wants to reformat any YouTube video content into structured output (chapters, threads, blog articles, key quotes)."
---

# YouTube — Transcript Extraction & Content Reformatting

> YouTube video URL → timestamped transcript → summary / chapters / thread / blog / quotes

## Language

All process output to user (progress updates, process notifications) follows the user's language.

## Objective

Extract the full transcript from a YouTube video's built-in transcript panel, then transform it into the output format the user requests.

## Prerequisites

- Target YouTube video page is already open in the browser: `https://www.youtube.com/watch?v={VIDEO_ID}`

## Pre-execution Checks

### 1. Tool Readiness

If browser-act has been confirmed available in the current session → skip this step.

Invoke `browser-act` via Skill tool to load usage. If installation or configuration issues arise, follow its guidance to resolve then retry.

## Capability Components

> This Skill's operational boundary = what the user can manually do in their browser. It only reads data already displayed to the user on the page, never bypassing authentication or access controls. JS code is encapsulated in Python files under the `scripts/` directory, invoked via `eval "$(python scripts/xxx.py)"`. Use the bash tool for execution.

### DOM: Check transcript availability and list languages

`eval "$(python scripts/get-languages.py)"`

No parameters. Reads `ytInitialPlayerResponse` from the current page.

Output example:
```json
{
  "available_languages": [
    {"code": "en", "name": "English", "kind": "manual", "is_auto": false},
    {"code": "en", "name": "English (auto-generated)", "kind": "asr", "is_auto": true}
  ],
  "count": 2
}
```

Returns `{"error": true, "message": "..."}` when transcripts are disabled or page is not a YouTube video.

### DOM: Open transcript panel

`eval "$(python scripts/open-transcript-panel.py)"`

No parameters. Clicks the "Show transcript" button below the video (handles multiple UI language variants automatically for robustness).

Must call `wait stable` after this to allow the panel to fully load.

Output example:
```json
{"success": true, "label": "内容转文字"}
```

### DOM: Extract all transcript segments

`eval "$(python scripts/extract-transcript-segments.py)"`

No parameters. Scrolls the open transcript panel to trigger lazy loading for long videos, then extracts all segments.

Output example:
```json
{
  "segment_count": 24,
  "segments": [
    {"ts": "0:18", "text": "We're no strangers to love"},
    {"ts": "0:27", "text": "You know the rules and so do I"}
  ],
  "full_text": "We're no strangers to love You know the rules...",
  "timestamped_text": "0:18 We're no strangers to love\n0:27 You know the rules..."
}
```

### Composite: Full transcript fetch workflow

1. `navigate https://www.youtube.com/watch?v={VIDEO_ID}` → `wait stable`
2. `eval "$(python scripts/get-languages.py)"` — confirm transcripts are available; note the language list
3. `eval "$(python scripts/open-transcript-panel.py)"` — open the panel
4. `wait stable` — wait for panel content to load
5. `eval "$(python scripts/extract-transcript-segments.py)"` — extract all segments

Use `timestamped_text` from the output as input for the Transform step below.

## Transform: Content Reformatting

After fetching the transcript, transform it based on what the user requests. If the user did not specify a format, default to the **Full Document** — output all five sections in order.

- **Summary**: Concise 5–10 sentence overview of the entire video
- **Chapters**: Group by topic shifts, output timestamped chapter list
- **Thread**: Twitter/X thread format — numbered posts, each under 280 characters
- **Blog post**: Full article with title, H2 sections per major topic, key quotes, and takeaways
- **Quotes**: Notable quotes with their timestamps

**Default Full Document output order** (when no specific format is requested):
1. Summary
2. Chapters
3. Thread
4. Blog Post
5. Quotes

### Workflow

1. Fetch transcript using the Composite component above.
2. **Validate**: confirm `segment_count >= 1`. If empty, tell the user the video has transcripts disabled.
3. **Chunk if needed**: if `full_text` exceeds ~50,000 characters, split `timestamped_text` into overlapping chunks (~40K characters with 2K overlap) and summarize each chunk before merging.
4. **Transform** into the requested format(s) using the `timestamped_text` field. If no format specified, produce all five sections.
5. **Verify**: re-read the output for coherence, correct timestamps (if chapters), and completeness before presenting.

### Example — Chapters Output

```
0:00 Introduction — host opens with the problem statement
3:45 Background — prior work and why existing solutions fall short
12:20 Core method — walkthrough of the proposed approach
24:10 Results — benchmark comparisons and key takeaways
31:55 Q&A — audience questions on scalability and next steps
```

### Example — Thread Output

```
1/ Just watched an incredible video on [topic]. Key takeaways 🧵

2/ First insight: [point]. This matters because [reason].

3/ The surprising part: [finding]. Most assume [belief], but this shows otherwise.

4/ Practical takeaway: [action].

5/ Full video: [URL]
```

## Error Handling

- **Transcripts disabled**: `get-languages.py` returns error; tell user and suggest checking if captions are available on the video page
- **Private/unavailable video**: page will not load correctly; relay the error and ask user to verify the URL
- **Transcript button not found**: usually means the user is not on a video page, or the page hasn't finished loading; navigate to the URL and retry
- **No segments after panel opens**: retry `open-transcript-panel.py` + `wait stable` + `extract-transcript-segments.py` once

## Known Limitations

- Language selection: the transcript panel shows the language YouTube defaults to for the user's region. Switching to a specific language requires changing the caption language in the player's CC settings first; automatic language switching is not implemented.
- Auto-generated transcripts (kind: asr) may have lower accuracy than manual captions.
- Videos that require login to view will not have a transcript panel accessible.

## Execution Efficiency

- **Batch orchestration**: Write a bash script to loop through video URLs serially within a single session — navigate to each video, run the 3-step composite workflow, save result, then move to the next. Do not parallelize within one browser. To increase throughput for large batches, open multiple stealth browser sessions and distribute URLs across them.
- **Test before batch execution**: After writing a batch script, first test with 1–2 videos to confirm the full workflow runs correctly; only then run the full batch.
- **Reduce redundant pre-operations**: Pre-execution checks (tool readiness) only need to run once per session; skip them for subsequent videos in the same batch.
- **Error resumption**: Save each video's result immediately after extraction; on failure, resume from the failed video rather than starting over.

## Success Criteria

`segment_count >= 1 AND full_text length > 0`

## Experience Notes

Path: `{working-directory}/browser-act-skill-forge-memories/youtube-content-youtube-transcript.memory.md`

**Before execution**: If the file exists, read it first — it records unexpected situations encountered during past executions (e.g., a strategy has become ineffective); adjust strategy order accordingly.

**After execution**: If an unexpected situation is encountered (strategy became ineffective, page redesigned, anti-scraping upgraded, better path discovered), append a line:
`{YYYY-MM-DD}: {what happened} → {conclusion}`

Normal execution does not write to the file.
