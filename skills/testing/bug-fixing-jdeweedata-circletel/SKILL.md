---
name: Bug Fixing Assistant
description: Systematic debugging workflow for CircleTel - analyzes errors, identifies root causes, proposes fixes, and validates solutions with tests
version: 1.0.0
dependencies: python>=3.8, typescript>=5.0
---

# Bug Fixing Assistant Skill

A comprehensive skill for systematically debugging and fixing software bugs in the CircleTel codebase. Uses structured workflows to identify root causes, propose targeted fixes, and validate solutions.

## When This Skill Activates

This skill automatically activates when you:
- Encounter runtime errors or exceptions
- Debug failing tests or build errors
- Investigate performance issues or memory leaks
- Troubleshoot API failures or timeout issues
- Fix infinite loading states or UI bugs
- Resolve database query problems
- Debug authentication or RLS policy issues
- Investigate TypeScript type errors

**Keywords**: bug, error, debug, fix, issue, broken, failing, crash, exception, timeout, undefined, null, 500 error, 403 error

## Core Debugging Strategy

### Phase 1: Understand the Problem (5-10 minutes)

**Don't jump to solutions.** Invest time understanding the failure mode first.

#### Step 1.1: Gather Evidence

Collect all relevant information:
- **Error messages**: Full stack traces, console logs, error codes
- **Reproduction steps**: Exact sequence to trigger the bug
- **Environment**: Browser, Node version, deployment environment
- **User impact**: How many users affected? Critical or minor?
- **Recent changes**: What was deployed recently?

#### Step 1.2: Identify Failure Modes

Ask Claude to outline possible scenarios:

```
"What could cause [symptom] in [context]?"

Examples:
- "What could cause pagination to silently drop results in Next.js 15?"
- "Why might a Supabase RLS policy block authenticated requests?"
- "What scenarios cause React components to re-render infinitely?"
```

#### Step 1.3: Form Hypotheses

Generate testable hypotheses ranked by likelihood:

```
"Given this error: [error message]
And this context: [relevant code/logs]
What are the top 3 most likely root causes, ranked by probability?"
```

### Phase 2: Investigate (15-30 minutes)

#### Step 2.1: Reproduce Locally

**Always reproduce first** before attempting fixes:

```bash
# CircleTel development setup
npm run dev:memory

# Check console for errors
# Navigate to affected page/feature
# Follow exact reproduction steps
```

Document the exact steps:
1. Navigate to [page]
2. Click [button]
3. Observe [unexpected behavior]

#### Step 2.2: Add Instrumentation

Add strategic logging to narrow down the issue:

```typescript
console.log('[DEBUG] Function entry:', { params })
console.log('[DEBUG] Before API call:', { payload })
console.log('[DEBUG] API response:', { data, error })
console.log('[DEBUG] State update:', { oldState, newState })
```

**Use DEBUG prefix** to easily filter logs.

#### Step 2.3: Isolate the Problem

Use binary search to narrow scope:
- Comment out half the code
- Does bug still occur?
- If yes, bug is in remaining half
- If no, bug is in commented half
- Repeat until isolated

### Phase 3: Analyze Root Cause (10-20 minutes)

#### Step 3.1: Review Related Code

Ask Claude to analyze the relevant code:

```
"Review this code for potential issues:

[paste code]

Context: [describe the bug]

Look for:
- Race conditions
- Missing error handling
- Incorrect state updates
- Type mismatches
- Missing null checks
```

#### Step 3.2: Check Architecture Patterns

For complex bugs, analyze architectural issues:

```
"Analyze this for architectural problems:

[paste relevant code sections]

Consider:
- Concurrency issues (Promise.all, async/await)
- State management problems (stale closures, derived state)
- Lifecycle issues (useEffect dependencies)
- Memory leaks (event listeners, timers)
```

#### Step 3.3: Identify CircleTel-Specific Patterns

Common CircleTel bug patterns:

**1. Infinite Loading States**
- **Cause**: Missing finally block in async callbacks
- **Fix**: Always set loading=false in finally block
- **Example**: `components/providers/CustomerAuthProvider.tsx:64-76`

**2. RLS Policy Blocking API Access**
- **Cause**: Missing service role policy
- **Fix**: Add service_role policy to table
- **Example**: See Database Migration Skill

