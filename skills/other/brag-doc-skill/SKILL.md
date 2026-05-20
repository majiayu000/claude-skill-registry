---
name: commit-based-brag-docs
description: Use when a user needs a personal brag doc draft generated from git commits in a specific repository and relative timeframe, with evidence-first bullets and prompts for non-commit contributions.
license: MIT
---

# Commit-Based Brag Docs

## Overview

Generate a structured brag doc draft from commit history. This skill is optimized for personal records: it is commit-only by default, then explicitly asks for non-commit contributions so invisible work is not lost.

Core rule: no impact claims without evidence in commit history or a manual note.

## Quick Start

1. Confirm inputs:
- target repo path
- relative window (default: `30 days`)
- optional author override

2. Run:

```bash
python3 scripts/generate_brag_doc.py \
  --repo /absolute/path/to/repo \
  --window "30 days"
```

Installed skill path variant:

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/commit-based-brag-docs/scripts/generate_brag_doc.py" \
  --repo /absolute/path/to/repo \
  --window "30 days"
```

3. Optional outputs:

```bash
python3 scripts/generate_brag_doc.py \
  --repo /absolute/path/to/repo \
  --window "90 days" \
  --author "you@company.com" \
  --output /absolute/path/to/output.md \
  --json-output /absolute/path/to/output.json
```

Default markdown destination:
`<repo>/docs/brag-docs/YYYY-MM-DD-brag-doc-last-<window>.md`

## Share / Install

Install from a GitHub repo/path:

```bash
$skill-installer scripts/install-skill-from-github.py \
  --repo benceHornyak/brag-doc-skill \
  --path . \
  --name commit-based-brag-docs
```

Or from a GitHub repo URL:

```bash
$skill-installer scripts/install-skill-from-github.py \
  --url https://github.com/benceHornyak/brag-doc-skill \
  --path . \
  --name commit-based-brag-docs
```

Or install with [skills.sh](https://skills.sh/):

```bash
npx skills add benceHornyak/brag-doc-skill
```

Usage example after install:

```text
Use $commit-based-brag-docs to draft my brag doc for the last 30 days from /absolute/path/to/repo.
```

## Workflow

1. Collect evidence from git:
- commits in timeframe
- metadata (hash, date, author, subject/body)
- numstat and filenames

2. Group evidence into themes:
- delivery/product
- quality/reliability
- tooling/DevEx
- docs/knowledge sharing
- maintenance/refactoring

3. Generate markdown sections:
- `## Snapshot`
- `## Key Accomplishments`
- `## Quality and Reliability`
- `## Invisible but Valuable Work (Manual Fill)`
- `## Lessons / What I'd Do Differently`
- `## Evidence Appendix`

4. Rewrite weak bullets:
- convert activity into outcomes
- name who benefited
- keep evidence pointers (commit hashes, file scope, diff stats)

## Guardrails

- Do not invent impact numbers.
- If impact is unknown, use `TODO:` prompts instead of guessing.
- Keep direct traceability to commit evidence.
- Preserve the manual-fill section; commit-only data misses mentoring, incident response, and cross-team support.

## Writing Rubric

Use this transformation pattern:

- Activity: "Refactored auth middleware."
- Better: "Reduced auth-path complexity in middleware used by X services (evidence: `abc123`, `def456`), lowering change risk for future auth work."

Checklist for each accomplishment bullet:
- clear action
- scope (system/team/user)
- plausible outcome
- concrete evidence pointer
- no unsupported claims

## Reference

For the distilled research principles, read:
`references/brag_doc_principles.md`
