---
name: lint-fixer
description: Expert assistant for analyzing and fixing linting and formatting issues in the KR92 Bible Voice project using Biome and TypeScript. Use when fixing lint errors, resolving TypeScript issues, applying code formatting, or reviewing code quality.
---

# Lint Fixer

## Capabilities
- Analyze Biome lint errors, warnings, and infos
- Auto-fix safe linting issues
- Review and apply TypeScript strict mode fixes
- Explain linting rules and best practices
- Batch fix common patterns

## Linting Tools

### Biome
The project uses Biome for linting and formatting:
```bash
npx @biomejs/biome lint .           # Check for lint issues
npx @biomejs/biome lint . --write   # Auto-fix safe issues
npx @biomejs/biome format .         # Format code
npx @biomejs/biome check --write .  # Lint + format
```

### TypeScript
```bash
npx tsc --noEmit                    # Type checking
npm run typecheck                   # Same as above
```

## Common Biome Issues

### 1. Template Literals (useTemplate)
**Issue:** String concatenation should use template literals

**Before:**
```javascript
alert('Error: ' + err.message);
const url = baseUrl + '/' + endpoint;
```

**After:**
```javascript
alert(`Error: ${err.message}`);
const url = `${baseUrl}/${endpoint}`;
```

### 2. Const Declarations (useConst)
**Issue:** Variables that are never reassigned should use `const`

**Before:**
```javascript
let value = 10;
let result = calculate();
```

**After:**
```javascript
const value = 10;
const result = calculate();
```

### 3. Unused Variables (noUnusedVariables)
**Issue:** Variables declared but never used

**Fix:**
```typescript
// Remove if truly unused
// const unused = value;

// Or prefix with _ if intentionally unused
const _intentionallyUnused = value;
```

### 4. Console Statements (noConsole)
**Issue:** Console statements in production code

**Fix:**
```typescript
// Remove or conditionally include
if (process.env.NODE_ENV === 'development') {
  console.log('Debug info');
}

// Or use proper logging
logger.debug('Debug info');
```

### 5. Any Type (noExplicitAny)
**Issue:** Using `any` type instead of specific types

**Before:**
```typescript
function process(data: any) {
  return data.value;
}
```

**After:**
```typescript
interface Data {
  value: string;
}

function process(data: Data) {
  return data.value;
}

// Or use unknown for truly dynamic data
function process(data: unknown) {
  if (isData(data)) {
    return data.value;
  }
}
```

### 6. Non-Null Assertions (noNonNullAssertion)
**Issue:** Using `!` non-null assertion

**Before:**
```typescript
const element = document.getElementById('app')!;
```

**After:**
```typescript
const element = document.getElementById('app');
if (!element) {
  throw new Error('Element not found');
}
```

## Usage Examples

### Example 1: Auto-Fix Safe Issues
**User:** "Fix all safe linting issues"

**Assistant:**
```bash
# Run Biome with auto-fix
npx @biomejs/biome check --write .

# Review changes
git diff

# If changes look good, commit
git add .
git commit -m "fix: apply Biome auto-fixes"
```

### Example 2: Fix Template Literal Issues
**User:** "Fix the template literal warnings"

**Assistant:**
I'll fix the string concatenation issues. Looking at the error:

```javascript
// public/embed-test.html:413
alert('Audion toisto epäonnistui: ' + err.message);
```

Let me fix this:

```javascript
// Replace with template literal
alert(`Audion toisto epäonnistui: ${err.message}`);
```

For batch fixing similar issues, I can use Find & Replace pattern:
- Find: `'([^']*?)'\s*\+\s*([^;]+)`
- Replace: `` `$1${$2}` ``

### Example 3: Fix TypeScript Errors
**User:** "I have TypeScript errors in my component"

**Assistant:**
Let me check the TypeScript errors:

```bash
npx tsc --noEmit 2>&1 | head -20
```

Common fixes:

**Missing type annotations:**
```typescript
// Before
const handleClick = (e) => {
  console.log(e);
};

// After
const handleClick = (e: React.MouseEvent<HTMLButtonElement>) => {
  console.log(e);
};
```

**Implicit any:**
```typescript
// Before
const data = await response.json();

// After
interface ApiResponse {
  success: boolean;
  data: any; // Define proper type
}
const data: ApiResponse = await response.json();
```

### Example 4: Batch Fix Const Issues
**User:** "Convert all `let` to `const` where possible"

**Assistant:**
```bash
# First, let Biome auto-fix
npx @biomejs/biome check --write .

# For remaining cases, manual review needed
# Search for: let (\w+) =
# Review each case to ensure variable isn't reassigned
```

### Example 5: Clean Up Console Statements
**User:** "Remove or fix console.log statements"

**Assistant:**

Strategy:
1. **Development logs** - Wrap in environment check
2. **Debug logs** - Remove or convert to proper logging
3. **Error logs** - Keep but use console.error

