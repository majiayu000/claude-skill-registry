---
name: trueskill-rank
description: Domain-agnostic TrueSkill batch ranking via LLM-as-judge. Ranks any list of text items using overlapping subsets dispatched to Codex Spark workers. Swappable rubrics. Use when you need to rank, score, curate, or sort a collection by quality.
---

# TrueSkill Rank

Rank any collection of text items by quality using TrueSkill + LLM-as-judge.

## Setup

```bash
pip install trueskill
```

- **Python 3.11+** required
- **agent-mux** for parallel dispatch (optional -- falls back to direct OpenAI API if `OPENAI_API_KEY` is set)
- **Claude Code:** copy this skill folder into `.claude/skills/trueskill-rank/`
- **Codex CLI:** append this SKILL.md content to your project's root `AGENTS.md`

For the full installation walkthrough (prerequisites, verification, API fallback), see [references/installation-guide.md](references/installation-guide.md).

## Staying Updated

This skill ships with an `UPDATES.md` changelog and `UPDATE-GUIDE.md` for your AI agent.

After installing, tell your agent: "Check `UPDATES.md` in the trueskill-rank skill for any new features or changes."

When updating, tell your agent: "Read `UPDATE-GUIDE.md` and apply the latest changes from `UPDATES.md`."

Follow `UPDATE-GUIDE.md` so customized local files are diffed before any overwrite.

---

## Quick Start

```bash
PYTHON="python3"
CLI="~/.claude/skills/trueskill-rank/scripts/trueskill-rank.py"

# Full pipeline: prepare + dispatch + aggregate
$PYTHON $CLI run \
  --input items.json \
  --overlap 3 \
  --rubric ~/.claude/skills/trueskill-rank/rubrics/practitioner-signal.md \
  --output results.json

# Or step by step:
$PYTHON $CLI prepare --input items.json --overlap 3 \
  --rubric ~/.claude/skills/trueskill-rank/rubrics/practitioner-signal.md \
  --output-dir /tmp/ts-run/
# Dispatch is handled internally by trueskill-rank.py (no separate script needed)
$PYTHON $CLI aggregate --run-dir /tmp/ts-run/ --output results.json
```

Cost: each subset of 10 items produces C(10,2)=45 implicit pairwise comparisons. 100 items at overlap 3 = 30 subsets = 30 API calls = 1,350 implicit comparisons.

## Decision Tree

### Mode Selection

| Question | Answer | Mode |
|----------|--------|------|
| Ranking individual items (messages, posts)? | Yes | `--mode batch` (default) |
| Comparing entities (channels, sources, candidates)? | Yes | `--mode pairwise` |
| Items > 50? | Yes | `--mode batch` (far more efficient) |
| Items < 20, need binary signal? | Yes | `--mode pairwise` |

### Overlap Selection

| Overlap | When to use | Cost |
|---------|-------------|------|
| `--overlap 2` | Quick scan, low stakes, small sets | Lowest |
| `--overlap 3` | Default. Good balance of speed and confidence | Medium |
| `--overlap 4` | High-stakes curation, final rankings | Highest |

### Rubric Selection

| Rubric | Use for |
|--------|---------|
| `practitioner-signal.md` | General content quality. 6 criteria led by practitioner signal |
| `signal-serendipity-entropy.md` | Content curation emphasizing surprise and cross-domain bridges |
| Custom rubric via `--rubric` | Any domain -- create from `example-template.md` |

## Input Format

```json
{"items": [{"id": "item_001", "text": "...", "metadata": {...}}, ...]}
```

Source doesn't matter -- TG messages, HN posts, articles, papers, tweets. The `id` field is required, `text` is the content to rank, `metadata` is optional and passed through to output.

## CLI Reference

### prepare

Generate subsets and prompt files from input items.

```bash
$PYTHON $CLI prepare \
  --input items.json \         # Required. JSON with {"items": [...]}
  --mode batch \               # batch (default) or pairwise
  --overlap 3 \                # 2-4, controls statistical robustness
  --subset-size 10 \           # Items per subset (batch) or matchups per batch (pairwise)
  --rubric rubric.md \         # Required. Scoring criteria file
  --output-dir /tmp/ts-run/ \  # Where to write subsets.json and prompts/
  --seed 42 \                  # Random seed for reproducibility
  --text-cap 1500              # Max chars per item in prompts
```

Output: `subsets.json` + `prompts/subset-NN.txt` (batch) or `prompts/batch-NN.txt` (pairwise)

