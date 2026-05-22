---
name: "Governance"
version: "1.4.0"
description: "Enforces engineering standards and code quality policies. Use during code reviews, before commits, when discussing standards or compliance, and for quality audits."
category: development
tags:
  - governance
  - code-review
  - standards
  - compliance
  - quality
author: Smith Horn
triggers:
  keywords:
    - code review
    - review this
    - commit
    - before I merge
    - standards
    - compliance
    - code quality
    - best practices
    - retro
    - retrospective
    - test edge function
    - edge function test
    - mock Deno
    - Deno is not defined
  explicit:
    - /governance
    - /review
    - /retro
    - /edge-test
composes:
  - linear
---

# Governance Skill

## Behavioral Classification

**Type**: Autonomous Execution (ADR-025)

This skill executes automatically without asking for permission. When triggered during code review:
1. All issues are identified (critical, major, minor)
2. **ALL issues are immediately FIXED** - no deferral, no "later"
3. Results are reported with commit hashes

**Anti-pattern**: "Would you like me to fix these issues?"
**Anti-pattern**: "Created SMI-1234 to track this for later."
**Correct pattern**: "Found 5 issues. Fixing all 5 now. Commits: abc123, def456."

**🚨 ZERO DEFERRAL POLICY**: Do not create Linear tickets for code review findings. Fix them immediately. The only exception is if the fix requires architectural changes that would expand scope beyond the current PR - and even then, implement a minimal fix now.

---

Enforces engineering standards from [standards.md](../../../docs/architecture/standards.md) during development.

## Trigger Phrases

See frontmatter `triggers` block for keyword and explicit command triggers.

**Explicit Commands**: `/governance`, `/review`, `/retro`, `/edge-test`

## Quick Audit

Run the standards audit (in Docker):

```bash
docker exec skillsmith-dev-1 npm run audit:standards
```

## Pre-Commit Checklist

Before every commit, run these in Docker:

```bash
docker exec skillsmith-dev-1 npm run typecheck
docker exec skillsmith-dev-1 npm run lint
docker exec skillsmith-dev-1 npm run format:check  # Catch formatting before CI
docker exec skillsmith-dev-1 npm test
docker exec skillsmith-dev-1 npm run audit:standards
```

### Pre-Push Verification

Before pushing, verify no source files are missing from commits:

```bash
# Check for untracked source files (common CI failure cause)
git status --short | grep "^??" | grep -E "packages/.*/src/"

# If any appear, they likely need to be staged and committed!
```

For the complete wave completion checklist, see [docs/process/wave-completion-checklist.md](../../../docs/process/wave-completion-checklist.md).

## Two-Document Model

| Document | Purpose | Location |
|----------|---------|----------|
| CLAUDE.md | AI operational context | Project root |
| standards.md | Engineering policy (authoritative) | docs/architecture/ |

## Key Standards Reference

### Code Quality (§1)

- **TypeScript strict mode** - No `any` without justification
- **500 line limit** - Split larger files
- **JSDoc for public APIs**
- **Co-locate tests** (`*.test.ts`)

### Type Safety Patterns (Code Review Focus)

Common type errors to catch during review:

| Pattern | Issue | Fix |
|---------|-------|-----|
| `null` vs `undefined` | Return type mismatch | Use consistent nullish type |
| `as any` cast | Type safety bypass | Use proper generic or type guard |
| Missing `\| undefined` | Optional field not typed | Add to type definition |

**Example fix for null/undefined mismatch:**
```typescript
// BAD: cache is null but return type is undefined
let cache: Data | null = null
function get(): Data | undefined { return cache }  // TS2322!

// GOOD: Use Symbol for uninitialized state
const NOT_LOADED = Symbol('not-loaded')
let cache: Data | undefined | typeof NOT_LOADED = NOT_LOADED
function get(): Data | undefined {
  return cache === NOT_LOADED ? undefined : cache
}
```

### Testing (§2)

