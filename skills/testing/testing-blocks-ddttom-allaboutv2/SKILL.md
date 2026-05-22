---
name: Testing Blocks
description: Guide for testing code changes in AEM Edge Delivery projects including blocks, scripts, and styles. Use this skill after making code changes and before opening a pull request to validate functionality. Covers unit testing for utilities and logic, browser testing with Playwright/Puppeteer, linting, performance validation, and guidance on which tests to maintain vs use as throwaway validation.
---

# Testing Blocks

This skill guides you through testing code changes in AEM Edge Delivery Services projects. Testing follows a value-versus-cost philosophy: create and maintain tests when the value they bring exceeds the cost of creation and maintenance.

## Related Skills

- **content-driven-development**: Test content created during CDD serves as the basis for testing
- **building-blocks**: This skill is automatically invoked after block implementation
- **block-collection-and-party**: May provide reference test patterns from similar blocks

## When to Use This Skill

Use this skill:
- ✅ After implementing or modifying blocks
- ✅ After changes to core scripts (scripts.js, delayed.js, aem.js)
- ✅ After style changes (styles.css, lazy-styles.css)
- ✅ After configuration changes that affect functionality
- ✅ Before opening any pull request with code changes

This skill should be automatically invoked by the **building-blocks** skill after implementation is complete.

## Testing Philosophy: Value vs Cost

**The Principle:** Create and maintain tests when the value they bring exceeds the cost of creation and maintenance.

### Keeper Tests (High Value, Worth Maintaining)

✅ **Write unit tests for:**
- Logic-heavy utility functions used across multiple blocks
- Data processing and transformation logic
- API integrations and external service interactions
- Complex algorithms or business logic
- Shared libraries and helper functions

These tests provide lasting value because they catch regressions in reused code, serve as living documentation, and are fast and easy to maintain.

### Throwaway Tests (Lower Value, Use Once)

⚠️ **Use browser tests for:**
- Block decoration logic (DOM transformations)
- Specific DOM structures or UI layouts
- Visual appearance validation
- Block-specific rendering behavior

These tests are better done in a browser because DOM structures change frequently, visual validation requires human judgment, and maintaining UI tests is expensive relative to their value.

**Important:** Even throwaway tests have value! Use them to:
1. Validate your implementation works correctly
2. Take screenshots to evaluate visual correctness
3. Show screenshots to humans for feedback
4. Include screenshots in PRs to aid review

**Organization:** Keep throwaway tests in `test/tmp/` and test content in `drafts/tmp/`. Both directories should be gitignored so temporary test artifacts aren't committed.

## Testing Checklist

Before opening a pull request, complete ALL of the following:

- [ ] **Existing tests pass** - All keeper tests still pass with your changes
- [ ] **Unit tests written** - New keeper tests for any logic-heavy utilities or data processing
- [ ] **Browser validation** - Feature tested in local dev server, screenshots captured
- [ ] **All variants tested** - Each variant/configuration of blocks validated
- [ ] **Responsive behavior** - Tested on mobile, tablet, desktop viewports
- [ ] **Linting passes** - `npm run lint` completes without errors
- [ ] **Branch pushed** - Code committed and pushed to feature branch
- [ ] **GitHub checks verified** - Use `gh checks` to confirm all CI checks pass

## Testing Methods Overview

### 1. Unit Tests (KEEPER TESTS)

**When to use:** Logic-heavy functions, utilities, data processing, API integrations

**Quick start:**
```bash
# Verify test setup (see resources/vitest-setup.md if not configured)
npm test

# Write test for utility function
# test/utils/my-utility.test.js
import { describe, it, expect } from 'vitest';
import { myUtility } from '../../scripts/utils/my-utility.js';

describe('myUtility', () => {
  it('should transform input correctly', () => {
    expect(myUtility('input')).toBe('OUTPUT');
  });
});

# Run tests during development
npm run test:watch
```

**Detailed guide:** See `resources/unit-testing.md`

### 2. Browser Testing (THROWAWAY TESTS)

**When to use:** Block decoration, visual validation, DOM structure, responsive design

**Organization:**
- Test scripts: `test/tmp/test-{block}-browser.js`
- Test content: `drafts/tmp/{block}.html`
- Screenshots: `test/tmp/screenshots/`
- Both `test/tmp/` and `drafts/tmp/` should be gitignored

