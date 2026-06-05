---
name: content-write
description: Write content using the most recent brief. Loads framework rules, persona hooks, learned patterns, and skill contract. Auto-runs quality gate on completion.
---

# /content-write — The Content Director

Write a piece of content using the most recent brief from `/content-brief`. Loads the appropriate framework, persona, and learned patterns. Automatically runs the quality gate on completion.

## Preamble

```bash
source "$(dirname "$0")/../lib/preamble.sh"
```

## The Skill

### Step 1: Find the Most Recent Brief

Look for the most recent `.json` file in `~/.kai-marketing/briefs/`. Read it and parse the JSON.

If no brief exists, tell the user: "No brief found. Run `/content-brief {format} {site} \"{keyword}\"` first."

If the brief is older than 7 days, warn: "Brief is {N} days old. Consider re-running `/content-brief` for fresh data."

Display a summary of the brief being used:
```
Using brief: {filename}
  Format:  {format}
  Site:    {site}
  Keyword: {keyword}
  Persona: {persona}
  Angle:   {angle}
```

### Step 2: Load Framework Context

Based on the brief's `format` field, read the corresponding framework files from the knowledge base:

| Format | Framework Files to Read |
|--------|----------------------|
| blog | `knowledge/frameworks/content-copywriting/algorithmic-authorship.md` |
| seo | `knowledge/frameworks/content-copywriting/algorithmic-authorship.md` + `knowledge/frameworks/aeo-ai-search/aeo-ai-search-playbook-2026.md` |
| linkedin | `knowledge/channels/linkedin-articles.md` |
| email-lifecycle | `knowledge/channels/email-lifecycle.md` |
| cold-email | `knowledge/channels/email-lifecycle.md` + `harness/references/cold-email-rules.md` |
| meta-ads | `knowledge/channels/meta-advertising.md` |
| google-ads | `knowledge/channels/paid-acquisition.md` + `harness/references/google-ads-rules.md` |
| press | `knowledge/channels/press-releases.md` |

Also read:
- The persona file from `knowledge/personas/{persona-slug}.md`
- The skill contract from `harness/skill-contracts/{format-slug}.yaml`
- Learned defaults from `~/.kai-marketing/marketing-defaults.md` (if exists)
- Voice profile from `~/.kai-marketing/voice.md` (if exists)

### Step 3: Write the Content

Using all the loaded context (framework rules, persona hooks, brief fields, learned patterns, voice profile, skill contract constraints), write the content piece.

Follow these rules strictly:
- **Word count**: Match the skill contract's word_count field (typically 1200-1800 for blog, shorter for ads/email)
- **Algorithmic Authorship rules** (for SEO content): conditions after main clause, instructions start with verbs, sentences under 20 words, bold the answer not the query
- **Persona voice**: Use the hooks, pain points, and language patterns from the persona file
- **Proof points**: Incorporate the brief's `proof_available` field as evidence
- **Internal links**: Include the brief's `internal_links` naturally
- **CTA**: End with the brief's `cta`

### Step 4: Save the Draft

Save the written content to `~/.kai-marketing/drafts/{date}-{slug}.md` using the Write tool.

### Step 5: Auto-Run Quality Gate

Run the quality gate on the draft:

```bash
kai-gate score ~/.kai-marketing/drafts/{date}-{slug}.md --format json
```

Display the scorecard to the user:
```
QUALITY GATE — {format}
═══════════════════════
Score: {score}/100 ({grade})

  Algorithmic Authorship: {aa_score}%
  GEO/AEO Signals:       {geo_score}%
  Content Structure:      {cs_score}%
  Four U's:              {four_us}/16

Violations: {count}
{top 3 violations with fix suggestions}
```

If the gate **passes** (score >= threshold per skill contract):
- Tell user: "Draft passed quality gate. Run `/content-gate` for full gate proposal, or publish directly."

If the gate **fails**:
- Show the specific failures
- Offer to revise: "Gate failed on {N} rules. Want me to fix the specific violations? (Only failing rules will be revised — passing sections are protected.)"
- If user says yes, revise ONLY the failing dimensions. Max 2 revision attempts.

### Step 6: Log to Content Chain

After gate pass, append to `~/.kai-marketing/content-log.jsonl`:
```json
{"id": "{site}-{format}-{date}", "site": "{site}", "keyword": "{keyword}", "format": "{format}", "publish_date": "{date}", "four_us_score": {score}, "hook_type": "{hook_type}", "persona": "{persona}", "draft_path": "{draft_path}", "performance_30d": null}
```

Create a pending check file at `~/.kai-marketing/pending/{id}.json`:
```json
{"id": "{id}", "url": "", "check_after": "{date+30days}", "status": "pending"}
```

## Error Handling

- **No brief found**: Direct to `/content-brief`
- **Framework file missing**: Warn and write without that framework (log the gap)
- **LLM failure**: Show error, suggest retry
- **Gate failure after 2 retries**: Escalate — show all remaining failures, suggest human review

## Chain State

**Reads from:** `~/.kai-marketing/briefs/{date}-{slug}.json`
**Writes to:** `~/.kai-marketing/drafts/{date}-{slug}.md`, `~/.kai-marketing/content-log.jsonl`
**Read by:** `/content-gate` (if user wants full gate proposal)
