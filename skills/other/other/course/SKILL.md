---
name: course
description: >-
  Process an online course into detailed vault notes — one per lecture, with
  slides and transcripts synthesized. Use this skill whenever the user shares a
  course URL, syllabus page, or lecture playlist and wants structured notes from
  it. Also triggers on "process this course", "take notes on these lectures",
  "course notes", any university course page, or when someone pastes a link to a
  course with multiple lectures/sessions. Even if the user just says "check out
  this course" or drops a .edu link with a schedule — use this skill.
allowed-tools: Bash, Read, Write, Edit, Agent, Grep, Glob, WebFetch
argument-hint: "<course-url> [lecture range, e.g. 1-3]"
---

<Purpose>
Two modes:

**Process mode** (default): Crawl an online course page, extract the lecture
schedule with all materials (slides PDFs, YouTube videos, readings), then
process each lecture into a detailed vault-formatted note with embedded slide
images and synthesized transcripts. Creates a Course index note linking
everything together.

**Refine mode**: Re-read existing course lecture notes and improve them —
deepen equation explanations, add missing analogies, fix structure, strengthen
cross-references. Triggered when user says "refine", "improve", "fix", or
references existing course notes rather than a URL.

This is an orchestrator — it coordinates downloading, extraction, and synthesis
across multiple lectures, producing a complete course knowledge package in the
vault.
</Purpose>

<Use_When>
- User shares a course URL (syllabus, schedule, or homepage)
- User says "process this course" or "take notes on these lectures"
- User pastes a university course page with a lecture list
- User wants to batch-process a series of lectures from one course
- User has a YouTube playlist of course lectures
- User wants to refine/improve existing course notes ("refine mit diffusion notes", "improve L03")
</Use_When>

<Do_Not_Use_When>
- User has a single YouTube video (use /youtube)
- User has a single local video file (use /lecture)
- User wants to process an existing vault note that's NOT a lecture (use /process)
- User wants a single paper summarized (use /paper)
</Do_Not_Use_When>

<Steps>

## Stage 1: CRAWL — Extract the Lecture List

Parse the course URL from $ARGUMENTS. If no URL, ask the user.

Fetch the course page and extract structured lecture data:

```
WebFetch(
  url="COURSE_URL",
  prompt="Extract the complete course structure as JSON. For each lecture/session, include:
    - number (int)
    - title (string)
    - date (string, if available)
    - slides_url (string or null — look for PDF links to slides/lecture notes)
    - video_url (string or null — look for YouTube links)
    - readings (array of {title, url} — papers, blog posts, textbook chapters)
    - description (string or null — any summary text)
  Also extract:
    - course_title (string)
    - course_code (string or null)
    - instructors (array of strings)
    - course_url (string — the page URL)
    - course_notes_url (string or null — if there's a single PDF of all course notes)
  Return ONLY valid JSON, no markdown fencing."
)
```

Parse the JSON response. If the page has relative URLs for slides/videos, resolve
them against the course URL's base.

**Handle edge cases:**
- If the page is a YouTube playlist: extract video IDs and titles from the playlist
- If slides URLs are relative (e.g., `../docs/lecture_01.pdf`): resolve to absolute URLs
- If no structured schedule found: ask user to provide lecture list manually

## Stage 1b: DERIVE COURSE TAG

Generate a short, memorable course hashtag from the course code or title.
This tag will be used consistently across ALL notes for this course.

Rules for the tag:
- Use a descriptive short slug from the course topic, not just the code
- The tag should tell you what the course is ABOUT at a glance
- Examples: `#mit-diffusion`, `#cs231n-vision`, `#stanford-rl`, `#fast-ai-dl`
- Format: `institution-topic` or `code-topic` — lowercase, hyphens
- Keep it under 20 characters — short enough to type, long enough to understand
- Confirm the tag with the user before proceeding

Also derive a COURSE_SLUG for asset folder naming (same as tag without `#`).
Example: assets folder `assets/mit-diffusion/`, tag `#mit-diffusion`.

## Stage 2: PLAN — Confirm Scope with User

