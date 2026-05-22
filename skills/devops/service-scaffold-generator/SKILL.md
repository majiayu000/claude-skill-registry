---
name: Service Scaffold Generator
description: Generator สำหรับสร้าง microservice ใหม่พร้อม structure, config, Docker, CI/CD, และ boilerplate code ครบชุด
---

# Service Scaffold Generator

## Overview

Generator สำหรับ bootstrap microservice ใหม่ให้พร้อมใช้งานทันที - มี folder structure, configuration, Docker, CI/CD, logging, monitoring ครบชุด

## Why This Matters

- **Speed**: สร้าง service ใหม่ใน 1 นาที
- **Consistency**: ทุก service มี structure เดียวกัน
- **Best practices**: Built-in logging, monitoring, testing
- **Production-ready**: Docker, CI/CD, health checks มาครบ

---

## Quick Start

```bash
# Generate new service
npx scaffold-service my-service --type api

# Output:
my-service/
├── src/
├── tests/
├── Dockerfile
├── docker-compose.yml
├── .github/workflows/
├── package.json
└── README.md

✓ Service scaffolded
✓ Dependencies installed
✓ Git initialized
✓ Ready to code!
```

---

## Service Types

### API Service
```bash
npx scaffold-service my-api --type api

# Includes:
- Express/Fastify setup
- REST endpoints
- OpenAPI docs
- Authentication middleware
```

### Worker Service
```bash
npx scaffold-service my-worker --type worker

# Includes:
- Queue processing (Bull/BullMQ)
- Job handlers
- Retry logic
- Dead letter queue
```

### Event Service
```bash
npx scaffold-service my-events --type event

# Includes:
- Event handlers
- Message bus (Kafka/RabbitMQ)
- Event schemas
- Replay capability
```

---

## Generated Structure

```
my-service/
├── src/
│   ├── api/              # API endpoints
│   ├── services/         # Business logic
│   ├── repositories/     # Data access
│   ├── middleware/       # Express middleware
│   ├── utils/            # Utilities
│   ├── config/           # Configuration
│   └── index.ts          # Entry point
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── scripts/
│   ├── migrate.ts
│   └── seed.ts
├── .github/
│   └── workflows/
│       ├── ci.yml
│       └── deploy.yml
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── package.json
├── tsconfig.json
└── README.md
```

---

## Configuration Files

### package.json
```json
{
  "name": "my-service",
  "version": "1.0.0",
  "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "jest",
    "lint": "eslint src",
    "migrate": "tsx scripts/migrate.ts"
  },
  "dependencies": {
    "express": "^4.18.0",
    "zod": "^3.22.0",
    "winston": "^3.11.0"
  }
}
```

### Dockerfile
```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
COPY package*.json ./
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### docker-compose.yml
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=development
      - DATABASE_URL=postgresql://postgres:postgres@db:5432/mydb
    depends_on:
      - db
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_PASSWORD=postgres
    ports:
      - "5432:5432"
```

---

## Built-in Features

### Health Checks
```typescript
// Auto-generated health endpoint
app.get('/health', async (req, res) => {
  const health = {
    uptime: process.uptime(),
    timestamp: Date.now(),
    status: 'ok',
    checks: {
      database: await checkDatabase(),
      redis: await checkRedis()
    }
  };
  
  const statusCode = Object.values(health.checks).every(c => c === 'ok') 
    ? 200 
    : 503;
  
  res.status(statusCode).json(health);
});
```

### Logging
```typescript
// Winston logger configured
import logger from './config/logger';

logger.info('Service started', { port: 3000 });
logger.error('Database error', { error: err.message });
```

### Error Handling
```typescript
// Global error handler
app.use((err, req, res, next) => {
  logger.error('Unhandled error', { 
    error: err.message,
    stack: err.stack,
    path: req.path
  });
  
  res.status(err.statusCode || 500).json({
    error: err.message,
    requestId: req.id
  });
});
```

---

## CI/CD Pipeline

### GitHub Actions
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run lint
      - run: npm test
      - run: npm run build
  
  deploy:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: docker build -t my-service .
      - run: docker push my-service
```

---

## Customization

### Templates
```typescript
// Custom template
export const customTemplate = {
  name: 'my-template',
  files: [
    { path: 'src/custom.ts', content: customContent },
    { path: 'tests/custom.test.ts', content: testContent }
  ],
  dependencies: ['custom-lib'],
  scripts: {
    'custom:run': 'tsx src/custom.ts'
  }
};
```

### Plugins
```typescript
// Add plugin
npx scaffold-service my-service --plugins auth,monitoring,caching

// Adds:
- Authentication middleware
- Prometheus metrics
- Redis caching
```

---

## Summary

**Service Scaffold:** สร้าง microservice ใหม่ครบชุด

**Includes:**
- Folder structure
- Docker + docker-compose
- CI/CD pipeline
- Health checks
- Logging
- Error handling
- Tests

**Usage:**
```bash
npx scaffold-service my-service --type api
cd my-service
npm run dev
```

**Time saved:** 2-4 hours per service
