---
name: content-brief
description: Generate a strategic content brief from format + site + keyword. Auto-resolves persona, pulls GSC data, generates hooks, angles, and competitor weakness via LLM.
---

# /content-brief — The CMO

Generate an 18-field content brief from three inputs. The brief drives everything downstream — `/content-write` reads it, `/content-gate` validates against it, `/content-retro` measures against it.

## Preamble

```bash
source "$(dirname "$0")/../lib/preamble.sh"
```

## Arguments

Parse from ARGUMENTS. All three are required:
- **format**: blog | seo | linkedin | email-lifecycle | cold-email | tiktok | meta-ads | google-ads | press
- **site**: Site key matching config (e.g., kaicalls, abp)
- **keyword**: Target keyword in quotes

Example invocation: `/content-brief blog kaicalls "AI receptionists for law firms"`

## The Skill

### Step 1: Validate Inputs

Check that the format is valid. Valid formats: blog, seo, linkedin, email-lifecycle, cold-email, tiktok, meta-ads, google-ads, press.

If invalid, tell the user: "Unknown format '{X}'. Valid formats: blog, seo, linkedin, email-lifecycle, cold-email, tiktok, meta-ads, google-ads, press."

### Step 2: Generate the Brief

Run this command and capture the JSON output:

```bash
kai-brief --format {format} --site {site} --keyword "{keyword}" --output json
```

If the command fails with a config error (missing API key), tell the user:
"Set your Gemini API key: `kai-config set llm.api_key_env GEMINI_API_KEY` and ensure the env var is set."

If GSC data is unavailable, the brief will still generate — it falls back to LLM-only research. Note this to the user: "GSC data unavailable — brief generated with LLM research only."

### Step 3: Display the Brief

Present the brief fields in a scannable format:

```
CONTENT BRIEF — {format} for {site}
═══════════════════════════════════════

Target keyword:     {keyword}
Secondary keywords: {secondary_keywords}
Format:             {format}
Persona:            {persona}

ANGLE:   {angle}
HOOKS:
  1. {hook_options[0]}
  2. {hook_options[1]}
  3. {hook_options[2]}

Competitor weakness: {competitor_weakness}
Audience pain:       {audience_pain}
Proof available:     {proof_available}
CTA:                 {cta}
Word count target:   {word_count_target}
Internal links:      {internal_links}
```

### Step 4: Save the Brief

Save the brief JSON to `~/.kai-marketing/briefs/{date}-{slug}.json` where:
- `{date}` = today in YYYY-MM-DD format
- `{slug}` = keyword slugified (spaces to hyphens, lowercase, max 40 chars)

Use the Write tool to save. Confirm to user: "Brief saved to ~/.kai-marketing/briefs/{filename}"

### Step 5: Offer Next Step

Tell the user: "Brief ready. Run `/content-write` to generate the draft, or edit the brief first."

## Error Handling

- **Missing API key**: Direct user to `kai-config set llm.api_key_env GEMINI_API_KEY`
- **Invalid format**: List valid formats
- **GSC timeout**: Generate brief without GSC data, note the limitation
- **LLM failure**: Show the error, suggest retrying

## Chain State

**Writes to:** `~/.kai-marketing/briefs/{date}-{slug}.json`
**Read by:** `/content-write` (next in chain)
