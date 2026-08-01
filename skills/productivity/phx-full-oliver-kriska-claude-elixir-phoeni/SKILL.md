---
name: phx-full
description: Use for large features spanning multiple contexts or autonomous end-to-end
  implementation. Runs the full plan-implement-review-compound cycle with specialist
  agents. NOT for executing an existing plan file — use $phx-work for that.
---

# Full Phoenix Feature Development

Execute complete Elixir/Phoenix feature development autonomously: research patterns,
plan with specialist agents, implement with verification, Elixir code review.
Cycles back automatically if review finds issues.

## Usage

```
$phx-full Add user authentication with magic links
$phx-full Real-time notification system with Phoenix PubSub
$phx-full Background job processing for email campaigns --max-cycles 5
$phx-full Add magic-link auth --codex
```

**Wrong input guard**: if the argument is a path to an existing plan file
(`.claude/plans/*/plan.md`), do NOT re-plan it. Say so and run `$phx-work {path}`
instead — the plan phase already happened.

## Flags

- **`--codex`** — Codex CLI joins the review panel on **every** review
  cycle, matching `$phx-review --codex`.
- **Requires** the `codex` CLI. A missing CLI degrades to a SKIPPED note —
  the cycle never fails.
- **Consensus** findings (flagged by a Claude agent **and** codex) are
  marked HIGH CONFIDENCE.

## Workflow Overview

```
┌──────────────────────────────────────────────────────────────────┐
│                       $phx-full {feature}                        │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  │
│  │Discover│→ │  Plan  │→ │  Work  │→ │ Verify │→ │ Review │→ │Compound│→Done│
│  │ Assess │  │[Pn-Tm] │  │Execute │  │  Full  │  │4 Agents│  │Capture │     │
│  │ Decide │  │ Phases │  │ Tasks  │  │  Loop  │  │Parallel│  │ Solve  │     │
│  └───┬────┘  └────────┘  └────────┘  └───┬────┘  └────────┘  └────────┘     │
│       │                            ↑      │    ↑              │         │
│       ├── "just do it" ────────────┤      │    │              │         │
│       ├── "plan it" ──┐            │      ↓    │              │         │
│       │               ↓            │ ┌────────┐│              │         │
│       │     ┌──────────────┐       │ │Fix     ││ ┌─────────┐ │         │
│       │     │   PLANNING   │       │ │Issues  │└─│ Fix     │←┘         │
│       │     └──────────────┘       │ └───┬────┘  │ Review  │           │
│       │                            │     ↓       │ Findings│           │
│       │                       ┌────┴─────────┐   └────┬────┘           │
│       │                       │   VERIFYING   │←──────┘                │
│       └── "research it" ─────┘  (re-verify)                            │
│            (comprehensive plan)                                         │
│                                                                  │
│  On Completion:                                                  │
│  Auto-compound: Capture solved problems → .claude/solutions/     │
│  Auto-suggest: $phx-document → $phx-learn-from-fix                       │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

## State Machine

```
STATES: INITIALIZING → DISCOVERING → PLANNING → WORKING →
        VERIFYING → REVIEWING → COMPLETED → COMPOUNDING | BLOCKED
```

Save state in `.claude/plans/{slug}/progress.md` AND via Claude Code
tasks. Create one task per phase at start, mark `in_progress` on
entry and `completed` on exit:

```
TaskCreate({subject: "Discover & assess complexity", activeForm: "Discovering..."})
TaskCreate({subject: "Plan feature", activeForm: "Planning..."})
TaskCreate({subject: "Implement tasks", activeForm: "Working..."})
TaskCreate({subject: "Verify implementation", activeForm: "Verifying..."})
TaskCreate({subject: "Review with specialists", activeForm: "Reviewing..."})
TaskCreate({subject: "Capture solutions", activeForm: "Compounding..."})
```

Set up `blockedBy` dependencies between phases (sequential).

Run COMPOUNDING phase on COMPLETED to capture solved problems in `.claude/solutions/`.
Suggest `$phx-document` for docs and `$phx-learn-from-fix` for quick pattern capture.

## Cycle Limits

| Setting | Default | Description |
|---------|---------|-------------|
| `--max-cycles` | 10 | Max plan→review cycles |
| `--max-retries` | 3 | Max retries per task |
| `--max-blockers` | 5 | Max blockers before stopping |

Stop with INCOMPLETE status when limits exceeded. List remaining work and recommended action.

## Integration

```text
$phx-full = $phx-plan → $phx-work → $phx-verify → $phx-review → (fix → $phx-verify) → $phx-compound
```

Use Ralph Wiggum Loop for fully autonomous execution:

```bash
/ralph-loop:ralph-loop "$phx-full {feature}" --completion-promise "DONE" --max-iterations 50
```

## Iron Laws

1. **NEVER skip verification** — Every task must pass `mix compile --warnings-as-errors` before moving to the next. Run `mix test <affected>` per-phase, full suite only at final gate
2. **Respect cycle limits** — When `--max-cycles` is exhausted, STOP with INCOMPLETE status. Do not continue indefinitely hoping the next fix works
3. **One state transition at a time** — Follow the state machine strictly. Never jump from PLANNING to REVIEWING — each state produces artifacts the next state needs
4. **Discover before deciding** — Always run DISCOVERING phase to assess complexity. Skipping it for "simple" features leads to underplanned implementations
5. **Agent output is findings, not fixes** — Review agents report issues. Only the WORKING state makes code changes
6. **Skip redundant review agents** — In REVIEWING phase: skip
   verification-runner (work phase already verified), skip iron-law-judge
   if PostToolUse hooks verified all files. For <200 lines changed,
   spawn only elixir-reviewer + security-analyzer (if auth files)
7. **ZERO narration in autonomous mode** — This is a HARD rule, not
   a suggestion. NEVER write "Let me now...", "Now I need to...",
   "I'll now...", "Next, I will...", or any preamble before a tool
   call. Just call the tool. Only output text for: decisions that
   need explanation, errors, or phase transitions. If you catch
   yourself narrating, delete the text and just make the tool call.
   (Post-PR validation: 30% of messages still violated this — the
   instruction was too soft. This stronger wording is required.)

## References

- `references/execution-steps.md` — Detailed step-by-step execution
- `references/example-run.md` — Example full cycle run
- `references/safety-recovery.md` — Safety rails, resume, rollback
- `references/cycle-patterns.md` — Advanced cycling strategies
