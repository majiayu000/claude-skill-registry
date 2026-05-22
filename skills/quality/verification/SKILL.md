---
name: verification-first
category: verification
version: 2.0.0
description: Verification-first development approach - Australian-enhanced
author: Unite Group
priority: 1
auto_load: true
---

# Verification-First Development

## The Problem with AI Coding Assistants

Most AI coding assistants:
- Claim fixes without verification
- Move on before testing
- Celebrate partial progress as complete
- Avoid acknowledging broken code

## This System's Approach

### Rule 1: Prove It Works
Every code change MUST be verified before moving on:
- Run the build
- Run the tests
- Check the actual output
- Confirm expected behavior

### Rule 2: Honest Failure Reporting
When something fails:
- State clearly: "This failed"
- Include the actual error message
- Don't soften or interpret the failure
- Don't say "almost working" - it either works or it doesn't

### Rule 3: No Assumptions
- Don't assume a fix worked
- Don't assume tests pass
- Don't assume code compiles
- VERIFY EVERYTHING

### Rule 4: Root Cause First
Before attempting any fix:
1. Read the actual error message
2. Understand what the error means
3. Identify the root cause
4. THEN propose a fix

### Rule 5: One Fix at a Time
- Make one change
- Verify it
- Then move to the next
- Don't stack multiple untested changes

## Verification Commands

### Frontend (Next.js)
```bash
# Type check
pnpm type-check

# Lint
pnpm lint

# Build
pnpm build

# Test
pnpm test
```

### Backend (Python)
```bash
# Type check
uv run mypy src/

# Lint
uv run ruff check src/

# Test
uv run pytest

# Run server
uv run uvicorn src.api.main:app --reload
```

### Full Stack
```bash
# Everything
pnpm turbo run build lint type-check test
```

## Australian Context Verification

Additional verification for Australian market:
- **Spelling**: Verify en-AU spelling (colour, organisation, licence)
- **Dates**: Verify DD/MM/YYYY format in UI
- **Currency**: Verify AUD currency formatting ($1,234.56)
- **Regulations**: Verify compliance with Privacy Act 1988, WCAG 2.1 AA
- **Design**: Verify NO Lucide icons used, 2025-2026 aesthetic enforced

## Verification Tiers

### Tier A: Quick Verification (30 seconds)
- Type check passes
- Lint passes
- No console errors

### Tier B: Standard Verification (2-3 minutes)
- All Tier A checks
- Unit tests pass
- Build succeeds
- Manual smoke test of changed functionality

### Tier C: Full Verification (5-10 minutes)
- All Tier B checks
- Integration tests pass
- E2E tests for affected flows
- Visual regression check
- Performance benchmark

### Tier D: Production Verification (15-20 minutes)
- All Tier C checks
- Full test suite (including slow tests)
- Lighthouse audit >90 all scores
- Security scan
- Accessibility audit (WCAG 2.1 AA)
- Australian context verification

## Output Format

When reporting status, use this format:

```
## Task: [Description]

### Status: [PASS | FAIL | BLOCKED]

### Verification Tier: [A | B | C | D]

### Verification:
- Build: [PASS/FAIL] - [output if failed]
- Tests: [PASS/FAIL] - [X/Y passed, failures listed]
- Manual check: [PASS/FAIL] - [what was checked]
- Australian context: [PASS/FAIL/N/A] - [en-AU compliance]

### Evidence:
[Screenshots, test output, logs]

### Next Steps:
- [If PASS: what's next]
- [If FAIL: what needs to be fixed and why]
```

## Integration with Hooks

This skill is automatically enforced by:
- `post-code.hook.md` - Runs Tier A verification after code generation
- `pre-commit.hook.md` - Runs Tier B verification before git commit
- `pre-deploy.hook.md` - Runs Tier D verification before deployment

## Independent Verification

**Critical**: Verification MUST be independent. The verification agent (`.claude/agents/verification/`) performs verification, NOT the agent that wrote the code.

NO SELF-ATTESTATION. Evidence required.
