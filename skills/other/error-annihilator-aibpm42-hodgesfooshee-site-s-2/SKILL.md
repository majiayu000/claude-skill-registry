---
name: error-annihilator
description: Elite debugging and error-resolution system optimized for Next.js/TypeScript/Supabase stacks. Use when encountering ANY error, bug, or unexpected behavior including API failures, database issues, build errors, runtime crashes, logic bugs, performance problems, or deployment issues. Specializes in cryptic webpack errors, Supabase RLS policies, vector database mismatches, module resolution, API cascades, and multi-error triage. Provides rapid root cause analysis + ranked solution approaches + explanatory insights. Trigger on error messages, stack traces, "why isn't this working", "something's broken", debugging requests, or troubleshooting needs.
---

# Error Annihilator

**The ultimate error-crushing, bug-demolishing, problem-solving machine for developers.**

## Core Philosophy

**Speed + Depth:** Deliver quick fix to unblock immediately, then explain root cause for learning.

**Solution Ranking:** Provide 3 solution approaches ranked by likelihood, effort, and risk.

**Pattern Recognition:** Identify error categories and apply proven resolution strategies.

## Triage Process (Multiple Errors)

When facing multiple errors simultaneously:

1. **Categorize each error** by impact:
   - **Blockers** - Prevent all progress (build failures, fatal crashes)
   - **Cascaders** - Cause downstream failures (API rate limits, auth issues)
   - **Independents** - Isolated problems (logic bugs, styling issues)

