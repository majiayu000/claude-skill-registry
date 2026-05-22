---
name: review:security
description: Security-focused review covering vulnerabilities, privacy, infrastructure security, data integrity, and supply chain. Spawns the senior-review-specialist agent for thorough security analysis.
---

# Security Code Review

Run a security-focused review using 5 security checklists via the senior-review-specialist agent.

## Instructions

Spawn the `senior-review-specialist` agent to perform this review.

## Checklists to Apply

Load and apply these review checklists:

- `commands/review/security.md` - Vulnerabilities, insecure defaults, missing controls
- `commands/review/privacy.md` - PII handling, data minimization, compliance
- `commands/review/infra-security.md` - IAM, networking, secrets, configuration
- `commands/review/data-integrity.md` - Data correctness over time, failures, concurrency
- `commands/review/supply-chain.md` - Dependency risks, lockfiles, build integrity

## Agent Instructions

The agent should:

1. **Get working tree changes**: Run `git diff` to see all changes
2. **Map threat surface**:
   - Identify entry points (HTTP handlers, CLI, webhooks)
   - Identify trust boundaries (user input, DB, external APIs)
   - Identify assets at risk (credentials, PII, financial data)
3. **For each changed file**:
   - Read the full file content
   - Go through each diff hunk
   - Apply all 5 security checklists
   - Look for OWASP Top 10 vulnerabilities
4. **Cross-reference related files**: Trace data flow, check auth
5. **Find ALL security issues**: Security bugs are critical

## Output Format

Generate a security review report with:

- **Critical Issues (BLOCKER)**: Security vulnerabilities that must be fixed
- **High Risk Issues**: Significant security concerns
- **Medium Risk Issues**: Security improvements recommended
- **Threat Surface Analysis**: Entry points, trust boundaries, assets
- **Security Posture**: Authentication, authorization, input validation assessment
- **File Summary**: Security issues per file
- **Overall Assessment**: Secure/Not Secure recommendation with rationale