```typescript
// Development only
if (import.meta.env.DEV) {
  console.log('Debug:', data);
}

// Remove debug logs
// console.log('Testing'); // ❌ Remove

// Keep error logs
console.error('Failed to load:', error); // ✅ Keep

// Better: Use proper error handling
try {
  await operation();
} catch (error) {
  console.error('Operation failed:', error);
  toast({
    title: "Error",
    description: error.message,
    variant: "destructive"
  });
}
```

## Biome Configuration

The project likely has a `biome.json` config file:

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "vcs": {
    "enabled": true,
    "clientKind": "git",
    "useIgnoreFile": true
  },
  "files": {
    "ignoreUnknown": false,
    "ignore": ["node_modules", "dist", ".next", "build"]
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "style": {
        "useTemplate": "error",
        "useConst": "error"
      },
      "suspicious": {
        "noExplicitAny": "warn",
        "noConsole": "warn"
      }
    }
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "semicolons": "always"
    }
  }
}
```

## Workflow for Fixing Lint Issues

### Step 1: Assess the Damage
```bash
# Run lint check
npx @biomejs/biome lint .

# Count issues by severity
npx @biomejs/biome lint . 2>&1 | grep -c "error"
npx @biomejs/biome lint . 2>&1 | grep -c "warn"
```

### Step 2: Auto-Fix Safe Issues
```bash
# Let Biome fix what it can
npx @biomejs/biome check --write .

# Check what changed
git diff --stat
```

### Step 3: Manual Fixes
```bash
# Run lint again to see remaining issues
npx @biomejs/biome lint . > lint-report.txt

# Fix manually by priority:
# 1. Errors first
# 2. Then warnings
# 3. Then infos
```

### Step 4: Verify
```bash
# Run full check
npx @biomejs/biome check .
npx tsc --noEmit

# If clean, commit
git add .
git commit -m "fix: resolve linting issues"
```

## Priority Fix Order

1. **TypeScript errors** - Breaks builds
2. **Biome errors** - Critical issues
3. **Biome warnings** - Important issues
4. **Biome infos** - Nice to have

## Common Patterns by File Type

### React Components (.tsx)
```typescript
// Common issues:
// - Missing type annotations for props
// - Unused imports
// - Console.log statements
// - Non-null assertions

// Fix template:
interface Props {
  data: DataType;
  onUpdate: (value: string) => void;
}

export const Component = ({ data, onUpdate }: Props) => {
  // No console.log here
  return <div>...</div>;
};
```

### Edge Functions (.ts)
```typescript
// Common issues:
// - Any types in request/response
// - Missing error handling types
// - String concatenation

// Fix template:
interface RequestBody {
  field: string;
}

interface ResponseData {
  success: boolean;
  data: ResultType;
}

serve(async (req: Request) => {
  try {
    const body: RequestBody = await req.json();
    // ...
    return new Response(
      JSON.stringify({ success: true, data }),
      { headers: corsHeaders }
    );
  } catch (error) {
    return new Response(
      JSON.stringify({
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error'
      }),
      { status: 500, headers: corsHeaders }
    );
  }
});
```

### Test Files
```typescript
// Often can ignore some rules
// Add to biome.json:
{
  "linter": {
    "rules": {
      "suspicious": {
        "noExplicitAny": "off"  // OK in tests
      }
    }
  }
}
```

## Ignoring Specific Issues

### Inline Comments
```javascript
// biome-ignore lint/style/useTemplate: Legacy code, will refactor later
const message = 'Error: ' + error;

// biome-ignore lint/suspicious/noExplicitAny: Third-party types
const data: any = externalLibrary.getData();
```

### File-Level Ignore
```javascript
/* biome-ignore lint/style/useTemplate: Multiple concatenations in this file */
```

## CI/CD Integration

Your GitHub Actions already runs these checks:
```yaml
# .github/workflows/ci.yml
- name: Lint
  run: |
    if npx -y @biomejs/biome --version > /dev/null 2>&1; then
      npx @biomejs/biome lint .
      npx @biomejs/biome format . --check
    fi

- name: TypeScript
  run: npm run typecheck --if-present || npx tsc --noEmit
```

## Quick Reference

| Issue Type | Command to Fix | Manual Review? |
|------------|----------------|----------------|
| Template literals | `--write` | No |
| Const declarations | `--write` | No |
| Formatting | `--write` | No |
| Unused variables | `--write` | Yes - verify not needed |
| Any types | Manual | Yes - add proper types |
| Console statements | Manual | Yes - keep errors only |
| Non-null assertions | Manual | Yes - add null checks |

## Related Documentation
- Biome: https://biomejs.dev/
- TypeScript strict mode: https://www.typescriptlang.org/tsconfig#strict
- See `Docs/04-DEV-WORKFLOW.md` for CI/CD details
