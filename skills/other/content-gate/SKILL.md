---
name: content-gate
description: Run the full quality gate on any content file. Score against 28 rules, apply policy, show detailed scorecard with fix suggestions. Works on any markdown file.
---

# /content-gate — Quality Assurance

> **See also:** `/voice-gate` — the complementary subjective-voice pass. Run `/content-gate` first for mechanical rule checks (banned words, SEO lint, Four U's), then `/voice-gate` for cadence, signature-move overuse, and voice-guide violations that require interpretation.

Run the full quality gate on any content. Scores against 28 rules across 4 categories, applies the approval policy, and produces a detailed scorecard with fix suggestions.

Can be used standalone on any file, or as part of the content sprint chain after `/content-write`.

## Preamble

```bash
source "$(dirname "$0")/../lib/preamble.sh"
```

## Arguments

Optional:
- **file path**: Path to a markdown file to score. If omitted, uses the most recent draft from `~/.kai-marketing/drafts/`.
- **--policy**: Gate policy name (blog-publish, linkedin-article, cold-email, default). Auto-detected from file if omitted.

Example: `/content-gate path/to/article.md --policy blog-publish`
Example: `/content-gate` (uses most recent draft)

## The Skill

### Step 1: Find the Content

If a file path is provided in ARGUMENTS, use that file.

If no file path, find the most recent `.md` file in `~/.kai-marketing/drafts/`. If no drafts exist, tell user: "No draft found. Run `/content-write` first, or provide a file path: `/content-gate path/to/file.md`"

### Step 2: Detect Policy

If `--policy` is specified, use it. Otherwise, detect from the filename or content:
- Contains "blog" or in drafts/ → `blog-publish`
- Contains "linkedin" → `linkedin-article`
- Contains "email" or "cold" → `cold-email`
- Contains "ad" or "meta" or "google" → default (no SEO lint)
- Otherwise → `default`

### Step 3: Run the Gate

Run two commands:

**Score the content:**
```bash
kai-gate score {file} --format json
```

**Run gate decision:**
```bash
kai-gate gate {file} --policy {policy}
```

### Step 4: Display the Scorecard

Present the results:

```
QUALITY GATE SCORECARD
══════════════════════════════════════════

File:   {filename}
Policy: {policy}

OVERALL: {score}/100 ({grade}) — {PASS|FAIL|HOLD}

┌─────────────────────────┬───────┬────────┐
│ Category                │ Score │ Weight │
├─────────────────────────┼───────┼────────┤
│ Algorithmic Authorship  │  {aa}%│  35%   │
│ GEO/AEO Signals        │ {geo}%│  20%   │
│ Content Structure       │  {cs}%│  25%   │
│ Four U's               │{4u}/16│  20%   │
├─────────────────────────┼───────┼────────┤
│ TOTAL                   │{total}│ 100%   │
└─────────────────────────┴───────┴────────┘

VIOLATIONS ({count}):
  {severity} {rule_id}: {description}
    Fix: {suggestion}
    Line: {line_number}

TOP FIXES:
  1. {most impactful fix}
  2. {second most impactful fix}
  3. {third most impactful fix}
```

### Step 5: Gate Decision

Based on the score and policy:
- **PASS** (score >= threshold, no tier-1 banned words): "Content approved. Ready to publish."
- **HOLD** (score close to threshold or policy=hold): "Content held for review. Score: {score}. Threshold: {threshold}."
- **FAIL** (score below threshold or tier-1 violations): "Content rejected. {N} violations must be fixed."

If FAIL, offer to auto-fix: "Want me to revise the draft to fix these {N} violations? (Only failing rules will be touched — passing sections protected.)"

### Step 6: Save Gate Result

Save the gate result to `~/.kai-marketing/gates/{date}-{slug}.json`:
```json
{"file": "{filename}", "policy": "{policy}", "score": {score}, "grade": "{grade}", "status": "{pass|hold|fail}", "violations_count": {N}, "timestamp": "{ISO datetime}"}
```

## Error Handling

- **File not found**: Show helpful message with file path
- **SQLite locked**: Retry once after 1 second, then warn user
- **LLM unavailable** (Four U's scoring): Score without LLM, note "Four U's scored rule-based only (LLM unavailable)"

## Chain State

**Reads from:** `~/.kai-marketing/drafts/{date}-{slug}.md` (or any file)
**Writes to:** `~/.kai-marketing/gates/{date}-{slug}.json`
