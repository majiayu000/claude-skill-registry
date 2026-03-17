---
name: html-lint-runner
description: Runs automated HTML linting using @axe-core/playwright (WCAG accessibility) and markuplint (HTML standards). Use when user asks to "lint HTML", "run automated checks", "validate HTML", "check accessibility", or mentions "axe-core", "markuplint", "automated audit".
---

# HTML Lint Runner

Automated HTML linting using @axe-core/playwright and markuplint with JSON output.

## Tools Overview

| Tool | Focus | Output |
|------|-------|--------|
| **@axe-core/playwright** | WCAG 2.1 AA accessibility | JSON with violations |
| **markuplint** | HTML standards, semantics | JSON with problems |

## Quick Start

```bash
# Install dependencies
cd ${CLAUDE_PLUGIN_ROOT}/skills/html-lint-runner && npm install

# Run combined lint (development)
npm --prefix ${CLAUDE_PLUGIN_ROOT}/skills/html-lint-runner run dev -- path/to/file.html

# Run with build
npm --prefix ${CLAUDE_PLUGIN_ROOT}/skills/html-lint-runner run build
node ${CLAUDE_PLUGIN_ROOT}/skills/html-lint-runner/dist/index.js path/to/file.html
```

## Options

| Option | Description |
|--------|-------------|
| `--json` | Output as JSON (default) |
| `--text` | Output as human-readable text |
| `--axe-only` | Run only axe-core (accessibility) |
| `--markuplint-only` | Run only markuplint (HTML standards) |

## Supported File Types

| Extension | axe-core | markuplint | Notes |
|-----------|----------|------------|-------|
| `.html` | Yes | Yes | Full support |
| `.htm` | Yes | Yes | Full support |
| `.jsx` | No* | Yes | markuplint only |
| `.tsx` | No* | Yes | markuplint only |

*JSX/TSX require rendering to HTML for axe-core analysis

## Output Structure

```json
{
  "file": "target.html",
  "timestamp": "2025-01-01T00:00:00Z",
  "axe": {
    "violations": [...],
    "passes": [...],
    "incomplete": [...]
  },
  "markuplint": {
    "problems": [...]
  },
  "summary": {
    "axe_violations": 3,
    "markuplint_problems": 5,
    "total_issues": 8
  }
}
```

## axe-core Violations

```json
{
  "id": "color-contrast",
  "impact": "serious",
  "description": "Elements must have sufficient color contrast",
  "nodes": [
    {
      "html": "<p class=\"light\">...</p>",
      "failureSummary": "Fix: Increase contrast ratio to 4.5:1"
    }
  ]
}
```

Impact levels: `critical` > `serious` > `moderate` > `minor`

## markuplint Problems

```json
{
  "severity": "error",
  "ruleId": "required-attr",
  "message": "The \"alt\" attribute is required",
  "line": 15,
  "col": 5,
  "raw": "<img src=\"photo.jpg\">"
}
```

## Workflow

1. **Run combined lint** - Check both accessibility and HTML standards
2. **Parse JSON results** - Identify issues by severity
3. **Prioritize issues** - critical > serious > error > warning
4. **Apply fixes** - Address high-priority issues first
5. **Re-run to verify** - Confirm fixes resolved issues

## Common Fixes

### Missing alt text
```html
<!-- Before -->
<img src="photo.jpg">

<!-- After -->
<img src="photo.jpg" alt="Description of image">
```

### Low contrast
```css
/* Before: #999 on #fff = 2.85:1 */
.text { color: #999; }

/* After: #595959 on #fff = 7:1 */
.text { color: #595959; }
```

## References

- [axe-core Documentation](https://github.com/dequelabs/axe-core)
- [@axe-core/playwright](https://www.npmjs.com/package/@axe-core/playwright)
- [markuplint Documentation](https://markuplint.dev/)
- [WCAG 2.1 Quick Reference](https://www.w3.org/WAI/WCAG21/quickref/)
