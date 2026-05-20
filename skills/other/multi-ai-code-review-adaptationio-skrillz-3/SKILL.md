---
name: multi-ai-code-review
description: Multi-perspective code review using Claude, Gemini, and Codex as specialized agents. 5-dimensional analysis (security, performance, maintainability, correctness, style) with LLM-as-judge consensus, quality scoring, and CI/CD integration. Use when reviewing PRs, auditing code quality, preparing production releases, or establishing code review workflows.
allowed-tools: Task, Read, Write, Edit, Glob, Grep, Bash
---

# Multi-AI Code Review

## Overview

multi-ai-code-review provides comprehensive code review using multiple AI models as specialized agents, each analyzing code from a different perspective. Based on 2024-2025 best practices for AI-assisted code review.

**Purpose**: Multi-perspective code quality assessment using AI ensemble with human oversight

**Pattern**: Task-based (5 independent review dimensions + orchestration)

**Key Principles** (validated by tri-AI research):
1. **Multi-Agent Architecture** - Specialized agents for each review dimension
2. **LLM-as-Judge Consensus** - Flag issues only when 2+ models agree
3. **Progressive Severity** - Critical → High → Medium → Low prioritization
4. **Human-in-Loop** - AI suggests, human decides
5. **Quality Gates** - Block merges for critical unresolved issues
6. **Actionable Feedback** - Every comment has What/Where/Why/How

**Quality Targets**:
- False Positive Rate: <15%
- Fix Acceptance Rate: >40%
- Review Turnaround: <5 minutes
- Bug Catch Rate: >30% pre-production

---

## When to Use

Use multi-ai-code-review when:

- Reviewing pull requests (any size)
- Auditing code quality before release
- Establishing consistent code review standards
- Security auditing code changes
- Performance profiling changes
- Technical debt assessment
- Onboarding reviews (mentorship mode)

**When NOT to Use**:
- Trivial changes (typos, comments only)
- Automated dependency updates (use dependabot labels)
- Generated code (migrations, scaffolds)

---

## Prerequisites

### Required
- Code to review (diff, file, or directory)
- At least one AI available (Claude required, Gemini/Codex optional)

### Recommended
- Gemini CLI for web research and fast analysis
- Codex CLI for deep code reasoning
- Git repository context

### Integration
- GitHub Actions (optional, for CI/CD)
- Pre-commit hooks (optional, for local checks)

---

## Review Dimensions

### 5-Dimensional Analysis

| Dimension | Agent | Focus | Weight |
|-----------|-------|-------|--------|
| **Security** | Security Specialist | OWASP Top 10, secrets, injection | 25% |
| **Performance** | Performance Engineer | Complexity, memory, latency | 20% |
| **Maintainability** | Architect | Patterns, modularity, DRY | 25% |
| **Correctness** | QA Engineer | Logic, edge cases, tests | 20% |
| **Style** | Nitpicker | Naming, formatting, conventions | 10% |

### Severity Levels

| Level | Action | Examples |
|-------|--------|----------|
| **Critical** | Block merge | SQL injection, exposed secrets, data loss |
| **High** | Require fix | Race conditions, missing auth, memory leaks |
| **Medium** | Suggest fix | Code duplication, missing tests, complexity |
| **Low** | Optional | Style issues, naming, minor refactors |

---

## Operations

### Operation 1: Quick Security Scan

**Time**: 2-5 minutes
**Automation**: 80%
**Purpose**: Fast security-focused review

**Process**:

1. **Scan for Critical Issues**:
```
Review this code for security vulnerabilities:
- SQL injection
- XSS vulnerabilities
- Hardcoded secrets/API keys
- Authentication bypasses
- Authorization flaws
- Input validation gaps
- Insecure dependencies

Code:
[PASTE CODE OR DIFF]

For each issue found, provide:
- Severity (Critical/High/Medium)
- Location (file:line)
- Description (what's wrong)
- Fix (specific code change)
```

2. **Validate with Gemini** (optional):
```bash
gemini -p "Verify these security findings. Are any false positives?
[PASTE CLAUDE FINDINGS]

Code context:
[PASTE RELEVANT CODE]"
```

3. **Output**: Security report with consensus findings

---

### Operation 2: Comprehensive PR Review

**Time**: 10-30 minutes
**Automation**: 60%
**Purpose**: Full multi-dimensional review

**Process**:

**Step 1: Gather Context**
```bash
# Get PR diff
git diff main...HEAD > /tmp/pr_diff.txt

# Identify affected areas
grep -E "^(\\+\\+\\+|---)" /tmp/pr_diff.txt | head -20
```

**Step 2: Run Parallel Agent Reviews**

Use Task tool to launch parallel agents:

```
Launch 3 parallel review agents:

Agent 1 (Security):
"Review this diff for security issues. Focus on:
- OWASP Top 10 vulnerabilities
- Authentication/authorization
- Input validation
- Secrets exposure
Diff: [DIFF]"

Agent 2 (Maintainability):
"Review this diff for maintainability. Focus on:
- Design patterns used correctly
- Code duplication (DRY)
- Modularity and cohesion
- Documentation quality
Diff: [DIFF]"

Agent 3 (Correctness):
"Review this diff for correctness. Focus on:
- Logic errors
- Edge cases not handled
- Test coverage gaps
- Error handling
Diff: [DIFF]"
```

**Step 3: Orchestrate & Deduplicate**
```
Synthesize findings from all agents:
[PASTE ALL AGENT OUTPUTS]

Tasks:
1. Remove duplicate findings
2. Rank by severity (Critical > High > Medium > Low)
3. Group by file
4. Generate summary table
5. Create final report with consensus issues only
```

**Step 4: Generate Report**

Output format:
```markdown
## PR Review Summary

| File | Risk | Issues | Critical | High | Medium |
|------|------|--------|----------|------|--------|
| auth.py | High | 3 | 1 | 2 | 0 |
| api.py | Medium | 2 | 0 | 1 | 1 |

### Critical Issues (Block Merge)
1. **[auth.py:45]** SQL Injection vulnerability
   - Why: User input directly in query
   - Fix: Use parameterized queries

### High Issues (Require Fix)
...

### Consensus Score: 72/100
- Security: 65/100
- Performance: 80/100
- Maintainability: 70/100
- Correctness: 75/100
- Style: 85/100
```

---

### Operation 3: LLM-as-Judge Tribunal

**Time**: 5-15 minutes
**Automation**: 70%
**Purpose**: High-confidence findings through consensus

**Process**:

1. **Run Code Through Multiple Models**:

**Claude Analysis**:
```
Analyze this code for issues. Rate severity 1-10 for each:
[CODE]
```

**Gemini Analysis** (via CLI):
```bash
gemini -p "Analyze this code for issues. Rate severity 1-10 for each:
[CODE]"
```

**Codex Analysis** (via CLI):
```bash
codex "Analyze this code for issues. Rate severity 1-10 for each:
[CODE]"
```

2. **Calculate Consensus**:
```
Given these analyses from 3 AI models:

Claude: [FINDINGS]
Gemini: [FINDINGS]
Codex: [FINDINGS]

Identify issues where at least 2 models agree:
1. List consensus findings
2. Average severity scores
3. Note any disagreements
4. Final verdict for each issue
```

3. **Output**: High-confidence issue list (≥67% agreement)

---

### Operation 4: Mentorship Review

**Time**: 15-30 minutes
**Automation**: 40%
**Purpose**: Educational code review for learning

**Process**:

```
Review this code in mentorship mode. For a developer learning [LANGUAGE/FRAMEWORK]:

Code: [CODE]

For each finding:
1. **What's the issue** (be encouraging, not critical)
2. **Why it matters** (explain the underlying concept)
3. **How to improve** (show before/after with explanation)
4. **Learn more** (link to relevant documentation)

Also highlight:
- What was done well
- Good patterns to continue using
- Growth opportunities

Tone: Supportive and educational, never condescending.
```

---

### Operation 5: Pre-Release Audit

**Time**: 30-60 minutes
**Automation**: 50%
**Purpose**: Comprehensive review before production

**Process**:

1. **Full Codebase Scan**:
```bash
# Identify all changes since last release
git diff v1.0.0...HEAD --stat
git log v1.0.0...HEAD --oneline
```

2. **Security Deep Dive**:
- Run all security checks
- Verify no new vulnerabilities
- Check dependency updates
- Audit secrets management

3. **Performance Review**:
- Identify potential bottlenecks
- Review database queries
- Check for N+1 problems
- Validate caching strategies

4. **Test Coverage**:
- Verify test coverage targets
- Check critical path coverage
- Validate edge case tests

