---
name: verify-work
description: Comprehensive pre-commit verification for security, best practices, and code standards. Checks for vulnerabilities, efficiency issues, and convention adherence.
---

# Verify Work Skill

Comprehensive pre-commit verification of code changes for security vulnerabilities, best practices violations, efficiency issues, and adherence to project conventions.

## When to Use

**Automatically invoked** as Phase 0 of `/ship` (mandatory - cannot be skipped)

Can also be invoked manually with `/verify-work` to check changes before committing.

## Instructions

### Phase 1: Analyze Changed Files

**Goal**: Get comprehensive view of all changes

```bash
# Get changed file list
git status --short

# Get diff statistics
git diff --stat HEAD

# Get detailed diff
git diff HEAD

# Get file paths only
git diff --name-only HEAD
```

**Categorize files**:
- API routes: `app/api/**/*.ts`
- Components: `src/components/**/*.tsx`
- Types: `src/types/**/*.ts`
- Utilities: `src/utils/**/*.ts`, `lib/**/*.ts`
- Migrations: `database/migrations/**/*.sql`

---

### Phase 2: Security Checks [BLOCKING]

#### 2.1 Hardcoded Secrets Detection

```bash
# Check for potential secrets
git diff HEAD | grep -iE "(password|secret|api[_-]?key|token|stripe[_-]?key|jwt[_-]?secret|database[_-]?url).*=.*['\"]" | grep -v "process\.env"

# Check for actual secret patterns (32+ character strings)
git diff HEAD | grep -E "^[+].*['\"][a-zA-Z0-9_-]{32,}['\"]"

# Check for .env files (should never be committed)
git diff --name-only HEAD | grep -E "^\.env"
```

**Flag if found**:
- ❌ **BLOCKING**: Any hardcoded credentials (passwords, API keys, tokens)
- ❌ **BLOCKING**: Database URLs with credentials
- ❌ **BLOCKING**: JWT secrets, Stripe keys
- ❌ **BLOCKING**: Any `.env` or `.env.local` files

**Auto-fix**: Not available - requires manual intervention

**Manual fix guidance**:
```
Found: const API_KEY = "sk_live_xxxxx"
Fix:
1. Add to .env.local: API_KEY=sk_live_xxxxx
2. Replace with: const API_KEY = process.env.API_KEY
3. Add validation: if (!API_KEY) throw new Error('API_KEY is required')
```

#### 2.2 SQL Injection Risks

```bash
# Check for template literal variables in SQL queries (dangerous)
git diff HEAD -- 'app/api/**/*.ts' 'lib/**/*.ts' | grep -E "\`.*\$\{.*\}.*\`" | grep -iE "select|insert|update|delete|where"

# Check for string concatenation in queries
git diff HEAD -- 'app/api/**/*.ts' 'lib/**/*.ts' | grep -E "query\(.*\+|sql\(.*\+"

# Check for non-parameterized queries
git diff HEAD -- 'app/api/**/*.ts' 'lib/**/*.ts' | grep -E "query\(|queryOne\(|sql\(" -A 2 | grep -E "^[+]" | grep -v "\$[0-9]"
```

**Flag if found**:
- ❌ **BLOCKING**: Template literals with variables in SQL queries
- ❌ **BLOCKING**: String concatenation in query building
- ⚠️ **WARNING**: Queries without parameterized values ($1, $2, etc.)

**Auto-fix**: Not available - requires query refactoring

**Manual fix guidance**:
```
Found: query(`SELECT * FROM users WHERE id = ${userId}`)
Fix:   query('SELECT * FROM users WHERE id = $1', [userId])

Found: query('SELECT * FROM users WHERE email = ' + email)
Fix:   query('SELECT * FROM users WHERE email = $1', [email])
```

**Safe patterns** (from CLAUDE.md):
- `query('SELECT * FROM users WHERE id = $1', [userId])`
- `queryOne('SELECT * FROM projects WHERE id = $1 AND user_id = $2', [projectId, userId])`

#### 2.3 XSS Vulnerabilities

```bash
# Check for dangerouslySetInnerHTML
git diff HEAD -- 'src/**/*.tsx' | grep -E "dangerouslySetInnerHTML|innerHTML"

# Check for unescaped user input rendering
git diff HEAD -- 'src/**/*.tsx' | grep -E "\{[^}]*input[^}]*\}|\{[^}]*value[^}]*\}" | grep -v "type=|placeholder=|value=|onChange="
```

**Flag if found**:
- ❌ **BLOCKING**: Any use of `dangerouslySetInnerHTML`
- ⚠️ **WARNING**: Direct rendering of user input without validation

**Auto-fix**: Not available - requires sanitization implementation

#### 2.4 Missing Input Validation

```bash
# Check API routes for missing Zod schemas
git diff HEAD -- 'app/api/**/*.ts' | grep -E "export const (POST|PATCH)" -A 20 | grep -L "z\.object"

# Check for request.json() without validation
git diff HEAD -- 'app/api/**/*.ts' | grep "request\.json()" -A 3 | grep -v "safeParse\|parse"

# Check for missing withAuth wrapper
git diff HEAD -- 'app/api/**/route.ts' | grep -E "export const (GET|POST|PATCH|DELETE)" -B 1 | grep -v "withAuth\|withAdmin"
```

**Flag if found**:
- ❌ **BLOCKING**: POST/PATCH routes without Zod validation
- ❌ **BLOCKING**: `request.json()` without `.safeParse()`
- ❌ **BLOCKING**: Protected routes not using `withAuth` or `withAdmin`
- ⚠️ **WARNING**: Missing project ownership verification

