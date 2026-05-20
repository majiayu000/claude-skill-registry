---
name: agentv-trace-analyst
description: >-
  Analyze AgentV evaluation traces and result JSONL files using `agentv trace` and `agentv compare` CLI commands.
  Use when asked to inspect AgentV eval results, find regressions between AgentV evaluation runs,
  identify failure patterns in AgentV trace data, analyze tool trajectories, or compute cost/latency/score statistics
  from AgentV result files.
  Do NOT use for benchmarking skill trigger accuracy, analyzing skill-creator eval performance,
  or measuring skill description quality — those tasks belong to the skill-creator skill.
---

# AgentV Trace Analyst

Analyze evaluation traces headlessly using `agentv trace` primitives and `jq`.

## Primitives

```bash
# List result files (most recent first)
agentv trace list [--limit N] [--format json|table]

# Show results with trace details
agentv trace show <result-file> [--test-id <id>] [--tree] [--format json|table]

# Percentile statistics
agentv trace stats <result-file> [--group-by target|dataset|test-id] [--format json|table]

# A/B comparison between runs
agentv compare <baseline.jsonl> <candidate.jsonl> [--threshold 0.1] [--format json|table]
```

## Analysis Workflow

### 1. Discover results

```bash
agentv trace list
```

Pick the result file to analyze. Most recent is first.

### 2. Get overview

```bash
agentv trace stats <result-file>
```

Read the percentile table. Key signals:
- **score p50 < 0.8**: Significant quality issues
- **latency p90 > 30s**: Performance bottleneck
- **cost p99 spike**: Outlier cost tests to investigate
- **tool_calls p90 >> p50**: Some tests are much chattier

### 3. Investigate failures

```bash
agentv trace show <result-file> --format json | jq '[.[] | select(.score < 0.8) | {test_id, score, assertions: [.assertions[] | select(.passed | not)], trace: {tools: (.trace.tool_calls | keys)}, duration_ms, cost_usd}]'
```

For each failing test, examine:
- **assertions (failed)**: What criteria were not met? (filter for `passed: false`)
- **trace.tool_calls**: Did the agent use expected tools?
- **duration_ms**: Did it time out or run too long?
- **reasoning**: Why did the evaluator score it low?

### 4. Inspect specific tests

```bash
# Flat view with trace summary
agentv trace show <result-file> --test-id <id>

# Tree view (if output messages available)
agentv trace show <result-file> --test-id <id> --tree
```

The tree view shows the agent's execution path — LLM calls interspersed with tool invocations. Look for:
- **Excessive tool calls**: Agent looping or exploring unnecessarily
- **Missing tools**: Expected tool not called
- **Long durations**: Specific tool calls that are slow

### 5. Compare runs

```bash
agentv compare <baseline.jsonl> <candidate.jsonl>
```

Look for:
- **Wins vs losses**: Net improvement or regression?
- **Mean delta**: Overall direction of change
- **Per-test deltas**: Which tests regressed?

### 6. Group analysis

```bash
# By target provider
agentv trace stats <result-file> --group-by target

# By dataset
agentv trace stats <result-file> --group-by dataset
```

Compare providers side-by-side: which is cheaper, faster, more accurate?

## Advanced Queries with jq

All commands support `--format json` for piping to `jq`:

```bash
# Top 3 most expensive tests
agentv trace show results.jsonl --format json \
  | jq 'sort_by(-.cost_usd) | .[0:3] | .[] | {test_id, cost: .cost_usd, score}'

# Tests where token usage exceeds 10k
agentv trace show results.jsonl --format json \
  | jq '[.[] | select(.token_usage.input + .token_usage.output > 10000) | {test_id, tokens: (.token_usage.input + .token_usage.output)}]'

# Score distribution by dataset
agentv trace show results.jsonl --format json \
  | jq 'group_by(.dataset) | .[] | {dataset: .[0].dataset, count: length, avg_score: ([.[].score] | add / length)}'

# Tool usage frequency across all tests
agentv trace show results.jsonl --format json \
  | jq '[.[].trace.tool_calls // {} | to_entries[]] | group_by(.key) | .[] | {tool: .[0].key, total_calls: ([.[].value] | add)}'

# Find regressions > 0.1 between two runs
agentv compare baseline.jsonl candidate.jsonl --format json \
  | jq '.matched[] | select(.delta < -0.1) | {test_id: .testId, delta, from: .score1, to: .score2}'
```

## Reasoning Patterns

When analyzing traces, think about:

1. **Efficiency**: Are tool calls/tokens proportional to task complexity? High tokens-per-tool may indicate verbose prompts or unnecessary context.

2. **Error patterns**: Do failures cluster by target, dataset, or tool usage? Common patterns:
   - Tool errors → agent can't access required resources
   - High LLM calls with low tool calls → agent stuck in reasoning loop
   - Missing tool calls → wrong tool routing

3. **Cost optimization**: Identify tests with high cost but acceptable scores — can they use a cheaper model? Compare `--group-by target` stats.

4. **Latency distribution**: P50 vs P99 spread indicates consistency. Large spread means unpredictable performance — investigate P99 outliers.

5. **Regression detection**: After a prompt/config change, compare before/after. Mean delta > 0 is good, but check individual test regressions — a few large losses can hide behind many small wins.
