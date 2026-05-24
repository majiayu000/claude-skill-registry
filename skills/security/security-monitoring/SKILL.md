---
name: Security Monitoring
description: Automate security monitoring, threat detection, incident response, and compliance workflows
version: 1.0.0
author: Claude Office Skills
category: security
tags:
  - security
  - monitoring
  - siem
  - incident-response
  - compliance
department: security
models:
  - claude-3-opus
  - claude-3-sonnet
  - gpt-4
mcp:
  server: security-mcp
  tools:
    - siem_query
    - alert_create
    - incident_manage
    - compliance_check
capabilities:
  - Threat detection and alerting
  - Incident response automation
  - Log analysis and correlation
  - Compliance monitoring
input:
  - Security logs
  - Alert rules
  - Incident data
  - Compliance requirements
output:
  - Security alerts
  - Incident reports
  - Compliance dashboards
  - Threat intelligence
languages:
  - en
related_skills:
  - devops-automation
  - log-analysis
  - compliance-audit
---

# Security Monitoring

Comprehensive skill for security monitoring, threat detection, and incident response automation.

## Core Architecture

### Security Monitoring Stack

```
SECURITY MONITORING ARCHITECTURE:
┌─────────────────────────────────────────────────────────┐
│                     DATA SOURCES                         │
├──────────┬──────────┬──────────┬──────────┬────────────┤
│ Firewall │ Endpoint │ Cloud    │ Network  │ Application│
│ Logs     │ Logs     │ Logs     │ Traffic  │ Logs       │
└────┬─────┴────┬─────┴────┬─────┴────┬─────┴─────┬──────┘
     │          │          │          │           │
     └──────────┴──────────┴────┬─────┴───────────┘
                                ▼
┌─────────────────────────────────────────────────────────┐
│                   LOG AGGREGATION                        │
│              (SIEM / Security Data Lake)                 │
└────────────────────────┬────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   DETECTION ENGINE                       │
│  • Rule-based Detection    • ML Anomaly Detection       │
│  • Correlation Rules       • Threat Intelligence        │
└────────────────────────┬────────────────────────────────┘
                         ▼
┌─────────────────────────────────────────────────────────┐
│                   RESPONSE & ACTION                      │
│  • Alerting        • Automated Response                 │
│  • Ticketing       • Containment                        │
└─────────────────────────────────────────────────────────┘
```

## Detection Rules

### Rule Categories

```yaml
detection_rules:
  authentication:
    - name: brute_force_login
      description: "Multiple failed login attempts"
      query: |
        event.type == "authentication" AND
        event.outcome == "failure" AND
        COUNT(*) > 5 WITHIN 5 minutes
        GROUP BY source.ip
      severity: high
      actions:
        - create_alert
        - block_ip_temporarily
        
    - name: impossible_travel
      description: "Login from geographically distant locations"
      query: |
        event.type == "authentication" AND
        event.outcome == "success" AND
        geo_distance(prev_location, current_location) > 500km AND
        time_diff < 1 hour
      severity: critical
      actions:
        - create_alert
        - require_mfa_verification
        - notify_user
        
  data_exfiltration:
    - name: large_data_transfer
      description: "Unusual data egress volume"
      query: |
        event.type == "network" AND
        direction == "outbound" AND
        bytes_transferred > 100MB WITHIN 1 hour
        GROUP BY user.id
      severity: medium
      actions:
        - create_alert
        - capture_network_session
        
  malware:
    - name: known_malware_hash
      description: "File matches known malware signature"
      query: |
        event.type == "file" AND
        file.hash.sha256 IN threat_intelligence.malware_hashes
      severity: critical
      actions:
        - quarantine_file
        - isolate_endpoint
        - create_incident
```

### Correlation Rules

```yaml
correlation_rules:
  - name: lateral_movement_detection
    description: "Detect potential lateral movement"
    events:
      - type: authentication_success
        from: internal_network
      - type: process_execution
        name: ["psexec", "wmic", "powershell"]
        within: 5_minutes
      - type: network_connection
        to: different_internal_host
        within: 10_minutes
    severity: high
    
  - name: privilege_escalation_chain
    description: "Detect privilege escalation attempts"
    events:
      - type: authentication
        account_type: standard_user
      - type: process_execution
        elevated: true
        within: 30_minutes
      - type: account_modification
        action: add_to_admin_group
        within: 1_hour
    severity: critical
```

## Alert Management

### Alert Configuration

```yaml
alert_config:
  severity_levels:
    critical:
      response_time: 15_minutes
      notifications:
        - pagerduty: security_oncall
        - slack: "#security-critical"
        - email: security-team@company.com
      auto_escalation: 30_minutes
      
    high:
      response_time: 1_hour
      notifications:
        - slack: "#security-alerts"
        - email: security-team@company.com
        
    medium:
      response_time: 4_hours
      notifications:
        - slack: "#security-alerts"
        
    low:
      response_time: 24_hours
      notifications:
        - ticket_only: true
        
  deduplication:
    enabled: true
    window: 1_hour
    key_fields:
      - rule_id
      - source.ip
      - destination.ip
```

### Alert Template

```yaml
alert_template:
  title: "[{{severity}}] {{rule_name}}"
  
  body: |
    ## Security Alert
    
    **Rule:** {{rule_name}}
    **Severity:** {{severity}}
    **Time:** {{timestamp}}
    
    ### Details
    - **Source IP:** {{source.ip}}
    - **Source User:** {{user.name}}
    - **Destination:** {{destination.ip}}
    - **Action:** {{event.action}}
    
    ### Context
    {{event_context}}
    
    ### Recommended Actions
    {{#each recommended_actions}}
    - {{this}}
    {{/each}}
    
    ### Related Events
    {{related_events_link}}
```