Present the extracted lecture list to the user in a clear table:

```
Found N lectures for "Course Title":
Course tag: #6s184
Assets folder: assets/6s184/

| # | Title | Slides | Video | Readings |
|---|-------|--------|-------|----------|
| 1 | Topic | PDF    | YT    | 2 papers |
| 2 | Topic | PDF    | —     | 1 paper  |
...

Which lectures should I process? (default: all)
Options: "all", "1-3", "1,3,5", or specific numbers
```

If $ARGUMENTS includes a range (e.g., "1-3"), skip confirmation and use that range.

## Stage 3: PROCESS — Handle Each Lecture

### Content Source Priority

Not all sources are equal. A 50-minute video transcript where the instructor
explains intuition, tells stories, and works through examples is 10x richer
than a terse slide deck with equations and bullet points. The skill must be
smart about which sources to use:

**Priority order** (use the best available, not just one):
1. **YouTube transcript + slides** — the gold standard. Transcript provides
   the instructor's voice, explanations, and examples. Slides provide structure
   and visual reference. Use BOTH together.
2. **YouTube transcript only** — still very rich. The instructor's words carry
   most of the value. Synthesize without slide embeds.
3. **Course notes PDF + slide PDFs** — some courses publish comprehensive
   written notes (like a textbook). These can be as good as transcripts. Read
   the course notes PDF for the lecture's section, plus extract slide images.
4. **Slide PDFs only** — the weakest source. Slides are terse by design —
   they're prompts for the speaker, not standalone explanations. When this is
   all you have, the noter agent must work harder to reconstruct meaning and
   add explanatory context. The notes will be less rich.

**Key rule**: When a YouTube video exists, ALWAYS extract its transcript even
if slides are also available. The transcript is the primary content source;
slides are supplementary visual aids.

For each lecture in scope, spawn a parallel subagent. Each subagent does:

### 3a. Download & Extract Slides (if PDF available)

```bash
SKILL_DIR="${CLAUDE_SKILL_DIR}"
COURSE_SLUG="mit-diffusion"  # derived from course tag
LECTURE_NUM="01"
SLIDES_DIR="temp/course-slides-${COURSE_SLUG}"
mkdir -p "$SLIDES_DIR"

# Download PDF
curl -sL "SLIDES_PDF_URL" -o "$SLIDES_DIR/lecture-${LECTURE_NUM}.pdf"

# Convert PDF pages to images
uv run "$SKILL_DIR/scripts/extract_pdf_slides.py" \
  "$SLIDES_DIR/lecture-${LECTURE_NUM}.pdf" \
  --output-dir "$SLIDES_DIR/lecture-${LECTURE_NUM}-frames" \
  --prefix "${COURSE_SLUG}-L${LECTURE_NUM}"
```

The script outputs images and a manifest JSON. Copy selected frames to a
**course-specific subfolder** in `assets/`:

```bash
ASSETS_DIR="assets/${COURSE_SLUG}"
mkdir -p "$ASSETS_DIR"
cp "$SLIDES_DIR/lecture-${LECTURE_NUM}-frames"/*.png "$ASSETS_DIR/"
```

All slides for this course live in `assets/6s184/`, keeping them organized
and easy to find. The embed syntax still works: `![[6s184-L01-03.png]]`
(Obsidian resolves short names across subfolders).

### 3b. Extract YouTube Transcript (if video available)

Reuse the youtube skill's fetch script:

```bash
YT_SKILL_DIR="${CLAUDE_PLUGIN_ROOT}/skills/youtube"
YT_OUTPUT="temp/course-yt-${COURSE_SLUG}-L${LECTURE_NUM}.json"
uv run "$YT_SKILL_DIR/scripts/fetch_youtube.py" "VIDEO_URL" --lang en > "$YT_OUTPUT"
```

Read the JSON output. If transcript fails, proceed with slides only.

### 3c. Read Supplementary Content

**If course notes PDF exists**: Read the relevant section from the course notes
PDF. This is often richer than individual slide PDFs — it's written prose with
explanations, not just bullet points. Pass this to the noter agent as primary
text content alongside any transcript.

