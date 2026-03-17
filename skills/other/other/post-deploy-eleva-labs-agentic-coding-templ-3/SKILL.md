---
name: post-deploy
description: >-
  Generic post-deployment validation and monitoring tasks. TODO: Implement for shared.
  Invoked by: "/post-deploy", "verify deployment", "post deployment checks".
---

# Post-Deploy

**Status**: Stub - Not Implemented
**Domain**: Shared

## Overview

Generic post-deployment validation skill that provides common verification tasks applicable across all domains. Domain-specific post-deploy skills extend this with specialized checks.

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| environment | Environment to verify | staging, production |
| --skip-health | Skip health checks | --skip-health |
| --verbose | Detailed output | --verbose |

## Usage Examples

```bash
# Run post-deployment checks for production
/post-deploy production

# Verify staging deployment
/post-deploy staging --verbose
```

## Common Checks

- Deployment verification (correct version deployed)
- Basic health endpoint checks
- Log monitoring for errors
- Rollback readiness verification
- Notification to stakeholders

## TODO

- [ ] Define generic post-deployment checklist
- [ ] Add health check templates
- [ ] Add log monitoring integration
- [ ] Define notification workflows
- [ ] Add rollback verification steps
- [ ] Document escalation procedures

---

**End of Skill**
