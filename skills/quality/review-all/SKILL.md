---
name: review:all
description: Comprehensive code review using all 30 review checklists. Spawns the senior-review-specialist agent for thorough file-by-file analysis.
---

# Comprehensive Code Review

Run a thorough review using ALL 30 review checklists via the senior-review-specialist agent.

## Instructions

Spawn the `senior-review-specialist` agent to perform this review.

## Checklists to Apply

Load and apply ALL of these review checklists:

### Correctness & Logic
- `commands/review/correctness.md` - Logic flaws, broken invariants, edge-case failures
- `commands/review/backend-concurrency.md` - Race conditions, atomicity, locking, idempotency
- `commands/review/refactor-safety.md` - Semantic drift, behavior equivalence

### Security & Privacy
- `commands/review/security.md` - Vulnerabilities, insecure defaults, missing controls
- `commands/review/infra-security.md` - IAM, networking, secrets, configuration
- `commands/review/privacy.md` - PII handling, data minimization, compliance
- `commands/review/supply-chain.md` - Dependency risks, lockfiles, build integrity
- `commands/review/data-integrity.md` - Data correctness over time, failures, concurrency

### Architecture & Design
- `commands/review/architecture.md` - Boundaries, dependencies, layering
- `commands/review/performance.md` - Algorithmic efficiency, N+1 queries, bottlenecks
- `commands/review/scalability.md` - Load handling, dataset growth, multi-tenancy
- `commands/review/api-contracts.md` - Stability, correctness, consumer usability
- `commands/review/maintainability.md` - Readability, change amplification
- `commands/review/overengineering.md` - Unnecessary complexity, YAGNI violations

### Infrastructure & Operations
- `commands/review/infra.md` - Deployment config, least privilege, operational clarity
- `commands/review/ci.md` - Pipeline security, deployment safety
- `commands/review/release.md` - Versioning, rollout, migration, rollback
- `commands/review/migrations.md` - Database migration safety
- `commands/review/reliability.md` - Failure modes, partial outages
- `commands/review/logging.md` - Secrets exposure, PII leaks, wide-events
- `commands/review/observability.md` - Logs, metrics, tracing, alertability
- `commands/review/cost.md` - Cloud infrastructure cost implications

### Quality & Testing
- `commands/review/testing.md` - Test quality, coverage, reliability
- `commands/review/style-consistency.md` - Codebase style, idioms
- `commands/review/docs.md` - Documentation completeness and accuracy

### User Experience
- `commands/review/accessibility.md` - Keyboard, assistive technology, ARIA
- `commands/review/frontend-accessibility.md` - SPA-specific accessibility
- `commands/review/frontend-performance.md` - Bundle size, rendering, latency
- `commands/review/ux-copy.md` - User-facing text clarity, error recovery
- `commands/review/dx.md` - Developer experience, onboarding

## Agent Instructions

The agent should:

1. **Get working tree changes**: Run `git diff` to see all changes
2. **For each changed file**:
   - Read the full file content
   - Go through each diff hunk
   - Apply ALL 30 checklists to the changes
   - Trace problems to their root cause
3. **Cross-reference related files**: Follow imports, check callers
4. **Find ALL issues**: Be thorough, expect to find many issues

## Output Format

Generate a comprehensive review report with:

- **Critical Issues**: Blocking problems (must fix)
- **Warnings**: Should address before merge
- **Suggestions**: Improvements to consider
- **File Summary**: Issues per file with counts by severity
- **Overall Assessment**: Ship/Don't Ship recommendation with rationale
