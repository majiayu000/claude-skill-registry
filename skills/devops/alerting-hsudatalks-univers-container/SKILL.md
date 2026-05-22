---
name: alerting
description: Real-time alerting and notification system for Univers infrastructure. Use this when you need to monitor system health, service status, and send proactive alerts when thresholds are exceeded or services fail.
---

# Alerting Skill

This skill provides comprehensive monitoring and alerting capabilities for the Univers infrastructure ecosystem.

## Capabilities

### 1. Real-time Monitoring
- System resource monitoring (CPU, Memory, Disk, Network)
- Service health checks (HTTP endpoints, ports, processes)
- Application-specific metrics (response times, error rates)
- Custom metric collection and aggregation

### 2. Alert Engine
- Threshold-based alerting
- Rate limiting and alert suppression
- Alert escalation policies
- Multi-condition alert rules

### 3. Notification Channels
- Email notifications with rich formatting
- Slack/Teams integration with actionable messages
- Webhook support for custom integrations
- In-app notifications and banners

### 4. Alert Management
- Alert acknowledgment and resolution
- Alert history and analytics
- Scheduled maintenance windows
- Alert rule testing and validation

### 5. Dashboards and Reports
- Real-time alert status dashboard
- Historical alert trends and analytics
- Service health overview
- Performance metrics visualization

## Common Tasks

### Basic Alert Setup
```bash
# Check system for alert conditions
alert check system

# Monitor specific services
alert monitor services

# Test notification channels
alert test channels
```

### Alert Rule Management
```bash
# List all alert rules
alert rules list

# Add new alert rule
alert rules add cpu-high --threshold 80 --duration 5m

# Update existing rule
alert rules update memory-usage --threshold 90

# Remove alert rule
alert rules remove disk-space-low
```

### Notification Configuration
```bash
# Configure email notifications
alert config email --smtp smtp.example.com --from alerts@example.com

# Configure Slack integration
alert config slack --webhook https://hooks.slack.com/... --channel #alerts

# Test notification delivery
alert test email --to admin@example.com
alert test slack --message "Test alert"
```

### Alert Operations
```bash
# View active alerts
alert status

# Acknowledge an alert
alert acknowledge CPU_HIGH_001

# Resolve an alert
alert resolve MEMORY_HIGH_003

# View alert history
alert history --last 24h
```

## Alert Rule Examples

### System Resource Alerts
```yaml
# High CPU Usage
name: cpu-high
condition: cpu_usage > 80
duration: 5m
severity: warning
message: "CPU usage is {{cpu_usage}}% on {{hostname}}"
actions:
  - type: email
    to: ops@example.com
  - type: slack
    channel: #alerts

# Critical Memory Usage
name: memory-critical
condition: memory_usage > 90
duration: 2m
severity: critical
message: "Critical memory usage: {{memory_usage}}%"
actions:
  - type: webhook
    url: https://api.pagerduty.com/incidents
```

### Service Health Alerts
```yaml
# Service Down
name: service-down
condition: service_health == 0
duration: 1m
severity: critical
message: "{{service_name}} is down on {{hostname}}"
actions:
  - type: email
    to: devops@example.com
  - type: restart
    service: "{{service_name}}"

# High Response Time
name: slow-response
condition: response_time > 2000
duration: 3m
severity: warning
message: "{{service_name}} response time: {{response_time}}ms"
actions:
  - type: slack
    channel: #performance
```

### Application-Specific Alerts
```yaml
# High Error Rate
name: high-error-rate
condition: error_rate > 5
duration: 5m
severity: warning
message: "{{application}} error rate: {{error_rate}}%"
actions:
  - type: email
    to: dev-team@example.com

# Database Connection Issues
name: db-connection-failed
condition: db_connection_status != "healthy"
duration: 30s
severity: critical
message: "Database connection failed for {{application}}"
actions:
  - type: webhook
    url: https://hooks.slack.com/...
```

## Integration Examples

### Univers Services Integration
```bash
# Monitor Univers services
alert monitor univers-services

# Check specific Univers endpoints
alert check endpoint http://localhost:3003/health --service univers-server
alert check endpoint http://localhost:6007 --service univers-ui
alert check endpoint http://localhost:5173 --service univers-web

# Monitor tmux sessions
alert monitor tmux-sessions --alert-if-missing univers-developer
```

### Container Integration
```bash
# Monitor Docker containers
alert monitor containers --include univers-*

# Check container health
alert check container univers-server
alert check container univers-ui
```

## Configuration Files

### Alert Rules Configuration
```yaml
# ~/.config/univers/alerting/rules.yaml
rules:
  - name: system-cpu-high
    type: system
    metric: cpu_usage
    operator: ">"
    threshold: 80
    duration: 5m
    severity: warning

  - name: service-unavailable
    type: service
    check: http_status
    target: "http://localhost:3003/health"
    operator: "!="
    threshold: 200
    duration: 1m
    severity: critical
```

### Notification Channels
```yaml
# ~/.config/univers/alerting/channels.yaml
channels:
  email:
    smtp_host: smtp.gmail.com
    smtp_port: 587
    username: alerts@company.com
    password: ${SMTP_PASSWORD}

  slack:
    webhook_url: ${SLACK_WEBHOOK_URL}
    default_channel: #univers-alerts

  webhook:
    endpoint: https://api.example.com/alerts
    headers:
      Authorization: "Bearer ${API_TOKEN}"
```

## Best Practices

1. **Set Meaningful Thresholds**: Avoid alert fatigue by setting realistic thresholds
2. **Use Escalation Policies**: Implement graduated alert escalation
3. **Provide Context**: Include relevant details in alert messages
4. **Test Regularly**: Verify alert rules and notification channels
5. **Document Procedures**: Maintain clear runbooks for common alerts

## Troubleshooting

### Common Issues
- **Missing Notifications**: Check channel configurations and connectivity
- **False Positives**: Review alert thresholds and conditions
- **Alert Storms**: Implement rate limiting and suppression rules
- **Slow Performance**: Optimize alert check intervals and data collection

### Debug Commands
```bash
# Check alert engine status
alert status --verbose

# Test specific rule
alert test-rule cpu-high

# Check notification delivery
alert test-notification email --to test@example.com

# View alert engine logs
alert logs --tail 100
```

## Version History

- v1.0 (2025-12-16): Initial alerting system implementation
- Basic monitoring, email notifications, and alert rules