**Auto-fix**: Available for adding imports, not for creating schemas

**Manual fix guidance**:
```
Found: const body = await request.json()
Fix:
1. Define schema:
   const createSchema = z.object({
     title: z.string().min(1).max(500),
     description: z.string().optional()
   });

2. Validate:
   const body = await request.json();
   const validation = createSchema.safeParse(body);
   if (!validation.success) {
     return errorResponse(validation.error.errors[0].message);
   }

3. Use validated data:
   const data = validation.data;
```

#### 2.5 Missing Rate Limiting

```bash
# Check auth routes for rate limiting
git diff HEAD -- 'app/api/auth/**/*.ts' | grep "export const POST" -A 15 | grep -v "withRateLimit"

# Check admin routes for rate limiting
git diff HEAD -- 'app/api/admin/**/*.ts' | grep "export const (POST|PATCH|DELETE)" -A 15 | grep -v "withRateLimit"

# Check new API routes generally
git diff HEAD -- 'app/api/**/*.ts' | grep "export const POST" -A 10 | grep -v "withRateLimit"
```

**Flag if found**:
- ❌ **BLOCKING**: Auth routes without rate limiting
- ❌ **BLOCKING**: Admin actions without rate limiting
- ⚠️ **WARNING**: Public POST endpoints without protection

**Auto-fix**: Available for adding rate limiting wrapper

**Available rate limit configs** (from `lib/rate-limit.ts`):
- `rateLimits.default` - 100 req/min (general endpoints)
- `rateLimits.strict` - 10 req/min (sensitive operations)
- `rateLimits.analytics` - 200 req/min (high-volume tracking)
- `rateLimits.webhook` - 50 req/min (external webhooks)
- `rateLimits.admin` - 60 req/min (admin operations)

---

### Phase 3: Best Practices Review [BLOCKING]

#### 3.1 Debug Code Removal

```bash
# Find console statements
git diff HEAD | grep -nE "console\.(log|warn|error|info|debug)" | grep -v "^-" | grep -v "// console"

# Find TODO/FIXME comments
git diff HEAD | grep -niE "^[+].*(//)?\s*(todo|fixme|xxx|hack)" | grep -v "TodoWrite"

# Find commented-out code blocks (3+ consecutive lines)
git diff HEAD | grep -E "^[+]\s*//\s*[a-zA-Z]" -A 2 | grep -E "^[+]\s*//"
```

**Flag if found**:
- ⚠️ **BLOCKING**: `console.log`, `console.warn`, `console.error` (except in error boundaries)
- ⚠️ **BLOCKING**: TODO/FIXME comments without tracking
- ⚠️ **BLOCKING**: Large blocks of commented code (3+ lines)

**Auto-fix**: Available - can remove console.logs and commented code

**Auto-fix command**:
```bash
# Remove console statements
git diff --name-only HEAD | while read file; do
  sed -i '/console\.\(log\|warn\|error\|info\|debug\)/d' "$file"
done
```

#### 3.2 TypeScript Issues

```bash
# Find 'any' types
git diff HEAD -- '*.ts' '*.tsx' | grep -nE ":\s*any[^a-zA-Z]" | grep -v "// "

# Find @ts-ignore or @ts-nocheck
git diff HEAD | grep -nE "@ts-(ignore|nocheck|expect-error)"

# Find excessive type assertions
git diff HEAD | grep -nE "as any|as unknown" | grep -v "^\-"
```

**Flag if found**:
- ⚠️ **BLOCKING**: `: any` type annotations (suggest proper typing)
- ⚠️ **BLOCKING**: `@ts-ignore` without explanation comment
- 💡 **OPTIMIZATION**: Excessive `as any` or `as unknown` casts

**Auto-fix**: Not available - requires proper type definition

**Manual fix guidance**:
```
Found: const data: any = await response.json()
Fix:
1. Define interface:
   interface ResponseData {
     items: Item[];
     total: number;
   }

2. Use proper type:
   const data = await response.json() as ResponseData;
   // OR
   const data: ResponseData = await response.json();
```

#### 3.3 Error Handling

```bash
# Check for empty catch blocks
git diff HEAD -- 'app/api/**/*.ts' | grep -E "catch.*\{" -A 5 | grep -E "^[+]\s*\}" | grep -v "errorResponse\|console\.error"

# Check for try-catch without error response
git diff HEAD -- 'app/api/**/*.ts' | grep -E "catch.*\{" -A 8 | grep -v "errorResponse\|return.*Response"

# Check for unhandled promise rejections (await outside try-catch in API routes)
git diff HEAD -- 'app/api/**/*.ts' | grep "await " | grep -v "try\|catch"
```

**Flag if found**:
- ⚠️ **BLOCKING**: Empty catch blocks
- ⚠️ **BLOCKING**: Catch blocks that swallow errors silently
- 💡 **OPTIMIZATION**: Async calls outside try-catch in API routes

**Auto-fix**: Not available - requires error handling logic

---

### Phase 4: Efficiency Review [OPTIMIZATION]

#### 4.1 React Hook Usage

```bash
# Check for hooks outside components
git diff HEAD -- 'src/**/*.tsx' | grep -B 5 "use(State|Effect|Memo|Callback|Context)" | grep -E "^[+]export (function|const) [a-z]"

# Check for useEffect without dependency array
git diff HEAD -- 'src/**/*.tsx' | grep "useEffect" -A 2 | grep -E "^\+.*\}\)" | grep -v ", \["

# Check for missing dependencies
git diff HEAD -- 'src/**/*.tsx' | grep -E "useEffect|useCallback|useMemo" -A 5 | grep "\[\]" -B 3 | grep -E "const|let|var"
```

