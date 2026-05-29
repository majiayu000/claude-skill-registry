---
name: dashboard
description: View all tracked vulnerabilities and their current status
user-invocable: true
allowed-tools: Read, Glob, Grep
model: haiku
---

# Vulnetix Vulnerability Dashboard

This skill reads `.vulnetix/memory.yaml` and displays a comprehensive vulnerability status report. It is read-only and does not modify any files.

## Workflow

### Step 1: Load Memory

1. Use **Glob** to check if `.vulnetix/memory.yaml` exists in the repo root
2. If it does not exist, display: **"No vulnerability data found. Run `/vulnetix:vuln <package>` or `/vulnetix:exploits-search` to start tracking."** and stop.
3. Use **Read** to load the full contents of `.vulnetix/memory.yaml`

### Step 2: Parse and Categorize

From the `vulnerabilities:` section, categorize each entry:

**Open (unresolved):**
- `status: affected` -- "Vulnerable"
- `status: under_investigation` -- "Investigating"

**Resolved:**
- `status: fixed` -- "Fixed"
- `status: not_affected` -- "Not affected"
- Entries with `decision.choice: risk-accepted` -- "Risk accepted"
- Entries with `decision.choice: deferred` -- "Deferred"

From the `manifests:` section, collect manifest tracking info.

### Step 3: Display Summary Header

```
Vulnetix Security Dashboard
============================
Open: <N> (<X> vulnerable, <Y> investigating)
Resolved: <N> (<X> fixed, <Y> not affected, <Z> risk-accepted, <W> deferred)
Manifests tracked: <N> (last scan: <timestamp>)
```

If there are zero vulnerabilities and zero manifests, display: **"Clean slate -- no vulnerabilities tracked yet."**

### Step 4: Open Vulnerabilities Table

If there are open vulnerabilities, display them sorted by CWSS priority (P1 first), then by severity:

```
Open Vulnerabilities
--------------------
| ID | Package | Severity | Status | Priority | Decision |
|----|---------|----------|--------|----------|----------|
| CVE-2021-44228 | log4j-core | critical | Vulnerable | P1 (87.5) | investigating |
| GHSA-xxxx-yyyy | express | high | Investigating | P2 (62.0) | investigating |
```

For each column:
- **ID**: Primary vulnerability key
- **Package**: `package` field
- **Severity**: `severity` field
- **Status**: Developer-friendly status (see VEX mapping above)
- **Priority**: `cwss.priority` and `cwss.score` if available, otherwise "--"
- **Decision**: `decision.choice` if available, otherwise "--"

### Step 5: Resolved Vulnerabilities Table

If there are resolved vulnerabilities, display them:

```
Resolved Vulnerabilities
------------------------
| ID | Package | Severity | Resolution | Decision | Date |
|----|---------|----------|------------|----------|------|
| CVE-2023-1234 | lodash | high | Fixed | fix-applied | 2024-01-15 |
```

For the **Date** column, use the most recent `history` entry timestamp, or `discovery.date` as fallback.

### Step 6: Manifest Tracking

If manifests are tracked, display:

```
Tracked Manifests
-----------------
| Manifest | Ecosystem | Last Scanned | Vulns Found |
|----------|-----------|--------------|-------------|
| package.json | npm | 2024-01-15T10:30:00Z | 3 |
| go.mod | go | 2024-01-15T10:31:00Z | 0 |
```

### Step 7: Suggested Actions

For each open vulnerability (up to 5), suggest a next action based on its state:

- Has no `threat_model` or `cwss`: `"/vulnetix:exploits <id>"` -- get exploit analysis and priority scoring
- Has `cwss` but no fix applied: `"/vulnetix:fix <id>"` -- get fix intelligence
- General: `"/vulnetix:remediation <id>"` -- get a full remediation plan

If there are more than 5 open vulns, add: `"Use /vulnetix:exploits-search to find exploited vulnerabilities across your ecosystem."`

Always end with: `"Use /vulnetix:vuln <id> for detailed info on any vulnerability."`
