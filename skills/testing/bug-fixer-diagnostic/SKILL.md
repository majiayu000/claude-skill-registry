---
name: bug-fixer-diagnostic
description: Advanced diagnostic workflow for bug-fixer agent with mandatory Context7 MCP consultations, Chrome DevTools MCP integration, and systematic root cause analysis across all Clean Architecture layers.
---

# Bug Fixer Diagnostic Skill

**Purpose**: Provide systematic debugging workflow with mandatory Context7 consultations and MCP tool integration for diagnosing and fixing bugs in production code.

---

## 🎯 CORE DEBUGGING PRINCIPLES

### Debugging Philosophy
- **Research First**: ALWAYS consult Context7 before implementing fixes
- **Root Cause Over Symptoms**: Never apply band-aid fixes
- **Minimal Changes**: Surgical fixes only, no refactoring
- **Verification Required**: ALL tests must pass after fix
- **Tools Are Mandatory**: Use MCPs (Chrome DevTools, Supabase) for diagnosis

### When NOT to Use This Skill
- ❌ Adding new features → Use Architect → TDD flow
- ❌ Large refactorings → Discuss with user first
- ❌ Performance optimization → Use separate optimization workflow
- ❌ Code cleanup → Not a bug, suggest improvements only

---

## 📋 4-PHASE DEBUGGING WORKFLOW

### PHASE 0: Bug Classification & Triage

**Objective**: Understand the bug and classify it for appropriate debugging strategy.

#### Step 0.1: Extract Bug Information

**Questions to answer**:
1. **Symptoms**: What is the observable error?
   - Exact error message/stack trace
   - Expected vs actual behavior
   - Frequency (always, intermittent, specific conditions)

2. **Context**: Where does it occur?
   - Which layer? (UI, API, use case, service, database, E2E test)
   - Which file/function?
   - Which environment? (local, staging, production)

3. **Impact**: How severe?
   - Blocking users completely?
   - Data corruption risk?
   - Intermittent/flaky?
   - Visual only?

4. **Reproduction**: Can you reproduce it?
   - Steps to reproduce
   - Consistency (100%, 50%, rare)
   - User role/permissions needed

#### Step 0.2: Classify Bug Type

**Bug categories** (determines debugging strategy):

**1. Validation Bug** (Zod schema issue)
- Symptoms: Validation errors, safeParse failures, type mismatches
- Tools: Context7 for Zod patterns
- Reference: `references/zod-validation.md`

**2. Database Bug** (Supabase/RLS issue)
- Symptoms: Data not appearing, RLS blocks, query errors
- Tools: Supabase MCP to query state, Context7 for RLS patterns
- Reference: `references/supabase-rls.md`

**3. UI Bug** (React/Next.js issue)
- Symptoms: Hydration errors, visual glitches, interaction failures
- Tools: Chrome DevTools MCP, Context7 for React/Next.js
- Reference: `references/nextjs-errors.md`, `references/react-debugging.md`

**4. E2E Bug** (Playwright test failure)
- Symptoms: Test failures, selector issues, timeouts, flaky tests
- Tools: Playwright debugger with --debug, Chrome DevTools MCP
- Reference: `references/playwright-debugging.md`

**5. Integration Bug** (Layer boundary issue)
- Symptoms: Type mismatches, data transformation errors
- Tools: Read relevant files, trace data flow
- Strategy: Check entity schemas, service interfaces, API contracts

**6. Performance Bug** (Slow queries, memory leaks)
- Symptoms: Timeouts, high memory usage, slow responses
- Tools: Supabase advisors, Chrome DevTools performance tab
- Note: May need separate performance optimization workflow

**7. Authorization Bug** (CASL/RLS permission issue)
- Symptoms: UI elements visible but API returns 403, elements hidden when user should have access, "Permission denied" errors
- Tools: Chrome DevTools console for ability inspection, Supabase MCP for RLS testing, Context7 for CASL patterns
- Strategy: Verify CASL + RLS alignment, check ability loading, test permission mapping
- Reference: See **CASL Authorization Debugging** section below

**Deliverable**: Bug classification and initial diagnosis notes

---

### PHASE 1: Deep Diagnosis (RESEARCH FIRST!)

