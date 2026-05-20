---
name: using-codebase-quality
description: Codebase quality orchestration for maintaining high-quality, secure, well-documented code. Use when completing features, running quality audits, checking security, updating documentation, or before merging PRs. Triggers on quality check, code review, security scan, documentation update, codebase audit, pre-merge check, bd close, feature complete.
version: 1.1.0
title: "Using Codebase Quality"
status: active
---

# Codebase Quality Superpowers

You are the Codebase Quality orchestrator. This meta-skill coordinates specialized sub-skills to maintain codebase excellence.

## Invocation Triggers

The following triggers invoke codebase-quality sub-skills. Claude recognizes these patterns:

```
/codebase-quality:security      → Load security sub-skill
/codebase-quality:code-quality  → Load code-quality sub-skill
/codebase-quality:documentation → Load documentation sub-skill
/codebase-quality:post-push     → Load post-push review sub-skill
/codebase-quality:codex         → Load Codex external reviewer sub-skill
/codebase-quality:full-audit    → Run all quality checks in sequence
```

**When triggered by system-reminder** (e.g., `[POST-PUSH CODE REVIEW TRIGGERED]`):
- Read the reminder for context (branch, commits, Codex report path)
- Load the appropriate sub-skill
- Execute according to its workflow

## Sub-Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `codebase-quality:security` | Vulnerability scans, secrets detection, dependency audits | First - blocks on critical issues |
| `codebase-quality:code-quality` | Linting, style, refactoring, type safety | Second - after security passes |
| `codebase-quality:documentation` | CLAUDE.md sync, doc updates, status tracking | Third - after code is clean |
| `codebase-quality:post-push` | Automated review after git push | Triggered by hook or manual |
| `codebase-quality:codex` | External GPT-5 Codex review | Independent external perspective |

## Quick Reference

### Invoking Sub-Skills

```python
# Security scan (run first)
Skill("codebase-quality:security")

# Code quality check
Skill("codebase-quality:code-quality")

# Documentation update
Skill("codebase-quality:documentation")

# Full audit (all quality checks)
Skill("codebase-quality:full-audit")

# Post-push review (triggered by hook or manual)
Skill("codebase-quality:post-push")

# External Codex review (independent GPT-5 perspective)
Skill("codebase-quality:codex")
```

### Commands

```bash
# Full quality audit
/codebase-quality audit

# Individual checks
/codebase-quality security
/codebase-quality code
/codebase-quality docs

# Pre-merge validation
/codebase-quality pre-merge

# Post-push review (triggered by hook or manual)
/codebase-quality post-push

# External Codex review
/codebase-quality codex

# Post-feature update (triggered by bd close)
/codebase-quality post-feature <bd-id>
```

## Automatic Triggers

### On Beads Close (`bd close`)

When a task is completed:
```
bd close <bd-id>
    ↓
codebase-quality:documentation triggered
    ↓
1. Scan changed files
2. Update relevant CLAUDE.md
3. Update solution_design status
4. Update INDEX.md cross-references
```

### On PR Merge to Main

```
PR merged to main
    ↓
codebase-quality:documentation triggered
    ↓
1. Update status to "rolled-out"
2. Set deployed_at timestamp
3. Update PROJECT_STATUS.md
```

### Pre-Merge Check (Recommended)

```
/codebase-quality pre-merge
    ↓
1. security → Block if critical issues
2. code-quality → Warn on violations
3. documentation → Warn if stale
```

## Workflow Patterns

### Pattern 1: Full Audit

