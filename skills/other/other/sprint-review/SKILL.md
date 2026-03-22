---
name: sprint-review
description: "Use when generating sprint review presentations: gathers sprint data from work items and git, generates a python-pptx script, and produces a branded PowerPoint slide deck."
effort: medium
argument-hint: "[--sprint <YYYY-MM>] [--iteration <name>]"
tags: [presentation, sprint, reporting, sdlc]
requires:
  anyBins:
  - gh
  - az
  bins:
  - python3
---



# Sprint Review

## Purpose

Generate branded sprint review PowerPoint presentations using python-pptx. Each invocation produces a NEW python-pptx script tailored to the current sprint's data -- the script is regenerated every time, not reused from a static template.

## Trigger

- Command: `/ai-sprint-review`
- Context: end of sprint, presenting delivered work to stakeholders.

## When to Use

- End of sprint: presenting delivered work to engineers, heads, and managers
- Monthly reviews with stakeholders
- Ad-hoc progress reports for a specific period

## When NOT to Use

- **Daily updates** -- use `/ai-standup`
- **Sprint planning** -- use `/ai-sprint plan`
- **Retrospectives** -- use `/ai-sprint retro`
- **Incident write-ups** -- use `/ai-postmortem`

## Pre-conditions (MANDATORY)

Before gathering data, read configuration:

1. Read `.ai-engineering/manifest.yml` -- focus on the `work_items` section.
2. Determine active provider: `work_items.provider` is either `github` or `azure_devops`.
3. Read provider-specific config:
   - GitHub: `work_items.github.team_label`
   - Azure DevOps: `work_items.azure_devops.area_path`
4. Read quality thresholds from `quality` section (coverage, duplication, cyclomatic, cognitive).

## Procedure

### Step 1 -- Determine Sprint Period

Resolve the date range for data gathering:

| Input | Behavior |
|-------|----------|
| `--sprint YYYY-MM` | Use that calendar month (1st to last day) |
| `--iteration <name>` | Query provider for iteration start/end dates |
| No arguments | Current calendar month |

### Step 2 -- Gather Data

Collect data from three sources in parallel:

#### 2a. Work Items (from provider)

**GitHub:**
```bash
gh issue list --label "<team_label>" --state all \
  --json number,title,state,labels,milestone,closedAt,assignees
```

**Azure DevOps:**
```bash
az boards query --wiql "SELECT [System.Id], [System.Title], [System.State], [System.AssignedTo], [System.WorkItemType] FROM WorkItems WHERE [System.AreaPath] UNDER '<area_path>' AND [System.IterationPath] = @CurrentIteration" --expand relations
```

Categorize each item:
- **Completed**: closed/resolved during the sprint period
- **In Progress**: open, with activity during the sprint
- **Carried Over**: open, existed before sprint start, no completion

Walk the hierarchy when available: Feature > User Story > Task.

#### 2b. Git Activity

```bash
# Commits
git log --since="<start>" --until="<end>" --format="%h|%s|%an" --no-merges

# Merged PRs (GitHub)
gh pr list --state merged --json number,title,mergedAt,author

# Merged PRs (Azure DevOps)
az repos pr list --status completed
```

Derive: commit count, unique authors, LOC delta, files changed.

#### 2c. Quality Metrics

```bash
# Test count
pytest --co -q 2>/dev/null | tail -1

# Lint status
ruff check . --statistics 2>/dev/null
```

Compare actuals against thresholds from `.ai-engineering/manifest.yml` quality section.

### Step 3 -- Generate python-pptx Script

Generate a NEW script each time. Reference `docs/presentations/generate_sprint_review.py` for style conventions. Do NOT copy the old script verbatim -- adapt all content to the current sprint's data.

#### Brand Constants (MUST use these exact values)

```python
AI_BG_DARK = RGBColor(0x0B, 0x11, 0x20)
AI_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
AI_TEXT_PRIMARY = RGBColor(0xE2, 0xE8, 0xF0)
AI_ACCENT = RGBColor(0x00, 0xD4, 0xAA)
AI_PRIMARY = RGBColor(0x1E, 0x3A, 0x5F)
AI_PRIMARY_LIGHT = RGBColor(0x2A, 0x4F, 0x7A)
AI_ERROR = RGBColor(0xEF, 0x44, 0x44)
AI_SUCCESS = RGBColor(0x10, 0xB9, 0x81)
AI_WARNING = RGBColor(0xF5, 0x9E, 0x0B)
AI_TEXT_LIGHT = RGBColor(0xF8, 0xFA, 0xFB)
AI_NEUTRAL = RGBColor(0x64, 0x74, 0x8B)
AI_TEXT_MUTED = RGBColor(0x94, 0xA3, 0xB8)
AI_BORDER_DARK = RGBColor(0x1A, 0x2A, 0x40)
AI_CARD_DARK = RGBColor(0x1E, 0x29, 0x3B)
SEC_BLUE = RGBColor(0x2E, 0x6B, 0xA4)
SEC_PURPLE = RGBColor(0x7B, 0x3F, 0xA0)
```