**Objective**: Identify root cause through systematic investigation with Context7 guidance.

**⚠️ MANDATORY**: Never skip Context7 consultation for your bug type.

#### Step 1.1: Context7 Research (ALWAYS FIRST)

**Why Context7 is mandatory**:
- Training data may be outdated
- Breaking changes in library versions
- New best practices emerge
- Known issues and workarounds

**Bug-specific Context7 queries**:

```typescript
// For Validation Bugs (Zod)
await context7.get_library_docs({
  context7CompatibleLibraryID: "/colinhacks/zod",
  topic: "safeParse error handling issues flatten custom errors debugging",
  tokens: 3000
})

// For Database Bugs (Supabase RLS)
await context7.get_library_docs({
  context7CompatibleLibraryID: "/supabase/supabase",
  topic: "RLS policies debugging circular errors authentication performance",
  tokens: 3000
})

// For UI Bugs (Next.js)
await context7.get_library_docs({
  context7CompatibleLibraryID: "/vercel/next.js",
  topic: "server components hydration errors client boundaries debugging",
  tokens: 2500
})

// For UI Bugs (React)
await context7.get_library_docs({
  context7CompatibleLibraryID: "/facebook/react",
  topic: "hooks dependencies useEffect memory leaks debugging",
  tokens: 2500
})

// For Authorization Bugs (CASL)
await context7.get_library_docs({
  context7CompatibleLibraryID: "/stalniy/casl",
  topic: "ability can cannot conditions debugging rules checking",
  tokens: 2500
})

// For E2E Bugs (Playwright)
await context7.get_library_docs({
  context7CompatibleLibraryID: "/microsoft/playwright",
  topic: "debugging test failures selectors wait for timeout race conditions",
  tokens: 3000
})

// For Unit Test Bugs (Vitest)
await context7.get_library_docs({
  context7CompatibleLibraryID: "/vitest-dev/vitest",
  topic: "debugging test failures error handling mock issues async",
  tokens: 3000
})
```

**Review Context7 output for**:
- ✅ Latest error handling patterns
- ✅ Known issues and workarounds
- ✅ Best practices for this specific case
- ✅ Breaking changes in recent versions
- ✅ Common mistakes to avoid

#### Step 1.2: Layer-Specific Diagnosis

**For Validation Bugs (Entities/Zod)**:

```typescript
// 1. Read the problematic schema
const entityFile = await Read('app/src/features/[feature]/entities.ts')

// 2. Check usage in use cases - look for .parse() vs .safeParse()
await Grep({
  pattern: "EntitySchema\\.parse",
  path: "app/src/features/[feature]/use-cases",
  output_mode: "content",
  "-n": true
})

// 3. Common issues to check:
// ❌ Using .parse() instead of .safeParse()? (throws instead of returning result)
// ❌ Error messages not clear?
// ❌ Refinement logic incorrect?
// ❌ Type mismatch between schema and usage?
```

**Best practices from Context7**:
- ✅ Always use `.safeParse()` for controllable error handling
- ✅ Use `.flatten()` on errors for better structure
- ✅ Create schemas inside components for translation access
- ✅ Check for circular refinements

**For Database Bugs (Services/Supabase)**:

```typescript
// 1. Query actual database state
const data = await supabase.execute_sql({
  query: `SELECT * FROM [table] WHERE [condition]`
})

// 2. Check RLS policies
const policies = await supabase.execute_sql({
  query: `SELECT * FROM pg_policies WHERE tablename = '[table]'`
})

// 3. Test RLS with specific user context
await supabase.execute_sql({
  query: `
    SET LOCAL ROLE authenticated;
    SET LOCAL request.jwt.claims.sub = '[test-user-id]';
    SELECT * FROM [table];  -- Should return expected data
  `
})

// 4. Check for circular policy references (common issue)
// Look for policies that reference the same table they're applied to

// 5. Check logs for errors
const logs = await supabase.get_logs({
  project_id: "project-id",
  service: "postgres"
})

// 6. Run security advisors
const advisors = await supabase.get_advisors({
  project_id: "project-id",
  type: "security"
})
```

**Common RLS issues** (from Context7):
- ❌ Circular policies (policy references same table)
- ❌ Missing auth.uid() checks
- ❌ Not scoping to authenticated role (TO authenticated)
- ❌ Complex joins in RLS (performance killer)

