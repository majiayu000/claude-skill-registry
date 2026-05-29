---
name: agent-analytics
description: Tracks key performance indicators (KPIs) for AI Agents: Token Usage, Task Duration, Loop Cycles, and Success Rate.
triggers: [analytics, metrics, tokens used, cost tracking, performance report, agent stats]
context_cost: low
---

# Agent Analytics Skill

## Goal
Provide visibility into the "Black Box" of agent execution by tracking cost (tokens) and efficiency (time/loops).

## Flow

### 1. Metric Capture
**Input**: Completion of a Task / Tool Call / Phase.
**Action**: Log the following structured data:
*   `timestamp`: ISO 8601
*   `agent_id`: Loki / Claude / Gemini
*   `task_id`: T-NNN
*   `tokens_in`: (Estimated)
*   `tokens_out`: (Estimated)
*   `duration_ms`: Execution time
*   `status`: SUCCESS | FAILURE | RETRY

### 2. Analysis & Alerts
*   **Loop Detection**: If `task_id` appears > 5 times in `metrics.log` with `status: RETRY`, trigger `human_escalation`.
*   **Cost Anomaly**: If `tokens_out` > 5000 for a simple task, flag as "Verbose/Inefficient".

### 3. Reporting
**Command**: `generate-report`
**Output**: `metrics/weekly_report.md`
*   Total Tokens consumed.
*   Average Task Duration.
*   Success Rate % (First-pass vs Retry).

## Storage
*   `agents/memory/metrics/analytics.jsonl` (Append-only log)