**Flag if found**:
- 💡 **OPTIMIZATION**: Hooks called outside React components
- 💡 **OPTIMIZATION**: `useEffect` without dependency array (infinite loop risk)
- 💡 **OPTIMIZATION**: Missing dependencies in effect/callback/memo

**Auto-fix**: Not available - requires React knowledge

#### 4.2 Unnecessary Re-renders

```bash
# Check for inline arrow functions in props
git diff HEAD -- 'src/**/*.tsx' | grep -E "onClick=\{.*=>|onChange=\{.*=>|onSubmit=\{.*=>"

# Check for inline object/array literals in props
git diff HEAD -- 'src/**/*.tsx' | grep -E "style=\{\{|className=\{\[|data=\{\{"
```

**Flag if found**:
- 💡 **OPTIMIZATION**: Inline arrow functions in render (suggest `useCallback`)
- 💡 **OPTIMIZATION**: Inline object/array literals in props (suggest `useMemo`)

**Auto-fix**: Not available - requires refactoring

#### 4.3 Import Optimization

```bash
# Check for potentially unused imports (added but not referenced in diff)
git diff HEAD | grep "^+import" | cut -d' ' -f2 | cut -d',' -f1 | while read import; do
  git diff HEAD | grep -v "^+import" | grep -q "$import" || echo "Unused: $import"
done
```

**Flag if found**:
- 💡 **OPTIMIZATION**: Imports added but not used in changes

**Auto-fix**: Available - can remove unused imports

#### 4.4 Code Complexity & File Size [REFACTOR]

```bash
# Find large files (500+ lines) in changed files
git diff --name-only HEAD | while read file; do
  if [ -f "$file" ]; then
    lines=$(wc -l < "$file" 2>/dev/null || echo 0)
    if [ "$lines" -gt 500 ]; then
      echo "LARGE FILE ($lines lines): $file"
    fi
  fi
done

# Find very large files (800+ lines) - high priority
git diff --name-only HEAD | while read file; do
  if [ -f "$file" ]; then
    lines=$(wc -l < "$file" 2>/dev/null || echo 0)
    if [ "$lines" -gt 800 ]; then
      echo "VERY LARGE FILE ($lines lines): $file"
    fi
  fi
done

# Find large React components (check for component files over 300 lines)
git diff --name-only HEAD | grep -E "\.tsx$" | while read file; do
  if [ -f "$file" ]; then
    lines=$(wc -l < "$file" 2>/dev/null || echo 0)
    if [ "$lines" -gt 300 ]; then
      echo "LARGE COMPONENT ($lines lines): $file"
    fi
  fi
done

# Find files with many functions (potential for extraction)
git diff --name-only HEAD | grep -E "\.(ts|tsx)$" | while read file; do
  if [ -f "$file" ]; then
    funcs=$(grep -cE "^(export )?(async )?(function |const \w+ = (\(|async \())" "$file" 2>/dev/null || echo 0)
    if [ "$funcs" -gt 10 ]; then
      echo "MANY FUNCTIONS ($funcs functions): $file"
    fi
  fi
done
```

**Thresholds**:
| Type | Warning | High Priority | Action |
|------|---------|---------------|--------|
| Any file | 500+ lines | 800+ lines | Consider splitting |
| Component (.tsx) | 300+ lines | 500+ lines | Extract sub-components |
| Functions per file | 10+ | 15+ | Extract to separate module |
| API route | 200+ lines | 300+ lines | Extract helpers to lib/ |

**Flag if found**:
- 🔧 **REFACTOR**: Files over 500 lines - consider splitting
- 🔧 **REFACTOR**: Components over 300 lines - extract sub-components
- 🔧 **REFACTOR**: Files with 10+ functions - extract related functions to module
- 🔧 **REFACTOR (HIGH)**: Files over 800 lines - strongly recommend splitting

**Auto-fix**: Not available - requires architectural decisions

**Refactoring Guidance**:

**Large Component Refactoring**:
```
Found: src/components/Dashboard.tsx (450 lines)

Recommendations:
1. Extract logical sections into sub-components:
   - DashboardHeader.tsx
   - DashboardStats.tsx
   - DashboardActions.tsx

2. Extract hooks to separate files:
   - useDashboardData.ts
   - useDashboardFilters.ts

3. Extract utility functions:
   - src/utils/dashboardHelpers.ts
```

**Large API Route Refactoring**:
```
Found: app/api/projects/[id]/data/route.ts (380 lines)

Recommendations:
1. Extract data transformation logic:
   - lib/transformers/projectTransformers.ts

2. Extract query builders:
   - lib/queries/projectQueries.ts

3. Keep route handler thin:
   - Validate input
   - Call service functions
   - Return response
```

**Many Functions Refactoring**:
```
Found: src/utils/dateUtils.ts (12 functions)

Recommendations:
1. Group related functions:
   - src/utils/date/formatting.ts (formatDate, formatTime, etc.)
   - src/utils/date/comparison.ts (isToday, isBefore, etc.)
   - src/utils/date/parsing.ts (parseDate, parseISO, etc.)

2. Create barrel export:
   - src/utils/date/index.ts
```

**When NOT to refactor** (acceptable large files):
- Type definition files (`src/types/index.ts`) - centralization is intentional
- Test files - keeping related tests together is fine
- Migration files - single file per migration is correct
- Generated code - don't refactor auto-generated files

