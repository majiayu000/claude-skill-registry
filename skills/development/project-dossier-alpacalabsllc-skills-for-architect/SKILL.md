---
name: project-dossier
description: Create or update the project dossier — a PROJECT.md file in the working directory holding persistent project facts (identity, site, zoning, program, code edition) plus an index of decisions. Use when starting a project, when the user says "set up the project" or "remember this for the project", or when an analysis skill needs somewhere to record findings. Facts only — to record a decision with its rationale, use /decision.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - AskUserQuestion
---

# /project-dossier — Project Facts File

You maintain `PROJECT.md`: a single file at the project root that holds the durable facts of an architecture project, so no skill re-derives what's already known and the whole team sees the same state.

The dossier is the **facts layer**. The **reasoning layer** — why a choice was made — lives in `decisions/` via `/decision`. Don't mix them: PROJECT.md says *what is*; a decision record says *why it is*.

## Usage

```
/project-dossier            → show current dossier status (or offer to init)
/project-dossier init       → create PROJECT.md, interview for the basics
/project-dossier update     → reconcile the dossier with new facts from the conversation
```

## Hard rules

1. **Every entry carries a source and a date.** `FAR 6.02 (PLUTO, 2026-06-10)` — never an orphan number. If the user states a fact verbally, the source is `client, YYYY-MM-DD`.
2. **Update in place, never duplicate.** If a fact changes (re-run analysis, corrected input), replace the value and refresh the source/date. The dossier holds current state, not history — history is git's job.
3. **Facts only.** "Zoning district: R7A" belongs here. "We chose the UAP bonus over the contextual envelope" is a decision — propose `/decision` instead.
4. **Project facts only.** User preferences, workflow habits, and firm conventions do NOT belong in the dossier — Claude Code's own memory (CLAUDE.md, auto memory) handles those.

## On `init`

1. If `PROJECT.md` already exists, say so and switch to `update` mode.
2. Ask for whatever basics aren't already evident from the conversation (one question, grouped): project name, address, client, jurisdiction.
3. Write `PROJECT.md` from the template below, filling what you know, leaving the rest blank.
4. If the working directory is a git repo, suggest committing it: the dossier is meant to be shared with the team.

## On `update`

1. Read `PROJECT.md`.
2. Collect new facts from the current conversation (analysis results, corrected values, user statements).
3. Apply rule 2 — replace stale values in place, append genuinely new ones to the right section, each with source + date.
4. Show a short diff-style summary of what changed.

## Template

```markdown
# Project Dossier — {project name}

> Maintained by Architecture Studio skills and the project team.
> Every entry carries a source and a date. Facts only — rationale lives in the decisions/ directory.

## Identity

| Field | Value |
|-------|-------|
| Project | |
| Address / BBL | |
| Client | |
| Jurisdiction | |

## Site

<!-- site-planner skills append here: climate, flood, transit, demographics, context -->

## Zoning

<!-- zoning skills append here: district, FAR, envelope results, overlays, landmark status -->

## Program

<!-- programming skills append here: headcount, space program, occupant loads -->

## Code

| Item | Value | Source | Date |
|------|-------|--------|------|
| Building code edition | | | |

## Decisions

<!-- maintained by /decision — do not edit by hand -->

| # | Decision | Status | Date |
|---|----------|--------|------|
```

## How other skills use the dossier

Analysis skills in this marketplace check for `PROJECT.md` before fetching (don't re-derive what's on file) and append their key findings after completing. That behavior lives in each skill — your job here is only init, update, and keeping the file well-formed.

## Edge cases

| Situation | Handling |
|-----------|----------|
| `PROJECT.md` exists but malformed / hand-edited | Preserve all content; reorganize into template sections; say what moved |
| Facts conflict (dossier says X, user says Y) | Ask once; the answer wins; update with new source + date |
| No project context at all, user just ran `/project-dossier` | Show usage and ask if they want `init` |
| Multiple projects in one directory | One dossier per directory — suggest separate working directories |
