---
name: capture-triage
description: Processes Drafts Pro captures from the Inbox folder. Classifies by intent, shows preview for approval, routes to Ready as tasks. Use when triaging captures, processing mobile notes, or as part of daily review. Triggers on "triage captures", "process captures", "check my captures".
allowed-tools: Read, Glob, Grep, Edit, Write, AskUserQuestion
skills: mission-context
---

# Capture Triage

## What This Does

Turns mobile captures into actionable tasks in your Ready queue. Everything captured has
intent - this skill makes it explicit so task-clarity-scanner can decide what's important.

## Who It's For

Ed - capturing quick thoughts in Drafts Pro throughout the day.

## The Philosophy

> Everything captured has intent. Route to Ready, let task-clarity-scanner decide what
> moves to Someday/Maybe.

No passive filing. Every capture becomes a decision point.

---

## Paths

```
Inbox:      /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/
Processed:  /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/Processed/
Daily note: /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md
Projects:   /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/PROJECT - *.md
Contacts:   /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/CONTACT - *.md
```

---

## Important: Naming Clarification

| Term | What It Means |
|------|---------------|
| Inbox **folder** | `/Zettelkasten/Inbox/` - where Drafts Pro sends mobile notes |
| Captures **section** | `## Captures` in daily note - links to docs created today |
| Ready **destination** | `## Ready` section in daily note - where triaged tasks go |

**Remember:** This skill reads from the Inbox FOLDER and routes to the Ready SECTION.
Tasks go to Ready section only - Captures section is for document links.

---

## Instructions

### Step 1: Check Inbox Folder (Root Only)

**Important:** Only check files directly in Inbox/, NOT subdirectories.

```bash
ls /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/Inbox/*.md 2>/dev/null
```

If no files found: Report "No captures waiting" and stop.
If files found: Continue to Step 2.

### Step 2: Load Context

Pull active project names from mission-context skill AND:

```
Glob: /Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/PROJECT - *.md
```

Build a list of project names for matching.

### Step 3: Read and Classify Each Capture (Background OK)

**This step can run in background.** Read and classify all captures before surfacing to user.

For each `.md` file in Inbox:
1. Read full content
2. **Extract source URL from frontmatter** (see Step 3b)
3. Detect if already-processed (see Step 3a)
4. Classify by intent (see Step 4)

Surface to user only after ALL files are read and classified.

### Step 3b: Extract Source URLs

**For x-bookmark files** (filename starts with `x-`):
- Read `tweet_url` from YAML frontmatter
- This URL MUST be included when routing to Ready

**For other captures with URLs:**
- Check for `url:`, `source_url:`, or `link:` in frontmatter
- Check for markdown links `[text](url)` in body
- Preserve any URLs found for routing step

### Step 3a: Detect Already-Processed Content

If capture content looks like a summary (has structure, headers, quotes sources):
- Flag as `[PROCESSED]`
- Will suggest routing as REFERENCE
- Won't offer research-swarm (already researched)

