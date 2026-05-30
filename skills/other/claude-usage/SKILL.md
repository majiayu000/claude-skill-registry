---
name: claude-usage
description: Report ground-truth Claude token consumption and estimated cost by parsing JSONL session files directly. Use when checking API spend, auditing token usage by project/session/model, generating daily/weekly/monthly cost reports, or diagnosing ccusage undercounting. Includes subagent files that ccusage ignores.
---

# Claude Usage

Ground-truth token usage and cost reporting for Claude Code sessions. Parses JSONL files directly—parent sessions and subagent sidechains—to produce accurate numbers.

## Why This Exists

ccusage (v18+, the standard community tool with 10.6k stars) **undercounts output tokens by 77-94%** for heavy users:

| Source | Output Tokens | Notes |
|--------|-------------|-------|
| Raw JSONL (all files) | 1,076,691 | Ground truth |
| Raw JSONL (date-filtered) | 412,987 | Properly filtered |
| ccusage --timezone UTC | 93,960 | 77% undercount |
| ccusage default | 62,375 | 94% undercount |

Three compounding bugs:
1. **Ignores subagent files** at `{session-uuid}/subagents/{agent-id}.jsonl`—132 files missed on a typical day with Agent Teams
2. **Timezone confusion** between UTC entry timestamps and local time filtering
3. **Drops entries** in parent files—even at UTC, reports only 23% of actual tokens

This script reads every JSONL file to produce correct totals.

---

## Usage

```bash
# Today's usage (default)
python3 ~/.claude/skills/claude-usage/scripts/claude_usage.py

# Last 7 days, broken down by day
python3 ~/.claude/skills/claude-usage/scripts/claude_usage.py --since 7d

# Weekly breakdown for the past month
python3 ~/.claude/skills/claude-usage/scripts/claude_usage.py --by week --since 30d

# Per-model breakdown
python3 ~/.claude/skills/claude-usage/scripts/claude_usage.py --by model --since 7d

# Per-session with human-readable summaries
python3 ~/.claude/skills/claude-usage/scripts/claude_usage.py --by session --since 1d

# Per-project breakdown
python3 ~/.claude/skills/claude-usage/scripts/claude_usage.py --by project --since 7d

# Filter to one project
python3 ~/.claude/skills/claude-usage/scripts/claude_usage.py --project Thera --since 30d

# Custom date range
python3 ~/.claude/skills/claude-usage/scripts/claude_usage.py --since 2026-02-01 --until 2026-02-28

# JSON output (pipe to jq)
python3 ~/.claude/skills/claude-usage/scripts/claude_usage.py --since 7d --json | jq '.grand_total'

# CSV output
python3 ~/.claude/skills/claude-usage/scripts/claude_usage.py --since 7d --csv

# Compare against ccusage (shows delta)
python3 ~/.claude/skills/claude-usage/scripts/claude_usage.py --compare

# PDF report (dark editorial, CTO-ready)
python3 ~/.claude/skills/claude-usage/scripts/claude_usage_report.py --since 30d

# PDF with custom output path
python3 ~/.claude/skills/claude-usage/scripts/claude_usage_report.py --since 30d -o ~/Desktop/feb-usage.pdf

# HTML only (no Playwright needed)
python3 ~/.claude/skills/claude-usage/scripts/claude_usage_report.py --since 7d --html
```

---

## Output Columns

| Column | Description |
|--------|-------------|
| Input | Prompt tokens (charged at input rate) |
| Output | Response tokens (most expensive category) |
| CacheW | Cache write tokens (`cache_creation_input_tokens`) |
| CacheR | Cache read tokens (significantly cheaper than input) |
| Total | Sum of all four token types |
| Cost | Estimated USD from the hardcoded pricing table |

---

## Aggregation Modes (`--by`)

