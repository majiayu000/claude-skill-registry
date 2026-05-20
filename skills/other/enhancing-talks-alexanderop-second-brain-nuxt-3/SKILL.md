---
name: enhancing-talks
description: Enhance talk notes with Blinkist-style summaries and timestamps. Use when asked to "enhance talk", "improve talk notes", "add timestamps", "blinkist-style talk summary", or "make talk notes better". Adds Core Message, Key Insights with timestamps, Talk Structure, Notable Quotes, Who Should Watch, and Action Items via transcript analysis.
allowed-tools: Read, Write, Edit, Bash, WebFetch, Glob, Grep, Task, TaskOutput, WebSearch, AskUserQuestion
---

# Enhancing Talk Notes

This skill transforms basic talk notes into Blinkist-style summaries with timestamped insights, talk structure, and actionable takeaways.

## Workflow Overview

```text
Phase 1: Talk Identification
   └─ Find and validate talk note

Phase 2: Transcript Acquisition
   └─ Fetch timestamped transcript (JSON format)

Phase 3: Parallel Analysis (4 agents)
   ├─ Agent 1: Key insights from transcript chunks
   ├─ Agent 2: Talk structure & section boundaries
   ├─ Agent 3: Notable quotes with timestamps
   └─ Agent 4: Audience, prerequisites & action items

Phase 4: Content Synthesis
   ├─ Core Message (1-2 sentences)
   ├─ Key Insights (8-12 timestamped blinks)
   ├─ Talk Structure (chapter-style overview)
   ├─ Notable Quotes (3 quotes with timestamps)
   ├─ Who Should Watch
   └─ Action Items

Phase 5: User Review (BLOCKING GATE)
   └─ Present content, await approval

Phase 6: Save Enhanced Note
   └─ Insert sections, preserve original

Phase 7: Quality Check
   └─ Run pnpm lint:fix && pnpm typecheck
```

---

## Phase 1: Talk Identification

### 1.1 Find the Talk Note

Accept a talk slug, title, or partial name as argument:

1. **Try exact slug match first**: Check if `content/{slug}.md` exists (convert spaces to hyphens, lowercase)
2. **If no exact match**: Use Grep to search for the title in talk notes:
   ```text
   Grep pattern: "title:.*{search term}" with glob: "content/*.md"
   ```
3. **Filter to talks only**: Read matching files and verify `type: talk` in frontmatter

**Outcomes:**
- Single match → proceed with that file
- Multiple matches → list options for user to choose
- No match → list available talks with `type: talk`

### 1.2 Validate and Extract

Read the note and verify:
1. Frontmatter has `type: talk`
2. Has required fields: `title`, `url`, `authors`

Extract and store:
- **URL**: YouTube video URL for transcript fetching
- **Frontmatter**: title, authors, conference, summary
- **Opening paragraph**: First paragraph before any `##` heading
- **Body sections**: All content from first `##` heading onwards

If not a talk, inform user this skill only works on talk notes.

---

## Phase 2: Transcript Acquisition

### 2.1 Fetch Timestamped Transcript

Use the enhanced transcript script with JSON format:

```bash
python3 .claude/skills/adding-notes/scripts/get-youtube-transcript.py '{url}' --format=json
```

This returns structured data:
```json
{
  "video_id": "abc123",
  "language": "en",
  "is_generated": true,
  "total_duration": 2700,
  "total_duration_formatted": "45:00",
  "segment_count": 90,
  "segments": [
    {"start": 0.0, "timestamp": "0:00", "duration": 30.5, "text": "..."},
    {"start": 30.5, "timestamp": "0:30", "duration": 28.2, "text": "..."}
  ]
}
```

### 2.2 Handle Transcript Failures

If transcript unavailable:
1. **Check for manual transcript**: `--list` flag shows available options
2. **Try alternative language**: Use `--lang` flag
3. **Fall back to web research**: Switch to WebSearch-based analysis (like enhancing-notes)

Store transcript data for parallel agent processing.

---

## Phase 3: Parallel Analysis

Spawn **4 agents in parallel** to analyze the transcript:

### Agent Configuration

Read `references/chunking-strategy.md` and `references/insight-extraction.md` before spawning agents.

