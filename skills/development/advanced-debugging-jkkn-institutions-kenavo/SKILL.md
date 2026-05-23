---
name: advanced-debugging
description: Advanced debugging skill for MyJKKN project. Specialized workflows for debugging Next.js 15, Supabase, React Query, TypeScript, and service layer issues. Includes automated analysis tools, common error patterns, and step-by-step troubleshooting guides for reducing debugging time. Use when investigating bugs, errors, performance issues, or unexpected behavior. (project)
---

# Advanced Debugging Skill for MyJKKN

## Purpose

This skill provides specialized debugging workflows, tools, and knowledge for efficiently troubleshooting issues in the MyJKKN application. It covers the complete tech stack including Next.js 15, Supabase, React Query, TypeScript, and custom service layer patterns, significantly reducing time spent on debugging.

## When to Use This Skill

Use this skill when:

- **Investigating Bugs** - Any unexpected behavior or errors in the application
- **Performance Issues** - Slow queries, render loops, memory leaks
- **Authentication Problems** - Login failures, middleware loops, session issues
- **Database Errors** - Supabase RLS failures, query timeouts, data inconsistencies
- **Build/Deploy Errors** - Type errors, build failures, deployment issues
- **React Query Issues** - Stale data, cache problems, mutation failures
- **Service Layer Bugs** - Business logic errors, data transformation issues
- **Production Debugging** - Analyzing logs, user-reported issues

## Tech Stack Overview

### Core Technologies
- **Framework**: Next.js 15.5.4 (App Router)
- **Language**: TypeScript (strict mode)
- **Backend**: Supabase (@supabase/ssr 0.6.1, @supabase/supabase-js 2.45.6)
- **State Management**: React Query 5.72.1, Zustand 5.0.0, SWR 2.2.5
- **UI**: Radix UI components, Tailwind CSS 3.4.1, Framer Motion 11.18.2
- **Forms**: React Hook Form 7.61.0, Zod 3.25.76
- **Data Visualization**: Chart.js, Recharts, React Big Calendar

### Architecture Patterns
- **Service Layer**: Centralized business logic in `lib/services/`
- **Module Organization**: Domain-based (academic, billing, organization, etc.)
- **Optimized Services**: Performance-critical services have `_optimized` variants
- **Authentication**: Middleware-based with profile caching
- **Logging**: Enhanced logger with deduplication and module categorization
- **Access Control**: Role-based + permission-based routing

## How to Use This Skill

### 1. Quick Diagnosis

When encountering an issue, start with the automated analyzer:

```bash
# Analyze current application state
node scripts/debug-analyzer.js

# Analyze specific log file
node scripts/log-analyzer.js logs/app.log

# Test database connectivity and RLS
node scripts/db-query-tester.js
```

### 2. Systematic Debugging Workflow

Follow the debugging workflow in `references/debugging-workflows.md`:

1. **Reproduce the Issue** - Create minimal reproduction steps
2. **Check Logs** - Review enhanced logger output and console
3. **Identify Layer** - Determine which layer has the issue (UI, Service, DB)
4. **Apply Pattern** - Use pattern-specific debugging from references
5. **Verify Fix** - Test thoroughly including edge cases
6. **Document** - Add to common issues if it's a recurring problem

### 3. Layer-Specific Debugging

#### Frontend/UI Issues
```typescript
// Check React Query devtools
import { ReactQueryDevtools } from '@tanstack/react-query-devtools';

// Add to layout for debugging
<ReactQueryDevtools initialIsOpen={false} />

// Monitor component renders
useEffect(() => {
  logger.dev('component-name', 'Component rendered', { props, state });
}, [props, state]);

// Check form validation errors
const { formState: { errors } } = useForm();
console.log('Form errors:', errors);
```

#### Service Layer Issues
```typescript
// Add debug logging to services
import { logger } from '@/lib/utils/enhanced-logger';

static async getData(filters: Filters) {
  logger.dev('module/service', 'Fetching data', { filters });

  try {
    const { data, error } = await this.supabase
      .from('table')
      .select('*')
      .eq('institution_id', filters.institutionId);

    logger.dev('module/service', 'Query result', {
      rowCount: data?.length,
      hasError: !!error
    });

    if (error) {
      logger.error('module/service', 'Query failed', error);
      throw error;
    }

    return data;
  } catch (error) {
    logger.error('module/service', 'Unexpected error', error);
    throw error;
  }
}
```

