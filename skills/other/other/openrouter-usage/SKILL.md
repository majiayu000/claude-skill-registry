---
name: openrouter-usage
description: Query OpenRouter API costs, credits, and usage breakdown by model, provider, and date. This skill should be used when checking API spending, auditing costs, or generating usage reports for the last 30 days.
---

# OpenRouter Usage

Query OpenRouter API costs and generate usage reports via the command line.

## When to Use

- Checking OpenRouter spend over the last 30 days
- Breaking down costs by model, provider, or date
- Exporting usage data as CSV or JSON for accounting
- Auditing which models and API keys consume the most credits

## Prerequisites

- `OPENROUTER_API_KEY` environment variable (or in a project `.env` file)
- The key **must be a Management key** — create one at https://openrouter.ai/settings/management-keys
- Regular provisioning keys return 401/403 on analytics endpoints

## Usage

```bash
# Full 30-day summary with credits balance
python3 ~/.claude/skills/openrouter-usage/scripts/openrouter_usage.py

# Filter to a single date
python3 ~/.claude/skills/openrouter-usage/scripts/openrouter_usage.py --date 2026-02-01

# Export as CSV (for spreadsheets)
python3 ~/.claude/skills/openrouter-usage/scripts/openrouter_usage.py --csv

# Raw JSON output (for piping to jq)
python3 ~/.claude/skills/openrouter-usage/scripts/openrouter_usage.py --json

# Skip credits lookup (activity only)
python3 ~/.claude/skills/openrouter-usage/scripts/openrouter_usage.py --no-credits
```

## Output

The default report includes:
- **Credits balance**: total purchased, used, remaining
- **Spend by model**: per-model cost with token counts (prompt, completion, reasoning)
- **Spend by provider**: aggregated by provider (OpenAI, Anthropic, Google, etc.)
- **Spend by date**: daily spend with visual bar chart

## API Endpoints

Both endpoints are read-only GETs authenticated via Bearer token:

| Endpoint | Purpose |
|----------|---------|
| `GET /api/v1/credits` | Total credits purchased and used |
| `GET /api/v1/activity` | Last 30 days of usage grouped by model/endpoint/provider |

The activity endpoint returns per-row: `date`, `model`, `provider_name`, `usage`, `byok_usage_inference`, `requests`, `prompt_tokens`, `completion_tokens`, `reasoning_tokens`.