```markdown
**Agent 1 - Key Insights:**
Task tool with subagent_type: "general-purpose"
prompt: |
  Analyze this talk transcript to extract 8-12 key insights.

  TRANSCRIPT (with timestamps):
  {timestamped_transcript}

  For each insight:
  1. Identify a specific, standalone idea (not vague)
  2. Note the timestamp where it's discussed
  3. Write 2-3 sentences explaining with concrete detail
  4. Use bold title format

  Output format for each insight:
  **[Insight Title]** (MM:SS) - [2-3 sentence explanation with specific examples or data from the talk]

  Guidelines from references/insight-extraction.md:
  - Each insight must be self-contained and valuable alone
  - Include concrete examples, data, or frameworks mentioned
  - Progress from foundational to advanced concepts
  - Avoid generic statements like "the speaker emphasizes the importance of X"

**Agent 2 - Talk Structure:**
Task tool with subagent_type: "general-purpose"
prompt: |
  Analyze this transcript to identify the talk's structure.

  TRANSCRIPT (with timestamps):
  {timestamped_transcript}

  Identify 4-7 major sections with:
  1. Section title (descriptive, 2-4 words)
  2. Starting timestamp
  3. Brief description (1 sentence)

  Look for:
  - Introduction/opening hook
  - Major topic transitions
  - Key examples or stories
  - Conclusion/call to action

  Output format:
  1. **[Section Title]** (MM:SS) - [One sentence description]
  2. **[Section Title]** (MM:SS) - [Description]
  ...

**Agent 3 - Notable Quotes:**
Task tool with subagent_type: "general-purpose"
prompt: |
  Extract the 3 most powerful, quotable moments from this talk.

  TRANSCRIPT (with timestamps):
  {timestamped_transcript}

  Selection criteria:
  - Captures the talk's core philosophy
  - Memorable and shareable phrasing
  - Represents different aspects of the talk
  - Surprising insight or contrarian view

  For each quote:
  1. Extract the exact words (clean up filler words if needed)
  2. Note the timestamp
  3. Keep under 40 words each

  Output format:
  > "Quote text here." (MM:SS)

  > "Second quote here." (MM:SS)

  > "Third quote here." (MM:SS)

**Agent 4 - Audience & Actions:**
Task tool with subagent_type: "general-purpose"
prompt: |
  Analyze this talk to identify the target audience and actionable takeaways.

  TRANSCRIPT (with timestamps):
  {timestamped_transcript}

  TALK INFO:
  Title: {title}
  Speaker: {author}
  Conference: {conference}

  Generate:

  1. WHO SHOULD WATCH (1-2 paragraphs):
     - Professional context (developers, designers, managers, etc.)
     - Problems they're trying to solve
     - What they'll gain from watching
     - Any prerequisites or background knowledge needed

  2. ACTION ITEMS (3-5 concrete actions):
     - Specific, actionable next steps viewers can take
     - Based on explicit or implicit recommendations in the talk
     - Checkbox format: - [ ] Action item

  Output format:
  ## Who Should Watch
  [1-2 paragraphs]

  ## Action Items
  - [ ] First action
  - [ ] Second action
  ...
```

Collect all results via `TaskOutput` (blocking).

### Writing Style Reference

Before generating content, read `.claude/skills/writing-style/SKILL.md` for the full writing guidelines. Key points:
- **Active voice**: "The speaker argues..." not "It is argued..."
- **No boilerplate**: Jump straight to insights, no "This talk explores..."
- **End with emphasis**: Put the key point at the end of sentences
- **Everyday words**: "use" not "utilize", "help" not "facilitate"
- **No vague pronouns**: Name the thing, don't say "this leads to that"

---

## Phase 4: Content Synthesis

Using transcript analysis results, generate six new sections:

### 4.1 Core Message

Write the talk's thesis in 1-2 sentences:
- Capture the central argument or insight
- Be concise (under 50 words)
- Make it memorable and quotable

**Example:**
> Local-first software must survive not just network outages, but the complete disappearance of its creators. The key is commoditized sync infrastructure with open protocols.

### 4.2 Key Insights

Compile 8-12 numbered insights from Agent 1:

**Format:**
```markdown
1. **[Insight Title]** (12:34) - [2-3 sentence explanation with specific detail]
```

**Guidelines:**
- Each insight should be standalone and valuable
- Timestamp links to the moment in the video
- Include concrete examples or data when mentioned
- Progress from foundational to advanced concepts
- Avoid generic statements - be specific

**Example:**
```markdown
1. **CRDTs Are Necessary But Not Sufficient** (8:45) - Skiff, built on yjs CRDTs, still shut down when Notion acquired it. Technology alone doesn't guarantee resilience—the entire application architecture must be built for independence.

2. **Self-Hosting Isn't the Answer** (15:22) - Self-hosting requires technical skills most users lack, and even skilled users don't want to run servers. It's a partial solution at best for the local-first vision.
```

### 4.3 Talk Structure

Compile section overview from Agent 2:

**Format:**
```markdown
1. **Introduction** (0:00) - Sets up the problem of cloud dependency
2. **Historical Context** (4:30) - Traces local-first from CRDTs to today
3. **Case Studies** (12:00) - Examines Skiff and other failures
4. **The Solution** (25:00) - Proposes commoditized sync infrastructure
5. **Q&A** (40:00) - Addresses audience questions
```

