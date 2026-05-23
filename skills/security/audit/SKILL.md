---
name: audit
description: Comprehensive system audit - analyze backend architecture, security, performance, and frontend UI/UX with browser automation testing. Use when reviewing system health, security posture, or code quality.
argument-hint: "[--backend|--frontend|--security|<area>] [--quick|--deep]"
context: fork
agent: tech-lead
---

# System Audit

Perform a comprehensive system audit covering backend and frontend.

## Input

The user may provide:
- `/audit` — Full system audit (backend + frontend)
- `/audit --backend` — Backend only (architecture, security, performance)
- `/audit --frontend` — Frontend only (UI/UX, browser automation)
- `/audit --security` — Security-focused audit
- `/audit <specific-area>` — Audit specific module (e.g., `/audit auth`)

Optional flags via $ARGUMENTS:
- `--quick` — High-level scan only
- `--deep` — Comprehensive deep dive
- `--live` — Test against live/staging environment

## Process

### 1. Clarify Scope

Ask the user if scope is unclear:
- What areas to focus on? (Full system vs specific modules)
- Which environment? (Local, staging, production)
- Depth of analysis? (Quick scan vs deep audit)

### 2. Backend Analysis

#### Architecture Review
```bash
# Check project structure
tree -L 3 -I 'node_modules|dist|build'

# Analyze TypeScript configuration
cat tsconfig.json

# Review key patterns
grep -r "export class" app/
grep -r "export function" app/
```

Look for:
- [ ] Clean Architecture adherence (layers separation)
- [ ] SOLID principles violations
- [ ] Circular dependencies
- [ ] Code duplication
- [ ] Proper error handling patterns

#### Security Assessment

```bash
# Search for potential security issues
grep -r "process.env" app/ --exclude-dir=node_modules
grep -r "password" app/ -i --exclude-dir=node_modules
grep -r "secret" app/ -i --exclude-dir=node_modules
grep -r "eval(" app/ --exclude-dir=node_modules
```

Check for:
- [ ] Hardcoded secrets or credentials
- [ ] SQL injection vulnerabilities
- [ ] XSS vulnerabilities
- [ ] CSRF protection
- [ ] Authentication/authorization logic
- [ ] Input validation and sanitization

#### Performance Analysis

Analyze:
- [ ] Database query patterns (N+1 queries)
- [ ] Caching strategies
- [ ] Memory usage patterns
- [ ] Async/await usage
- [ ] Bundle size and code splitting

### 3. Frontend Analysis with Browser Automation

#### Critical User Flows Testing

Use `browser_subagent` to test:

**Authentication Flow**
```
TaskName: "Testing Login Flow"
Task: Navigate to the app login page, test the authentication flow:
1. Verify login form is visible
2. Test with valid credentials
3. Verify successful redirect to dashboard
4. Test with invalid credentials and verify error messages
5. Capture screenshots of each state
Return: Pass/Fail status and any UI issues found

RecordingName: audit_login_flow
```

**Main User Journey**
```
TaskName: "Testing Core User Flow"
Task: Test the primary user journey:
1. Navigate through the main workflow
2. Verify all interactive elements work
3. Check for console errors
4. Test responsive design at mobile (375px) and desktop (1920px)
5. Capture screenshots at key steps
Return: List of issues found with screenshots

RecordingName: audit_core_flow
```

**Form Validation**
```
TaskName: "Testing Form Validation"
Task: Test all forms in the application:
1. Submit empty forms - verify validation messages
2. Submit invalid data - verify error handling
3. Submit valid data - verify success states
4. Check accessibility (keyboard navigation, labels)
Return: Validation coverage report

RecordingName: audit_forms
```

#### UI/UX Review

Analyze:
- [ ] Component structure and reusability
- [ ] Responsive design implementation
- [ ] Accessibility compliance (ARIA labels, keyboard navigation)
- [ ] Loading states and error handling
- [ ] Visual consistency
- [ ] Performance (bundle size, render optimization)

### 4. Infrastructure Review (if applicable)

Check:
- [ ] Docker configuration
- [ ] Environment variables management
- [ ] Deployment scripts
- [ ] CI/CD pipeline
- [ ] Monitoring and logging setup

### 5. Generate Audit Report

Create comprehensive report with:

#### Executive Summary
```
System Health Score: X/10
Critical Issues: X
High Priority: X
Medium Priority: X
Total Findings: X
```

#### Backend Findings
For each issue:
```
**[SEVERITY]** Category: Description
- Impact: <potential consequences>
- Location: file:///path/to/file.ts:123
- Recommendation: <fix suggestion>
```

#### Frontend Findings (with Browser Test Results)
```
**Test**: Login Flow
- Status: FAIL
- Issues:
  - Password field not masked properly
  - Error message not accessible
- Screenshots: [login_error.png]
- Recording: audit_login_flow.webp
```

#### Risk Assessment Matrix

| Risk | Severity | Likelihood | Priority | Status |
|------|----------|------------|----------|--------|
| SQL Injection in search | CRITICAL | Medium | P0 | Open |
| Missing rate limiting | HIGH | High | P1 | Open |
| Poor error handling | MEDIUM | Low | P2 | Open |

### 6. Provide Next Steps

Recommend immediate actions:
1. **Critical (P0)**: Fix within 24 hours
2. **High (P1)**: Address within 1 week
3. **Medium (P2)**: Plan for next sprint
4. **Low (P3)**: Add to backlog

## Output Format

1. **Audit Report Document**
   - Save as markdown in project docs
   - Include all findings with evidence
   - Attach screenshots and recordings

2. **Quick Action Items**
   - Top 3 critical fixes needed immediately
   - Recommended order of execution

## Guidelines

- **Be Thorough**: Don't skip areas even if they look fine
- **Use Evidence**: Screenshots and recordings for frontend issues
- **Be Specific**: File paths, line numbers, exact reproduction steps
- **Prioritize**: Not all issues are equal - rank by impact
- **Actionable**: Every finding should have a clear fix recommendation
- **Automate**: Use browser automation extensively for frontend

## Browser Automation Best Practices

When testing frontend:
- Test critical paths first (auth, checkout, core features)
- Capture screenshots at each major step
- Test on multiple viewport sizes
- Check for console errors during flows
- Verify error states display correctly
- Test keyboard navigation and accessibility
- Record evidence for any issues found

## Success Criteria

Audit is complete when:
- [ ] All specified areas analyzed
- [ ] Findings documented with severity and evidence
- [ ] Next steps clearly communicated
- [ ] All browser test recordings saved
