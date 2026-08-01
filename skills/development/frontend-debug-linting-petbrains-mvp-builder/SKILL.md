---
name: frontend-debug-linting
description: 'Quality gates for frontend code. ALWAYS use after writing React/Next.js
  code and before delivery. Covers: ESLint linting, TypeScript type-checking, Prettier
  formatting, browser console debugging. Catc'
---

---
name: frontend-debug-linting
description: Quality gates for frontend code. ALWAYS use after writing React/Next.js code and before delivery. Covers: ESLint linting, TypeScript type-checking, Prettier formatting, browser console debugging. Catches errors before they reach users.
allowed-tools: Read, Edit, Bash (*)
---

# Debug & Linting

Catch errors before delivery. Lint, type-check, browser verify.

## When to Use

- After writing code → run checks
- Before delivery → verify quality
- Debugging → check console/network

## Process

**LINT → TYPE → BROWSER → DELIVER**

1. Run lint: `npm run lint`
2. Type check: `npm run typecheck`
3. Browser check: console + screenshot
4. Deliver when clean

## Quick Commands

```bash
npm run lint          # ESLint check
npm run lint:fix      # Auto-fix
npm run typecheck     # TypeScript check
npm run format        # Prettier format
npm run check         # All checks
```

## Common Fixes

### TypeScript

```yaml
"Type 'X' not assignable to 'Y'":
  → Fix type mismatch or add assertion

"'X' declared but never used":
  → Remove or prefix with _

"Object possibly 'undefined'":
  → Add null check: obj?.property
  → Add fallback: obj ?? default
```

### React

```yaml
"Missing dependencies in useEffect":
  → Add deps or wrap in useCallback

"Each child should have unique key":
  → Add key={item.id} to list items

"img must have alt prop":
  → Add alt text or alt=""
```

### Formatting

```yaml
"Prettier errors":
  → Run: npm run format
```

## Browser Verification

```yaml
# Check console errors
browser_console_messages: { onlyErrors: true }
→ Must be empty before delivery

# Check network
browser_network_requests
→ No failed (4xx, 5xx) requests

# Debug element styles
browser_evaluate: { function: "() => getComputedStyle(el)" }
```

## Pre-Delivery Checklist

```yaml
MUST PASS:
  - [ ] npm run lint → 0 errors
  - [ ] npm run typecheck → 0 errors
  - [ ] browser_console_messages → 0 errors
  - [ ] No failed network requests

CAN DELIVER WITH:
  - ESLint warnings (with explanation)
  - Console warnings (if understood)
```

## Project Setup

```bash
# Add to existing Next.js project
npm install -D prettier eslint-config-prettier

# package.json scripts
{
  "lint": "eslint . --ext .ts,.tsx",
  "lint:fix": "eslint . --ext .ts,.tsx --fix",
  "format": "prettier --write .",
  "typecheck": "tsc --noEmit",
  "check": "npm run typecheck && npm run lint"
}
```

## Debug Checklist

```yaml
WHEN SOMETHING BREAKS:
  1. browser_console_messages → check errors
  2. browser_network_requests → failed requests?
  3. npm run typecheck → type errors?
  4. Add console.log → trace flow
  5. Isolate → comment out sections
  6. Fix → run checks → verify
```
