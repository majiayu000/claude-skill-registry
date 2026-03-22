---
name: grok-research
description: "Investigate a topic with Grok 4.1 via OpenRouter and generate a Markdown report with a timeline, verifiable claims, and sources (web/X). Use it when the user says “investiga…”, “haz research…”, “averigua…”, “búscame fuentes…”, “research…”, “look into…”, or when you need fast, source-backed research (news, rumors, product/policy changes, competitive context)."
---

# Grok Research (OpenRouter + Grok 4.1)

This skill automates a source-backed “deep dive” on a recent topic using Grok 4.1 via OpenRouter. Output is a Markdown report with citations.

## Quick start

1) Export the API key:

```bash
export OPENROUTER_API_KEY="..."
```

2) Run the script:

```bash
node skills/grok-research/scripts/grok-research.js --topic "What's going on with …" --out report.md
```

By default it tries to use `x-ai/grok-4.1-fast:online`. If your account/model uses a different id, pass `--model` or set `GROK_RESEARCH_MODEL`.

## Environment variables

- `OPENROUTER_API_KEY` (required)
- `GROK_RESEARCH_MODEL` (optional) (default: `x-ai/grok-4.1-fast:online`)
- `OPENROUTER_SITE_URL` (optional) (recommended header by OpenRouter)
- `OPENROUTER_APP_NAME` (optional) (recommended header by OpenRouter)

## Useful flags (script)

- `--topic "..."`: topic to research (or first positional argument)
- `--out report.md`: saves the report and prints the resulting path to stdout
- `--model <id>`: forces the OpenRouter model id
- `--max-tokens 2200`, `--temperature 0.2`: length/style controls

## Recommended workflow (agent)

1) Clarify the goal: “do you want an executive summary or a decision-making report?”
2) Ask for constraints: country/language, time window (last 24/72h), and any specific claims to verify.
3) Run `scripts/grok-research.js` and review the **Claims & verification** section:
   - If sources are weak/missing, re-run with higher `--max-tokens` or narrow the topic.
4) If the topic is sensitive/controversial, ask the model to list alternative hypotheses and what evidence would falsify/confirm each.

## Resources

- Main script: `scripts/grok-research.js`
- API notes: `references/api_reference.md`
