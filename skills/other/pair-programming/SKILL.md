---
name: pair-programming
description: "Collaborative coding with enforced micro-steps and user-paced control."
user-invocable: false
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
routing:
  triggers:
    - "pair program"
    - "collaborative coding"
    - "micro-steps"
    - "step by step coding"
    - "one change at a time"
    - "show each change"
    - "walk me through"
    - "interactive coding"
  category: process
  pairs_with:
    - test-driven-development
    - subagent-driven-development
---

# Pair Programming Skill

Collaborative coding through the **Announce-Show-Wait-Apply-Verify** micro-step protocol. The user controls pace, sees every planned change as a diff, and confirms before any file is modified. Works with any domain agent as executor.

This skill runs in the main session (not `context: fork`) because every step requires an interactive user gate — forking would execute autonomously and break the confirmation protocol.

## Instructions

### Session Setup

1. **User describes what they want to build.** Read relevant code to understand the starting point.
2. **Create a high-level plan.** Break the task into numbered steps, each representing one logical change. Show the numbered step list to the user before starting any micro-steps.
3. **Confirm the plan.** Wait for user acknowledgment before starting Step 1. The user may reorder, remove, or add steps.

Maintain step count, current speed setting, and remaining plan throughout the session so you can display "Step N of ~M" with each announcement. The user needs this orientation to stay engaged with the collaborative flow.

### Micro-Step Protocol (Per Change)

For each step in the plan, execute this 5-step protocol:

**1. Announce** — Describe the next change in 1-2 sentences: what will change and why. Keep announcements brief (1-2 sentences) before showing code immediately because the user came to code together, not to read an essay. Long explanations break flow and reduce collaborative momentum.

**2. Show** — Display the planned code as a diff or code block. The current step size limit (default 15 lines, max 50 lines) exists because users cannot make informed decisions about changes they have not seen. Every change gets shown—even trivial ones, which are fast to approve—so you and the user stay synchronized. Never exceed the limit: split large changes into sub-steps instead.

**3. Wait** — Stop and let the user respond with a control command. Do not proceed until you receive an explicit command—assuming the user will say "ok" and applying preemptively turns this into autonomous mode with a running commentary, violating the micro-step protocol.

| Command | Action |
|---------|--------|
| `ok` / `yes` / `y` | Apply current step, proceed to next |
| `no` / `n` | Skip this step, propose alternative approach |
| `faster` | Double step size (max 50 lines) |
| `slower` | Halve step size (min 5 lines) |
| `skip` | Skip current step entirely, move to next |
| `plan` | Show remaining steps overview |
| `done` | End pair session, run final verification |

**4. Apply** — Execute the change only after receiving `ok`/`yes`/`y`. Never apply changes without explicit confirmation—doing so turns collaborative pair programming into autonomous mode with a running commentary.

**5. Verify** — Run relevant checks (lint, type check, test) and report results in one sentence. Catching errors immediately keeps the codebase green and prevents error accumulation across steps, ensuring every change is validated before moving forward.

If a step exceeds the current size limit, split it into sub-steps (Step 3a, 3b, 3c). Announce the split: "This change is ~40 lines. I will split it into 3 sub-steps." This splitting exists because the user must be able to approve or reject individual logical changes—bundling multiple logical changes into one step to avoid splitting defeats the purpose of the micro-step protocol.

### Speed Adjustment

Sessions start at 15 lines per step, balancing progress with reviewability. Apply speed changes immediately when the user requests them and acknowledge the new setting because ignoring pace signals breaks trust and the user's sense of control. The user must feel they are the one steering the session.

| Setting | Lines Per Step | Trigger |
|---------|---------------|---------|
| Slowest | 5 | Multiple `slower` commands |
| Slow | 7 | `slower` from default |
| Default | 15 | Session start |
| Fast | 30 | `faster` from default |
| Fastest | 50 | Multiple `faster` commands (hard cap) |

When the user says `faster` or `slower`, acknowledge the change: "Speed adjusted to ~N lines per step."

### Session End

When the user says `done` or all steps are complete: run final verification (lint, type check, full test suite), show a summary (steps completed, steps skipped, files modified), and report verification results. This end-of-session gate ensures the codebase is left in a valid state.

### Examples

**Standard Session** — User says: "Pair program a function that parses CSV lines in Go"
1. Read existing code, create 5-step plan (struct, parser func, error handling, tests, integration)
2. Show plan, wait for confirmation
3. Step 1: Announce "Define a CSVRecord struct" — show 8-line struct — wait — user says `ok` — apply — verify
4. Step 2: Announce "Add ParseLine function" — show 12-line function — wait — user says `ok` — apply — verify
5. Continue through remaining steps

**Speed Adjustment** — User says `faster` after Step 2
1. Acknowledge: "Speed adjusted to ~30 lines per step."
2. Next step shows up to 30 lines instead of 15
3. If user says `slower` later, drop to ~15

**Session End** — User says `done` after Step 4 of 6
1. Run `go vet`, `go test ./...`
2. Report: "4 of 6 steps completed, 0 skipped. Modified: parser.go, parser_test.go. Tests: all passing."

## Error Handling

### User Says "Just Do It" / Wants Autonomous Mode
Cause: User wants speed, not collaboration.
Solution: Acknowledge the preference and offer to switch. Say: "Would you like to switch to autonomous mode? I can implement the remaining steps without confirmation." If they accept, drop the micro-step protocol and implement normally.

### Verification Fails After a Step
Cause: Applied change introduces a lint error, type error, or test failure.
Solution: Announce the fix as the next micro-step. Show the fix diff, wait for confirmation, apply, re-verify. Do not silently fix verification failures regardless of cause—silent fixes violate the protocol.

### Step Too Large to Fit Size Limit
Cause: A logical change requires more lines than the current limit.
Solution: Split into sub-steps (Step 3a, 3b, 3c). Each sub-step stays within the limit. Announce the split: "This change is ~40 lines. I will split it into 3 sub-steps."

## References

- [Micro-step protocol control commands](#micro-step-protocol-per-change) — user command table
- [Speed adjustment table](#speed-adjustment) — lines-per-step settings