### aggregate

Parse dispatch results and run TrueSkill rating.

```bash
$PYTHON $CLI aggregate \
  --run-dir /tmp/ts-run/ \     # Directory with subsets.json and results/
  --output results.json        # Final rankings JSON
```

### run

Full pipeline: prepare + dispatch + aggregate.

```bash
$PYTHON $CLI run \
  --input items.json \
  --overlap 3 \
  --rubric rubric.md \
  --output results.json
```

Dispatch runs automatically via the built-in `dispatch_workers()` function. No external scripts required.

## Output Format

```json
{
  "rankings": [
    {"id": "item_001", "mu": 35.2, "sigma": 2.1, "conservative": 28.9,
     "rank": 1, "appearances": 3, "wins": 8, "losses": 2}
  ],
  "stats": {
    "total_items": 100, "subsets": 30, "results_parsed": 30,
    "parse_errors": 0, "coverage_gaps": 0, "mode": "batch",
    "overlap": 3, "rubric": "practitioner-signal"
  }
}
```

`conservative` = mu - 3*sigma. This is the ranking key. Penalizes items with few appearances (high uncertainty).

## Dispatch

Built into `trueskill-rank.py` via `dispatch_workers()`. No external scripts.

Primary: `agent-mux --engine codex --model gpt-5.3-codex-spark --reasoning low --effort low` (free via GPT subscription). Resolves agent-mux via `AGENT_MUX_PATH` env var, then `which agent-mux`, then relative to skill directory. Runs 6 workers in parallel via `concurrent.futures.ThreadPoolExecutor`.

Fallback: If `agent-mux` not found, falls back to direct OpenAI API via `urllib.request` (stdlib, zero deps). Requires `OPENAI_API_KEY` env var. Uses `gpt-4o-mini`. Results written as `{"success": true, "response": "..."}` JSON.

## Creating Custom Rubrics

Copy `rubrics/example-template.md` and fill in:

```markdown
# Rubric Name

## Criteria (ordered by importance)
1. **CRITERION** -- Description
2. **CRITERION** -- Description

## Tiebreaker
How to break ties.

## Context
What kind of content this is for.
```

3-6 criteria recommended. Order matters -- most important first.

---

## Anti-Patterns

| Do NOT | Do Instead |
|--------|------------|
| Use overlap 2 for high-stakes curation | Use overlap 3-4 for reliable rankings |
| Use pairwise mode for 50+ items | Use batch ranking (far more efficient at scale) |
| Skip the rubric file | Always specify a rubric via `--rubric` |
| Run without trueskill installed | `pip install trueskill` first |
| Parse result files manually | Use the `aggregate` subcommand |

## Error Handling

| Problem | Solution |
|---------|----------|
| `trueskill` not installed | `pip install trueskill` |
| agent-mux not found + no `OPENAI_API_KEY` | Install agent-mux or set `OPENAI_API_KEY` env var |
| Parse errors in results | Check result files in `results/` dir, retry failed subsets |
| Coverage gaps in aggregate output | Increase overlap coefficient (`--overlap 3` or `--overlap 4`) |
| Empty items array error | Check input JSON format -- must be `{"items": [...]}` with at least one item |

---

## Bundled Resources Index

| Path | What | When to Load |
|------|------|-------------|
| `./SKILL.md` | Skill runbook (this file) | Always |
| `./UPDATES.md` | Structured changelog for AI agents | When checking for new features or updates |
| `./UPDATE-GUIDE.md` | Instructions for AI agents performing updates | When updating this skill |
| `./scripts/trueskill-rank.py` | Main CLI script -- prepare, dispatch, aggregate | Always (execution) |
| `./references/algorithm.md` | TrueSkill math, N-player mode, convergence, cost scaling | When tuning parameters or understanding ranking behavior |
| `./references/prior-runs.md` | Previous runs with statistics and lessons learned | When calibrating overlap, rubrics, or interpreting results |
| `./references/installation-guide.md` | Detailed install walkthrough for Claude Code and Codex CLI | First-time setup or environment repair |
| `./rubrics/practitioner-signal.md` | General content quality rubric (6 criteria) | Default rubric for most ranking tasks |
| `./rubrics/signal-serendipity-entropy.md` | Curation rubric emphasizing surprise and cross-domain bridges | Content discovery and curation |
| `./rubrics/example-template.md` | Template for creating custom rubrics | When creating a new domain-specific rubric |
