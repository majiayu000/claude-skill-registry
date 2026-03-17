---
name: quick-quality-check
description: Lightning-fast quality check using parallel command execution. Runs theater detection, linting, security scan, and basic tests in parallel for instant feedback on code quality.
tags: [quality, quick, parallel, essential, tier-1]
version: 1.0.0
---

# Quick Quality Check

## Purpose

Run a fast, comprehensive quality check on code in under 30 seconds using parallel execution.

## Specialist Agent

I am a quality assurance specialist focused on rapid feedback loops.

**Methodology** (Parallel Execution Pattern):
1. Spawn swarm with optimal topology for speed
2. Execute independent checks in parallel
3. Aggregate results in real-time
4. Provide instant actionable feedback
5. Prioritize findings by severity

**Checks Performed** (parallel):
- Theater detection (mocks, TODOs, placeholders)
- Style audit (linting, formatting)
- Security scan (vulnerabilities, unsafe patterns)
- Basic test execution
- Token usage analysis

**Output**: Unified quality report with severity-ranked issues

## Input Contract

```yaml
input:
  path: string (file or directory path, required)
  parallel: boolean (default: true)
  quick_mode: boolean (skip deep analysis, default: true)
```

## Output Contract

```yaml
output:
  quality_score: number (0-100)
  issues:
    critical: array[issue]
    high: array[issue]
    medium: array[issue]
    low: array[issue]
  execution_time: number (seconds)
  checks_run: array[string]
```

## Execution Flow

```bash
# Initialize swarm for parallel execution
npx claude-flow coordination swarm-init --topology mesh --max-agents 5

# Spawn specialized agents in parallel
npx claude-flow automation auto-agent --task "Quick quality assessment" --strategy optimal

# Execute all checks in parallel
parallel ::: \
  "npx claude-flow theater-detect '$path' --output theater.json" \
  "npx claude-flow style-audit '$path' --quick --output style.json" \
  "npx claude-flow security-scan '$path' --fast --output security.json" \
  "npx claude-flow test-coverage '$path' --quick --output tests.json" \
  "npx claude-flow analysis token-usage --time-range 1h --output tokens.json"

# Aggregate results
npx claude-flow merge-reports theater.json style.json security.json tests.json tokens.json \
  --output quality-report.json \
  --prioritize severity

# Display summary
cat quality-report.json | jq '.summary'
```

## Integration Points

### Cascades
- Part of `/production-readiness` cascade
- Used by `/code-review-assistant` cascade
- Invoked by `/quick-check` command

### Commands
- Combines: `/theater-detect`, `/style-audit`, `/security-scan`, `/test-coverage`, `/token-usage`
- Uses: `/swarm-init`, `/auto-agent`, `/parallel-execute`

### Other Skills
- Input to `deep-code-audit` skill
- Used by `pre-commit-check` skill
- Part of `continuous-quality` skill

## Usage Example

```bash
# Quick check current directory
quick-quality-check .

# Quick check specific file
quick-quality-check src/api/users.js

# Quick check with detailed output
quick-quality-check src/ --detailed
```

## Failure Modes

- **Insufficient resources**: Reduce parallelism, run sequentially
- **Tests failing**: Flag but continue other checks
- **Security issues found**: Escalate to detailed security review
- **Poor quality score**: Trigger `deep-code-audit` skill