- **80% unit coverage** (90% for MCP tools)
- **Tests alongside code**
- **Mock external services only**

### Workflow (§3)

- **Docker-first** - All commands via `docker exec skillsmith-dev-1`
- **Trunk-based development** - Short-lived feature branches
- **Conventional commits** - `<type>(scope): <description>`

### Security (§4)

- **No hardcoded secrets**
- **Validate all input** - Zod at boundaries
- **Prototype pollution checks** - Before JSON.parse
- **Safe subprocess spawning** - execFile with arrays

## Automated Checks

The `npm run audit:standards` command verifies:

- [ ] Docker command usage in scripts
- [ ] File length under 500 lines
- [ ] No console.log statements
- [ ] Import organization
- [ ] Test file coverage

## Code Review Workflow

**IMPORTANT: All issues are FIXED before PR merge. No deferral.**

**⚠️ EXECUTE, DON'T DEFER**: This workflow is mandatory. Do NOT ask "would you like me to fix these?" and do NOT create Linear tickets for findings. Fix everything immediately.

When performing a code review:

1. **Identify ALL issues** - Critical, major, and minor severity
2. **Fix EVERY issue immediately** - No exceptions, no deferral
3. **Commit each fix** - Include the fix in the PR before approval
**Anti-pattern (NEVER do this):**
> "I found 5 issues. Would you like me to fix them or create tickets?"

**Anti-pattern (NEVER do this):**
> "Created SMI-1234 to track this. Deferring to post-merge."

**Correct pattern:**
> "Found 5 issues. Fixing all 5 now. Commits: abc123, def456, ghi789."

### Zero Deferral Policy

**All findings are fixed immediately. No Linear tickets for code review findings.**

This ensures:
- Issues don't accumulate in the backlog
- Code quality is maintained at merge time
- Reviewers take ownership of quality

**Exception**: Only defer if the fix requires architectural changes that would significantly expand PR scope. Even then, implement a minimal fix first.

### Severity Guide (SMI-1726)

| Severity | Action | Examples |
|----------|--------|----------|
| Critical | **Fix immediately** | Security vulnerabilities, data loss risks |
| High | **Fix immediately** | Missing tests, type safety issues |
| Medium | **Fix immediately** | Architecture issues, style problems |
| Low | **Fix immediately** | Minor refactors, documentation gaps |

**🚨 ALL SEVERITIES ARE FIXED. NO EXCEPTIONS.**

### Code Review Completion Checklist

Before marking a code review complete:

- [ ] All critical issues **fixed** (with commit hash)
- [ ] All high issues **fixed** (with commit hash)
- [ ] All medium issues **fixed** (with commit hash)
- [ ] All low issues **fixed** (with commit hash)
- [ ] Lint passes after all fixes
- [ ] Typecheck passes after all fixes
- [ ] Re-review confirms fixes are correct
- [ ] **Code review report written to `docs/code_review/`**

### Code Review Report (Mandatory)

**Every code review MUST produce a written report** saved to `docs/code_review/`.

📄 **Full template**: [code-review-template.md](code-review-template.md)

**Quick reference**:
- File naming: `YYYY-MM-DD-<brief-slug>.md`
- Required sections: Summary, Pre-Review Checks, Files Reviewed, Findings, CI Impact Assessment

---

## Retrospective Reports

When running a retrospective ("retro"), **MUST produce a written report** saved to `docs/retros/`.

📄 **Full template**: [retro-template.md](retro-template.md)

**Quick reference**:
- File naming: `YYYY-MM-DD-<topic-slug>.md`
- Required sections: What Went Well, What Went Wrong, Metrics, Key Lessons

### Retrospective Completion Checklist

- [ ] All completed issues listed with SMI numbers
- [ ] PRs and branch documented
- [ ] "What Went Well" has at least 2 items
- [ ] "What Went Wrong" is honest (even if brief)
- [ ] Metrics are accurate (including code review findings)
- [ ] Key lessons are actionable
- [ ] Breaking changes documented (if applicable)
- [ ] **Report written to `docs/retros/`**

