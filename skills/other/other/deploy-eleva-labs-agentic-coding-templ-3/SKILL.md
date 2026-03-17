---
name: deploy
description: >-
  Deploy applications to target environments. TODO: Implement for devops.
  Invoked by: "/deploy", "/deploy staging", "/deploy production".
---

# Deploy

**Status**: Stub - Not Implemented
**Domain**: DevOps

## Overview

Unified deployment skill for deploying applications to any environment (staging, production, development, etc.). Consolidates environment-specific deployment logic into a single skill with environment as an argument.

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| environment | Target deployment environment | staging, production, dev |

## Usage Examples

```bash
# Deploy to staging (default)
/deploy staging

# Deploy to production
/deploy production

# Deploy without argument (prompts for environment)
/deploy
```

## TODO

- [ ] Define deployment workflow for each environment
- [ ] Add templates for environment configuration
- [ ] Define blue-green and canary deployment strategies
- [ ] Add pre-deployment validation checks
- [ ] Add supporting files for health checks
- [ ] Document rollback procedures
- [ ] Document incident response procedures
- [ ] Define environment variable management
- [ ] Add smoke test automation

---

**End of Skill**
