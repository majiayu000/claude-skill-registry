---
name: step1
description: "ONLY when user explicitly types /step1. Never auto-trigger on think, scan, consider, or examine."
---

# /step1 - Explore → Interrogate → Bridge

Structured Q&A that converges on decisions. Questions evolve based on answers.

## Arguments

- `/step1` — asks "What needs solving?"
- `/step1 <topic>` — skips opening question
- `/step1 resume` — finds last decision tracker in conversation, continues

## Flow

### 1. EXPLORE

1. Read relevant codebase files (5-10). For greenfield projects, ask about constraints instead.
2. Identify decision points. Form an opinion on each from codebase evidence.
3. Output: `"~N decisions to work through (some will be auto-decided)"`

### 2. INTERROGATE

One question at a time via `AskUserQuestion`.

**Auto-decide** when:
- Codebase evidence makes one option overwhelmingly correct
- LLM-readability clearly favors one option (naming, structure, indirection) — still ask, but put the best option first with `(Recommended)` and include the rationale so the user can confirm quickly

Present initial auto-decisions as a batch before the first human question:

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

**Park** (user types via Other): Stop. Output tracker as-is. Write `_step1_decisions.md` with `## Unresolved` section. Do NOT suggest `/step2`.

### 3. BRIDGE

**Early resolution** — ONLY when outcome is a single localized fix (one file, no conventions, no docs):
- Skip `_step1_decisions.md`, summarize inline. Simple enough to implement directly — no pipeline needed.
- After the summary, ask: "Ready to implement? I can do this directly." Do NOT suggest `/step2` — early resolution bypasses the pipeline entirely.
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
`Rejected` and `Risks` exist so /step2 can convert them into guardrails. One line each. Omit if genuinely empty.
2. Ask "Anything you'd change?" — apply changes if requested.
3. **MANDATORY: Write `_step1_decisions.md`** at repo root using the Write tool. Do this BEFORE any closing remarks. This file is the primary deliverable — without it, /step1 failed.
4. Only AFTER the file is confirmed written, end with: `Next: /step2 to plan the implementation. Tip: /clear first so /step2 gets a full context window.`

## Rules

- **NEVER use Task or EnterPlanMode.** This skill IS the exploration framework. Subagents lose your context. Plan mode hijacks your flow. Read/Glob/Grep directly.
- No implementation. Only output is `_step1_decisions.md`. Exception: early resolution.
- One question at a time. Never batch.
- Never auto-chain to `/step2`.
- Recommend, warn, push back, challenge.
- **Take sides.** When one option is obviously better for LLM development (explicit names, less indirection, flatter structure), lead with it as `(Recommended)` with rationale. Still ask — but make the right choice effortless to confirm.
- **Gate: file before farewell.** Never mention `/step2` or signal completion until `_step1_decisions.md` has been written with the Write tool in the current conversation. The file is proof the skill finished. No file = skill failed.
