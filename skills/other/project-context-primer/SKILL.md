---
name: project-context-primer
description: >
  Run this skill at the very start of any new conversation or agent session
  before writing a single line of code. It loads the project's architectural
  decisions, conventions, known gotchas, and current task status so the agent
  operates with full context — not as a blank slate.
---

<!--
  TÜRKÇE AÇIKLAMA
  ───────────────
  Bu skill, yeni bir konuşma veya agent oturumu başladığında projenin bağlamını
  hızla yüklemek için kullanılır. Mimari kararlar, kurallar, bilinen tuzaklar ve
  mevcut görev durumu yüklenerek agent "boş sayfa" modunda değil, tam bağlamla çalışır.
  Kod yazmadan önce MUTLAKA çalıştırılmalıdır — bu, yeniden iş yapmanın en ucuz önlemidir.

  NE ZAMAN: Her yeni konuşmanın ilk adımı olarak. HİÇBİR ZAMAN atlanmaz.
  ÇIKTI:    "Context Loaded" özet bloğu — proje adı, stack, güncel görev, yüklenen bilgiler.
-->

# Project Context Primer Skill

## When to Trigger

**Always run first** when:
- Starting a new conversation about this project
- A subagent is spawned to work on a module
- Picking up work after a gap of more than a day
- Someone says "can you help with this project?" without any context

## Step-by-Step Process

### 1. Load the Knowledge Index

Read `.agent/knowledge/INDEX.md` first.

The INDEX.md file contains rows in this format:
```
| Date | Type | Topic (linked) | One-line summary |
```

- Scan all rows for entries relevant to today's task
- For each relevant row, follow the link and read the full `.agent/knowledge/<slug>.md` file
- Pay special attention to entries of type `decision` and `gotcha` — these prevent the most costly mistakes
- Extract the slug from the link: `[topic](./auth/token-refresh.md)` → slug is `auth/token-refresh`

**If INDEX.md does not exist**, output this exact warning and proceed:
```
⚠️ Knowledge base not initialized (.agent/knowledge/INDEX.md missing).
This means no architectural decisions, conventions, or gotchas have been recorded yet.
Action: Use the `knowledge-base-update` skill at the end of this session to start building it.
```

### 2. Load the Project README

Read `README.md` (or `docs/README.md` if present).

Extract and internalize:
- What the project does (one sentence)
- Tech stack (language, framework, major libraries)
- How to run it locally
- How to run tests

### 3. Load Active Task Context

Check for these files in order and read whichever exist:

```
.agent/CURRENT_TASK.md       ← What is being worked on right now
.agent/OPEN_QUESTIONS.md     ← Decisions not yet made
```

> **Note:** Architectural decisions and past decisions are stored in `.agent/knowledge/` (via `knowledge-base-update` skill),
> not in a separate DECISIONS_LOG. The INDEX.md (Step 1) is your decisions history.

If `.agent/CURRENT_TASK.md` exists, treat it as ground truth for your current mission.
If it does not exist, ask the user what today's task is before proceeding.

### 4. Scan Project Structure

Run a shallow directory listing (top 2 levels) to understand layout:

```
src/
  components/
  services/
  utils/
docs/
tests/
.agent/
```

Note any non-standard folders and check `.agent/knowledge/` for explanations.

### 5. Check for Active Conventions

Read `.agent/rules/` if it exists. These are hard constraints — not suggestions.

Common rule files to look for:
- `code-style.md`
- `commit-messages.md`
- `test-coverage.md`
- `no-secrets.md`

### 6. Produce a Context Summary

Before doing any task work, output a brief summary in this format:

```
## Context Loaded

**Project:** <name> — <one-line description>
**Stack:** <languages, frameworks>
**Current Task:** <what we're doing today, from CURRENT_TASK.md or user>
**Relevant Knowledge Entries Loaded:** <list of slugs>
**Active Rules:** <list or "none found">
**Open Questions:** <any blockers or undecided things>
**Ready to proceed:** Yes / No (explain if No)
```

Only after producing this summary should you begin the actual task.

## Rules

- **Never skip this skill** on a new session. A 2-minute scan saves hours of rework.
- **Don't assume.** If the README contradicts a knowledge entry, flag it — don't silently pick one.
- **Update CURRENT_TASK.md** at the end of each session with what was done and what's next.
- **If context is missing**, ask the user the minimum questions needed to fill the gaps before starting.

## Maintaining CURRENT_TASK.md

At the end of every session, update `.agent/CURRENT_TASK.md`:

```markdown
# Current Task

## What We're Building
<description>

## Status
<In Progress | Blocked | Review Needed | Done>

## Last Session Summary
<date> — <what was done>

## Next Steps
1. <next action>
2. <next action>

## Blockers
- <anything preventing progress>
```