5. **Generate Release Report**:
```markdown
## Pre-Release Audit: v1.1.0

### Security Clearance: PASS ✓
- No critical vulnerabilities
- All high issues resolved
- Secrets audit: Clean

### Performance Assessment: PASS ✓
- No new N+1 queries
- Response time within SLA
- Memory usage stable

### Test Coverage: 82% (target: 80%)
- Critical paths: 95%
- Edge cases: 78%

### Release Recommendation: APPROVED
```

---

## Multi-AI Coordination

### Agent Assignment Strategy

| Task | Primary | Verification | Speed |
|------|---------|--------------|-------|
| Security scan | Claude | Gemini | Fast |
| Architecture review | Claude | Codex | Medium |
| Logic validation | Codex | Claude | Medium |
| Style checking | Gemini | Claude | Fast |
| Performance analysis | Claude | Codex | Medium |

### Coordination Commands

**Launch Multi-Agent Review**:
```bash
# Using Task tool for parallel execution
# Each agent reviews independently, orchestrator synthesizes
```

**Gemini Quick Check**:
```bash
gemini -p "Quick security scan of this code: [CODE]"
```

**Codex Deep Analysis**:
```bash
codex "Analyze this code architecture and suggest improvements: [CODE]"
```

---

## CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/ai-review.yml
name: Multi-AI Code Review
on: [pull_request]

jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Get PR Diff
        run: |
          git diff origin/main...HEAD > pr_diff.txt

      - name: Claude Review
        uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          model: "claude-sonnet-4-5-20250929"
          review_level: "detailed"

      - name: Post Summary
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## AI Review Summary\n${process.env.REVIEW_SUMMARY}`
            })
```

### Quality Gate Configuration

```yaml
# Block merge for critical issues
quality_gates:
  critical_issues: 0      # Must be zero
  high_issues: 3          # Max allowed
  coverage_minimum: 80    # Percent
  score_minimum: 70       # Out of 100
```

---

## Quality Scoring

### Scoring Formula

```
Overall = (Security × 0.25) + (Performance × 0.20) +
          (Maintainability × 0.25) + (Correctness × 0.20) +
          (Style × 0.10)
```

### Grade Mapping

| Score | Grade | Status |
|-------|-------|--------|
| ≥90 | A | Excellent - Ship it |
| 80-89 | B | Good - Minor fixes |
| 70-79 | C | Acceptable - Address issues |
| 60-69 | D | Needs work - Significant fixes |
| <60 | F | Failing - Major revision needed |

---

## Anti-Patterns to Detect

1. **Hardcoded Secrets** - API keys, passwords in code
2. **SQL Injection** - Unparameterized queries
3. **XSS Vulnerabilities** - Unsanitized output
4. **Race Conditions** - Unprotected shared state
5. **Memory Leaks** - Unclosed resources
6. **N+1 Queries** - Loop database calls
7. **Dead Code** - Unreachable branches
8. **God Objects** - Classes doing too much
9. **Copy-Paste Code** - Duplicated logic
10. **Missing Error Handling** - Unhandled exceptions

---

## Example Review Session

```
User: Review this PR for my authentication module

Claude: I'll perform a comprehensive multi-dimensional review.

[Launches parallel agents for security, maintainability, correctness]

## PR Review: Authentication Module

### Critical Issues (1)
1. **[auth.py:67]** Password stored in plaintext
   - Severity: Critical
   - Consensus: 3/3 models agree
   - Fix: Use bcrypt hashing
   ```python
   # Before
   user.password = request.password

   # After
   import bcrypt
   user.password = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt())
   ```

### High Issues (2)
1. **[auth.py:45]** No rate limiting on login endpoint
2. **[auth.py:89]** JWT secret hardcoded

### Quality Score: 58/100 (Grade: F)
- Security: 35/100 (Critical issues)
- Performance: 70/100
- Maintainability: 65/100
- Correctness: 60/100
- Style: 80/100

### Recommendation: BLOCK MERGE
Resolve critical security issues before merging.
```

---

## Related Skills

- **multi-ai-testing**: Generate tests for reviewed code
- **multi-ai-verification**: Validate fixes
- **multi-ai-implementation**: Implement suggested fixes
- **codex-review**: Codex-specific review patterns
- **review-multi**: Skill-specific reviews

---

## References

- `references/security-checklist.md` - OWASP Top 10 checklist
- `references/performance-patterns.md` - Performance anti-patterns
- `references/ci-cd-integration.md` - Full CI/CD setup guide
