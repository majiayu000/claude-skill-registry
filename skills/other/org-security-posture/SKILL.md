---
name: org-security-posture
description: Assess the overall organization security posture
user-invocable: true
---

You are helping the team assess Jocko Fuel's overall security posture.

Follow these steps:

### Step 1: Gather Current State

Delegate to the `security-orchestrator` agent to collect data across all security domains:
- **Identity and Access**: User counts, role assignments, MFA adoption via `identity-access-reviewer`
- **Endpoint Security**: TLS grades, header compliance, certificate expiry via `endpoint-security-auditor`
- **Vulnerability Status**: Known CVEs, unpatched systems via `vulnerability-scanner`
- **SaaS Security**: Integration security, SSO coverage via `saas-security-auditor`
- **Attack Surface**: External exposure inventory via `attack-surface-monitor`

### Step 2: Score Security Domains

Rate each domain on a 1-10 scale:
- **Access Control** (IAM, MFA, least privilege)
- **Data Protection** (encryption, masking, backup)
- **Network Security** (TLS, firewalls, CDN)
- **Application Security** (API security, input validation)
- **Monitoring and Response** (logging, alerting, incident readiness)
- **Compliance** (regulatory adherence, policy documentation)

### Step 3: Identify Gaps

Highlight the widest gaps between current state and target state:
- Which domains are strongest?
- Which domains need the most improvement?
- What are the quick wins vs. long-term projects?

### Step 4: Deliver Assessment

Present a posture report with:
- **Overall security score** (composite of domain scores)
- **Domain scorecard** (table with scores and key findings)
- **Risk register** (top risks ranked by likelihood and impact)
- **Improvement roadmap** (prioritized by impact and effort)

### Error Handling

- If some domains cannot be assessed, note gaps and recommend follow-up
- If the organization lacks baseline security policies, recommend establishing them first
- If data is stale, note the last assessment date and recommend a fresh scan
