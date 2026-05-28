---
name: Release Checklist Gate
description: Checklist gate สำหรับ production release ครอบคลุม testing, documentation, rollback plan, และ stakeholder sign-off
---

# Release Checklist Gate

## Overview

Checklist gate สำหรับ production release - ต้องผ่านทุกข้อก่อน deploy ไป production

## Why This Matters

- **Safety**: ไม่ลืมขั้นตอนสำคัญ
- **Quality**: Release มี standard
- **Accountability**: รู้ว่าใครอนุมัติ
- **Rollback ready**: พร้อม rollback ถ้ามีปัญหา

---

## Release Checklist

```markdown
## Pre-Release Checklist

### Code Quality
☐ All tests passing (unit, integration, E2E)
☐ Code review approved
☐ No critical/high security issues
☐ Performance benchmarks pass
☐ No known bugs (P0/P1)

### Documentation
☐ Changelog updated
☐ Release notes written
☐ API docs updated (if applicable)
☐ Migration guide (if breaking changes)
☐ Runbook updated

### Testing
☐ Smoke tests pass in staging
☐ Load testing completed (if needed)
☐ Security testing completed
☐ UAT completed (if applicable)
☐ Rollback tested

### Infrastructure
☐ Database migrations tested
☐ Feature flags configured
☐ Monitoring/alerts in place
☐ Rollback plan documented
☐ Capacity planning done

### Communication
☐ Stakeholders notified
☐ Support team briefed
☐ Customers notified (if needed)
☐ Status page prepared

### Approvals
☐ Tech lead approval
☐ Product owner approval
☐ Security team approval (if needed)
☐ Change management approval

### Deployment
☐ Deployment window scheduled
☐ On-call engineer assigned
☐ Deployment runbook ready
☐ Rollback command ready
```

---

## Automated Checks

```yaml
# .github/workflows/release-gate.yml
name: Release Gate
on:
  push:
    tags:
      - 'v*'

jobs:
  release-gate:
    runs-on: ubuntu-latest
    steps:
      - name: Check Tests
        run: npm test
      
      - name: Check Security
        run: npm audit --audit-level=high
      
      - name: Check Changelog
        run: |
          if ! grep -q "${{ github.ref_name }}" CHANGELOG.md; then
            echo "Changelog not updated"
            exit 1
          fi
      
      - name: Check Approvals
        uses: actions/github-script@v6
        with:
          script: |
            const approvals = await github.rest.pulls.listReviews({
              owner: context.repo.owner,
              repo: context.repo.repo,
              pull_number: context.issue.number
            });
            if (approvals.data.length < 2) {
              throw new Error('Need 2 approvals');
            }
```

---

## Release Template

```markdown
## Release v1.2.3

### Summary
[Brief description of release]

### Changes
- Feature: Added user authentication
- Bug fix: Fixed login timeout
- Performance: Improved API response time

### Breaking Changes
- None

### Migration Steps
1. Run database migration: `npm run migrate`
2. Update environment variables
3. Restart services

### Rollback Plan
```bash
# Rollback to v1.2.2
kubectl set image deployment/api api=myapp:v1.2.2
npm run migrate:rollback
```

### Testing
- ✓ All tests pass
- ✓ Smoke tests pass in staging
- ✓ Load testing completed

### Approvals
- ✓ Tech Lead: @john
- ✓ Product Owner: @jane
- ✓ Security: @bob

### Deployment
- Date: 2024-01-16
- Time: 10:00 AM UTC
- On-call: @alice
```

---

## Summary

**Release Checklist Gate:** ต้องผ่านทุกข้อก่อน release

**Categories:**
- Code quality (tests, review, security)
- Documentation (changelog, notes, runbook)
- Testing (smoke, load, UAT)
- Infrastructure (migrations, monitoring)
- Communication (stakeholders, support)
- Approvals (tech lead, product, security)

**Enforcement:**
- Automated checks (CI)
- Manual checklist (release template)
- Required approvals (2+ reviewers)

**No release without complete checklist**