**If no video transcript and no course notes**: Read the slide PDF directly via
the Read tool. This is the weakest source — the noter agent must reconstruct
meaning from terse bullets and equations. Flag this in the agent prompt so it
knows to add more explanatory context.

### 3d. Synthesize Lecture Note

Read the agent definition:
```
Read("${CLAUDE_SKILL_DIR}/agents/course-noter.md")
```

Launch the course-noter agent:

```
Agent(
  subagent_type="general-purpose",
  model="sonnet",
  run_in_background=true,
  prompt="You are Course Noter. Follow these instructions exactly:

  [INSERT FULL CONTENT OF agents/course-noter.md HERE]

  COURSE CONTEXT:
  - Course: [course_title]
  - Lecture [number] of [total]: [lecture_title]
  - Date: [date]
  - Instructors: [instructors]
  - Other lectures in this course: [list of other lecture titles for cross-referencing]

  SOURCE LINKS (include these in the note's Source Materials section):
  - Video: [YouTube URL or null]
  - Slides PDF: [PDF URL or null]
  - Course page: [course URL]

  CONTENT QUALITY TIER: [one of: transcript+slides, transcript-only, notes+slides, slides-only]
  (If slides-only: you're working from terse bullet points and equations.
   Work harder to explain WHY each concept matters, add intuitive analogies,
   and fill in the reasoning the instructor would have spoken aloud.)

  SLIDE FRAMES (for ![[embedding]]):
  [frame manifest — filename, page number, brief description of each slide]

  EXISTING VAULT NOTES ON RELATED TOPICS:
  [search results from vault]

  TRANSCRIPT (if available — this is your PRIMARY content source):
  [full transcript text]

  COURSE NOTES TEXT (if available — richer than slides alone):
  [relevant section from course notes PDF]

  PDF TEXT CONTENT (fallback when no transcript or course notes):
  [extracted PDF text]

  READINGS LISTED:
  [titles and URLs of any readings for this lecture]

  Produce the note body following the Output Format. Do NOT include frontmatter."
)
```

## Stage 4: INTEGRATE — Assemble Everything

### 4a. Create Lecture Notes

For each processed lecture, create a note file:

```markdown
---
id: YYYYMMDDHHMMSS
type: lecture
processing_status: inbox
link: "COURSE_URL"
created_date: YYYY-MM-DD
updated_date: YYYY-MM-DD
---

[AGENT OUTPUT — starts with # title]
```

**Naming convention:** `(Lecture) Short Tag - L01 Topic Title.md`
Example: `(Lecture) MIT Diffusion - L01 Flow and Diffusion Models.md`

The short tag in the filename matches the course tag (capitalized for readability).

Place in `notes/ml/` for ML/AI courses, `notes/` + appropriate subfolder for others.

### 4b. Create Course Index Note

```markdown
---
id: YYYYMMDDHHMMSS
type: course
processing_status: inbox
link: "COURSE_URL"
created_date: YYYY-MM-DD
updated_date: YYYY-MM-DD
---

# (Course) Course Title
- **🏷️Tags** : #course #mit-diffusion #diffusion #flow-matching #MM-YYYY

## Overview
- **Institution**: MIT / Stanford / etc.
- **Instructors**: Names
- **Lectures processed**: N of M
- **Course tag**: `#mit-diffusion` — use this to find all notes from this course

## Lectures
- [[(Lecture) MIT Diffusion - L01 Flow and Diffusion Models]] — one-line summary
- [[(Lecture) MIT Diffusion - L02 Flow Matching]] — one-line summary
- ...

## Course Materials
- [Course page](URL)
- [Course notes PDF](URL) (if available)

## Key Concepts Across Lectures
- [[(Term) Concept]] — appears in L01, L03, L05
- [[(Term) Another Concept]] — introduced in L02, applied in L04