**3. Next.js 15 Params Type Error**
- **Cause**: Async params not awaited
- **Fix**: `const { id } = await context.params`
- **Example**: See CLAUDE.md TypeScript Patterns

**4. Memory Heap Overflow**
- **Cause**: Large TypeScript compilation
- **Fix**: Use `npm run build:memory`
- **Example**: See package.json scripts

### Phase 4: Propose Fix (5-15 minutes)

#### Step 4.1: Generate Targeted Solution

Ask Claude for fix proposals:

```
"Given this root cause: [analysis]

Propose a minimal fix that:
1. Resolves the issue
2. Matches CircleTel coding style
3. Doesn't introduce new bugs
4. Includes error handling

Show the exact code changes needed.
```

#### Step 4.2: Review for Side Effects

Check if fix affects other areas:

```
"This fix changes [component/function]:

[paste proposed fix]

What other parts of the codebase might be affected?
Search for:
- Files that import this
- Components that use this hook
- API routes that depend on this
```

#### Step 4.3: Apply Fix Locally

Make the change in your local environment:

```typescript
// Example: Fix infinite loading state
useEffect(() => {
  const callback = async () => {
    try {
      const data = await fetchData()
      setState(data)
    } catch (error) {
      console.error('Failed:', error)
      setState(null)
    } finally {
      setLoading(false) // ✅ Always executes
    }
  }
  onAuthStateChange(callback)
}, [])
```

### Phase 5: Validate (10-20 minutes)

#### Step 5.1: Test the Fix

**Validation Checklist**:
- [ ] Bug no longer reproduces
- [ ] Original functionality still works
- [ ] No new errors in console
- [ ] Type check passes: `npm run type-check`
- [ ] Build succeeds: `npm run build:memory`
- [ ] Related features still work

#### Step 5.2: Write Tests

Ask Claude to generate tests:

```
"Generate a test that verifies this fix:

Bug: [description]
Fix: [code change]
Expected behavior: [what should happen now]

Use [testing framework] and follow CircleTel patterns.
```

#### Step 5.3: Run Full Test Suite

```bash
# Type check
npm run type-check

# Build test
npm run build:memory

# E2E tests (if applicable)
npm run test:e2e

# Manual testing checklist
# - Test happy path
# - Test error scenarios
# - Test edge cases
```

## Bug Type Templates

### Template 1: Runtime Error

**Symptom**: Application crashes with error message

**Investigation Prompt**:
```
"Analyze this runtime error:

Error: [error message]
Stack trace: [stack trace]
File: [file:line]

1. What is the immediate cause?
2. What conditions trigger this?
3. Is this a timing issue, null reference, or logic error?
4. What's the safest fix?
```

### Template 2: Infinite Loop/Loading

**Symptom**: UI stuck in loading state or infinite re-renders

**Investigation Prompt**:
```
"Debug this infinite loop/loading issue:

Component: [component name]
Code: [paste useEffect or relevant code]

Analyze for:
1. Missing dependency array
2. State updates triggering re-renders
3. Missing finally block
4. Async callback error handling
```

### Template 3: API/Database Error

**Symptom**: API calls fail or return unexpected data

**Investigation Prompt**:
```
"Troubleshoot this API/database issue:

API: [endpoint]
Error: [error message or behavior]
Request: [request payload]
Response: [response or error]

Check for:
1. RLS policy blocking access
2. Missing authentication
3. Incorrect query parameters
4. Type mismatches in payload
```

### Template 4: Type Error

**Symptom**: TypeScript compilation fails

**Investigation Prompt**:
```
"Fix this TypeScript error:

Error: [type error message]
File: [file:line]
Code: [relevant code]

1. What type is expected vs provided?
2. Is this a Next.js 15 async params issue?
3. Is this a missing type definition?
4. What's the minimal fix?
```

### Template 5: Performance Issue

**Symptom**: Slow page load, high memory usage, or lag

**Investigation Prompt**:
```
"Analyze this performance issue:

Symptom: [slow loading, memory leak, etc.]
Context: [page, component, or operation]
Metrics: [load time, memory usage]

Investigate:
1. Unnecessary re-renders
2. Large data sets without pagination
3. Missing memoization
4. Inefficient database queries
5. Missing indexes
```

## CircleTel-Specific Debugging Patterns

### Pattern 1: Customer Dashboard Infinite Loading

