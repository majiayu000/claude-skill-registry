---
name: youtube
description: >-
  Analyze a YouTube video and create a vault note from its transcript.
  Use this skill whenever a YouTube URL is pasted — even with casual commentary
  like "check this out" or "interesting talk." Also triggers on "youtube",
  "take notes from this video", "summarize this video", or any YouTube link
  (youtube.com, youtu.be) regardless of surrounding context.
allowed-tools: Bash, Read, Write, Edit, Agent, TodoWrite, Grep, Glob
argument-hint: "<youtube-url>"
---

<Purpose>
Extract transcript and metadata from a YouTube video, then synthesize it into
a vault-formatted post note. Uses youtube-transcript-api for transcript and
yt-dlp for rich metadata (with oEmbed fallback).
</Purpose>

<Use_When>
- User shares a YouTube URL and wants notes taken
- User says "take notes from this video"
- User pastes a YouTube link with /youtube
- User wants to add a video's insights to the vault
</Use_When>

<Do_Not_Use_When>
- User wants to watch or download the video itself
- User has a local video file (not YouTube)
- Video has no transcript/captions at all
- User wants to process an existing vault note (use /process)
</Do_Not_Use_When>

<Execution_Policy>
- Extract first, synthesize second, integrate third
- Always check vault for existing notes on the same video before creating
- Create note as type: post with processing_status: inbox
- The note is a starting point — user can /process it later for deeper engagement
</Execution_Policy>

<Steps>

## Stage 1: EXTRACT

Parse the YouTube URL/ID from $ARGUMENTS. If no URL provided, ask the user.

Run the extraction script. Redirect stdout to a temp file (stderr has progress messages that break piping):

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR}"
YT_OUTPUT="$SKILL_DIR/_output.json"
uv run "$SKILL_DIR/scripts/fetch_youtube.py" "VIDEO_URL" --lang en > "$YT_OUTPUT"
```

Then read `$YT_OUTPUT` with the Read tool to get the JSON. Clean up the file after use.

The JSON contains:
- `title`, `channel`, `duration`, `upload_date`, `description`, `chapters`
- `transcript.full_text`, `transcript.segments`, `transcript.language`
- `transcript.error` (null if success)

**If transcript.error is not null:** inform the user and stop. No note without content.

**If transcript is very long (>50,000 chars):** warn the user this is a long video.
Chunk the transcript for the agent if needed — send first 40,000 chars with a note
about total length. For very long videos (>2hrs), consider suggesting the user
watch key sections instead.

## Stage 2: SYNTHESIZE

Read the agent definition:
```
Read("${CLAUDE_SKILL_DIR}/agents/video-noter.md")
```

Search the vault for existing notes related to the video's topics using the MCP tool:
```
search_notes(query="KEYWORD", limit=20)
```
Or fall back to Grep if MCP is unavailable:
```
Grep(pattern="KEYWORD", path="notes/", glob="*.md", head_limit=20)
```

Launch the video-noter agent:

```
Agent(
  subagent_type="general-purpose",
  model="sonnet",
  run_in_background=false,
  prompt="You are Video Noter. Follow these instructions exactly:

  [INSERT FULL CONTENT OF agents/video-noter.md HERE]

  VIDEO METADATA:
  - Title: [title]
  - Channel: [channel]
  - Duration: [duration]
  - Upload date: [upload_date]
  - Chapters: [chapters if any]
  - Description: [first 500 chars of description]

  EXISTING VAULT NOTES ON RELATED TOPICS:
  [List any matching notes found in grep]

  TRANSCRIPT:
  [full_text or chunked text]

  Produce the note body following the Output Format. Do NOT include frontmatter —
  only the body starting from the # title line."
)
```

## Stage 3: INTEGRATE

1. Generate timestamp ID:
```bash
date +%Y%m%d%H%M%S
```

2. Format the upload_date for frontmatter (YYYYMMDD → YYYY-MM-DD)

3. Check for duplicate notes:
```bash
grep -rl "VIDEO_TITLE" notes/ --include="*.md" | head -5
```

4. Create the note file with frontmatter + agent output:

```markdown
---
id: YYYYMMDDHHMMSS
type: post
processing_status: inbox
author: Channel Name
link: "https://www.youtube.com/watch?v=VIDEO_ID"
created_date: YYYY-MM-DD
updated_date: YYYY-MM-DD
---

[AGENT OUTPUT HERE — starts with # title and 🏷️Tags line]
```

Place the note in `notes/` under the most appropriate topic subfolder:
- ML/AI content → `notes/ml/`
- Startup/business → `notes/startup/`
- Finance → `notes/finance/`
- Design → `notes/design/`
- Psychology → `notes/psychology/`
- General/unclear → `notes/`

5. Report to user:
   - Note path and title
   - Number of concepts suggested for extraction
   - Any related vault notes found
   - Remind: "Run /process on this note when you're ready to deepen it"

</Steps>

<Tool_Usage>
- **Bash**: Run fetch_youtube.py script (via uv run), generate timestamps, search vault
- **Read**: Read agent definition, read existing vault notes for context
- **Write**: Create the post note in vault
- **Agent**: Delegate synthesis to video-noter agent (sonnet)
- **Grep/Glob**: Search vault for duplicates and related notes
- **TodoWrite**: Track progress through stages
</Tool_Usage>

<Examples>
<Good>
User: /youtube https://www.youtube.com/watch?v=abc123
1. Extract → transcript (12 min video, 3400 words) + metadata (title, channel, chapters)
2. Search vault → found 2 related notes on the topic
3. Agent synthesizes → 6 themed sections, 4 questions, 3 concept suggestions
4. Create note → notes/ml/(Post) Video Title.md
5. Report: "Created note with 6 sections. Found connections to [[Existing Note 1]]
   and [[Existing Note 2]]. 3 concepts could become Term notes. Run /process when ready."
</Good>

<Bad>
User: /youtube https://www.youtube.com/watch?v=abc123
- Creates note that is just a chronological transcript summary
- Misses connections to existing vault notes
- Doesn't check for duplicates
- Places note in wrong folder
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- **No transcript available**: Inform user, suggest manual notes while watching
- **Transcript in wrong language**: Try other available languages, report what's available
- **yt-dlp fails for metadata**: Fall back to oEmbed (basic title/channel only)
- **Video extremely long (>3hrs)**: Warn user, offer to process first N minutes only
- **Duplicate note exists**: Show existing note, ask if user wants to update or create new
</Escalation_And_Stop_Conditions>

$ARGUMENTS
