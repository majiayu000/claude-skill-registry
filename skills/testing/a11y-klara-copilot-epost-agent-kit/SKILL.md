---
name: a11y
description: (ePost) Use when "accessibility", "WCAG", "POUR", "a11y", "screen reader", or accessibility workflow ("audit", "fix", "review", "close finding") is mentioned across any platform — loads cross-platform a11y compliance rules
user-invocable: true
context: fork
agent: epost-a11y-specialist
metadata:
  argument-hint: "[--audit [platform] | --fix [#id|n] | --review [area] | --close [id]]"
  keywords:
    - a11y
    - accessibility
    - wcag
    - aria
    - screen-reader
    - pour
  connections:
    enhances: []
  agent-affinity:
    - epost-a11y-specialist
  platforms:
    - all
---

# A11y — Unified Accessibility Command & Foundation

Cross-platform accessibility foundation (WCAG 2.1 AA) with auto-detection of audit, fix, review, or close workflows.

## Step 0 — Flag Override

If `$ARGUMENTS` starts with `--audit`: load `/audit --a11y` (references/a11y-workflow.md in audit skill). Pass remaining args as platform hint.
If `$ARGUMENTS` starts with `--fix`: load `/fix --a11y` (references/a11y-mode.md in fix skill). Pass remaining args as finding ID or count.
If `$ARGUMENTS` starts with `--review`: load `/review --a11y` (references/a11y.md in review skill). Pass remaining args as focus area.
If `$ARGUMENTS` starts with `--close`: load `/audit --close` (references/a11y-close.md in audit skill). Pass remaining args as finding ID.
Otherwise: continue to Auto-Detection.

## Auto-Detection

Analyze `$ARGUMENTS` for positional patterns and keywords:

| Pattern | Dispatch |
|---------|----------|
| `audit` or empty + staged changes exist | `/audit --a11y` (detect platform from changed file extensions) |
| `fix` or `#<id>` or bare number | `/fix --a11y` with the ID/count |
| `review` | `/review --a11y` |
| `close` or `resolve` | `/audit --close` |
| Ambiguous | Ask user: audit, fix, review, or close? |

## Platform Detection

| Signal | Platform | Skill |
|--------|----------|-------|
| `.swift`, `.xib`, SwiftUI | iOS | `ios-a11y` |
| `.kt`, Compose | Android | `android-a11y` |
| `.tsx`, `.jsx`, HTML, CSS | Web | `web-a11y` |

If no signal, ask the user. Activate ONLY the skill matching the detected platform.

## POUR Framework

| Principle | Requirement |
|-----------|-------------|
| **Perceivable** | Content available through sight, hearing, or touch |
| **Operable** | Interface navigable by keyboard, pointer, voice |
| **Understandable** | Content readable, predictable, input-assisted |
| **Robust** | Compatible with assistive technologies |

## WCAG Conformance Levels

| Level | Requirement | Target |
|-------|-------------|--------|
| **A** | Minimum | Must pass |
| **AA** | Standard (legal baseline) | **Our target** |
| **AAA** | Enhanced | Nice to have |

## Severity & Scoring

Accessibility score: 0–100 (start at 100, subtract per finding).

| Severity | Points | Examples |
|----------|--------|----------|
| Critical | -10 | Missing labels, keyboard traps, no alt text, zero contrast |
| Serious | -5 | No focus indicator, non-descriptive links, missing headings |
| Moderate | -2 | Inconsistent nav, positive tabIndex, heading gaps |
| Minor | -1 | Missing ARIA on decorative elements |

### PR Blocking Rule

Block PR when **any** of:
- 1+ critical violations
- 1+ regressions (resolved finding reappears)
- 5+ serious violations

## Operating Modes

| Mode | Trigger | Behavior |
|------|---------|----------|
| **Guidance** | `/review --a11y`, direct questions | Human-readable examples, no file writes |
| **Audit** | `/audit --a11y` | JSON-only output, read-only (no Write/Edit) |
| **Fix** | `/fix --a11y` | JSON status + code edits, surgical changes only |
| **Close** | `/audit --close` | Update known-findings DB, JSON confirmation |

## Routing

| Intent | Command | When |
|--------|---------|------|
| Audit violations | `/audit --a11y` | "audit accessibility" |
| Fix violations | `/fix --a11y` | "fix a11y", fix top N |
| Close finding | `/audit --close <id>` | Mark resolved |
| Review compliance | `/review --a11y` | "review accessibility" |

## Data Store

```
.epost-data/a11y/
├── fixes/
│   ├── findings/     ← audit-a11y reports (audit-YYMMDD-HHMM.json)
│   ├── patches/      ← fix-a11y diffs (finding-{id}-YYMMDD.diff)
│   └── reviews/      ← review-a11y reports (review-YYMMDD-HHMM.json)
├── README.md
├── analysis.md       ← trend summary
└── known-findings.json (v1.3 schema)
```

Schema: `.claude/assets/known-findings-schema.json`
Each finding: `id`, `platform`, `wcag`, `title`, `file_pattern`, `code_pattern`, `fix_template`, `priority` (1–3), `resolved`, `resolved_date`, `fix_applied`, `source`, `first_detected_date`.

On first run, any a11y command creates missing directories and copies `README.md` from assets template.

See `data-store` skill for directory convention and gitignore rules.
