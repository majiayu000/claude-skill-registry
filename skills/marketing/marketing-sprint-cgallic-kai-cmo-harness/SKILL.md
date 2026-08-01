---
name: marketing-sprint
description: Run the full content pipeline in one command — brief, write, gate, log. Progress updates between steps. 5-minute timeout with partial state recovery.
---

# /marketing-sprint — The Full Pipeline

One command, full pipeline. Chains `/content-brief` → `/content-write` → `/content-gate` → log in a single interactive session. Shows progress between each step.

This is the marketing equivalent of gstack's `/ship`.

## Arguments

Required:
- **format**: Content format (blog, seo, linkedin, etc.)
- **site**: Site key
- **keyword**: Target keyword in quotes

Example: `/marketing-sprint blog kaicalls "AI receptionists for law firms"`

## The Skill

### Step 1: Brief (60 seconds)

Show: "Step 1/4: Generating brief..."

Run the brief generation:
```bash
kai-brief --format {format} --site {site} --keyword "{keyword}" --output json
```

Display the brief summary. Save to `~/.kai-marketing/briefs/`.

If brief generation fails, stop and show the error. Save partial state: "Sprint stopped at Step 1. Fix the error and resume with `/content-brief {format} {site} \"{keyword}\"`"

### Step 2: Write (120 seconds)

Show: "Step 2/4: Writing content using {framework} + {persona}..."

Using the brief from Step 1, write the content following the same process as `/content-write`:
- Load framework files
- Load persona
- Load learned defaults
- Write the piece
- Save to `~/.kai-marketing/drafts/`

If writing fails, save partial state with the brief: "Sprint stopped at Step 2. Brief saved. Resume with `/content-write`"

### Step 3: Gate (30 seconds)

Show: "Step 3/4: Running quality gate..."

Score the draft:
```bash
kai-gate score {draft_path} --format json
```

Display the scorecard summary:
```
Gate: {score}/100 ({grade}) — {PASS|FAIL}
  AA: {aa}%  |  GEO: {geo}%  |  CS: {cs}%  |  4U: {4u}/16
```

If gate **fails**: Attempt one auto-revision (fix only failing rules). Re-score. If still fails after 1 retry in sprint mode, show failures and stop: "Sprint paused at gate. Run `/content-gate` to review failures in detail."

### Step 4: Log (5 seconds)

Show: "Step 4/4: Logging content..."

Append to `~/.kai-marketing/content-log.jsonl` and create pending check in `~/.kai-marketing/pending/`.

### Completion

```
MARKETING SPRINT COMPLETE
══════════════════════════════════════════

Brief:    ~/.kai-marketing/briefs/{filename}
Draft:    ~/.kai-marketing/drafts/{filename}
Gate:     {score}/100 ({grade}) — PASS
Logged:   {id} — 30-day check scheduled for {date+30}

Total time: {elapsed}

Next: Publish the draft, then run /content-report in 30 days.
```

## Timeout and Recovery

**Total timeout: 5 minutes.** If any step exceeds its budget:
- Step 1 (brief): 60s
- Step 2 (write): 180s (includes LLM call)
- Step 3 (gate): 60s
- Step 4 (log): 10s

On timeout, save partial state and tell user which step to resume from.

## Error Handling

- **Any step fails**: Save partial state, show which step failed, suggest resume command
- **LLM timeout**: "LLM timed out at Step {N}. Partial state saved. Resume with /{skill_for_step}"
- **Config missing**: Direct to `kai-config init`

## Chain State

**Writes:** Brief, draft, gate result, content log entry, pending check
**Reads:** Config, frameworks, personas, learned defaults
