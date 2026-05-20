---
# VERSION: 2.88.1
name: security
description: "Security audit with Codex + MiniMax second opinion. Uses LSP for code navigation during analysis. Use when: (1) /security is invoked, (2) task relates to security functionality."
user-invocable: true
context: fork
allowed-tools:
  - LSP
  - Read
  - Bash
  - Grep
  - Glob
hooks:
  PreToolUse:
    - path: .claude/hooks/validate-lsp-servers.sh
      match_tool: LSP
---

# /security - Multi-Agent Security Audit (v2.24)

Comprehensive security audit using Codex GPT-5 for primary analysis and MiniMax for second opinion validation.

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Works with the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

## Agent Teams Integration (v2.88)

**Optimal Scenario**: Integrated (Agent Teams + Custom Subagents)

This skill uses the INTEGRATED approach combining Agent Teams coordination with Custom Subagent specialization.

### Why Scenario C for This Skill
- **Parallel security scanning** requires coordinated multi-agent analysis across different vulnerability types
- **Quality gates (TeammateIdle, TaskCompleted)** ensure all security findings are properly addressed
- **Specialized ralph-reviewer agents** for vulnerability detection, ralph-coder for remediation
- **Shared task list** tracks findings and fix assignments
- **Multi-phase workflow** (scan -> prioritize -> fix -> verify) benefits from team coordination

### Configuration
1. **TeamCreate**: Create team "security-audit-${TARGET}" on security invocation
2. **TaskCreate**: Create tasks for analysis, prioritization, and remediation phases
3. **Spawn**: Use ralph-reviewer for scanning, ralph-coder for fixes
4. **Hooks**: TeammateIdle + TaskCompleted for security validation
5. **Coordination**: Shared task list at ~/.claude/tasks/{team}/

### Workflow Pattern
```
TeamCreate(team_name, description)
  → TaskCreate(scan_task, "Security vulnerability analysis")
  → Task(subagent_type="ralph-reviewer", team_name) for parallel scanning
  → TaskCreate(fix_task, "Apply security fixes")
  → Task(subagent_type="ralph-coder", team_name) for remediation
  → TaskUpdate(status="completed") as findings are resolved
  → Hooks validate security standards
  → VERIFIED_DONE when all critical/high findings fixed
```

### Automatic Team Creation

When `/security` is invoked on a directory with multiple files, it automatically:

```bash
# 1. Create security audit team
TeamCreate(team_name="security-audit-${TARGET}", description="Security analysis and fixes")

# 2. Spawn specialized teammates
Task(subagent_type="ralph-reviewer", team_name="security-audit-${TARGET}")  # Analyze vulnerabilities
Task(subagent_type="ralph-coder", team_name="security-audit-${TARGET}")     # Apply security fixes
```

### Teammate Roles

| Agent | Role | Model | Tasks |
|-------|------|-------|-------|
| `ralph-reviewer` | Security analysis, vulnerability detection | Model from settings | - CWE vulnerability scan<br>- OWASP Top 10 check<br>- Input validation review<br>- Remediation guidance |
| `ralph-coder` | Security fix implementation | Model from settings | - Apply security patches<br>- Add validation<br>- Implement secure patterns<br>- Add security tests |
| `team-lead` | Coordination | Opus | - Assign tasks<br>- Aggregate findings<br>- Validate remediation |

### Coordination via Shared Task List

```yaml
# Team lead creates coordinated tasks
TaskCreate:
  subject: "Analyze ${TARGET} for security vulnerabilities"
  description: |
    ralph-reviewer: Perform security audit on assigned files
    Focus on:
    - CWE vulnerabilities (prioritize High/Critical)
    - OWASP Top 10 risks
    - Input validation issues
    - Authentication/authorization flaws
    - SQL/Command/XSS injection vectors

    Output format per file:
    {
      "findings": [
        {
          "severity": "CRITICAL|HIGH|MEDIUM|LOW",
          "cwe": "CWE-XXX",
          "owasp": "A01:2021-Broken Access Control",
          "title": "Brief description",
          "file": "path/to/file.ext",
          "line": 42,
          "code": "vulnerable code snippet",
          "description": "Detailed explanation",
          "remediation": "How to fix",
          "references": ["URL1", "URL2"]
        }
      ]
    }

TaskCreate:
  subject: "Fix CRITICAL/HIGH security findings in ${TARGET}"
  description: |
    ralph-coder: Implement security fixes
    - Read findings from ralph-reviewer
    - Apply remediation steps
    - Add input validation
    - Implement secure patterns
    - Add security tests
    - Run quality gates after each fix
```

