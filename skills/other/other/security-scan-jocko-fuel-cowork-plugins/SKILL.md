---
name: security-scan
description: Run a comprehensive security scan across all systems
user-invocable: true
---

You are helping the team run a comprehensive security scan across Jocko Fuel systems.

Follow these steps:

### Step 1: Define Scan Scope

Ask the user what to scan. Options:
- **Full scan**: All systems (APIs, infrastructure, SaaS, Snowflake, endpoints)
- **Domain-specific**: Target a specific area (e.g., "just APIs" or "just Snowflake")
- **Project-specific**: Scan a particular project or service

If the user says "everything," delegate to `security-orchestrator` to coordinate a full scan.

### Step 2: Execute Scans

Delegate to the `security-orchestrator` agent to route scans to specialized agents:
- **API endpoints** → `api-security-audit` agent
- **Identity and access** → `identity-access-reviewer` agent
- **Endpoints and TLS** → `endpoint-security-auditor` agent
- **Dependencies and code** → `vulnerability-scanner` agent
- **SaaS platforms** → `saas-security-auditor` agent
- **Snowflake** → `snowflake-security-auditor` agent
- **External attack surface** → `attack-surface-monitor` agent

### Step 3: Aggregate Findings

Collect results from all agents and categorize by:
- **Critical**: Actively exploitable or data-exposing issues
- **High**: Significant risk requiring prompt remediation
- **Medium**: Notable issues for planned remediation
- **Low**: Minor issues or hardening recommendations
- **Informational**: Best practice suggestions

### Step 4: Present Results

Deliver a scan summary with:
- Total findings by severity
- Top 5 priority items requiring immediate attention
- Per-domain breakdown table
- Recommended remediation timeline

### Error Handling

- If a system is unreachable, note it as "not scanned" and recommend manual review
- If credentials are insufficient for a scan, inform the user of required access
- If scan scope is too broad, suggest breaking into phased scans
