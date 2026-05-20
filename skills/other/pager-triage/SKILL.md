---
name: pager-triage
version: 0.1.2
displayName: PagerDuty Incident Triage
description: >
  AI-powered incident triage for PagerDuty. List active incidents, deep-dive
  with timeline and alert correlation, check on-call schedules, acknowledge,
  resolve, and annotate — all from your agent. Read-only by default;
  write operations require explicit --confirm.
author: Anvil AI
tags:
  - pagerduty
  - opsgenie
  - incident
  - sre
  - oncall
  - triage
  - discord
  - discord-v2
tools:
  - name: pd_incidents
    description: List active PagerDuty incidents (triggered + acknowledged)
  - name: pd_incident_detail
    description: Get detailed incident info including timeline, alerts, and notes
  - name: pd_oncall
    description: Show current on-call schedules and escalation policies
  - name: pd_incident_ack
    description: Acknowledge an incident (requires --confirm)
  - name: pd_incident_resolve
    description: Resolve an incident (requires --confirm)
  - name: pd_incident_note
    description: Add a note to an incident (requires --confirm)
  - name: pd_services
    description: List PagerDuty services and their current status
  - name: pd_recent
    description: Show recent incidents for a service (last 24h/7d/30d)
---

# PagerDuty Incident Triage

AI-powered incident triage for PagerDuty. Read-only by default. Write operations require explicit confirmation.

## When to Activate

Use this skill when the user:

- Asks **"what's firing?"**, **"any incidents?"**, **"what's on fire?"**, or anything about active alerts
- Mentions **PagerDuty**, **pager**, **on-call**, or **incidents**
- Asks **"who's on call?"** or **"who's oncall right now?"**
- Wants to **acknowledge**, **resolve**, or **add a note** to an incident
- Says **"triage"**, **"incident response"**, or **"what happened last night?"**
- Asks about **service health** or **recent incidents** for a service

## Quick Setup

### 1. Create a PagerDuty API Key

1. Go to **PagerDuty → Settings → API Access Keys**
2. Click **"Create New API Key"**
3. Name it `OpenClaw Agent`
4. Select **Read-only** (recommended for triage; choose Full Access only if you need ack/resolve)
5. Copy the key

### 2. Set Environment Variables

```bash
# Required — your PagerDuty REST API v2 token
export PAGERDUTY_API_KEY="u+your_key_here"

# Optional — required only for write operations (ack, resolve, note)
export PAGERDUTY_EMAIL="you@company.com"
```

### 3. Verify

Ask your agent: **"What's firing on PagerDuty?"**

## Subcommands Reference

### Read Operations (always safe, no confirmation needed)

---

#### `incidents` — List Active Incidents

Lists all triggered and acknowledged incidents, sorted by urgency.

```
pager-triage incidents
```

**Example output:**
```json
{
  "tool": "pd_incidents",
  "provider": "pagerduty",
  "timestamp": "2026-02-16T03:45:00Z",
  "total_incidents": 3,
  "incidents": [
    {
      "id": "P123ABC",
      "incident_number": 4521,
      "title": "High CPU on prod-web-03",
      "status": "triggered",
      "urgency": "high",
      "service": { "id": "PSVC123", "name": "Production Web" },
      "created_at": "2026-02-16T03:00:00Z",
      "assignments": [{ "name": "Jane Doe", "email": "..." }],
      "alert_count": 3,
      "escalation_level": 1,
      "last_status_change": "2026-02-16T03:05:00Z"
    }
  ],
  "summary": "3 active incident(s): high (triggered) x1, high (acknowledged) x1, low (triggered) x1"
}
```

---

#### `detail <incident_id>` — Incident Deep Dive

Full incident details including timeline (log entries), related alerts, notes, and automated analysis.

```
pager-triage detail P123ABC
```

