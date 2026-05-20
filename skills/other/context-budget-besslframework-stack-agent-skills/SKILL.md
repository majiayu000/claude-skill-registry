---
name: context-budget
description: |
  Tracks approximate context window usage during a session. Reports estimates
  periodically and warns when approaching limits so you can summarize, compress,
  or hand off before losing important context to truncation.
user-invocable: true
allowed-tools:
  - Read
  - Bash
---

# Context Budget

Know when you are running out of room.

---

## Why This Exists

Claude Code sessions degrade silently. As the conversation grows, earlier messages get compressed or dropped. You do not get a warning. One moment the model remembers the architecture decision from message 5; the next moment it does not. By the time you notice, you have already lost context you needed.

This skill tracks how much of the context window has been consumed and tells you before things go wrong.

---

## Commands

### `/context-budget`

Show the current estimate: approximate tokens used, percentage of window consumed, number of files read, and a recommendation (keep going, start compressing, or hand off).

### `/context-budget reset`

Reset the internal tracking counters. Use this after a session-handoff load, when the effective context has been compressed.

---

## This Is Not a Tool

There are no scripts. No state files. No external dependencies. This skill is a set of instructions that changes how Claude behaves during the session. It adds awareness of consumption, not new capabilities.

---

## Tracking Rules

### What to count

Maintain a running mental estimate of token usage based on these rough heuristics:

| Content type | Estimate |
|---|---|
| User message (short, 1-2 sentences) | ~50 tokens |
| User message (paragraph) | ~200 tokens |
| User message (pasted code/error) | ~4 tokens per line |
| Assistant response (short) | ~100 tokens |
| Assistant response (long explanation) | ~500 tokens |
| Assistant response (code generation) | ~4 tokens per line generated |
| File read (via Read tool) | ~4 tokens per line read |
| Bash output | ~4 tokens per line of output |
| Tool call overhead | ~20 tokens per call |

These are rough. The point is order-of-magnitude awareness, not exact accounting.

### What to track

- Running token estimate
- Number of exchanges (user message + assistant response = 1 exchange)
- Number of files read (and approximate total lines)
- Number of large code blocks generated

---

## Reporting Schedule

### Every 10 exchanges

After every 10th exchange, append a brief status line at the end of the response:

```
[Context: ~45K tokens, ~35% used, 8 files read]
```

Keep it on one line. Do not make it a section or a heading. It should be easy to ignore if the user does not care.

### At 60% estimated usage

Add a note after the response:

```
[Context: ~78K tokens, ~60% used. Consider summarizing the conversation
so far or compressing context. Files read: 14]
```

Suggest specific actions:
- "The architecture discussion from earlier could be summarized into 2 sentences."
- "The 3 files read at the start of the session may no longer be relevant."

### At 80% estimated usage

Stronger warning:

```
[Context: ~104K tokens, ~80% used. Recommend running /session-handoff save
before context loss. Key decisions and progress should be captured now.]
```

At this point, also:
- List the key things that would be lost if context truncation happens
- Offer to run `/session-handoff save` immediately

### At 90%+ estimated usage

```
[Context: ~117K tokens, ~90% used. Session handoff strongly recommended.
Responses may start losing earlier context.]
```

Stop reading new files unless absolutely necessary. Each file read at this point accelerates context loss.

---

## Context Window Size Assumptions

Use 128K tokens as the assumed context window size. This is conservative; the actual limit depends on the model and configuration. Better to warn early than late.

If the user says their context window is a different size, adjust accordingly.

---

## File Read Tracking

Every time the Read tool is called, note:

1. The file path
2. Approximate lines read
3. Whether the file is still relevant to the current task

When reporting at the 60% threshold, list files that were read early in the session and might no longer be needed:

```
Files consuming context:
  src/components/Dashboard.tsx (~400 lines, read in exchange 2)
  src/api/routes.ts (~200 lines, read in exchange 3)
  package.json (~80 lines, read in exchange 1)

The Dashboard and routes files were read for the initial bug fix,
which is now complete. Their content is still in context but may
not be needed for the current task.
```

---

## Interaction with Other Skills

### session-handoff

At the 80% threshold, suggest `/session-handoff save` explicitly. If the session-handoff skill is available, reference it by name. If not, suggest the user manually note their progress.

### habit-formation

If habit-formation is active, suggest `/habit-formation save` before the session ends due to context limits. Patterns detected in this session should not be lost.

---

## What This Skill Does NOT Do

- It does not actually measure tokens. There is no API for that inside the conversation. Everything is an estimate.
- It does not truncate or compress the conversation. It only advises.
- It does not persist between sessions. The tracking resets when a new session starts.
- It does not slow down the session. The tracking happens in the background; the periodic reports are one line.

---

## Important Constraints

- Keep the periodic reports minimal. One line, end of response. The user came here to work, not to read context budgets.
- Never refuse to do work because of estimated context usage. Warn, then proceed if the user wants to continue.
- The estimates are rough. Do not present them with false precision. "~45K tokens" is fine. "44,892 tokens" is not.
- If the user says "I don't care about context budget," stop reporting. Respect the preference.
- After a `/context-budget reset`, restart all counters from zero. The user is telling you that prior context has been handled.