### Quality Gates Integration

Agent Teams hooks automatically validate security fixes:

```bash
# Hooks run automatically (configured in ~/.claude/settings.json)
TeammateIdle  → teammate-idle-quality-gate.sh    # Before going idle
TaskCompleted → task-completed-quality-gate.sh   # Before marking complete

# Security-specific quality checks:
# 1. No hardcoded secrets
# 2. Proper input validation
# 3. No console.log with sensitive data
# 4. All CRITICAL/HIGH findings fixed
```

### Parallel Security Scanning Workflow

```
┌─────────────────────────────────────────────────────────┐
│ AGENT TEAMS: Security Audit Parallel Scan               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│ 1. TEAM CREATE   → TeamCreate("security-audit-${TARGET}")│
│                                                         │
│ 2. PARALLEL SCAN → ralph-reviewer x N (file chunks)     │
│    ├─ Reviewer 1: auth files                            │
│    ├─ Reviewer 2: API endpoints                         │
│    └─ Reviewer 3: data handling                         │
│                                                         │
│ 3. AGGREGATE    → Team lead consolidates findings       │
│                                                         │
│ 4. PRIORITIZE   → Sort by severity (CRITICAL first)     │
│                                                         │
│ 5. PARALLEL FIX → ralph-coder x N (vulnerability assignments)│
│    ├─ Coder 1: CRITICAL injections                     │
│    ├─ Coder 2: HIGH auth flaws                         │
│    └─ Coder 3: MEDIUM validation issues                │
│                                                         │
│ 6. QUALITY GATE → Hooks validate all security fixes     │
│                                                         │
│ 7. VERIFY      → Re-scan until all findings resolved   │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

### Example Team-Based Security Audit

```bash
# User invokes /security on large codebase
ralph security src/

# Behind the scenes:
# 1. Team created: "security-audit-src"
# 2. Files split among 3 ralph-reviewer agents by module
# 3. Each reviewer performs security audit in parallel
# 4. Team lead aggregates findings, removes duplicates
# 5. CRITICAL/HIGH findings assigned to ralph-coder agents
# 6. Quality gates run automatically after each fix
# 7. Final verification scan confirms all vulnerabilities resolved

# Time savings: 3x faster than sequential audit
# Coverage: Parallel agents catch different vulnerability types
```

### Multi-Model Second Opinion (Optional)

For critical security audits, combine Agent Teams with multi-model validation:

```bash
# Primary audit: ralph-reviewer (model from settings)
# Second opinion: Additional reviewer with different model
Task(subagent_type="ralph-reviewer", model="opus", team_name="security-audit-${TARGET}")
```

## Overview

The `/security` command performs a thorough security audit of your codebase, checking for:
- CWE (Common Weakness Enumeration) vulnerabilities
- OWASP Top 10 security risks
- Input validation and sanitization issues
- Authentication and authorization flaws
- Cryptographic weaknesses
- Injection vulnerabilities (SQL, Command, XSS, etc.)
- Path traversal and file handling risks
- Race conditions and TOCTOU bugs
- Insecure defaults and misconfigurations

Results are returned in structured JSON format with severity ratings, CWE references, and remediation guidance.

## When to Use

Trigger `/security` when:
- Adding new features that handle user input
- Before merging security-critical changes
- After dependency updates that may introduce vulnerabilities
- Implementing authentication or authorization logic
- Working with file operations, shell commands, or network requests
- Preparing for production deployment
- Conducting periodic security reviews

## Workflow

```
┌────────────────────────────────────────────────────────┐
│                  Security Audit Flow                   │
├────────────────────────────────────────────────────────┤
│                                                        │
│  1. CODEX PRIMARY AUDIT                                │
│     ├─ CWE vulnerability scan                          │
│     ├─ OWASP Top 10 check                              │
│     ├─ Input validation review                         │
│     ├─ Authentication/authorization audit              │
│     └─ Generate findings (JSON)                        │
│                                                        │
│  2. MINIMAX SECOND OPINION                             │
│     ├─ Independent vulnerability review                │
│     ├─ Cross-validate Codex findings                   │
│     ├─ Catch additional issues                         │
│     └─ Consensus report                                │
│                                                        │
│  3. QUALITY GATES INTEGRATION                          │
│     └─ Findings feed into ralph gates                  │
│                                                        │
│  4. STRUCTURED REPORT                                  │
│     ├─ Severity: CRITICAL/HIGH/MEDIUM/LOW              │
│     ├─ CWE references                                  │
│     ├─ OWASP categories                                │
│     ├─ Code snippets                                   │
│     └─ Remediation steps                               │
│                                                        │
└────────────────────────────────────────────────────────┘
```

## CLI Execution

```bash
# Audit entire project
ralph security .

