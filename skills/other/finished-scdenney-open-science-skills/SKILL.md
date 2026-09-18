---
disable-model-invocation: true
name: finished
description: End-of-session closure for a research or code repository. Records what actually changed into the project's own handoff and log files, distinguishing verified work from work merely attempted, and reports what was left uncommitted. Use when wrapping up a work session so the next one can resume without re-deriving state. Its start-of-session twin is sitrep.
argument-hint: '[optional: note anything the session should record that the diff would not show]'
---

# Session closure

Write down what the next session would otherwise have to rediscover. The record is only useful if it is honest: a log that reports intentions as accomplishments costs more than no log, because the next session trusts it.

## 0. Defer to the repository first

`Glob` for `.claude/commands/*finish*.md` and `.claude/commands/*wrap*.md` — the patterns catch variants such as `finished.md` or `wrap-up.md`. If one matches, `Read` it, follow its instructions instead of the steps below, and say which file you used. Otherwise continue here.

## 1. Learn the project's conventions

Read `CLAUDE.md` and `AGENTS.md` for the stated handoff or logging convention, then locate the artifacts the project actually keeps: `HANDOFF.md`, `CODEX_HANDOFF.md`, `STATUS.md`, `SESSION_LOG.md`, `NOTES.md`, or a dated `logs/` directory. Match the structure already in the file. If the project keeps none, summarize in the reply and ask **once** whether to start a durable file — do not create one unprompted.

## 2. Establish what changed

```
git status --short
git log --oneline <session-start>..HEAD
git diff --stat
```

Ground every claim in one of these outputs. For each item, classify it:

- **Done and verified** — the change exists and a check passed. Name the check.
- **Done, unverified** — the change exists; nothing confirmed it works.
- **Half-finished** — started, and the next session needs to know where the seam is.
- **Decided, not implemented** — a decision that constrains future work. These are the most valuable entries and the easiest to lose.

## 3. Update the project's artifacts

- **Handoff file** — refresh "last updated", the current objective, completed work, and next actions, inside whatever section structure the file already uses. Overwrite the state; do not append a second competing account.
- **Session log** — append a dated entry **at the top**. Never rewrite earlier entries. Concise bullets: work completed, notable outputs, commit hashes, next actions.

Keep both terse. A handoff that has to be skimmed is a handoff that gets skipped.

## 4. Commit, only if asked

If the user asked for a commit or push, run it and record the resulting hash in both the handoff file and the log entry. Otherwise leave the tree alone and report what is uncommitted — closing a session is not authorization to publish it.

## 5. Report

State exactly which files were updated, with paths, and list anything left uncommitted or unresolved. If any part of the session's work is unverified, say so here rather than letting the log imply otherwise.
