---
name: logging-monitoring
description: |
    Use when designing security logging, monitoring, and incident detection capabilities. Covers SIEM architecture, audit trail requirements, security event correlation, and compliance logging for GDPR, PCI DSS, HIPAA, and SOX.
    USE FOR: SIEM, security logging, audit trails, security monitoring, incident detection, log aggregation, security event correlation, compliance logging, intrusion detection
    DO NOT USE FOR: application performance monitoring (use observability skills), general logging frameworks (use logging skills), incident response procedures (use secure-sdlc)
license: MIT
metadata:
  displayName: "Security Logging & Monitoring"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "OWASP Logging Cheat Sheet"
    url: "https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html"
  - title: "NIST SP 800-92 Guide to Computer Security Log Management"
    url: "https://csrc.nist.gov/publications/detail/sp/800-92/final"
  - title: "OWASP Top Ten A09:2021 Security Logging and Monitoring Failures"
    url: "https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/"
---

# Security Logging & Monitoring

## Overview

OWASP A09:2021 — Security Logging and Monitoring Failures — highlights the critical importance of comprehensive logging and active monitoring in application security. Without adequate logging, breaches go undetected; without effective monitoring, alerts go unnoticed. Security logging is the foundation of incident detection and forensics. On average, organizations take over 200 days to detect a breach, and insufficient logging is a primary contributing factor. Every security-relevant event must be captured, stored securely, and analyzed in near real time to enable rapid detection, investigation, and response.

## What to Log

Every application must log security-relevant events with enough detail to support forensic investigation and compliance audits.

| Event Category | Examples | Priority |
|---|---|---|
| Authentication events | Login, logout, failed login attempts, password changes, MFA enrollment/bypass | Critical |
| Authorization failures | Access denied, privilege escalation attempts, role changes | Critical |
| Data access | PII read/write/delete, bulk data exports, sensitive record access | High |
| Configuration changes | System settings modifications, feature flag changes, security policy updates | High |
| Administrative actions | User creation/deletion, role assignments, permission grants, system restarts | High |
| Input validation failures | Rejected input, SQL injection attempts, XSS payloads, malformed requests | Medium |
| Application errors | Unhandled exceptions, stack traces, crash reports, resource exhaustion | Medium |
| API usage | Rate limit hits, deprecated endpoint calls, unusual request patterns, quota exhaustion | Medium |

**Critical events** must trigger immediate alerts. **High-priority events** should be reviewed within hours. **Medium-priority events** should be included in daily or weekly reviews.

## Audit Trail Requirements

A complete audit trail answers five fundamental questions for every security-relevant action:

- **Who** — The authenticated identity that performed the action (user ID, service account, API key identifier).
- **What** — The specific action taken (created, read, updated, deleted, configured, approved).
- **When** — The precise timestamp in UTC with millisecond precision (ISO 8601 format).
- **Where** — The source IP address, device identifier, geographic location (if available), and the system or endpoint acted upon.
- **Outcome** — Whether the action succeeded or failed, including the reason for failure (e.g., "access denied: insufficient permissions").

### Tamper Protection

Audit logs must be protected against modification or deletion by the systems and people they are designed to monitor.

- **Immutable logs** — Write logs to append-only storage such as write-once, read-many (WORM) storage, or immutable cloud storage buckets (e.g., S3 Object Lock, Azure Immutable Blob Storage).
- **Cryptographic signing** — Sign log entries or batches using HMAC or digital signatures to detect any post-hoc modification. Chain signatures (hash chaining) to detect deletions or reordering.
- **Separate storage** — Store security logs in a dedicated system with independent access controls, isolated from the application and its administrators.
- **Integrity verification** — Regularly verify log integrity by validating cryptographic signatures and checking for gaps in sequence numbers or timestamps.

## SIEM Architecture

Security Information and Event Management (SIEM) systems aggregate, normalize, correlate, and analyze security events from across the organization. A well-architected SIEM pipeline follows this flow:

```
Collection --> Normalization --> Correlation --> Alerting --> Reporting
     |              |               |              |             |
  Log agents    Parse and      Match events    Notify SOC    Dashboards,
  Syslog        enrich with    against rules   via PagerDuty compliance
  API ingestion common schema  and baselines   Slack, email  audit reports
```

