---
name: project-health-check
description: Complete project health audit (7 checks)
user-invocable: true
---

# Project Health Check

Comprehensive 7-point audit for project health.

---

## 7-Point Audit

### 1. Documentation
- [ ] README is accurate
- [ ] API docs exist
- [ ] Code comments explain "why"

### 2. Test Coverage
- [ ] Coverage > 80%
- [ ] Critical paths tested
- [ ] Edge cases covered

### 3. Security
- [ ] No secrets in code
- [ ] No vulnerable dependencies
- [ ] Input validation exists

### 4. Code Quality
- [ ] Linting passes
- [ ] No large files (> 500 lines)
- [ ] Consistent naming

### 5. Dependencies
- [ ] No outdated majors
- [ ] No unused deps
- [ ] Compatible licenses

### 6. Database
- [ ] Schema documented
- [ ] Migrations versioned
- [ ] Indexes documented

### 7. Build/Deploy
- [ ] Build succeeds
- [ ] CI/CD exists
- [ ] Env vars documented

---

## Health Score Template

```markdown
# Project Health Report - [Date]

## Overall Score: [X]/100

| Area | Score | Status |
|------|-------|--------|
| Documentation | /15 | |
| Test Coverage | /15 | |
| Security | /20 | |
| Code Quality | /15 | |
| Dependencies | /15 | |
| Database | /10 | |
| Build/Deploy | /10 | |

### Critical Issues
1. [Fix immediately]

### Warnings
1. [Fix this week]

### Suggestions
1. [Consider]
```

---

## Frequency

| Check | When |
|-------|------|
| Quick | Weekly |
| Standard | Bi-weekly |
| Full | Monthly |