---

## Sub-Documentation

| Document | Contents |
|----------|----------|
| [code-review-template.md](code-review-template.md) | Full code review report template with field descriptions |
| [retro-template.md](retro-template.md) | Full retrospective template with completion checklist |
| [edge-function-test.md](edge-function-test.md) | Edge Function test scaffold generator with vi.hoisted() pattern |

---

## When to Invoke

This skill activates automatically during:

1. **Code reviews** - Creates Linear issues for ALL findings
2. **Pre-commit** - Reminds about checklist
3. **Quality discussions** - References authoritative standards
4. **Edge Function testing** - Generates test scaffolds with proper Deno mocking

## Full Standards

For complete policy details, see [docs/architecture/standards.md](../../../docs/architecture/standards.md).

## Related Process Documents

| Document | Purpose |
|----------|---------|
| [Wave Completion Checklist](../../../docs/process/wave-completion-checklist.md) | Pre/post commit verification steps |
| [Exploration Phase Template](../../../docs/process/exploration-phase-template.md) | Discover existing code before implementing |
| [Linear Hygiene Guide](../../../docs/process/linear-hygiene-guide.md) | Prevent duplicate issues |
| [Infrastructure Inventory](../../../docs/architecture/infrastructure-inventory.md) | What exists in the codebase |

## Common CI Failures

Patterns that pass locally but fail in CI:

| Failure | Root Cause | Prevention |
|---------|------------|------------|
| `Cannot find module './foo.types.js'` | New files created but not committed | Run `git status` before push |
| Prettier formatting errors | Formatting not run locally | Add `format:check` to pre-commit |
| `TS2322: Type 'null' not assignable` | null vs undefined mismatch | Use consistent nullish types |
| Native module errors | Missing rebuild after install | Run `npm rebuild` in Docker |

## Git Hooks

A pre-commit hook is available to warn about untracked files in `packages/*/src/`:

```bash
# Install the hook
cp scripts/git-hooks/pre-commit-check-src.sh .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

See [scripts/git-hooks/README.md](../../../scripts/git-hooks/README.md) for details.

---

## Changelog

### v1.4.0 (2026-01-28)
- **Breaking**: Zero Deferral Policy - all code review findings must be fixed immediately
- **Removed**: Linear ticket creation for deferred issues
- **Updated**: Severity guide - all severities now require immediate fix
- **Updated**: Completion checklist - removed deferral options
- **Updated**: Behavioral Classification to emphasize execution over deferral

### v1.3.0 (2026-01-27)
- **Added**: `edge-function-test.md` subskill for Edge Function test scaffolds (SMI-1877)
- **Added**: `templates/edge-function-test-template.ts` with vi.hoisted() pattern
- **Added**: `/edge-test` explicit command
- **Added**: Trigger phrases: "test edge function", "mock Deno", "Deno is not defined"

### v1.2.0 (2026-01-24)
- **Refactored**: Split templates into sub-documentation files (SMI-1783)
- **Added**: `code-review-template.md` with full template and field descriptions
- **Added**: `retro-template.md` with full template and completion checklist
- **Added**: Sub-documentation table linking to template files
- **Reduced**: Main SKILL.md from ~450 lines to ~350 lines

### v1.1.0 (2026-01-24)
- **Enhanced**: Code review report template with Docker validation, pre-review checks, CI impact assessment
- **Enhanced**: Retrospective report template with waves/sessions, breaking changes, per-wave findings
- **Added**: Structured triggers in YAML frontmatter
- **Added**: Explicit commands (`/governance`, `/review`, `/retro`)
- **Added**: `composes: [linear]` for skill composition
- **Added**: "retro", "retrospective" trigger phrases

### v1.0.0 (2025-12)
- Initial release
- Code review workflow with severity guide
- Pre-commit checklist
- Standards reference from standards.md

---

**Created**: December 2025
**Updated**: January 2026
**Maintainer**: Skillsmith Team