1. **Collection** — Gather logs from all sources: applications, infrastructure, cloud services, endpoints, network devices. Use agents, syslog forwarding, or API-based ingestion.
2. **Normalization** — Parse raw logs into a common schema (e.g., Elastic Common Schema, OCSF). Enrich events with contextual data such as geolocation, threat intelligence, and asset inventory.
3. **Correlation** — Apply detection rules, statistical baselines, and behavioral analytics to identify patterns indicative of attacks. Correlate events across multiple sources to detect multi-stage attacks.
4. **Alerting** — Route alerts to the appropriate team based on severity and type. Integrate with incident management tools (PagerDuty, Opsgenie, ServiceNow). Minimize false positives through tuning.
5. **Reporting** — Generate dashboards for real-time visibility and compliance reports for auditors. Track metrics such as mean time to detect (MTTD) and mean time to respond (MTTR).

### SIEM Tools

| Tool | Type | Best For |
|---|---|---|
| Splunk | Commercial | Enterprise-scale deployments with advanced analytics and extensive integrations |
| Elastic SIEM | Open-source core | Cost-effective deployments leveraging the Elastic Stack (ELK) with detection rules |
| Microsoft Sentinel | Cloud-native | Azure-centric environments with native Microsoft 365 and Azure integration |
| Sumo Logic | SaaS | Multi-cloud environments requiring a fully managed, cloud-native solution |
| Wazuh | Open-source | Host-based intrusion detection (HIDS) combined with SIEM, file integrity monitoring |

## Compliance Requirements

Different regulatory frameworks impose specific requirements on security logging and monitoring. Failing to meet these requirements can result in significant fines and legal liability.

| Standard | Logging Requirement |
|---|---|
| PCI DSS | Centralized log collection and retention for a minimum of 1 year (3 months immediately available); daily log review; monitoring of all access to cardholder data environments |
| GDPR | Audit trail of all personal data processing activities; breach detection capabilities with 72-hour notification requirement; data subject access request logging |
| HIPAA | Access logs for all systems containing Protected Health Information (PHI); 6-year minimum log retention; monitoring of access patterns for unauthorized disclosure |
| SOX | Financial system audit trails demonstrating integrity of financial reporting; tamper-proof logs; segregation of duties verification through log analysis |

## Log Security

Security logs are themselves a high-value target. If an attacker can modify or delete logs, they can cover their tracks and extend the dwell time of a breach.

- **Protect logs from tampering** — Use append-only storage, cryptographic signing, and hash chaining to ensure log integrity.
- **Separate log storage** — Store security logs on dedicated infrastructure with independent authentication and access controls. Application administrators should not have write or delete access to security logs.
- **Encrypt log transport** — Use TLS for all log shipping. Encrypt logs at rest using AES-256-GCM or equivalent.
- **Restrict log access** — Apply the principle of least privilege. Only security operations and compliance personnel should have read access to security logs. Log all access to the logs themselves (meta-auditing).
- **Retention policies** — Define retention periods based on compliance requirements and organizational needs. Automate log lifecycle management to ensure logs are retained for the required duration and securely deleted afterward.

## Best Practices

- **Log all security-relevant events** at the application layer, not just at the infrastructure layer; application context (user identity, business action, data sensitivity) is essential for meaningful detection.
- **Use structured logging formats** (JSON, key-value pairs) with a consistent schema across all services to enable reliable parsing, searching, and correlation in your SIEM.
- **Include correlation identifiers** (request ID, trace ID, session ID) in every log entry to enable end-to-end tracing of a single request or user session across distributed services.
- **Never log sensitive data** such as passwords, tokens, credit card numbers, or PII in cleartext; mask or redact sensitive fields before writing to the log.
- **Set up real-time alerting** for critical security events (authentication failures exceeding a threshold, privilege escalation, data exfiltration patterns) with clearly defined escalation paths.
- **Regularly test your detection capabilities** by running tabletop exercises, purple team engagements, and SIEM detection rule testing to ensure alerts fire correctly and are actionable.
- **Monitor the monitoring** — alert on gaps in log ingestion (silent sources), SIEM processing delays, and storage capacity thresholds to ensure your logging pipeline remains healthy.
- **Review and tune detection rules quarterly** to reduce false positives, adapt to evolving threats, and incorporate lessons learned from incidents and near-misses.
