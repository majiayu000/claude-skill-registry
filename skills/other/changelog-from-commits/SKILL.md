---
name: changelog-from-commits
description: Use when cutting a release, writing a CHANGELOG entry, or summarizing what changed since a tag — when the repo's commits follow (or mostly follow) Conventional Commits and a mechanically-accurate section breakdown beats a model's reading of the diff.
---

# Changelog From Commits

## Overview

Parses `git log` against the [Conventional Commits](https://www.conventionalcommits.org/) spec and prints a categorized changelog: Features, Fixes, Performance, Refactoring, Docs, Tests, Build, CI, Chore, Other, plus a BREAKING CHANGES section pulled from `!` markers and `BREAKING CHANGE:` footers. Deterministic — the categorization is a fact about the commit message, not a judgment call, so a script produces it more reliably than a model re-reading commit subjects.

**Core principle:** A changelog section is either correct (matches the commit's own declared type) or it silently drops/miscategorizes a change. Parsing is not the place for approximation.

## Usage

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/generate.sh [from-ref] [to-ref]
```

- `from-ref` defaults to the most recent tag, or the repo's root commit if there are no tags.
- `to-ref` defaults to `HEAD`.
- Requires a git repository; exits 2 if run outside one.
- Prints Markdown to stdout — pipe into a file, or paste directly into `CHANGELOG.md`.

```bash
bash ${CLAUDE_SKILL_DIR}/scripts/generate.sh v1.2.0 HEAD > /tmp/new-entries.md
bash ${CLAUDE_SKILL_DIR}/scripts/generate.sh                    # since the last tag, to HEAD
```

## What it gets right and what it doesn't

**Reliable:** `type(scope)!: subject` parsing, breaking-change detection (`!` or a `BREAKING CHANGE:` footer), section grouping, short-hash linking, merge commits excluded automatically.

**Falls back to "Other":** any commit whose subject doesn't start with a known Conventional Commits type (`feat`/`fix`/`perf`/`refactor`/`docs`/`test`/`build`/`ci`/`chore`) — including free-text subjects like "Initial plan" or "Add X". A repo that doesn't consistently use Conventional Commits will produce a large "Other" section; that's an honest signal about the commit history, not a script bug. See it happen: run this against this library's own pre-2.0 history and most entries land in Other because they predate the Conventional Commits convention adopted later.

**Not attempted:** rewriting or improving commit subjects, deduplicating near-identical entries, or inferring a type the author didn't declare.

## After generating

The script produces raw categorized entries — it does not write prose framing, a version header, or a date. Add those yourself (or ask Claude to), and edit any "Other" entries that deserve reclassification before they ship in a release. Don't paste the raw output into `CHANGELOG.md` as the final section without a pass over "Other" and "BREAKING CHANGES" — those two sections are exactly where a human or model read adds real value on top of the deterministic parse.

## Remember

> Categorization is deterministic; the narrative framing around it (a version header, a "why" sentence, what to call out) is not. Do the first with the script, the second with judgment.
