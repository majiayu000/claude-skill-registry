---
name: cortex-skills-loop
description: "Drives the cortex skills recommend-feedback-rate loop. Use when a context change occurs (new file types, domain shift, task pivot) or when a task completes and skill effectiveness should be recorded."
---

# Cortex Skills Loop

## Overview

The cortex CLI includes an AI-powered recommendation engine that learns from usage patterns. This
skill establishes the workflow for participating in that learning loop: get recommendations when
context shifts, provide feedback on recommendation quality, and rate skills after use. Each
interaction improves future recommendations.

## When to Engage

### Signals That Trigger Recommendations

Run `cortex skills recommend` when any of these mismatch signals appear:

- **File pattern shift** — `git diff` or the working set includes file types not covered by
  active skills (e.g., `.tf` Terraform files appear but no infrastructure skill is active,
  or `**/auth/**` paths get touched without security skills loaded)
- **Agent activation change** — a new agent gets activated that likely has complementary skills
  not yet loaded (the recommender maps agents to skill sets internally)
- **Explicit domain pivot** — the user switches focus to a different domain ("now let's handle
  the database migrations") and the current skill set is oriented elsewhere
- **Skill gap felt** — a task requires domain knowledge that no active skill covers, or an
  active skill is providing no value to the current work

### Signals That Trigger Rating/Feedback

- **Task completion** — a skill was active during work that just finished successfully
- **Recommendation acted on** — a recommendation was recently followed or dismissed
- **Negative experience** — a skill actively misled or produced unhelpful guidance

### When Not to Engage

Do **not** run recommendations on every session start or for routine tasks where the active
skill set is clearly appropriate. The loop adds value through selective, signal-driven use.

## Workflow

### 1. Recommend — Surface Relevant Skills

When a context change is detected, run:

```bash
cortex skills recommend
```

This analyzes the current git state, active agents, and historical patterns to suggest skills
grouped by confidence level:

- **High confidence (>=0.8):** Auto-activate candidates — consider activating immediately
- **Medium confidence (0.6-0.8):** Worth reviewing with the user
- **Low confidence (<0.6):** Informational only

To check what is currently active before acting on recommendations:

```bash
cortex status
```

For full option details: `cortex skills recommend --help`

### 2. Feedback — Improve Recommendation Quality

After a recommendation has been acted on (activated or dismissed), record whether it was useful:

```bash
cortex skills feedback <skill-name> helpful --comment "Caught auth vulnerability early"
cortex skills feedback <skill-name> not-helpful --comment "Not relevant to this API work"
```

Positive feedback with context available teaches the recommender to associate the current
project context with that skill for future sessions. Always provide a `--comment` when possible
to enrich the learning signal.

For full option details: `cortex skills feedback --help`

### 3. Rate — Record Skill Effectiveness

After a task completes and a skill was active during the work, rate its contribution:

```bash
cortex skills rate <skill-name> --stars <1-5> --review "Description of experience"
```

Additional flags to enrich the signal:

- `--helpful` / `--not-helpful` — binary usefulness indicator
- `--succeeded` / `--failed` — whether the task the skill supported succeeded

Ratings feed back into the recommendation engine. Highly rated skills get prioritized in
future suggestions; low-rated skills get demoted.

To view existing ratings before adding one: `cortex skills ratings <skill-name>`

To discover top-performing skills: `cortex skills top-rated`

For full option details: `cortex skills rate --help`

## Closing the Loop

The recommend-feedback-rate cycle is cumulative. Each interaction updates the SQLite-backed
learning database, improving four recommendation strategies:

1. **Semantic similarity** — embeds successful session contexts for future matching
2. **Rule-based** — matches file patterns to skill suggestions
3. **Agent-based** — maps active agents to complementary skills
4. **Pattern-based** — promotes skills with high historical success rates

When multiple strategies converge on the same skill, confidence gets boosted. Consistent
feedback and ratings are what make this convergence happen over time.

## Quick Reference

| Action | Command |
|--------|---------|
| Get recommendations | `cortex skills recommend` |
| Check current status | `cortex status` |
| Give positive feedback | `cortex skills feedback <skill> helpful --comment "..."` |
| Give negative feedback | `cortex skills feedback <skill> not-helpful --comment "..."` |
| Rate a skill (1-5 stars) | `cortex skills rate <skill> --stars N --review "..."` |
| View skill ratings | `cortex skills ratings <skill>` |
| See top-rated skills | `cortex skills top-rated` |
| View usage analytics | `cortex skills analytics` |
