---
name: handoff
description: "Session handoff — compress current context into a structured prompt for seamless continuation in a new session. Use when: switching sessions, running low on context, or needing to hand off work."
---

# Session Handoff

Compress the critical context from the current conversation into a prompt so the user can paste it into a new session and the new AI can pick up the work immediately.

## The Problem

Long sessions accumulate cache tokens that slow responses and drain quota. But starting a new session cold loses all conversation context.
This skill solves: **compress context, don't lose context.**

## Execution Steps

### Phase 1: Retrospective Scan

Scan back through the entire conversation history in sequence. Early context is easily lost to attention decay or compression truncation — **scan from the beginning forward**, don't rely only on recent memory.

Tag each piece of information with a priority:
- **P0 (must include)**: information that, if lost, would cause the new session to make errors, redo work, or violate user intent
- **P1 (should include)**: improves efficiency and avoids detours, but not fatal if lost

P0 criteria: user instructions and corrections, incomplete task state, key decisions and ruled-out alternatives, known pitfalls.
P1 criteria: technical details, supporting context, reference resources, details of already-completed items.

### Phase 2: Organize Output

Organize content according to the extraction checklist and output format below. Keep all P0 items; include P1 items based on total handoff length.

### Phase 3: Self-Verification

Before output, go through the extraction checklist item by item:

- [ ] Every independent task/workflow in the conversation is covered?
- [ ] All user instructions and corrections are listed individually?
- [ ] Key decisions include both "why" and "what was ruled out"?
- [ ] Known pitfalls are recorded? (not just failed approaches, but also environment constraints and unexpected behaviors)
- [ ] Next steps are specific enough to execute immediately?
- [ ] Any important understanding built during the conversation not covered by any section?

For low-confidence items (fuzzy on details, uncertain if complete), annotate the entry with `[⚠ Please confirm with user]`.

### Phase 4: Delivery Confirmation

Output the handoff, then ask the user to confirm.

## Extraction Checklist

**P0 items must be listed individually — no omissions, no merging. P1 items may be condensed when handoff exceeds 4000 tokens.**

### Tasks and Progress

If the conversation involved multiple independent workflows, **group by workflow** — don't flatten everything into one linear list.

Each workflow includes:
- **Task goal**: what's being done and why
- **Current state**: how far along, what's done, what's not
- **Next step**: what the new session should do next (written as a directly executable instruction)

### User Instructions Given in This Session [P0]

This is the information most easily lost when switching sessions. List each one individually, **preserve the original wording**:
- **Response requirements**: tone, format, style, "always do X", "never do Y"
- **Behavioral corrections**: directions the user corrected, reasons for redirects
- **Explicit preferences and decisions**: which option was chosen, why, what was ruled out

### Shared Understanding Built in This Conversation [P0]

Understanding that developed gradually through the conversation and no longer needs to be re-explained by either party. This is the tacit knowledge most likely to be missing in a new session:
- **Codebase understanding**: "Module X behaves differently from the docs — what it actually does is…", "API Y has constraint Z"
- **Problem understanding**: root cause judgment reached through discussion, clarified requirements
- **Solution evolution**: how the final approach evolved (A → found problem → switched to B → added constraint C → final solution D)

Record not just the "conclusion" but "why that conclusion."

### Working Context

- **Working directory and relevant files**: path + status of each file (modified/created/pending) + what changed
- **Key decisions and rationale**: what choices were made, why, **which alternatives were ruled out and why**
- **Known pitfalls**: failed approaches, environment constraints, routes to avoid, unexpected behaviors
- **Technical details** [P1]: architecture, dependencies, versions, special configuration

### Unresolved Items

- **Open questions**: unanswered questions, items pending confirmation
- **External resources** [P1]: referenced documentation, URLs, APIs

## Output Principles

- **Verbatim**: user instructions, corrections, and preferences are quoted word-for-word — not paraphrased or summarized. The new session needs to "hear" the user's actual voice, not the AI's interpretation
- **Concrete not abstract**: write file paths, function names, commands, error messages — not "some file" or "that bug"
- **Executable**: "Next step" must be written so the AI in the new session can act on it immediately
- **Don't copy file contents**: record paths and key findings only — don't paste entire files
- **Self-contained**: the handoff must stand alone. The new session should be able to function normally with only this handoff, without depending on any external state. All important context must be included (repeated items can be summarized in one line, but must not be omitted). Reason: this handoff may be pasted into any AI environment (Claude.ai, ChatGPT, other tools) — not just Claude Code. Do not assume the new session has a memory system, CLAUDE.md, or any persistence mechanism

## Output Format

Output a single markdown code block with the following structure. Sections only appear when they have content:

````
# Session Handoff — {YYYY-MM-DD}

## Background
{One or two sentences describing the task and motivation}

## Working Directory
{Project path}

## Progress

### Workflow A: {Name} (omit grouping if only one workflow)
**Completed**
- {Specific completed items, with file paths}

**In Progress / Pending**
- {Incomplete items, with current state and where things are stuck}

**Next Step**
{Written as a directly executable instruction}

### Workflow B: {Name}
...

## Shared Understanding
(Key understanding built during the conversation — missing this would cause incorrect judgments in the new session)
- {Understanding}
- {Solution evolution}: A (failed because X) → B (constrained by Y) → final C

## Key Decisions
- {Decision} — Because: {reason} — Ruled out: {alternatives and why}

## Relevant Files
| File | Status | Notes |
|------|--------|-------|
| {path} | modified/created/pending | {what was done or needs to be done} |

## Known Pitfalls
- {Failed approach or route to avoid} — Reason: {why it failed}

## User Instructions
(Listed individually, verbatim, no merging, no omissions)
- Response style: "{exact words}"
- Behavioral correction: "{exact words}" — Context: {why this correction was given}
- Preference/decision: "{exact words}"

## Unresolved
- {Items pending confirmation or still unanswered}
````

## Length Management

| Estimated handoff length | Strategy |
|---|---|
| < 2000 tokens | Expand everything, no condensing needed |
| 2000–4000 tokens | Keep all P0, condense P1 to one-line summaries |
| > 4000 tokens | Keep all P0, include only P1 items needed for the new session's first step, omit the rest and note "see {file path}" |

If keeping only P0 still exceeds 6000 tokens, compress completed workflows to a one-line summary ("Completed X — see git log") and reserve space for in-progress and pending work.

## Supplemental Behavior

- After producing the handoff, explicitly flag low-confidence items and ask: "The above is the complete handoff — anything missing?"
- If a plan or task list was produced during the conversation, integrate it into "Progress" and "Next Step"
- If the user gave more than 3 instructions during the conversation, add a line at the end of the handoff: "The above contains N user instructions — all listed."
- **(Claude Code environment only)** If the conversation contains feedback or project context worth persisting that hasn't been written to memory yet, **write it to memory first, then produce the handoff**. The handoff is one-time; memory is the persistent layer across sessions. Ignore this step in non-Claude Code environments.
