---
name: lint
description: "Run linting and fix code quality issues in the codebase"
---

# Lint

Run linting and fix code quality issues in the codebase.

## Target

$ARGUMENTS

## Lint Strategy for Solo Developers

### 1. **Run Linting Commands**

```bash
# ESLint (JavaScript/TypeScript)
npm run lint
npx eslint . --fix

# TypeScript Compiler
npx tsc --noEmit

# Prettier (formatting)
npx prettier --write .

# All together
npm run lint && npx tsc --noEmit && npx prettier --write .
```

### 2. **Common ESLint Issues**

**TypeScript Errors**
- Missing type annotations
- `any` types used
- Unused variables
- Missing return types

**React/Next.js Issues**
- Missing keys in lists
- Unsafe useEffect dependencies
- Unescaped entities in JSX
- Missing alt text on images

**Code Quality**
- Unused imports
- Console.log statements
- Debugger statements
- TODO comments

**Best Practices**
- No var, use const/let
- Prefer const over let
- No nested ternaries
- Consistent return statements

### 3. **Auto-Fix What You Can**

**Safe Auto-Fixes**
```bash
# Fix formatting
prettier --write .

# Fix ESLint auto-fixable rules
eslint --fix .

# Fix import order
eslint --fix --rule 'import/order: error' .
```

**Manual Fixes Needed**
- Type annotations
- Logic errors
- Missing error handling
- Accessibility issues

### 4. **Lint Configuration**

**ESLint Config** (`.eslintrc.json`)
```json
{
  "extends": [
    "next/core-web-vitals",
    "plugin:@typescript-eslint/recommended"
  ],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/no-unused-vars": "error",
    "no-console": "warn"
  }
}
```

**Prettier Config** (`.prettierrc`)
```json
{
  "semi": false,
  "singleQuote": true,
  "tabWidth": 2,
  "trailingComma": "es5"
}
```

### 5. **Priority Fixes**

**High Priority** (fix immediately)
- Type errors blocking build
- Security vulnerabilities
- Runtime errors
- Broken accessibility

**Medium Priority** (fix before commit)
- Missing type annotations
- Unused variables
- Code style violations
- TODO comments

**Low Priority** (fix when convenient)
- Formatting inconsistencies
- Comment improvements
- Minor refactoring opportunities

### 6. **Pre-Commit Hooks** (Recommended)

**Install Husky + lint-staged**
```bash
npm install -D husky lint-staged
npx husky init
```

**Configure** (`.husky/pre-commit`)
```bash
npx lint-staged
```

**lint-staged config** (`package.json`)
```json
{
  "lint-staged": {
    "*.{js,jsx,ts,tsx}": [
      "eslint --fix",
      "prettier --write"
    ]
  }
}
```

### 7. **VSCode Integration**

**Settings** (`.vscode/settings.json`)
```json
{
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll.eslint": true
  },
  "typescript.tsdk": "node_modules/typescript/lib"
}
```

## What to Generate

1. **Lint Report** - All issues found
2. **Auto-Fix Results** - What was automatically fixed
3. **Manual Fix Suggestions** - Issues requiring manual intervention
4. **Priority List** - Ordered by severity
5. **Configuration Recommendations** - Improve lint setup

## Common Fixes

**Remove Unused Imports**
```typescript
// Before
import { A, B, C } from 'lib'

// After
import { A, C } from 'lib'  // B was unused
```

**Add Type Annotations**
```typescript
// Before
function process(data) {
  return data.map(x => x.value)
}

// After
function process(data: DataItem[]): number[] {
  return data.map(x => x.value)
}
```

**Fix Missing Keys**
```typescript
// Before
{items.map(item => <div>{item.name}</div>)}

// After
{items.map(item => <div key={item.id}>{item.name}</div>)}
```

Focus on fixes that improve code quality and prevent bugs. Run linting before every commit.
