---
name: identify
description: Identify friction points, bottlenecks, bugs, and technical debt. Use for audits, debugging sessions, when something feels wrong, or before major work to surface hidden issues. This is the second system in the 5-system framework.
---

# Identity System (Detection)

> **Purpose:** Surface problems, friction, and bottlenecks before they compound.
> **When to trigger:** Audits, debugging, pre-work analysis, or when something feels off.

## Detection Categories

### 1. Code Health

Run these checks:

- Type errors: `npx tsc --noEmit`
- Build errors: `npm run build`
- Lint issues: Check for warnings
- Unused imports/variables
- Circular dependencies

### 2. Performance Issues

Look for:

- Slow database queries (check Supabase logs)
- Large bundle sizes
- Unnecessary re-renders
- N+1 query patterns
- Missing indexes

### 3. User Experience Friction

Identify:

- Error states not handled gracefully
- Loading states missing
- Confusing user flows
- Edge cases not covered
- Poor error messages

### 4. Architecture Debt

Spot:

- Duplicated logic across files
- Inconsistent patterns
- Missing or premature abstractions
- Tightly coupled components
- God components/functions

### 5. Operational Gaps

Find:

- Missing error tracking/logging
- No observability into failures
- Manual processes that should be automated
- Missing environment variables
- Insecure configurations

### 6. Security Concerns

Check for:

- Exposed secrets or credentials
- Missing input validation
- SQL injection vectors
- XSS vulnerabilities
- Missing authentication/authorization

## Detection Process

### Quick Scan (5 min)

```bash
# Run type check
npx tsc --noEmit

# Check for build errors
npm run build

# Look for TODOs and FIXMEs
grep -r "TODO\|FIXME\|HACK\|XXX" src/
```

### Deep Scan (30 min)

1. Review recent git changes for introduced issues
2. Check Supabase logs for errors
3. Review component complexity
4. Check for missing error boundaries
5. Audit API route error handling

## Output Requirements

Log all findings to `.claude/issues-registry.md`:

```markdown
# Issues Registry

## Active Issues

| ID    | Category    | Severity | Description                | Location                | Detected   | Status |
| ----- | ----------- | -------- | -------------------------- | ----------------------- | ---------- | ------ |
| I-001 | Code Health | High     | Type error in auth flow    | src/lib/auth.ts:45      | 2026-01-01 | Open   |
| I-002 | UX Friction | Medium   | No loading state on submit | src/components/Form.tsx | 2026-01-01 | Open   |

## Severity Levels

- **Critical:** Blocks users or causes data loss
- **High:** Major functionality broken or security issue
- **Medium:** Degraded experience or tech debt
- **Low:** Minor polish or optimization

## Resolved Issues

(Move issues here when fixed, note resolution)
```

## Rules

1. **Document everything found** - Even minor issues, log them
2. **Severity matters** - Be honest about impact level
3. **Location is key** - Include file:line for code issues
4. **Don't fix while identifying** - Separate detection from resolution
5. **Update regularly** - Keep the registry current

## Transition

After identification:

- Multiple issues found → Proceed to **Priority System**
- Single clear issue → Proceed to **Execution System**
- Blocked by confusion → Return to **Clarity System**

---

_This is System 2 of 5: Clarity → Identity → Priority → Execution → Reset_