**Best practice** (from Context7):
```sql
-- ✅ GOOD: No circular reference
CREATE POLICY "access_policy" ON tasks
  FOR SELECT
  TO authenticated
  USING (
    organization_id IN (
      SELECT organization_id
      FROM user_organizations
      WHERE user_id = (SELECT auth.uid())  -- No join back to tasks!
    )
  );

-- ❌ BAD: Circular reference
CREATE POLICY "bad_policy" ON tasks
  FOR SELECT
  USING (
    auth.uid() IN (
      SELECT user_id FROM team_user
      WHERE team_user.team_id = tasks.team_id  -- CIRCULAR! References tasks
    )
  );
```

**For UI Bugs (Components/React)**:

```typescript
// 1. Use Chrome DevTools MCP to inspect live state
await mcp__chrome_devtools__new_page()
await mcp__chrome_devtools__navigate_page({
  url: "http://localhost:3000/problematic-page"
})

// 2. Take snapshot for visual inspection
const snapshot = await mcp__chrome_devtools__take_snapshot()

// 3. Evaluate JavaScript to check state
const state = await mcp__chrome_devtools__evaluate_script({
  script: `
    return {
      errors: document.querySelector('.error')?.textContent,
      consoleErrors: [...console.memory || []],
      hydrationErrors: window.__NEXT_DATA__?.props?.pageProps?.errors
    }
  `
})

// 4. Check for hydration mismatches (Next.js specific)
// Look for console warnings: "Hydration failed because..."
// Common cause: Server/client render different content

// 5. Consult Context7 for React patterns
await context7.get_library_docs({
  context7CompatibleLibraryID: "/facebook/react",
  topic: "hooks useEffect dependencies errors hydration debugging",
  tokens: 2500
})
```

**Common React/Next.js issues** (from Context7):
- ❌ useEffect missing dependencies
- ❌ Server/client rendering mismatch (hydration error)
- ❌ Race conditions (component unmounts before async completes)
- ❌ Incorrect 'use client' directive placement

**Best practices from Context7**:
```typescript
// ✅ Cleanup on unmount to prevent race conditions
useEffect(() => {
  let cancelled = false

  fetchData().then(result => {
    if (!cancelled) setData(result)
  })

  return () => { cancelled = true }
}, [])

// ❌ Race condition - no cleanup
useEffect(() => {
  fetchData().then(setData) // Fails if component unmounts!
}, [])
```

**For E2E Test Failures (Playwright)**:

```bash
# 1. Run with Playwright Inspector for step-through debugging
npx playwright test failing-test.spec.ts:42 --debug

# 2. Run with verbose API logs
DEBUG=pw:api npx playwright test failing-test.spec.ts

# 3. Generate trace for analysis
npx playwright test failing-test.spec.ts --trace on

# 4. View trace after failure
npx playwright show-trace trace.zip

# 5. Run in UI mode for interactive debugging
npx playwright test --ui
```

```typescript
// Use Chrome DevTools MCP for live inspection
await mcp__chrome_devtools__new_page()
await mcp__chrome_devtools__navigate_page({
  url: "http://localhost:3000/test-page"
})

// Wait for problematic element
await mcp__chrome_devtools__wait_for({
  selector: ".expected-element",
  timeout: 5000
})

// Take screenshot of current state
await mcp__chrome_devtools__take_screenshot()
```

**Common Playwright issues** (from Context7):
- ❌ Using brittle CSS selectors (`.button.primary.large`)
- ❌ Not using web-first assertions (`toBeVisible()`)
- ❌ Manual checks instead of automatic retries
- ❌ Race conditions with async content

**Best practices from Context7**:
```typescript
// ✅ GOOD: Web-first assertion (auto-retries)
await expect(page.getByText('welcome')).toBeVisible()

// ❌ BAD: Manual check (no retry)
expect(await page.getByText('welcome').isVisible()).toBe(true)

// ✅ GOOD: Semantic selector (robust)
await page.getByRole('button', { name: 'Submit' })

// ❌ BAD: Brittle CSS selector
await page.click('.btn-primary-submit-form-action')
```