| Mode | Groups by | Example key |
|------|-----------|-------------|
| `day` (default) | Calendar date in local timezone | `2026-02-20` |
| `week` | ISO week number | `2026-W08` |
| `month` | Month | `2026-02` |
| `session` | Session UUID (resolved to summary from sessions-index.json) | `8a6c801a  Working on Claudicle...` |
| `model` | Model name | `claude-opus-4-6` |
| `project` | Project directory (decoded to path) | `~/Desktop/Programming` |

---

## Pricing Table

Prices are hardcoded in the `PRICING` dict at the top of `claude_usage.py`. Update when Anthropic changes rates. Keys are model name substrings matched most-specific-first.

Current defaults (USD per million tokens, verified 2026-02-21):

| Model | Input | Output | Cache Write (1h) | Cache Read |
|-------|-------|--------|-------------------|------------|
| Opus 4.5 / 4.6 | $5.00 | $25.00 | $10.00 | $0.50 |
| Opus 4.0 / 4.1 | $15.00 | $75.00 | $30.00 | $1.50 |
| Sonnet 4.x | $3.00 | $15.00 | $6.00 | $0.30 |
| Haiku 4.5 | $1.00 | $5.00 | $2.00 | $0.10 |
| Sonnet 3.7 / 3.5 | $3.00 | $15.00 | $6.00 | $0.30 |
| Haiku 3.5 | $0.80 | $4.00 | $1.60 | $0.08 |
| Opus 3 | $15.00 | $75.00 | $30.00 | $1.50 |
| Haiku 3 | $0.25 | $1.25 | $0.50 | $0.03 |

Cache write column shows the 1-hour rate (2x base input). Claude Code uses 1-hour prompt caching exclusively. The 5-minute rate (1.25x base input) is also supported when the JSONL `cache_creation` sub-object provides a TTL split.

---

## Timezone Handling

JSONL timestamps are UTC. The script converts to the system's local timezone (or `--tz America/New_York`) before applying `--since`/`--until` filters. This prevents the midnight-boundary confusion that causes ccusage to drop entries when the UTC date differs from the local date.

---

## Data Sources

JSONL files at `~/.claude/projects/{encoded-path}/`:
- **Parent sessions**: `{session-uuid}.jsonl`
- **Subagent sidechains**: `{session-uuid}/subagents/{agent-id}.jsonl`
- **Session metadata**: `sessions-index.json` (summaries for `--by session`)

The script uses streaming line-by-line reads (O(1) memory) to handle files exceeding 300MB.

---

## PDF Reports

`claude_usage_report.py` generates a dark editorial PDF with Crimson Pro + JetBrains Mono typography, gold Minoan accents, bar charts, model distribution with color-coded stacked bars, token composition breakdown, and detailed tables. Designed for executive sharing.

Requires Playwright (`uv pip install --system playwright && playwright install chromium`). Uses Chromium for pixel-perfect CSS rendering—same engine as the Aldea Slide Deck skill. Falls back to HTML output with `--html` flag.

---

## Caveats

- **Estimated accuracy: ~95%.** The remaining gap comes from data residency multipliers (1.1x for US-only inference, not tracked) and potential edge cases in streaming chunk boundaries.
- Streaming chunks are deduplicated by message ID using last-wins strategy—`output_tokens` monotonically increases across chunks, so only the final chunk per message ID has the correct value. Without dedup, costs were overcounted by 2-5x.
- Cost is estimated from the pricing table. Anthropic billing may differ due to batch discounts or promotional pricing.
- Cache write pricing uses the 1-hour rate by default (Claude Code's caching mode). When JSONL provides `cache_creation.ephemeral_5m_input_tokens` / `ephemeral_1h_input_tokens`, rates are split accordingly.
- Synthetic entries (`model: "<synthetic>"`) and billing error entries (all-zero token counts) are automatically filtered.
- Malformed JSON lines and duplicate streaming chunks are counted and reported in the output footer.
- Requires Python 3.9+ for `zoneinfo` module.
- PDF reports require Playwright with Chromium (`playwright install chromium`). Includes a Pricing Methodology section with full rate table, formula, and confidence badge.
