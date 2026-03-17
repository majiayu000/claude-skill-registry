---
name: verification-loops
description: Verify changes work before completing. Use browser testing, test suites, and manual checks.
triggers: testing, verification, QA, quality assurance, checking changes, validating code, build check, lint check
---

# Verification Loops

Always verify changes work before marking tasks complete.

## Verification Methods

### 1. Test Suite

```bash
npm test / pytest / cargo test / go test ./...
```

### 2. Browser (Playwright MCP)

- `browser_navigate` - Go to page
- `browser_snapshot` - Accessibility tree
- `browser_take_screenshot` - Visual verification

### 3. Build Verification

```bash
npm run build / cargo build / go build ./...
```

### 4. Lint Check

```bash
npm run lint / ruff check . / golangci-lint run
```

## Checklist Before Completing

- [ ] Tests pass
- [ ] Build succeeds
- [ ] Lint passes
- [ ] Manual verification (if UI)