#### Step 1.3: Root Cause Identification

**Document findings**:

```markdown
## Root Cause Analysis

**Bug Type**: [Validation/Database/UI/E2E/Integration/Performance]

**Layer Affected**: [Entities/Use Cases/Services/Components/E2E]

**Root Cause**:
[Clear explanation of WHY the bug occurs, not just what]

**Evidence**:
1. [Finding from Context7 documentation]
2. [Finding from Chrome DevTools inspection]
3. [Finding from Supabase query]
4. [Finding from Playwright debugger]
5. [Finding from code analysis]

**Why It Wasn't Caught**:
- Missing test coverage?
- Edge case not considered?
- Environment-specific issue?
- Timing/race condition?

**Impact Scope**:
- Which users affected?
- Which features broken?
- Data integrity risk?
```

**Deliverable**: Complete root cause analysis document

---

### PHASE 2: Research-Driven Fix Implementation

**Objective**: Apply minimal, targeted fix using latest patterns from Context7.

**⚠️ CRITICAL**: Only fix AFTER understanding root cause and verifying latest patterns.

#### Step 2.1: Verify Latest Fix Patterns (Context7)

```typescript
// NEVER use outdated patterns from training data
// ALWAYS verify latest approach with Context7

// Example: Fixing Zod validation
await context7.get_library_docs({
  context7CompatibleLibraryID: "/colinhacks/zod",
  topic: "safeParse error handling best practices latest version",
  tokens: 2000
})

// Review to ensure fix follows:
// ✅ Latest API patterns
// ✅ Recommended best practices
// ✅ No deprecated methods
// ✅ Optimal performance approach
```

#### Step 2.2: Implement Minimal Fix

**Principle**: Make the SMALLEST change that fixes the root cause.

**Example Fix Patterns** (validated with Context7):

**Validation Bug Fix**:
```typescript
// ❌ BEFORE (using .parse - throws)
export async function createEntity(input: unknown) {
  const validated = EntityCreateSchema.parse(input) // Throws!
  return service.create(validated)
}

// ✅ AFTER (using .safeParse - returns result)
export async function createEntity(input: unknown) {
  const result = EntityCreateSchema.safeParse(input)

  if (!result.success) {
    // Use flatten() for better error structure (Context7 pattern)
    const errors = result.error.flatten()
    throw new ValidationError('Invalid input', errors)
  }

  return service.create(result.data)
}
```

**RLS Policy Bug Fix**:
```sql
-- ❌ BEFORE (circular policy - slow!)
CREATE POLICY "bad_policy" ON tasks
  FOR SELECT
  USING (
    auth.uid() IN (
      SELECT user_id FROM team_user
      WHERE team_user.team_id = tasks.team_id  -- CIRCULAR!
    )
  );

-- ✅ AFTER (no circular reference - fast!)
CREATE POLICY "fixed_policy" ON tasks
  FOR SELECT
  TO authenticated
  USING (
    organization_id IN (
      SELECT organization_id
      FROM user_organizations
      WHERE user_id = (SELECT auth.uid())  -- No join to tasks!
    )
  );
```

**UI Race Condition Fix**:
```typescript
// ❌ BEFORE (race condition)
export function Component() {
  const [data, setData] = useState(null)

  useEffect(() => {
    fetchData().then(setData) // Race condition if component unmounts!
  }, [])

  return <div>{data?.name}</div>
}

// ✅ AFTER (cleanup on unmount - Context7 pattern)
export function Component() {
  const [data, setData] = useState(null)

  useEffect(() => {
    let cancelled = false

    fetchData().then(result => {
      if (!cancelled) setData(result)
    })

    return () => { cancelled = true }
  }, [])

  return <div>{data?.name}</div>
}
```

**E2E Test Selector Fix**:
```typescript
// ❌ BEFORE (brittle selector - Context7 anti-pattern)
await page.click('.button-primary') // Breaks if CSS changes

// ✅ AFTER (semantic selector - Context7 best practice)
await page.getByRole('button', { name: 'Submit' }) // Robust

// OR (data-testid - also recommended)
await page.click('[data-testid="submit-button"]') // Explicit test hook
```

#### Step 2.3: Add Defensive Error Handling

If bug was caused by missing error handling, add proper guards:

```typescript
// Add null checks
if (!user) {
  throw new NotFoundError('User not found')
}

// Add type guards
if (typeof data.email !== 'string') {
  throw new ValidationError('Email must be a string')
}

// Add try-catch for external calls
try {
  await externalApi.call()
} catch (error) {
  logger.error('External API failed', { error })
  throw new IntegrationError('Failed to contact external service', { cause: error })
}
```

**Deliverable**: Implemented fix with defensive guards

---

### PHASE 3: Comprehensive Verification

**Objective**: Ensure fix works and no regressions introduced.

**⚠️ CRITICAL**: NEVER consider a bug fixed until ALL verification passes.

#### Step 3.1: Run Affected Tests

```bash
# 1. Run unit tests for affected layer
npm run test app/src/features/[feature]/

# 2. Run integration tests
npm run test app/src/app/api/[feature]/

# 3. Run ALL E2E tests (regression check)
npm run test:e2e

# 4. Run type checking
npm run typecheck

# 5. Run linting
npm run lint
```

**All tests must pass**. If any fail:
- Investigate if test revealed another bug
- Fix the newly discovered bug
- Re-run full test suite

#### Step 3.2: Manual Verification

**For UI bugs**:
```typescript
// 1. Use Chrome DevTools MCP to verify fix
await mcp__chrome_devtools__new_page()
await mcp__chrome_devtools__navigate_page({
  url: "http://localhost:3000/fixed-page"
})

// 2. Reproduce original bug scenario
await mcp__chrome_devtools__click({ selector: "button" })

// 3. Verify fix worked
const state = await mcp__chrome_devtools__evaluate_script({
  script: "return document.querySelector('.error') === null"
})

// 4. Take screenshot for comparison
await mcp__chrome_devtools__take_screenshot()
```

**For database bugs**:
```typescript
// 1. Verify RLS policy works correctly
await supabase.execute_sql({
  query: `
    SET LOCAL ROLE authenticated;
    SET LOCAL request.jwt.claims.sub = '[test-user-id]';
    SELECT * FROM tasks;  -- Should only return user's tasks
  `
})

// 2. Check security advisors again
await supabase.get_advisors({
  project_id: "project-id",
  type: "security"
})
```

**For E2E bugs**:
```bash
# 1. Run fixed test in debug mode
npx playwright test fixed-test.spec.ts --debug

# 2. Run in UI mode to visually verify
npx playwright test fixed-test.spec.ts --ui

# 3. Run multiple times to check for flakiness
for i in {1..10}; do npx playwright test fixed-test.spec.ts; done
```

#### Step 3.3: Regression Check

**Verify no new issues**:

1. **Run FULL Test Suite**:
   ```bash
   npm run test
   npm run test:e2e
   ```

2. **Check All Affected Flows**:
   - If you fixed validation, test ALL CRUD operations
   - If you fixed RLS, test with different user roles
   - If you fixed UI, test on different browsers/devices

3. **Performance Check**:
   - Did fix introduce performance regression?
   - Use Chrome DevTools Performance tab
   - Use Supabase EXPLAIN ANALYZE for queries

4. **Security Check**:
   - Did fix introduce security vulnerability?
   - Run Supabase security advisors
   - Verify RLS still enforces isolation

**Deliverable**: All tests passing, no regressions detected

---

### PHASE 4: Documentation & Prevention

**Objective**: Document fix and recommend preventive measures.

#### Step 4.1: Document the Fix

```markdown
## Bug Fix Report

**Bug ID**: [Reference to issue/ticket if applicable]

**Summary**: [One sentence description]

**Root Cause**:
[Detailed explanation of why bug occurred]

**Files Changed**:
- `path/to/file1.ts` (Lines X-Y)
- `path/to/file2.ts` (Lines X-Y)

**Fix Applied**:
[Explanation of what was changed and why]

**Research Sources**:
- Context7: [Library and topic searched]
- Chrome DevTools: [Findings from inspection]
- Supabase: [Database queries/logs reviewed]
- Playwright: [Debugging commands used]

**Verification**:
- ✅ Unit tests passing
- ✅ Integration tests passing
- ✅ E2E tests passing
- ✅ Manual testing completed
- ✅ No regression detected

**Prevention**:
[How to prevent this bug in future]
- [ ] Add missing test coverage?
- [ ] Update validation schema?
- [ ] Improve error messages?
- [ ] Add documentation?
```

