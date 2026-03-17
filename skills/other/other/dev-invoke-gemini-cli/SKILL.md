---
name: dev_invoke_gemini-cli
description: |
  Delegate QAQC and review tasks to Google Gemini CLI using markdown file handoff pattern.
  Write review request to REVIEW.md, Gemini analyzes, outputs findings to FINDINGS.md.
  Use for code review, security audits, documentation review, large context analysis.

  Triggers: gemini, gemini cli, delegate to gemini, gemini subagent, code review,
  QAQC, quality check, security audit, documentation review, large context,
  second opinion, architecture review, gemini-3-pro-preview, gemini-3-flash-preview

  Prerequisites: Gemini CLI authenticated (gemini login or GEMINI_API_KEY)
  Models: gemini-3-pro-preview (default), gemini-3-flash-preview (large context)
---

# Invoking Gemini CLI

Delegate QAQC, code review, and analysis tasks to Gemini CLI using markdown files for input and output.

## Pattern: Markdown File Handoff

```
Claude Code                         Gemini CLI
    |                                   |
    +-- Write REVIEW.md ----------------+
    |   (code + review criteria)        |
    |                                   |
    +-- Execute: gemini -y "Read        |
    |   REVIEW.md, analyze, write       |
    |   findings to FINDINGS.md"        |
    |                                   |
    |                                   +-- Reads REVIEW.md
    |                                   +-- Analyzes content
    |                                   +-- Writes FINDINGS.md
    |                                   |
    +-- Read FINDINGS.md <--------------+
    |   (analysis + recommendations)    |
    v                                   v
```

**Benefits**:
- No shell escaping issues
- Full context in structured format
- Explicit output structure
- Session resume available

## When to Use

- **QAQC / Code review** - Second opinion on implementation
- **Architecture review** - Validate design decisions
- **Documentation review** - Check clarity and completeness
- **Security audit** - Identify vulnerabilities
- **Large context analysis** - 1M+ token context window

## Model Selection

| Model | Use Case | Status |
|-------|----------|--------|
| `gemini-3-pro-preview` | **Default.** Strong reasoning | CLI default |
| `gemini-3-flash-preview` | Large context, fast analysis | For big codebases |

**Recommendation**: Use default `gemini-3-pro-preview` for most tasks. Use `gemini-3-flash-preview` for very large context (>100K tokens) via `-m` flag.

**Note**: If you encounter 429 capacity errors with `gemini-3-pro-preview`, retry or wait briefly.

## Invocation

### Standard Pattern (Recommended)

```bash
cd /path/to/project && gemini -y "Read REVIEW.md in the current directory. Follow the review criteria. Write all findings to FINDINGS.md."
```

### With Explicit Model

```bash
cd /path/to/project && gemini -y -m gemini-3-flash-preview "Read REVIEW.md, analyze per criteria, write findings to FINDINGS.md"
```

### Resume Session

```bash
gemini -r <session_id> "Read REVIEW.md for updated criteria, append to FINDINGS.md"
```

## Core Flags Reference

| Flag | Purpose |
|------|---------|
| `-y` | YOLO mode - auto-approve all actions |
| `-m <model>` | Model: `gemini-3-pro-preview`, `gemini-3-flash-preview` |
| `-r <id>` | Resume session by ID |
| `--output-format json` | JSON output for parsing |
| `--list-sessions` | List available sessions |

## Review Request Template (REVIEW.md)

```markdown
# Review Request: [Brief Title]

## Objective
[What kind of review/analysis is needed]

## Review Criteria
Rate each finding: CRITICAL | HIGH | MEDIUM | LOW

### Security
- SQL injection vulnerabilities
- XSS risks
- Authentication/authorization issues
- Hardcoded secrets

### Reliability
- Error handling gaps
- Edge cases not covered
- Race conditions
- Resource leaks

### Performance
- N+1 query patterns
- Unnecessary allocations
- Missing caching opportunities

### Maintainability
- Code clarity
- Naming conventions
- Documentation gaps

## Code to Review

### File: src/api/users.ts
```typescript
// Paste code here or reference file
```

### File: src/services/auth.ts
```typescript
// Paste code here
```

## Context
[Any relevant background, constraints, or requirements]

## Output Format
Write to FINDINGS.md with:
- Summary of review
- Findings table with severity, location, description
- Specific recommendations
- Overall assessment
- Session ID for follow-up
```

