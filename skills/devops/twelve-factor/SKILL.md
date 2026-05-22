---
name: twelve-factor
description: Guide for 12-Factor cloud-native applications. Use when designing microservices, configuring containers, deploying to Kubernetes, or following cloud-native patterns.
license: MIT
---

# 12-Factor App Methodology

Guide for building scalable, maintainable, and portable cloud-native applications following the 12-Factor App principles and modern extensions.

## When to Activate

Use this skill when:
- Designing or refactoring cloud-native applications
- Building applications for Kubernetes deployment
- Setting up CI/CD pipelines
- Implementing microservices architecture
- Migrating applications to containers
- Reviewing architecture for cloud readiness
- Troubleshooting deployment or scaling issues
- Working with environment configuration

## The 12 Factors

### I. Codebase

**One codebase tracked in revision control, many deploys**

```
myapp-repo/
├── src/
├── config/
├── deploy/
│   ├── staging/
│   ├── production/
│   └── development/
└── Dockerfile
```

**Key principles:**
- Single Git repository for the application
- Multiple environments deploy from same codebase
- Environment-specific config separate from code
- Use GitOps (ArgoCD, Flux) for deployment automation

**Anti-patterns:**
- ❌ Multiple repositories for the same application
- ❌ Different codebases for different environments
- ❌ Copying code between repositories

### II. Dependencies

**Explicitly declare and isolate dependencies**

Declare all dependencies explicitly using package managers:

```dockerfile
# Multi-stage build for dependency isolation
FROM node:18-alpine AS dependencies
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

FROM node:18-alpine AS runtime
WORKDIR /app
COPY --from=dependencies /app/node_modules ./node_modules
COPY . .
CMD ["node", "index.js"]
```

**Language-specific examples:**
- Node.js: `package.json` and `package-lock.json`
- Python: `requirements.txt` or `Pipfile.lock`
- Java: `pom.xml` or `build.gradle`
- Go: `go.mod` and `go.sum`
- Elixir: `mix.exs` and `mix.lock`
- Rust: `Cargo.toml` and `Cargo.lock`

**Key principles:**
- Never rely on system-wide packages
- Use lock files for reproducible builds
- Vendor dependencies when possible
- Multi-stage builds for smaller images

### III. Config

**Store config in the environment**

All configuration should come from environment variables:

```elixir
# Elixir - config/runtime.exs
import Config

config :my_app, MyApp.Repo,
  database: System.get_env("DATABASE_NAME") || "my_app_dev",
  username: System.get_env("DATABASE_USER") || "postgres",
  password: System.fetch_env!("DATABASE_PASSWORD"),
  hostname: System.get_env("DATABASE_HOST") || "localhost",
  pool_size: String.to_integer(System.get_env("POOL_SIZE") || "10")
```

```javascript
// Node.js
const config = {
  database: {
    url: process.env.DATABASE_URL,
    pool: {
      min: parseInt(process.env.DB_POOL_MIN || '2'),
      max: parseInt(process.env.DB_POOL_MAX || '10')
    }
  },
  cache: {
    ttl: parseInt(process.env.CACHE_TTL || '3600')
  }
};
```

**Kubernetes ConfigMaps:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  DATABASE_HOST: "postgres-service"
  CACHE_TTL: "3600"
  LOG_LEVEL: "info"
```

**Kubernetes Secrets:**

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
data:
  DATABASE_PASSWORD: <base64-encoded>
  JWT_SECRET: <base64-encoded>
  API_KEY: <base64-encoded>
```

**Anti-patterns:**
- ❌ Hardcoded configuration values
- ❌ Configuration files committed to version control
- ❌ Different code paths for different environments

### IV. Backing Services

**Treat backing services as attached resources**

Connect to all backing services (databases, queues, caches, APIs) via URLs in environment variables:

```javascript
// Treat all backing services uniformly
const services = {
  database: createConnection(process.env.DATABASE_URL),
  cache: createRedisClient(process.env.REDIS_URL),
  queue: createQueueClient(process.env.RABBITMQ_URL),
  storage: createS3Client(process.env.S3_ENDPOINT)
};
```

**Kubernetes Service Discovery:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: redis-service
spec:
  selector:
    app: redis
  ports:
  - port: 6379
    targetPort: 6379