#### Step 4.2: Suggest Preventive Measures

**Recommendations to user**:

1. **Test Coverage Gap**:
   "This bug wasn't caught because we lack test coverage for [scenario].
   I recommend adding tests to prevent regression."

2. **Pattern Improvement**:
   "According to latest Context7 docs, the recommended pattern is [X].
   Consider refactoring similar code to follow this pattern."

3. **Monitoring**:
   "Add logging/monitoring for this scenario to catch future issues early."

4. **Documentation**:
   "This edge case should be documented in [location] to help future developers."

**Deliverable**: Complete bug fix report with prevention recommendations

---

## 🚨 COMMON ANTI-PATTERNS TO AVOID

### ❌ DON'T: Fix Without Research
```typescript
// ❌ WRONG: Fixing based on assumptions
// "I think this is the problem, let me try this fix"
export function createEntity(input: any) {  // Using 'any' to bypass error
  // ...
}
```

```typescript
// ✅ CORRECT: Research first, then fix
// 1. Consulted Context7 for Zod patterns
// 2. Identified .parse() vs .safeParse() issue
// 3. Applied recommended pattern
export function createEntity(input: unknown) {
  const result = EntityCreateSchema.safeParse(input)
  if (!result.success) {
    throw new ValidationError('Invalid input', result.error.flatten())
  }
  return service.create(result.data)
}
```

### ❌ DON'T: Skip Verification
```bash
# ❌ WRONG: "Looks good, done!"
# Fix applied, no tests run
```

```bash
# ✅ CORRECT: Comprehensive verification
npm run test                    # All unit tests
npm run test:e2e                # All E2E tests
npm run typecheck               # Type safety
npx playwright test --ui        # Visual verification
```

### ❌ DON'T: Ignore Chrome DevTools for UI Bugs
```typescript
// ❌ WRONG: Guessing what's wrong with UI
// "Maybe it's a CSS issue? Let me change some styles"
```

```typescript
// ✅ CORRECT: Use Chrome DevTools MCP to inspect
await mcp__chrome_devtools__new_page()
await mcp__chrome_devtools__navigate_page({ url: "..." })
const snapshot = await mcp__chrome_devtools__take_snapshot()
// Now I can SEE the actual problem!
```

### ❌ DON'T: Overengineer the Fix
```typescript
// ❌ WRONG: Complex refactoring for simple bug
// Changing entire architecture to fix a typo
```

```typescript
// ✅ CORRECT: Minimal fix
// Change 'organizaton_id' → 'organization_id' (typo fix)
```

### ❌ DON'T: Skip Root Cause Analysis
```typescript
// ❌ WRONG: Band-aid fix
try {
  buggyFunction()
} catch {
  // Ignore error (just hiding the problem!)
}
```

```typescript
// ✅ CORRECT: Fix root cause
// Identified that buggyFunction fails due to null input
// Added null check at source instead of catching error
if (input === null) {
  throw new ValidationError('Input cannot be null')
}
validFunction(input)
```

---

## ✅ QUALITY CRITERIA

Your bug fix is complete when:

### Research Quality
- ✅ Context7 consulted for ALL library-related fixes
- ✅ Chrome DevTools MCP used for ALL UI/E2E bugs
- ✅ Supabase MCP used for ALL database bugs
- ✅ Playwright debugger used for ALL E2E test failures
- ✅ Root cause clearly identified and documented

### Fix Quality
- ✅ Minimal change to fix root cause
- ✅ No over-engineering or unnecessary refactoring
- ✅ Follows latest patterns from Context7
- ✅ Defensive error handling added
- ✅ Type-safe (no `any` types)
- ✅ Clear code comments explaining fix

### Verification Quality
- ✅ ALL unit tests pass
- ✅ ALL integration tests pass
- ✅ ALL E2E tests pass
- ✅ Manual verification completed
- ✅ No regression detected
- ✅ Performance not degraded

### Documentation Quality
- ✅ Root cause documented
- ✅ Fix approach explained
- ✅ Research sources cited
- ✅ Prevention recommendations provided
- ✅ Changed files clearly listed