---

### Phase 4.5: Database Performance [BLOCKING]

Critical database/API performance patterns not covered by Phase 4.
For full benchmark with historical data, run `/benchmark-performance`.

#### 4.5.1 N+1 Query Patterns

```bash
# Queries inside loops (major performance killer)
git diff HEAD -- 'app/api/**/*.ts' | grep -nE "for\s*\(|while\s*\(|\.forEach\(|\.map\(" -A 10 | grep -E "await.*query|await.*queryOne"

# Async array methods with database calls
git diff HEAD -- 'app/api/**/*.ts' | grep -nE "\.map\(async|\.forEach\(async" -A 5 | grep -E "query|queryOne"
```

**Flag if found**:
- 🐢 **BLOCKING**: Queries inside loops (use batch query with IN/ANY clause instead)

**Manual fix guidance**:
```
Found: items.forEach(async (item) => { await query('SELECT...', [item.id]) })

Fix: Batch query with ANY:
     const ids = items.map(i => i.id);
     const results = await query('SELECT... WHERE id = ANY($1)', [ids]);
```

#### 4.5.2 Unbounded Queries

```bash
# SELECT without LIMIT or ID filter (can return unlimited rows)
git diff HEAD -- 'app/api/**/*.ts' | grep -nE "SELECT.*FROM" | grep -v "LIMIT|WHERE.*id\s*=|RETURNING|COUNT\(|EXISTS\(|MAX\(|MIN\("
```

**Flag if found**:
- 🐢 **BLOCKING**: Unbounded queries without LIMIT (add pagination or ID filter)

**Safe patterns**:
- `SELECT * FROM items WHERE id = $1` (single row by ID)
- `SELECT * FROM items WHERE project_id = $1 LIMIT 100` (paginated)
- `SELECT COUNT(*) FROM items` (aggregation)
- `SELECT * FROM items WHERE id = ANY($1)` (bounded by input array)

#### 4.5.3 Missing Index Patterns

```bash
# Leading wildcard LIKE (cannot use index, causes full table scan)
git diff HEAD -- 'app/api/**/*.ts' | grep -nE "LIKE\s*['\"]%"

# Excessive OR chains
git diff HEAD -- 'app/api/**/*.ts' | grep -nE "WHERE.*OR.*OR.*OR"
```

**Flag if found**:
- ⏱️ **WARNING**: Leading wildcard LIKE (consider full-text search for large tables)
- ⏱️ **WARNING**: Excessive OR chains (consider using IN or ANY)

**For full analysis:** Run `/benchmark-performance` for historical context and additional checks.

---

### Phase 4.6: API Performance Tests [BLOCKING]

Check for performance regressions in API endpoints when API routes are changed.

#### 4.6.1 Check for API Changes

```bash
# Check if any API routes were modified
git diff --name-only HEAD | grep -E "app/api/.*route\.ts$"
```

**If no API routes changed**: Skip to Phase 5.

#### 4.6.2 Run Performance Tests

```bash
# Run performance test suite
npm test tests/performance/ -- --reporter=verbose
```

**Wait for tests to complete before proceeding.**

#### 4.6.3 Evaluate Results

**Flag if found**:
- 🏎️ **BLOCKING**: Response time exceeds P50 threshold
- 🏎️ **BLOCKING**: Performance regression detected (>50% slower than baseline)

**Auto-fix**: Not available - requires endpoint optimization

**Manual fix guidance**:
```
Found: GET /api/global/data - 892ms (target: <400ms) - REGRESSION!
       Baseline: 250ms | Current: 892ms | +256% slower

Fix options:
1. Optimize queries (add indexes, reduce joins, use LIMIT)
2. Add caching (server-side or HTTP Cache-Control headers)
3. Reduce data payload (return only what's needed)
4. Use parallel queries with Promise.all()
5. If regression is intentional, update baseline with justification

Baseline location: tests/performance/baselines.ts
```

**Performance Baselines** (from `tests/performance/baselines.ts`):
| Endpoint | P50 Target | P95 Target |
|----------|-----------|-----------|
| `/api/projects/:id/dashboard` | <200ms | <500ms |
| `/api/global/dashboard` | <300ms | <800ms |
| `/api/projects` | <100ms | <300ms |
| `/api/projects/:id/data` | <500ms | <1500ms |

**For manual verification:** Run `/verify-performance` for detailed performance analysis.

---

### Phase 5: Code Standards Review [BLOCKING]

#### 5.1 CSS Modules Pattern

```bash
# Check for inline styles instead of CSS Modules
git diff HEAD -- 'src/**/*.tsx' | grep -E "style=\{\{"

# Check for new components without .module.css
git diff --name-only HEAD | grep "src/components/.*\.tsx$" | while read file; do
  module_file="${file%.tsx}.module.css"
  [ ! -f "$module_file" ] && echo "Missing: $module_file for $file"
done

# Check CSS imports (should be .module.css)
git diff HEAD -- 'src/**/*.tsx' | grep "import.*\.css" | grep -v "\.module\.css"
```

**Flag if found**:
- 📝 **BLOCKING**: Inline styles (should use CSS Modules)
- 📝 **BLOCKING**: New components without corresponding `.module.css` files
- 📝 **BLOCKING**: Importing non-module CSS in components

**Auto-fix**: Available for simple cases - extract inline styles to CSS Module

**CSS Variables to use** (from `src/styles/global.css`):
- Spacing: `var(--space-1)` to `var(--space-8)`
- Typography: `var(--text-xs)` to `var(--text-2xl)`
- Colors: `var(--color-bg)`, `var(--color-primary)`, `var(--color-text)`
- Borders: `var(--radius-sm)`, `var(--radius-md)`, `var(--radius-lg)`