**Common Locations**:
- `app/dashboard/page.tsx`
- `components/providers/CustomerAuthProvider.tsx`
- `app/dashboard/*/page.tsx`

**Root Cause**: Missing finally block in async auth callback

**Fix Pattern**:
```typescript
useEffect(() => {
  const callback = async () => {
    try {
      // Fetch data
    } catch (error) {
      // Handle error
    } finally {
      setLoading(false) // ✅ CRITICAL
    }
  }
  onAuthStateChange(callback)
}, [])
```

**Reference**: `components/providers/CustomerAuthProvider.tsx:64-76`

### Pattern 2: RLS Policy Blocking API Routes

**Common Error**: `new row violates row-level security policy`

**Root Cause**: Missing service role policy on table

**Fix Pattern**:
```sql
CREATE POLICY "service_role_all" ON public.table_name
  FOR ALL
  USING (auth.jwt() ->> 'role' = 'service_role');
```

**Debug Steps**:
1. Check RLS policies: `SELECT * FROM pg_policies WHERE tablename = 'table_name'`
2. Verify API uses service role client
3. Add service role policy if missing

### Pattern 3: Next.js 15 Async Params Error

**Common Error**: `Type 'Promise<{ id: string }>' is not assignable to type '{ id: string }'`

**Root Cause**: Next.js 15 made params async

**Fix Pattern**:
```typescript
// ❌ OLD (breaks in Next.js 15)
export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  const { id } = params
}

// ✅ NEW (Next.js 15 compatible)
export async function GET(
  request: NextRequest,
  context: { params: Promise<{ id: string }> }
) {
  const { id } = await context.params
}
```

### Pattern 4: Supabase Client Type Mismatch

**Common Error**: `Cannot read properties of undefined (reading 'from')`

**Root Cause**: Wrong Supabase client for context

**Fix Pattern**:
```typescript
// ✅ Server-side (API routes)
import { createClient } from '@/lib/supabase/server'
const supabase = await createClient() // Service role

// ✅ Client-side (components)
import { createClient } from '@/lib/supabase/client'
const supabase = createClient() // Anonymous with RLS
```

### Pattern 5: Memory Heap Overflow

**Common Error**: `JavaScript heap out of memory`

**Root Cause**: Large TypeScript compilation or build

**Fix Pattern**:
```bash
# Use memory-optimized commands
npm run dev:memory          # 8GB heap
npm run type-check:memory   # 4GB heap
npm run build:memory        # 8GB heap
```

## Debugging Workflows by Category

### Workflow A: Frontend UI Bug

1. **Reproduce in browser**
   - Open DevTools console
   - Check for errors
   - Note exact steps

2. **Check React DevTools**
   - Inspect component props
   - Check state values
   - Look for re-render count

3. **Add console.log strategically**
   ```typescript
   console.log('[DEBUG] Component render:', { props, state })
   console.log('[DEBUG] Before setState:', oldValue)
   console.log('[DEBUG] After setState:', newValue)
   ```

4. **Isolate the component**
   - Test component in isolation
   - Remove parent props temporarily
   - Check if issue persists

5. **Review useEffect dependencies**
   ```typescript
   useEffect(() => {
     // Check this runs when expected
     console.log('[DEBUG] useEffect triggered')
   }, [/* Verify dependencies */])
   ```

### Workflow B: API Route Error

1. **Check API logs**
   ```bash
   # Check Vercel logs
   # Or run locally with debug
   npm run dev:memory
   ```

2. **Test with curl/Postman**
   ```bash
   curl -X POST https://localhost:3000/api/endpoint \
     -H "Content-Type: application/json" \
     -d '{"test": "data"}'
   ```

3. **Verify authentication**
   - Check headers for auth token
   - Verify token is valid
   - Check RLS policies

4. **Check database query**
   ```typescript
   const { data, error } = await supabase
     .from('table')
     .select()

   console.log('[DEBUG] Query result:', { data, error })
   ```

5. **Review error response**
   - Check status code
   - Read error message
   - Verify response format

### Workflow C: Database/RLS Issue

1. **Check RLS policies**
   ```sql
   SELECT schemaname, tablename, policyname, permissive, roles, cmd, qual
   FROM pg_policies
   WHERE schemaname = 'public'
   AND tablename = 'your_table'
   ORDER BY policyname;
   ```

