---
name: siem-logging
description: Configure security information and event management (SIEM) systems for threat detection, log aggregation, and compliance. Use when implementing centralized security logging, writing detection rules, or meeting audit requirements across cloud and on-premise infrastructure.
---

# SIEM Logging

## Purpose

Configure comprehensive security logging infrastructure using SIEM platforms (Elastic SIEM, Microsoft Sentinel, Wazuh, Splunk) to detect threats, investigate incidents, and maintain compliance audit trails. This skill covers platform selection, log aggregation architecture, detection rule development (SIGMA format and platform-specific), alert tuning, and retention policies for regulatory compliance (GDPR, HIPAA, PCI DSS, SOC 2).

## When to Use This Skill

Use this skill when:

- Implementing centralized security event monitoring across infrastructure
- Writing threat detection rules for authentication failures, privilege escalation, data exfiltration
- Designing log aggregation for multi-cloud environments (AWS, Azure, GCP, Kubernetes)
- Meeting compliance requirements for log retention and audit trails
- Tuning security alerts to reduce false positives and alert fatigue
- Calculating costs for high-volume security logging (TB/day scale)
- Integrating security logging with incident response workflows

## SIEM Platform Selection

### Quick Decision Framework

Choose SIEM platform based on:

**Budget Considerations:**
- **Unlimited budget** → Splunk Enterprise Security (enterprise features, proven scale)
- **Moderate budget** ($50k-$500k/year) → Microsoft Sentinel or Elastic SIEM (cloud-native, flexible)
- **Tight budget** (<$50k/year) → Wazuh (free, open-source XDR/SIEM)

**Infrastructure Context:**
- **Heavy Azure investment** → Microsoft Sentinel (native integration, built-in SOAR)
- **Heavy AWS investment** → AWS Security Lake + OpenSearch (AWS-native)
- **Multi-cloud or on-premise** → Elastic SIEM or Wazuh (platform-agnostic)

**Data Volume:**
- **>1 TB/day** → Splunk or Elastic Cloud (proven at scale)
- **100 GB - 1 TB/day** → Microsoft Sentinel or Elastic SIEM
- **<100 GB/day** → Wazuh or Sentinel 50 GB tier

**Team Expertise:**
- **Elasticsearch experience** → Elastic SIEM (familiar tooling)
- **Microsoft/Azure expertise** → Microsoft Sentinel (Azure ecosystem)
- **Generalists or limited resources** → Wazuh (easiest learning curve)

### Platform Comparison Summary

| Platform | Cost | Deployment | Best For |
|----------|------|------------|----------|
| **Elastic SIEM** | $$$ | Cloud/Self-Hosted | Multi-cloud, customization needs, DevOps teams |
| **Microsoft Sentinel** | $$$ | Cloud (Azure) | Azure-heavy orgs, built-in SOAR, cloud-first |
| **Wazuh** | Free | Self-Hosted | Cost-conscious, SMBs, compliance requirements |
| **Splunk ES** | $$$$$ | Cloud/On-Prem | Large enterprises, massive scale, unlimited budget |

For detailed feature comparison, see `references/platform-comparison.md`.

## Detection Rules

### Universal Format: SIGMA Rules

SIGMA provides a universal detection rule format that compiles to any SIEM query language (Elastic EQL, Splunk SPL, Microsoft KQL).

**SIGMA Rule Structure:**

```yaml
title: Multiple Failed Login Attempts from Single Source
id: 8a9e3c7f-4b2d-4e8a-9f1c-2d5e6f7a8b9c
status: stable
description: Detects potential brute force attacks (10+ failed logins in 10 minutes)
author: Security Team
date: 2025/12/03
references:
  - https://attack.mitre.org/techniques/T1110/
tags:
  - attack.credential_access
  - attack.t1110
logsource:
  category: authentication
  product: linux
detection:
  selection:
    event.type: authentication
    event.outcome: failure
  timeframe: 10m
  condition: selection | count() by source.ip > 10
level: high
```

**Compile SIGMA to Platform-Specific:**

```bash
# Install SIGMA compiler
pip install sigma-cli

# Compile to Elastic EQL
sigmac -t es-eql sigma_rule.yml

# Compile to Splunk SPL
sigmac -t splunk sigma_rule.yml

# Compile to Microsoft KQL
sigmac -t kusto sigma_rule.yml
```

### Platform-Specific Detection Formats

**Elastic EQL (Event Query Language):**

```eql
sequence by user.name with maxspan=5m
  [process where process.name == "powershell.exe" and
   process.args : ("Invoke-WebRequest", "iwr", "wget")]
  [process where process.parent.name == "powershell.exe"]
```

**Microsoft Sentinel KQL:**

```kql
SigninLogs
| where TimeGenerated > ago(1h)
| where ResultType != 0  // Failed login
| summarize FailedAttempts=count() by UserPrincipalName, IPAddress
| where FailedAttempts >= 10
```

