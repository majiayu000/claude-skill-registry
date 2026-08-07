---
name: idea
description: >-
  Use when capturing ONE new idea the user voices and wants recorded — "save this idea",
  "I have an idea", "log this idea", "/idea", "idea: ...". Creates a provenance-tracked folder
  (one folder per idea) in your ideas repo, dedups against an index, optionally mirrors to a
  GitHub Project view filtered by label:idea. NOT for mining ideas out of transcripts/meetings
  (use a dedicated extraction skill) and NOT for dated work tasks (use an issue tracker / the
  manager skill). Triggers also in Russian: «запиши идею», «у меня идея», «зафиксируй идею».
---

# Idea — fast capture of a single idea

Part of the Personal Corp framework — running a one-person business through AI agents.

One pipeline: your voice → a provenance-tracked folder in your ideas repo → (optional) an issue mirror on a GitHub Project view. The folder is the source of truth; everything else is a pointer to it.

This skill is **self-contained** — it inlines the folder structure, status enum, and provenance formats below. You don't need any external canon file.

## What this skill is NOT for

- **Mining ideas out of a transcript / meeting / thread** — that's bulk extraction from a source. Use a separate extraction skill for that. This skill captures ONE idea the user is voicing right now.
- **A dated work task with a deadline** — use an issue tracker / the `manager` skill. Ideas have no deadline; they're seeds.

## Setup

Before first use, define this in your project's `CLAUDE.md`:

```markdown
## Idea Config

### Ideas repo path
Where idea folders live (one folder per idea):
- ideas_repo: ~/Projects/ideas

### Default author
Name written into `first_voiced_by` when the user doesn't say otherwise:
- default_author: Me

### GitHub mirror (optional)
Mirror each idea as an issue (added to a Project view filtered by `label:idea`):
- mirror_enabled: false
- owner: your-github-handle               # only if mirror_enabled: true
- ideas_repo_name: ideas                  # GitHub repo name for the issue, only if mirror_enabled: true
- project_number: <your Project number>   # only if mirror_enabled: true

(if mirror_enabled is false, the skill only writes to the ideas repo — no issue, no Project)
```

No separate init skill needed — this section is the setup. If `mirror_enabled` is false, the GitHub Project step is skipped entirely; the idea still lives as a folder.

## One question — max

Ask **at most one** short question, and only if the idea's essence can't be extracted from the wording (what is it / for whom). Do NOT ask about mechanics, pricing, risks, or tech stack — capture the raw material as-is and write the gaps into `next-steps.md` as open questions. The question **"how should I record it — issue / file / both?"** is forbidden: the form is fixed by this skill. Never block on form.

## Status enum (in `idea.md` frontmatter)

- `seedling` — just voiced, not yet worked on
- `exploring` — first research gathered, `market.md` filled
- `building` — landing / pilot / prototype in progress
- `live` — a public artifact exists
- `parked` — set aside, reason in `next-steps.md`
- `dropped` — closed, reason in `next-steps.md`

A freshly captured idea is always `seedling`.

## Provenance formats (rows in `sources.md`)

Every idea needs at least one source. Each sighting is one row. Genericize the source kind — no real internal paths:

| Source kind | Format in `sources.md` |
|---|---|
| Meeting note | `meeting note — {who/where}, {date}` |
| CRM card | `CRM card — {contact}, {date}` |
| DM | `DM — {channel}, {date}` |
| Voice draft (solo) | `voice draft, {date}` |
| Reading / web | `{url}, {date}` |
| Direct capture | `direct /idea invocation, session, {date}` |

## Steps

1. **`date`** — resolve the real date. Between 00:00–04:00, "today" means the previous calendar day.

2. **Dedup against the index.** Read `INDEX.md` at the root of your ideas repo. Match is **semantic, not string** ("a board of advisors run on agents" ≈ `advisory-agent-grounded-data`). If unsure, open the candidate's `idea.md` to compare.
   - **Match found** → this is a repeat sighting, not a new idea:
     - append a row to the existing folder's `sources.md`,
     - in `idea.md` bump `last_touch` and increment `sources_count` (do NOT touch `first_voiced`),
     - if mirror is enabled, add a one-line comment to the issue mirror ("voiced again: {date}, {context}"),
     - regenerate `INDEX.md`, commit, report. **STOP.** Do not create a new folder.

3. **New idea** → create the folder `ideas/YYYY-MM-DD-{slug}/` with the template files below.
   - **Slug**: kebab-case, 3–5 words, by meaning not by form (`live-sales-coach-b2b`, not `b2b-product-1`). The date prefix is the date of **first capture** — it never changes on later sightings.
   - In `idea.md`: `title`, `status: seedling`, `first_voiced_by: {default_author from config unless user said otherwise}`, an "Essence" of 1–2 sentences, and the **raw verbatim wording** preserved exactly as voiced. Interpretation, if any, goes in a separate section — never overwrite the raw wording.
   - In `sources.md`: one row for this sighting (see provenance formats).
   - `market.md` is optional (leave the stub; fill only when researched).
   - `next-steps.md` holds open questions and the "what next?" — this is where pricing/mechanics/stack gaps land.

