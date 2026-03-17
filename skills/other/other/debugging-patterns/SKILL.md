---
name: debugging-patterns
description: Debugging strategies and error resolution patterns. Stack trace analysis, runtime errors, build errors, network issues. Use when debugging any type of error.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Debugging Patterns - Error Resolution Best Practices

## Purpose

Expert guidance for debugging:

- **Error Analysis** - Stack traces, error messages
- **Runtime Issues** - Type errors, null references
- **Build Errors** - Compilation, bundling
- **Network Issues** - API, CORS, HTTP errors
- **Performance Bugs** - Slow operations, memory leaks

---

## Debug Process

```
1. UNDERSTAND - What should happen vs what happens
   ↓
2. REPRODUCE - Consistent steps to trigger bug
   ↓
3. ISOLATE - Narrow down to specific code
   ↓
4. IDENTIFY - Find root cause
   ↓
5. FIX - Implement solution
   ↓
6. VERIFY - Confirm fix works + no regressions
```

---

## Stack Trace Analysis

### Reading Error Stack

```
TypeError: Cannot read properties of undefined (reading 'name')
    at getUserName (src/utils/user.ts:45:23)
    at ProfileCard (src/components/ProfileCard.tsx:12:18)
    at renderWithHooks (node_modules/react-dom/...)
```

**Key Information:**

- **Error Type**: `TypeError`
- **Message**: `Cannot read properties of undefined`
- **Property**: `name`
- **Location**: `src/utils/user.ts:45:23` (file:line:column)
- **Call Stack**: Shows how we got here

### Fix Pattern

```typescript
// Error at line 45
function getUserName(user: User) {
	return user.name; // ERROR: user is undefined
}

// Fix: Add null check
function getUserName(user: User | undefined): string {
	return user?.name ?? 'Unknown';
}

// Or use assertion with clear error
function getUserName(user: User | undefined): string {
	if (!user) {
		throw new Error('User is required for getUserName');
	}
	return user.name;
}
```

---

## Common Error Patterns

### TypeError: Cannot read properties of undefined

```typescript
// Pattern: Accessing property on undefined
const name = user.profile.name;

// Fix 1: Optional chaining
const name = user?.profile?.name ?? 'Unknown';

// Fix 2: Early return
if (!user?.profile) return null;
const name = user.profile.name;

// Fix 3: Default value
const profile = user?.profile ?? { name: 'Unknown' };
```

### TypeError: X is not a function

```typescript
// Pattern: Calling non-function
onClick(); // onClick is undefined

// Fix 1: Check before calling
onClick?.();

// Fix 2: Provide default
const handleClick = onClick ?? (() => {});
handleClick();
```

### ReferenceError: X is not defined

```typescript
// Pattern: Using undefined variable
console.log(userData); // userData not imported/declared

// Fix: Import or declare
import { userData } from './data';
// or
const userData = await fetchUserData();
```

### SyntaxError: Unexpected token

```typescript
// Pattern: Invalid JSON
const data = JSON.parse(response);
// SyntaxError: Unexpected token '<'

// Fix: Check response before parsing
if (!response.ok) {
	throw new Error(`HTTP ${response.status}`);
}
const text = await response.text();
try {
	return JSON.parse(text);
} catch {
	throw new Error(`Invalid JSON: ${text.slice(0, 100)}`);
}
```

---

## TypeScript Errors

### TS2339: Property does not exist

```typescript
// Error
const env = process.env.NODE_ENV;
// Property 'NODE_ENV' does not exist on type 'ProcessEnv'

// Fix: Use bracket notation
const env = process.env['NODE_ENV'];
```

### TS2532: Object is possibly undefined

```typescript
// Error
const items = array.map((x) => x.value);
// Object is possibly 'undefined'

// Fix 1: Non-null assertion (if certain)
const items = array!.map((x) => x.value);

// Fix 2: Default value
const items = (array ?? []).map((x) => x.value);

// Fix 3: Conditional
const items = array ? array.map((x) => x.value) : [];
```

### TS2345: Argument type mismatch

```typescript
// Error
function greet(name: string) {}
greet(user.name); // Argument of type 'string | undefined'

// Fix 1: Provide default
greet(user.name ?? 'Guest');

// Fix 2: Assert
greet(user.name!);

// Fix 3: Guard
if (user.name) greet(user.name);
```

### TS7053: Index signature

```typescript
// Error
const value = obj[key];
// Element implicitly has 'any' type

// Fix: Type the index
const value = (obj as Record<string, unknown>)[key];

// Or define proper type
interface MyObj {
	[key: string]: string | undefined;
}
```

---

## Build Errors

### Module Not Found

```bash
# Error
Cannot find module './utils' or its corresponding type declarations

# Check 1: File exists?
ls src/utils.ts

# Check 2: Extension needed?
import { helper } from './utils.js';  # ESM requires extension

# Check 3: Path alias configured?
# Check tsconfig.json paths
```

