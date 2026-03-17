---
name: meeting
description: Process meeting transcripts to extract reports, tasks, and memory. Handles "Process this meeting", action item extraction, meeting summaries. Calendar integration for scheduling context.
user-invocable: true
help:
  purpose: |-
    Process meeting transcripts with automatic extraction and calendar integration.
  use_cases:
    - "Process this meeting [transcript]"
    - "Extract action items from this meeting"
    - "Summarize this meeting"
  scope: meetings,transcripts,action-items
---

# Meeting processor protocol

Process meeting transcripts to extract structured reports, persist to journal, create tasks, and extract memory using a unified orchestrated pipeline.

---

## Pipeline overview

This skill combines transcript analysis, structured report generation, task extraction, memory persistence, and journal creation into a single coordinated workflow. Progress is tracked with real-time TodoWrite updates.

**Parallelization**: After the journal entry is saved (Step 3), task extraction (Step 4) and memory extraction (Step 5) run as **parallel sub-agents** using the Task tool. This yields a 30-40% wall-clock improvement on typical meetings. Both sub-agents read from the saved journal file, ensuring isolated context and no cross-contamination.

---

## Step 1: Process transcript (MANDATORY)

### 1.1: Load replacements (MANDATORY)

Read `reference/replacements.md` BEFORE processing any content. Apply canonical names to ALL text: frontmatter, prose, action items, task assignments.

### 1.2: Input handling

The transcript may be:
1. **Plain text** with speaker labels and timestamps
2. **JSON array** with `SPEAKER`, `LINE_TEXT`, `LINE_ID` fields

### 1.3: Calendar lookup (MANDATORY WHEN AVAILABLE)

Read `reference/integrations.md` Calendar section for provider details and status. If calendar integration is configured, query for this meeting if date/time can be inferred. Resolve the meeting date to `YYYY-MM-DD` format before querying. Execute the `list_events` operation with the meeting date and offset=1.

**Why:** Calendar provides full attendee list (including silent participants), official meeting title, organizer, and meeting notes/agenda. The attendee list is also critical for name resolution in Step 1.4.

**Extract:**
- Complete attendee list (for `participants` frontmatter and name resolution)
- Meeting time
- Organizer
- **Calendar meeting title** (authoritative source for filename and title)

If meeting not found or calendar integration is unreachable, proceed with transcript-only processing and note the gap.

### 1.4: Speaker name resolution (MANDATORY)

Apply the **name resolution protocol** (core skill, Memory protocol section):

1. For each speaker name in the transcript, check `reference/replacements.md` for an exact match
2. If a name is ambiguous (matches multiple canonical entries) or unknown (no match), attempt contextual resolution using:
   - Calendar attendees from Step 1.3 (primary source — narrows to people actually present)
   - Transcript context (role references, team mentions, topic expertise)
   - Memory people files (recent interactions, team membership)
3. If any names remain unresolved, batch ALL unresolved names into a single user clarification before proceeding
4. Identify the user from role references matching CLAUDE.md identity
5. NEVER use generic speaker labels ("Speaker 1") in output — resolve or ask

Build a name resolution table mapping each raw speaker label to its canonical form. Apply this table to all downstream steps (report, tasks, memory).

---

## Step 2: Generate structured report (MANDATORY)

Produce ALL of the following sections from the transcript analysis:

### Topics
- Discussion points as bullet points
- Infer meeting type but do NOT state it

### Updates
- Status updates from anyone OTHER than the user
- Be specific: names, projects, dates

### Concerns
- Risks raised with WHO, ISSUE, DEADLINE

### Decisions
- What was decided and who made the call

### Action items
Classify into:
- **For me**: Tasks the user committed to
- **For others**: Tasks assigned to specific people
- **Unassigned**: Needed but not assigned

Format: **"Owner"** -- Task description (deadline if stated)

---

## Step 3: Save to journal (MANDATORY)

Create file in `journal/YYYY-MM/`:

**Filename:** `YYYY-MM-DD-meeting-slug.md`

**Template:**
```yaml
---
date: YYYY-MM-DD
title: Meeting Title
calendar_title: Original Calendar Title  # Only if different from title
type: meeting
participants: [Name1, Name2, Name3]
organizer: Name  # From calendar if available
topics: [topic1, topic2]
initiatives: [Initiative1, Initiative2]
source: calendar | transcript  # Indicate primary data source
---
```

