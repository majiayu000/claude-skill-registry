---
name: twelve-factor
description: |
    Use when designing, deploying, or evaluating cloud-native applications — based on the Twelve-Factor App methodology from Heroku.
    USE FOR: cloud-native app design, environment configuration, stateless process design, backing service integration, build/release/run pipelines, dev/prod parity
    DO NOT USE FOR: cloud infrastructure provisioning (use iac), container configuration (use iac/docker or iac/kubernetes), microservice decomposition (use dev/architecture/microservices)
license: MIT
metadata:
  displayName: "Twelve-Factor App"
  author: "Tyler-R-Kendrick"
compatibility: claude, copilot, cursor
references:
  - title: "The Twelve-Factor App"
    url: "https://12factor.net/"
  - title: "Twelve-Factor App Methodology — Wikipedia"
    url: "https://en.wikipedia.org/wiki/Twelve-Factor_App_methodology"
---

# The Twelve-Factor App

## Overview
The Twelve-Factor App is a methodology for building software-as-a-service applications, originally published by Adam Wiggins at Heroku in 2012. It provides a set of best practices for building applications that are portable, scalable, and suitable for deployment on modern cloud platforms.

These factors are technology-agnostic and apply equally to applications written in any language, deployed on any cloud provider or container orchestrator.

## Quick Reference

| # | Factor | One-Line Summary |
|---|--------|------------------|
| 1 | Codebase | One codebase tracked in revision control, many deploys. |
| 2 | Dependencies | Explicitly declare and isolate dependencies. |
| 3 | Config | Store config in the environment. |
| 4 | Backing Services | Treat backing services as attached resources. |
| 5 | Build, Release, Run | Strictly separate build and run stages. |
| 6 | Processes | Execute the app as one or more stateless processes. |
| 7 | Port Binding | Export services via port binding. |
| 8 | Concurrency | Scale out via the process model. |
| 9 | Disposability | Maximize robustness with fast startup and graceful shutdown. |
| 10 | Dev/Prod Parity | Keep development, staging, and production as similar as possible. |
| 11 | Logs | Treat logs as event streams. |
| 12 | Admin Processes | Run admin/management tasks as one-off processes. |

---

## I. Codebase

> One codebase tracked in revision control, many deploys.

A twelve-factor app is always tracked in a version control system (Git, Mercurial). There is a one-to-one correlation between the codebase and the app:
- If there are multiple codebases, it is not an app — it is a distributed system. Each component is an app that can individually comply with twelve-factor.
- Multiple apps sharing the same code is a violation. Factor shared code into libraries managed through the dependency system.

**Multiple deploys** of the same codebase (staging, production, developer local) are different *deploys*, not different apps.

**Modern interpretation:** Monorepos are acceptable as long as each app within the monorepo has its own build pipeline and can be deployed independently. The principle is about deploy independence, not repository structure.

---

## II. Dependencies

> Explicitly declare and isolate dependencies.

A twelve-factor app never relies on the implicit existence of system-wide packages. It declares all dependencies completely and exactly via a **dependency declaration manifest** and uses a **dependency isolation tool** to ensure no implicit dependencies leak in.

| Language | Declaration | Isolation |
|----------|-------------|-----------|
| Node.js | `package.json` | `node_modules` |
| Python | `requirements.txt` / `pyproject.toml` | `venv` / `virtualenv` |
| Go | `go.mod` | Module system |
| .NET | `.csproj` / `Directory.Packages.props` | NuGet restore |
| Rust | `Cargo.toml` | Cargo |
| Java | `pom.xml` / `build.gradle` | Maven/Gradle dependency resolution |

**Modern interpretation:** Container images (Docker) provide an additional layer of isolation. Lock files (`package-lock.json`, `poetry.lock`, `go.sum`) guarantee reproducible builds across environments.

---

## III. Config

> Store config in the environment.

Config is everything that varies between deploys (staging, production, developer environments). This includes:
- Resource handles to backing services (database URLs, cache endpoints)
- Credentials to external services (API keys, OAuth secrets)
- Per-deploy values (canonical hostname, feature flags)

Config does **not** include internal application config that does not vary between deploys (e.g., route definitions, dependency injection wiring).

**The litmus test:** Could the codebase be made open source at any moment without compromising any credentials? If not, config and code are not properly separated.

```typescript
// Bad — hardcoded config
const dbUrl = "postgres://user:pass@prod-db:5432/myapp";

// Good — from the environment
const dbUrl = process.env.DATABASE_URL;
if (!dbUrl) throw new Error("DATABASE_URL is required");
```

**Modern interpretation:** Environment variables remain the lowest common denominator. In Kubernetes, use ConfigMaps for non-sensitive config and Secrets for credentials. Tools like HashiCorp Vault, AWS Secrets Manager, or Azure Key Vault add rotation and auditing. The principle stands: config must not be baked into the artifact.

---

## IV. Backing Services

> Treat backing services as attached resources.

A backing service is any service the app consumes over the network as part of its normal operation: databases (PostgreSQL, MySQL), message queues (RabbitMQ, Kafka), caches (Redis, Memcached), SMTP services, object storage (S3), monitoring systems, and APIs.