## Findings Template (FINDINGS.md)

Gemini should produce:

```markdown
# Review Findings: [Title]

## Summary
[Brief overview of review results]

## Findings

| Severity | Location | Issue | Recommendation |
|----------|----------|-------|----------------|
| CRITICAL | users.ts:45 | SQL injection via unsanitized input | Use parameterized queries |
| HIGH | auth.ts:23 | Missing rate limiting on login | Add rate limiter middleware |
| MEDIUM | users.ts:78 | No input validation | Add schema validation |
| LOW | auth.ts:12 | Magic number | Extract to named constant |

## Detailed Analysis

### CRITICAL: SQL Injection (users.ts:45)
[Detailed explanation with code example]

### HIGH: Missing Rate Limiting (auth.ts:23)
[Detailed explanation with recommendation]

## Recommendations
1. [Priority action items]
2. [Secondary improvements]

## Overall Assessment
[Summary judgment: PASS | NEEDS WORK | FAIL]

## Session
Session ID: `<id>` (for follow-up questions)
```

## Workflow Example (ras-commander)

### 1. Write REVIEW.md

```markdown
# Review Request: Remote Execution Security

## Objective
Security review of the PsExec-based remote execution module.

## Review Criteria
Rate findings: CRITICAL | HIGH | MEDIUM | LOW

Focus on:
- Command injection vulnerabilities
- Credential exposure
- Path traversal risks
- Session hijacking

## Code to Review

### File: ras_commander/remote/PsexecWorker.py
```python
[paste relevant code]
```

### File: ras_commander/remote/Execution.py
```python
[paste relevant code]
```

## Context
- This module executes HEC-RAS remotely via PsExec
- Runs with elevated privileges on remote Windows machines
- Handles user credentials for authentication

## Output Format
Write to FINDINGS.md with severity-rated findings and specific mitigations.
```

### 2. Execute Gemini

```bash
cd "C:/GH/ras-commander" && gemini -y "Read REVIEW.md, perform security review per criteria, write findings to FINDINGS.md"
```

### 3. Read FINDINGS.md

Review findings, address issues, continue development.

## Environment Variables

```bash
GEMINI_API_KEY=xxx         # Required (or use OAuth login)
GOOGLE_API_KEY=xxx         # Alternative (takes precedence)
```

## Rate Limits

| Limit | Value |
|-------|-------|
| Requests/minute | 60 |
| Requests/day | 1,000 |

## Session Management

- Session ID appears in Gemini output
- Use `gemini --list-sessions` to see available sessions
- Resume with `gemini -r <id> "follow-up instruction"`

## Tips

1. **Paste actual code** - Don't describe, include the real code in REVIEW.md
2. **Define severity levels** - CRITICAL/HIGH/MEDIUM/LOW helps prioritization
3. **Specify output structure** - Tell Gemini exactly what FINDINGS.md should contain
4. **Provide context** - Domain, compliance requirements, constraints
5. **Ask focused questions** - One review type per request gets better results

## Decision Matrix: Gemini vs Codex

| Task | Gemini | Codex |
|------|:------:|:-----:|
| Code review / QAQC | Best | OK |
| Security audit | Best | OK |
| Implementation | OK | Best |
| Refactoring | OK | Best |
| Large codebase analysis | Best | OK |
| Documentation review | Best | OK |
| Extended thinking (20-30 min) | OK | Best |

## When to Escalate

**Use Gemini for**:
- Quick code reviews
- Documentation checks
- Large context analysis
- Security audits (initial scan)

**Use Codex for**:
- Complex implementation
- Extended thinking tasks
- Multi-file refactoring

**Use specialized ras-commander agents for**:
- HDF analysis -> `hdf-analyst`
- Geometry parsing -> `geometry-parser`
- USGS integration -> `usgs-integrator`

---

**See Also**:
- `code-oracle-gemini` agent - Full orchestration capabilities
- `.claude/rules/subagent-output-pattern.md` - Output format standards
