---
name: brutal-review
description: Use when user wants brutally honest feedback on business ideas, plans, pitches, or strategies. Triggers on "brutal feedback", "honest review", "devil's advocate", "red team", "tear apart", "critique", "what's wrong with this", "find holes in", "challenge this idea", or requests for harsh/critical evaluation.
user-invocable: true
argument-hint: <idea or plan to review>
---

# BRUTAL Review

## Overview

Parallel critical analysis using three distinct critic personas at escalating intensity, followed by synthesis with meta-analysis. Each persona uses a different analytical framework to ensure comprehensive coverage.

## Quick Reference

| Code | Persona | Intensity | Framework |
|------|---------|-----------|-----------|
| `da` | Devil's Advocate | Mild | Assumption Autopsy + Bias Scan + Inversion + Steelman |
| `rt` | Red Team | Medium | Attack Surface Mapping + Threat Sweep + Adversary Sims + Pre-Mortem |
| `gr` | Gordon Ramsay | Intense | Plate Inspection Scores + Bollocking Triplets + Non-Negotiable Fixes |
| _(none)_ | All three | Full | Parallel dispatch + synthesis + meta-analysis |

## When NOT to Use

- Factual or data-driven assessments (this is opinion-based critique)
- When user wants encouragement or validation
- Technical code review (use code review tools instead)
- When the idea is already in execution and needs operational help, not critique

## Persona Selector

$ARGUMENTS may optionally start with a persona code (`da`, `rt`, or `gr`). Parse the first token:

- **If first token is a persona code:** Run only that agent. Strip the code from $ARGUMENTS. Skip synthesis — deliver agent output directly.
- **Otherwise (default):** Run all three. Full synthesis.

**Examples:**
- `/brutal-review da My SaaS idea...` — Devil's Advocate only
- `/brutal-review rt My SaaS idea...` — Red Team only
- `/brutal-review gr My SaaS idea...` — Gordon Ramsay only
- `/brutal-review My SaaS idea...` — All three + synthesis

## Workflow

```
$ARGUMENTS
    ↓
Parse persona selector
    ↓
Detect language (default: Danish)
    ↓
┌── Single agent? ──┐
│ yes               │ no
▼                   ▼
Run selected    ┌───┼───┐
agent only      ▼   ▼   ▼
│              DA  RT  GR
▼               └───┼───┘
Deliver             ↓
directly      Synthesize + Meta
                    ↓
              Deliver report
```

## Dispatch

Read full agent prompts from `references/prompts.md`. Before dispatching, replace `$ARGUMENTS` with the idea text and append a language instruction line: `Respond entirely in [detected language].`

**All three (default):** Spawn three `Task` calls in a **single message** (parallel). Results return together before your next turn.

**Single agent:** One `Task` call for the selected persona. No synthesis needed.

Settings for each Task call:
- `subagent_type`: `"general-purpose"`
- `model`: `"sonnet"`

## Synthesis (all-three mode only)

When all three return, synthesize into this structure. Adapt headings to user's language:

```
# BRUTAL Review: [Idea title]

## Overall Verdict
[2-3 sentences integrating all three perspectives]

## The Three Critics

### Devil's Advocate (Mild)
[Verdict + top 3 sleep-on-it questions + steelman alternative]

### Red Team (Medium)
[Pre-mortem + kill shot ranking + top adversary simulation]

### Gordon Ramsay (Intense)
[First bite + plate scores + top 3 non-negotiable fixes]

## Common Themes
[What did ALL three flag? Intersection = highest-confidence signal]

## Disagreements
[Where did they diverge? What does the divergence tell us?]

## Meta-Analysis
YOUR OWN assessment:
- Was anything exaggerated or theatrical?
- What blind spots do the critics share?
- Real risk vs. theoretical concern?
- What did the DA's "one thing stronger than they think" reveal?

## Next Steps
[Top 3 actions, synthesized from all critics, ordered by impact]
```

## If Sub-Agent Fails

Continue with available critiques. Note which perspective is missing and how it limits the analysis.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Sequential dispatch | ALL 3 Task calls in a single message |
| Forgetting meta-analysis | ALWAYS add your own assessment — you are the senior partner |
| Copy-pasting sub-agent output | Synthesize: find patterns, contradictions, consensus |
| Skipping common themes | The overlap between critics is the highest-confidence signal |
| Same intensity across all 3 | DA=constructive doubt, RT=adversarial attack, GR=standards fury |
