---
name: a
description: "Trigger: /a. Never auto-trigger on think, scan, consider, or examine."
---

# /analyze - Explore → Interrogate → Bridge

Structured Q&A that converges on decisions. Questions evolve based on answers.

## Arguments

- `/analyze` — asks "What needs solving?"
- `/analyze <topic>` — skips opening question
- `/analyze resume` — finds last decision tracker in conversation, continues

## Flow

### 1. EXPLORE

1. Read relevant codebase files (5-10). For greenfield projects, ask about constraints instead.
2. Identify decision points. Form an opinion on each from codebase evidence.
3. Output: `"~N decisions to work through (some will be auto-decided)"`

### 2. INTERROGATE

One question at a time via `AskUserQuestion`.

**Auto-decide** when codebase evidence makes one option overwhelmingly correct. Present initial auto-decisions as a batch before the first human question:

```
### Auto-decided (review before we continue)
1. ✅ (auto) [topic]: [answer] — [rationale]
```

Ask: "Want to revisit any of these, or move on?" If flagged, convert to regular question.

**Questions:**
- Order options by recommendation strength (best first)
- All option slots are for real answers — user can type "go back" or "park" via Other

**After each answer:**
- Reassess: does this reveal new decisions (mark `🆕`), kill existing ones (mark `➖`)?
- Flag conflicts with previous decisions
- Push back on risky choices even if user seems confident
- If decisions exceed 8, suggest splitting the task before continuing
- Output tracker:

```
### Decisions (N decided, ~M remaining)
1. ✅ [topic]: [answer] — [why]
2. ✅ (auto) [topic]: [answer] — [rationale]
3. ⬜ [next]...
```

**Go back** (user types via Other): Re-ask previous question, mark it ⬜, re-evaluate downstream.

**Park** (user types via Other): Stop. Output tracker as-is. Write `decisions.md` with `## Unresolved` section. Do NOT suggest `/b`.

### 3. BRIDGE

**Early resolution** — ONLY when outcome is a single localized fix (one file, no conventions, no docs):
- Skip `decisions.md`, summarize inline. Simple enough to implement directly — no pipeline needed.
- Question count is irrelevant. 1 human question + multi-file scope = full bridge.

**Full bridge** — default path (multi-file, conventions, or docs):

1. Present decision block(s):
```
## Decision: [topic]
**Approach:** [what and how]
**Why:** [codebase-grounded reasons]
**Rejected:** [alternative] — [why it fails]; ...
**Risks:** [trade-offs and pitfalls carried by chosen approach]
**Scope:** [in/out]
**Key decisions:**
- [decision]
```
`Rejected` and `Risks` exist so /b can convert them into guardrails. One line each. Omit if genuinely empty.
2. Ask "Anything you'd change?" — apply changes if requested.
3. **Write `decisions.md`** at repo root. This is the primary deliverable. Never skip it on the full bridge path.
4. Suggest: "Run `/b` in a fresh session."

## Rules

- No implementation. Only output is `decisions.md`. Exception: early resolution.
- One question at a time. Never batch.
- Never auto-chain to `/b`.
- Recommend, warn, push back, challenge.