# Audit specific directory
ralph security src/

# Audit single file
ralph security src/auth/login.ts

# Audit with verbose output
ralph security src/ --verbose

# Audit and save JSON report
ralph security src/ --output security-report.json
```

## Task Tool Invocation

### Primary Security Audit (Codex GPT-5)

```yaml
Task:
  subagent_type: "security-auditor"
  model: "sonnet"  # Sonnet manages the Codex CLI call
  run_in_background: true
  description: "Codex: Primary security audit"
  prompt: |
    Execute via Codex CLI for security analysis:
    cd /absolute/path/to/project && codex exec -m gpt-5.2-codex "
    Perform comprehensive security audit on: <path>

    Check for:
    1. CWE vulnerabilities (prioritize High/Critical)
    2. OWASP Top 10 risks
    3. Input validation issues
    4. Authentication/authorization flaws
    5. SQL/Command/XSS injection vectors
    6. Path traversal (CWE-22, CWE-59)
    7. Command injection (CWE-78)
    8. Insecure crypto (CWE-327, CWE-338)
    9. Race conditions (CWE-362, CWE-367)
    10. Information disclosure (CWE-200, CWE-209)

    Output format: JSON with structure:
    {
      'findings': [
        {
          'severity': 'CRITICAL|HIGH|MEDIUM|LOW',
          'cwe': 'CWE-XXX',
          'owasp': 'A01:2021-Broken Access Control',
          'title': 'Brief description',
          'file': 'path/to/file.ext',
          'line': 42,
          'code': 'vulnerable code snippet',
          'description': 'Detailed explanation',
          'remediation': 'How to fix',
          'references': ['URL1', 'URL2']
        }
      ],
      'summary': {
        'total': 10,
        'critical': 2,
        'high': 3,
        'medium': 4,
        'low': 1
      }
    }
    "

    Apply Ralph Loop: iterate until audit complete and all findings validated.
```

### Secondary Validation (MiniMax Second Opinion)

```yaml
Task:
  subagent_type: "minimax-reviewer"
  model: "sonnet"  # Sonnet manages the mmc CLI call
  run_in_background: true
  description: "MiniMax: Security second opinion"
  prompt: |
    Execute via MiniMax CLI for independent security validation:
    mmc --query "
    Perform independent security review on: <path>

    Focus on vulnerabilities Codex might have missed:
    1. Subtle logic flaws in authentication
    2. Business logic vulnerabilities
    3. Race conditions in concurrent code
    4. Insecure defaults and misconfigurations
    5. Complex injection chains

    Cross-validate Codex findings and identify additional issues.
    Use same JSON format as Codex for consistency.
    "

    MiniMax provides Opus-level quality at 8% cost for second opinion.
```

## Output Format

### JSON Structure

```json
{
  "findings": [
    {
      "severity": "CRITICAL",
      "cwe": "CWE-78",
      "owasp": "A03:2021-Injection",
      "title": "Command Injection in file upload handler",
      "file": "src/upload/handler.ts",
      "line": 145,
      "code": "execSync(`convert ${filename} output.png`)",
      "description": "User-supplied filename passed to shell without sanitization",
      "remediation": "Use execFile with array arguments instead of shell interpolation. Import execFileNoThrow from utils.",
      "references": [
        "https://cwe.mitre.org/data/definitions/78.html",
        "https://owasp.org/Top10/A03_2021-Injection/"
      ]
    },
    {
      "severity": "HIGH",
      "cwe": "CWE-22",
      "owasp": "A01:2021-Broken Access Control",
      "title": "Path Traversal in file download",
      "file": "src/api/download.ts",
      "line": 67,
      "code": "readFile(path.join('/uploads', req.query.file))",
      "description": "User-controlled file parameter allows access to arbitrary files via '../' sequences",
      "remediation": "Validate path is within allowed directory using realpath and startsWith check",
      "references": [
        "https://cwe.mitre.org/data/definitions/22.html"
      ]
    }
  ],
  "summary": {
    "total": 2,
    "critical": 1,
    "high": 1,
    "medium": 0,
    "low": 0,
    "files_scanned": 45,
    "scan_duration": "12.3s",
    "tools": ["codex-gpt5", "minimax-m2.1"]
  }
}
```

### Markdown Report

```markdown
# Security Audit Report