**Splunk SPL:**

```spl
index=web_logs sourcetype=access_combined
| rex field=uri "(?<sql_keywords>union|select|insert|update|delete)"
| where isnotnull(sql_keywords)
| stats count by src_ip, uri
| where count > 5
```

For comprehensive detection rule examples, see:
- `examples/sigma-rules/` - Universal SIGMA detection rules
- `examples/elastic-eql/` - Elastic-specific queries
- `examples/microsoft-kql/` - Microsoft Sentinel queries
- `examples/splunk-spl/` - Splunk searches
- `references/detection-rules-guide.md` - Complete guide

## Log Aggregation Architecture

### Centralized Architecture

Single SIEM instance for all logs. Use when:
- Single region deployment
- Small to medium volumes (<1 TB/day)
- Single cloud provider or on-premise
- Limited security team (1-10 analysts)

**Architecture:**

```
Application Servers → Log Shippers (Filebeat/Fluentd)
                   ↓
              Log Aggregator (Logstash/Fluentd)
                   ↓
          SIEM Platform (Elasticsearch/Splunk/Sentinel)
                   ↓
            Security Analysts (Dashboard/Alerts)
```

### Distributed Architecture (Multi-Region)

Regional SIEM instances with global aggregation. Use when:
- Multi-region global deployments
- Data residency requirements (GDPR, sovereignty)
- High volumes (>1 TB/day per region)
- Low-latency requirements for regional analysis

**Architecture:**

```
Global SIEM (Correlation, Threat Intelligence)
    ↓
Regional SIEM (US-East) | Regional SIEM (EU-West) | Regional SIEM (APAC)
    ↓                        ↓                          ↓
Local Logs               Local Logs                 Local Logs
```

### Cloud-Native Architecture

Leverage managed cloud services. Use when:
- Cloud-first organization (AWS/Azure/GCP)
- Want to avoid managing infrastructure
- Elastic workloads with variable log volumes
- Budget for cloud service costs

**AWS Example:**

```
CloudTrail + VPC Flow Logs + GuardDuty
              ↓
       AWS Security Lake (S3 Data Lake)
              ↓
    OpenSearch (Analysis) | Athena (SQL Queries)
```

For deployment examples, see:
- `examples/architectures/elk-stack-docker-compose.yml`
- `examples/architectures/fluentd-kubernetes-daemonset.yaml`
- `examples/architectures/aws-security-lake-terraform/`
- `examples/architectures/wazuh-docker-compose.yml`
- `references/cloud-native-logging.md`

## Log Aggregation Tools

**Fluentd (Cloud-Native):** CNCF project for Kubernetes and multi-cloud environments. Use for containerized applications.

**Logstash (Elastic Stack):** Native Elasticsearch integration. Use for advanced parsing (grok patterns) and data enrichment.

For complete configuration examples, see `examples/logstash-pipelines/` and `references/cloud-native-logging.md`.

## Log Retention and Compliance

### Compliance Requirements

| Framework | Minimum Retention | Hot Storage | Warm Storage | Cold Storage |
|-----------|------------------|-------------|--------------|--------------|
| **GDPR** | 30-90 days | 7 days | 30 days | 60 days |
| **HIPAA** | 6 years | 30 days | 180 days | 6 years |
| **PCI DSS** | 1 year | 90 days | 180 days | 1 year |
| **SOC 2** | 1 year | 30 days | 90 days | 1 year |

### Storage Tiering Strategy

**Hot Tier (SSD, Real-Time):**
- Last 7-30 days
- Real-time indexing and fast queries
- Most expensive ($0.10/GB/month)

**Warm Tier (HDD, Recent):**
- 30-90 days
- Read-only indices, occasional searches
- Moderate cost ($0.05/GB/month)

**Cold Tier (S3/Blob, Archive):**
- 90 days to retention limit
- Searchable snapshots, rare queries
- Cheapest ($0.01/GB/month)

**Example Cost Optimization:**

```
500 GB/day log volume, 1-year retention

Hot (30 days):   15 TB @ $0.10/GB = $1,500/month
Warm (60 days):  30 TB @ $0.05/GB = $1,500/month
Cold (275 days): 137.5 TB @ $0.01/GB = $1,375/month

Total: $4,375/month = $52,500/year

vs. Hot-only: $18,250/month = $219,000/year
Savings: 76% ($166,500/year)
```

For detailed retention policies and cost optimization, see:
- `references/log-retention-policies.md`
- `references/cost-optimization.md`
- `scripts/cost-calculator.py`

## What to Log (Security Events)

**Critical Events (MUST LOG):**
- Authentication: Login attempts, MFA, password changes, privilege escalation
- Authorization: Permission changes, role modifications, access denials
- Data Access: Sensitive database/file access, API calls, exports
- Network: Connections, firewall denials, VPN, DNS queries
- System: Service changes, configuration modifications, software installations

