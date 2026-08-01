---
name: review
description: Use when reviewing a staged diff or a commit range for soundness against the project's taste rules. Triggers on "sound review", "review this diff/commit", "review my changes for taste", a pre-commit pass.
---

# sound:review

## What to read

- **No argument** → `git diff --cached`.
- **A range** (e.g. `main..HEAD`) → its commits and the whole `git diff <range>`.

## How to review

The project's taste rules live under `.claude/sound/`. Read the ones that bear on the code the diff touches, and apply each rule's `Detect:` and `Not-when:` **verbatim** — never from memory. If `.claude/sound/` is absent, say so and stop.

Review deeply: for every change, surface each rule it violates and each enhancement it invites. Ground every finding in the diff and the intent behind it — never rule from the text alone. Stay silent where a rule's `Not-when:` applies.

Report most-consequential first: `- <file>: <rule or enhancement> — <anchor>`. If nothing stands, say `CLEAN`.
