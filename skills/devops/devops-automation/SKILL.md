---
name: devops-automation
description: "DevOps and IT Ops automation - CI/CD, monitoring, incident management, and infrastructure workflows"
version: "1.0.0"
author: claude-office-skills
license: MIT

category: devops
tags:
  - devops
  - ci-cd
  - monitoring
  - incident
  - automation
department: Engineering

models:
  recommended:
    - claude-sonnet-4

mcp:
  server: devops-mcp
  tools:
    - github_api
    - jenkins_trigger
    - aws_cli
    - kubernetes_api

capabilities:
  - ci_cd_pipelines
  - monitoring_alerts
  - incident_management
  - infrastructure_automation
  - deployment_workflows

languages:
  - en
  - zh

related_skills:
  - slack-workflows
  - telegram-bot
  - ai-agent-builder
---

# DevOps Automation

Automate DevOps workflows including CI/CD pipelines, monitoring, incident management, and infrastructure operations. Based on n8n's IT Ops workflow templates.

## Overview

This skill covers:
- CI/CD pipeline automation
- Monitoring and alerting
- Incident management
- Infrastructure automation
- Deployment workflows

---

## CI/CD Automation

### GitHub Actions Integration

```yaml
workflow: "GitHub CI/CD Notifications"

triggers:
  - github_push
  - github_pull_request
  - github_workflow_run
  
on_push:
  action:
    - trigger_ci: if_main_branch
    - notify_slack:
        channel: "#deployments"
        message: |
          📦 *New Push to {branch}*
          
          Commit: `{commit_sha_short}`
          Author: {author}
          Message: {commit_message}
          
          [View Diff]({compare_url})

on_pr_opened:
  action:
    - notify_slack:
        channel: "#code-review"
        message: |
          🔀 *New Pull Request*
          
          Title: {pr_title}
          Author: {author}
          Branch: {head} → {base}
          
          [Review PR]({pr_url})
    - assign_reviewers: based_on_codeowners
    - run_ci_checks

on_workflow_complete:
  action:
    - notify_slack:
        message: |
          {status_emoji} *Build {status}*
          
          Workflow: {workflow_name}
          Branch: {branch}
          Duration: {duration}
          
          {if_failed: [View Logs]({logs_url})}
```

### Deployment Pipeline

```yaml
deployment_pipeline:
  stages:
    build:
      trigger: push_to_main
      steps:
        - checkout_code
        - install_dependencies
        - run_tests
        - build_artifact
        - push_to_registry
        
    staging:
      trigger: build_success
      steps:
        - deploy_to_staging
        - run_integration_tests
        - notify_qa
        
    production:
      trigger: manual_approval
      steps:
        - create_backup
        - deploy_to_production
        - run_smoke_tests
        - notify_team
        
  rollback:
    trigger: deployment_failed OR manual
    steps:
      - revert_to_previous
      - notify_team
      - create_incident
```

---

## Monitoring & Alerting

### Alert Routing

```yaml
alert_routing:
  sources:
    - prometheus
    - datadog
    - cloudwatch
    - new_relic
    
  severity_levels:
    critical:
      response_time: 5_minutes
      channels: [pagerduty, slack_urgent, sms]
      escalation: immediate
      
    high:
      response_time: 15_minutes
      channels: [slack_alerts, email]
      escalation: after_15_minutes
      
    medium:
      response_time: 1_hour
      channels: [slack_alerts]
      
    low:
      response_time: 24_hours
      channels: [slack_logging]
      
  routing_rules:
    - if: service == "payments"
      team: payments_oncall
      severity_boost: +1
      
    - if: service == "auth"
      team: security_oncall
      
    - default:
      team: platform_oncall
```

### Alert Templates

```yaml
alert_templates:
  infrastructure:
    cpu_high:
      title: "🔥 High CPU Usage"
      body: |
        Server: {host}
        CPU: {cpu_percent}%
        Duration: {duration}
        
        Threshold: {threshold}%
        
        [View Dashboard]({grafana_url})
        
    memory_critical:
      title: "💾 Critical Memory"
      body: |
        Server: {host}
        Memory: {memory_percent}%
        Available: {available_mb}MB
        
        [SSH to Server]({ssh_link})
        
    disk_full:
      title: "💿 Disk Space Critical"
      body: |
        Server: {host}
        Disk: {disk_percent}%
        Available: {available_gb}GB
        
        Suggestion: Clean logs or expand volume
        
  application:
    error_spike:
      title: "📈 Error Rate Spike"
      body: |
        Service: {service}
        Error Rate: {error_rate}%
        Normal: {baseline}%
        
        Top Errors:
        {top_errors}
        
    latency_high:
      title: "🐢 High Latency"
      body: |
        Service: {service}
        P99 Latency: {p99_ms}ms
        Threshold: {threshold_ms}ms
```

---

## Incident Management

### Incident Workflow