### 4.4 Notable Quotes

Select 3 quotes from Agent 3:

**Format:**
```markdown
> "Quote text here." (12:34)

> "Another powerful quote." (23:45)

> "Third memorable quote." (34:56)
```

Clean blockquotes with timestamps, no attribution needed (speaker is in frontmatter).

### 4.5 Who Should Watch

Use Agent 4's audience analysis (1-2 paragraphs):
- Professional context
- Problems they're trying to solve
- What they'll gain
- Prerequisites if any

### 4.6 Action Items

Use Agent 4's actionable takeaways:
- 3-5 concrete next steps
- Checkbox format for actionability
- Based on talk recommendations

---

## Phase 5: User Review (BLOCKING GATE)

**This is a mandatory approval step.** Present the generated content to the user before saving.

### 5.1 Present Content

Display the six generated sections in a formatted preview:

```markdown
## Preview of Enhanced Content

### Core Message
[Generated core message]

### Key Insights
[Generated 8-12 timestamped insights]

### Talk Structure
[Generated section overview]

### Notable Quotes
[3 timestamped quotes]

### Who Should Watch
[Generated audience description]

### Action Items
[Generated action items]
```

### 5.2 Request Approval

Use the `AskUserQuestion` tool:

```yaml
question: "Does this enhancement look good?"
header: "Review"
multiSelect: false
options:
  - label: "Save"
    description: "Add these sections to the talk note"
  - label: "Regenerate"
    description: "Try again with different focus"
  - label: "Edit"
    description: "Tell me what to change"
  - label: "Cancel"
    description: "Don't modify the note"
```

### 5.3 Handle Response

- **Save**: Proceed to Phase 6
- **Regenerate**: Return to Phase 3 with modified prompts
- **Edit**: Apply user feedback, show updated preview
- **Cancel**: Exit without changes

**Do NOT proceed to Phase 6 without explicit user approval.**

---

## Phase 6: Save Enhanced Note

### 6.1 Structure the Enhanced Content

Insert new sections after the opening paragraph, before existing headings:

```markdown
---
(existing frontmatter unchanged)
---

(existing opening paragraph preserved)

## Core Message

[Generated core message]

## Key Insights

1. **[Title]** (timestamp) - [Explanation]
2. **[Title]** (timestamp) - [Explanation]
...

## Talk Structure

1. **[Section]** (timestamp) - [Description]
2. **[Section]** (timestamp) - [Description]
...

## Notable Quotes

> "Quote 1 here." (timestamp)

> "Quote 2 here." (timestamp)

> "Quote 3 here." (timestamp)

## Who Should Watch

[Generated audience description]

## Action Items

- [ ] Action 1
- [ ] Action 2
- [ ] Action 3

---

(original body content preserved below)

## [Original sections]
...
```

### 6.2 Preserve Original Content

**Critical:** Never delete existing content:
- Keep all frontmatter fields
- Keep opening paragraph
- Keep all original `##` sections and their content
- Keep all wiki-links `[[slug]]`

The `---` separator clearly divides generated content from original notes.

### 6.3 Write the File

Use the Edit tool to insert the new sections at the correct position.

### 6.4 Confirmation

Report to user:
```markdown
Saved: content/{slug}.md
  - Core Message: [word count] words
  - Key Insights: [count] timestamped insights
  - Talk Structure: [count] sections
  - Notable Quotes: 3 quotes
  - Who Should Watch: added
  - Action Items: [count] items
  - Original content: preserved
```

---

## Phase 7: Quality Check

Run linter and type check to catch any issues:

```bash
pnpm lint:fix && pnpm typecheck
```

If errors are found, fix them before completing the task.

---

## Error Recovery

| Error | Recovery |
|-------|----------|
| Talk not found | List available talks with `type: talk` |
| Not a talk type | Inform user skill only works on talks |
| Transcript unavailable | Fall back to WebSearch analysis |
| Agent analysis fails | Retry with simplified prompts |
| User rejects content | Allow regeneration with feedback |
| No insights extracted | Try broader analysis or web research |

---

## Quality Checklist

Before saving, verify:
- [ ] Talk note exists and has `type: talk`
- [ ] Transcript was fetched (or web research fallback used)
- [ ] Core Message is under 50 words
- [ ] Generated 8-12 Key Insights with timestamps
- [ ] Each insight has bold title, timestamp, and explanation
- [ ] Talk Structure has 4-7 sections with timestamps
- [ ] 3 notable quotes with timestamps included
- [ ] Who Should Watch section is present
- [ ] Action Items has 3-5 concrete items
- [ ] Original content preserved
- [ ] User explicitly approved changes
- [ ] Markdown formatting is valid
