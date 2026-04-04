---
name: agent-benchmark
description: Framework for measuring and tracking agent response quality over time. Detects regressions before they reach production. Use when evaluating agent changes, auditing quality, or establishing performance baselines.
---

# Agent Benchmark Framework

Without benchmarks, we cannot know whether agent changes improve or degrade quality. This skill defines how to measure, track, and protect agent performance.

## When to Activate

- Before and after modifying any agent definition file
- When adding a new skill that an agent depends on
- Periodic quality audits (weekly/monthly)
- When a user reports degraded agent output
- Before promoting an agent from experimental to production

## Core Concepts

### Why Benchmarks Matter

Agent quality degrades silently. A prompt tweak that improves one response can break ten others. Without a baseline to compare against, every change is a guess. Benchmarks make quality visible and regressions detectable.

### Benchmark Types

| Type | Scope | Cost | Frequency |
|------|-------|------|-----------|
| Prompt Benchmark | Single agent, single task | Low | Every agent change |
| Task Benchmark | End-to-end scenario | Medium | Feature changes |
| Regression Suite | All critical agents | High | Weekly / before release |

## Directory Structure

```
~/.claude/benchmarks/
  fixtures/
    code-reviewer/
      missing-error-handling.ts      # Input: code with no try/catch
      sql-injection.py               # Input: unparameterized query
      clean-code.ts                  # Input: code with no issues
    security-reviewer/
      hardcoded-secret.ts            # Input: API key in source
      parameterized-query.py         # Input: safe query (no findings expected)
    verifier/
      passing-build/                 # Input: project that builds
      failing-types/                 # Input: project with type errors
  ground-truth/
    code-reviewer/
      missing-error-handling.json    # Expected findings
      sql-injection.json             # Expected findings
      clean-code.json                # Expected: empty findings
    security-reviewer/
      hardcoded-secret.json
      parameterized-query.json
  rubrics/
    code-reviewer.md                 # Scoring rubric
    security-reviewer.md
    verifier.md
  baselines/
    code-reviewer-2026-03-01.json    # Timestamped baseline scores
    code-reviewer-2026-03-26.json
    security-reviewer-2026-03-26.json
  results/
    run-2026-03-26T14-00.json        # Latest run output
```

## Scoring Rubric Template

Each agent has its own rubric file. The template:

```markdown
## [Agent Name] Scoring Rubric

### Completeness (0-30 points)
Did the agent find everything it should have found?

- Found all expected issues: 30
- Missed 1 non-critical issue: 22
- Missed 1 critical issue: 10
- Missed 2+ issues: 5
- Found nothing when issues exist: 0

### Accuracy (0-30 points)
Were the findings correct? No false positives?

- All findings verified correct: 30
- 1 false positive: 22
- 2 false positives: 12
- 3+ false positives: 5
- Majority of findings are wrong: 0

### Actionability (0-20 points)
Did the agent give concrete, implementable fixes?

- Clear fix with file/line reference: 20
- Clear fix without location: 14
- Vague suggestion (refactor this): 7
- No fix suggested: 0

### Format Compliance (0-20 points)
Did the output follow the agent's output contract?

- Matches contract exactly (VERDICT + sections): 20
- Minor deviation (missing one section): 12
- Major deviation (no VERDICT): 5
- Unstructured free text: 0
```

## Ground Truth Format

Ground truth files define what a correct agent response must contain:

```json
{
  "fixture": "missing-error-handling.ts",
  "agent": "code-reviewer",
  "required_findings": [
    {
      "id": "missing-try-catch",
      "severity": "HIGH",
      "description_contains": ["error handling", "try", "catch"],
      "location_hint": "fetchUserData"
    }
  ],
  "forbidden_findings": [],
  "required_verdict": "FAIL",
  "min_score": 70
}
```

## Scoring Logic

### How a Run Is Scored

```
1. Load fixture (input code / task)
2. Run agent with fixture as input
3. Parse agent output
4. Check required_findings: each found = +completeness points
5. Check forbidden_findings: each false positive = -accuracy points
6. Check verdict matches required_verdict
7. Check format follows output contract
8. Sum scores → final 0-100
9. Compare against min_score threshold
```

### Score Interpretation

| Score | Status | Action |
|-------|--------|--------|
| 90-100 | EXCELLENT | No action needed |
| 75-89 | GOOD | Minor tuning optional |
| 60-74 | WARN | Investigate degradation |
| 40-59 | POOR | Agent needs rework |
| 0-39 | CRITICAL | Block deployment |

## Running Benchmarks

### Run All Benchmarks

```bash
# Full suite
node ~/.claude/benchmarks/run.mjs

# Output: results/run-{timestamp}.json
```

### Run Single Agent

```bash
# Benchmark one agent
node ~/.claude/benchmarks/run.mjs --agent code-reviewer

# With verbose output (shows actual vs expected per fixture)
node ~/.claude/benchmarks/run.mjs --agent code-reviewer --verbose
```

### Compare Against Baseline

```bash
# Compare latest run against saved baseline
node ~/.claude/benchmarks/run.mjs --compare

# Compare specific run against specific baseline
node ~/.claude/benchmarks/run.mjs \
  --compare results/run-2026-03-26.json \
  --baseline baselines/code-reviewer-2026-03-01.json
```

### Update Baseline

Only run this after verifying an improvement is real:

```bash
# Promote latest results to new baseline
node ~/.claude/benchmarks/run.mjs --baseline update

# Creates: baselines/{agent}-{date}.json
```

## Regression Detection Rules