2. **Prioritize fix order:**
   - Fix blockers first (can't proceed without)
   - Fix cascaders second (stop error spread)
   - Fix independents last (won't affect other issues)

3. **Identify dependencies:**
   - "Will fixing X automatically resolve Y?"
   - "Are errors A and B symptoms of same root cause?"

**Example from today:**
- PDF worker error (blocker) → Fix first with alternative library
- Dimension mismatch (independent) → Fix second after PDF parsing works
- Canvas dependency (cascader from pdfjs-dist) → Resolved by switching libraries

## Diagnostic Workflow

### Step 1: Extract Error Intelligence (30 seconds)

Parse error message for:
- **Error type** (syntax, runtime, network, database, build)
- **Component** (which file, function, service)
- **Context** (what was happening when it broke)
- **Stack trace** (execution path to failure)

Use: `scripts/parse_error.py` if error message is cryptic

### Step 2: Identify Root Cause (1-2 minutes)

Match error pattern to known categories:

**API/Network Failures** → See `references/api-debugging.md`
- Rate limiting, timeouts, 4xx/5xx errors
- Authentication failures
- CORS issues
- Response format mismatches

**Database/Data Issues** → See `references/database-debugging.md`
- Schema mismatches, migration failures
- RLS policy violations
- Vector dimension errors
- Query failures, connection issues

**Build/Compilation Errors** → See `references/build-debugging.md`
- Webpack bundling issues
- Module resolution (missing dependencies, peer deps)
- TypeScript type errors
- Import path problems

**Runtime Errors** → See `references/runtime-debugging.md`
- Null/undefined access
- Type mismatches
- Promise rejections
- Event handling failures

**Logic Bugs** → See `references/logic-debugging.md`
- Wrong results, unexpected behavior
- State management issues
- Race conditions
- Edge case failures

### Step 3: Generate Solution Plan (2-3 minutes)

For identified root cause:

1. **Quick Fix** (unblock immediately)
2. **Proper Fix** (address root cause)
3. **Preventive Fix** (catch before it happens again)

Rank by:
- **Likelihood** (will this actually fix it?)
- **Effort** (how long to implement?)
- **Risk** (could this break something else?)

### Step 4: Execute & Validate (implementation time)

1. Apply quick fix
2. Test that error is resolved
3. Implement proper fix if different
4. Add preventive measures

## Error Category Deep Dives

### API/Network Failures (Priority #1)

**Common patterns:**

1. **Rate Limiting (429)**
   - Root cause: Too many requests, no backoff
   - Quick fix: Reduce request frequency manually
   - Proper fix: Implement exponential backoff (see `references/api-debugging.md#rate-limiting`)
   - Prevention: Rate limit detector + queue system

2. **Authentication Failures (401/403)**
   - Root cause: Invalid/expired token, wrong credentials
   - Quick fix: Regenerate token, check env vars
   - Proper fix: Token refresh logic
   - Prevention: Token expiry monitoring

3. **Timeout Errors**
   - Root cause: Request takes too long, network issue
   - Quick fix: Increase timeout value
   - Proper fix: Optimize request or paginate
   - Prevention: Progress indicators, background jobs

4. **CORS Issues**
   - Root cause: Missing headers, wrong origin
   - Quick fix: Proxy through API route
   - Proper fix: Configure CORS on server
   - Prevention: Environment-specific CORS config

**Diagnostic script:** `scripts/test_api_endpoint.py`

### Database/Data Issues (Priority #2)

**Common patterns:**

1. **Vector Dimension Mismatch**
   - Root cause: Model output ≠ schema dimensions
   - Quick fix: Verify model dimensions, update schema
   - Proper fix: Dimension validation before insert
   - Prevention: Config-driven dimension management
   - **See:** `references/database-debugging.md#vector-dimensions`

2. **RLS Policy Violations**
   - Root cause: Row-level security blocking query
   - Quick fix: Disable RLS temporarily to isolate
   - Proper fix: Adjust policy or query conditions
   - Prevention: RLS policy testing suite
   - **See:** `references/supabase-issues.md#rls-debugging`

3. **Migration Failures**
   - Root cause: Schema conflict, data incompatibility
   - Quick fix: Rollback migration
   - Proper fix: Fix migration script, re-run
   - Prevention: Staging environment testing
   - **See:** `references/database-debugging.md#migrations`

4. **Connection Issues**
   - Root cause: Pool exhaustion, network problem
   - Quick fix: Restart service, check connection string
   - Proper fix: Connection pooling config
   - Prevention: Connection monitoring

**Diagnostic script:** `scripts/test_db_connection.py`

### Build/Compilation Errors (Priority #3)

**Common patterns:**

1. **Webpack Module Errors**
   - Root cause: Module not found, bundling issue
   - Quick fix: Check import paths, reinstall deps
   - Proper fix: Webpack config adjustment
   - Prevention: Import validation
   - **See:** `references/nextjs-troubleshooting.md#webpack`

2. **Missing Dependencies**
   - Root cause: Peer dep not installed, wrong version
   - Quick fix: Install missing package
   - Proper fix: Update package.json properly
   - Prevention: Dependency audit script
   - **Use:** `scripts/check_dependencies.py`

3. **TypeScript Errors**
   - Root cause: Type mismatch, missing types
   - Quick fix: Use `any` temporarily (caution!)
   - Proper fix: Correct types, install @types
   - Prevention: Strict TypeScript config
   - **See:** `references/typescript-errors.md`

4. **Next.js Edge Cases**
   - Root cause: Server/client mismatch, SSR issue
   - Quick fix: Dynamic import with ssr: false
   - Proper fix: Proper hydration handling
   - Prevention: Component testing
   - **See:** `references/nextjs-troubleshooting.md`

**Diagnostic script:** `scripts/analyze_build_error.py`

## Tech Stack Specific Guides

### Next.js Debugging
**See:** `references/nextjs-troubleshooting.md`

Common issues:
- Webpack bundling problems
- Server vs. client code
- Dynamic imports
- API routes
- Middleware issues

### Supabase Debugging
**See:** `references/supabase-issues.md`

Common issues:
- RLS policies
- Realtime subscriptions
- Edge functions
- Storage permissions
- Vector operations

### TypeScript Debugging
**See:** `references/typescript-errors.md`

Common issues:
- Type inference failures
- Generic constraints
- Module augmentation
- Type narrowing

## Solution Ranking Methodology

For each error, provide 3 solutions ranked:

**Solution 1: Highest Likelihood** (try this first)
- Why it's likely to work
- Implementation steps
- Expected result
- Risk level: [Low/Medium/High]
- Time: [5 min / 30 min / 2+ hours]

**Solution 2: Alternative Approach** (if #1 fails)
- Different strategy
- Implementation steps
- Expected result
- Risk level: [Low/Medium/High]
- Time: [5 min / 30 min / 2+ hours]

**Solution 3: Nuclear Option** (last resort)
- Fundamental change or workaround
- Implementation steps
- Expected result
- Risk level: [Low/Medium/High]
- Time: [5 min / 30 min / 2+ hours]

**Example: PDF Parse Worker Error**

**Solution 1: Switch to pdfjs-dist** (Highest likelihood)
- Why: Works natively with Next.js webpack
- Steps: `npm install pdfjs-dist`, update import, configure worker
- Risk: Low - Well-tested library
- Time: 15 minutes

**Solution 2: Use pdf2json** (Alternative)
- Why: Simpler API, no worker needed
- Steps: `npm install pdf2json`, rewrite parsing code
- Risk: Medium - Less feature-rich
- Time: 30 minutes

**Solution 3: Extract text server-side** (Nuclear)
- Why: Avoid client-side bundling entirely
- Steps: Create API route, use pdf-parse on server
- Risk: Low - Architectural change
- Time: 1 hour

## Rapid Response Templates

### Quick Diagnostic

When user shares error:

```markdown
## 🔍 Error Analysis

**Error Type:** [API/Database/Build/Runtime/Logic]
**Component:** [File/Service/Function]
**Root Cause:** [Identified cause]

## ⚡ Quick Fix (Unblock Now)
[Immediate action to get unstuck]

## 🎯 Proper Fix (Root Cause)
[Correct implementation]

## 🛡️ Prevention
[How to catch this early]
```

### Solution Plan

```markdown
## 💡 Solution Approaches

**Solution 1: [Name]** ⭐ Recommended
- Likelihood: High | Effort: Low | Risk: Low
- [Steps]

**Solution 2: [Name]** 
- Likelihood: Medium | Effort: Medium | Risk: Low
- [Steps]

**Solution 3: [Name]** ⚠️ Last Resort
- Likelihood: High | Effort: High | Risk: Medium
- [Steps]

## 📚 Why This Happened
[Brief explanation of root cause]
```

## Proactive Error Prevention

Beyond fixing errors, help prevent them:

1. **Validation checks** before operations
   - Dimension checks before vector insert
   - Type validation before API calls
   - Schema validation before migrations

2. **Error boundaries** for graceful degradation
   - React error boundaries
   - API fallbacks
   - Retry logic with exponential backoff

3. **Configuration validation** at startup
   - Environment variable checks
   - Dependency version checks
   - API connectivity tests

4. **Monitoring and alerting**
   - Error rate tracking
   - Performance monitoring
   - Health check endpoints

## Multi-Error Scenarios

When multiple errors occur simultaneously:

1. **Draw dependency graph**
   - Which errors might share root cause?
   - Which errors cascade from others?

2. **Prioritize by criticality**
   - What blocks all progress? (Fix first)
   - What causes downstream issues? (Fix second)
   - What's isolated? (Fix last)

3. **Sequential resolution**
   - Fix highest priority
   - Re-test to see if others resolved
   - Continue down priority list

**Example Triage:**
```
Today's errors:
1. PDF worker error → BLOCKER (can't parse PDFs)
2. Canvas dependency → CASCADER (caused by pdfjs-dist)
3. Vector dimension → INDEPENDENT

Fix order:
1. Switch PDF library (resolves #1 and #2)
2. Fix vector dimensions (resolves #3)
```

## Advanced Debugging Techniques

### Stack Trace Analysis
**See:** `references/stack-trace-analysis.md`
- Reading stack traces effectively
- Identifying call chain
- Finding actual error source

### Network Debugging
**See:** `references/network-debugging.md`
- Browser DevTools Network tab
- Request/response inspection
- Timing analysis

### Database Query Optimization
**See:** `references/query-optimization.md`
- Slow query identification
- Index optimization
- Query plan analysis

## Error Categories Reference

Quick lookup for error patterns:

- **API Issues:** `references/api-debugging.md`
- **Database Issues:** `references/database-debugging.md`
- **Build Errors:** `references/build-debugging.md`
- **Runtime Errors:** `references/runtime-debugging.md`
- **Logic Bugs:** `references/logic-debugging.md`
- **Next.js Specific:** `references/nextjs-troubleshooting.md`
- **Supabase Specific:** `references/supabase-issues.md`
- **TypeScript Errors:** `references/typescript-errors.md`

## Success Metrics

A successful error resolution:
- ✅ Error identified and categorized
- ✅ Root cause explained
- ✅ Quick fix provided (if available)
- ✅ Proper fix implemented
- ✅ Prevention strategy suggested
- ✅ User learns the pattern

## Usage Examples

**Example 1: Vector Dimension Error**
User: "Getting error: expected 768 dimensions, not 1024"
Response: Root cause analysis → HuggingFace model outputs 1024 → Quick fix: Update schema → Proper fix: Add dimension validation → Prevention: Config-driven dimensions

**Example 2: Webpack Module Error**
User: "Cannot find module './pdf.worker.mjs'"
Response: Identify webpack issue → Quick fix: Switch to pdfjs-dist → Explain why pdf-parse doesn't work → Prevention: Check Next.js compatibility before installing

**Example 3: RLS Policy Violation**
User: "Row violates row-level security policy"
Response: Isolate which policy → Check policy conditions → Quick fix: Adjust query → Proper fix: Update policy → Prevention: RLS testing suite

The Error Annihilator doesn't just fix bugs—it makes you a better debugger.
