---
name: agent-performance
description: Track and report agent invocation metrics including usage counts, success/failure rates, and completion times. Use for understanding which agents are utilized, identifying underused agents, and optimizing agent delegation patterns.
source_urls:
  - https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
---

# Agent Performance Dashboard

## Purpose

Provides visibility into agent usage patterns to optimize delegation and identify improvement opportunities.

## When I Activate

I automatically load when you mention:

- "agent performance" or "agent metrics"
- "agent dashboard" or "agent usage"
- "which agents are used" or "underutilized agents"
- "agent success rate" or "agent statistics"

## What I Do

1. **Track Invocations**: Record agent usage via workflow tracker
2. **Measure Success**: Track completion rates per agent
3. **Analyze Patterns**: Identify usage trends and gaps
4. **Generate Reports**: Create actionable dashboards

## Quick Start

```
User: "Show me agent performance metrics"
Skill: *activates automatically*
       "Generating agent performance report..."
```

## Core Capabilities

### 1. Report Generation

Generate a performance report by reading workflow logs and aggregating agent metrics:

```
User: "Generate agent performance report"
```

Report includes:

- Invocation counts per agent
- Success/failure rates
- Average completion times (when tracked)
- Underutilized agents list
- Recommendations for optimization

### 2. Live Tracking

Track agent invocations during workflow execution using the existing `workflow_tracker`:

```python
# Already available in .claude/tools/amplihack/hooks/workflow_tracker.py
from workflow_tracker import log_agent_invocation

log_agent_invocation(
    agent_name="architect",
    purpose="Design authentication module",
    step_number=2
)
```

### 3. Metrics Storage

Metrics are stored in:

- **Raw logs**: `.claude/runtime/logs/workflow_adherence/workflow_execution.jsonl`
- **Aggregated**: `.claude/runtime/metrics/agent_performance.yaml`

## Report Format

### Summary Dashboard

```yaml
# Agent Performance Summary
# Generated: 2025-11-25

total_invocations: 142

agents:
  architect:
    invocations: 45
    success_rate: 95.6%
    avg_duration_ms: 2340
    trend: increasing

  builder:
    invocations: 38
    success_rate: 89.5%
    avg_duration_ms: 4520
    trend: stable

  reviewer:
    invocations: 25
    success_rate: 100%
    avg_duration_ms: 1890
    trend: increasing

underutilized:
  - database (0 invocations in last 30 days)
  - integration (2 invocations in last 30 days)
  - patterns (3 invocations in last 30 days)

recommendations:
  - Consider using database agent for schema work
  - Integration agent available for external service connections
  - Patterns agent can identify reusable solutions
```

## Implementation Guide

### To Generate a Report

1. Read workflow execution logs:

   ```
   Read: .claude/runtime/logs/workflow_adherence/workflow_execution.jsonl
   ```

2. Filter for `agent_invoked` events:

   ```json
   { "event": "agent_invoked", "agent": "architect", "purpose": "...", "step": 2 }
   ```

3. Aggregate by agent name:
   - Count invocations
   - Calculate success rates from workflow_end events
   - Compute average durations

4. Identify underutilized agents:
   - List all available agents from `.claude/agents/amplihack/`
   - Compare against invocation counts
   - Flag agents with <5 invocations in analysis period

5. Write report to:
   ```
   .claude/runtime/metrics/agent_performance.yaml
   ```

### Available Agents Inventory

**Core Agents** (6):

- architect, builder, reviewer, tester, optimizer, api-designer

**Specialized Agents** (25):

- ambiguity, amplifier-cli-architect, analyzer, azure-kubernetes-expert
- ci-diagnostic-workflow, cleanup, database, documentation-writer
- fallback-cascade, fix-agent, integration, knowledge-archaeologist
- memory-manager, multi-agent-debate, n-version-validator, patterns
- philosophy-guardian, pre-commit-diagnostic, preference-reviewer
- prompt-writer, rust-programming-expert, security, visualization-architect
- worktree-manager, xpia-defense

**Note**: Agent count may change as specialized agents are added/removed. Use `ls .claude/agents/amplihack/specialized/` for current count.

## Tracking Best Practices

### When Invoking Agents

Always log invocations for accurate tracking:

```python
# Before invoking an agent via Task tool
log_agent_invocation(
    agent_name="security",
    purpose="Audit authentication implementation",
    step_number=7  # Optional: link to workflow step
)

# Then invoke the agent
Task(subagent_type="security", prompt="...")
```

### Workflow Integration

The DEFAULT_WORKFLOW.md specifies agent delegation at each step. This skill helps verify adherence:

- Step 1: prompt-writer
- Step 2: architect
- Step 3: builder
- Step 4: tester
- Step 5: reviewer
- etc.

## Configuration

| Setting                   | Default                  | Description                            |
| ------------------------- | ------------------------ | -------------------------------------- |
| `ANALYSIS_DAYS`           | 30                       | Days of history to analyze             |
| `UNDERUTILIZED_THRESHOLD` | 5                        | Invocations below this = underutilized |
| `METRICS_FILE`            | `agent_performance.yaml` | Output file name                       |

## Philosophy Alignment

This skill follows:

- **Ruthless Simplicity**: Uses existing infrastructure (workflow_tracker)
- **Zero-BS**: No placeholders, working aggregation logic
- **Modular Design**: Self-contained skill, clear boundaries
- **Emergence**: Insights emerge from simple tracking patterns

## Interpreting Metrics

### Success Rate Guidelines

| Rate      | Assessment      | Action                                     |
| --------- | --------------- | ------------------------------------------ |
| 95-100%   | Excellent       | Maintain current patterns                  |
| 85-94%    | Good            | Review occasional failures for patterns    |
| 70-84%    | Needs Attention | Investigate failure causes, adjust prompts |
| Below 70% | Critical        | Agent may need redesign or prompt overhaul |

### Invocation Volume Interpretation

- **High volume (30+ in 30 days)**: Core workflow agent, ensure reliability
- **Medium volume (10-29)**: Regular use, monitor for optimization opportunities
- **Low volume (5-9)**: Specialized use case, verify still needed
- **Very low (<5)**: Consider if agent is discoverable or relevant

### Duration Benchmarks

- **< 2 seconds**: Fast execution, typical for simple analysis
- **2-10 seconds**: Normal for moderate complexity
- **10-60 seconds**: Expected for deep analysis or multi-step tasks
- **> 60 seconds**: May indicate inefficiency, consider optimization

## Empty State Handling

When no log data exists (new project or logs cleared):

```yaml
# Agent Performance Report
# Period: Last 30 days
# Status: No data available

summary:
  total_invocations: 0
  message: "No agent invocations logged yet"

getting_started:
  - "Agent tracking begins when workflow_tracker logs invocations"
  - "Ensure agents are invoked via Task tool with proper logging"
  - "First report available after initial workflow execution"

next_steps:
  - "Run a workflow task to generate initial data"
  - "Verify workflow_tracker is properly configured"
  - "Check .claude/runtime/logs/ directory exists"
```

## Limitations

This skill has the following constraints:

1. **Depends on workflow_tracker**: Only tracks agents invoked through the logging system
2. **No real-time metrics**: Reports are generated on-demand, not streamed
3. **Historical data only**: Cannot predict future usage patterns
4. **Manual log analysis**: Does not auto-detect anomalies or alert on issues
5. **Single-project scope**: Metrics are per-project, no cross-project aggregation
6. **Time-based only**: No correlation with code quality or PR outcomes
