---
name: df:security-audit
description: |
  Scan codebase for security vulnerabilities using parallel auditor agents.
  Standalone — works without .planning/ state. Covers OWASP Top 10, secrets, dependency risks, auth flaws.
  Triggers on: "security audit", "scan for vulnerabilities", "check for secrets", "security review", "find security issues"
argument-hint: "[optional: path scope like 'src/api' or focus filter like 'secrets-only', 'auth-only', 'deps-only']"
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - Write
  - Task
---

<objective>
Scan codebase for security vulnerabilities using 3 parallel df-security-auditor agents, each covering a different domain. Agents write findings directly to temp files. Orchestrator merges, deduplicates, ranks by severity, and produces a final SECURITY-AUDIT.md report.

This is a standalone command — no `.planning/` directory or DevFlow project state required. Works on any codebase.

Output: SECURITY-AUDIT.md (in `.planning/` if it exists, otherwise project root).
</objective>

<execution_context>
@~/.claude/devflow/workflows/security-audit.md
</execution_context>

<context>
Arguments: $ARGUMENTS (optional)

**Supported argument formats:**
- Path scope: `src/api` — limits scan to a subdirectory
- Focus filter: `secrets-only` — runs only the secrets-and-code agent
- Focus filter: `auth-only` — runs only the auth-and-access agent
- Focus filter: `deps-only` — runs only the config-and-deps agent
- Combination: `src/api secrets-only` — scoped + filtered

**This command can run:**
- On any codebase, at any time — no DevFlow initialization required
- Before `/df:new-project` — assess security posture of brownfield codebase
- After major changes — re-audit for regressions
- As part of release prep — generate audit report for review
</context>

<when_to_use>
**Use security-audit for:**
- Initial security assessment of a codebase
- Checking for hardcoded secrets before open-sourcing
- Reviewing auth/authz patterns after changes
- Dependency vulnerability awareness
- Pre-release security checklist
- Onboarding to an unfamiliar codebase (security perspective)

**Skip security-audit for:**
- Codebases with zero source files (nothing to scan)
- If you just need to check one specific file (manual review is faster)
</when_to_use>

<process>
1. Load init context, detect stack, determine scope and focus filter
2. Clean up any stale `.security-audit-tmp/` directory
3. Create `.security-audit-tmp/` directory
4. Spawn parallel df-security-auditor agents (1-3 depending on focus filter)
5. Collect confirmations, verify findings files exist
6. Read + merge all findings, deduplicate, renumber, sort by severity
7. Write SECURITY-AUDIT.md with YAML frontmatter (counts, categories, status)
8. Clean up `.security-audit-tmp/`
9. Present severity-based summary with next steps
</process>

<success_criteria>
- [ ] Init context loaded (model, stack, output path)
- [ ] Agents spawned with correct focus modes
- [ ] Agents wrote findings to `.security-audit-tmp/`
- [ ] Findings merged, deduplicated, sorted by severity
- [ ] SECURITY-AUDIT.md written with YAML frontmatter
- [ ] Temp directory cleaned up
- [ ] No secret values in any output
- [ ] User presented with actionable summary
</success_criteria>
