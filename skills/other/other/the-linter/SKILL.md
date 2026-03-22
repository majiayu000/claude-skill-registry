---
name: the-linter
description: Identifies and fixes ESLint errors and TypeScript type issues across the codebase.
license: HPL3-ECO-NC-ND-A 2026
---

Task: Run ESLint, identify all errors and warnings, and fix them systematically.

Role: You're a code quality engineer focused on maintaining clean, consistent, and type-safe code.

## Execution Steps

1. **Run ESLint check**
   ```bash
   npm run lint 2>&1 | head -200
   ```

2. **Analyze errors** - Group by:
   - TypeScript type errors
   - ESLint rule violations
   - Unused imports/variables
   - Missing dependencies

3. **Fix in priority order**:
   - Type errors (highest priority)
   - Security-related warnings
   - Unused code removal
   - Style/formatting issues

4. **Verify fixes**
   ```bash
   npm run lint
   ```

## Common Fixes

### TypeScript Errors
- Add explicit types for function parameters
- Use `unknown` instead of implicit `any`
- Add null checks for optional values
- Fix type mismatches in props

### ESLint Rules
- `@typescript-eslint/no-explicit-any` → Use proper types
- `@typescript-eslint/no-unused-vars` → Remove or prefix with `_`
- `react-hooks/exhaustive-deps` → Add missing dependencies
- `@next/next/no-img-element` → Use `next/image`

### Import Organization
```typescript
// 1. External packages
import { useState } from 'react'
import { NextResponse } from 'next/server'

// 2. Internal aliases
import { Button } from '@/components/ui/button'
import prisma from '@/lib/prisma'

// 3. Relative imports
import { helper } from './utils'

// 4. Type imports
import type { User } from '@/lib/types'
```

## Rules
- Fix errors without changing functionality
- Preserve existing code patterns
- Don't introduce new dependencies
- Keep changes minimal and focused
- Run lint after each batch of fixes to verify

## Do NOT
- Refactor unrelated code
- Change business logic
- Add new features
- Modify test files unless fixing lint errors in them
