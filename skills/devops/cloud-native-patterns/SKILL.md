---
name: cloud-native-patterns
description: Apply cloud-native architecture patterns. Use when designing for scalability, resilience, or cloud deployment. Covers microservices, containers, and distributed systems.
allowed-tools: Read, Write, Glob, Grep
---

# Cloud-Native Patterns

## Twelve-Factor App

1. **Codebase**: One codebase, many deploys
2. **Dependencies**: Explicitly declare and isolate
3. **Config**: Store in environment
4. **Backing Services**: Treat as attached resources
5. **Build, Release, Run**: Strictly separate stages
6. **Processes**: Execute as stateless processes
7. **Port Binding**: Export services via port
8. **Concurrency**: Scale out via process model
9. **Disposability**: Fast startup and graceful shutdown
10. **Dev/Prod Parity**: Keep environments similar
11. **Logs**: Treat as event streams
12. **Admin Processes**: Run as one-off processes

## Resilience Patterns

### Circuit Breaker
Prevent cascading failures by failing fast.

```typescript
class CircuitBreaker {
  private failures = 0;
  private lastFailure?: Date;

  async call<T>(fn: () => Promise<T>): Promise<T> {
    if (this.isOpen()) {
      throw new Error('Circuit is open');
    }
    try {
      const result = await fn();
      this.reset();
      return result;
    } catch (error) {
      this.recordFailure();
      throw error;
    }
  }
}
```

### Retry with Backoff
```typescript
async function withRetry<T>(
  fn: () => Promise<T>,
  maxRetries = 3
): Promise<T> {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await fn();
    } catch (error) {
      if (i === maxRetries - 1) throw error;
      await sleep(Math.pow(2, i) * 1000); // Exponential backoff
    }
  }
}
```

### Bulkhead
Isolate failures to prevent system-wide impact.

## Service Communication

### Synchronous
- REST/HTTP
- gRPC

### Asynchronous
- Message queues (RabbitMQ, SQS)
- Event streaming (Kafka)

## Health Checks

```typescript
app.get('/health', (req, res) => {
  res.json({ status: 'healthy' });
});

app.get('/ready', async (req, res) => {
  const dbHealthy = await checkDatabase();
  const cacheHealthy = await checkCache();

  if (dbHealthy && cacheHealthy) {
    res.json({ status: 'ready' });
  } else {
    res.status(503).json({ status: 'not ready' });
  }
});
```

## Container Best Practices

- One process per container
- Use multi-stage builds
- Run as non-root user
- Use health checks
- Keep images small
