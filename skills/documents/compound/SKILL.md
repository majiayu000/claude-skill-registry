---
name: compound
description: Document a durable solution or project concept in the repo. Use when the user says "compound this", "document this fix", or after a verified non-trivial outcome that should live in docs/solutions/ or CONCEPTS.md.
metadata:
  short-description: Write durable solution docs and concept definitions
---

# Compound — durable project knowledge

`Op: extend` — adds structured, in-repo documentation of solved problems and project-specific vocabulary.

`compound` writes exactly two surfaces:

- `docs/solutions/<category>/<slug>.md` — one learning per solved problem.
- `CONCEPTS.md` at the repo root — one definition per project-specific term.

It does not write memory files. User/preference facts are handed to `memory-update`.

## Auto-invoke

Fire automatically after a verified non-trivial outcome:

- "that worked"
- "it's fixed"
- "ship it"
- "merged"
- "resolved"
- "verified"
- "done"

Auto-fire is permission to evaluate, not permission to fabricate. The reject-by-default gate below still decides whether a doc is warranted.

## Reject-by-default gate

A doc is earned, not assumed. All three filters must clear:

1. **Would I forget this?** Skip baseline knowledge anyone in this codebase already carries.
2. **Already covered?** Update an existing doc rather than duplicate it.
3. **Scope-qualified?** A repo-specific quirk qualifies; a general programming truth does not.

If nothing clears the gate, say so in one line and exit. Never fabricate a doc.

## Mode routing

Strip `mode:` tokens from `$ARGUMENTS`.

| Mode | Trigger | What it does |
|---|---|---|
| **Solution** (default) | none | Document one solved problem → `docs/solutions/` |
| **Vocabulary** | when a durable, reusable project term surfaces | Reconcile `CONCEPTS.md` — read `references/concepts.md` |
| **Headless** | `mode:headless` | Non-interactive overlay on whichever mode is active |

## Writing a solution doc

1. Read `references/schema.yaml` and `assets/solution-template.md`.
2. Classify the problem: bug or knowledge track.
3. Check `docs/solutions/` for duplicates by grepping frontmatter (`title:`, `tags:`, `module:`, `component:`).
4. Write one file: `docs/solutions/<category>/<slug>.md`.
5. Run `python3 scripts/validate-frontmatter.py <path>` until it exits 0.
6. Read the file back to confirm.

## Writing a concept entry

1. Read `references/concepts.md`.
2. Check `CONCEPTS.md` for an existing definition of the term.
3. If absent and the term clears the gate, add one entry: a one-sentence local definition and a second paragraph only for non-obvious behavioral rules.
4. One definition per concept — refresh on drift, never duplicate.

## Commits

One learning per commit. Body carries an ODIN `Op:` trailer:

- New doc → `Op: extend`
- Refresh a drifted doc → `Op: correct` + `Restores: spec:<invariant>`
- Delete/consolidate-away → `Op: purge` + `Removes: path:<ref>`

Stage only the surfaces `compound` wrote or edited.

## Disambiguation

- **vs `autolearn`** — `autolearn` extracts session learnings into memory; `compound` documents durable project knowledge into repo docs.
- **vs `memory-update`** — `memory-update` writes auto-memory about users and cross-project context. `compound` never writes memory.