```markdown
# Meeting Title
**Date:** YYYY-MM-DD | **Participants:** [[Name1]], [[Name2]], [[Name3]]
**Initiatives:** [[Initiative1]], [[Initiative2]]

## Topics
[From report]

## Updates
[From report]

## Concerns
[From report]

## Decisions
[From report]

## Action items
[From report]
```

### Title and slug generation

**Title priority hierarchy:**
1. **Calendar meeting title** (authoritative source when available)
2. **Transcript header/title** (fallback when no calendar data)
3. **Context-inferred title** (last resort, based on content analysis)

**Slug rules:**
- Lowercase, hyphenated
- Remove filler words
- Example: "MCP Planning Session" -> `mcp-planning`

When calendar title is used, if it differs significantly from transcript context, keep `calendar_title` in frontmatter for reference.

---

## Steps 4 and 5: Parallel sub-agent execution (MANDATORY)

After saving the journal entry in Step 3, spawn **two parallel sub-agents** using the Task tool. Both sub-agents run concurrently, reading from the saved journal file path rather than from the raw transcript in context.

**Launch both sub-agents in a single message** using multiple Task tool calls. Do NOT wait for one to complete before starting the other.

### Sub-agent A: Task extraction

Spawn a Task sub-agent with the following prompt structure:

```
You are extracting tasks from a meeting journal entry.

Read the journal file at: {journal_file_path}
Read the task integration config at: reference/integrations.md (Tasks section)

For each action item in the journal:
1. Apply accountability test (NEVER create tasks for "Team" or "We" without a specific lead)
2. Check for duplicates: execute the task integration `list` operation for all configured lists
3. Resolve metadata:
   - Map relative dates to YYYY-MM-DD using date resolution
   - Default to `backlog` if no due date
   - Source: {journal_file_path}
4. Execute the `add` operation via the task integration with metadata in notes field
5. Check each tool response. Only add to tasks_created if the response confirms success.
   If the response indicates failure, add to errors[].
6. Place in appropriate list based on owner and due date:
   - Has due date + owner is user -> `Active` list
   - Has due date + owner is other -> `Delegated` list
   - No due date -> `Backlog` list

After all creation attempts, execute `list_reminders` for each list that received
new tasks. Verify each task appears by matching title. Add any tasks that were
reported as created but are missing from the list to the "creation_unverified" array.

NEVER populate tasks_created based on intent. Only include tasks confirmed present
in the verification query.

Return a JSON summary of tasks created:
{
  "tasks_created": [
    {"title": "...", "owner": "...", "list": "...", "due": "..."}
  ],
  "creation_unverified": [],
  "duplicates_skipped": [...],
  "errors": [...]
}
```

Standard task creation fields:
```
title: "Task description"
list: Active
due: YYYY-MM-DD
notes: |
  source: journal/YYYY-MM/YYYY-MM-DD-slug.md
  created: YYYY-MM-DD
  initiative: [[Initiative Name]]
  owner: Name
```

### Sub-agent B: Memory extraction

Spawn a Task sub-agent with the following prompt structure:

```
You are extracting durable memory from a meeting journal entry.

Read the journal file at: {journal_file_path}
Read memory indexes: memory/people/_index.md, memory/initiatives/_index.md, memory/decisions/_index.md
Read reference/replacements.md and apply canonical names.
If the main agent provided a name resolution table, use those resolved names.

Apply durability test to insights from the meeting:
- Stakeholder updates -> memory/people/{name}.md
- Initiative updates -> memory/initiatives/{name}.md
- Decisions -> memory/decisions/{slug}.md
- Update relevant _index.md files

Do NOT persist: scheduling logistics, temporary blockers, action items.

BEFORE writing any [[wikilink]] in a memory file, verify the referenced entity exists
in one of the memory indexes read above. If the entity does NOT exist in any index,
do NOT fabricate the wikilink. Instead, write the name as plain text and note it in
the "skipped" array with reason "unverified entity reference".

Return a JSON summary of memory updates:
{
  "created": [{"path": "...", "summary": "..."}],
  "updated": [{"path": "...", "summary": "..."}],
  "skipped": [{"insight": "...", "reason": "failed durability test"}]
}
```

### Collecting sub-agent results

After both sub-agents complete, collect their results and merge into the output summary. If either sub-agent fails:
- Log the failure in the output summary
- Do NOT retry automatically (the user can re-run the failed step manually)
- The other sub-agent's results are still valid and should be reported