```
Skill("codebase-quality:full-audit")
    ↓
┌─────────────────────────────────────────┐
│ Phase 1: Security (BLOCKING)            │
│ - Secrets detection                     │
│ - Dependency vulnerabilities            │
│ - Injection risks                       │
│ IF CRITICAL → STOP, report, remediate   │
└─────────────────────────────────────────┘
    ↓ (passes)
┌─────────────────────────────────────────┐
│ Phase 2: Code Quality                   │
│ - Linting errors                        │
│ - Type safety issues                    │
│ - Style violations                      │
│ IF MAJOR → Warn, suggest fixes          │
└─────────────────────────────────────────┘
    ↓ (passes or warns)
┌─────────────────────────────────────────┐
│ Phase 3: Documentation                  │
│ - CLAUDE.md freshness                   │
│ - Status metadata accuracy              │
│ - INDEX.md cross-references             │
│ Report staleness, update if needed      │
└─────────────────────────────────────────┘
    ↓
Generate Quality Report
```

### Pattern 2: Post-Feature (After bd close)

```
Skill("codebase-quality:documentation")
    ↓
1. Identify changed files from recent commits
2. Determine affected documentation
3. Update module CLAUDE.md if patterns changed
4. Update solution_design status to "implemented"
5. Commit docs with "docs(module): Update for <bd-id>"
```

### Pattern 3: Pre-Merge Validation

```
/codebase-quality pre-merge
    ↓
1. Run security scan
   - Block merge if secrets found
   - Block merge if critical vulnerabilities
    ↓
2. Run code quality check
   - Require lint passing
   - Warn on type errors
    ↓
3. Run documentation check
   - Warn if CLAUDE.md stale
   - Warn if no status update
    ↓
4. Generate pre-merge report
   - ✅ Ready to merge, or
   - ❌ Issues to resolve
```

## Integration with Orchestrator

### In orchestrator Phase 2 workflow:

```
... (feature validation complete)
   ↓
7. `bd close <bd-id>`
   ↓
8. Invoke codebase-quality:documentation
   - Updates CLAUDE.md for affected modules
   - Updates solution_design status
   - Commits documentation changes
   ↓
9. Final commit with code + docs
```

### In worker completion:

```
Worker: "Task bd-xxxx COMPLETE"
   ↓
Orchestrator validates feature
   ↓
Orchestrator runs: Skill("codebase-quality:documentation")
   ↓
Documentation updated automatically
```

## Output Locations

| Output | Location |
|--------|----------|
| Quality reports | `.claude/docs/quality-reports/` |
| Security findings | `.claude/docs/security-findings/` |
| Documentation diffs | `.claude/docs/doc-changes/` |
| Audit history | `.claude/docs/audit-log.md` |

## Best Practices

1. **Security First**: Always run security before code quality
2. **Block on Critical**: Don't proceed if security finds critical issues
3. **Update Docs Early**: Run documentation update immediately after feature
4. **Pre-Merge Always**: Never skip pre-merge checks for significant PRs
5. **Automate Triggers**: Configure hooks for automatic quality checks

## Sub-Skill Details

### codebase-quality:security
- **Purpose**: Find and prevent security vulnerabilities
- **Blocks**: Critical vulnerabilities, exposed secrets
- **Warns**: Outdated dependencies, potential risks
- **Full docs**: [security/SKILL.md](../security/SKILL.md)

### codebase-quality:code-quality
- **Purpose**: Ensure consistent, clean code
- **Blocks**: Lint errors, type errors (configurable)
- **Warns**: Style violations, complex code
- **Full docs**: [code-quality/SKILL.md](../code-quality/SKILL.md)

### codebase-quality:documentation
- **Purpose**: Keep documentation accurate and current
- **Blocks**: (nothing - documentation is never blocking)
- **Warns**: Stale CLAUDE.md, missing status updates
- **Full docs**: [documentation/SKILL.md](../documentation/SKILL.md)

### codebase-quality:post-push
- **Purpose**: Automated post-push code review
- **Trigger**: PostToolUse hook after git push success
- **Blocks**: (nothing - advisory only)
- **Behavior**: Orchestrates security → code-quality → documentation sequentially
- **Full docs**: [post-push/SKILL.md](../post-push/SKILL.md)

## Exit Condition

Stay in codebase-quality mode until:
- `/end-quality` command
- Quality report generated
- All sub-skills completed

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-12-19
**Related Skills**: orchestrator-multiagent, worker-focused-execution