The app makes **no distinction** between local and third-party services. A deploy should be able to swap a local PostgreSQL database with one managed by Amazon RDS by changing a config variable — no code changes required.

```
┌──────────┐       DATABASE_URL        ┌───────────────┐
│          │ ──────────────────────────>│  PostgreSQL    │
│   App    │       REDIS_URL           ├───────────────┤
│          │ ──────────────────────────>│  Redis         │
│          │       SMTP_URL            ├───────────────┤
│          │ ──────────────────────────>│  SendGrid      │
└──────────┘                           └───────────────┘
           Attached via config (URLs/credentials)
```

**Modern interpretation:** Service meshes (Istio, Linkerd) and cloud-native connection poolers (PgBouncer, ProxySQL) sit between the app and its backing services. The app still treats them as attached resources configured via environment.

---

## V. Build, Release, Run

> Strictly separate build and run stages.

The three stages:
1. **Build:** Converts code into an executable bundle (compile, bundle assets, install dependencies). Input: code + dependencies. Output: build artifact.
2. **Release:** Combines the build artifact with the deploy's config. Every release has a unique release ID (timestamp, semantic version, or commit SHA). Releases are append-only — you cannot modify a release in place; you create a new one.
3. **Run:** Launches the release in the execution environment.

```
Code ──> [Build] ──> Artifact ──> [Release = Artifact + Config] ──> [Run]
                                       │
                                  Immutable, versioned
```

**Modern interpretation:** CI/CD pipelines (GitHub Actions, GitLab CI, Azure Pipelines) automate the Build stage. Container registries store immutable build artifacts (Docker images). Helm charts, Kustomize overlays, or ArgoCD manifests handle the Release stage. Kubernetes handles the Run stage.

---

## VI. Processes

> Execute the app as one or more stateless processes.

Twelve-factor processes are **stateless** and **share-nothing**. Any data that needs to persist must be stored in a stateful backing service (database, object storage). Memory and filesystem of the process are a single-transaction cache — they must not be relied upon across requests.

This rules out:
- **Sticky sessions** — session state belongs in a backing service (Redis, database).
- **Local file uploads** — uploaded files should go directly to object storage (S3, Azure Blob).
- **In-memory caches that cannot tolerate loss** — use Redis or Memcached.

```typescript
// Bad — sticky session reliance
app.use(session({ store: new MemoryStore() })); // lost on restart/scale

// Good — external session store
app.use(session({ store: new RedisStore({ client: redisClient }) }));
```

**Modern interpretation:** Serverless functions (AWS Lambda, Azure Functions) embody this perfectly — they are ephemeral by design. Containers in Kubernetes may have ephemeral storage, but any state written there is lost when the pod is evicted.

---

## VII. Port Binding

> Export services via port binding.

A twelve-factor app is **completely self-contained**. It does not rely on runtime injection of a webserver (e.g., deploying into Apache/Tomcat). Instead, the app includes its own HTTP server library and binds to a port, listening for requests.

```typescript
import express from "express";

const app = express();
const port = parseInt(process.env.PORT || "3000", 10);

app.listen(port, () => {
    console.log(`Listening on port ${port}`);
});
```

This also means one app can become the backing service for another by providing its URL as a config variable.

**Modern interpretation:** In Kubernetes, containers bind to a port, Services provide stable networking, and Ingress/Gateway controllers handle external routing. The app still binds to a port; the platform handles the rest.

---

## VIII. Concurrency

> Scale out via the process model.

Instead of scaling by making a single process larger (vertical scaling), twelve-factor apps scale by running more processes (horizontal scaling). Different types of work are assigned to different **process types**:

```
web        ──> handles HTTP requests
worker     ──> processes background jobs from a queue
scheduler  ──> triggers periodic tasks
```

Each process type can be independently scaled. Need more HTTP capacity? Run more `web` processes. Background queue growing? Run more `worker` processes.

**Modern interpretation:** Kubernetes Deployments scale process types independently via `replicas`. KEDA (Kubernetes Event Driven Autoscaling) scales based on queue depth or custom metrics. Serverless platforms scale to zero and up automatically.

---

## IX. Disposability

> Maximize robustness with fast startup and graceful shutdown.

Processes should:
- **Start fast** — seconds, not minutes. Fast startup enables rapid elastic scaling and quick deploys.
- **Shut down gracefully** — on receiving `SIGTERM`, stop accepting new work, finish in-progress work, then exit.
- **Be robust against sudden death** — design for crash resilience. Use robust queue systems (work is returned to the queue if the worker dies). Use database transactions. Make jobs idempotent and reentrant.

```typescript
process.on("SIGTERM", async () => {
    console.log("SIGTERM received. Shutting down gracefully...");
    server.close(async () => {
        await database.disconnect();
        await messageQueue.close();
        process.exit(0);
    });

    // Force exit after timeout
    setTimeout(() => process.exit(1), 30_000);
});
```

**Modern interpretation:** Kubernetes sends `SIGTERM` and waits for `terminationGracePeriodSeconds` (default 30s) before sending `SIGKILL`. Liveness and readiness probes ensure traffic is not routed to shutting-down pods.