---

## 🔐 CASL AUTHORIZATION DEBUGGING

**When to use**: Authorization bug (type 7) - UI elements visible but API returns 403, elements hidden when user should have access, "Permission denied" errors.

### Symptoms of CASL Bugs

1. **UI visible, API rejects**:
   - User sees "Delete" button
   - Click triggers API call
   - API returns 403 Forbidden
   - Root cause: CASL says YES, RLS says NO (RLS is stricter)

2. **UI hidden, should be visible**:
   - User should have permission
   - Button/element completely missing from DOM
   - Root cause: CASL ability not loaded correctly, or wrong logic in `defineAbilitiesFor()`

3. **Inconsistent behavior**:
   - Works for Owner, fails for normal users
   - Works in one workspace, fails in another
   - Root cause: Conditional permissions not working, workspace context incorrect

### Diagnostic Steps

#### Step 1: Inspect Ability in Browser

**Use Chrome DevTools console to inspect user's current ability**:

```javascript
// In browser console (when on the page with issue)
// Add temporary logging to component
console.log('Current ability:', ability);
console.log('Can delete board?', ability.can('delete', 'Board'));
console.log('All rules:', ability.rules);
```

**What to look for**:
- Is ability loaded? (not null/undefined)
- Does `ability.can('action', 'Subject')` return expected value?
- Are there any rules at all? (empty rules = no permissions loaded)

#### Step 2: Verify Ability Loading

**Check if `loadUserAbility()` is being called**:

```typescript
// Look for AbilityProvider in layout/page
// app/(main)/{feature}/layout.tsx

// Should have:
const ability = await loadUserAbility(userId, workspaceId);

// Common mistakes:
// ❌ Not awaiting loadUserAbility()
// ❌ Wrong userId or workspaceId
// ❌ loadUserAbility() not called at all
```

**Verify data sources**:
- User object correct? Check user.id
- Workspace object correct? Check workspace.id, workspace.owner_id
- Permissions loaded? Check permissions array length

#### Step 3: Compare CASL vs RLS

**Read both implementations**:

```typescript
// 1. Read CASL logic
Read('features/{feature}/abilities/defineAbility.ts')

// 2. Query RLS policies
supabase_mcp.execute_sql({
  query: "SELECT * FROM pg_policies WHERE schemaname = 'public' AND tablename = '{table}'"
})
```

**Look for misalignment**:
- CASL allows Owner → RLS should too
- CASL allows permission → RLS should check same permission
- CASL has Super Admin restrictions → RLS should too

#### Step 4: Test Permission Mapping

**Check resource-to-subject mapping**:

```typescript
// In defineAbilitiesFor(), find mapResourceToSubject()
function mapResourceToSubject(resource: string): Subjects {
  const mapping: Record<string, Subjects> = {
    'boards': 'Board',  // DB table → CASL subject
    'cards': 'Card',
  };
  return mapping[resource] || 'all';
}

// Common mistakes:
// ❌ Wrong mapping ('boards' → 'Boards' - typo!)
// ❌ Missing mapping (permission exists but no mapping)
// ❌ Wrong subject case ('board' vs 'Board')
```

**Verify permission names**:
```sql
-- Query actual permissions in database
SELECT full_name FROM permissions WHERE user_id = '{userId}';

-- Compare to CASL mapping:
// 'boards.create' → can('create', 'Board')
// 'boards.delete' → can('delete', 'Board')
```

### Common CASL Bugs and Fixes

#### Bug 1: AbilityContext Not Provided

**Symptom**: `Error: useAppAbility must be used within AbilityProvider`

**Fix**:
```typescript
// ❌ BEFORE - Component outside provider
export default function Page() {
  return <BoardActions />; // Uses useAppAbility() → ERROR
}

// ✅ AFTER - Wrap with provider in layout
export default async function Layout({ children }) {
  const ability = await loadUserAbility(userId, workspaceId);
  return (
    <AbilityProvider ability={ability}>
      {children}
    </AbilityProvider>
  );
}
```

#### Bug 2: Typo in Action/Subject Names

**Symptom**: User has permission but UI still hidden

