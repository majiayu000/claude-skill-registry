---
name: web-test
description: Browser-based QA testing with Playwright MCP. Triggers on "test in browser", "QA test", "visual test", "check the page".
---

# Web Test

Browser-based QA testing using Playwright MCP to verify UI, interactions, and responsive behavior.

## When to Use

- After implementing a new page or feature
- When verifying responsive design
- Testing form submissions
- Checking animations and transitions
- Verifying navigation and links

## When NOT to Use

- Unit testing logic (use Jest/Vitest instead)
- Testing API routes directly (use curl or Postman)

## Prerequisites

- Dev server running (`npm run dev`)
- Playwright MCP configured in `.cursor/mcp.json`

## Core Principles

- Test on multiple viewport sizes (mobile 375px, tablet 768px, desktop 1280px)
- Verify visual appearance matches design intent
- Test user interactions (clicks, form fills, navigation)
- Check for console errors

## Test Workflow

### Phase 1: Test Case Design

**Goal**: Define what to test.

1. List all pages/features to test
2. Define test scenarios per page
3. Identify edge cases (empty states, long text, etc.)
4. Define viewport sizes to test

### Phase 2: Browser Testing

**Goal**: Execute tests in browser.

**Actions**:
1. Navigate to the page under test
2. Take screenshots at each viewport size
3. Interact with clickable elements
4. Fill and submit forms
5. Verify navigation works
6. Check for console errors

**Viewport sizes**:
- Mobile: 375 x 812
- Tablet: 768 x 1024
- Desktop: 1280 x 800
- Wide: 1920 x 1080

### Phase 3: Issue Analysis

**Goal**: Document issues found.

**Format**:

```markdown
## Test Results: [Page/Feature]

### Passed
- [x] [test case] — [viewport]

### Issues Found
- [ ] **[severity]**: [description]
  - Page: [URL]
  - Viewport: [size]
  - Expected: [what should happen]
  - Actual: [what happens]
  - Screenshot: [if available]

### Recommendations
- [fix suggestion]
```

## Related Skills

| Skill | When to Chain |
|-------|--------------|
| feature-dev | Test after feature implementation |
| review-pr | Test before PR review |