4. **Regenerate `INDEX.md`** (format below). It's auto-generated — don't hand-edit individual rows; rewrite the whole file from the folders.

5. **GitHub Project mirror — OPTIONAL** (only if `mirror_enabled: true` in config). The folder is the source of truth; the issue is just a pointer for board view. See "Project mirror" below.

6. **Commit + push** to the ideas repo: `feat: idea {slug}` (invoking this skill is consent to record; the ideas repo is private).

7. **Report** — one line per item: folder path, issue `#N` (if mirrored), and the Project view link (if mirrored).

## Template files

Create these four files in `ideas/YYYY-MM-DD-{slug}/`. Keep them minimal — the folder is a seed, not a spec.

**`idea.md`**

```markdown
---
title: {short human title}
status: seedling
first_voiced_by: {default_author}
first_voiced: {YYYY-MM-DD}
last_touch: {YYYY-MM-DD}
sources_count: 1
---

# {title}

## Essence
{1–2 sentences — what it is and for whom.}

## Raw wording
> {the idea exactly as voiced — verbatim, do not paraphrase}

## Interpretation (optional)
{any reading/expansion goes here — never inside Raw wording}
```

**`sources.md`**

```markdown
# Sources

| Date | Who | Context | Reference |
|---|---|---|---|
| {YYYY-MM-DD} | {default_author} | first voiced | direct /idea invocation, session, {YYYY-MM-DD} |
```

**`market.md`** (optional stub)

```markdown
# Market

_Not researched yet. Fill when status moves to `exploring`: analogues, demand signals, where it could fit._
```

**`next-steps.md`**

```markdown
# Next steps

## Open questions
- {gaps you didn't ask about — mechanics, pricing, audience, stack}

## What next
- {landing? brainstorm? park? close? — leave blank if undecided}
```

## INDEX.md regeneration

`INDEX.md` is auto-generated — never hand-edit. Rewrite it whole from the current folders. Structure:

```markdown
# Ideas index

Updated: {YYYY-MM-DD}

## Active ideas
| Slug | Status | First voiced | Sources count | Last touch |
|---|---|---|---|---|
| live-sales-coach-b2b | seedling | 2026-05-01 | 1 | 2026-05-01 |

## Parked / dropped
| Slug | Status | First voiced | Last touch |
|---|---|---|---|

## By status
- seedling: N
- exploring: N
- building: N
- live: N
- parked: N
- dropped: N
```

## Project mirror (optional — only if `mirror_enabled: true`)

Each idea folder gets one issue mirror in the ideas repo, added to a GitHub Project view filtered by `label:idea`. The folder is the source of truth; the issue is a pointer for quick board scanning. **Don't copy folder contents into the issue body.**

Mirror format:

- **title:** `idea: {title}`
- **label:** `idea` (the only label — don't invent others)
- **body:** link to `ideas/{folder}/idea.md` + one "Essence" paragraph + status + one provenance line. Nothing more.

Commands (after creating a new idea folder):

```bash
url=$(gh issue create -R {owner}/{ideas_repo_name} \
  --title "idea: {title}" \
  --body "{body — link + essence + status + provenance}" \
  --label idea)

# Add to the Project board (number from config), so it appears in the label:idea view
gh project item-add {project_number} --owner {owner} --url "$url"
```

On rename → update the issue title. On `dropped` → close the issue with a comment stating the reason. On a repeat sighting (step 2) → just add a one-line comment, no new issue.

If `mirror_enabled` is false, skip this whole section — the idea still lives correctly as a folder.

## Failure without the skill → rule

| Failure | Rule |
|---|---|
| Only an issue created, no folder | The folder owns the truth (provenance, sources); the issue is a pointer |
| Fat issue body with full architecture | Body = link + essence + status + provenance, never a copy of the folder |
| `INDEX.md` not read → duplicate of an existing idea | Dedup is mandatory; a repeat = a new source row, not a new folder |
| Issue not added to the Project (when mirror enabled) | Without `item-add` the `label:idea` view won't show it |
| Invented labels (`monetization`, etc.) | Only `idea` |
| Blocking question "issue / file / both?" | Form is fixed; max one question — and only about the essence |
| Raw idea rewritten into "architecture" | seedling = raw material verbatim; interpretation is a separate section |

## Red flags — stop

- About to create an issue without a folder → step 3 was skipped.
- Writing a body longer than ~10 lines → you're copying, not linking.
- Asked the user a second question → just capture it as-is.
- Finished without `item-add` (when mirror enabled) or without commit → steps 5–6 not done.

## Cross-references

- **Mining ideas out of a transcript / meeting / thread** — a separate extraction skill (bulk source → many ideas). This skill is single-idea capture only.
- **A dated work task** with a deadline — the `manager` skill / your issue tracker, not an idea folder.
