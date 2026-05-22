---
name: review-clean-code
description: 'Analyze code quality based on "Clean Code" principles. Identify naming, function size, duplication, over-engineering, and magic number issues with severity ratings and refactoring suggestions. Use when the user requests code quality checks, refactoring advice, Clean Code analysis, code smell detection, or mentions terms like code review, code quality, refactoring check.'
---

# Clean Code Review

Focused on 7 high-impact review dimensions based on "Clean Code" principles.

## Review Workflow

```
Review Progress:
- [ ] 1. Scan codebase: identify files to review
- [ ] 2. Check each dimension (naming, functions, DRY, YAGNI, magic numbers, clarity, conventions)
- [ ] 3. Rate severity (High/Medium/Low) for each issue
- [ ] 4. Generate report sorted by severity
```

## Core Principle: Preserve Functionality

All suggestions target **implementation approach** only—never suggest changing the code's functionality, output, or behavior.

## Check Dimensions

### 1. Naming Issues (Meaningful Names)

Check for:
- Meaningless names like `data1`, `temp`, `result`, `info`, `obj`
- Inconsistent naming for same concepts (`get`/`fetch`/`retrieve` mixed)

```typescript
// ❌ 
const d = new Date();
const data1 = fetchUser();

// ✅ 
const currentDate = new Date();
const userProfile = fetchUser();
```

### 2. Function Issues (Small Functions + SRP)

Check for:
- Functions exceeding **100 lines**
- More than **3 parameters**
- Functions doing multiple things

```typescript
// ❌ 7 parameters
function processOrder(user, items, address, payment, discount, coupon, notes)

// ✅ Use parameter object
interface OrderParams { user: User; items: Item[]; shipping: Address; payment: Payment }
function processOrder(params: OrderParams)
```

### 3. Duplication Issues (DRY)

Check for:
- Similar if-else structures
- Similar data transformation/error handling logic
- Copy-paste traces

### 4. Over-Engineering (YAGNI)

Check for:
- `if (config.legacyMode)` branches that are never true
- Interfaces with only one implementation
- Useless try-catch or if-else

```typescript
// ❌ YAGNI violation: unused compatibility code
if (config.legacyMode) {
  // 100 lines of compatibility code
}
```

### 5. Magic Numbers (Avoid Hardcoding)

Check for:
- Bare numbers without explanation
- Hardcoded strings

```typescript
// ❌ 
if (retryCount > 3) // What is 3?
setTimeout(fn, 86400000) // How long is this?

// ✅ 
const MAX_RETRY_COUNT = 3;
const ONE_DAY_MS = 24 * 60 * 60 * 1000;
```

### 6. Structural Clarity (Readability First)

Check for:
- Nested ternary operators
- Overly compact one-liners
- Deep conditional nesting (> 3 levels)

```typescript
// ❌ Nested ternary
const status = a ? (b ? 'x' : 'y') : (c ? 'z' : 'w');

// ✅ Use switch or if/else
function getStatus(a, b, c) {
  if (a) return b ? 'x' : 'y';
  return c ? 'z' : 'w';
}
```

### 7. Project Conventions (Consistency)

Check for:
- Mixed import order (external libs vs internal modules)
- Inconsistent function declaration styles
- Mixed naming conventions (camelCase vs snake_case)

```typescript
// ❌ Inconsistent style
import { api } from './api'
import axios from 'axios'  // External lib should come first
const handle_click = () => { ... }  // Mixed naming style

// ✅ Unified style
import axios from 'axios'
import { api } from './api'
function handleClick(): void { ... }
```

> [!TIP]
> Project conventions should refer to `CLAUDE.md`, `AGENTS.md`, or project-defined coding standards.

## Severity Levels

| Level | Criteria |
|-------|----------|
| High | Affects maintainability/readability, should fix immediately |
| Medium | Room for improvement, recommended fix |
| Low | Code smell, optional optimization |

## Output Format

```markdown
### [Issue Type]: [Brief Description]

- **Principle**: [Clean Code principle]
- **Location**: `file:line`
- **Severity**: High/Medium/Low
- **Issue**: [Specific description]
- **Suggestion**: [Fix direction]
```

## Artifacts (Pipeline Mode)

- Output: `clean-code-review.md` (human-readable report)
- Output: `clean-code-review.json` (structured issue list for aggregation/deduplication/statistics)

## References

**Detailed examples**: See [detailed-examples.md](detailed-examples.md)
- Complete cases for each dimension (naming, functions, DRY, YAGNI, magic numbers)

**Language patterns**: See [language-patterns.md](language-patterns.md)
- TypeScript/JavaScript common issues
- Python common issues
- Go common issues

## Multi-Agent Parallel

Split by the following dimensions for parallel multi-agent execution:

1. **By check dimension** - One agent per dimension (7 total)
2. **By module/directory** - One agent per module
3. **By language** - One agent each for TypeScript, Python, Go
4. **By file type** - Components, hooks, utilities, type definitions

Example: `/review-clean-code --scope=components` or `--dimension=naming`

Deduplication and unified severity rating needed when aggregating.