A regression is triggered when:

1. **Score drops more than 10 points** on any single fixture
2. **Average score drops more than 5 points** across all fixtures for an agent
3. **A previously PASS fixture becomes FAIL**
4. **Format compliance drops below 80** (agent stopped following output contract)

### Regression Report Format

```
REGRESSION DETECTED: code-reviewer

Fixture: sql-injection.py
  Baseline score:  88
  Current score:   61
  Delta:           -27 (CRITICAL)

  Missing finding: SQL injection in execute_query() line 14
  Root cause: Agent definition changed, removed security focus

  Recommendation: Revert agent change or add SQL injection examples
```

## Metrics Tracked Per Agent

| Metric | Formula | Target |
|--------|---------|--------|
| accuracy | correct_findings / total_findings | >= 0.85 |
| completeness | found_issues / total_issues | >= 0.90 |
| false_positive_rate | false_positives / total_findings | <= 0.10 |
| format_compliance | correct_format_runs / total_runs | >= 0.95 |
| response_time_p50 | median seconds to complete | <= 30s |
| response_time_p95 | 95th percentile seconds | <= 60s |
| token_usage_avg | average tokens per run | tracked only |
| pass_rate | fixtures scoring above min_score | >= 0.80 |

## Per-Agent Benchmark Definitions

### code-reviewer

Fixtures: 6 (2 missing error handling, 2 code smell, 1 SQL injection, 1 clean code)
Pass threshold: 70/100
Critical findings: error handling, injection vulnerabilities, magic numbers
Non-critical findings: naming conventions, comment quality

### security-reviewer

Fixtures: 8 (hardcoded secrets, injection flaws, auth bypass, safe code)
Pass threshold: 75/100
Zero tolerance: must find all HIGH/CRITICAL security issues
Acceptable miss: LOW severity cosmetic issues only

### verifier

Fixtures: 4 (passing build, type errors, failing tests, lint errors)
Pass threshold: 80/100
Critical: must correctly identify PASS vs FAIL state
Scoring focus: verdict accuracy over prose quality

### sleuth (bug investigator)

Fixtures: 5 (null pointer, race condition, wrong logic, correct code)
Pass threshold: 65/100
Critical: must identify root cause, not just symptom
Scoring focus: root cause analysis depth

## Baseline Management

### Baseline File Format

```json
{
  "agent": "code-reviewer",
  "created_at": "2026-03-26T00:00:00Z",
  "commit": "abc1234",
  "scores": {
    "missing-error-handling": 88,
    "sql-injection": 92,
    "clean-code": 95,
    "code-smell-nesting": 79,
    "magic-numbers": 82,
    "dead-code": 76
  },
  "aggregate": {
    "average": 85.3,
    "min": 76,
    "max": 95,
    "pass_rate": 1.0
  }
}
```

### Baseline Lifecycle

```
Create baseline → Make changes → Run benchmark →
Compare → PASS (no regression) → Update baseline
                               → FAIL (regression) → Fix and rerun
```

## CI Integration

### GitHub Actions Example

```yaml
name: Agent Benchmark
on:
  push:
    paths:
      - '.claude/agents/**'
      - '.claude/skills/**'

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run agent benchmarks
        run: node ~/.claude/benchmarks/run.mjs --compare

      - name: Comment PR with results
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const results = require('./benchmark-output.json')
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              body: formatBenchmarkResults(results)
            })

      - name: Fail on regression
        run: |
          node ~/.claude/benchmarks/run.mjs --check-regression
          # Exits non-zero if regression > 10 points on any fixture
```

## Benchmark Authoring Guide

### Writing a Good Fixture

A good benchmark fixture is:

1. **Realistic** - Code that could exist in a real project
2. **Focused** - Tests one specific thing the agent should find
3. **Unambiguous** - The ground truth is objectively correct
4. **Minimal** - No unnecessary noise that could confuse the agent

### Example: Good Fixture (code-reviewer)

```typescript
// fixtures/code-reviewer/missing-error-handling.ts
// BENCHMARK: Agent must find missing error handling in fetchUser

async function fetchUser(id: string) {
  const response = await fetch(`/api/users/${id}`)
  const data = await response.json()
  return data
}

export default fetchUser
```

Ground truth:
```json
{
  "required_findings": [{
    "severity": "HIGH",
    "description_contains": ["error handling", "network", "try"],
    "location_hint": "fetchUser"
  }],
  "required_verdict": "FAIL",
  "min_score": 70
}
```

### Example: Bad Fixture (too complex)

Do not create fixtures with 10 different issues. The agent may find 7, miss 3, and you cannot tell if the misses are regressions or noise. One fixture = one primary concern.

## Integration with Canavar

When a benchmark run produces a regression, log it to the Canavar error ledger:

```bash
node ~/.claude/hooks/dist/canavar-cli.mjs errors
```

Canavar cross-training means a regression in code-reviewer will inject a warning into all producer agents that use code-reviewer output, preventing cascading quality failures.

## Quick Reference

```bash
# Before changing an agent:
node ~/.claude/benchmarks/run.mjs --agent code-reviewer --save-as before

# After changing the agent:
node ~/.claude/benchmarks/run.mjs --agent code-reviewer --compare before

# Full regression check:
node ~/.claude/benchmarks/run.mjs --compare --fail-on-regression

# Update baselines after confirmed improvement:
node ~/.claude/benchmarks/run.mjs --baseline update
```

---

**Remember**: A benchmark suite that is never run is decoration. Run benchmarks before every agent change. Protect quality proactively, not reactively.
