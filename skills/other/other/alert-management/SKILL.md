---
name: alert-management
description: Implement comprehensive alert management with PagerDuty, escalation policies, and incident coordination. Use when setting up alerting systems, managing on-call schedules, or coordinating incident response.
---

# Alert Management

## Overview

Design and implement sophisticated alert management systems with PagerDuty integration, escalation policies, alert routing, and incident coordination.

## When to Use

- Setting up alert routing
- Managing on-call schedules
- Coordinating incident response
- Creating escalation policies
- Integrating alerting systems

## Instructions

### 1. **PagerDuty Client Integration**

```javascript
// pagerduty-client.js
const axios = require('axios');

class PagerDutyClient {
  constructor(apiToken) {
    this.apiToken = apiToken;
    this.baseUrl = 'https://api.pagerduty.com';
    this.eventUrl = 'https://events.pagerduty.com/v2/enqueue';

    this.client = axios.create({
      baseURL: this.baseUrl,
      headers: {
        'Authorization': `Token token=${apiToken}`,
        'Accept': 'application/vnd.pagerduty+json;version=2'
      }
    });
  }

  async triggerEvent(config) {
    const event = {
      routing_key: config.routingKey,
      event_action: config.eventAction || 'trigger',
      dedup_key: config.dedupKey || `event-${Date.now()}`,
      payload: {
        summary: config.summary,
        timestamp: new Date().toISOString(),
        severity: config.severity || 'error',
        source: config.source || 'Monitoring System',
        component: config.component,
        custom_details: config.customDetails || {}
      }
    };

    try {
      const response = await axios.post(this.eventUrl, event);
      return response.data;
    } catch (error) {
      console.error('Failed to trigger PagerDuty event:', error);
      throw error;
    }
  }

  async resolveEvent(dedupKey) {
    const event = {
      routing_key: process.env.PAGERDUTY_ROUTING_KEY,
      event_action: 'resolve',
      dedup_key: dedupKey
    };

    try {
      return await axios.post(this.eventUrl, event);
    } catch (error) {
      console.error('Failed to resolve event:', error);
      throw error;
    }
  }

  async getServices() {
    const response = await this.client.get('/services');
    return response.data.services;
  }

  async getEscalationPolicies() {
    const response = await this.client.get('/escalation_policies');
    return response.data.escalation_policies;
  }

  async createIncident(config) {
    const incident = {
      type: 'incident',
      title: config.title,
      service: {
        id: config.serviceId,
        type: 'service_reference'
      },
      escalation_policy: {
        id: config.escalationPolicyId,
        type: 'escalation_policy_reference'
      },
      body: {
        type: 'incident_body',
        details: config.details || ''
      }
    };

    try {
      const response = await this.client.post('/incidents', incident, {
        headers: { 'From': process.env.PAGERDUTY_EMAIL }
      });
      return response.data.incident;
    } catch (error) {
      console.error('Failed to create incident:', error);
      throw error;
    }
  }

  async acknowledgeIncident(incidentId, userId) {
    try {
      const response = await this.client.put(
        `/incidents/${incidentId}`,
        {
          incidents: [{
            id: incidentId,
            type: 'incident_reference',
            status: 'acknowledged'
          }]
        },
        { headers: { 'From': process.env.PAGERDUTY_EMAIL } }
      );
      return response.data.incidents[0];
    } catch (error) {
      console.error('Failed to acknowledge:', error);
      throw error;
    }
  }

  async resolveIncident(incidentId) {
    try {
      const response = await this.client.put(
        `/incidents/${incidentId}`,
        {
          incidents: [{
            id: incidentId,
            type: 'incident_reference',
            status: 'resolved'
          }]
        },
        { headers: { 'From': process.env.PAGERDUTY_EMAIL } }
      );
      return response.data.incidents[0];
    } catch (error) {
      console.error('Failed to resolve:', error);
      throw error;
    }
  }
}

module.exports = PagerDutyClient;
```

### 2. **Alertmanager Configuration**

```yaml
# /etc/alertmanager/alertmanager.yml
global:
  resolve_timeout: 5m
  slack_api_url: '${SLACK_WEBHOOK_URL}'

templates:
  - '/etc/alertmanager/templates/*.tmpl'

route:
  receiver: 'default'
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 4h

  routes:
    - match:
        severity: critical
      receiver: pagerduty
      continue: true
      group_wait: 0s

    - match:
        severity: warning
      receiver: slack

    - match:
        service: payment-service
      receiver: payment-team
      group_wait: 30s

receivers:
  - name: 'default'
    slack_configs:
      - channel: '#alerts'
        title: 'Alert: {{ .GroupLabels.alertname }}'

  - name: 'pagerduty'
    pagerduty_configs:
      - service_key: '${PAGERDUTY_SERVICE_KEY}'
        description: '{{ .GroupLabels.alertname }}'

  - name: 'slack'
    slack_configs:
      - channel: '#alerts'
        title: 'Warning: {{ .GroupLabels.alertname }}'

  - name: 'payment-team'
    pagerduty_configs:
      - service_key: '${PAYMENT_PAGERDUTY_KEY}'
    slack_configs:
      - channel: '#payment-alerts'

inhibit_rules:
  - source_match:
      severity: 'critical'
    target_match:
      severity: 'warning'
    equal: ['alertname', 'service']
```

### 3. **Alert Handler Middleware**

