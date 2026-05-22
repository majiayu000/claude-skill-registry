---
name: monitoring-observability
description: Implement comprehensive monitoring, logging, metrics, tracing, and alerting for production applications to ensure reliability and quick incident response. Use when setting up application monitoring, implementing structured logging, creating metrics and dashboards, setting up alerts, implementing distributed tracing, monitoring performance, tracking errors, or building observability into applications.
---

# Monitoring & Observability - System Health

## When to use this skill

- Setting up application monitoring systems
- Implementing structured logging
- Creating metrics and performance dashboards
- Setting up alerts for critical issues
- Implementing distributed tracing
- Monitoring API performance and latency
- Tracking error rates and exceptions
- Building observability into applications
- Setting up log aggregation
- Creating SLO/SLA monitoring
- Implementing health checks
- Building incident detection systems

## When to use this skill

- Setting up metrics, alerts, dashboards.
- When working on related tasks or features
- During development that requires this expertise

**Use when**: Setting up metrics, alerts, dashboards.

## Three Pillars
1. **Metrics** - Time-series data (CPU, memory, requests/sec)
2. **Logs** - Event records with context
3. **Traces** - Request flow through system

## Example
\`\`\`typescript
import * as Sentry from '@sentry/node';
import { metrics } from './metrics';

app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    metrics.histogram('request_duration', Date.now() - start, {
      method: req.method,
      route: req.route?.path,
      status: res.statusCode
    });
  });
  next();
});
\`\`\`

## Resources
- [Observability Guide](https://www.honeycomb.io/what-is-observability)
- [Grafana](https://grafana.com/)
- [Sentry](https://sentry.io/)