**Quick start:**
```bash
# Install Playwright
npm install --save-dev playwright
npx playwright install chromium

# Create test content
# drafts/tmp/my-block.html (copy head.html content, add test markup)

# Start dev server with drafts folder
aem up --html-folder drafts

# Create throwaway test script in test/tmp/
# test/tmp/test-my-block.js
import { chromium } from 'playwright';
import { mkdir } from 'fs/promises';

async function test() {
  await mkdir('./test/tmp/screenshots', { recursive: true });
  const browser = await chromium.launch({ headless: false });
  const page = await browser.newPage();

  await page.goto('http://localhost:3000/drafts/tmp/my-block');
  await page.waitForSelector('.my-block');
  await page.screenshot({ 
    path: './test/tmp/screenshots/my-block.png',
    fullPage: true 
  });

  await browser.close();
}

test().catch(console.error);

# Run the test
node test/tmp/test-my-block.js

# Clean up when done (optional - gitignored either way)
rm -rf test/tmp/*
```

**Detailed guide:** See `resources/browser-testing.md`

### 3. Linting (ALWAYS)

**When to use:** Before every commit

**Quick start:**
```bash
# Run linting
npm run lint

# Auto-fix issues
npm run lint:fix
```

**Linting MUST pass before opening a PR.** Non-negotiable.

### 4. Performance Testing (AUTOMATED)

**When to use:** After pushing branch, automatically via GitHub checks

**Quick start:**
```bash
# Push branch
git push -u origin your-branch

# Create PR with test link
# PR description MUST include:
# Preview: https://branch--repo--owner.aem.page/path/to/test

# Monitor checks
gh pr checks --watch
```

Performance tests run automatically when you include a test link in your PR description.

## Complete Workflow

For detailed step-by-step workflow, see `resources/testing-workflow.md`.

**Quick summary:**

### During Development
1. Write unit tests for new utilities
2. Run `npm run test:watch`
3. Manually test in browser

### Before Committing
4. Run `npm test` - all tests pass
5. Run `npm run lint` - linting passes
6. Write throwaway browser test in `test/tmp/`
7. Create test content in `drafts/tmp/`
8. Review screenshots from `test/tmp/screenshots/`
9. Manual validation in browser

### Before Opening PR
10. Commit and push to feature branch (test/tmp/ won't be included)
11. Verify branch preview loads
12. Run `gh checks`
13. Create PR with test link
14. Monitor `gh pr checks`

### After PR Review
15. Address feedback
16. Re-test
17. Verify checks pass

## Troubleshooting

For detailed troubleshooting guide, see `resources/troubleshooting.md`.

**Common issues:**

### Tests fail
- Read error message carefully
- Run single test: `npm test -- path/to/test.js`
- Fix code or update test

### Linting fails
- Run `npm run lint:fix`
- Manually fix remaining issues

### GitHub checks fail
- Ensure PR has test link
- Check `gh pr checks` for details
- Fix performance issues if PSI fails

### Browser tests fail
- Verify dev server running: `aem up --html-folder drafts`
- Check test content exists in `drafts/tmp/`
- Verify URL uses `/tmp/` path: `http://localhost:3000/drafts/tmp/my-block`
- Add waits: `await page.waitForSelector('.block')`

## Resources

- **Unit Testing:** `resources/unit-testing.md` - Complete guide to writing and maintaining unit tests
- **Browser Testing:** `resources/browser-testing.md` - Playwright/Puppeteer workflows and best practices
- **Testing Workflow:** `resources/testing-workflow.md` - Step-by-step workflow from dev to PR
- **Troubleshooting:** `resources/troubleshooting.md` - Solutions to common testing issues
- **Vitest Setup:** `resources/vitest-setup.md` - One-time configuration guide

## Integration with Building Blocks Skill

The **building-blocks** skill automatically invokes this skill after implementation.

**Expected flow:**
1. Building blocks completes implementation
2. Invokes **testing-blocks** skill
3. This skill guides testing process
4. Returns control when testing complete

**Building blocks provides:**
- Block name being tested
- Test content URL from CDD process
- Any variants that need testing

**This skill returns:**
- Confirmation all tests pass
- Screenshots from browser testing (if requested)
- Any issues discovered during testing

## Summary

Testing in AEM Edge Delivery follows a pragmatic value-versus-cost approach:

**Create keeper tests for:**
- Logic-heavy utilities
- Data processing and transformations
- API integrations
- Shared libraries

**Use throwaway browser tests for:**
- Block decoration validation
- Visual appearance
- DOM structure
- Interactive behavior

**Always do:**
- Run linting before commits
- Test manually in browser
- Verify GitHub checks pass
- Include test links in PRs

**Remember:** The goal is confidence that your code works correctly, not achieving 100% test coverage. Write tests that provide value, and validate everything else in a browser.