**Example output (abbreviated):**
```json
{
  "tool": "pd_incident_detail",
  "incident": {
    "id": "P123ABC",
    "title": "High CPU on prod-web-03",
    "status": "triggered",
    "urgency": "high",
    "service": { "id": "PSVC123", "name": "Production Web" },
    "escalation_policy": { "name": "Production Escalation" },
    "assignments": [{ "name": "Jane Doe", "escalation_level": 1 }]
  },
  "timeline": [
    { "type": "trigger_log_entry", "created_at": "...", "summary": "Incident triggered via Prometheus Alertmanager" },
    { "type": "escalate_log_entry", "created_at": "...", "summary": "Escalated to Jane Doe (Level 1)" }
  ],
  "alerts": [
    { "id": "A456DEF", "severity": "critical", "summary": "CPU > 95% on prod-web-03", "source": "Prometheus Alertmanager" }
  ],
  "notes": [],
  "analysis": {
    "alert_count": 3,
    "escalation_count": 1,
    "acknowledged": false,
    "trigger_source": "Prometheus Alertmanager"
  }
}
```

---

#### `oncall` — On-Call Schedules

Shows who's currently on call across all schedules and escalation policies.

```
pager-triage oncall
```

**Example output:**
```json
{
  "tool": "pd_oncall",
  "oncalls": [
    {
      "user": { "name": "Jane Doe", "email": "jane@company.com" },
      "schedule": { "name": "Primary SRE", "id": "PSCHED1" },
      "escalation_policy": { "name": "Production Escalation" },
      "escalation_level": 1,
      "start": "2026-02-15T17:00:00Z",
      "end": "2026-02-16T17:00:00Z"
    }
  ],
  "summary": "2 on-call assignment(s). Primary SRE: Jane Doe. Secondary SRE: Bob Smith."
}
```

---

#### `services` — List Services

Lists all PagerDuty services with their current operational status.

```
pager-triage services
```

**Example output:**
```json
{
  "tool": "pd_services",
  "services": [
    {
      "id": "PSVC123",
      "name": "Production Web",
      "status": "critical",
      "description": "Production web application servers",
      "escalation_policy": "Production Escalation",
      "integrations": ["Prometheus Alertmanager", "CloudWatch"]
    }
  ],
  "summary": "12 services: 1 critical, 1 warning, 10 active, 0 disabled"
}
```

---

#### `recent` — Recent Incident History

Shows recent incidents for a service or across all services with summary statistics.

```
pager-triage recent                          # All services, last 24h
pager-triage recent --service PSVC123        # Specific service
pager-triage recent --since 7d               # Last 7 days
pager-triage recent --service PSVC123 --since 30d
```

**Flags:**
| Flag | Default | Description |
|------|---------|-------------|
| `--service <id>` | all | Filter to a specific PagerDuty service ID |
| `--since <window>` | `24h` | Time window: `24h`, `7d`, or `30d` |

**Example output:**
```json
{
  "tool": "pd_recent",
  "period": "last 24 hours",
  "service": "PSVC123",
  "incidents": [ ... ],
  "stats": {
    "total": 5,
    "by_urgency": { "high": 2, "low": 3 },
    "by_status": { "resolved": 4, "triggered": 1 },
    "mean_time_to_resolve_minutes": 42
  }
}
```

---

### Write Operations (⚠️ require `--confirm`)

These operations modify state in PagerDuty. They **require** the `--confirm` flag AND `PAGERDUTY_EMAIL` to be set. Without `--confirm`, the tool displays what it *would* do and exits.

---

#### `ack <incident_id> --confirm` — Acknowledge Incident

Acknowledges a triggered incident, stopping further escalation.

```
pager-triage ack P123ABC --confirm
```

Without `--confirm`, displays:
```json
{
  "error": "confirmation_required",
  "message": "⚠️ ACKNOWLEDGE INCIDENT — --confirm flag is required to proceed.",
  "incident": { "id": "P123ABC", "title": "High CPU on prod-web-03", "urgency": "high" },
  "hint": "Re-run with --confirm to acknowledge this incident."
}
```