### Duplicate Identifier

```bash
# Error
Duplicate identifier 'User'

# Fix: Check imports for conflicts
# May have both named and default import
import User from './User';
import { User } from './types';  # Conflict!

# Solution: Rename one
import { User as UserType } from './types';
```

### ESM/CJS Compatibility

```typescript
// Error: require is not defined in ES module
const fs = require('fs');

// Fix: Use ESM import
import fs from 'fs';
import { readFileSync } from 'fs';

// If must use require in ESM
import { createRequire } from 'module';
const require = createRequire(import.meta.url);
```

---

## Network & API Errors

### CORS Errors

```
Access to fetch at 'https://api.example.com' has been blocked by CORS policy
```

```typescript
// Server-side fix (add headers)
res.setHeader('Access-Control-Allow-Origin', 'https://yoursite.com');
res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');

// Client-side workaround (proxy in dev)
// vite.config.ts
export default {
	server: {
		proxy: {
			'/api': {
				target: 'https://api.example.com',
				changeOrigin: true,
			},
		},
	},
};
```

### HTTP Error Handling

```typescript
async function fetchWithErrorHandling<T>(url: string): Promise<T> {
	const response = await fetch(url);

	if (!response.ok) {
		// Get error details
		let message: string;
		try {
			const error = await response.json();
			message = error.message || response.statusText;
		} catch {
			message = response.statusText;
		}

		throw new Error(`${response.status} ${message}`);
	}

	return response.json();
}
```

### Network Timeout

```typescript
async function fetchWithTimeout(url: string, timeout = 5000) {
	const controller = new AbortController();
	const id = setTimeout(() => controller.abort(), timeout);

	try {
		const response = await fetch(url, { signal: controller.signal });
		clearTimeout(id);
		return response;
	} catch (error) {
		clearTimeout(id);
		if (error instanceof Error && error.name === 'AbortError') {
			throw new Error(`Request timeout after ${timeout}ms`);
		}
		throw error;
	}
}
```

---

## React Debugging

### "Cannot update a component while rendering"

```typescript
// Error: State update during render
function Component({ value }) {
	const [state, setState] = useState(0);
	setState(value); // ERROR!

	// Fix: Use useEffect
	useEffect(() => {
		setState(value);
	}, [value]);
}
```

### "Too many re-renders"

```typescript
// Error: Infinite loop
function Component() {
	const [count, setCount] = useState(0);
	setCount(count + 1); // Causes re-render, which sets count...

	// Fix: Add condition or use effect
	useEffect(() => {
		if (count < 10) {
			setCount((c) => c + 1);
		}
	}, [count]);
}
```

### "Invalid hook call"

```typescript
// Error: Hook outside component or conditional
function Component() {
	if (condition) {
		const [state] = useState(0); // ERROR!
	}
}

// Fix: Hooks must be at top level
function Component() {
	const [state] = useState(0); // OK
	if (condition) {
		// use state here
	}
}
```

---

## Debug Commands

### Git - Find Breaking Commit

```bash
# Start bisect
git bisect start
git bisect bad HEAD
git bisect good abc123  # Last known good commit

# Test and mark each commit
git bisect good  # or bad

# End bisect
git bisect reset
```

### Find Error in Code

```bash
# Search for error message
grep -rn "specific error text" src/

# Search for pattern
grep -rn "throw new Error" src/ --include="*.ts"

# Find file with symbol
grep -rn "functionName" src/ --include="*.ts" -l
```

### Bun Debugging

```bash
# Debug mode
bun --inspect src/index.ts

# With breakpoint on start
bun --inspect-brk src/index.ts

# Low memory mode (for memory issues)
bun --smol src/index.ts
```

---

## Debugging Checklist

### Before You Start

- [ ] Can you reproduce the bug?
- [ ] Do you have the exact error message?
- [ ] What changed recently? (`git log`, `git diff`)

### Investigation

- [ ] Read the full error message and stack trace
- [ ] Check the line number mentioned in error
- [ ] Add console.log at key points
- [ ] Check network tab for API errors

### After Fix

- [ ] Does the fix work for all cases?
- [ ] Did you add tests to prevent regression?
- [ ] Did you handle edge cases?

---

## Agent Integration

This skill is used by:

- **debugger** agent
- **error-stack-analyzer** agent
- **type-error-resolver** agent
- **runtime-error-fixer** agent
- **network-debugger** agent
- **build-error-fixer** agent

---

## FORBIDDEN

1. **Swallowing errors silently** - Always log or handle
2. **Using `any` to hide errors** - Fix the actual type issue
3. **`@ts-ignore` without comment** - Use `@ts-expect-error` with explanation
4. **Empty catch blocks** - At minimum, log the error
5. **Fixing symptoms not causes** - Find and fix root cause

---

## Version

- **v1.0.0** - Initial implementation based on 2024-2025 debugging patterns