```javascript
// alert-handler.js
const PagerDutyClient = require('./pagerduty-client');

const pdClient = new PagerDutyClient(process.env.PAGERDUTY_API_TOKEN);

class AlertHandler {
  constructor() {
    this.alertCache = new Map();
    this.deduplicationWindow = 300000; // 5 minutes
  }

  shouldSendAlert(dedupKey) {
    const cacheEntry = this.alertCache.get(dedupKey);

    if (!cacheEntry) return true;

    const timeSinceLastAlert = Date.now() - cacheEntry.timestamp;
    return timeSinceLastAlert >= this.deduplicationWindow;
  }

  recordAlert(dedupKey) {
    this.alertCache.set(dedupKey, { timestamp: Date.now() });
  }

  determineSeverity(value, thresholds) {
    if (value >= thresholds.critical) return 'critical';
    if (value >= thresholds.warning) return 'warning';
    return 'info';
  }

  async sendAlert(config) {
    const dedupKey = config.dedupKey || `alert-${config.alertName}-${Date.now()}`;

    try {
      if (!this.shouldSendAlert(dedupKey)) {
        console.log('Alert recently sent, skipping');
        return;
      }

      const event = {
        routingKey: config.routingKey,
        eventAction: config.eventAction || 'trigger',
        dedupKey: dedupKey,
        summary: config.summary,
        severity: config.severity,
        source: config.source || 'Monitoring System',
        component: config.component,
        customDetails: {
          ...config.customDetails,
          alertName: config.alertName,
          timestamp: new Date().toISOString()
        }
      };

      const result = await pdClient.triggerEvent(event);
      this.recordAlert(dedupKey);

      console.log('Alert sent', {
        alertName: config.alertName,
        severity: config.severity
      });

      return result;
    } catch (error) {
      console.error('Failed to send alert:', error);
      await this.sendSlackAlert(config);
    }
  }

  async sendSlackAlert(config) {
    const axios = require('axios');
    const webhookUrl = process.env.SLACK_WEBHOOK_URL;

    const message = {
      color: config.severity === 'critical' ? 'danger' : 'warning',
      title: config.summary,
      text: config.customDetails?.description || '',
      fields: [
        { title: 'Severity', value: config.severity, short: true },
        { title: 'Component', value: config.component, short: true }
      ]
    };

    try {
      await axios.post(webhookUrl, { attachments: [message] });
    } catch (error) {
      console.error('Failed to send Slack alert:', error);
    }
  }

  async resolveAlert(dedupKey) {
    try {
      await pdClient.resolveEvent(dedupKey);
      console.log('Alert resolved');
    } catch (error) {
      console.error('Failed to resolve alert:', error);
    }
  }
}

module.exports = new AlertHandler();
```

### 4. **Alert Routing Engine**

```javascript
// alert-router.js
class AlertRouter {
  constructor() {
    this.routes = [];
  }

  addRoute(rule) {
    this.routes.push({
      priority: rule.priority || 0,
      condition: rule.condition,
      handler: rule.handler,
      escalation: rule.escalation
    });
    this.routes.sort((a, b) => b.priority - a.priority);
  }

  async route(alert) {
    for (const route of this.routes) {
      if (route.condition(alert)) {
        return await route.handler(alert, route.escalation);
      }
    }
    return this.defaultHandler(alert);
  }

  async defaultHandler(alert) {
    console.log('Routing to default handler:', alert.name);
    return { routed: true, handler: 'default' };
  }
}

// Usage
const router = new AlertRouter();

router.addRoute({
  priority: 100,
  condition: (alert) => alert.severity === 'critical' && alert.component === 'database',
  handler: async (alert) => {
    console.log('Routing critical database alert to DBA team');
    return { team: 'dba', escalation: 'immediate' };
  }
});

router.addRoute({
  priority: 90,
  condition: (alert) => alert.component === 'payment-service',
  handler: async (alert) => {
    console.log('Routing to payment team');
    return { team: 'payment', escalation: 'payment-policy' };
  }
});

router.addRoute({
  priority: 10,
  condition: (alert) => alert.severity === 'warning',
  handler: async (alert) => {
    console.log('Routing warning to Slack');
    return { handler: 'slack-only' };
  }
});

module.exports = router;
```

### 5. **Docker Compose Alert Stack**

```yaml
# docker-compose.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  alertmanager:
    image: prom/alertmanager:latest
    ports:
      - "9093:9093"
    volumes:
      - ./alertmanager.yml:/etc/alertmanager/alertmanager.yml
    environment:
      SLACK_WEBHOOK_URL: ${SLACK_WEBHOOK_URL}
      PAGERDUTY_SERVICE_KEY: ${PAGERDUTY_SERVICE_KEY}
    depends_on:
      - prometheus

  alert-handler:
    build: .
    environment:
      PAGERDUTY_API_TOKEN: ${PAGERDUTY_API_TOKEN}
      SLACK_WEBHOOK_URL: ${SLACK_WEBHOOK_URL}
    ports:
      - "3000:3000"
    depends_on:
      - alertmanager
```

## Best Practices

### ✅ DO
- Set appropriate thresholds
- Implement alert deduplication
- Use clear alert names
- Include runbook links
- Configure escalation properly
- Test alert rules
- Monitor alert quality
- Set repeat intervals
- Track alert metrics
- Document alert meanings

### ❌ DON'T
- Alert on every anomaly
- Ignore alert fatigue
- Set thresholds arbitrarily
- Skip runbooks
- Alert without action
- Disable alerts in production
- Use vague alert names
- Forget escalation policies
- Re-alert too frequently

## Alert Severity Levels

- **Critical**: Immediate action required, customer impact
- **Warning**: Investigation needed, potential issues
- **Info**: Informational, no action required

## Key Metrics

- Alert volume
- Resolution time
- False positive rate
- Escalation frequency
- MTTD (Mean Time to Detection)
- MTTR (Mean Time to Resolution)