#### 5.2 API Route Patterns

```bash
# Check for missing withAuth/withAdmin wrappers
git diff HEAD -- 'app/api/**/*.ts' | grep -E "export const (GET|POST|PATCH|DELETE)" -B 1 | grep -v "withAuth\|withAdmin\|export"

# Check for direct NextResponse instead of helpers
git diff HEAD -- 'app/api/**/*.ts' | grep "NextResponse\.json" | grep -v "jsonResponse\|errorResponse\|import"

# Check for missing project ownership verification
git diff HEAD -- 'app/api/projects/\[id\]/**/*.ts' | grep "export const" -A 10 | grep -v "user_id = \$2\|projects WHERE.*user_id"
```

**Flag if found**:
- 📝 **BLOCKING**: Routes not using `withAuth` or `withAdmin` wrappers
- 📝 **BLOCKING**: Direct `NextResponse.json()` instead of `jsonResponse` or `errorResponse`
- 📝 **BLOCKING**: Missing project ownership verification in `/projects/[id]` routes

**Auto-fix**: Available for adding imports and simple wrapper additions

**API Pattern** (from CLAUDE.md):
```typescript
export const POST = withAuth(async (request, { user, params }) => {
  const body = await request.json();
  const validation = createSchema.safeParse(body);
  if (!validation.success) {
    return errorResponse(validation.error.errors[0].message);
  }
  // ... implementation
  return jsonResponse({ item }, 201);
});
```

#### 5.3 Database Query Patterns

```bash
# Check for raw pg Pool usage instead of query helpers
git diff HEAD -- 'app/api/**/*.ts' 'lib/**/*.ts' | grep -E "Pool|Client|pg\." | grep -v "import|from"

# Check for non-parameterized queries
git diff HEAD -- 'app/api/**/*.ts' 'lib/**/*.ts' | grep -E "query\(|queryOne\(" -A 1 | grep -E "^[+]" | grep -v "\$[0-9]"

# Check for snake_case conversion issues
git diff HEAD -- 'app/api/**/*.ts' | grep -E "user_id|project_id|created_at|updated_at" | grep -v "SELECT|WHERE|FROM|INSERT"
```

**Flag if found**:
- 📝 **BLOCKING**: Direct `pg.Pool` usage instead of `query`/`queryOne` helpers
- 📝 **BLOCKING**: Missing parameterization in queries
- 💡 **OPTIMIZATION**: Not following snake_case (DB) → camelCase (API) pattern

**Auto-fix**: Not available - requires query refactoring

#### 5.4 File Naming and Structure

```bash
# Check component files are PascalCase
git diff --name-only HEAD | grep "src/components/.*\.tsx$" | grep -v "^[A-Z]" | grep -v "/[A-Z]"

# Check for orphaned CSS Modules
git diff --name-only HEAD | grep "\.module\.css$" | while read css; do
  component="${css%.module.css}.tsx"
  [ ! -f "$component" ] && echo "Orphaned CSS Module: $css (no matching .tsx)"
done
```

**Flag if found**:
- 📝 **BLOCKING**: Component files not in PascalCase
- 💡 **OPTIMIZATION**: CSS Modules without matching component files

**Auto-fix**: Not available - requires file renaming

#### 5.5 Unused Components Detection

```bash
# Find components that are never imported anywhere else in the codebase
# For each .tsx file in src/components/, check if it's imported elsewhere

find src/components -name "*.tsx" -type f | while read component; do
  # Get the component name (filename without extension)
  name=$(basename "$component" .tsx)

  # Skip index files and test files
  if [[ "$name" == "index" ]] || [[ "$name" == *.test* ]] || [[ "$name" == *.spec* ]]; then
    continue
  fi

  # Search for imports of this component (excluding its own file)
  imports=$(grep -r "from.*['\"].*$name['\"]" --include="*.tsx" --include="*.ts" . 2>/dev/null | grep -v "$component" | grep -v "node_modules" | wc -l)

  # Also check for named imports
  named_imports=$(grep -r "import.*{.*$name.*}" --include="*.tsx" --include="*.ts" . 2>/dev/null | grep -v "$component" | grep -v "node_modules" | wc -l)

  total=$((imports + named_imports))

  if [ "$total" -eq 0 ]; then
    echo "UNUSED: $component"
  fi
done
```

**Flag if found**:
- 🗑️ **CLEANUP**: Component files that are never imported (dead code)
- 🗑️ **CLEANUP**: CSS Modules for unused components

**Auto-fix**: Not available - requires confirmation before deletion

**Manual fix guidance**:
```
Found: src/components/common/UnusedWidget.tsx (never imported)

Options:
1. DELETE if truly unused: rm src/components/common/UnusedWidget.tsx src/components/common/UnusedWidget.module.css
2. KEEP if planned for future use (add TODO comment explaining intent)
3. INTEGRATE if it should be used somewhere
```

**When to ignore**:
- Components exported from index.ts barrel files for external use
- Components used dynamically (string-based imports)
- Components under active development (check git history)

---

### Phase 5.5: Analytics Tracking Coverage [WARNING]

Check that new features and pages have appropriate analytics tracking.

#### 5.5.1 New Pages Missing Page View Tracking

