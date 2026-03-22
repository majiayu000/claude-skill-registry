---
name: cco-pipeline
description: "Use this to generate UGC content scripts for Martinican influencers. Takes a validated product brief and runs the 4-step CCO chain: trend deconstruction, cultural mapping, script generation with slang injection, and authenticity validation."
---

# CCO Pipeline — 4-Step Content Generation

Transform a validated product brief into an authentic Martinican UGC script using the Chief Creative Officer prompt chain. Every step must complete before the next begins. A REJECT at step 4 restarts from step 2.

## Prerequisites

- Validated brief at `campaigns/<brand>-<date>/brief.json` with `status: "validated"`
- Access to `forge/lexicon/martinique_slang.json`
- Access to Martinique_DB via MCP (optional but preferred for step 2)

## The 4-Step Chain

### Step 1 — Deconstruction

Find 2-3 currently trending video formats on TikTok/Instagram Reels (from CMO trend feed or manual input).

For each trending format, extract:
- **Hook** (first 3 seconds — what stops the scroll)
- **Stakes/Conflict** (what is at play, why should the viewer care)
- **Pacing** (fast cuts / slow vlog / talking head / POV)
- **CTA** (what the viewer is supposed to feel or do)

Output: `campaigns/<brand>-<date>/trend_deconstruction.json`

### Step 2 — Cultural Mapping

For each deconstructed trend, replace every foreign cultural reference with a Martinican equivalent.

Mapping rules:
- Locations → Martinican communes, beaches, landmarks (Les Salines, Rocher du Diamant, Fort-de-France centre)
- Food references → local equivalents (colombo, accras, bokit, ti-punch)
- Traffic/commute stress → embouteillages à la Lézarde, TCSP wait times
- Weather → specific Martinican seasons (carême, hivernage)
- Social dynamics → family structure, matador role, voisinage
- Query Martinique_DB `search_culture` tool for additional grounding if available

Output: `campaigns/<brand>-<date>/cultural_map.json`

### Step 3 — Script Generation & Slang Injection

Write a 30-second TikTok script for the assigned influencer.

Script format:
```
[HOOK — 0-3s]: <exact words or action>
[VISUAL CUE]: [B-ROLL: describe shot]
[BODY — 4-25s]: <voiceover or dialogue>
[PRODUCT INTEGRATION — natural, not forced]: <how product appears>
[CTA — 26-30s]: <closing line>
[CAPTION]: <suggested caption with 3-5 hashtags>
```

Slang injection rules:
- Pull 2-4 expressions from `forge/lexicon/martinique_slang.json` that match the tone
- Use Creole expressions in the exact context they appear in real conversation — never as decoration
- French must sound like spoken Martinican French, not metropolitan French
- Product name appears max 2 times (once visual, once verbal)

### Step 4 — CCO Authenticity Validation

Review the generated script as a strict Martinican creative director.

Ask:
1. Does this sound like a Martinican creator or an AI trying to sound Caribbean?
2. Are the Creole expressions used correctly in context (not awkwardly inserted)?
3. Is the product integration natural or does it feel like a pause-for-ad?
4. Would a 25-year-old from Fort-de-France cringe at this?
5. Does it pass the "could only be Martinique" test — or could it be Guadeloupe, Réunion, or any tropical destination?

Output: `APPROVE` or `REJECT <specific rewrite instructions>`

- **APPROVE** → write final script to `campaigns/<brand>-<date>/scripts/<influencer_id>.md`
- **REJECT** → return to Step 2 with rewrite instructions. Max 3 rejection cycles, then surface to human.

## Loop Limit

If Step 4 rejects 3 times for the same script, do NOT loop again. Write a `HUMAN_REVIEW_NEEDED.md` file explaining what the CCO keeps rejecting and why, and surface to the user.

## Output Structure

```
campaigns/<brand>-<date>/
  brief.json               ← validated brief (from product-brief skill)
  trend_deconstruction.json
  cultural_map.json
  scripts/
    influencer_2.md        ← approved script per influencer
    influencer_5.md
  status.json              ← current pipeline stage + timestamps
```
