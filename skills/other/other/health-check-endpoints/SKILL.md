---
name: health-check-endpoints
description: Health check endpoints for liveness, readiness, dependency monitoring. Use for Kubernetes, load balancers, auto-scaling, or encountering probe failures, startup delays, dependency checks, timeout configuration errors.
---

# Health Check Endpoints

Implement health checks for monitoring service availability and readiness.

## Probe Types

| Probe | Purpose | Failure Action |
|-------|---------|----------------|
| Liveness | Is process alive? | Restart container |
| Readiness | Can handle traffic? | Remove from LB |
| Startup | Has app started? | Delay other probes |
| Deep | All deps healthy? | Trigger alerts |

## Implementation (Express)

```javascript
class HealthChecker {
  async checkDatabase() {
    const start = Date.now();
    try {
      await db.query('SELECT 1');
      return { status: 'healthy', latency: Date.now() - start };
    } catch (err) {
      return { status: 'unhealthy', error: String(err?.message || err) };
    }
  }

  async checkRedis() {
    try {
      await redis.ping();
      return { status: 'healthy' };
    } catch (err) {
      return { status: 'unhealthy', error: err.message };
    }
  }

  async getReadiness() {
    const checks = await Promise.all([
      this.checkDatabase(),
      this.checkRedis()
    ]);
    const healthy = checks.every(c => c.status === 'healthy');
    return { healthy, checks };
  }
}

// Liveness - lightweight
app.get('/health/live', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// Readiness - check dependencies
app.get('/health/ready', async (req, res) => {
  const health = await healthChecker.getReadiness();
  res.status(health.healthy ? 200 : 503).json(health);
});
```

## Kubernetes Configuration

```yaml
livenessProbe:
  httpGet:
    path: /health/live
    port: 3000
  initialDelaySeconds: 15
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /health/ready
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 10
```

## Best Practices

- Keep liveness checks minimal (no external deps)
- Check only critical systems in readiness
- Return 200 for healthy, 503 for unhealthy
- Set reasonable timeouts to prevent cascading failures
- Include response time metrics

## Additional Implementations

See [references/implementations.md](references/implementations.md) for:
- Python Flask complete health checker
- Java Spring Boot Actuator
- Full Kubernetes deployment config

## Never Do

- Make liveness depend on external services
- Return 200 when dependencies are down
- Skip dependency checks in readiness