**Diagnosis**:
```typescript
// Check CASL check:
ability.can('delete', 'Board') // FALSE

// But permission exists:
{ full_name: 'boards.delete' }

// Problem: mapResourceToSubject has typo
const mapping = {
  'boards': 'Boards', // ❌ Should be 'Board' (singular!)
};
```

**Fix**:
```typescript
// ✅ CORRECT - Singular, PascalCase
const mapping = {
  'boards': 'Board',
  'cards': 'Card',
  'comments': 'Comment',
};
```

#### Bug 3: Stale Ability (Permissions Changed)

**Symptom**: User was granted permission but UI still doesn't update

**Root cause**: Ability loaded once on page load, not reactive to permission changes

**Fix**:
```typescript
// ✅ Option 1: Reload ability when permissions change
const queryClient = useQueryClient();
await updatePermissions(userId, newPermissions);
queryClient.invalidateQueries(['ability']); // If ability in React Query

// ✅ Option 2: Navigate to refresh server component
router.refresh(); // For Next.js App Router
```

#### Bug 4: CASL + RLS Mismatch

**Symptom**: Button visible, API returns 403

**Diagnosis**:
```typescript
// CASL says YES:
if (user.id === workspace.owner_id) {
  can('delete', 'Organization'); // ❌ Owner CAN delete
}

// But PRD says:
// "Super Admin restrictions: Cannot delete Organization"

// RLS correctly blocks:
CREATE POLICY "block_org_delete" ON organizations
  FOR DELETE USING (false); // ✅ Nobody can delete (even Owner)
```

**Fix**:
```typescript
// ✅ Align CASL with PRD and RLS
if (user.id === workspace.owner_id) {
  can('manage', 'all');
  cannot('delete', 'Organization'); // Add restriction
}
```

### CASL Debugging Checklist

- [ ] ✅ Inspect ability in browser console (`ability.can()`, `ability.rules`)
- [ ] ✅ Verify AbilityProvider wraps components
- [ ] ✅ Check loadUserAbility() is called with correct user/workspace
- [ ] ✅ Verify permissions array has data
- [ ] ✅ Compare defineAbilitiesFor() logic to RLS policies
- [ ] ✅ Check mapResourceToSubject() mappings (singular, PascalCase)
- [ ] ✅ Verify action names match ('create' not 'add')
- [ ] ✅ Test Owner bypass logic
- [ ] ✅ Test Super Admin restrictions
- [ ] ✅ Test normal user permission mapping
- [ ] ✅ Verify no typos in subject names

### Coordination with Supabase Agent

If CASL and RLS are misaligned:
1. **Determine correct logic** from PRD
2. **Update CASL** if Implementer was wrong
3. **Update RLS** if Supabase Agent was wrong
4. **Ask Architect** if PRD is unclear

---

## 📚 REFERENCE DOCUMENTS

Load these on demand when needed:

1. **`references/playwright-debugging.md`** - Playwright debugging patterns
2. **`references/vitest-debugging.md`** - Vitest test debugging
3. **`references/zod-validation.md`** - Zod schema debugging
4. **`references/supabase-rls.md`** - RLS policy debugging
5. **`references/nextjs-errors.md`** - Next.js error patterns
6. **`references/react-debugging.md`** - React debugging patterns

---

## 🎯 REMEMBER

1. **Research is MANDATORY** - Never fix without consulting Context7
2. **Chrome DevTools for UI** - Use MCP to inspect live browser state
3. **Playwright for E2E** - Use debugger for test failures
4. **Minimal fixes only** - Don't refactor, just fix the bug
5. **Verify everything** - All tests must pass, no exceptions
6. **Document thoroughly** - Future developers need to understand
7. **Root cause first** - Never apply band-aid fixes
8. **Layer boundaries** - Respect Clean Architecture even in fixes

**Your success is measured by**:
- ✅ **Research**: Did you consult all available documentation?
- ✅ **Diagnosis**: Did you identify the true root cause?
- ✅ **Fix**: Is it minimal, targeted, and follows best practices?
- ✅ **Verification**: Do ALL tests pass with no regression?

---

**YOU ARE THE BUG DETECTIVE. YOUR FIXES ARE SURGICAL, RESEARCHED, AND VERIFIED.**
