---
name: maintain-docs
description: Process session summaries and skill usage logs, identify documentation issues, and apply frequency-gated fixes. Use periodically to maintain project documentation quality.
disable-model-invocation: true
user-invocable: true
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
hooks:
  Stop:
    - command: "bash .claude/hooks/log-skill-usage.sh maintain-docs"
---

# Process Feedback and Maintain Documentation

## Phase 1: Evaluate session summaries

1. Read all `.md` files in `feedback/summaries/` that haven't been processed yet
   - Check `feedback/issue-tracker.md` to see which summaries are already listed as sources
2. For each new summary, identify doc/skill issues: incorrect information, missing guidance, confusing instructions, stale examples
3. If deeper investigation is needed, read the raw transcript in `feedback/transcripts/` (if still on disk)
4. Record findings in `feedback/issue-tracker.md` with file path, issue description, and source summary

## Phase 2: Review skill usage

5. Read `feedback/skill-usage.log` if it exists
6. Identify:
   - Skills never invoked (candidates for removal or better descriptions)
   - Skills invoked frequently (candidates for optimization)
   - Skills with consistent post-invocation errors in summaries (need fixing)
7. Record findings in `feedback/issue-tracker.md`

## Phase 3: Apply fixes (frequency-gated)

8. Read `feedback/issue-tracker.md`
9. Only act on issues reported by **2+ independent sessions** (or 1 session with concrete evidence like a build failure)
10. For each actionable issue:
    - Read the referenced doc/skill file
    - Only edit sections within `<!-- AUTO-MANAGED: feedback-driven -->` markers (or add new auto-managed sections)
    - Make minimal, targeted fixes
11. If an issue requires substantial work, create a document in `docs/` describing the problem and proposed fix instead

## Phase 4: Prune and consolidate

12. Scan docs/skills for redundant or conflicting instructions — flag for human review
13. Print summary of all changes made and issues deferred

## Constraints

- Do NOT edit content outside `<!-- AUTO-MANAGED: feedback-driven -->` markers
- Do NOT act on single-occurrence reports — require 2+ independent sessions (or 1 with concrete build/test failure evidence)
- Do NOT delete documentation or skills — only flag candidates for human review
- Do NOT rewrite entire files — make minimal, targeted fixes
- Do NOT maintain `.claude/HISTORY.md` — that is the history-keeper agent's responsibility
