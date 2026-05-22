---
name: web-frontend-tester
description: Run frontend functional, accessibility, visual, and performance test planning with structured reports.
compatibility: codex, claude-code, claude-ai, agent-skills
license: Apache-2.0
allowed-tools:
  - read_file
  - write_file
  - run_terminal_cmd
  - web_search
metadata:
  category: web-builder
  stage: 8-frontend-testing
  pipeline: web-builder
---

# Web Frontend Tester

## Objective

Validate frontend quality across user journeys, a11y, visual regressions, and
performance targets.

## Required Workflow

1. Set up Playwright for E2E critical journeys (login, checkout, form submit, navigation).
2. Configure unit/component tests with Vitest + Testing Library (or Jest + Testing Library).
3. Run accessibility audits:
   - axe-core via `@axe-core/playwright`
   - Lighthouse CI for performance, SEO, accessibility
4. Run visual regression tests with Percy or Chromatic.
5. Verify page load under 3 seconds on 4G, Lighthouse performance score >= 80, and no console errors.
6. Check missing alt tags, color contrast, and keyboard navigation.
7. Output `frontend-test-report.json` with Lighthouse scores and pass/fail counts.

## Execution

```bash
python skills/web-frontend-tester/scripts/frontend_tester.py --input <workspace> --output <out.json> --format json
```

## References

- `references/tools.md`
