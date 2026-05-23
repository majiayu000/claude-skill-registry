---
name: [PROJECT]-deployment-patterns
description: [PROJECT] CI/CD pipeline and deployment automation patterns
globs: [".github/workflows/**/*.yml", ".gitlab-ci.yml", "Jenkinsfile", "**/Dockerfile", "docker-compose.yml"]
---

# Deployment Automation Patterns

> **Template for project-specific deployment patterns skill**
> Fill in [CUSTOMIZE] sections with your project's deployment infrastructure

**Project**: [PROJECT NAME]
**Platform**: [CUSTOMIZE: GitHub Actions / GitLab CI / Jenkins / CircleCI]
**Last Updated**: [DATE]

---

## CI/CD Platform

### Configuration Files

**Location**: [CUSTOMIZE: .github/workflows/ / .gitlab-ci.yml / Jenkinsfile / .circleci/]

**File Structure**:
```
[CUSTOMIZE: Show your pipeline file organization]

Examples:
- GitHub Actions: .github/workflows/ci.yml, deploy-staging.yml, deploy-production.yml
- GitLab CI: .gitlab-ci.yml (single file with stages)
- Jenkins: Jenkinsfile (declarative or scripted)
```

---

## CI Pipeline (Test + Build)

### Trigger

**Events**: [CUSTOMIZE: push to main/develop / pull requests / merge requests]