2. **Test query directly**
   ```sql
   -- In Supabase SQL Editor
   SELECT * FROM public.your_table LIMIT 10;
   ```

3. **Verify service role policy exists**
   ```sql
   SELECT * FROM pg_policies
   WHERE policyname LIKE '%service_role%'
   AND tablename = 'your_table';
   ```

4. **Check foreign key constraints**
   ```sql
   SELECT constraint_name, table_name, column_name
   FROM information_schema.key_column_usage
   WHERE table_name = 'your_table';
   ```

5. **Review indexes**
   ```sql
   SELECT indexname, indexdef
   FROM pg_indexes
   WHERE tablename = 'your_table';
   ```

### Workflow D: Build/Type Error

1. **Run type check**
   ```bash
   npm run type-check:memory
   ```

2. **Read error message carefully**
   - Note file and line number
   - Understand expected vs actual type
   - Check for Next.js 15 patterns

3. **Check import statements**
   - Verify imports are correct
   - Check for missing type definitions
   - Ensure @ alias is used

4. **Review recent changes**
   ```bash
   git diff HEAD~1
   ```

5. **Fix incrementally**
   - Fix one error at a time
   - Re-run type check after each fix
   - Verify fix doesn't create new errors

## Validation Checklist

After applying a fix, verify:

### Immediate Checks (2 minutes)
- [ ] Bug no longer reproduces locally
- [ ] No new console errors
- [ ] No new console warnings
- [ ] Original feature still works

### Code Quality (5 minutes)
- [ ] Type check passes: `npm run type-check`
- [ ] No linting errors: `npm run lint`
- [ ] Code follows CircleTel patterns
- [ ] Error handling is comprehensive

### Build & Deploy (10 minutes)
- [ ] Build succeeds: `npm run build:memory`
- [ ] Test on staging environment
- [ ] No performance regression
- [ ] Database migrations work (if applicable)

### Testing (15 minutes)
- [ ] Unit tests pass (if applicable)
- [ ] E2E tests pass: `npm run test:e2e`
- [ ] Manual testing of related features
- [ ] Edge cases tested

### Documentation (5 minutes)
- [ ] Fix documented in commit message
- [ ] Updated CLAUDE.md if pattern is common
- [ ] Added to debugging knowledge base
- [ ] Team notified if critical

## Quick Reference Commands

```bash
# Development with debugging
npm run dev:memory          # Start with 8GB heap
npm run type-check:memory   # Type check with memory

# Check logs
tail -f .next/server-logs.txt

# Database debugging
npx supabase db dump --schema public
npx supabase db execute -f debug.sql

# Test specific route
curl http://localhost:3000/api/endpoint

# Check build
npm run build:memory

# Clean rebuild
npm run clean && npm run build:memory
```

## Common Bug Patterns & Solutions

| Bug Pattern | Symptom | Root Cause | Quick Fix |
|-------------|---------|------------|-----------|
| Infinite Loading | UI stuck on "Loading..." | Missing finally block | Add `finally { setLoading(false) }` |
| 403 API Error | RLS blocks request | Missing service role policy | Add service_role policy to table |
| Type Error | TypeScript won't compile | Next.js 15 async params | `await context.params` |
| Heap Overflow | Build fails with OOM | Large compilation | Use `npm run build:memory` |
| Undefined Error | Cannot read property of undefined | Missing null check | Add `?.` optional chaining |
| Stale Data | Component shows old data | Missing dependency | Add to useEffect deps array |

## Resources

- **Templates**: See `templates/` for debugging prompt templates
- **Examples**: See `examples/` for real CircleTel bug fixes
- **Checklists**: See `checklists/` for debugging workflows
- **CLAUDE.md**: CircleTel-specific debugging patterns

## Best Practices

1. **Reproduce first, fix second** - Never fix what you can't reproduce
2. **Add logging strategically** - Use [DEBUG] prefix for easy filtering
3. **Test incrementally** - Verify each change doesn't break other features
4. **Document patterns** - Add common bugs to this skill
5. **Use type safety** - Let TypeScript catch bugs early
6. **Follow CircleTel patterns** - Check CLAUDE.md for established solutions

---

**Version**: 1.0.0
**Last Updated**: 2025-11-08
**Maintained By**: CircleTel Development Team
**Based On**: Claude blog post "Fix Software Bugs Faster with Claude"