```

**Key principles:**
- No distinction between local and third-party services
- Swappable via configuration change only
- No code changes to swap backing services
- Connection via URL in environment

### V. Build, Release, Run

**Strictly separate build and run stages**

Three distinct stages:
1. **Build**: Convert code to executable bundle
2. **Release**: Combine build with config
3. **Run**: Execute in target environment

```yaml
# GitHub Actions CI/CD Pipeline
name: Build and Deploy
on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build Docker image
        run: docker build -t myapp:${{ github.sha }} .
      - name: Push to registry
        run: docker push myapp:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        run: kubectl set image deployment/myapp myapp=myapp:${{ github.sha }}
```

**Key principles:**
- Immutable releases (never modify, only deploy new)
- Unique release identifiers (git SHA, semver)
- Rollback by redeploying previous release
- Separate build artifacts from runtime config

### VI. Processes

**Execute the app as one or more stateless processes**

Application processes should be stateless and share-nothing. Store persistent state in backing services.

```javascript
// ❌ Bad: In-memory session store
app.use(session({
  secret: process.env.SESSION_SECRET,
  resave: false
  // Uses memory store by default
}));

// ✓ Good: Store session in Redis
app.use(session({
  store: new RedisStore({
    client: redisClient,
    prefix: 'sess:'
  }),
  secret: process.env.SESSION_SECRET,
  resave: false,
  saveUninitialized: false
}));
```

**Kubernetes Deployment:**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: myapp
spec:
  replicas: 3  # Can scale horizontally
  selector:
    matchLabels:
      app: myapp
  template:
    spec:
      containers:
      - name: myapp
        image: myapp:latest
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
```

**Key principles:**
- Stateless processes enable horizontal scaling
- No sticky sessions
- No local filesystem for persistent data
- Shared state goes in databases, caches, or queues

### VII. Port Binding

**Export services via port binding**

Applications are self-contained and bind to a port:

```javascript
const express = require('express');
const app = express();
const port = process.env.PORT || 3000;

app.listen(port, '0.0.0.0', () => {
  console.log(`Server running on port ${port}`);
});
```

```elixir
# Phoenix endpoint config
config :my_app, MyAppWeb.Endpoint,
  http: [port: String.to_integer(System.get_env("PORT") || "4000")],
  server: true
```

**Kubernetes Service:**

```yaml
apiVersion: v1
kind: Service
metadata:
  name: myapp-service
spec:
  selector:
    app: myapp
  ports:
  - port: 80
    targetPort: 3000
  type: LoadBalancer
```

**Key principles:**
- Bind to `0.0.0.0`, not `localhost`
- Port number from environment variable
- No reliance on runtime injection (e.g., Apache, Nginx)
- HTTP server library embedded in app

### VIII. Concurrency

**Scale out via the process model**

Scale by adding more processes (horizontal scaling), not by making processes larger (vertical scaling):

```yaml
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: myapp-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: myapp
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**Process types (Procfile concept):**

```
web: node server.js
worker: node worker.js
scheduler: node scheduler.js
```

**Key principles:**
- Different process types for different workloads
- Processes can scale independently
- OS process manager handles processes
- Never daemonize or write PID files

### IX. Disposability

**Maximize robustness with fast startup and graceful shutdown**

```javascript
const server = app.listen(port, () => {
  console.log('Server started');
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully');

  server.close(() => {
    // Close database connections
    db.close();

    // Close other connections
    redis.quit();

    console.log('Process terminated');
    process.exit(0);
  });
});
```

**Kubernetes lifecycle hooks:**

```yaml
spec:
  containers:
  - name: myapp
    image: myapp:latest
    lifecycle:
      preStop:
        exec:
          command: ["/bin/sh", "-c", "sleep 15"]
    terminationGracePeriodSeconds: 30
```

**Key principles:**
- Minimize startup time (< 10 seconds ideal)
- Handle SIGTERM for graceful shutdown
- Finish in-flight requests before shutting down
- Robust against sudden death
- Fast startup enables rapid scaling

### X. Dev/Prod Parity

**Keep development, staging, and production as similar as possible**

**Docker Compose for local development:**

```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:15
    environment:
      POSTGRES_DB: myapp
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass

  redis:
    image: redis:7-alpine