**Branches**: [CUSTOMIZE: main, develop, feature/* / all branches]

### Stages

**[CUSTOMIZE WITH YOUR PIPELINE STAGES]**

**Your Pipeline Flow**:
```
[CUSTOMIZE: Describe your stages]

Examples:
1. Checkout code
2. Install dependencies (with caching)
3. Lint code
4. Run unit tests (backend)
5. Run unit tests (frontend)
6. Run integration tests
7. Run E2E tests
8. Build artifacts
9. Upload artifacts
```

### Parallelization

**Jobs Running in Parallel**:
```yaml
[CUSTOMIZE: Show parallel jobs]

Example (GitHub Actions):
jobs:
  backend-tests:
    runs-on: ubuntu-latest
  frontend-tests:
    runs-on: ubuntu-latest
  # Both run simultaneously
```

### Caching Strategy

**Dependencies**:
```yaml
[CUSTOMIZE: Show dependency caching]

Examples:
- Maven: cache: 'maven'
- npm: cache: 'npm'
- pip: cache: 'pip'
```

**Build Artifacts**:
```yaml
[CUSTOMIZE: Show build artifact caching]
```

---

## CD Pipeline (Deployment)

### Environments

**Environment Matrix**:

| Environment | Trigger | Approval | URL |
|-------------|---------|----------|-----|
| [Dev/Staging] | [Auto on push] | [No] | [URL] |
| [Production] | [Manual/Tag] | [Yes] | [URL] |

### Deployment Strategy

**Approach**: [CUSTOMIZE: Rolling / Blue-Green / Canary / Recreate]

**Why This Strategy**: [CUSTOMIZE: Reasoning]

**Rollback Plan**:
```bash
[CUSTOMIZE: How to rollback]

Examples:
- Kubernetes: kubectl rollout undo
- Docker: docker-compose pull <previous-tag>
- Cloud: Revert to previous deployment
```

---

## Containerization

### Docker Setup

**Dockerfile Location**: [CUSTOMIZE: ./Dockerfile / backend/Dockerfile / Dockerfile.production]

**Base Images**:
- Backend: [CUSTOMIZE: eclipse-temurin:17-jre-alpine / node:22-alpine / python:3.11-slim]
- Frontend: [CUSTOMIZE: node:22-alpine + nginx:alpine / Static hosting]

### Multi-Stage Build Pattern

**[CUSTOMIZE WITH YOUR DOCKERFILE PATTERN]**

**Backend Example**:
```dockerfile
[CUSTOMIZE: Show your multi-stage Dockerfile]

Example pattern:
# Stage 1: Build
FROM [build-image] AS builder
WORKDIR /app
COPY [dependency-files]
RUN [install-deps]
COPY [source]
RUN [build-command]

# Stage 2: Runtime
FROM [runtime-image]
COPY --from=builder /app/[artifact] /app/
CMD [start-command]
```

### Docker Compose

**Services**: [CUSTOMIZE: backend, frontend, database, redis, etc.]

**Local Development Setup**:
```yaml
[CUSTOMIZE: Show docker-compose.yml structure]
```

---

## Secrets Management

### Where Secrets Are Stored

**Platform**: [CUSTOMIZE: GitHub Secrets / GitLab Variables / Jenkins Credentials / Vault]

**Required Secrets**:
```
[CUSTOMIZE: List all secrets needed]

Examples:
- DOCKER_USERNAME
- DOCKER_PASSWORD
- DATABASE_URL_STAGING
- DATABASE_URL_PRODUCTION
- API_KEY
- JWT_SECRET
```

### How Secrets Are Used

**In Pipeline**:
```yaml
[CUSTOMIZE: Show secret usage pattern]

Example (GitHub Actions):
env:
  DATABASE_URL: ${{ secrets.DATABASE_URL }}
```

---

## Deployment Commands

### Staging Deployment

**Trigger**: [CUSTOMIZE: Auto on push to main / Manual]

**Commands**:
```bash
[CUSTOMIZE: Show deployment commands]

Examples:
- Docker: docker-compose pull && docker-compose up -d
- Kubernetes: kubectl apply -f k8s/
- Cloud: eb deploy staging
- SSH: ssh user@staging 'cd app && git pull && restart'
```

### Production Deployment

**Trigger**: [CUSTOMIZE: Manual workflow / Git tag / Release]

**Approval**: [CUSTOMIZE: Required reviewers / Manual gate]

**Commands**:
```bash
[CUSTOMIZE: Show production deployment]
```

---

## Health Checks & Smoke Tests

### Health Endpoints

**Backend**: [CUSTOMIZE: /health / /actuator/health / /api/health]

**Frontend**: [CUSTOMIZE: /health / / (root) / /api/health]

**Database**: [CUSTOMIZE: /health/db / Connection check]

### Smoke Tests

**Post-Deployment Verification**:
```bash
[CUSTOMIZE: Show smoke test commands]

Examples:
sleep 10  # Wait for startup
curl -f https://api.myapp.com/health || exit 1
curl -f https://myapp.com/ || exit 1
```

---

## Database Migrations

### Migration Tool

**Tool**: [CUSTOMIZE: Flyway / Liquibase / Prisma Migrate / Django migrations / Rails migrations]

**When Migrations Run**: [CUSTOMIZE: Before deployment / After deployment / Separate job]

**Example**:
```bash
[CUSTOMIZE: Show migration command]

Examples:
- Flyway: mvn flyway:migrate
- Prisma: npx prisma migrate deploy
- Django: python manage.py migrate
```

### Rollback Strategy

**Migration Rollback**:
```bash
[CUSTOMIZE: How to rollback migrations]
```

---

## Monitoring & Logging

### Monitoring Tools

**Uptime**: [CUSTOMIZE: UptimeRobot / Pingdom / DataDog]

**Error Tracking**: [CUSTOMIZE: Sentry / Rollbar / Bugsnag]

**Logs**: [CUSTOMIZE: Papertrail / CloudWatch / Loggly]

**Metrics**: [CUSTOMIZE: Prometheus / New Relic / DataDog]

### Log Aggregation

**Where Logs Go**: [CUSTOMIZE: Stdout → Cloud logging / File → Aggregator]

**Log Format**: [CUSTOMIZE: JSON / Plain text / Structured]

---

## Build Optimization

### Build Time Targets

**CI Build**: [CUSTOMIZE: <5 minutes / <10 minutes]

**Local Build**: [CUSTOMIZE: <2 minutes / <3 minutes]

### Optimization Techniques

**[CUSTOMIZE WITH USED TECHNIQUES]**

- [ ] Dependency caching (Maven, npm, pip)
- [ ] Build artifact caching
- [ ] Docker layer caching
- [ ] Parallel job execution
- [ ] [PROJECT-SPECIFIC OPTIMIZATION]

---

## Security Scanning

### Tools

**Dependency Scanning**: [CUSTOMIZE: Dependabot / Snyk / OWASP Dependency Check]

**Container Scanning**: [CUSTOMIZE: Trivy / Snyk / Clair]

**SAST**: [CUSTOMIZE: SonarQube / CodeQL / Semgrep]

### Scan Timing

**When**: [CUSTOMIZE: Every PR / Nightly / Weekly]

**Failure Threshold**: [CUSTOMIZE: Critical vulnerabilities / High+ / All]

---

## Deployment Checklist

**[CUSTOMIZE WITH PROJECT REQUIREMENTS]**

Before deploying:
- [ ] All tests passing (unit, integration, E2E)
- [ ] Code coverage ≥ [80]%
- [ ] Build successful
- [ ] No critical security vulnerabilities
- [ ] Database migrations reviewed
- [ ] Secrets configured in environment
- [ ] Health checks implemented
- [ ] Smoke tests defined
- [ ] Rollback plan documented
- [ ] [PROJECT-SPECIFIC REQUIREMENT]

---

## Project-Specific Patterns

**[CUSTOMIZE - ADD DEPLOYMENT CONTEXT]**

### Deployment Windows
- [When deployments are allowed]

### Approval Process
- [Who must approve]
- [What must be verified]

### Post-Deployment Steps
- [Smoke tests]
- [Monitoring checks]
- [Team notifications]

---

**Customization Complete**: Replace all [CUSTOMIZE] sections with project-detected or chosen patterns.

**Auto-generated by**: `/add-skill deployment-automation` command
