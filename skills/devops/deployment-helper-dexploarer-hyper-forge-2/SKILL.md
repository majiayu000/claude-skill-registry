---
name: deployment-helper
description: Deploy elizaOS agents to production with best practices, monitoring, and scaling. Triggers on "deploy agent", "production setup", or "deploy elizaOS"
allowed-tools: [Write, Read, Bash]
---

# Deployment Helper Skill

Production deployment configurations for elizaOS agents with Docker, monitoring, and scaling.

## Deployment Patterns

### 1. Single Agent Deployment

```typescript
// src/index.ts
import { AgentRuntime } from '@elizaos/core';
import { PGAdapter } from '@elizaos/adapter-postgresql';
import character from './character';

const runtime = new AgentRuntime({
  databaseAdapter: new PGAdapter(process.env.DATABASE_URL),
  character,
  env: process.env
});

await runtime.initialize();

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    agent: character.name,
    uptime: process.uptime()
  });
});

// Graceful shutdown
process.on('SIGTERM', async () => {
  await runtime.stop();
  process.exit(0);
});
```

### 2. Docker Deployment

```dockerfile
# Dockerfile
FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  agent:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/eliza
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:15
    volumes:
      - pgdata:/var/lib/postgresql/data
    environment:
      - POSTGRES_DB=eliza
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass

  redis:
    image: redis:7-alpine
    volumes:
      - redisdata:/data

volumes:
  pgdata:
  redisdata:
```

### 3. Multi-Agent Deployment

```typescript
// agents/coordinator.ts
const agents = [
  { character: agent1, id: 'agent-1' },
  { character: agent2, id: 'agent-2' },
  { character: agent3, id: 'agent-3' }
];

const runtimes = await Promise.all(
  agents.map(async ({ character, id }) => {
    const runtime = new AgentRuntime({
      databaseAdapter: new PGAdapter(DATABASE_URL),
      character,
      env: process.env
    });
    await runtime.initialize();
    return { id, runtime };
  })
);

// Load balancing
function selectAgent(message: string): AgentRuntime {
  const hash = hashCode(message);
  const index = hash % runtimes.length;
  return runtimes[index].runtime;
}
```

## Monitoring

```typescript
// Metrics collection
import { collectDefaultMetrics, register, Counter, Histogram } from 'prom-client';

collectDefaultMetrics();

const messageCounter = new Counter({
  name: 'agent_messages_total',
  help: 'Total messages processed',
  labelNames: ['agent', 'status']
});

const responseTime = new Histogram({
  name: 'agent_response_duration_seconds',
  help: 'Response time',
  buckets: [0.1, 0.5, 1, 2, 5]
});

// Metrics endpoint
app.get('/metrics', async (req, res) => {
  res.set('Content-Type', register.contentType);
  res.end(await register.metrics());
});
```

## Production Checklist

- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] Health check endpoint working
- [ ] Monitoring configured
- [ ] Logging setup
- [ ] Error tracking (Sentry)
- [ ] Rate limiting enabled
- [ ] HTTPS configured
- [ ] Secrets secured
- [ ] Backup strategy
- [ ] Scaling plan
- [ ] Rollback procedure
