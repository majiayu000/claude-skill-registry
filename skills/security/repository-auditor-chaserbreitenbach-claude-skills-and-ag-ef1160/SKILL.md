---
name: repository-auditor
version: 1.0.0
description: |
  Comprehensive codebase analysis system that evaluates security vulnerabilities,
  code quality, architecture patterns, and operational readiness across any technology stack.
author: QuantQuiver AI R&D
license: MIT

category: tooling
tags:
  - security
  - code-review
  - audit
  - quality-assurance
  - static-analysis
  - vulnerability-detection

dependencies:
  skills: []
  python: ">=3.9"
  packages:
    - pyyaml
    - gitpython
  tools:
    - bash
    - code_execution
    - web_fetch

triggers:
  - "audit this repository"
  - "security scan"
  - "code quality review"
  - "assess production readiness"
  - "vulnerability assessment"
  - "remediation roadmap"
  - "repository analysis"
---

# Universal Repository Auditor

## Purpose

A comprehensive codebase analysis system that evaluates security vulnerabilities, code quality, architecture patterns, and operational readiness across any technology stack. This skill codifies audit best practices into a systematic, repeatable process that produces actionable findings with effort estimates.

**Problem Space:**
- Manual code reviews miss systemic issues
- Security vulnerabilities often discovered post-deployment
- No standardized scoring for "production readiness"
- Effort estimation for fixes is guesswork

**Solution Approach:**
- Multi-dimensional scoring (Security, Architecture, Quality, Operations)
- Pattern-based vulnerability detection
- Technology-agnostic analysis framework
- Automated roadmap generation

## When to Use

- Pre-deployment security review
- Onboarding to inherited codebase
- Quarterly security audits
- Due diligence for acquisitions
- CI/CD integration for continuous auditing
- When user asks "Is this code production ready?"
- When evaluating third-party code or dependencies

## When NOT to Use

- Simple syntax error debugging
- Runtime performance profiling (use profiling tools instead)
- Real-time monitoring (use APM tools)
- Single-file code review (overkill)

---

## Core Instructions

### Analysis Dimensions

| Dimension | Weight | Indicators |
|-----------|--------|------------|
| **Security** | 30% | Hardcoded secrets, missing auth, SQL injection vectors, dependency vulnerabilities |
| **Architecture** | 25% | Separation of concerns, coupling metrics, scalability patterns |
| **Code Quality** | 25% | Type coverage, test coverage, linting compliance, documentation |
| **Operations** | 20% | CI/CD presence, containerization, logging, monitoring hooks |

### Standard Audit Procedure

1. **Ingestion Phase**
   - Clone or access repository
   - Identify primary branch
   - Enumerate all files (respecting .gitignore)
   - Parse dependency manifests

2. **Discovery Phase**
   - Detect technology stack(s)
   - Identify framework patterns
   - Map directory structure
   - Catalog entry points

3. **Analysis Phase**
   - Run security pattern detection
   - Evaluate architecture patterns
   - Assess code quality metrics
   - Check operational readiness

4. **Scoring Phase**
   - Calculate dimension scores (0-100)
   - Apply severity-weighted penalties
   - Compute overall score

5. **Synthesis Phase**
   - Generate prioritized issue list
   - Create remediation roadmap
   - Estimate effort ranges

### Detection Patterns

```yaml
security_patterns:
  hardcoded_credentials:
    - regex: '(password|secret|api_key|token)\s*=\s*["\'][^"\']+["\']'
    - exclude: ['*.example', '*.template', 'test_*']
    - severity: CRITICAL

  missing_input_validation:
    - pattern: 'request\.(body|query|params)\[.*\]'
    - without: ['validate', 'sanitize', 'escape']
    - severity: HIGH

  sql_injection:
    - pattern: 'f".*SELECT.*{.*}"'
    - severity: CRITICAL

architecture_patterns:
  circular_dependencies:
    - tool: 'madge --circular'
    - severity: MEDIUM

  god_class:
    - metric: 'lines_per_file > 1000'
    - severity: LOW

quality_patterns:
  missing_types:
    - python: 'mypy --strict'
    - typescript: 'tsc --noEmit'
    - threshold: 80%

  test_coverage:
    - tool: 'coverage report'
    - threshold: 60%

operations_patterns:
  no_cicd:
    - missing: ['.github/workflows', '.gitlab-ci.yml', 'Jenkinsfile']
    - severity: HIGH

  no_containerization:
    - missing: ['Dockerfile', 'docker-compose.yml']
    - severity: MEDIUM
```

### Scoring Algorithm

```
Score = 100 - Σ(severity_weight × issue_count)

Severity Weights:
- CRITICAL: 15 points
- HIGH: 8 points
- MEDIUM: 3 points
- LOW: 1 point
- INFO: 0 points

Dimension Weights:
- Security: 30%
- Architecture: 25%
- Quality: 25%
- Operations: 20%

Overall = Σ(dimension_score × dimension_weight)
```