---

## X. Dev/Prod Parity

> Keep development, staging, and production as similar as possible.

The twelve-factor app minimizes three gaps:

| Gap | Traditional | Twelve-Factor |
|-----|------------|---------------|
| **Time gap** | Weeks between develop and deploy | Hours or minutes (continuous deployment) |
| **Personnel gap** | Developers write, ops deploy | Developers who write code are closely involved in deploying it |
| **Tools gap** | SQLite in dev, PostgreSQL in prod | Same backing services everywhere |

**Resist the temptation to use different backing services in development.** Using SQLite locally but PostgreSQL in production will cause subtle bugs.

**Modern interpretation:** Docker Compose provides identical backing services locally. Dev containers (VS Code Dev Containers, GitHub Codespaces) replicate the full production environment. Infrastructure as Code (Terraform, Pulumi) ensures staging and production are provisioned from the same templates.

---

## XI. Logs

> Treat logs as event streams.

A twelve-factor app never concerns itself with routing or storage of its output stream. It writes all logs to `stdout` as an unbuffered stream of time-ordered events. In development, the developer watches the stream in the terminal. In production, the execution environment captures and routes the stream.

```typescript
// Good — write to stdout
console.log(JSON.stringify({
    timestamp: new Date().toISOString(),
    level: "info",
    message: "Order placed",
    orderId: order.id,
}));

// Bad — writing to a file
fs.appendFileSync("/var/log/app.log", logEntry);
```

**Modern interpretation:** Container runtimes capture stdout/stderr automatically. Log aggregation systems (Datadog, Elastic/ELK, Grafana Loki, AWS CloudWatch) collect, index, and alert on log streams. Structured logging (JSON) enables querying and dashboarding. OpenTelemetry provides a vendor-neutral logging (and tracing) pipeline.

---

## XII. Admin Processes

> Run admin/management tasks as one-off processes.

Administrative tasks (database migrations, REPL console sessions, one-time scripts) should be run as one-off processes in an identical environment to the app's regular long-running processes. They use the same codebase and config, against the same backing services.

```bash
# Run migration using the same artifact and config
kubectl exec -it deploy/myapp -- npx prisma migrate deploy

# Open a REPL in the production environment
kubectl exec -it deploy/myapp -- node

# Run a one-time data fix
kubectl run --rm -it data-fix --image=myapp:v1.2.3 --env=DATABASE_URL=$DB_URL -- node scripts/fix-orphaned-records.js
```

**Modern interpretation:** Kubernetes Jobs and CronJobs formalize one-off and scheduled admin processes. Database migration tools (Flyway, Prisma Migrate, Alembic) integrate into CI/CD pipelines as a release step.

---

## Beyond the Twelve Factors

Kevin Hoffman's *Beyond the Twelve-Factor App* (2016) adds several factors relevant to modern cloud-native development:

| Factor | Description |
|--------|-------------|
| **API First** | Design the API contract before implementation. Use OpenAPI/Swagger, gRPC proto definitions, or AsyncAPI specs. |
| **Telemetry** | Go beyond logs: include metrics (Prometheus, StatsD), distributed tracing (OpenTelemetry, Jaeger), and health checks. |
| **Authentication & Authorization** | Security is not optional. Implement identity (OAuth2, OIDC), token validation, and least-privilege access at the app level. |

## Twelve-Factor Checklist

| # | Factor | Question to Ask |
|---|--------|-----------------|
| 1 | Codebase | Is there exactly one repo for this app? Can it be deployed independently? |
| 2 | Dependencies | Can a new developer clone and run with only the declared manifest? No global installs? |
| 3 | Config | Is every environment-specific value in env vars or a secrets manager? Zero secrets in code? |
| 4 | Backing Services | Can you swap the database provider by changing one config variable? |
| 5 | Build/Release/Run | Is the build artifact immutable? Is every release versioned? |
| 6 | Processes | If the process restarts, is all state preserved in a backing service? |
| 7 | Port Binding | Is the app self-contained with its own HTTP listener? No external webserver dependency? |
| 8 | Concurrency | Can you scale by running more instances, not bigger instances? |
| 9 | Disposability | Does the app start in under 10 seconds? Handle SIGTERM gracefully? |
| 10 | Dev/Prod Parity | Are the same backing services used in dev, staging, and production? |
| 11 | Logs | Does the app write to stdout only? No file-based logging? |
| 12 | Admin Processes | Are migrations and scripts run in the same environment as the app? |

## Best Practices
- Treat the twelve factors as a checklist during architecture reviews and pull requests.
- Adopt factors incrementally — you do not need to satisfy all twelve on day one.
- Use containers (Docker) as the natural packaging for twelve-factor apps: they enforce dependency isolation, port binding, and process disposability.
- Combine twelve-factor with cloud-native patterns: circuit breakers, retries with backoff, health checks, and graceful degradation.
- Automate compliance: use CI checks to verify no secrets in code (Factor III), lock files present (Factor II), and health endpoints exist (Factor IX).
- When twelve-factor conflicts with pragmatism (e.g., local file caching for performance), document the deviation and contain the blast radius.
