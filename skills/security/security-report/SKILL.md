---
name: security-report
description: Generate a comprehensive security report for stakeholders
user-invocable: true
---

You are helping the team generate a comprehensive security report for Jocko Fuel.

Follow these steps:

### Step 1: Define Report Scope

Ask the user:
- **Audience**: Executive summary, technical team, or compliance/audit
- **Time period**: Last 30 days, quarter, or custom range
- **Focus areas**: All domains or specific areas (e.g., just infrastructure, just IAM)
- **Include recommendations?** Yes (actionable) or no (status only)

### Step 2: Collect Data

Delegate to the `security-orchestrator` agent to gather data from all relevant agents:
- Vulnerability scan results from `vulnerability-scanner`
- IAM review findings from `identity-access-reviewer`
- Endpoint security status from `endpoint-security-auditor`
- SaaS security posture from `saas-security-auditor`
- Snowflake security status from `snowflake-security-auditor`
- Attack surface changes from `attack-surface-monitor`
- Compliance status from `compliance-auditor`
- Any incident history from `incident-responder`

### Step 3: Structure the Report

Format based on audience:

**Executive summary** (for leadership):
- Overall security posture score (1-10)
- Key risk areas in plain language
- Top 3 actions needed
- Trend comparison vs. previous period

**Technical report** (for engineering):
- Detailed findings by domain
- Specific vulnerabilities with remediation steps
- Configuration recommendations
- Metrics and benchmarks

**Compliance report** (for audit):
- Control status by framework
- Evidence inventory
- Gap analysis
- Remediation timeline

### Step 4: Deliver Report

Present the report in the requested format. Offer to:
- Export as markdown for documentation
- Highlight items needing immediate action
- Schedule follow-up assessments
- Create task tickets for remediation items

### Error Handling

- If data from some domains is unavailable, note gaps and provide partial report
- If no previous assessment exists for comparison, establish this as the baseline
- If findings are sensitive, remind the user about proper handling of security reports