**Signals of processed content:**
- Has markdown headers (##, ###)
- Contains bullet lists with structured info
- Quotes or attributes other sources
- Looks like notes from a video/article

### Step 4: Classify Each Capture

**Priority Rule:** Inline hints override auto-detection. Check for these FIRST:
- `IDEA:` or `Idea:` → IDEA
- `Research:` → RESEARCH (triggers swarm option)
- `for [Project Name]` → PROJECT_UPDATE
- `Task:` or `TODO:` → TASK

**Auto-Detection (if no inline hint):**

| Signal | Classification |
|--------|----------------|
| Starts with verb (call, email, buy, check, send, schedule) | TASK |
| Contains `Research:` hint or explicit question needing investigation | RESEARCH |
| "What if..." or speculative language | IDEA |
| Mentions active project name | PROJECT_UPDATE |
| Person's name + action context | CONTACT |
| Links, articles, saved content, observations | REFERENCE |

### Step 5: Show Classification Preview (Two-Step)

**Two-Step Pattern:** Show preview table first, then ask decision in a separate message.
Let user absorb the information before asking what to do.

---

#### Step 5a: Present the Table

Show what you found. Let user absorb the information first:

```
## Capture Triage Preview

Found [N] captures. Here's how I've classified them:

| # | File | Preview | Classification | Suggested Routing |
|---|------|---------|----------------|-------------------|
| 1 | note1.md | "Call dentist..." | TASK | Ready: Call dentist (MM-DD) |
| 2 | note2.md | "What if we..." | IDEA | Ready: Consider: [idea] (MM-DD) |
| 3 | summary.md | [PROCESSED] "Article about..." | REFERENCE | Ready: Review: [title] (MM-DD) |
| 4 | question.md | "Research: how do..." | RESEARCH | Spawn research-swarm? |
```

**Pause here.** Let the user see and absorb the table before asking for a decision.

---

#### Step 5b: Ask for Decision

After showing the table, ask ONE question using AskUserQuestion:

```
How would you like to proceed?

1. **Approve all** - Route everything as shown
2. **Go one-by-one** - Review each item individually
3. **Modify** - Change specific classifications before routing
4. **Skip all** - Don't process any captures right now
```

**Key points:**
- Show [PROCESSED] flag for already-summarized content
- RESEARCH items present in preview table with spawn option - user approves before spawning
- Let user approve, modify, or skip before any changes

### Step 6: Route by Classification

After approval, route each capture:

| Classification | Destination | Format |
|----------------|-------------|--------|
| TASK | Ready | `- [ ] [action] (MM-DD)` |
| IDEA | Ready | `- [ ] Consider: [idea] (MM-DD)` |
| REFERENCE | Ready | `- [ ] Review: [linked title](URL) - brief context (MM-DD)` |
| RESEARCH | If approved: spawn agent | See Step 7 |
| PROJECT_UPDATE | Project file | Timestamped append to `## Context Gathered` |
| CONTACT | Create note + Ready | `- [ ] Follow up with [Name] (MM-DD)` |

**IMPORTANT: Review tasks MUST include links.**

For REFERENCE items, always include the source link so Ed can find it:
- X bookmarks: `[Title](https://x.com/author/status/ID)`
- Articles: `[Article Title](URL)`
- Obsidian docs: `[[Document Name]]`
- YouTube: `[Video Title](URL)`

If a capture has no URL but references external content, note this: `(source needed)`

---

**Edit Instructions:**

For each item routed to Ready:
1. Open today's daily note at:
   `/Users/eddale/Documents/COPYobsidian/MAGI/Zettelkasten/YYYY-MM-DD.md`
2. Find the `## Ready` section
3. Use Edit tool to append the task in the format shown above
4. **Do NOT add to `## Captures`** - that section is for document links only

Example Edit operation:
```
old_string: "## Ready\n- [ ] existing task"
new_string: "## Ready\n- [ ] existing task\n- [ ] [new task from capture] (01-06)"
```

**If creating PROJECT or CONTACT files:** Those files get created separately, and a
LINK to them goes in Ready as a task (e.g., `- [ ] [[PROJECT - Name]] - brief desc`).

### Step 7: Handle Research (Only When Requested)

**Only spawn research-swarm if:**
- User explicitly approved during Step 5 preview
- Capture has `Research:` inline hint AND user confirmed

For each approved RESEARCH item:

```
Task(
  description="Research: [Topic]",
  prompt="Research question: [Full capture content]

  Use research-swarm pattern to investigate. Save findings to Zettelkasten.
  When complete, add review task to Ready: '- [ ] Review: [[Research - Topic]] (MM-DD)'",
  subagent_type="research-swarm",
  run_in_background=true
)
```

Add placeholder to daily note:
```
- [RESEARCH] [Topic] - swarm running in background
```

### Step 8: Handle Contacts

When a capture mentions a person with action context:

1. Check if `CONTACT - [Name].md` exists
2. If exists: Append to `## Interactions` section
3. If new: Create contact note using template
4. Always add follow-up task to Ready

**Contact Note Template:**

```markdown
---
type: contact
created: YYYY-MM-DD
source: capture-triage
---

# [Person Name]

## Context
[Original capture content]

## Interactions
- YYYY-MM-DD: Initial capture - [summary]

## Follow-up
[Any implied next steps]
```

### Step 9: Move to Processed

After routing each capture:

```bash
mv "[Inbox file]" "[Processed folder]"
```

Move files to Inbox/Processed/ as safety net (preserves originals).

### Step 10: Generate Triage Summary

```markdown
## Capture Triage - YYYY-MM-DD HH:MM

**Processed:** N items | **Research spawned:** M (if any)

### Routed to Ready
- [N] tasks
- [N] ideas (Consider:)
- [N] references (Review:)

### Research Running
- [Topic] - spawned at HH:MM

### Actions Taken
- Moved N files to Inbox/Processed/
- Created CONTACT - [Name].md (if any)
- Updated PROJECT - [Name].md (if any)
```

---

## Examples

### Example 1: Dry Run Preview

**Inbox folder contains 4 files:**

```
1. "Call dentist Monday about cleaning"
2. "What if we did a 5-day hook challenge?"
3. [PROCESSED] "Summary of Karpathy video - 6 paradigm shifts..."
4. "Research: how do successful coaches use AI?"
```

**Skill shows:**

```
## Capture Triage Preview

| # | Capture | Classification | Suggested Action |
|---|---------|----------------|------------------|
| 1 | "Call dentist..." | TASK | → Ready: "Call dentist Monday (01-05)" |
| 2 | "What if we..." | IDEA | → Ready: "Consider: 5-day hook challenge (01-05)" |
| 3 | [PROCESSED] "Summary of Karpathy..." | REFERENCE | → Ready: "Review: [Karpathy video](URL) - 6 paradigm shifts (01-05)" |
| 4 | "Research: how do coaches..." | RESEARCH | → Spawn research-swarm? |

Approve all, modify, or skip items?
```

### Example 2: After Approval

User approves all, including research swarm for #4.

**Result:**
- Ready gets 3 new tasks + 1 research placeholder
- Research-swarm spawns in background
- All 4 files moved to Processed/
- Summary generated

---

## Guidelines

- **Two-step preview** - Show table first, ask decision second (separate messages)
- **Ready, not Captures** - All triaged items become tasks in `## Ready` section
- **Dry run is standard** - Always show preview before routing
- **Respect inline hints** - They override auto-detection
- **Research-swarm is opt-in** - Ask before spawning
- **[PROCESSED] content** - Flag summaries, suggest REFERENCE routing
- **Everything to Ready** - Let task-clarity-scanner handle prioritization
- **Preserve originals** - Move to Processed/ folder as safety net
- **Review tasks need links** - Always include source URL or wikilink so Ed can find the content

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2025-01-05 | Initial build as inbox-triage |
| 2.0 | 2025-01-05 | Renamed to capture-triage, added dry run, AskUserQuestion flow, all routes to Ready |
| 2.1 | 2026-01-06 | Renamed folder Captures→Inbox, split Step 5 into two-step preview, explicit Ready section routing, background OK for classification |
| 2.2 | 2026-01-12 | Added requirement: Review tasks MUST include source links (URL or wikilink). Added Step 3b to extract URLs from frontmatter (especially x-bookmark tweet_url) |

---

## Notes & Learnings

- Day 1 test processed 32 captures with backlog - dry run prevented overwhelm
- [PROCESSED] detection helps avoid re-researching already-summarized content
- Research-swarm opt-in prevents runaway agent spawning
- Review tasks without links are useless - Ed can't find the content to review (added v2.2)
