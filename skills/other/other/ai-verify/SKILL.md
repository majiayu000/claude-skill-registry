---
name: ai-verify
description: "Use when you need to PROVE a claim with evidence, run quality/security scans, or validate that work is actually complete. Evidence before claims -- no 'should work' allowed."
effort: max
argument-hint: "claim|governance|security|quality|performance|a11y|feature|architecture|platform"
---


# Verify

## Purpose

Evidence before claims. This skill has two faces: (1) a verification protocol that proves claims with commands, and (2) a multi-mode scanner for quality, security, and governance. Both share the same principle: run the command, read the output, check the exit code. No guessing.

## When to Use

- Before claiming "it works" (run the test, show the output)
- Before claiming "it's secure" (run the scan, show the findings)
- Before claiming "Done!" (verify every acceptance criterion with evidence)
- When running quality/security/governance scans on a codebase

## Process

### Verification Protocol (claim mode)

For every claim, follow IRRV:

**I -- IDENTIFY**: What command proves this claim?
- "Tests pass" -> `uv run pytest tests/ -v`
- "No lint errors" -> `ruff check .`
- "No secrets" -> `gitleaks protect --staged`
- "File exists" -> `ls -la path/to/file`

**R -- RUN**: Execute the FULL command. Not a subset. Not from memory. Fresh execution.

**R -- READ**: Read the FULL output. Check:
- Exit code (0 = success, non-zero = failure)
- Warning lines (even with exit code 0)
- Actual numbers (test count, coverage %, finding count)

**V -- VERIFY**: Does the output CONFIRM the claim?
- If yes: report with evidence (exact command + key output lines)
- If no: report the discrepancy. Do not claim success.

**Forbidden words** (never use these without evidence):
- "should work", "probably fine", "seems to", "looks good"
- "Done!", "Perfect!", "All set!"
- "I believe", "I think", "most likely"

### Scan Modes (7 parallel modes)

| Mode | Command | What it assesses |
|------|---------|------------------|
| `governance` | `/ai-verify governance` | Integrity, compliance, ownership boundaries |
| `security` | `/ai-verify security` | OWASP SAST, secret detection, dependency vulns |
| `quality` | `/ai-verify quality` | Coverage, complexity, duplication, lint |
| `performance` | `/ai-verify performance` | N+1 queries, O(n^2), memory leaks, bundle size |
| `a11y` | `/ai-verify a11y` | WCAG 2.1 AA compliance |
| `feature` | `/ai-verify feature` | Spec vs code gaps, disconnected implementations |
| `architecture` | `/ai-verify architecture` | Drift, coupling, cohesion, boundaries |
| `platform` | `/ai-verify platform` | All 7 modes aggregated -> GO/NO-GO |

Auto-detect: when invoked without a mode, infer from context.

### Scan Output Contract

Every scan mode produces:

```markdown
## Score: N/100
## Verdict: PASS | WARN | FAIL

## Findings
| # | Severity | Category | Description | Location | Remediation |

## Gate Check
- Blocker findings: N (threshold: 0)
- Critical findings: N (threshold: 0)
```

### Scan Thresholds

| Mode | Blocker if... | Critical if... |
|------|--------------|----------------|
| governance | Any integrity FAIL | Any compliance FAIL |
| security | Critical/high CVE | Any secret detected |
| quality | Coverage < 80% | Blocker/critical lint |
| performance | N+1 in critical path | O(n^2) in hot path |
| architecture | Circular dependency | Critical drift from spec |
| **platform** | Any blocker in ANY mode | Score < 60 |

## Verification Checklist (use before claiming DONE)

```
- [ ] Every acceptance criterion verified with a command
- [ ] All tests pass (exact count reported)
- [ ] Lint/format clean (zero warnings)
- [ ] No secrets in staged files
- [ ] Coverage maintained or improved (exact % reported)
- [ ] No forbidden words used in the completion report
```

## Common Mistakes

- Claiming success without running the command
- Running a subset of tests instead of the full suite
- Ignoring warnings when exit code is 0
- Using forbidden words ("should work") instead of evidence
- Not checking exit codes
- Reporting coverage from memory instead of from the tool output

## Integration

- **Called by**: `/ai-dispatch` (post-task review), `ai-build agent` (after implementation), user directly
- **Calls**: stack-specific tools (pytest, ruff, gitleaks, etc.)
- **Read-only**: never modifies source code -- produces findings with remediation

$ARGUMENTS
