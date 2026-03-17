---
name: metrics
description: Collect agent usage metrics from git history and generate health reports.
  Use when measuring agent adoption, reviewing system health, or producing periodic
  dashboards. Implements 8 key metrics from agent-metrics.md.
license: MIT
metadata:
version: 1.0.0
model: claude-haiku-4-5
---

# Agent Metrics Collection Utility

## Purpose

This utility collects and reports metrics on agent usage from git history. It implements the 8 key metrics defined in `docs/agent-metrics.md` for measuring agent system health, effectiveness, and adoption.

## Triggers

| Trigger Phrase | Operation |
|----------------|-----------|
| `collect agent metrics` | Run collect_metrics.py with default 30-day window |
| `generate metrics dashboard` | Run with markdown output for reporting |
| `check agent adoption rate` | Run and highlight Metric 2 (agent coverage) |
| `weekly metrics report` | Run with 7-day window, markdown output |
| `export metrics as JSON` | Run with JSON output for automation |

---

## When to Use

Use this skill when:

- Measuring agent system health or adoption trends
- Producing periodic dashboards or reports
- Evaluating whether agent usage is balanced across types
- Checking infrastructure review coverage

Use manual git log inspection instead when:

- Investigating a single commit's agent attribution
- Debugging a specific CI run's metrics workflow

---

## Process

1. Run the metrics collection script for the desired time range
2. Review generated reports for agent usage patterns
3. Identify trends and anomalies in adoption metrics

---

## Anti-Patterns

| Avoid | Why | Instead |
|-------|-----|---------|
| Running without specifying time window | Default 30 days may not match your intent | Use --since with explicit day count |
| Comparing metrics across different time windows | Misleading trends | Normalize to same window size |
| Ignoring zero agent coverage | Indicates broken detection patterns | Verify commit message conventions match patterns |
| Manual commit counting | Error-prone, misses patterns | Use the script for consistent detection |
| Storing JSON output without markdown | Loses human-readable context | Generate both formats for archival |

---

## Verification

After execution:

- [ ] Script exits with code 0
- [ ] Output contains all 4 collected metrics (Invocation Rate, Coverage, Infrastructure Review, Distribution)
- [ ] Agent coverage percentage is plausible (not 0% unless truly no agent commits)
- [ ] Time window matches intended period
- [ ] For markdown output: report file created at expected path

---

## Available Scripts

| Script | Platform | Usage |
|--------|----------|-------|
| `collect_metrics.py` | Python 3.8+ | Cross-platform |

## Quick Start

```bash
# Basic usage (30 days, summary output)
python .claude/skills/metrics/collect_metrics.py

# Last 90 days as markdown
python .claude/skills/metrics/collect_metrics.py --since 90 --output markdown

# JSON output for automation
python .claude/skills/metrics/collect_metrics.py --output json
```

## Metrics Collected

The utility collects the following metrics:

| Metric | Description | Target |
|--------|-------------|--------|
| Metric 1: Invocation Rate | Agent usage distribution | Proportional to task types |
| Metric 2: Agent Coverage | % of commits with agent involvement | 50% |
| Metric 4: Infrastructure Review | % of infra changes with security review | 100% |
| Metric 5: Usage Distribution | Agent utilization patterns | Balanced distribution |

## Detection Patterns

### Agent Detection

The utility detects agents in commit messages using these patterns:

- Direct agent names: `orchestrator`, `analyst`, `architect`, etc.
- Review attribution: `Reviewed by: security`
- Agent tags: `agent: implementer` or `[security-agent]`

### Infrastructure Files

Infrastructure commits are identified by these patterns:

- `.github/workflows/*.yml`
- `.githooks/*`
- `Dockerfile*`
- `*.tf`, `*.tfvars`
- `.env*`
- `.agents/*`

### Commit Types

Conventional commit prefixes are classified:

- `feat:` - Feature
- `fix:` - Bug fix
- `docs:` - Documentation
- `ci:` - CI/CD
- `refactor:` - Refactoring

## Output Formats

### Summary (Default)

Human-readable console output with key metrics highlighted.

### Markdown

Formatted markdown suitable for dashboards and reports. Can be saved directly to `.agents/metrics/` for archival.

### JSON

Structured data for programmatic consumption and CI integration.

## CI Integration

See `.github/workflows/agent-metrics.yml` for automated weekly metrics collection.

The workflow:

1. Runs weekly on Sundays
2. Collects metrics for the previous 7 days
3. Generates a markdown report
4. Creates a PR with the report (if significant changes)

## Manual Report Generation

To generate a monthly dashboard report:

```bash
# Generate report
python .claude/skills/metrics/collect_metrics.py \
    --since 30 \
    --output markdown \
    > .agents/metrics/report-$(date +%Y-%m).md

# Review and commit
git add .agents/metrics/
git commit -m "docs(metrics): add monthly metrics report"
```

## Extending the Utility

### Adding New Metrics

1. Define the metric in `docs/agent-metrics.md`
2. Add collection logic to both scripts
3. Update the output formatters
4. Add tests if applicable

### Adding New Agent Patterns

Update the `AGENT_PATTERNS` / `$AgentPatterns` arrays to detect new agent references.

### Adding Infrastructure Patterns

Update the `INFRASTRUCTURE_PATTERNS` / `$InfrastructurePatterns` arrays for new infrastructure file types.

## Troubleshooting

### No Agents Detected

- Ensure commit messages reference agents explicitly
- Check that conventional commit format is used
- Verify the patterns match your team's conventions

### Git Errors

- Confirm you're in a git repository
- Check that the repository has commits in the date range
- Verify git is available in PATH

## Related Documents

- [Agent Metrics Definition](../../../docs/agent-metrics.md)
- [Dashboard Template](../metrics/dashboard-template.md)
- [Baseline Report](../metrics/baseline-report.md)
- [CI Workflow](../../../.github/workflows/agent-metrics.yml)