**Date:** 2025-01-04
**Target:** src/
**Tools:** Codex GPT-5 + MiniMax M2.1

## Summary

- **Total Findings:** 2
- **Critical:** 1
- **High:** 1
- **Medium:** 0
- **Low:** 0

## Findings

### [CRITICAL] Command Injection in file upload handler

**CWE:** CWE-78
**OWASP:** A03:2021-Injection
**File:** src/upload/handler.ts:145

**Vulnerable Code:**
```typescript
// UNSAFE - allows command injection
execSync(`convert ${filename} output.png`)
```

**Description:** User-supplied filename passed to shell without sanitization, allowing arbitrary command execution.

**Remediation:** Use execFile with array arguments:
```typescript
// SAFE - no shell interpolation
import { execFileNoThrow } from '../utils/execFileNoThrow.js'
await execFileNoThrow('convert', [filename, 'output.png'])
```

**References:**
- https://cwe.mitre.org/data/definitions/78.html
- https://owasp.org/Top10/A03_2021-Injection/
```

## Security Considerations

### For the Security Command Itself

1. **Safe Code Analysis** - The security audit reads code but never executes it
2. **Sensitive Data Handling** - Reports may contain code snippets with secrets; handle with care
3. **False Positives** - Manual review required; automated tools may flag benign patterns
4. **Scope Limitation** - Static analysis only; cannot detect runtime vulnerabilities
5. **Tool Trust** - Codex and MiniMax are third-party services; do not send proprietary code if restricted

### CWE Categories Checked

| Category | CWEs | Description |
|----------|------|-------------|
| **Injection** | CWE-78, CWE-89, CWE-79 | Command, SQL, XSS injection |
| **Path Traversal** | CWE-22, CWE-59 | File access outside allowed directories |
| **Input Validation** | CWE-20, CWE-116 | Improper input sanitization |
| **Authentication** | CWE-287, CWE-307 | Broken authentication, brute force |
| **Authorization** | CWE-284, CWE-862 | Missing access controls |
| **Cryptography** | CWE-327, CWE-338 | Weak crypto, insecure RNG |
| **Race Conditions** | CWE-362, CWE-367 | TOCTOU, concurrent access |
| **Information Disclosure** | CWE-200, CWE-209 | Leaking sensitive data |
| **Resource Management** | CWE-400, CWE-770 | DoS, resource exhaustion |

### OWASP Top 10 Mapping

| OWASP Category | CWE Examples | Priority |
|----------------|--------------|----------|
| A01:2021-Broken Access Control | CWE-22, CWE-862 | High |
| A02:2021-Cryptographic Failures | CWE-327, CWE-338 | High |
| A03:2021-Injection | CWE-78, CWE-89, CWE-79 | Critical |
| A04:2021-Insecure Design | CWE-840 | Medium |
| A05:2021-Security Misconfiguration | CWE-16 | Medium |
| A06:2021-Vulnerable Components | CVE references | High |
| A07:2021-Authentication Failures | CWE-287, CWE-307 | Critical |
| A08:2021-Data Integrity Failures | CWE-502 | High |
| A09:2021-Logging Failures | CWE-778 | Low |
| A10:2021-SSRF | CWE-918 | Medium |

## Integration with Quality Gates

The security audit integrates with `ralph gates`:

```bash
# Run security audit as part of quality gates
ralph gates

# Quality gates automatically include:
# 1. Language-specific linting (9 languages)
# 2. Security audit (if security-critical files changed)
# 3. Test coverage validation
# 4. Git safety checks
```

**Gate Failure Criteria:**
- Any CRITICAL severity finding → BLOCK merge
- 2+ HIGH severity findings → BLOCK merge
- MEDIUM findings → Warning (review required)
- LOW findings → Info only

## Related Commands

| Command | Purpose | Use Case |
|---------|---------|----------|
| `/security` | Full security audit | Pre-merge security review |
| `/adversarial` | Adversarial spec refinement | Critical features (complexity >= 7) |
| `/bugs` | Bug hunting | Functional issues, not security |
| `/security-loop` | Iterative security fixes | Apply fixes until audit passes |
| `/code-review` | General code review | Quality, not security-focused |
| `ralph gates` | Quality gates | Pre-commit validation |

## Examples

### Example 1: Pre-Merge Security Review

```bash
# Scenario: About to merge authentication feature
ralph security src/auth/