## Related links
- [[(Type) Related Vault Note]] — connection
```

### 4c. Report to User

Show:
- Course note path
- List of lecture notes created with paths
- Total slides embedded
- Key concepts identified across lectures
- Remind: "Run /process on individual lecture notes to deepen them"

</Steps>

<Tool_Usage>
- **WebFetch**: Crawl course page to extract lecture list and metadata
- **Bash**: Download PDFs, run extraction scripts, generate timestamps
- **Read**: Read agent definitions, read PDFs for content, view slide images
- **Write**: Create lecture and course notes
- **Agent**: Parallel subagents for lecture processing (one per lecture)
- **Grep/Glob**: Search vault for related notes and duplicates
</Tool_Usage>

<Examples>
<Good>
User: /course https://diffusion.csail.mit.edu/2026/index.html
1. Crawl → found 6 lectures with PDF slides, no videos
2. Derive tag → `#mit-diffusion`, assets folder `assets/mit-diffusion/`
3. Plan → "Found 6 lectures. Course tag: #mit-diffusion. Process all?"
4. User confirms → spawn 6 parallel agents
4. Each agent: download PDF slides → extract 8-15 slide images → read PDF text → synthesize
5. Create 6 lecture notes with embedded slide images + thematic synthesis
6. Create course index linking all 6 lectures
7. Report: "Created (Course) 6.S184 and 6 lecture notes. 67 slide images embedded.
   Found connections to [[(Term) Diffusion Models]] and [[(Paper) Scaling Laws]].
   Run /process on individual lectures to deepen."
</Good>

<Bad>
- Downloads all slides but doesn't read or embed them
- Creates chronological transcript dumps instead of thematic synthesis
- Processes lectures sequentially instead of in parallel
- Doesn't cross-reference between lectures
- Creates notes but no course index
- Misses existing vault connections
</Bad>
</Examples>

<Escalation_And_Stop_Conditions>
- **Course page can't be parsed**: Ask user to provide lecture list manually
- **PDF download fails**: Skip slides for that lecture, note the gap
- **YouTube transcript unavailable**: Proceed with slides-only synthesis
- **Neither slides nor video**: Skip lecture, report to user
- **Very large course (>20 lectures)**: Suggest processing in batches of 5-6
- **Paywall or login required**: Inform user, can't access behind auth
</Escalation_And_Stop_Conditions>

<Refine_Mode>

## Detecting Refine Mode

If $ARGUMENTS contains NO URL and instead references existing notes ("refine",
"improve", "fix", mentions a course name or lecture number, or complains about
note quality), enter refine mode instead of process mode.

## Refine Steps

### Step 1: Find the Course Notes

Search the vault for the course index note and all lecture notes:
```
Glob(pattern="notes/**/*Course*KEYWORD*.md")
Glob(pattern="notes/**/*Lecture*KEYWORD*.md")
```

If ambiguous, ask the user which course.

### Step 2: Determine Scope

- If user specifies lectures ("L03", "1-3", "all"): refine those
- If user gives general feedback ("too technical", "needs more examples"):
  apply to all lectures in the course
- Ask the user what's wrong if the feedback is unclear

### Step 3: Read and Diagnose

For each lecture in scope:
1. Read the full note
2. Diagnose against the course-noter quality criteria:
   - Are key equations present AND deeply explained? (not just stated)
   - Does every section lead with intuition, not formalism?
   - Are there cross-domain analogies?
   - Are sections organized by insight, not slide order?
   - Is the Concepts for extraction list reasonable (3-6 items)?

Present a brief diagnosis to the user: "Here's what I'd fix in each note..."
Get confirmation before proceeding.

### Step 4: Refine in Parallel

Spawn one subagent per lecture note. Each subagent:
1. Reads the current note
2. Reads agents/course-noter.md for quality standards
3. Applies targeted edits (using Edit tool, NOT full rewrite) to fix
   the diagnosed issues
4. Preserves all frontmatter, slide embeds, and wikilinks

The agent prompt should include:
- The specific issues diagnosed for this note
- The user's feedback verbatim
- The full course-noter.md quality standards
- Instructions to use Edit for targeted fixes, not Write for full rewrite

### Step 5: Report

Show the user what changed in each note — section-level summary, not diffs.
Suggest running /process on individual notes for deeper engagement.

</Refine_Mode>

$ARGUMENTS