**Severity Levels:** Failed auth (3+): HIGH alert | Privilege escalation: CRITICAL alert | Data export: HIGH alert | Config change: MEDIUM (no alert)

## Alert Tuning and Noise Reduction

### Alert Lifecycle

1. **Detection Rule Created** - Conservative thresholds, deploy to production
2. **Baseline Period (2-4 weeks)** - Collect alert data, tag true/false positives
3. **Tuning Phase** - Add whitelisting, adjust thresholds, refine correlation
4. **Continuous Improvement** - Weekly metrics review, monthly effectiveness review

### Noise Reduction Techniques

**Whitelisting (Known-Safe Patterns):**

```yaml
# Example: Allow scanner IPs
- rule_id: brute_force_detection
  whitelist:
    - source_ip: "10.0.0.100"  # Security scanner
    - user_agent: "Nagios"      # Monitoring system
```

**Threshold Tuning:**

```yaml
# Before: Too sensitive (500 alerts/day, 5% true positive rate)
- rule: failed_login_attempts
  threshold: 3 attempts in 5 minutes

# After: Tuned (50 alerts/day, 40% true positive rate)
- rule: failed_login_attempts
  threshold: 10 attempts in 10 minutes
```

**Multi-Event Correlation:**

```yaml
# Instead of: Single event alert
- alert_on: "Failed authentication"

# Use: Correlated pattern
- alert_on:
    - "Failed authentication (5+ times)"
    - AND "From new IP address"
    - AND "Successful authentication follows"
    - WITHIN: 30 minutes
```

### Target Alert Metrics

| Metric | Target |
|--------|--------|
| Total Alerts/Day | <100 |
| True Positive Rate | >30% |
| Mean Time to Investigate | <15 min |
| False Positive Rate | <50% |
| Critical Alerts/Day | <10 |

For comprehensive alert tuning strategies, see `references/alert-tuning-strategies.md`.

## Quick Start

**Deploy Wazuh:** `git clone https://github.com/wazuh/wazuh-docker.git && cd wazuh-docker/single-node && docker-compose up -d` (see `examples/architectures/wazuh-docker-compose.yml`)

**Create SIGMA Rule:** See `examples/sigma-rules/brute-force-detection.yml` for SSH brute force detection template

**Elastic Cloud:** Sign up at cloud.elastic.co, create Security tier deployment, install Elastic Agent on endpoints

## Integration with Related Skills

**observability skill:**
- Route security logs to SIEM, performance logs to observability platform
- Shared log aggregation infrastructure (Fluentd/Logstash)
- Different analysis purposes (security vs. performance)

**incident-management skill:**
- SIEM alerts trigger incident response workflows
- Integration with PagerDuty, Opsgenie, ServiceNow
- Automated incident creation for critical security events

**security-hardening skill:**
- SIEM monitors security configurations and compliance
- Detect configuration drift from CIS benchmarks
- Alert on security policy violations

**building-ci-pipelines skill:**
- Log CI/CD security events (deployments, secrets access)
- GitHub Actions/GitLab CI integration with SIEM
- Supply chain security monitoring

**secret-management skill:**
- Audit all secrets access operations
- HashiCorp Vault/AWS Secrets Manager logs to SIEM
- Detect unauthorized secrets access attempts

## Reference Documentation

### Detailed Guides

- `references/platform-comparison.md` - Comprehensive SIEM platform feature comparison
- `references/detection-rules-guide.md` - Detection rule formats (SIGMA, EQL, KQL, SPL)
- `references/log-retention-policies.md` - Compliance requirements and retention strategies
- `references/cloud-native-logging.md` - AWS, Azure, GCP, Kubernetes logging setup
- `references/alert-tuning-strategies.md` - False positive reduction and alert optimization
- `references/cost-optimization.md` - Storage tiering and cost management

### Working Examples

- `examples/sigma-rules/` - Universal SIGMA detection rules (10+ examples)
- `examples/elastic-eql/` - Elastic Event Query Language queries
- `examples/microsoft-kql/` - Microsoft Sentinel Kusto queries
- `examples/splunk-spl/` - Splunk Search Processing Language
- `examples/architectures/` - Complete deployment examples (Docker, Kubernetes, Terraform)
- `examples/logstash-pipelines/` - Logstash pipeline configurations

### Utility Scripts

- `scripts/sigma-to-elastic.sh` - Convert SIGMA rules to Elastic EQL
- `scripts/cost-calculator.py` - Estimate SIEM costs based on volume and retention

## Official Documentation

- **Elastic SIEM:** https://www.elastic.co/security
- **Microsoft Sentinel:** https://azure.microsoft.com/en-us/products/microsoft-sentinel
- **Wazuh:** https://wazuh.com/
- **Splunk Enterprise Security:** https://www.splunk.com/en_us/products/enterprise-security.html
- **SIGMA Rules Repository:** https://github.com/SigmaHQ/sigma
- **MITRE ATT&CK Framework:** https://attack.mitre.org/
