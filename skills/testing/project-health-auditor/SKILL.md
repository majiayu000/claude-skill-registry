---
name: project-health-auditor
description: Comprehensive codebase health analysis. Use when reviewing code quality, identifying technical debt, checking dependencies, or assessing project structure.
allowed-tools: Read, Grep, Glob, Bash
---
# Project Health Auditor

> Inspired by [claude-code-plugins-plus](https://github.com/jeremylongshore/claude-code-plugins-plus)

## Purpose

Analyze codebase health across multiple dimensions: code quality, dependencies, security, testing, documentation, and architecture.

## Audit Categories

### 1. Code Quality

#### Complexity Analysis

```bash
# Count lines per file (identify large files)
find src -name "*.ts" -o -name "*.js" | xargs wc -l | sort -n

# Find long functions (over 50 lines)
# Check for deeply nested code
# Identify duplicate code patterns
```

#### Code Smells

| Smell | Indicator | Action |
|-------|-----------|--------|
| Long files | >500 lines | Split into modules |
| Long functions | >50 lines | Extract methods |
| Deep nesting | >4 levels | Flatten logic |
| Many parameters | >5 params | Use objects |
| Duplicate code | Similar blocks | Extract shared |
| Dead code | Unused exports | Remove |
| Magic numbers | Hardcoded values | Use constants |

#### Checklist

```markdown
## Code Quality Audit
- [ ] No files over 500 lines
- [ ] No functions over 50 lines
- [ ] No nesting deeper than 4 levels
- [ ] No functions with >5 parameters
- [ ] No obvious code duplication
- [ ] No dead/unused code
- [ ] Consistent naming conventions
- [ ] Proper error handling
```

### 2. Dependencies

#### Dependency Health

```bash
# Check outdated packages (npm)
npm outdated

# Check for vulnerabilities
npm audit

# Analyze bundle size
npx webpack-bundle-analyzer

# Check unused dependencies
npx depcheck
```

#### Evaluation Criteria

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Outdated (major) | 0 | 1-3 | >3 |
| Outdated (minor) | <5 | 5-10 | >10 |
| Vulnerabilities | 0 | Low/Med | High/Crit |
| Unused deps | 0 | 1-3 | >3 |
| Bundle size | <500KB | 500KB-1MB | >1MB |

#### Checklist

```markdown
## Dependencies Audit
- [ ] No critical vulnerabilities
- [ ] No high vulnerabilities
- [ ] <3 major version updates pending
- [ ] No unused dependencies
- [ ] Lock file in sync
- [ ] Bundle size reasonable
```

### 3. Security

#### Security Checks

```bash
# Check for secrets in code
grep -r "password\|secret\|api_key\|token" --include="*.ts" --include="*.js"

# Check for hardcoded credentials
grep -r "Bearer \|Basic " --include="*.ts"

# Check .env is gitignored
cat .gitignore | grep ".env"
```

#### Security Audit Points

| Check | Concern | Solution |
|-------|---------|----------|
| Secrets in code | Credential exposure | Use env vars |
| .env committed | Secret leak | Add to .gitignore |
| SQL strings | SQL injection | Use parameterized queries |
| User input in HTML | XSS | Sanitize/escape |
| Outdated deps | Known vulns | Update regularly |
| No rate limiting | DoS | Add rate limits |
| No input validation | Injection | Validate all inputs |

#### Checklist

```markdown
## Security Audit
- [ ] No hardcoded secrets
- [ ] .env files gitignored
- [ ] Dependencies scanned for vulns
- [ ] Input validation in place
- [ ] Output encoding for XSS
- [ ] SQL injection prevention
- [ ] Authentication implemented
- [ ] Authorization checks exist
```

### 4. Testing

#### Test Coverage Analysis

```bash
# Run tests with coverage (npm/jest)
npm test -- --coverage

# Run tests with coverage (pytest)
pytest --cov=src --cov-report=html
```

#### Coverage Standards

| Metric | Good | Acceptable | Poor |
|--------|------|------------|------|
| Line coverage | >80% | 60-80% | <60% |
| Branch coverage | >70% | 50-70% | <50% |
| Function coverage | >80% | 60-80% | <60% |

#### Checklist

```markdown
## Testing Audit
- [ ] Unit tests exist
- [ ] Integration tests exist
- [ ] Line coverage >60%
- [ ] Critical paths tested
- [ ] Edge cases covered
- [ ] Tests run in CI
- [ ] Test execution <5 min
- [ ] No flaky tests
```

### 5. Documentation

#### Documentation Inventory

```bash
# Check for README
ls README.md

# Check for API docs
ls docs/ || ls documentation/

# Check for inline docs (JSDoc, docstrings)
grep -r "@param\|@returns\|Args:\|Returns:" src/
```

#### Documentation Standards

| Doc Type | Purpose | Required |
|----------|---------|----------|
| README.md | Project overview | Always |
| CONTRIBUTING.md | Contribution guide | Open source |
| API docs | Endpoint reference | APIs |
| Code comments | Complex logic | As needed |
| Architecture docs | System design | Large projects |
| CHANGELOG.md | Version history | Libraries |

#### Checklist

```markdown
## Documentation Audit
- [ ] README exists and current
- [ ] Installation instructions
- [ ] Usage examples
- [ ] API documentation
- [ ] Contributing guide
- [ ] License specified
- [ ] Complex code documented
```

### 6. Architecture

#### Architecture Review

| Aspect | Check | Concern |
|--------|-------|---------|
| Coupling | Import chains | Tight coupling |
| Cohesion | Module size | God modules |
| Layers | Directory structure | Layer violations |
| Dependencies | Package.json | Circular deps |
| Config | Hardcoded values | Environment issues |

#### Common Issues

```markdown
## Architecture Smells
- Circular dependencies
- God classes/modules
- Feature envy (cross-module reaching)
- Shotgun surgery (changes touch many files)
- Inappropriate intimacy (modules know too much)
```

#### Checklist

```markdown
## Architecture Audit
- [ ] Clear module boundaries
- [ ] No circular dependencies
- [ ] Proper layer separation
- [ ] Configuration externalized
- [ ] Environment-specific settings
- [ ] Scalability considered
- [ ] Single responsibility
```

## Health Report Template

```markdown
# Project Health Report

**Project:** [Name]
**Date:** [Date]
**Auditor:** Claude

## Summary

| Category | Score | Status |
|----------|-------|--------|
| Code Quality | X/10 | 🟢/🟡/🔴 |
| Dependencies | X/10 | 🟢/🟡/🔴 |
| Security | X/10 | 🟢/🟡/🔴 |
| Testing | X/10 | 🟢/🟡/🔴 |
| Documentation | X/10 | 🟢/🟡/🔴 |
| Architecture | X/10 | 🟢/🟡/🔴 |
| **Overall** | **X/10** | **Status** |

## Critical Issues (Fix Immediately)
1. [Issue description]
2. [Issue description]

## High Priority (Fix Soon)
1. [Issue description]
2. [Issue description]

## Recommendations
1. [Recommendation]
2. [Recommendation]

## Technical Debt
- [Debt item with estimated effort]
- [Debt item with estimated effort]
```

## Quick Commands

```bash
# Full audit script
echo "=== Code Stats ===" && cloc src/
echo "=== Dependencies ===" && npm outdated
echo "=== Security ===" && npm audit
echo "=== Test Coverage ===" && npm test -- --coverage
echo "=== TODO/FIXME ===" && grep -r "TODO\|FIXME" src/
```
