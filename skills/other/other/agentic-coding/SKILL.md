---
name: Agentic Coding
slug: agentic-coding
version: 1.0.0
homepage: https://clawic.com/skills/agentic-coding
description: Ship production code with AI agents through acceptance contracts, micro diffs, red green loops, and deterministic handoff checkpoints.
changelog: Initial release with PACT protocol, contract templates, and handoff-first delivery workflow.
metadata: {"clawdbot":{"emoji":"AI","requires":{"bins":["git"]},"os":["linux","darwin","win32"]}}
---

## Setup

If `~/agentic-coding/` does not exist or is empty, read `setup.md`, ask a concise kickoff question, and keep any persistence explicitly opt-in.

## Positioning

This skill is intentionally different from `agentic-engineering` and `vibe-coding`:
- `agentic-engineering` focuses on multi-agent operating patterns and team throughput.
- `vibe-coding` focuses on prompt-led exploration and fast idea shipping.
- `agentic-coding` focuses on contract-first implementation, proof of fix, and reviewer-ready handoff.

## When to Use

User needs merge-ready code from an AI agent with explicit quality gates. Use for production features, risky refactors, bug fixes with reproducible failures, and Xcode-centered work such as Swift feature delivery, iOS/macOS regressions, and release-branch hotfixes.

## Architecture

Memory lives in `~/agentic-coding/`. See `memory-template.md` for setup.

```text
~/agentic-coding/
|- memory.md       # Persistent preferences and operating mode
|- contracts.md    # Accepted task contracts and non-goals
|- evidence.md     # Test evidence and verification snapshots
`- handoffs.md     # Delivery notes and rollback hints
```

## Quick Reference

Load these files on demand to keep context focused and execution fast.

| Topic | File |
|-------|------|
| Setup process | `setup.md` |
| Memory template | `memory-template.md` |
| PACT loop | `protocol.md` |
| Contract prompts | `prompt-contracts.md` |
| Merge handoff checklist | `handoff.md` |

## Core Rules

### 1. Lock a Contract Before Writing Code
Start every task with a compact contract:
- Objective: exact outcome in one sentence
- Acceptance: checks that prove success
- Non-goals: what must stay untouched
- Constraints: stack, style, limits, deadlines

No contract, no code.

### 2. Run the PACT Loop
Use the same execution loop every time:
1. **P**roblem framing: restate objective and assumptions
2. **A**cceptance design: define checks before edits
3. **C**hange set: produce the smallest useful diff
4. **T**race and test: show evidence and residual risk

This skill is execution discipline, not brainstorming.
For Xcode workflows, tie acceptance to a concrete target, simulator/device, and test command before editing.

### 3. Keep Diffs Surgical
One user objective maps to one focused change set:
- Prefer file-local edits over broad rewrites
- Separate behavior change from style cleanup
- Avoid hidden side effects outside declared scope

If scope grows, split into a second contract.

### 4. Prove Failure Then Prove Fix
For bugs and regressions:
- Capture the failing condition first (test, log, or reproduction)
- Apply minimal fix
- Re-run the same check to prove resolution

Never claim fixed without before and after evidence.

### 5. Deliver Handoff-Grade Output
End each cycle with a delivery packet:
- What changed and why
- Files touched and blast radius
- Validation run and results
- Known risks and rollback path

If handoff is unclear, the task is not finished.

### 6. Escalate With a Structured Fallback
When blocked after two failed attempts:
- Stop editing
- State what was tried
- Propose two grounded alternatives
- Request a decision with tradeoffs

Do not keep guessing in loops.

## Common Traps

- Starting implementation without acceptance checks -> endless iteration and unclear done state.
- Asking the agent for full rewrites -> noisy diffs and avoidable regressions.
- Mixing feature work with architecture overhaul -> weak reviewability and hard rollback.
- Reporting success without reproducible evidence -> false confidence in production.
- Treating AI output as final draft -> quality debt moved to code review.

## Security & Privacy

**Data that leaves your machine:**
- None from this skill itself

**Data that stays local:**
- Contracts, evidence notes, and handoff summaries in `~/agentic-coding/`

**This skill does NOT:**
- Trigger undeclared network requests
- Access files outside its own memory path
- Write to global or platform memory stores
- Auto-approve risky code without explicit evidence

## Scope

This skill ONLY:
- Improves execution quality of AI-assisted coding
- Enforces contract driven implementation and verification
- Produces clear handoff packets for reviewers

This skill NEVER:
- Replaces security review for high risk domains
- Encourages blind trust in generated code
- Overrides project specific contribution rules

## Related Skills
Install with `clawhub install <slug>` if user confirms:
- `agentic-engineering` - Multi-agent collaboration and operating patterns.
- `coding` - General coding support across stacks and tasks.
- `code` - Broad code authoring and editing assistance.
- `copilot` - Companion style IDE assistance patterns.
- `delegate` - Structured task delegation to autonomous agents.

## Feedback

- If useful: `clawhub star agentic-coding`
- Stay updated: `clawhub sync`