#### Database/Supabase Issues
```typescript
// Test RLS policies
const { data, error } = await supabase
  .from('table')
  .select('*')
  .eq('id', 'test-id');

console.log('RLS Test:', { data, error });

// Check current user
const { data: { user } } = await supabase.auth.getUser();
console.log('Current user:', user);

// Verify role and permissions
const { data: profile } = await supabase
  .from('profiles')
  .select('*')
  .eq('id', user.id)
  .single();
console.log('Profile:', profile);
```

### 4. Common Error Patterns

Refer to `references/common-issues.md` for solutions to frequent problems:

**Authentication Issues:**
- Middleware redirect loops
- Stale profile cache
- Session timeout errors
- RLS policy failures

**Performance Issues:**
- React Query stale data
- Unnecessary re-renders
- N+1 queries in services
- Large bundle sizes

**Build Errors:**
- TypeScript type mismatches
- Windows EPERM errors
- Module resolution issues
- Environment variable problems

### 5. Supabase-Specific Debugging

See `references/supabase-debugging.md` for detailed Supabase troubleshooting:

**Query Debugging:**
```typescript
// Enable query logging
const { data, error, status, statusText } = await supabase
  .from('table')
  .select('*')
  .explain();

console.log('Query plan:', { data, error, status, statusText });
```

**RLS Policy Testing:**
```sql
-- Test as specific user
SET LOCAL role = 'authenticated';
SET LOCAL request.jwt.claim.sub = 'user-id-here';

SELECT * FROM table WHERE condition;
```

**Connection Issues:**
```typescript
// Test connection with timeout
import { createClient WithTimeout } from '@/lib/supabase/client-with-timeout';

const supabase = createClientWithTimeout(5000); // 5 second timeout
```

### 6. React Query Debugging

Common React Query issues and solutions:

```typescript
// Inspect query state
const { data, isLoading, isError, error, failureReason } = useQuery({
  queryKey: ['key'],
  queryFn: fetchData
});

console.log('Query state:', {
  data,
  isLoading,
  isError,
  error,
  failureReason
});

// Force refetch
const { refetch } = useQuery({ ... });
refetch();

// Invalidate cache
queryClient.invalidateQueries({ queryKey: ['key'] });

// Reset query
queryClient.resetQueries({ queryKey: ['key'] });
```

### 7. Type Debugging

TypeScript-specific debugging:

```typescript
// Check inferred types
type InferredType = typeof variable;
// Hover over InferredType to see the actual type

// Use satisfies for type checking without assertion
const config = {
  api: 'url',
  timeout: 5000
} satisfies Config;

// Debug complex types
type Debug<T> = { [K in keyof T]: T[K] };
type DebuggableType = Debug<ComplexType>;

// Check assignability
const test: ExpectedType = actualValue; // Will error if not assignable
```

### 8. Production Debugging

For debugging production issues:

1. **Check Enhanced Logger Output** - All logs are captured with deduplication
2. **Review Bug Reports** - Use the bug reporter module for user-submitted issues
3. **Analyze Supabase Logs** - Check Supabase dashboard for database errors
4. **Monitor Performance** - Use Vercel Speed Insights for performance issues
5. **Check Error Boundaries** - Review error boundary catches

```typescript
// Production-safe logging
if (process.env.NODE_ENV === 'production') {
  logger.error('module', 'Error occurred', {
    userId: user.id,
    timestamp: new Date().toISOString(),
    error: error.message // Don't log full error in production
  });
}
```

## Debugging Tools

### Enhanced Logger
Location: `lib/utils/enhanced-logger.ts`

Features:
- Automatic log deduplication
- Module-based categorization
- Component name extraction
- Occurrence counting
- Bug reporter integration

Usage:
```typescript
import { logger } from '@/lib/utils/enhanced-logger';

logger.dev('module', 'Development log', data);      // Dev only
logger.info('module', 'Info message', data);         // Production
logger.warn('module', 'Warning message', data);      // Production
logger.error('module', 'Error message', error);      // Production
logger.debug('module', 'Debug message', data);       // Dev only
```

