---
name: quality
description: "Comprehensive code quality assessment in spaces/[project]/. Use before commits, merges, or releases to ensure consistent quality."
model: claude-sonnet-4-20250514
allowed-tools: Read, Glob, Grep, Bash, Task
---

# /quality

Comprehensive quality assessment of code using multi-agent analysis.

## Usage

```bash
/quality yourbench                  # Full assessment
/quality yourbench --focus security # Security-focused
/quality coordinatr --focus testing # Test coverage focus
```

## Focus Areas

| Flag | Analysis | Agent |
|------|----------|-------|
| (none) | All dimensions | All specialists |
| `--focus security` | OWASP, vulnerabilities | security-auditor |
| `--focus performance` | Bottlenecks, N+1 | performance-optimizer |
| `--focus testing` | Coverage, test quality | test-engineer |
| `--focus code` | Maintainability | code-reviewer |

## Execution Flow

### 1. Locate Project

```bash
ls spaces/[project]/
```

### 2. Run Automated Checks

```bash
cd spaces/[project]
npm test -- --coverage
npm run lint
npm run type-check  # if TypeScript
```

### 3. Agent Analysis

Coordinate specialists via Task tool:
- **code-reviewer**: Complexity, best practices
- **security-auditor**: OWASP Top 10
- **performance-optimizer**: N+1 queries, bottlenecks
- **test-engineer**: Coverage, test quality

### 4. Generate Report

```markdown
## Quality Assessment: [project]

**Overall Score: XX/100** [status]

### Code Quality: XX/100
- Issues found
- Recommendations

### Security: XX/100
- Critical/High/Medium issues
- Recommendations

### Performance: XX/100
- Bottlenecks identified
- Recommendations

### Testing: XX/100
- Coverage percentage
- Untested areas

### Priority Actions
1. **CRITICAL**: [action]
2. **HIGH**: [action]
3. **MEDIUM**: [action]
```

## Scoring

| Score | Status | Meaning |
|-------|--------|---------|
| 90-100 | Excellent | Ship it |
| 80-89 | Good | Minor improvements |
| 70-79 | Acceptable | Address soon |
| 60-69 | Concerning | Fix before merge |
| <60 | Critical | Must fix |

## Quality Dimensions

### Code Quality
- Cyclomatic complexity
- Code duplication
- SOLID principles
- Dead code detection

### Security
- OWASP Top 10
- Auth/authz patterns
- Input validation
- Secrets in code

### Performance
- N+1 query detection
- Inefficient algorithms
- Bundle size
- Caching opportunities

### Testing
- Line/branch coverage
- Test quality
- Edge case coverage
- Integration test gaps

## When to Use

- Before major release
- Onboarding to new codebase
- Periodic health checks
- Before refactoring
