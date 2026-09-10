---
disable-model-invocation: true
name: deliverable-open
description: Opens a deliverable, such as a talk, course module, paper, book chapter, or referee report, for AI-assisted work across sessions. Interviews the author until the manifest is written, then scaffolds deliverable.yml, append-only HANDOFF.md, a numbered planning/ wiki with index and open questions, inbox/ for dictated braindumps, gitignored checks/, and the house deck template for talks. Use when the user says "open a deliverable", "set up this talk/paper/module for the pipeline", "make a manifest", or starts deadline-driven work that spans sessions. Not for one-off tasks.
argument-hint: '[path to the deliverable directory; optionally --kind talk|course|paper|chapter|review]'
allowed-tools:
- Read
- Glob
- Grep
- Bash
- Write
- Edit
- AskUserQuestion
---

# Deliverable open

<p align="center"><img src="assets/pipeline.svg" alt="The deliverable pipeline: eight steps over three layers (one wiki per piece of research, one manifest per deliverable, a shared commons)" width="900"></p>

Full guide: [`docs/deliverable-pipeline.md`](../../../docs/deliverable-pipeline.md).

A deliverable gets the pipeline when it has a deadline, an audience, and more than one session of work. This skill writes the files the rest of the pipeline reads: `check_deliverable.py` (the deterministic gate), `deliverable-intake` (braindumps into the wiki), `deliverable-lint` (the editorial review), and the `session` skill's `/sitrep` and `/finished`.

## Where the tooling lives

- Gate script: `~/Documents/GitHub/resources/project_hygiene/scripts/check_deliverable.py` (or `$DELIVERABLE_CHECK`). Its docstring is the manifest reference; read it before writing a manifest.
- Hook installer: `~/Documents/GitHub/resources/project_hygiene/scripts/install-hooks.sh <repo>`.
- Deck template: `~/Documents/GitHub/resources/deck-template/` (self-contained HTML + PDF deck, `content.md` -> `src/build.py`).
- Handoff format: the one `courses/hdw/HANDOFF.md` uses; wiki format: `courses/hdw/data-module/lecture-planning/00-README.md`.

## Kind profiles

One file per kind at `~/Documents/GitHub/resources/project_hygiene/kinds/<kind>.md` (talk, paper, module, chapter, review): the interview questions beyond the common five, the manifest defaults, the lint questions `lint_prepare.py` appends, the ship step, and the related skills. Read the profile for the deliverable's kind before round 1 and let it drive rounds 2 and 3; never load more than one profile. One piece of research has one wiki: a paper's talk and referee response declare the paper's `planning/` as their `planning_dir` and add their own numbered files to it, rather than opening a second wiki.

## Rounds

Run the interview the way `research-grill` does: ask the whole frontier at once, numbered, each with a one-line "why this matters" and a recommended answer; facts you can look up (dates from a calendar file, the number snapshot in a manuscript, an existing planning directory) you look up. Two or three rounds usually suffice.

Round 1, always:

1. **Kind and root.** Which directory is the deliverable? A talk is its own folder; a course module is the module folder (`hdw/data-module/`), not the repo; a paper is the folder holding `manuscript/`; a chapter is its folder under `chapters/`.
2. **Audience and deadline.** Who reads or hears it, and when it ships. A talk names the panel and date; a module names the class dates; a paper names the venue and submission date.
3. **Claim and done-test.** One sentence each. `claim` is what the deliverable asserts; `done` is what a finished one looks like ("15 slides, ten minutes, every number traced to the snapshot, published at the URL on the QR code").
4. **Sources of truth.** The files nothing else may contradict: `content.md` and `notes.md` for a talk, `_data/course.yml` for a course site, `numbers.tex` and `references.bib` for a paper, the canonical syllabus for a module.
5. **Sections.** How the deliverable divides for review: `content-keys` (deck `@N.*` fields), `latex` (`\section`), `markdown-headings`, `rmd-chunks`, or an explicit list. Sections are logical; never split a source file to make them.

Round 2, from the answers:

6. **Checks.** Which gate checks apply (see the script docstring): `citations` (bib, scan files, `cite_fields` for decks, `reading_lists` for Markdown syllabi, `verify_bib` where fabricated entries are the risk), `numbers` (source, snapshot id, the data tables that copy it), `facts` and `leaks` for a Jekyll site, `deck_budget`, `prose_tells`, `build`.
7. **Knowledge base** (research repos). If the repo has a `research-repo` layout, set `knowledge_base: sources/md` and add `references.bib` to `sources_of_truth`; the gate then warns when a cited work has no Markdown source, intake routes unknown sources to `process-source`, and lint checks claims against the sources. Ask once; default to setting it when `sources/md/` exists.
8. **Planning wiki.** Does a wiki already exist (`lecture-planning/`, `chapters/CLAUDE.md`, `planning/map.md`)? Declare it as `planning_dir`; never move it. Otherwise create `planning/`.
9. **Voice pin.** The writing-toolkit commit the prose rules are pinned to: `git -C ~/Documents/GitHub/resources/writing-toolkit rev-parse --short HEAD`.
10. **Night shift.** Stays `enabled: false` at open. Say so; it is switched on only after one manual `deliverable-lint` run has been read.

## What gets written

At the deliverable root:

- `deliverable.yml` with every field the interview settled; comment the ones it did not.
- A vendor-neutral `agent:` block at the top of the manifest (Claude runs `/oss:<name>`, Codex runs `$<name>`; the shared `deliverable_context.py` prints it at session start for both):
  ```yaml
  agent:
    on_braindump: deliverable-intake
    on_review_request: deliverable-lint
    on_session_end: finished
    preserve_raw_captures: true
    session_state: HANDOFF.md
  ```
- Commons fields when the research commons exists (`~/Documents/GitHub/research/commons/`): `commons_root` (relative path), `commons_tags` (sorted lowercase slugs), and optionally `commons_revision` (a full commit to pin). At session start only the commons INDEX lines matching the tags enter context, capped at twenty; cards and threads are read on demand.
- `HANDOFF.md` with the standard header and a first entry dated today: **Decision** (what was opened and why), **Completed** (the files created), **Next actions** (run the gate; first intake).
- `planning/00-README.md` (folder map, sources of truth, decisions recorded here) and `planning/08-open-questions.md` (open list plus a resolved log) unless an existing wiki was declared; then add the manifest pointer to that wiki's index instead.
- `inbox/README.md`: "Raw captures. Dictate into a new dated file here; never edit a capture; `deliverable-intake` promotes it and renames it `*.done.md`."
- `checks/.gitignore` containing `*` and `!.gitignore` and `!release.json` and `!citations.json`.
- For `--kind talk` with no `src/` present: copy the deck template's `src/`, `content.md`, `notes.md`, and `README.md`, then set `build.command` and `sources_of_truth` in the manifest accordingly.

Then:

- If the repo has no `.githooks/pre-commit`, offer `install-hooks.sh`; install only on a yes.
- Offer to append the deliverable's proper nouns (people, places, named theories, project names) to `~/.config/macwhspr/vocab.md` so dictation renders them correctly; append only on a yes, one term per line, under a heading naming the deliverable.
- Offer to add the manifest path to `~/.claude-assistant/config/deliverables.yml` (the night-shift registry). Listing is not enabling.
- If the repo root has no `AGENTS.md`, say so and stop; do not create one here. If it has one and lacks a `## Deliverable pipeline` section, offer to append the canonical paragraph from `~/Documents/GitHub/resources/project_hygiene/notes/agents-pipeline-paragraph.md` (it is what tells either vendor when to invoke which on-demand skill, and what lets Codex, which has no hooks, start from the same context).

## Exit

Run `python3 check_deliverable.py --root <dir>` once and show the result. Name the next step in one line: dictate the first braindump into `inbox/`, then `/oss:deliverable-intake`.

## Notes

- Threshold: a deadline, an audience, more than one session. A four-hour referee report qualifies; a two-day analysis nobody reads does not.
- One manifest per deliverable; a course with six sessions is one deliverable with six sections, not six deliverables.
- Overleaf submodules: the manifest and the other house files live in the parent repository beside the submodule, never inside it.
