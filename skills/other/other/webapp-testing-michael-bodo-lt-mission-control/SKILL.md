---
name: webapp-testing
description: Web application testing principles. E2E, Playwright, deep audit strategies.
category: security
version: 4.1.0-fractal
layer: master-skill
---

# Web App Testing

> Discover and test everything. Leave no route untested.

## 🔧 Runtime Scripts

**Execute these for automated browser testing:**

| Script | Purpose | Usage |
|--------|---------|-------|
| `scripts/playwright_runner.py` | Basic browser test | `python scripts/playwright_runner.py https://example.com` |
| | With screenshot | `python scripts/playwright_runner.py <url> --screenshot` |
| | Accessibility check | `python scripts/playwright_runner.py <url> --a11y` |

**Requires:** `pip install playwright && playwright install chromium`

---

## 1. Deep Audit Approach

## 🧠 Knowledge Modules (Fractal Skills)

### 1. [Discovery First](./sub-skills/discovery-first.md)
### 2. [Systematic Testing](./sub-skills/systematic-testing.md)
### 3. [What to Test](./sub-skills/what-to-test.md)
### 4. [E2E Best Practices](./sub-skills/e2e-best-practices.md)
### 5. [Core Concepts](./sub-skills/core-concepts.md)
### 6. [Configuration](./sub-skills/configuration.md)
### 7. [When to Use](./sub-skills/when-to-use.md)
### 8. [Strategy](./sub-skills/strategy.md)
### 9. [Coverage Areas](./sub-skills/coverage-areas.md)
### 10. [File Structure](./sub-skills/file-structure.md)
### 11. [Naming Convention](./sub-skills/naming-convention.md)
### 12. [Pipeline Steps](./sub-skills/pipeline-steps.md)
### 13. [Parallelization](./sub-skills/parallelization.md)
