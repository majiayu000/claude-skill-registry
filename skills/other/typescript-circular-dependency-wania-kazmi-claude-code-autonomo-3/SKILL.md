---
name: typescript-circular-dependency
description: |
  Detect and resolve TypeScript/JavaScript circular import dependencies. Use when:
  (1) "Cannot access 'X' before initialization" at runtime, (2) Import returns 
  undefined unexpectedly, (3) "ReferenceError: Cannot access X before initialization",
  (4) Type errors that disappear when you change import order, (5) Jest/Vitest tests 
  fail with undefined imports that work in browser.
author: Claude Code
version: 1.0.0
date: 2024-03-10
---

# TypeScript Circular Dependency Detection and Resolution

## Problem

Circular dependencies occur when module A imports from module B, which imports 
(directly or indirectly) from module A. TypeScript compiles successfully, but at 
runtime, one of the imports evaluates to `undefined` because the module hasn't 
finished initializing yet.

## Context / Trigger Conditions

Common error messages:

```
ReferenceError: Cannot access 'UserService' before initialization
```

```
TypeError: Cannot read properties of undefined (reading 'create')
```

```
TypeError: (0 , _service.doSomething) is not a function
```

Symptoms that suggest circular imports:

- Import is `undefined` even though the export exists
- Error only appears at runtime, not during TypeScript compilation
- Moving an import statement changes which import is undefined
- Tests fail but the app works (or vice versa)
- Adding `console.log` at the top of a file changes behavior

## Solution

### Step 1: Detect the Cycle

Use a tool to visualize dependencies:

```bash
# Install madge
npm install -g madge

# Find circular dependencies
madge --circular --extensions ts,tsx src/

# Generate visual graph
madge --circular --image graph.svg src/
```

Or use the TypeScript compiler:

```bash
# Check for cycles (requires tsconfig setting)
npx tsc --listFiles | head -50
```

### Step 2: Identify the Pattern

Common circular dependency patterns:

**Pattern A: Service-to-Service**
```
services/userService.ts → services/orderService.ts → services/userService.ts
```

**Pattern B: Type imports**
```
types/user.ts → types/order.ts → types/user.ts
```

**Pattern C: Index barrel files**
```
components/index.ts → components/Button.tsx → components/index.ts
```

### Step 3: Resolution Strategies

**Strategy 1: Extract Shared Dependencies**

Before:
```typescript
// userService.ts
import { OrderService } from './orderService';
export class UserService { ... }

// orderService.ts  
import { UserService } from './userService';
export class OrderService { ... }
```

After:
```typescript
// types/interfaces.ts (new file - no imports from services)
export interface IUserService { ... }
export interface IOrderService { ... }

// userService.ts
import { IOrderService } from '../types/interfaces';
export class UserService implements IUserService { ... }
```

**Strategy 2: Dependency Injection**

```typescript
// orderService.ts
export class OrderService {
  constructor(private userService: IUserService) {}
  
  // Instead of importing UserService directly
}

// main.ts
const userService = new UserService();
const orderService = new OrderService(userService);
```

**Strategy 3: Dynamic Imports**

```typescript
// Only import when needed, not at module level
async function processOrder() {
  const { UserService } = await import('./userService');
  // ...
}
```

**Strategy 4: Use Type-Only Imports**

If you only need types (not values), use type-only imports:

```typescript
// This doesn't create a runtime dependency
import type { User } from './userService';
```

**Strategy 5: Restructure Barrel Files**

Before (problematic):
```typescript
// components/index.ts
export * from './Button';
export * from './Modal';  // Modal imports Button from './index'
```

After:
```typescript
// components/Modal.tsx
import { Button } from './Button';  // Direct import, not from index
```

### Step 4: Prevent Future Cycles

Add to your CI/build process:

```json
// package.json
{
  "scripts": {
    "check:circular": "madge --circular --extensions ts,tsx src/"
  }
}
```

Or configure ESLint:

```javascript
// .eslintrc.js
module.exports = {
  plugins: ['import'],
  rules: {
    'import/no-cycle': ['error', { maxDepth: 10 }]
  }
}
```

## Verification

1. Run `madge --circular src/` - should report no cycles
2. Run your test suite - previously undefined imports should work
3. Delete `node_modules` and reinstall - app should still work
4. Build for production - no runtime errors

## Example

**Problem**: `OrderService` is undefined when imported in `UserService`

**Detection**:
```bash
$ madge --circular src/
Circular dependencies found!
  src/services/userService.ts → src/services/orderService.ts → src/services/userService.ts
```

**Fix**: Extract shared interface

```typescript
// NEW: src/types/services.ts
export interface IOrderService {
  createOrder(userId: string): Promise<Order>;
}

// MODIFIED: src/services/userService.ts
import type { IOrderService } from '../types/services';

export class UserService {
  constructor(private orderService: IOrderService) {}
}

// MODIFIED: src/services/orderService.ts  
// No longer imports UserService
export class OrderService implements IOrderService {
  async createOrder(userId: string): Promise<Order> { ... }
}
```

## Notes

- TypeScript `import type` is your friend—it's erased at runtime and can't cause cycles
- Barrel files (`index.ts`) are a common source of accidental cycles
- The order of exports in a file can matter when there's a cycle
- Jest/Vitest may handle module resolution differently than your bundler
- Some bundlers (Webpack, Vite) have better cycle handling than others
- `require()` can sometimes mask circular dependency issues that `import` exposes
