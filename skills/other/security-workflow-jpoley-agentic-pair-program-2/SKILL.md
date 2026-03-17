---
name: security-workflow
description: Use when creating backlog tasks from security findings, integrating security scans into workflow states, or managing security remediation tracking. Invoked for security workflow integration and task automation.
---

# Security Workflow Integration Skill

You are an expert at integrating security assessment findings into development workflows and backlog management systems. You excel at translating security vulnerabilities into actionable development tasks with clear acceptance criteria and appropriate prioritization.

## When to Use This Skill

- Creating backlog tasks from security scan findings
- Integrating security into workflow states
- Managing security remediation tracking
- Automating security task creation with --create-tasks flag
- Mapping vulnerabilities to development work items
- Prioritizing security fixes in backlog

## Core Responsibilities

1. **Task Creation** - Convert security findings into well-formed backlog tasks
2. **Prioritization** - Map severity levels to task priorities
3. **AC Generation** - Create verifiable acceptance criteria for security fixes
4. **Metadata Management** - Apply appropriate labels, assignments, and tracking
5. **Workflow Integration** - Ensure security fits into existing development workflow

## Backlog Task Format for Security Findings

### Task Title Convention

```
Security: [Vulnerability Type] in [Component]
```

**Examples:**
- `Security: SQL Injection in login endpoint`
- `Security: XSS vulnerability in admin panel`
- `Security: Outdated dependency (lodash) with known CVEs`
- `Security: Missing authentication on API endpoint`

### Task Description Format

```markdown
## Security Finding

**Vulnerability ID:** [VULN-XXX]
**Severity:** [Critical|High|Medium|Low]
**CVSS Score:** [X.X]
**CWE:** [CWE-XXX: Description]
**OWASP:** [A0X: Category]

## Description

[Technical description of the vulnerability]

## Location

- File: `[path/to/file.ext:line]`
- Component: [component name]
- Function: [function/method name]

## Impact

[What could an attacker do with this vulnerability?]

## Remediation Steps

[Specific steps to fix the vulnerability]

## References

- [CWE-XXX](https://cwe.mitre.org/data/definitions/XXX.html)
- [CVE-YYYY-XXXX](https://nvd.nist.gov/vuln/detail/CVE-YYYY-XXXX) (if applicable)

---

**Created by:** `/flow:security --create-tasks`
**Audit Report:** `docs/security/audit-report.md`
```

### Acceptance Criteria Mapping

Map remediation steps to acceptance criteria:

**Example Finding:**
```
Remediation:
1. Replace string concatenation with parameterized queries
2. Add input validation for user_id parameter
3. Add security test to verify fix
```

**Resulting ACs:**
```bash
--ac "Parameterized queries implemented for all SQL statements"
--ac "Input validation added for user_id with integer type checking"
--ac "Security test added to verify SQL injection is prevented"
--ac "Code review completed by security-reviewer"
```

### Priority Mapping

Map security severity to backlog priority:

| Security Severity | Backlog Priority | Rationale |
|-------------------|------------------|-----------|
| Critical | critical | Remote code execution, auth bypass - immediate fix required |
| High | high | Data exposure, privilege escalation - fix within 7 days |
| Medium | medium | Info disclosure, weak crypto - fix within 30 days |
| Low | low | Config issues, best practices - fix within 90 days |
| Info | low | No security impact - informational only |

### Label Strategy

Apply multiple labels for filtering and tracking:

**Required Labels:**
- `security` - All security-related tasks
- Severity: `critical`, `high`, `medium`, or `low`

**Optional Context Labels:**
- `backend` / `frontend` / `infra` - Component type
- `dependency` - Dependency vulnerability
- `auth` - Authentication/authorization issue
- `injection` - SQL/Command/XSS injection
- `crypto` - Cryptographic failure
- `compliance` - Compliance requirement

**Example:**
```bash
-l security,critical,backend,injection
```

### Assignment Strategy

Map vulnerability types to appropriate engineers:

| Vulnerability Type | Suggested Assignee |
|--------------------|-------------------|
| Backend vulnerabilities (SQL injection, auth) | `@backend-engineer` |
| Frontend vulnerabilities (XSS, CSRF) | `@frontend-engineer` |
| Infrastructure issues (TLS, network) | `@platform-engineer` |
| Dependency vulnerabilities | `@backend-engineer` or `@frontend-engineer` |
| Design issues | `@software-architect` |

## Task Creation Commands

### Single Finding

```bash
backlog task create "Security: SQL Injection in login endpoint" \
  -d "$(cat <<'EOF'
## Security Finding

**Vulnerability ID:** VULN-001
**Severity:** Critical
**CVSS Score:** 9.8
**CWE:** CWE-89: SQL Injection
**OWASP:** A03: Injection

## Description

The login endpoint uses string concatenation to build SQL queries, allowing attackers to inject arbitrary SQL code.

## Location

- File: `src/auth/login.py:45`
- Component: Authentication Service
- Function: `authenticate_user()`

## Impact

An attacker could bypass authentication, extract database contents, modify data, or execute arbitrary commands on the database server.

## Remediation Steps

1. Replace string concatenation with parameterized queries
2. Add input validation for username and password parameters
3. Implement prepared statements via SQLAlchemy
4. Add security test to verify SQL injection is prevented

## References

- [CWE-89](https://cwe.mitre.org/data/definitions/89.html)
- [OWASP A03](https://owasp.org/Top10/A03_2021-Injection/)

---

**Created by:** /flow:security --create-tasks
**Audit Report:** docs/security/audit-report.md
EOF
)" \
  --ac "Parameterized queries implemented using SQLAlchemy" \
  --ac "Input validation added for username and password" \
  --ac "Prepared statements used for all database queries" \
  --ac "Security test added to test suite" \
  --ac "Code review completed by @backend-code-reviewer" \
  -l security,critical,backend,injection \
  --priority critical \
  -a @backend-engineer
```

### Bulk Creation Script

For multiple findings, use a shell script:

```bash
#!/bin/bash
# Create backlog tasks for all critical/high findings
# Usage: ./create-security-tasks.sh docs/security/triage-results.json

TRIAGE_FILE="$1"

# Parse JSON and create tasks for critical/high findings
jq -r '.findings[] | select(.severity == "critical" or .severity == "high") |
  "backlog task create \"Security: \(.title)\" " +
  "-d \"\(.description)\" " +
  "--ac \"\(.remediation.steps[0])\" " +
  "--ac \"\(.remediation.steps[1])\" " +
  "--ac \"Security test added\" " +
  "--ac \"Code review completed\" " +
  "-l security,\(.severity),\(.component) " +
  "--priority \(.severity) " +
  "-a \(.suggested_assignee)"
' "$TRIAGE_FILE" | while read -r cmd; do
  eval "$cmd"
done
```

## Workflow State Integration Options

### Option 1: Dedicated Security State

Add a dedicated security verification state to `flowspec_workflow.yml`:

```yaml
states:
  - "To Do"
  - "Assessed"
  - "Specified"
  - "Researched"
  - "Planned"
  - "In Implementation"
  - "Security Review"      # NEW: Dedicated security state
  - "Validated"
  - "Deployed"
  - "Done"

workflows:
  security:
    command: "/flow:security"
    description: "Execute security scans and create remediation tasks"
    agents:
      - name: "secure-by-design-engineer"
        identity: "@secure-by-design-engineer"
        description: "Security specialist"
        responsibilities:
          - "Security scanning (SAST, SCA, secrets)"
          - "Vulnerability triage and prioritization"
          - "Security task creation in backlog"
    input_states: ["In Implementation"]
    output_state: "Security Review"
    optional: false
    creates_backlog_tasks: true

transitions:
  - name: "security_review"
    from: "In Implementation"
    to: "Security Review"
    via: "security"
    description: "Security scan completed, findings triaged"
    output_artifacts:
      - type: "security_scan_results"
        path: "./docs/security/scan-results.json"
        required: true
      - type: "security_triage"
        path: "./docs/security/triage-results.json"
        required: true
      - type: "backlog_tasks"
        path: "./backlog/tasks/*.md"
        multiple: true
    validation: "NONE"

  - name: "validate_after_security"
    from: "Security Review"
    to: "Validated"
    via: "validate"
    description: "QA validation after security fixes"
    validation: "NONE"
```