### Sub-agent input/output contracts

| Sub-agent | Input | Output | Failure mode |
|-----------|-------|--------|-------------|
| Task extraction | Journal file path, integrations.md Tasks section, replacements.md | JSON: tasks created, creation unverified, duplicates skipped, errors | Report errors in summary, do not block memory extraction |
| Memory extraction | Journal file path, memory indexes, replacements.md | JSON: files created, files updated, insights skipped | Report errors in summary, do not block task extraction |

**Shared constraints for both sub-agents:**
- Read from the saved journal file, NEVER from raw transcript context
- Read `reference/replacements.md` and apply canonical names
- Each sub-agent operates with isolated context (no shared state)
- Neither sub-agent should modify the journal file
- Memory extraction must use `.lock` files when writing shared memory files (see core skill cowork protocol)

---

## Step 6: Replacement verification (MANDATORY)

Scan ENTIRE output for any terms from `reference/replacements.md` that were not replaced. Correct before saving.

### Auto-add unknown names

When processing transcripts, if new names are found that:
- Are not in `reference/replacements.md`
- Appear to be nicknames, abbreviations, or informal names (e.g., "Mick", "JT", "Dan")

Add them to `reference/replacements.md` with a placeholder for the user to complete:

```markdown
| Mick | ?? (needs full name) |
| JT | ?? (needs full name) |
```

This allows the user to update canonical names as needed without losing track of unknown references. Report these additions in the output summary.

---

## Output summary

End your response with:

```markdown
---
## Meeting context
Created: `journal/YYYY-MM/YYYY-MM-DD-meeting-slug.md`

## Task updates
| Operation | Task | Details |
|-----------|------|---------|
| Created | Task description | Owner, due date, destination |

## Memory updates
| Action | File | Summary |
|--------|------|---------|
| Created/Updated | `memory/path/file.md` | What changed |

## Summary
- Journal entry created (file path)
- Tasks created (count by list)
- Memory entries created or updated (count by category)
- Any warnings or gaps (e.g., names not in replacements.md, calendar lookup failed)
```

---

## Progress tracking (TodoWrite)

Use the `TodoWrite` tool to give the user real-time visibility into pipeline progress. Create the todo list at the start and update as steps complete:

```
1. Process transcript and generate structured report     [in_progress → completed]
2. Save journal entry                                    [pending → completed]
3. Extract tasks (parallel sub-agent)                    [pending → completed]
4. Extract memory (parallel sub-agent)                   [pending → completed]
5. Replacement verification                              [pending → completed]
6. Compile and return summary                            [pending → completed]
```

**Parallelization note**: Steps 3 and 4 run concurrently. Mark BOTH as `in_progress` when spawning the sub-agents. Mark each `completed` as its sub-agent returns. If one sub-agent completes before the other, update its status immediately without waiting for the other.

Mark each step `in_progress` before starting it and `completed` immediately after. If a step fails, keep it as `in_progress` and add a new todo describing the issue.

---

## Context management

For long transcripts (>30 minutes or >5,000 words), offload intermediate results to files rather than keeping everything in context:

1. After Step 3 (save to journal), the journal file path becomes the canonical source for all subsequent steps
2. Both parallel sub-agents (task extraction and memory extraction) read from the saved journal file, NOT from the raw transcript in context
3. Each sub-agent operates in isolated context via the Task tool, which naturally prevents context overflow
4. The main agent only needs to hold the journal file path and the sub-agent results for the final summary

This architecture means transcript length has minimal impact on Steps 4-5 performance, since sub-agents load only the structured journal output.

---

## Context budget
- Memory: Read `_index.md` + up to 5 targeted files
- Tasks: Execute task integration `list` operation for all configured lists (duplicate check)
- Calendar: Execute calendar integration `list_events` operation for meeting metadata
- Reference: `reference/replacements.md` (mandatory)

---

## Absolute constraints

- NEVER skip any of the 6 core steps
- ALWAYS return a summary (even if some steps failed)
- ALWAYS preserve the source transcript metadata in journal frontmatter
- NEVER skip any of the 5 report sections
- NEVER use generic speaker labels
- NEVER skip saving to journal
- NEVER skip creating tasks from action items
- NEVER omit the replacement verification step
- NEVER output names that appear in replacements.md without using canonical form