#### Typography

- Titles/headings: `JetBrains Mono`
- Body text: `Inter`

#### Layout

- 16:9 aspect ratio: 13.333" x 7.5"
- LEFT_MARGIN: 1.2"

#### Helper Functions (include in generated script)

Include these helpers matching the signature patterns in the reference script:
- `add_textbox` -- single-style text box with font, alignment, anchor controls
- `add_rich_textbox` -- multi-line text box with per-line styling (font, size, color, bold)
- `add_accent_bar` -- thin colored horizontal bar
- `add_card` -- filled rectangle with optional border and left accent stripe
- `add_rounded_rect` -- rounded rectangle for badges
- `_add_kpi_card` -- card with large value + small label, centered
- `add_slide_header` -- accent bar + title + optional subtitle
- `_blank_slide` -- blank layout with dark background fill
- `set_notes` -- attach speaker notes to a slide
- `add_styled_table` -- table with colored header row
- `_style_cell` -- style a single table cell (text, font, alignment, fill)
- `_add_feature_card` -- card with title + bullet list and left accent

#### Slide Structure (8-14 slides)

| # | Slide | Content |
|---|-------|---------|
| 1 | **Title** | Project name, sprint period, hero KPI badges |
| 2 | **Sprint Overview** | KPI cards (commits, LOC, PRs merged, coverage) + theme cards |
| 3-N | **Feature Deep-Dives** | One slide per major feature/spec delivered: before/after or bullet cards |
| N+1 | **Quality Metrics** | Table: metric, target, actual, status (color-coded) |
| N+2 | **Risks & Next Sprint** | Risk cards (severity-coded: HIGH=red, MEDIUM=yellow, LOW=teal) + next sprint priorities |
| N+3 | **Q&A** | Thank-you slide with summary badges |

#### Content Rules

- Technical but accessible -- audience is engineers, heads, and managers
- Include speaker notes for EVERY slide (the `set_notes` call)
- Quantify everything: numbers, percentages, before/after comparisons
- Use accent colors to differentiate categories (AI_ACCENT for primary features, SEC_BLUE/SEC_PURPLE/AI_WARNING/AI_ERROR for variety)
- Feature deep-dive slides use `_add_feature_card` for consistent card layout
- KPI cards use `_add_kpi_card` for large-value display

### Step 4 -- Execute and Output

1. Write the generated script to `docs/presentations/generate_sprint_review.py` (overwrite the existing file).
2. Run: `python3 docs/presentations/generate_sprint_review.py`
3. Output file: `docs/presentations/sprint-review-YYYY-MM.pptx`
4. Report to user: slide count, file path, key stats (commits, PRs, coverage).

## Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--sprint YYYY-MM` | current month | Sprint period as year-month |
| `--iteration <name>` | none | Iteration name (queries provider for dates) |

## Quick Reference

```
/ai-sprint-review                          # current month, auto-detect provider
/ai-sprint-review --sprint 2026-03         # March 2026 sprint
/ai-sprint-review --iteration "Sprint 12"  # named iteration from provider
```

## Common Mistakes

1. **Reusing the old script** -- every invocation MUST generate a new script with current data. Never copy-paste the previous script unchanged.
2. **Missing speaker notes** -- every slide must have `set_notes()`. Stakeholders use presenter view.
3. **Wrong color palette** -- use the brand constants above, not arbitrary colors.
4. **Skipping pre-conditions** -- always read `manifest.yml` first to get provider config and quality thresholds.
5. **Hardcoding dates** -- derive the sprint period from arguments or current date, never hardcode.
6. **Missing `python-pptx` import** -- the generated script must import from `pptx` and its submodules.

## Integration

- Reads `work_items` config from `.ai-engineering/manifest.yml`
- Can reference active specs from `.ai-engineering/specs/`
- Quality thresholds from `manifest.yml` quality section drive the metrics table
- Git history and PR data provide quantitative backing for every claim

$ARGUMENTS