```

**Key principles:**
- Use same backing services in dev and prod
- Containers ensure environment consistency
- Infrastructure as code for reproducibility
- Minimize time gap between dev and production
- Same deployment process for all environments

### XI. Logs

**Treat logs as event streams**

Write all logs to stdout/stderr, let the environment handle aggregation:

```javascript
// Structured logging to stdout
const winston = require('winston');

const logger = winston.createLogger({
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.json()
  ),
  transports: [
    new winston.transports.Console()
  ]
});

logger.info('User logged in', {
  userId: 123,
  ip: '192.168.1.1',
  userAgent: 'Mozilla/5.0...'
});
```

```elixir
# Elixir structured logging
require Logger

Logger.info("User logged in",
  user_id: 123,
  ip: "192.168.1.1"
)
```

**Key principles:**
- Never manage log files
- Write unbuffered to stdout
- Use structured logging (JSON)
- Let platform route logs (Fluentd, Logstash)
- Include correlation IDs for tracing

**Anti-patterns:**
- ❌ Writing to log files
- ❌ Log rotation within the app
- ❌ Sending logs directly to aggregation service

### XII. Admin Processes

**Run admin/management tasks as one-off processes**

Database migrations, console, one-time scripts:

```yaml
# Kubernetes Job for database migration
apiVersion: batch/v1
kind: Job
metadata:
  name: db-migration
spec:
  template:
    spec:
      containers:
      - name: migrate
        image: myapp:latest
        command: ["npm", "run", "migrate"]
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: DATABASE_URL
      restartPolicy: OnFailure
```

```yaml
# CronJob for scheduled cleanup
apiVersion: batch/v1
kind: CronJob
metadata:
  name: data-cleanup
spec:
  schedule: "0 2 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: cleanup
            image: myapp:latest
            command: ["npm", "run", "cleanup"]
          restartPolicy: OnFailure
```

**Key principles:**
- Same environment as regular processes
- Same codebase and config
- Run against release, not development code
- Use scheduler for recurring tasks
- Ship admin code with application code

## Modern Extensions (Beyond 12)

### XIII. API First

Design and document APIs before implementation:

```yaml
# OpenAPI specification
openapi: 3.0.0
info:
  title: My API
  version: v1
paths:
  /users:
    get:
      summary: List users
      responses:
        '200':
          description: Success
```

**Key principles:**
- OpenAPI/Swagger specifications
- API versioning (URL or header)
- API gateway pattern
- Contract-first development

### XIV. Telemetry

Comprehensive observability with metrics, tracing, and monitoring:

```yaml
# Prometheus ServiceMonitor
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: myapp-monitor
spec:
  selector:
    matchLabels:
      app: myapp
  endpoints:
  - port: metrics
    path: /metrics
```

**Key principles:**
- Expose /metrics endpoint (Prometheus format)
- Distributed tracing (OpenTelemetry)
- Application Performance Monitoring (APM)
- Custom business metrics
- Health check endpoints

### XV. Security

Authentication, authorization, and security by design:

```javascript
// JWT authentication middleware
function authenticateToken(req, res, next) {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) return res.sendStatus(401);

  jwt.verify(token, process.env.JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
}
```

**Key principles:**
- OAuth 2.0 / OpenID Connect
- RBAC (Role-Based Access Control)
- Secrets in environment, never in code
- TLS everywhere
- Security scanning in CI/CD

## Common Patterns

### Configuration Validation

Validate required configuration at startup:

```javascript
function validateConfig() {
  const required = ['DATABASE_URL', 'JWT_SECRET', 'REDIS_URL'];
  const missing = required.filter(key => !process.env[key]);

  if (missing.length > 0) {
    throw new Error(`Missing required environment variables: ${missing.join(', ')}`);
  }
}

// Call before starting server
validateConfig();
```

### Health Checks

Implement health and readiness endpoints:

```javascript
// Liveness probe
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'healthy',
    timestamp: new Date().toISOString()
  });
});

