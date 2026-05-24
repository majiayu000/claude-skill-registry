---
name: lecture
description: >-
  Extract transcript and key slides from a local video file, then create a
  vault-formatted lecture note. Use this skill whenever a user provides a local
  video file (.mp4, .mov, .mkv, .avi, .webm) and wants notes from it. Triggers
  on "lecture", "take notes", "I have a recording of", "class video",
  "transcribe this presentation", "process this video for notes", or /lecture.
  Works with any language — auto-detects transcript language.
allowed-tools: Bash, Read, Write, Edit, Agent, Grep, Glob
argument-hint: "<path-to-video-file>"
---

<Purpose>
Transcribe a local video lecture using mlx-whisper (Apple Silicon), extract key
slide frames with timestamps, then synthesize into a vault-formatted lecture note
with embedded screenshots. Auto-detects transcript language — works with any language,
outputs English notes.
</Purpose>

<Use_When>
- User provides a local video file and wants lecture notes
- User says "take notes from this lecture/video"
- User uses /lecture with a file path
- User has an MP4/MOV/MKV file to process
</Use_When>

<Do_Not_Use_When>
- User has a YouTube URL (use /youtube instead)
- User wants to process an existing vault note (use /process)
- User wants audio-only transcription without note synthesis
</Do_Not_Use_When>

<Prerequisites>
- `ffmpeg` installed (for audio extraction and frame capture)
- `uv` installed (`brew install uv` or `curl -LsSf https://astral.sh/uv/install.sh | sh`)
- Apple Silicon Mac (mlx-whisper is optimized for M-series chips)
</Prerequisites>

<Execution_Policy>
- Extract first, synthesize second, integrate third
- Always check vault for existing notes on the same topic before creating
- Create note as type: lecture with processing_status: inbox
- The note is a starting point — user can /process it later for deeper engagement
- Transcription can take several minutes for long videos — inform the user
</Execution_Policy>

<Steps>

## Stage 1: EXTRACT

Parse the video file path from $ARGUMENTS. If no path provided, ask the user.
Verify the file exists and is a video format (mp4, mov, mkv, avi, webm).

Run the extraction script:

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR}"
LECTURE_OUTPUT="temp/lecture-extract-output.json"
uv run "$SKILL_DIR/scripts/extract_lecture.py" "VIDEO_PATH" > "$LECTURE_OUTPUT" 2>&1 &
```

**IMPORTANT:** This script takes time (several minutes for a 30-60 min video).
Inform the user: "Extracting audio and transcribing — this will take a few minutes for a [duration] video."

Run it and wait for completion. Then read the output JSON.

The JSON contains:
- `filename`, `duration`, `duration_seconds`, `width`, `height`
- `transcript.full_text`, `transcript.segments` (with start/end times), `transcript.language`
- `transcript.error` (null if success)
- `frames[]` — array of `{path, timestamp_seconds, timestamp}` for each extracted slide
- `output_dir` — temp directory with extracted frames

**If transcript.error is not null:** inform the user and stop. Check if mlx-whisper is installed.

**If transcript is very long (>80,000 chars):** warn the user. Send first 60,000 chars to the agent
with a note about total length.

## Stage 2: PREPARE FRAMES

Copy the extracted frames to the vault's assets directory with a descriptive naming scheme:

```bash
# Generate a slug from the video filename
SLUG=$(echo "VIDEO_FILENAME" | sed 's/\.[^.]*$//' | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | sed 's/[^a-z0-9-]//g' | cut -c1-30)
ASSETS_DIR="assets"

for frame in FRAME_PATHS; do
  FRAME_NUM=$(basename "$frame" | grep -o '[0-9]*')
  cp "$frame" "$ASSETS_DIR/lecture-${SLUG}-${FRAME_NUM}.jpg"