### Debug Scripts

**debug-analyzer.js** - Analyzes application state and configuration
```bash
node scripts/debug-analyzer.js
```

**log-analyzer.js** - Parses and analyzes log files
```bash
node scripts/log-analyzer.js logs/app.log --filter error
node scripts/log-analyzer.js logs/app.log --module billing
```

**db-query-tester.js** - Tests database queries and RLS policies
```bash
node scripts/db-query-tester.js --test-connection
node scripts/db-query-tester.js --test-rls table_name
```

## Best Practices

### 1. Systematic Approach
- Always start with reproduction steps
- Check logs before diving into code
- Use binary search for narrowing down issues
- Test one thing at a time

### 2. Proper Logging
- Use enhanced logger with module prefixes
- Log errors with context (user ID, timestamp, input data)
- Remove temporary console.log before committing
- Keep console.warn and console.error for production

### 3. Type Safety
- Let TypeScript catch errors at compile time
- Don't use 'any' unless absolutely necessary
- Use type guards for runtime type checking
- Leverage Zod for runtime validation

### 4. Testing Changes
- Test in development first
- Check all user roles and permissions
- Verify mobile responsiveness
- Test both light and dark modes
- Check error states and loading states

### 5. Documentation
- Add comments for complex logic
- Document workarounds with TODO and explanation
- Update common-issues.md for recurring problems
- Share findings with the team

## Troubleshooting Checklist

Before diving deep, check these common issues:

**Authentication:**
- [ ] Is the user logged in?
- [ ] Is the session valid?
- [ ] Are cookies being set correctly?
- [ ] Is the profile cache invalidated?

**Database:**
- [ ] Is Supabase reachable?
- [ ] Are RLS policies correct?
- [ ] Is the institution_id filter applied?
- [ ] Are foreign keys valid?

**React Query:**
- [ ] Is the queryKey correct and stable?
- [ ] Is staleTime appropriate?
- [ ] Are mutations invalidating queries?
- [ ] Is the cache being cleared when needed?

**Service Layer:**
- [ ] Is error handling present?
- [ ] Are null checks in place?
- [ ] Is data transformation correct?
- [ ] Are optimized services being used?

**UI/Components:**
- [ ] Are props being passed correctly?
- [ ] Is conditional rendering working?
- [ ] Are loading states shown?
- [ ] Are error states handled?

**Build/Deploy:**
- [ ] Do TypeScript types pass?
- [ ] Are environment variables set?
- [ ] Are dependencies up to date?
- [ ] Is the build cache cleared?

## References

- **Debugging Workflows**: `references/debugging-workflows.md`
  - Step-by-step debugging processes
  - Layer-specific workflows
  - Decision trees for quick diagnosis

- **Common Issues**: `references/common-issues.md`
  - Known bugs and solutions
  - Workarounds for platform issues
  - Frequently encountered errors

- **Supabase Debugging**: `references/supabase-debugging.md`
  - RLS policy debugging
  - Query optimization
  - Connection troubleshooting
  - Auth debugging

- **Performance Debugging**: `references/performance-debugging.md`
  - React Query optimization
  - Service layer optimization
  - Bundle size analysis
  - Render performance

## Quick Reference

### Essential Commands
```bash
# Development
npm run dev          # Start dev server
npm run build        # Test production build
npm run lint         # Check linting errors

# Debugging
npm run clean        # Clear Next.js cache
npm run clean:all    # Clear all caches

# Testing
npx tsc --noEmit     # Type check without building
```

### Key File Locations
```
lib/utils/enhanced-logger.ts     # Logging utility
lib/supabase/client.ts          # Supabase client
middleware.ts                   # Auth middleware
lib/services/                   # Service layer
types/                          # TypeScript types
app/(routes)/                   # Page routes
```

### Environment Variables
```
NEXT_PUBLIC_SUPABASE_URL        # Supabase project URL
NEXT_PUBLIC_SUPABASE_ANON_KEY   # Supabase anon key
NEXT_PUBLIC_APP_VERSION         # App version for caching
NODE_ENV                        # development | production
```

---

**Version**: 1.0.0
**Last Updated**: 2025-01-16
**Maintained by**: MyJKKN Development Team