```bash
# Find new page.tsx files without tracking imports
git diff --name-only HEAD | grep -E "app/.*page\.tsx$" | while read file; do
  if ! grep -q "trackFeatureUse\|useAnalytics\|useDemoAnalytics\|usePublicAnalytics" "$file" 2>/dev/null; then
    echo "MISSING TRACKING: $file"
  fi
done
```

**Flag if found**:
- ⚠️ **WARNING**: New pages without analytics tracking

#### 5.5.2 New Lite/Demo Components Missing Tracking

```bash
# Check lite components for demo analytics
git diff --name-only HEAD | grep -E "src/components/lite/.*\.tsx$" | while read file; do
  if ! grep -q "useDemoAnalytics\|trackFeatureUse" "$file" 2>/dev/null; then
    echo "MISSING DEMO TRACKING: $file"
  fi
done
```

**Flag if found**:
- ⚠️ **WARNING**: Lite/demo components without useDemoAnalytics

#### 5.5.3 New Feature Constants Missing Display Config

```bash
# Check if AnalyticsFeatures has entries not in FEATURE_CATEGORIES
# Get feature IDs from useAnalytics.ts and compare with EngagementChart.tsx

# Get feature IDs from useAnalytics.ts (values like 'quick_capture')
grep -E ":\s*'[a-z_]+'" hooks/useAnalytics.ts | sed "s/.*'\([^']*\)'.*/\1/" | sort > /tmp/analytics_features.txt

# Get feature IDs from EngagementChart.tsx
grep -E "^\s+[a-z_]+:\s*\{" src/components/admin/analytics/EngagementChart.tsx | sed "s/^\s*\([a-z_]*\):.*/\1/" | sort > /tmp/engagement_features.txt

# Find features missing from display config
comm -23 /tmp/analytics_features.txt /tmp/engagement_features.txt
```

**Flag if found**:
- ⚠️ **WARNING**: Feature constants without display config in EngagementChart

#### 5.5.4 Marketing Pages Without Public Analytics

```bash
# Check marketing/public pages for analytics
git diff --name-only HEAD | grep -E "app/(marketing|features|pricing|changelog)/.*\.tsx$" | while read file; do
  if ! grep -q "usePublicAnalytics\|useDemoAnalytics\|trackFeatureUse" "$file" 2>/dev/null; then
    echo "MISSING PUBLIC ANALYTICS: $file"
  fi
done
```

**Flag if found**:
- ⚠️ **WARNING**: Marketing pages without public analytics

**Auto-fix**: Not available - requires manual implementation

**Manual fix guidance**:
```
Found: New page app/features/new-feature/page.tsx without tracking

Fix for authenticated pages:
  import { useAnalytics, AnalyticsFeatures, AnalyticsActions } from '@/hooks/useAnalytics';
  const { trackFeatureUse } = useAnalytics();
  useEffect(() => { trackFeatureUse(AnalyticsFeatures.MY_FEATURE, AnalyticsActions.VIEWED); }, []);

Fix for public/marketing pages:
  import { useDemoAnalytics, DemoFeatures, DemoActions } from '@/hooks/useDemoAnalytics';
  const { trackDemoEvent } = useDemoAnalytics();
  useEffect(() => { trackDemoEvent(DemoFeatures.MARKETING_FEATURES, DemoActions.VIEWED); }, []);

Don't forget to add display config to EngagementChart.tsx:
  my_feature: { label: 'My Feature', color: '#6366f1' },
```

**Key files to reference**:
- `hooks/useAnalytics.ts` - AnalyticsFeatures constants
- `hooks/useDemoAnalytics.ts` - DemoFeatures for public pages
- `src/components/admin/analytics/EngagementChart.tsx` - FEATURE_CATEGORIES display config

---

### Phase 6: Present Findings

Present all findings in a clear, interactive format:

```markdown
## 🔍 Verification Results

### 🔒 Security Issues [BLOCKING] - X found
- [ ] ❌ **Hardcoded Secret** in app/config.ts:23
  Found: `DATABASE_URL="postgres://user:pass@host/db"`
  Fix: Move to .env.local and use process.env.DATABASE_URL
  Auto-fix: ❌ Not available

- [ ] ❌ **SQL Injection Risk** in app/api/users/route.ts:45
  Found: query(\`SELECT * FROM users WHERE email = ${email}\`)
  Fix: query('SELECT * FROM users WHERE email = $1', [email])
  Auto-fix: ❌ Not available

- [ ] ❌ **Missing Rate Limit** in app/api/auth/login/route.ts:15
  POST /api/auth/login has no rate limiting
  Fix: Add withRateLimit(request, rateLimits.strict, 'login')
  Auto-fix: ✅ Available

### ⚠️ Best Practices [BLOCKING] - Y found
- [ ] ⚠️ **Debug Code** - 3 console.log found
  - src/components/Dashboard.tsx:45
  - src/components/Dashboard.tsx:78
  - src/components/build/BuildPanel.tsx:123
  Auto-fix: ✅ Available - will remove all

- [ ] ⚠️ **TypeScript** - 2 `: any` types found
  - src/hooks/useApi.ts:34 - Consider defining proper interface
  - app/api/projects/[id]/route.ts:67 - Define type for params
  Auto-fix: ❌ Not available

### 💡 Efficiency [OPTIMIZATION] - Z found
- [ ] 💡 **React Hook** - Inline function in onClick
  src/components/objectives/ObjectiveCard.tsx:45
  Recommendation: Extract to useCallback to prevent re-renders
  Auto-fix: ❌ Not available

### 🔧 Refactor Candidates [REFACTOR] - R found
- [ ] 🔧 **Large Component** (487 lines): src/components/Dashboard.tsx
  Recommendation: Extract sub-components (DashboardStats, DashboardActions)
  Auto-fix: ❌ Not available

- [ ] 🔧 **Very Large File** (892 lines): src/context/AppContext.tsx
  Recommendation: Extract entity hooks to separate files (useInitiatives.ts, etc.)
  Priority: HIGH
  Auto-fix: ❌ Not available

- [ ] 🔧 **Many Functions** (14 functions): lib/api-utils.ts
  Recommendation: Group related functions into sub-modules
  Auto-fix: ❌ Not available

### 📝 Code Standards [BLOCKING] - W found
- [ ] 📝 **CSS Modules** - Inline style found
  src/components/common/Badge.tsx:12
  Found: style={{ backgroundColor: color }}
  Fix: Move to Badge.module.css
  Auto-fix: ✅ Available

- [ ] 📝 **API Pattern** - Missing Zod validation
  app/api/initiatives/[id]/route.ts:23
  POST route has no input validation
  Fix: Define updateSchema with z.object()
  Auto-fix: ❌ Not available (schema needs manual definition)

---

**Summary:**
- 🚨 3 Security Issues (BLOCKING)
- ⚠️ 5 Best Practice Issues (BLOCKING)
- 💡 1 Efficiency Issue (optimization only)
- 🔧 3 Refactor Candidates (1 HIGH priority)
- 📝 2 Code Standard Issues (BLOCKING)

**Total Blocking Issues: 10** - Must be resolved to proceed with commit
**Refactor Candidates: 3** - Not blocking, but recommended for maintainability

**Auto-fix Available:**
- ✅ Remove 3 console.logs
- ✅ Add rate limiting to auth route
- ✅ Convert inline style to CSS Module

**Actions:**
1. Type 'fix all' - Auto-fix all available issues (5 issues)
2. Type 'fix N' - Fix specific issue number N
3. Type 'show fix N' - Preview fix for issue N without applying
4. Fix blocking issues manually, then type 'verify' to re-run
5. Type 'approve override' - Override and proceed (NOT RECOMMENDED for security issues)
```

---

### Phase 7: Auto-Fix Implementation

When user requests auto-fix, apply available corrections:

#### Auto-fix 1: Remove Console Statements

```bash
# Get list of files with console.logs
files=$(git diff --name-only HEAD)

# Remove console statements from each file
for file in $files; do
  if [ -f "$file" ]; then
    # Remove console.log, console.warn, console.error, console.info, console.debug
    sed -i.bak '/^\s*console\.\(log\|warn\|error\|info\|debug\)/d' "$file"

    # Remove inline console calls on same line as other code
    sed -i.bak 's/;\s*console\.\(log\|warn\|error\|info\|debug\)([^)]*);/;/g' "$file"

    # Clean up backup
    rm -f "$file.bak"
  fi
done

echo "✅ Removed all console statements"
```

#### Auto-fix 2: Remove TODO Comments

```bash
files=$(git diff --name-only HEAD)

for file in $files; do
  if [ -f "$file" ]; then
    # Remove standalone TODO/FIXME comment lines
    sed -i.bak '/^\s*\/\/\s*\(TODO\|FIXME\|XXX\|HACK\)/d' "$file"
    rm -f "$file.bak"
  fi
done

echo "✅ Removed TODO/FIXME comments"
```

#### Auto-fix 3: Remove Commented Code

```bash
# Note: Only remove obvious commented code blocks (3+ lines)
# Manual review recommended for complex cases

echo "⚠️ Commented code removal requires manual review"
echo "Review and manually delete commented code blocks"
```

#### Auto-fix 4: Convert Inline Styles to CSS Modules

```typescript
// This requires programmatic code analysis and transformation
// Not suitable for bash script - would need Edit tool with careful analysis

// Example transformation:
// Before: <div style={{ padding: '20px', color: 'red' }}>
// After:
//   - Component: <div className={styles.container}>
//   - CSS Module: .container { padding: var(--space-4); color: var(--color-danger); }

echo "⚠️ Inline style conversion requires Edit tool"
echo "Will be applied via Edit tool for each occurrence"
```

#### Auto-fix 5: Add Missing API Helpers

Use the Edit tool to:
1. Add imports: `import { errorResponse, jsonResponse } from '@/lib/api-utils';`
2. Replace `NextResponse.json({ error }, { status })` with `errorResponse(error, status)`
3. Replace `NextResponse.json({ data }, { status })` with `jsonResponse({ data }, status)`

#### Auto-fix 6: Add Rate Limiting

Use the Edit tool to add rate limiting after route wrapper:

```typescript
// Add import
import { withRateLimit, rateLimits } from '@/lib/rate-limit';

// Add check at start of route handler
export const POST = withAuth(async (request, { user }) => {
  const rateLimitResponse = withRateLimit(request, rateLimits.strict, 'unique-key');
  if (rateLimitResponse) return rateLimitResponse;

  // ... rest of handler
});
```

---

## Quick Reference