```yaml
incident_workflow:
  detection:
    sources: [monitoring, user_report, automated_check]
    
  triage:
    auto_severity:
      - if: affects_payments
        severity: critical
      - if: affects_auth
        severity: critical
      - if: affects_api AND error_rate > 10%
        severity: high
        
  response:
    critical:
      - create_incident_channel: "#inc-{timestamp}"
      - page_oncall: immediately
      - notify_stakeholders: [engineering_lead, product]
      - start_war_room: zoom_link
      - create_status_page: incident
      
    high:
      - create_incident_channel
      - notify_oncall: slack
      - create_ticket: jira
      
  communication:
    internal:
      frequency: every_30_minutes
      channel: incident_channel
      template: |
        📊 *Incident Update*
        
        Status: {status}
        Impact: {impact}
        Next update: {next_update_time}
        
        Current actions:
        {action_items}
        
    external:
      channel: status_page
      template: customer_facing_update
      
  resolution:
    steps:
      - confirm_resolution
      - update_status_page: resolved
      - notify_stakeholders
      - schedule_postmortem
      - close_incident_channel: after_24h
```

### Postmortem Template

```yaml
postmortem_template:
  sections:
    summary:
      - incident_title
      - duration
      - severity
      - impact
      
    timeline:
      format: |
        | Time | Event |
        |------|-------|
        | {time} | {event} |
        
    root_cause:
      - what_happened
      - why_it_happened
      - contributing_factors
      
    impact:
      - users_affected
      - revenue_impact
      - sla_breach
      
    resolution:
      - how_it_was_fixed
      - time_to_detect
      - time_to_resolve
      
    action_items:
      format: |
        | Action | Owner | Due Date | Status |
        |--------|-------|----------|--------|
        
    lessons_learned:
      - what_went_well
      - what_went_poorly
      - lucky_breaks
```

---

## Infrastructure Automation

### Server Provisioning

```yaml
provisioning_workflow:
  trigger: jira_ticket OR slack_request
  
  steps:
    1. validate_request:
        check: [budget_approval, security_review]
        
    2. create_infrastructure:
        terraform:
          - vpc
          - security_groups
          - ec2_instances
          - load_balancer
          
    3. configure_server:
        ansible:
          - base_configuration
          - security_hardening
          - monitoring_agent
          - application_setup
          
    4. validate:
        - health_check
        - security_scan
        - performance_baseline
        
    5. notify:
        slack: "✅ Server {hostname} is ready"
        include: [ssh_access, dashboard_link]
```

### Scheduled Maintenance

```yaml
maintenance_automation:
  tasks:
    certificate_renewal:
      schedule: "30 days before expiry"
      action:
        - request_new_cert: letsencrypt
        - deploy_cert
        - verify_ssl
        - notify: if_failure
        
    security_patching:
      schedule: "weekly"
      action:
        - check_updates
        - if_critical: immediate_patch
        - else: schedule_maintenance_window
        
    log_rotation:
      schedule: "daily"
      action:
        - rotate_logs
        - compress_old
        - upload_to_s3
        - delete_local: older_than_7_days
        
    backup_verification:
      schedule: "weekly"
      action:
        - restore_to_test_env
        - run_integrity_checks
        - report_status
```

---

## Kubernetes Automation

### K8s Workflows

```yaml
kubernetes_automation:
  deployment:
    trigger: docker_image_pushed
    steps:
      - update_manifest: with_new_image_tag
      - apply_to_staging
      - run_tests
      - if_success: apply_to_production
      
  scaling:
    trigger: metric_threshold
    rules:
      - if: cpu > 80%
        action: scale_up
        max_replicas: 10
      - if: cpu < 20%
        action: scale_down
        min_replicas: 2
        
  rollback:
    trigger: health_check_failed
    action:
      - kubectl_rollout_undo
      - notify_team
      - create_incident
```

---

## Output Example

**Request**: "Set up deployment notifications for GitHub Actions"

**Output**:

```markdown
# GitHub Actions Deployment Notifications

## n8n Workflow

```yaml
trigger: GitHub Webhook
events: [workflow_run]
```

## Notification Templates

**Build Started:**
```
🚀 *Deployment Started*

Branch: main
Commit: abc1234
Author: @developer
Triggered by: Push

[View Workflow](https://github.com/...)
```

**Build Success:**
```
✅ *Deployment Successful*

Environment: Production
Duration: 3m 42s
Version: v1.2.3

Changes:
• Feature X
• Bug fix Y

[View Deployment](https://app.example.com)
```

**Build Failed:**
```
❌ *Deployment Failed*

Stage: Test
Error: npm test failed

[View Logs](https://github.com/...)
[Retry](https://github.com/...)
```

## Slack Integration

```yaml
channel: "#deployments"
mention_on_failure: "@oncall"
thread_replies: true
```
```

---

*DevOps Automation Skill - Part of Claude Office Skills*
