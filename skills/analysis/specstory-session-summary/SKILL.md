---
name: specstory-session-summary
description: Summarize recent SpecStory AI coding sessions in standup format. Use when the user wants to review sessions from .specstory/history, prepare for standups, track work progress, or understand what was accomplished.
metadata:
  author: SpecStory
  version: "1.0"
---

## Context

You will analyze recent SpecStory session history files to provide a standup-style summary.

Argument provided: `$ARGUMENTS` (default: 5 sessions, or "today" for today's sessions only)

## Your Task

### Step 1: Find Recent Sessions

First, check if the SpecStory history folder exists and list recent session files:

```zsh
ls -t .specstory/history/*.md 2>/dev/null | head -20
```

**If no `.specstory/history` folder exists or it's empty**, respond with:

> No SpecStory session history found in this directory.
>
> SpecStory automatically saves your AI coding sessions for later reference. To start recording your sessions, install SpecStory from https://specstory.com

Then stop - do not proceed with the remaining steps.

**If sessions are found**, continue with the analysis. If the argument is "today", filter to today's date. Otherwise use the number provided (default 5).

### Step 2: Read and Analyze Each Session

Session files can be very large and may contain multiple user requests. Use this chunked reading strategy:

**Step 2a: Understand the session structure**

First, grep for all user message markers to see the session's scope:
```
grep -n "_\*\*User\*\*_" <file> | head -10
```

This shows line numbers of user messages, helping you understand:
- How many distinct requests were made
- Where to read for each request's context

**Step 2b: Read strategically based on structure**

1. **Beginning (first 500 lines)** - Read with `offset=0, limit=500`
   - Captures the initial request even if it includes pasted code/logs
   - May include early assistant responses showing the approach taken

2. **End (last 300 lines)** - Use `tail -300 <file>` via Bash
   - Contains the final outcome and conclusion
   - Shows whether tasks were completed or left pending

3. **File operations** - Grep for modifications:
   ```
   grep -E "(Edit|Write)\(" <file>
   ```

**Step 2c: For multi-request sessions**

If the grep in 2a shows multiple user messages at distant line numbers (e.g., lines 50, 800, 1500), this indicates multiple distinct tasks. For these sessions:
- Read around each user message line number (e.g., `offset=795, limit=100`)
- Summarize the 2-3 main tasks rather than just the first one

**Extract this information:**

1. **Goal(s)**: The user's request(s) from `_**User**_` blocks
   - For single-task sessions: one main goal
   - For multi-task sessions: list the 2-3 primary tasks
2. **Outcome**: Determine from the end of the conversation:
   - ✅ Completed - task was finished successfully
   - 📚 Research - information gathering, no code changes
   - 🔧 In Progress - work started but session ended mid-task
   - ❌ Abandoned - user changed direction or gave up
   - 🚧 Blocked - ended with unresolved error or blocker
3. **Files**: Modified files from Edit/Write tool uses (extract filenames only)
4. **Key decisions**: Look in the conversation for:
   - Explicit choices ("decided to", "chose", "instead of")
   - Trade-off discussions
   - Architecture or design conclusions

### Step 3: Format Output

Present each session as:

```
### {YYYY-MM-DD HH:MM} - {Brief Title from Main Goal}
**Goal**: {1 sentence summarizing what user wanted}
**Outcome**: {emoji} {Brief result description}
**Files**: {comma-separated list, or "None" if research only}
**Key insight**: {Notable decision or learning, if any}
```

For multi-task sessions, adjust the format:

```
### {YYYY-MM-DD HH:MM} - {Overall Theme or Primary Task}
**Tasks**:
  1. {First task} - {outcome emoji}
  2. {Second task} - {outcome emoji}
**Files**: {comma-separated list}
**Key insight**: {Notable decision or learning, if any}
```

### Step 4: Summary Section

After all sessions, add:

```
---
**Patterns**: {Note any recurring themes, files touched multiple times, ongoing work}
**Unfinished**: {Any sessions that ended with TODOs, blockers, or incomplete work}
```

## Guidelines

- Keep each session summary to 5-6 lines maximum (slightly more for multi-task sessions)
- Infer the title from the user's goal, not the filename
- For files, prefer showing just the filename, not full paths
- Skip sessions that are just quick questions with no real work
- For multi-task sessions, summarize up to 3 main tasks; group minor tasks as "various small fixes"
- Be concise - this is for quick daily review, not detailed documentation
- If a file read fails or is too large, work with what you can extract; don't skip the session entirely

## Example Output

```
## Session Summary (Last 3 Sessions)

### 2025-10-18 11:42 - Investigate Chat CRDT Storage
**Goal**: Understand why chat index CRDT doesn't contain the thread
**Outcome**: 📚 Explained dual storage design for offline/online sync
**Files**: threads.json, crdt-debug/4X/, crdt-debug/aT/
**Key insight**: Two storage layers (CRDT + JSON) serve different sync scenarios

### 2025-10-18 11:09 - Address Code Review Comments
**Goal**: Fix clarity issues from code review
**Outcome**: ✅ Refactored normalizeChatIndexDoc function
**Files**: chat.go, automerge-bridge.js
**Key insight**: Replaced complex normalization with toPlainString helper

### 2025-10-11 14:30 - Automerge Architecture Deep Dive
**Goal**: Document how Automerge docs are constructed temporally
**Outcome**: 📚 Research complete, walkthrough provided
**Files**: automerge-bridge.js, document.go (read only)

---
**Patterns**: 3 sessions focused on CRDT/chat subsystem; automerge-bridge.js touched repeatedly
**Unfinished**: None detected
```