# Output: JSON report with 3 findings
# - CRITICAL: Hardcoded JWT secret (CWE-798)
# - HIGH: Missing rate limiting (CWE-307)
# - MEDIUM: Weak password requirements (CWE-521)
```

### Example 2: Dependency Update Review

```bash
# Scenario: Updated Express from 4.17 to 4.18
ralph security src/api/

# Output: No new vulnerabilities introduced
# - Validates middleware security
# - Checks request parsing
# - Reviews error handling
```

### Example 3: File Upload Security

```bash
# Scenario: Implementing file upload feature
ralph security src/upload/

# Output: 2 CRITICAL findings
# - Command injection in filename handling (CWE-78)
# - Path traversal in storage location (CWE-22)
```

### Example 4: Task Tool Invocation with Second Opinion

```yaml
# Primary audit
Task:
  subagent_type: "security-auditor"
  model: "sonnet"
  run_in_background: true
  description: "Codex: Security audit of auth module"
  prompt: |
    codex exec -m gpt-5.2-codex "
    Security audit: src/auth/
    Focus on authentication bypasses, session hijacking, and credential storage.
    JSON output with CWE/OWASP references.
    "

# Second opinion
Task:
  subagent_type: "minimax-reviewer"
  model: "sonnet"
  run_in_background: true
  description: "MiniMax: Validate Codex findings"
  prompt: |
    mmc --query "
    Independent security review: src/auth/
    Cross-validate Codex findings and find missed issues.
    Same JSON format.
    "
```

### Example 5: Integration with Worktree Workflow

```bash
# Create isolated worktree for security fixes
ralph worktree "fix-security-findings"

# Run security audit in worktree
cd ~/worktrees/fix-security-findings
ralph security src/

# Fix findings, then PR review with multi-agent validation
ralph worktree-pr fix-security-findings
```

## Anti-Patterns

- **Don't skip security audits for "quick fixes"** - Small changes can introduce big vulnerabilities
- **Don't ignore LOW severity findings** - Multiple LOW can combine to HIGH impact
- **Don't trust static analysis alone** - Manual review + penetration testing required
- **Don't audit third-party code** - Focus on your code; use dependency scanners for libraries
- **Don't send proprietary code to external services** - Check company policies first

## Advanced Usage

### Custom Security Rules

```bash
# Audit with custom CWE focus
ralph security src/ --cwe CWE-78,CWE-89,CWE-79

# Audit with severity threshold
ralph security src/ --min-severity HIGH

# Audit with specific OWASP category
ralph security src/ --owasp A03:2021-Injection
```

### Continuous Security Monitoring

```bash
# Add to CI/CD pipeline
name: Security Audit
on: [push, pull_request]
jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: ralph security . --output security-report.json
      - run: |
          if jq -e '.summary.critical > 0 or .summary.high > 1' security-report.json; then
            echo "Security audit failed"
            exit 1
          fi
```

### Security Loop Pattern

```bash
# Iterate until all findings resolved
ralph loop --security "Fix security findings in src/auth/"

# The loop will:
# 1. Run security audit
# 2. Apply fixes
# 3. Re-audit
# 4. Repeat until clean (max 15 iterations)
```


## Action Reporting (v2.93.0)

**Esta skill genera reportes automáticos completos** para trazabilidad:

### Reporte Automático

Cuando esta skill completa, se genera automáticamente:

1. **En la conversación de Claude**: Resultados visibles
2. **En el repositorio**: `docs/actions/security/{timestamp}.md`
3. **Metadatos JSON**: `.claude/metadata/actions/security/{timestamp}.json`

### Contenido del Reporte

Cada reporte incluye:
- ✅ **Summary**: Descripción de la tarea ejecutada
- ✅ **Execution Details**: Duración, iteraciones, archivos modificados
- ✅ **Results**: Errores encontrados, recomendaciones
- ✅ **Next Steps**: Próximas acciones sugeridas

### Ver Reportes Anteriores

```bash
# Listar todos los reportes de esta skill
ls -lt docs/actions/security/

# Ver el reporte más reciente
cat $(ls -t docs/actions/security/*.md | head -1)

# Buscar reportes fallidos
grep -l "Status: FAILED" docs/actions/security/*.md
```

### Generación Manual (Opcional)

```bash
source .claude/lib/action-report-lib.sh
start_action_report "security" "Task description"
# ... ejecución ...
complete_action_report "success" "Summary" "Recommendations"
```

### Referencias del Sistema

- [Action Reports System](docs/actions/README.md) - Documentación completa
- [action-report-lib.sh](.claude/lib/action-report-lib.sh) - Librería helper
- [action-report-generator.sh](.claude/lib/action-report-generator.sh) - Generador
