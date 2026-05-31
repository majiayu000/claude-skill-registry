---
name: cost-model
description: Standardized cost-estimation framework for great_cto plans. Forces explicit LLM cost, infra cost, human-supervision time, and the (defensible) human-equivalent comparison. Output format is parsable by the board's /api/cost path — must follow exactly.
when_to_use: |
  Apply when:
  - pm is writing PLAN-*.md and the Cost section is required
  - architect is forecasting LLM burn for a new feature (gate:cost for AI archetypes)
  - any report claims a savings ratio — must show methodology
effort: low
allowed-tools: Read, Write
paths:
  - "docs/plans/**"
  - "docs/architecture/**"
---

# Cost model — make cost claims defensible

great_cto reports cost numbers on the board. Those numbers MUST be
auditable, because a wrong "7,638×" claim killed credibility (see
docs/blog/cost-dashboard-rebuild.md). This skill defines the format.

## The 4-line cost section

Every PLAN-*.md and ARCH-*.md cost section follows this exact template:

```markdown
## Cost estimate

**LLM**: $<low>–<high> (<N> calls × $<per-call avg>)
**Human equiv**: $<low>–<high> (<hours> × $<rate>/h)
**Infra delta**: $<low>–<high>/month
**Time to ship**: <hours> agent-time, <hours> wall-clock

> Methodology: <one-sentence rationale for each range>
```

### Why this exact format?

The board's `getCostHistory()` parser anchors on **line-start** "LLM" and
"Human" labels. Mid-line references are ignored to prevent the
$240-trap regression. Stick to the template.

## How to estimate each line

### LLM cost

For each agent in the pipeline, estimate:
- **Prompt tokens** = (system prompt size) + (context the agent receives)
- **Completion tokens** = (typical output for that agent type)

Quick reference for Sonnet 4 ($3/M in, $15/M out):

| Agent | Typical prompt | Typical output | Per-call cost |
|---|---|---|---|
| architect | 14k | 1.5k | ~$0.06 |
| pm | 6k | 0.6k | ~$0.03 |
| senior-dev | 8k | 0.8k | ~$0.04 |
| qa-engineer | 11k | 0.5k | ~$0.04 |
| reviewer (avg) | 8-12k | 0.6k | ~$0.04 |
| security-officer | 12k | 1k | ~$0.05 |
| devops | 9k | 0.8k | ~$0.04 |

For Haiku ($0.80/M / $4/M), divide by ~4. For Opus 4 ($15/M / $75/M),
multiply by ~5.

Sum across the pipeline stages that actually fire (use `gatesFor()` and
`reviewersFor()` from archetypes.ts to know the count).

### Human equiv

The human cost to do the SAME work without agents. This is the "if I
hired a senior engineer, how long would this task take, at what rate?"

- Senior engineer: $120-180/hour (mid-market US/EU)
- Staff engineer / specialist: $200-300/hour
- Domain expert (security, compliance): $250-400/hour

Estimate hours conservatively. A "small feature" the LLM does in 15
minutes might take a human 2-4 hours (it's never just the typing).

### Infra delta

Only count what's NEW. If the feature adds a Redis instance, count
Redis. If it adds 10MB/month of S3 storage, that's noise — don't list.

### Time to ship

Two numbers — both useful:
- **Agent-time**: wall-clock of LLM calls (typically 5-30 min)
- **Wall-clock**: actual elapsed including human gates (typically hours
  to days)

## Sanity check before writing

Before committing the section to the plan, verify:

```
ratio = human_equiv / llm_cost
```

If `ratio > 1000`, something is wrong. Common bugs:

| Bug | How to detect | Fix |
|---|---|---|
| Wrong unit ($ vs ¢) | LLM cost ends in /M tokens not $ | Convert: tokens / 1M × price |
| Counting savings not spend | "Human time saved" not "Human cost" | Use cost of doing it, not value of skipping |
| Mid-line label pollution | Plan has "$X LLM | $Y human" on one line | Use multi-line format from template |
| Forecast vs actual mixed | LLM forecast counts toward total_llm | Separate forecast section if needed |

## Cost gates

For AI archetypes (`mlops`, `ai-system`, `agent-product`), the pipeline
opens `gate:cost` after architect's forecast. CTO must approve the
projected monthly burn before senior-dev starts.

Use the GATE template:

```markdown
## Gate:cost forecast

| Production volume | Monthly LLM cost |
|---|---|
| 1K req/day | $X |
| 10K req/day | $Y |
| 100K req/day | $Z |

Recommended monthly cap: $<cap>
Triggers above cap: <what alerts fire, who gets paged>
```

## Anti-patterns

❌ **Round-number theatre.** "$0.50 LLM | $7,500 human" — looks
suspicious. Use realistic ranges: "$0.50–1.20 | $225–360".

❌ **Single point estimates.** Always provide a range. Single numbers
hide uncertainty.

❌ **No methodology line.** Just numbers without rationale is unverifiable.

❌ **Hand-waved infra.** "Some hosting cost" is not a number. Either give
$, or say "infra: no change."

## Example — good

```markdown
## Cost estimate

**LLM**: $0.75–1.85 (3 tasks × $0.25–0.62 per Sonnet call)
**Human equiv**: $225–300 (1.5–2h × $150/h, mid-market senior)
**Infra delta**: $0/month (uses existing Express + Postgres)
**Time to ship**: ~15min agent-time, ~3h wall-clock (1 human gate)

> Methodology: tasks sized by line-count estimate; per-call cost from
> historical Sonnet 4 averages on this archetype's plans.
```

Ratio = 300/1.85 = **162×**. Plausible. Defensible.