// Readiness probe
app.get('/ready', async (req, res) => {
  try {
    await db.ping();
    await redis.ping();
    res.status(200).json({ status: 'ready' });
  } catch (err) {
    res.status(503).json({ status: 'not ready', error: err.message });
  }
});
```

**Kubernetes probes:**

```yaml
livenessProbe:
  httpGet:
    path: /health
    port: 3000
  initialDelaySeconds: 10
  periodSeconds: 10

readinessProbe:
  httpGet:
    path: /ready
    port: 3000
  initialDelaySeconds: 5
  periodSeconds: 5
```

### Graceful Degradation

Handle backing service failures gracefully:

```javascript
async function getCachedData(key) {
  try {
    return await redis.get(key);
  } catch (err) {
    logger.warn('Redis unavailable, falling back to database', { error: err.message });
    return await db.query('SELECT data FROM cache WHERE key = ?', [key]);
  }
}
```

## Anti-Patterns to Avoid

### ❌ Environment-Specific Code Paths

```javascript
// DON'T
if (process.env.NODE_ENV === 'production') {
  // Different behavior
} else {
  // Different behavior
}

// DO: Use configuration
const timeout = parseInt(process.env.TIMEOUT || '5000');
```

### ❌ Local File Storage

```javascript
// DON'T: Write to local filesystem
fs.writeFile('/tmp/uploads/' + filename, data);

// DO: Use object storage
await s3.putObject({
  Bucket: process.env.S3_BUCKET,
  Key: filename,
  Body: data
});
```

### ❌ In-Memory State

```javascript
// DON'T: Store state in memory
const sessions = new Map();

// DO: Use external store
const session = await redis.get(`session:${sessionId}`);
```

### ❌ Hardcoded Dependencies

```javascript
// DON'T: Hardcode service locations
const db = connect('localhost:5432');

// DO: Use environment variables
const db = connect(process.env.DATABASE_URL);
```

## Troubleshooting Guide

### Application Won't Start

1. Check required environment variables are set
2. Validate configuration at startup
3. Check backing service connectivity
4. Review logs for initialization errors

### Application Won't Scale

1. Identify stateful operations
2. Move state to backing services
3. Remove file system dependencies
4. Eliminate sticky sessions

### Inconsistent Behavior Across Environments

1. Ensure same backing service types (not SQLite in dev, Postgres in prod)
2. Use containers for dev environment
3. Check for environment-specific code paths
4. Verify configuration is environment-only

### Logs Not Appearing

1. Ensure writing to stdout/stderr
2. Avoid buffering log output
3. Check log aggregation configuration
4. Verify Kubernetes logging sidecar/daemonset

## Best Practices Summary

1. **Environment variables for all configuration**
2. **Stateless processes that can scale horizontally**
3. **Structured logging to stdout**
4. **Containers for development parity**
5. **Automated CI/CD pipelines**
6. **Health checks for orchestration**
7. **Graceful shutdown handling**
8. **Fast startup times (< 10s)**
9. **Immutable releases with unique IDs**
10. **Comprehensive monitoring and telemetry**

## Kubernetes-Specific Best Practices

### Resource Limits

```yaml
resources:
  requests:
    memory: "128Mi"
    cpu: "100m"
  limits:
    memory: "256Mi"
    cpu: "200m"
```

### Init Containers

```yaml
initContainers:
- name: wait-for-db
  image: busybox
  command: ['sh', '-c', 'until nc -z postgres-service 5432; do sleep 1; done']
```

### Pod Disruption Budgets

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: myapp-pdb
spec:
  minAvailable: 1
  selector:
    matchLabels:
      app: myapp
```

## Resources

- **12factor.net**: Original methodology
- **Kubernetes Documentation**: https://kubernetes.io/docs/
- **Docker Best Practices**: https://docs.docker.com/develop/dev-best-practices/
- **OpenTelemetry**: https://opentelemetry.io/
- **Prometheus**: https://prometheus.io/

## Key Insights

> "The twelve-factor methodology can be applied to apps written in any programming language, and which use any combination of backing services (database, queue, memory cache, etc)."

> "A twelve-factor app never relies on implicit existence of state on the filesystem. Even if a process has written something to disk, it must assume that file won't be available on the next request."

Design applications from day one to be cloud-native, scalable, and maintainable. The investment in following these principles pays dividends in operational simplicity and development velocity.
