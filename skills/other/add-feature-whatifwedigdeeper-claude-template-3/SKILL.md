---
skill: add-feature
description: Add new feature with full validation in isolated worktree
arguments: feature name
---

# Add Feature: $ARGUMENTS

Create a complete new feature with component, tests, and integration.

## Process

### 1. Create Isolated Worktree

```bash
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
WORKTREE_PATH="../add-feature-$ARGUMENTS-$TIMESTAMP"
git worktree add "$WORKTREE_PATH" -b "feature-$ARGUMENTS-$TIMESTAMP"
cd "$WORKTREE_PATH"
```

### 2. Create Feature Files

Generate based on feature name (convert to PascalCase for component):

- `components/[FeatureName].tsx` - Main React component with `data-testid`
- `components/[FeatureName].test.tsx` - Unit tests (happy path, edge cases, errors)
- `tests/e2e/[feature-name].spec.ts` - E2E tests with Playwright
- Update `types/index.ts` if new types needed

### 3. Integrate into App

- Import and add component to appropriate page/layout
- Wire up props and event handlers

### 4. Validate

Run in order, collect all errors:
```bash
npm run build
npm run lint
npm test
npm run test:e2e
```

### 5. Report and Prompt

**On success**: Show summary, prompt to merge or keep for review
**On failure**: Categorize errors (build/lint/test), provide remediation steps

### 6. Cleanup

If merging:
```bash
git checkout main
git merge "feature-$ARGUMENTS-$TIMESTAMP"
git worktree remove "$WORKTREE_PATH"
```

## Component Template

```tsx
'use client';

import { useState } from 'react';

interface FeatureNameProps {
  // props
}

export default function FeatureName({}: FeatureNameProps) {
  return (
    <div data-testid="feature-name">
      {/* content */}
    </div>
  );
}
```

## Test Patterns

- Use `data-testid` for selectors
- Test: rendering, user interactions, props, edge cases, accessibility
- Clear localStorage in E2E beforeEach
