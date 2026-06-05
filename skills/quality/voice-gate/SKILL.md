---
name: voice-gate
description: Line-editor pass on any content draft against a client voice guide. Flags cadence issues, signature-move overuse, voice-guide violations, receipt gaps — things a rule-based gate can't catch. Use after /content-gate and before human review.
---

# /voice-gate — The Line Editor

Run a subjective-voice review of a drafted piece against a client's voice guide. Produces a structured editorial report with severity-ranked issues, verbatim quotes, rule citations, and direction for human-editor fixes.

This is the complementary pass to `/content-gate`. Rule-based gates (Four U's, banned words, SEO lint) catch mechanical quality issues. Voice Gate catches what they can't: sing-songy cadence, signature-move overuse, voice-guide violations that require interpretation, receipt gaps, and flow. Claude Code's session executes the judge prompt inline — no external API, no script wrapper, no env vars.

## Preamble

```bash
source "$(dirname "$0")/../lib/preamble.sh"
```

## Arguments

Required:
- **file path**: Path to the draft markdown file to review.

Optional:
- **--voice-guide <path>**: Path to the client's writing guide. If omitted, auto-discovered (see Step 1).
- **--persona <path>**: Path to the writer persona file for extra biographical context. Optional but improves flag specificity.
- **--max-issues <n>**: Cap the number of issues in the report. Default 30.

Example: `/voice-gate clients/GrowthModeOn/outputs/blog-posts/how-to-write-a-podcast-pitch.md`
Example: `/voice-gate path/to/draft.md --voice-guide path/to/writing-guide.md --persona path/to/persona.md`

## The Skill

### Step 1: Resolve Arguments

Parse ARGUMENTS. The first positional argument is the draft file path. Use the Read tool to validate it exists. If the draft is not a readable markdown file, stop and tell the user: `"Draft not found: {path}. Pass a valid markdown file path."`

**Resolve the voice guide:**
- If `--voice-guide <path>` is provided, use that path.
- Otherwise, auto-discover. Walk up from the draft's directory until you find an `outputs/personas/` directory (or a plain `personas/` directory). Inside, look for a file matching `*-writing-guide.md`. The canonical convention is `clients/<client>/outputs/personas/<writer>-writing-guide.md`. Pick the first match in the closest candidate directory.
- If no match is found, stop and tell the user: `"No voice guide found. Pass --voice-guide <path> explicitly, or place a *-writing-guide.md file in the nearest outputs/personas/ directory."`

**Resolve the persona (optional):**
- If `--persona <path>` is provided, use it.
- Otherwise, look in the same directory as the resolved voice guide for a sibling `*-persona.md` whose basename prefix matches the writing guide (e.g. `lexie-smith-writing-guide.md` → `lexie-smith-persona.md`). If found, use it. If not, proceed without a persona.

**Resolve max-issues:** default `30`. Parse `--max-issues <n>` if present and coerce to an integer.

### Step 2: Read Inputs

Use the Read tool to load:
- The draft file (full text).
- The voice guide (full text).
- The persona file (full text, if resolved).

If any required file fails to read, surface the error and stop.

### Step 3: Load the Judge Prompt

Use the Read tool to load `voice-gate/judge-prompt.md` from this skill's own directory. This is the rubric Claude applies to produce the editorial report. If the file is missing, stop and tell the user: `"Voice Gate judge prompt missing at voice-gate/judge-prompt.md. Re-install the skill."`

### Step 4: Execute the Judge Prompt (inline)

You (Claude) are the judge. There is no external API call. Apply the judge prompt against the three inputs: the draft text, the voice guide text, and (if present) the persona text. Produce a structured editorial report that conforms to the output contract defined in `judge-prompt.md`.

Hard requirements on the report — these are non-negotiable:
- Every issue cites a **verbatim quote** from the draft (never a paraphrase).
- Every issue references a **specific rule** — a numbered section of the voice guide (e.g., "Voice guide §11 DO #4"), a named signature-move cap ("I repeat — cap 1, count 3"), or a named editorial principle when the voice guide is silent ("Editorial: triple-list cadence monotony").
- Severity is one of: **High** (publish-blocking), **Medium** (meaningful craft issue), **Low** (polish).
- Recommended fixes are **direction only**, never rewrites. The human editor owns the rewrite.
- If the total issue count exceeds `max_issues`, include only the top `max_issues` by severity and note in the Summary Table that the cap was hit.

### Step 5: Write the Report

Derive the report path: `<draft-path-without-extension>.VOICE-GATE.md`. Example: `.../how-to-write-a-podcast-pitch.md` → `.../how-to-write-a-podcast-pitch.VOICE-GATE.md`.

Use the Write tool to save the report at that path.

### Step 6: Compute the Verdict

Count issues by severity. Apply the verdict logic:

- **PASS**: 0 High issues AND ≤3 Medium issues. Message: `"Ready for human review."`
- **HOLD**: 1–2 High issues OR >3 Medium issues (and no FAIL triggers). Message: `"Moderate edits needed. See report."`
- **FAIL**: 3+ High issues OR any voice-guide hard-rule violation. Hard-rule violation triggers:
  - A Tier 1 banned word from the voice guide's DON'T list appears in the draft.
  - A year-count canonicalization rule is violated (e.g., the guide canonicalizes "15+ years" but draft says "13 years" or "11 years").
  - An AI-slop phrase the guide explicitly flags appears ("In conclusion," "delve," "innovative," "disruptive," "holistic," etc., per the guide's forbidden list).
  - The cold-open rule for SEO posts is violated (e.g., "Hey guys" opening a blog post).

  Message: `"Blocking issues. Fix before human review."`

### Step 7: Display the Summary

Print a concise scorecard:

```
VOICE GATE REPORT
═══════════════════════════════════════════
File:        {draft_filename}
Voice guide: {voice_guide_filename}
Persona:     {persona_filename or "—"}
Report:      {report_path}

Issues:      {total} total
  High:      {high}
  Medium:    {medium}
  Low:       {low}

VERDICT: {PASS | HOLD | FAIL}
{verdict_message}

Top 3 issues:
  1. [{severity}] {category} — {one_line_summary}
  2. [{severity}] {category} — {one_line_summary}
  3. [{severity}] {category} — {one_line_summary}

Full report: {report_path}
```

### Step 8: Save the Gate Log

Append a log entry to `~/.kai-marketing/gates/{date}-{slug}-voice.json` — where `{date}` is today's date in `YYYY-MM-DD` and `{slug}` is the draft filename stem. One log file per draft per day (overwrite if the file already exists).

```json
{
  "file": "{draft_path}",
  "voice_guide": "{voice_guide_path}",
  "persona": "{persona_path or null}",
  "report_path": "{report_path}",
  "verdict": "{PASS|HOLD|FAIL}",
  "high_count": {n},
  "medium_count": {n},
  "low_count": {n},
  "total_count": {n},
  "timestamp": "{ISO datetime}"
}
```

## Error Handling

- **Draft file not found**: Stop. Tell user the exact path checked.
- **Voice guide not resolvable**: Stop. Tell user to pass `--voice-guide <path>` explicitly.
- **Judge prompt file missing**: Install error. Tell user: `"Voice Gate judge prompt missing at voice-gate/judge-prompt.md. Re-install the skill."`
- **Draft exceeds ~40K words**: Proceed, but add a note at the top of the report: `"Draft exceeds the comfortable review window; the report may be partial."`
- **Voice guide lacks numbered rules**: The judge falls back to editorial-principle citations. Add a note at the top of the report: `"Voice guide lacks numbered rules — citations use editorial principles only."`

## Chain State

**Reads from:** the draft, the voice guide, the persona (if present), `voice-gate/judge-prompt.md`
**Writes to:**
- `<draft-path-stem>.VOICE-GATE.md` — the editorial report (alongside the draft)
- `~/.kai-marketing/gates/{date}-{slug}-voice.json` — log entry

**Read by:** Human editor who opens the report for triage. Optionally re-read by `/content-retro` downstream.

## When to Use This Skill

**Use it:**
- For any client with a written voice guide (`outputs/personas/*-writing-guide.md`).
- After `/content-gate` passes — it is the subjective complement to the rule-based gate.
- On blog posts, LinkedIn articles, newsletters, long-form content.
- Any time a reviewer has flagged "this doesn't sound like them" on prior drafts.

**Skip it:**
- Ad copy (voice matters less than claim-compliance; `/content-gate` is enough).
- Technical documentation, product release notes.
- Content without a written voice standard — the gate has nothing to score against.
- When the voice owner is about to read the draft themselves within an hour.

## Pipeline Position

```
draft agent  →  /content-gate (rule-based)  →  /voice-gate (subjective)  →  human review  →  publish
```