### Decision Framework

**When to Flag CRITICAL:**
- Any hardcoded secrets or credentials
- SQL injection vectors
- Command injection possibilities
- Authentication bypass potential
- Known CVEs in dependencies (CVSS ≥ 9.0)

**When to Flag HIGH:**
- Missing input validation on user data
- Insecure deserialization
- Missing rate limiting on public endpoints
- Dependencies with CVEs (CVSS ≥ 7.0)
- No CI/CD pipeline

**When to Flag MEDIUM:**
- Missing type annotations (>20% untyped)
- Test coverage below threshold
- No containerization
- Circular dependencies
- Missing error handling

**When to Flag LOW:**
- Code style violations
- Missing documentation
- Unused imports/variables
- Overly complex functions (cyclomatic complexity > 10)

---

## Templates

### Audit Report Template

```markdown
# Repository Audit Report

**Repository**: [name]
**Branch**: [branch]
**Commit**: [sha]
**Audit Date**: [timestamp]
**Auditor Version**: 1.0.0

---

## Executive Summary

| Dimension | Score | Grade |
|-----------|-------|-------|
| **Overall** | [score]/100 | [A-F] |
| Security | [score]/100 | [A-F] |
| Architecture | [score]/100 | [A-F] |
| Code Quality | [score]/100 | [A-F] |
| Operations | [score]/100 | [A-F] |

### Issue Summary

| Severity | Count |
|----------|-------|
| CRITICAL | [n] |
| HIGH | [n] |
| MEDIUM | [n] |
| LOW | [n] |
| INFO | [n] |

---

## Findings

### CRITICAL Issues

#### [ISSUE-001] [Title]

**Category**: Security
**File**: `path/to/file.py:42`
**Evidence**:
```python
[code snippet showing vulnerability]
```

**Remediation**: [specific fix instructions]
**Effort**: [X-Y hours]
**References**: [links to documentation]

---

## Remediation Roadmap

### Phase 1: Critical Security (P0) - [X-Y hours]
- [ ] ISSUE-001: [description]
- [ ] ISSUE-002: [description]

### Phase 2: High Priority (P1) - [X-Y hours]
- [ ] ISSUE-003: [description]

### Phase 3: Medium Priority (P2) - [X-Y hours]
...

---

## Appendix

### Technology Stack Detected
- Primary Language: [language]
- Framework: [framework]
- Database: [if detected]
- Dependencies: [count]

### Files Analyzed
- Total Files: [n]
- Lines of Code: [n]
- Test Files: [n]
```

**Usage**: Generate this report after completing all analysis phases.

---

## Examples

### Example 1: Python Web Application Audit

**Input**: "Audit this Flask repository for security issues"

**Execution**:
1. Clone repository
2. Detect stack: Python (Flask)
3. Run security patterns:
   - Check for hardcoded secrets in config files
   - Scan for SQL injection in database queries
   - Verify input validation on routes
4. Run quality patterns:
   - Check for type hints
   - Measure test coverage
5. Check operations:
   - Look for Dockerfile
   - Check for CI/CD workflows

**Output**:
```
## Executive Summary

| Dimension | Score | Grade |
|-----------|-------|-------|
| **Overall** | 62/100 | D |
| Security | 45/100 | F |
| Architecture | 72/100 | C |
| Code Quality | 68/100 | D |
| Operations | 75/100 | C |

### Critical Findings

1. **CRITICAL: Hardcoded Database Password**
   - File: `config.py:15`
   - Remediation: Use environment variables

2. **CRITICAL: SQL Injection in User Query**
   - File: `routes/users.py:42`
   - Remediation: Use parameterized queries
```

**Explanation**: The audit identified critical security issues that require immediate attention before deployment.

### Example 2: Node.js Microservice

**Input**: "Review this TypeScript API for production readiness"

**Output Summary**:
- Overall Score: 78/100 (C+)
- Key Finding: Missing rate limiting on public endpoints
- Recommendation: Add express-rate-limit middleware

---

## Validation Checklist

Before completing any audit, verify:

- [ ] All file types in repository were scanned
- [ ] Dependency manifests were analyzed (package.json, requirements.txt, etc.)
- [ ] .env.example checked for sensitive defaults
- [ ] Git history not searched (respects privacy)
- [ ] All CRITICAL issues have specific remediation steps
- [ ] Effort estimates provided for all actionable items
- [ ] Report uses consistent severity classifications
- [ ] No false positives in CRITICAL/HIGH findings (verified manually)

---

## Related Resources

- [OWASP Top 10](https://owasp.org/Top10/)
- [CWE/SANS Top 25](https://cwe.mitre.org/top25/)
- Skill: `cicd-pipeline-generator` - Generate pipelines with security scanning
- Skill: `system-hardening-toolkit` - Server-side security configuration

---

## Changelog

### 1.0.0 (January 2026)
- Initial release
- Support for Python, Node.js, Go, Rust detection
- Four-dimension scoring system
- Automated roadmap generation