### Option 2: Extend Validate Workflow

Integrate security into the existing validate workflow:

```yaml
workflows:
  validate:
    command: "/flow:validate"
    description: "Execute validation using QA, security, and documentation agents"
    agents:
      - name: "quality-guardian"
        identity: "@quality-guardian"
        description: "Quality Guardian"
        responsibilities:
          - "Functional and integration testing"
          - "Performance testing"
      - name: "secure-by-design-engineer"
        identity: "@secure-by-design-engineer"
        description: "Secure-by-Design Engineer"
        responsibilities:
          - "Security scanning (SAST, SCA, secrets)"
          - "Vulnerability triage and assessment"
          - "Security task creation with --create-tasks"  # NEW
      - name: "tech-writer"
        identity: "@tech-writer"
        description: "Senior Technical Writer"
        responsibilities:
          - "API documentation and user guides"
    input_states: ["In Implementation"]
    output_state: "Validated"
    optional: false
    creates_backlog_tasks: true  # NEW: Security can create tasks
```

## Pre-Commit Hook Integration

### Hook Configuration

Create `.flowspec/hooks/hooks.yaml`:

```yaml
version: "1.0"

hooks:
  # Pre-commit security scanning
  pre-commit:
    - name: "security-scan-staged"
      description: "Scan staged files for security issues"
      script: "scripts/security/pre-commit-scan.sh"
      on_failure: "warn"  # or "block" to prevent commit

  # Post-scan task creation
  security-findings:
    - name: "create-security-tasks"
      description: "Create backlog tasks for findings"
      script: "scripts/security/create-tasks.sh"
      condition: "findings.critical > 0 or findings.high > 0"
```

### Pre-Commit Script

```bash
#!/bin/bash
# scripts/security/pre-commit-scan.sh
# Run security scan on staged files

set -e

echo "Running security scan on staged files..."

# Get staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
  echo "No staged files to scan"
  exit 0
fi

# Run security scan on staged files only
flowspec security scan --staged-only --output docs/security/pre-commit-scan.json

# Check for critical/high findings
CRITICAL_COUNT=$(jq '[.findings[] | select(.severity == "critical")] | length' docs/security/pre-commit-scan.json)
HIGH_COUNT=$(jq '[.findings[] | select(.severity == "high")] | length' docs/security/pre-commit-scan.json)

if [ "$CRITICAL_COUNT" -gt 0 ]; then
  echo "❌ Found $CRITICAL_COUNT critical security issues in staged files"
  echo "   Run 'flowspec security triage' to review findings"
  exit 1
fi

if [ "$HIGH_COUNT" -gt 0 ]; then
  echo "⚠️  Found $HIGH_COUNT high security issues in staged files"
  echo "   Consider fixing before committing"
  # Warn but don't block (change exit 0 to exit 1 to block)
  exit 0
fi

echo "✅ No critical security issues found in staged files"
exit 0
```

## CI/CD Integration

### GitHub Actions Example

```yaml
name: Security Scan

on:
  pull_request:
    branches: [main]
  push:
    branches: [main]

jobs:
  security-scan:
    runs-on: ubuntu-latest
    permissions:
      security-events: write  # For SARIF upload
      pull-requests: write     # For comments

    steps:
      - uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install uv
          uv sync
          uv tool install .

      - name: Run security scan
        run: |
          flowspec security scan --format sarif --output security-results.sarif

      - name: Upload SARIF to GitHub Security
        uses: github/codeql-action/upload-sarif@v3
        with:
          sarif_file: security-results.sarif

      - name: Triage findings
        run: |
          flowspec security triage --input security-results.sarif

      - name: Create backlog tasks for findings
        if: github.event_name == 'pull_request'
        run: |
          flowspec security report --create-tasks

      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs');
            const report = fs.readFileSync('docs/security/audit-report.md', 'utf8');

            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `## Security Scan Results\n\n${report}`
            });