| Category | Check | Command Pattern | Severity |
|----------|-------|-----------------|----------|
| **Security** |
| Secrets | Hardcoded credentials | `grep -iE "password\|secret\|api_key"` | 🔒 BLOCKING |
| SQL Injection | String interpolation | `grep '\${.*}' \| grep -i select` | 🔒 BLOCKING |
| Validation | Missing Zod | `grep 'request.json()' -A 3 \| grep -v safeParse` | 🔒 BLOCKING |
| Rate Limits | Missing withRateLimit | `grep 'POST' -A 10 \| grep -v withRateLimit` | 🔒 BLOCKING |
| **Best Practices** |
| Debug Code | console.log | `grep 'console\.'` | ⚠️ BLOCKING |
| TypeScript | any types | `grep ': any\|@ts-ignore'` | ⚠️ BLOCKING |
| Error Handling | Empty catch | `grep 'catch' -A 3 \| grep -v errorResponse` | ⚠️ BLOCKING |
| **Efficiency** |
| Hooks | Missing deps | `grep 'useEffect' -A 5 \| grep -v '\[\]'` | 💡 OPTIMIZATION |
| Re-renders | Inline functions | `grep 'onClick={\|onChange={'` | 💡 OPTIMIZATION |
| **Database Performance** |
| N+1 Queries | Loop + await query | `grep -E "forEach\|map" -A 10 \| grep query` | 🐢 BLOCKING |
| Unbounded SELECT | No LIMIT/ID filter | `grep "SELECT" \| grep -v "LIMIT\|WHERE.*id"` | 🐢 BLOCKING |
| Missing Index | LIKE '%...' | `grep "LIKE.*%"` | ⏱️ WARNING |
| **API Performance** |
| Response Time | Exceeds P50 threshold | `npm test tests/performance/` | 🏎️ BLOCKING |
| Regression | >50% slower than baseline | Compare with baselines.ts | 🏎️ BLOCKING |
| **Refactor** |
| Large Files | 500+ lines | `wc -l < file` | 🔧 REFACTOR |
| Large Components | 300+ lines (.tsx) | `wc -l < file` | 🔧 REFACTOR |
| Many Functions | 10+ per file | `grep -c "function\|const.*=.*("` | 🔧 REFACTOR |
| Very Large Files | 800+ lines | `wc -l < file` | 🔧 REFACTOR (HIGH) |
| **Standards** |
| CSS Modules | Inline styles | `grep 'style={{' src/**/*.tsx` | 📝 BLOCKING |
| API Pattern | Missing helpers | `grep 'NextResponse.json' \| grep -v jsonResponse` | 📝 BLOCKING |
| DB Queries | Parameterization | `grep 'query' -A 2 \| grep -v '\$[0-9]'` | 📝 BLOCKING |
| Unused Components | Never imported | `find + grep import pattern` | 🗑️ CLEANUP |
| **Analytics** |
| Page Tracking | New pages without tracking | `grep trackFeatureUse\|useAnalytics` | ⚠️ WARNING |
| Lite Components | Missing useDemoAnalytics | `grep useDemoAnalytics` | ⚠️ WARNING |
| Display Config | Features missing from EngagementChart | Compare constants | ⚠️ WARNING |

---

## Example Flow

```
User: /verify-work

Claude: I'll verify all your changes for security, best practices, efficiency, and code standards.

[Runs Phase 1: Analyze Changed Files]

Found 8 changed files:
- 3 API routes (app/api/*)
- 4 components (src/components/*)
- 1 type definition (src/types/index.ts)

[Runs Phases 2-5: All Checks in parallel]

[Presents Phase 6: Findings Report]

## 🔍 Verification Results

### 🔒 Security Issues [BLOCKING] - 1 found
- [ ] ❌ **Missing Rate Limit** in app/api/auth/login/route.ts:15
  Auto-fix: ✅ Available

### ⚠️ Best Practices [BLOCKING] - 2 found
- [ ] ⚠️ **Debug Code** - 2 console.logs
  Auto-fix: ✅ Available

### 💡 Efficiency [OPTIMIZATION] - 0 found
✅ All hooks properly configured
✅ No obvious re-render issues

### 📝 Code Standards [BLOCKING] - 0 found
✅ All components use CSS Modules
✅ All API routes follow project patterns

---

**Summary:** 1 security + 2 best practice = 3 blocking issues

**Actions:**
1. Type 'fix all' to auto-fix all 3 issues
2. Type 'verify' to re-run after manual fixes
3. All issues have auto-fix available!

User: fix all

Claude: Applying auto-fixes...

✅ Added rate limiting to app/api/auth/login/route.ts
✅ Removed 2 console.log statements from src/components/Dashboard.tsx

All issues resolved! Re-running verification...

[Phase 6: Re-verify]

## 🔍 Verification Results

✅ **All checks passed!**

- 🔒 Security: No issues
- ⚠️ Best Practices: No issues
- 💡 Efficiency: No issues
- 📝 Code Standards: No issues

Ready to proceed with `/ship`!
```

---

## Notes

- This skill runs **automatically** as Phase 0 of `/ship` (mandatory)
- **Security issues** are BLOCKING - must be resolved before commit
- **Best practice issues** are BLOCKING - ensures code quality
- **Code standard issues** are BLOCKING - maintains consistency
- **Efficiency issues** are OPTIMIZATION - recommended but not blocking
- All checks respect project conventions from CLAUDE.md
- Auto-fix capability for common issues (console.logs, rate limiting, etc.)
- Manual fix guidance provided for complex issues (SQL injection, Zod schemas, etc.)
- Use `approve override` to bypass (NOT RECOMMENDED - only for emergencies)
- The skill is read-only until user approves fixes
- Verification can be re-run with `/verify-work` after making manual fixes
- Supports preview mode: `show fix N` to see changes before applying

---

## Integration with /ship

This skill integrates as **Phase 0** of the `/ship` workflow:

**Phase 0: Verify Work** → **Phase 1: Organize Commits** → **Phase 2: Update Roadmap** → **Phase 3: Import to App**

Cannot proceed to Phase 1 until all BLOCKING issues are resolved or explicitly overridden.