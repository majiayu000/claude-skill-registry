---
name: verification-before-completion
description: "Use when about to claim completion, express satisfaction with work, or state that a task is done. Triggers on phrases like 'done', 'complete', 'finished', 'ready', 'all set', 'looks good'."
user-invokable: false

metadata:
  agent-affinity: [all]
  keywords: [done, complete, finished, ready, verified, passing, success, all-set, looks-good]
  platforms: [all]
  connections:
    enhances: [cook, cook-fast, cook-parallel, fix, fix-deep, plan, plan-fast, plan-deep, plan-parallel, bootstrap, bootstrap-fast, bootstrap-parallel]
---

# Verification Before Completion

> **IRON LAW: NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE.**
>
> Every claim of "done", "complete", "passing", or "working" MUST be backed by output from a command run in THIS conversation turn. Memory of previous results is NOT evidence.

## The 5-Step Verification Gate

Before ANY completion claim, execute ALL five steps in order:

1. **IDENTIFY** — Determine the verification command (test suite, build, type check, lint)
2. **RUN** — Execute the command NOW, in this turn
3. **READ** — Read the FULL output, not a summary
4. **VERIFY** — Compare output against original requirements line by line
5. **THEN CLAIM** — Only after steps 1–4 produce passing evidence

Skip any step → completion claim is INVALID.

## Common Verification Failures

| Claim | Problem | Required Action |
|-------|---------|-----------------|
| "Tests pass" | Recalling old results | Run test suite NOW and read output |
| "Build succeeds" | Assuming from no errors seen | Run fresh build command and confirm exit code 0 |
| "Feature works" | Mental simulation | Demonstrate with specific input → output |
| "Agent reported success" | Trusting summary | Read the agent's ACTUAL output, not its self-assessment |
| "Looks correct" | Visual scan only | Diff against spec/requirements |
| "No errors" | Checked stdout only | Check stderr, exit codes, and log files too |

## Red Flags — Stop and Re-verify

If you catch yourself doing ANY of these, STOP and run verification:

1. Using words: "should", "probably", "seems", "likely", "I believe"
2. Feeling satisfied BEFORE running verification commands
3. Trusting cached/remembered results instead of fresh output
4. Claiming success based on a subagent's self-report without reading its output
5. Skipping verification because "the change was small"
6. Saying "done" immediately after writing code, before testing
7. Conflating "no errors during edit" with "feature works correctly"
8. Assuming passing state persists across multiple edits

## Anti-Rationalization Table

| Rationalization | Reality | Required Action |
|-----------------|---------|-----------------|
| "Should work now" | "Should" is not evidence | Run verification command |
| "Just verified this" | State may have changed since last verification | Verify AGAIN after every change |
| "Agent said it passes" | Agents summarize optimistically | Read the actual command output yourself |
| "Only changed one line" | One line can break everything | Run full test suite |
| "Tests were passing before" | Your changes may have broken them | Run tests NOW |
| "It's obvious it works" | Obvious bugs are the most common bugs | Demonstrate with concrete input/output |

## When This Applies

ALWAYS. Before ANY claim that work is complete, successful, passing, working, ready, done, or finished. No exceptions. No shortcuts. The cost of verification is minutes; the cost of false completion is rework.

### Foundational Principle

Violating the letter of these rules IS violating the spirit. There are no clever workarounds that preserve the intent while skipping the steps.

### Related Skills
- `auto-improvement` — Verification failures tracked for rework detection across sessions
