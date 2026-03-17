---
name: full-review
description: Comprehensive code review using all available skills. Use before committing or when you want a thorough analysis of changes. Triggers on review code, check changes, full review, pre-commit review.
---

# Full Code Review

Orchestrates all available review skills to provide comprehensive code analysis.

## When to Use

- Before committing code changes
- Performing pre-merge reviews
- Running comprehensive audits
- Checking code against all quality standards
- Validating changes across the full stack

## Workflow

### Step 1: Identify Changes

Get list of changed files using git diff.

### Step 2: Map Skills to Files

Invoke relevant skills based on file patterns.

### Step 3: Run Checklists

Apply security, DeFi, type safety, and performance checks.

### Step 4: Generate Report

Produce structured report with severity levels.

### Step 5: Auto-Fix (Optional)

Offer to fix critical issues automatically.

---

## Trigger Phrases
- "review code", "check changes", "full review"
- "pre-commit review", "review before commit"
- "run all skills", "comprehensive review"

## Review Process

### Step 1: Identify Changes
```bash
# Get changed files
git diff --name-only HEAD~1 2>/dev/null || git diff --name-only
git status --porcelain
```

### Step 2: Skill Mapping

Based on changed files, invoke these skills:

| Changed Files | Skills to Invoke |
|--------------|------------------|
| Any `.ts`, `.tsx` | code-review-expert, common-pitfalls |
| `server/src/routes/*` | system-integration-validator |
| `server/src/services/*` | defi-expert, hft-quant-expert |
| `server/src/db/*` | code-consistency-validator |
| `client/src/pages/*`, `client/src/components/*` | apple-ui-design, common-pitfalls |
| `client/src/hooks/*` | common-pitfalls (TanStack Query) |
| `rust-core/**/*.rs` | code-consistency-validator, latency-tracker |
| `*token*`, `*protocol*`, `*chain*` | defi-registry-manager |
| `*arbitrage*`, `*trade*`, `*swap*` | liquidity-depth-analyzer |
| `*logger*`, `*error*` | error-logger |
| `*websocket*`, `*ws*` | common-pitfalls (WebSocket) |
| `schema.ts`, `*.sql` | common-pitfalls (Drizzle) |

### Step 3: Review Checklist

For EVERY review, check these critical items:

#### Security
- [ ] No SQL injection vulnerabilities
- [ ] No XSS in React components (dangerouslySetInnerHTML)
- [ ] No command injection in Bash calls
- [ ] No hardcoded secrets/credentials
- [ ] Proper input validation on all endpoints
- [ ] Rate limiting on sensitive routes

#### DeFi-Specific
- [ ] Token decimals correct (USDC/USDT=6, WBTC=8, ETH=18)
- [ ] Token addresses in checksum format
- [ ] BigInt handling (no precision loss with Number())
- [ ] Slippage protection on swaps
- [ ] Proper error handling for reverts

#### Type Safety
- [ ] No `as any` type assertions
- [ ] Types match across TypeScript ↔ Rust ↔ PostgreSQL
- [ ] Zod schemas for all API inputs
- [ ] Proper null/undefined handling

#### Performance
- [ ] No N+1 queries
- [ ] Proper indexing on queried columns
- [ ] Timeouts on external calls
- [ ] Connection pooling configured

#### Code Quality
- [ ] Error messages don't leak internal details
- [ ] Consistent naming conventions
- [ ] No dead code or unused imports
- [ ] Proper async/await usage

#### TanStack Query (if applicable)
- [ ] QueryKeys use full URL paths
- [ ] Mutations invalidate relevant queries
- [ ] Using isPending (not isLoading) for mutations in v5
- [ ] Responses typed with schema types

#### Drizzle ORM (if applicable)
- [ ] No primary key type changes
- [ ] Array columns use `text().array()` syntax
- [ ] Insert/select types exported for models
- [ ] Using drizzle-zod for validation

#### React Components (if applicable)
- [ ] Loading/error states handled
- [ ] data-testid on interactive elements
- [ ] Using router Link, not window.location
- [ ] Helper functions defined before use

#### Blockchain/RPC (if applicable)
- [ ] All contract calls wrapped in try/catch
- [ ] Multicall uses `allowFailure: true`
- [ ] Prices validated against expected ranges
- [ ] Handling "execution reverted" gracefully

### Step 4: Report Format

```markdown
## Code Review Report

### Files Reviewed
- [list files]

### Skills Applied
- [list skills invoked]

### Critical Issues (MUST FIX)
🔴 [issue description]
   File: path/to/file.ts:line
   Fix: [how to fix]

### Warnings (SHOULD FIX)
🟡 [issue description]
   File: path/to/file.ts:line
   Suggestion: [recommendation]

### Suggestions (NICE TO HAVE)
🟢 [improvement idea]

### Summary
- Critical: X issues
- Warnings: X issues
- Suggestions: X items
- Ready to commit: Yes/No
```

### Step 5: Auto-Fix

If critical issues found, offer to fix them:
1. Show the issue
2. Show the proposed fix
3. Apply if approved
4. Re-run validation

## Quick Commands

- `/review` - Full review of all changes
- `/quick-review` - Fast check of critical issues only
- Invoke `full-review` skill for this comprehensive process