```

### GitLab CI Example

```yaml
security-scan:
  stage: test
  image: python:3.11

  before_script:
    - pip install uv
    - uv sync
    - uv tool install .

  script:
    - flowspec security scan --format sarif --output gl-sast-report.json
    - flowspec security triage --input gl-sast-report.json
    - flowspec security report --create-tasks

  artifacts:
    reports:
      sast: gl-sast-report.json
    paths:
      - docs/security/

  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
    - if: '$CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH'
```

## SARIF Output for GitHub Security Tab

### SARIF Format

Security scans should output SARIF 2.1.0 format for GitHub Code Scanning integration:

```json
{
  "version": "2.1.0",
  "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "Flowspec Security Scanner",
          "version": "1.0.0",
          "informationUri": "https://github.com/jpoley/flowspec"
        }
      },
      "results": [
        {
          "ruleId": "CWE-89",
          "level": "error",
          "message": {
            "text": "SQL Injection vulnerability detected"
          },
          "locations": [
            {
              "physicalLocation": {
                "artifactLocation": {
                  "uri": "src/auth/login.py"
                },
                "region": {
                  "startLine": 45,
                  "startColumn": 10
                }
              }
            }
          ],
          "properties": {
            "severity": "critical",
            "cvss": 9.8,
            "cwe": "CWE-89",
            "owasp": "A03"
          }
        }
      ]
    }
  ]
}
```

## Best Practices

### Task Creation

1. **Be Specific** - Task titles should clearly identify the vulnerability type and location
2. **Include Context** - Description should have enough detail for the engineer to understand
3. **Actionable ACs** - Acceptance criteria must be verifiable (testable)
4. **Appropriate Priority** - Map severity to priority correctly
5. **Assign Correctly** - Route to the appropriate team/engineer

### Workflow Integration

1. **Choose the Right Pattern** - Dedicated state for security-focused teams, extend validate for integrated teams
2. **Automate When Possible** - Use --create-tasks flag to automate task creation
3. **Gate Appropriately** - Block critical/high vulnerabilities, warn on medium/low
4. **Track Progress** - Use backlog tasks to track remediation progress
5. **Close the Loop** - Re-scan after fixes to verify remediation

### CI/CD Integration

1. **Run on Every PR** - Catch issues before merge
2. **Upload SARIF** - Integrate with GitHub Security tab
3. **Comment on PRs** - Surface findings directly in code review
4. **Block on Critical** - Prevent merging code with critical vulnerabilities
5. **Track Metrics** - Monitor security posture over time

## Integration with Existing Skills

### Works With:

- **security-triage** - Receives triaged findings to convert to tasks
- **security-reporter** - Uses task creation for remediation tracking
- **pm-planner** - Coordinates with product planning for security priorities
- **qa-validator** - Validates security fixes are properly tested

## Quality Checklist

Before creating security tasks, verify:

- [ ] Vulnerability is real (not a false positive)
- [ ] Severity is accurately assessed
- [ ] Location information is correct and specific
- [ ] Remediation steps are actionable
- [ ] Acceptance criteria are verifiable
- [ ] Priority matches severity
- [ ] Appropriate assignee selected
- [ ] Labels applied correctly

## Common Pitfalls to Avoid

- **Creating Tasks for False Positives** - Always triage first
- **Vague Task Titles** - Be specific about what and where
- **Unclear Remediation** - Provide concrete steps, not just "fix it"
- **Wrong Priority** - Don't inflate or deflate severity
- **Missing Context** - Include enough information for the engineer
- **No Verification** - Always include a test AC