## Incident Response

### Incident Workflow

```
INCIDENT RESPONSE WORKFLOW:
┌─────────────────┐
│    Detection    │
│  (Alert Fired)  │
└────────┬────────┘
         ▼
┌─────────────────┐
│     Triage      │
│  - Validate     │
│  - Classify     │
│  - Prioritize   │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Containment   │
│  - Isolate      │
│  - Block        │
│  - Preserve     │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Investigation  │
│  - Collect      │
│  - Analyze      │
│  - Correlate    │
└────────┬────────┘
         ▼
┌─────────────────┐
│   Eradication   │
│  - Remove       │
│  - Patch        │
│  - Harden       │
└────────┬────────┘
         ▼
┌─────────────────┐
│    Recovery     │
│  - Restore      │
│  - Verify       │
│  - Monitor      │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Post-Incident  │
│  - Document     │
│  - Review       │
│  - Improve      │
└─────────────────┘
```

### Playbook Automation

```yaml
playbooks:
  - name: ransomware_response
    trigger:
      alert_type: ransomware_detected
    steps:
      - name: isolate_endpoint
        action: network_isolate
        target: "{{affected_host}}"
        
      - name: disable_account
        action: disable_ad_account
        target: "{{user.name}}"
        
      - name: preserve_evidence
        action: capture_memory_image
        target: "{{affected_host}}"
        
      - name: notify_stakeholders
        action: send_notification
        channels:
          - security_team
          - it_leadership
          - legal_if_needed
          
      - name: create_incident
        action: create_ticket
        priority: critical
        template: ransomware_incident
        
  - name: phishing_response
    trigger:
      alert_type: phishing_reported
    steps:
      - name: analyze_email
        action: extract_iocs
        extract:
          - sender_address
          - urls
          - attachments
          
      - name: check_recipients
        action: query_email_logs
        find: all_recipients
        
      - name: block_sender
        action: add_to_blocklist
        target: "{{sender_address}}"
        
      - name: remove_emails
        action: delete_from_mailboxes
        target: all_recipients
```

## Compliance Monitoring

### Compliance Frameworks

```yaml
compliance_checks:
  pci_dss:
    - requirement: "10.2.1"
      description: "Log all access to cardholder data"
      query: |
        SELECT * FROM audit_logs
        WHERE data_classification = 'cardholder'
        AND timestamp > NOW() - INTERVAL '24 hours'
      expected: all_access_logged
      
    - requirement: "10.6.1"
      description: "Review logs daily"
      check: daily_log_review_completed
      
  hipaa:
    - requirement: "164.312(b)"
      description: "Audit controls"
      checks:
        - audit_logging_enabled
        - log_retention_6_years
        - tamper_protection
        
  soc2:
    - control: "CC6.1"
      description: "Logical access security"
      checks:
        - mfa_enabled
        - password_policy_enforced
        - access_reviews_quarterly
```

### Compliance Dashboard

```
COMPLIANCE STATUS DASHBOARD
═══════════════════════════════════════

PCI-DSS:      ████████████░░░░ 92% ✓
HIPAA:        ██████████████░░ 98% ✓
SOC 2:        █████████████░░░ 95% ✓
GDPR:         ████████████████ 100% ✓

FINDINGS BY SEVERITY:
Critical  ░░░░░░░░░░░░░░░░ 0
High      ██░░░░░░░░░░░░░░ 3
Medium    ████░░░░░░░░░░░░ 8
Low       ██████░░░░░░░░░░ 15

UPCOMING DEADLINES:
• Jan 30: Quarterly access review
• Feb 15: Penetration test scheduled
• Feb 28: Annual audit prep
```

## Security Metrics

### KPI Dashboard

```
SECURITY OPERATIONS METRICS
═══════════════════════════════════════

DETECTION:
MTTD (Mean Time to Detect): 4.2 hours
Alert Volume: 1,234/day
True Positive Rate: 78%

RESPONSE:
MTTR (Mean Time to Respond): 1.8 hours
Incidents Resolved: 23/week
SLA Compliance: 96%

COVERAGE:
Assets Monitored: 2,456/2,500 (98%)
Log Sources: 45 active
Detection Rules: 234 active

THREAT LANDSCAPE:
Blocked Attacks: 12,456/month
Vulnerabilities: 89 open
Patch Compliance: 94%
```

### Reporting

```yaml
reports:
  - name: daily_security_briefing
    schedule: "0 8 * * *"
    recipients: security_team
    sections:
      - overnight_alerts
      - active_incidents
      - threat_intelligence_updates
      
  - name: weekly_executive_summary
    schedule: "0 9 * * 1"
    recipients: leadership
    sections:
      - key_metrics
      - significant_incidents
      - risk_posture
      - recommendations
      
  - name: monthly_compliance_report
    schedule: "0 9 1 * *"
    recipients: compliance_team
    sections:
      - control_status
      - audit_findings
      - remediation_progress
```

## Best Practices

1. **Defense in Depth**: Multiple detection layers
2. **Least Privilege**: Minimize access rights
3. **Log Everything**: Comprehensive audit trails
4. **Automate Response**: Reduce MTTR
5. **Regular Testing**: Validate controls
6. **Threat Intelligence**: Stay informed
7. **Incident Drills**: Practice response
8. **Continuous Improvement**: Learn from incidents