With `--confirm`:
```json
{
  "tool": "pd_incident_ack",
  "incident_id": "P123ABC",
  "status": "acknowledged",
  "acknowledged_at": "2026-02-16T03:46:00Z",
  "acknowledged_by": "jane@company.com"
}
```

---

#### `resolve <incident_id> --confirm` — Resolve Incident

Resolves an incident, marking it as fixed.

```
pager-triage resolve P123ABC --confirm
```

Same confirmation pattern as `ack`. Without `--confirm`, shows incident details and exits. With `--confirm`, resolves and returns confirmation JSON.

---

#### `note <incident_id> --content "text" --confirm` — Add Incident Note

Adds a permanent note to an incident's timeline.

```
pager-triage note P123ABC --content "Root cause: memory leak in auth-service v2.14.3. Rolling back." --confirm
```

**Flags:**
| Flag | Required | Description |
|------|----------|-------------|
| `--content <text>` | Yes | The note text to add |
| `--confirm` | Yes | Confirmation gate |

**Example output:**
```json
{
  "tool": "pd_incident_note",
  "incident_id": "P123ABC",
  "note_id": "PNOTE456",
  "content": "Root cause: memory leak in auth-service v2.14.3. Rolling back.",
  "created_at": "2026-02-16T04:00:00Z",
  "user": "Jane Doe"
}
```

---

## Incident Triage Workflow

When the user needs help triaging an incident, follow this workflow:

### Step 1: Assess the Situation
```
→ pager-triage incidents
```
List all active incidents. Prioritize by urgency (high first) and duration (oldest first).

### Step 2: Deep-Dive the Critical One
```
→ pager-triage detail <incident_id>
```
Get full timeline, alerts, and notes. Identify the trigger source and escalation history.

### Step 3: Correlate with Other Skills
If available, use companion skills to investigate root cause:
- **prom-query** → Query Prometheus for the underlying metrics (CPU, memory, latency, error rate)
- **kube-medic** → Check pod health, restarts, OOMKills, node status in Kubernetes
- **log-dive** → Search application logs for errors around the incident timeframe

### Step 4: Act
```
→ pager-triage ack <incident_id> --confirm        # Stop escalation while investigating
→ pager-triage note <incident_id> --content "..." --confirm   # Document findings
→ pager-triage resolve <incident_id> --confirm     # Mark as fixed
```

### Agent Guidance
- When the user says "what's wrong?" → start with `incidents`
- When they mention a specific incident → use `detail`
- When triaging → show incidents first, then detail on the most urgent
- When correlating → suggest prom-query / kube-medic if installed
- **ALWAYS** show the confirmation preview before executing write operations
- **NEVER** ack/resolve without the user explicitly asking to do so

### Discord v2 Delivery Mode (OpenClaw v2026.2.14+)

When the conversation is happening in a Discord channel:

- Send a compact first response (active incident count, highest urgency incident, recommended next step), then ask if the user wants full detail.
- Keep the first response under ~1200 characters and avoid full timeline dumps in the first message.
- If Discord components are available, include quick actions:
  - `Deep Dive Incident`
  - `Acknowledge Incident`
  - `Add Incident Note`
- If components are not available, provide the same follow-ups as a numbered list.
- Prefer short follow-up chunks (<=15 lines per message) for incident timelines and alert lists.

## Security Notes

- **API keys** are read from environment variables only — never logged, displayed, or included in output
- **Read-only by default** — 5 read commands work with any API key; 3 write commands require `--confirm`
- **Confirmation gates** — Write operations show full incident context and refuse to proceed without `--confirm`
- We recommend starting with a **read-only PagerDuty API key** for triage workflows
- See [SECURITY.md](./SECURITY.md) for the full threat model and RBAC recommendations

## OpsGenie Support (Planned)

OpsGenie integration is planned for a future release. When `OPSGENIE_API_KEY` is set, the same subcommands will map to OpsGenie's REST API with normalized output schemas.

---

<sub>Powered by [Anvil AI](https://labs.anvil-ai.io) · Built for the engineer who gets paged at 3am</sub>
