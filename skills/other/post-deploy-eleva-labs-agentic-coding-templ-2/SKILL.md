---
name: post-deploy
description: >-
  Backend post-deployment health checks and monitoring. TODO: Implement for backend.
  Invoked by: "/post-deploy", "verify deployment", "health check", "api monitoring".
---

# Post-Deploy (Backend)

**Status**: Stub - Not Implemented
**Domain**: Backend

## Overview

Backend-specific post-deployment skill for verifying service health, running smoke tests against APIs, monitoring error rates, and validating database migrations after deploying server applications.

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| environment | Target environment | staging, production |
| --skip-smoke | Skip smoke tests | --skip-smoke |
| --skip-db | Skip database verification | --skip-db |

## Usage Examples

```bash
# Run all post-deployment checks
/post-deploy production

# Quick health check without smoke tests
/post-deploy staging --skip-smoke

# Full production verification
/post-deploy production --verbose
```

## Backend-Specific Checks

- Health endpoint verification (/health, /ready, /live)
- API smoke tests (critical endpoints)
- Database migration verification
- Connection pool health
- Cache connectivity (Redis, Memcached)
- Message queue connectivity (RabbitMQ, Kafka)
- Error rate monitoring (Sentry, Datadog)
- Response time baseline verification
- Log aggregation verification

## TODO

- [ ] Define health check endpoint standards
- [ ] Add smoke test templates
- [ ] Define database migration verification
- [ ] Add monitoring integration guide
- [ ] Document rollback procedures
- [ ] Add connection pool verification
- [ ] Define error rate thresholds

---

**End of Skill**