done
```

Build a frame manifest for the noter agent — each frame gets:
- Its vault filename (for `![[embedding]]`)
- Its timestamp in the video (e.g., "12:30")

Example manifest:
```
FRAMES WITH TIMESTAMPS:
- lecture-risk-mgmt-01.jpg (timestamp: 0:10)
- lecture-risk-mgmt-02.jpg (timestamp: 2:00)
- lecture-risk-mgmt-03.jpg (timestamp: 4:00)
...
```

## Stage 3: SYNTHESIZE

Read the agent definition:
```
Read("${CLAUDE_SKILL_DIR}/agents/lecture-noter.md")
```

Search the vault for existing notes related to the lecture's topics using the MCP tool:
```
search_notes(query="KEYWORD", limit=20)
```
Or fall back to Grep if MCP is unavailable:
```
Grep(pattern="KEYWORD", path="notes/", glob="*.md", head_limit=20)
```

**Review each frame** using the Read tool to see what's on each slide.
Build a brief description of each frame's content (1 line each) to include in the agent prompt.

Launch the lecture-noter agent:

```
Agent(
  subagent_type="general-purpose",
  model="sonnet",
  run_in_background=false,
  prompt="You are Lecture Noter. Follow these instructions exactly:

  [INSERT FULL CONTENT OF agents/lecture-noter.md HERE]

  VIDEO METADATA:
  - Filename: [filename]
  - Duration: [duration]
  - Transcript language: [language from extraction JSON]

  FRAMES WITH TIMESTAMPS AND DESCRIPTIONS:
  - lecture-slug-01.jpg (timestamp: 0:10) — Title slide showing course name
  - lecture-slug-02.jpg (timestamp: 2:00) — Diagram of risk framework
  [... one line per frame with what you see on it]

  EXISTING VAULT NOTES ON RELATED TOPICS:
  [List any matching notes found in grep search]

  TRANSCRIPT:
  [full_text]

  Produce the note body following the Output Format. Do NOT include frontmatter —
  only the body starting from the # title line.
  Use the exact filenames from FRAMES list for ![[embedding]] — do not invent filenames."
)
```

## Stage 4: INTEGRATE

1. Generate timestamp ID:
```bash
date +%Y%m%d%H%M%S
```

2. Determine the best subfolder for the note:
   - ML/AI → `notes/ml/`
   - Business/startup → `notes/startup/`
   - Finance → `notes/finance/`
   - Design → `notes/design/`
   - Psychology → `notes/psychology/`
   - General → `notes/`

3. Create the note file with frontmatter + agent output:

```markdown
---
id: YYYYMMDDHHMMSS
type: lecture
processing_status: inbox
created_date: YYYY-MM-DD
updated_date: YYYY-MM-DD
---

[AGENT OUTPUT HERE — starts with # title, includes embedded screenshots]
```

4. Clean up temp files:
```bash
rm -rf "$OUTPUT_DIR"
rm -f "$LECTURE_OUTPUT"
```

5. Report to user:
   - Note path and title
   - Number of screenshots embedded
   - Number of concepts suggested for extraction
   - Any related vault notes found
   - Remind: "Run /process on this note when you're ready to deepen it"

</Steps>

<Tool_Usage>
- **Bash**: Run extract_lecture.py, copy frames, generate timestamps, search vault
- **Read**: Read agent definition, read extracted JSON, view frame images for descriptions, read existing vault notes
- **Write**: Create the lecture note in vault
- **Agent**: Delegate synthesis to lecture-noter agent (sonnet model)
- **Grep/Glob**: Search vault for duplicates and related notes
</Tool_Usage>

<Examples>
<Good>
User: /lecture /tmp/risk-management-training.mp4
1. Extract → transcript (48 min video, ~59K chars Vietnamese) + 12 frames with timestamps
2. Copy frames to assets/ as lecture-risk-mgmt-01.jpg through lecture-risk-mgmt-08.jpg
3. Review each frame → build descriptions (title slide, framework diagram, severity table, etc.)
4. Search vault → found 3 related notes on risk and finance topics
5. Agent synthesizes → 6 themed sections, 5 embedded screenshots, 4 questions, 3 concept suggestions
6. Create note → notes/finance/(Lecture) Risk Management Overview.md
7. Report: "Created lecture note with 6 sections and 5 embedded slides.
   Found connections to [[(Term) Credit Cycle]] and [[(Term) Second-Order Thinking]].
   3 concepts could become Term notes. Run /process when ready."
</Good>

<Bad>
User: /lecture /tmp/risk-management-training.mp4
- Dumps raw transcript into a note without synthesis
- Saves screenshots without timestamps, can't trace back to video
- Creates chronological summary instead of thematic organization
- Misses cross-domain connections
- Doesn't review frame content before passing to agent
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- **uv not installed**: Print install command (`brew install uv`) and stop
- **ffmpeg not found**: Inform user to install via homebrew
- **Transcript error**: Report the error, suggest checking audio track
- **Video extremely long (>3hrs)**: Warn user, offer to process first half only
- **No audio track**: Inform user, offer to extract frames only
- **Duplicate note exists**: Show existing note, ask if user wants to update or create new
</Escalation_And_Stop_Conditions>

$ARGUMENTS
