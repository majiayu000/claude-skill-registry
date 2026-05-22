---
name: post-deploy
description: >-
  Frontend post-deployment validation and performance checks. TODO: Implement for frontend.
  Invoked by: "/post-deploy", "verify deployment", "lighthouse check", "cdn check".
---

# Post-Deploy (Frontend)

**Status**: Stub - Not Implemented
**Domain**: Frontend

## Overview

Frontend-specific post-deployment skill for verifying CDN cache invalidation, running Lighthouse performance audits, and validating static asset delivery after deploying web applications.

## Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| environment | Target environment | staging, production |
| --skip-lighthouse | Skip Lighthouse audit | --skip-lighthouse |
| --skip-cdn | Skip CDN verification | --skip-cdn |

## Usage Examples

```bash
# Run all post-deployment checks
/post-deploy production

# Quick verification without Lighthouse
/post-deploy staging --skip-lighthouse

# Full production verification
/post-deploy production --verbose
```

## Frontend-Specific Checks

- CDN cache invalidation verification
- Lighthouse performance audit (Performance, Accessibility, SEO, Best Practices)
- Static asset delivery verification
- Service worker update verification
- Analytics tracking verification
- A/B test configuration verification
- CSP and security header checks
- Third-party script loading verification

## TODO

- [ ] Define CDN cache invalidation workflow
- [ ] Add Lighthouse CI integration
- [ ] Define performance budget checks
- [ ] Add analytics verification steps
- [ ] Document A/B test verification
- [ ] Add security header validation
- [ ] Define bundle size regression checks

---

**End of Skill**
