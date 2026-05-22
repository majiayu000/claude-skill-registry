---
name: web-design-guidelines
description: 'Visual inspection and code review for Web Interface Guidelines compliance. Triggers on "review my UI", "check accessibility", "audit design", "review UX", "fix the layout", "find design problems". Supports both static code analysis and visual browser inspection with auto-fixing.'
metadata:
  author: vercel
  version: "2.0.0"
  argument-hint: <url-or-file-pattern>
---

# Web Interface Guidelines

Review and fix UI for compliance with Web Interface Guidelines through static code analysis and visual browser inspection.

## Scope of Application

- Static sites (HTML/CSS/JS)
- SPA frameworks: React / Vue / Angular / Svelte
- Full-stack frameworks: Next.js / Nuxt / SvelteKit
- Any web application with accessible source code

## Workflow Overview

```
Step 1: Information Gathering
    ↓
Step 2: Guidelines Fetch + Static Analysis
    ↓
Step 3: Visual Inspection (if URL provided)
    ↓
Step 4: Issue Fixing
    ↓
Step 5: Re-verification
    ↓
(Loop if issues remain)
```

---

## Step 1: Information Gathering

### 1.1 Determine Review Mode

| Input | Mode | Actions |
|-------|------|---------|
| File/pattern only | Static Analysis | Code review against guidelines |
| URL only | Visual Inspection | Browser-based visual review |
| URL + files | Full Review | Both static and visual analysis |

### 1.2 URL Confirmation (Visual Mode)

If visual inspection requested but no URL provided, ask:

> Please provide the URL of the website to review (e.g., `http://localhost:3000`)

### 1.3 Project Detection

Attempt automatic detection from workspace files:

| File | Detection |
|------|-----------|
| `package.json` | Framework and dependencies |
| `tailwind.config.*` | Tailwind CSS |
| `next.config.*` | Next.js |
| `nuxt.config.*` | Nuxt |
| `vite.config.*` | Vite |

### 1.4 Styling Method Identification

| Method | Detection | Edit Target |
|--------|-----------|-------------|
| Pure CSS | `*.css` files | Global or component CSS |
| SCSS/Sass | `*.scss`, `*.sass` | SCSS files |
| CSS Modules | `*.module.css` | Module CSS files |
| Tailwind CSS | `tailwind.config.*` | className in components |
| styled-components | `styled.` in code | JS/TS files |
| CSS-in-JS | Inline styles | JS/TS files |

---

## Step 2: Guidelines Fetch + Static Analysis

### 2.1 Fetch Latest Guidelines

Fetch fresh guidelines before each review:

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

Use WebFetch to retrieve the latest rules. The fetched content contains all the rules and output format instructions.

### 2.2 Static Code Analysis

1. Read the specified files (or prompt user for files/pattern)
2. Check against all rules in the fetched guidelines
3. Collect findings with `file:line` references

---

## Step 3: Visual Inspection (Browser Mode)

### 3.1 Prerequisites

- Target website must be running (local dev server or remote)
- Browser automation available (Playwright MCP or cursor-browser-extension)

### 3.2 Page Inspection

1. Navigate to the specified URL
2. Capture screenshots
3. Retrieve DOM structure/snapshot
4. If additional pages exist, traverse through navigation

### 3.3 Viewport Testing

Test at the following viewports for responsive issues:

| Name | Width | Representative Device |
|------|-------|----------------------|
| Mobile | 375px | iPhone SE/12 mini |
| Tablet | 768px | iPad |
| Desktop | 1280px | Standard PC |
| Wide | 1920px | Large display |

### 3.4 Visual Inspection Checklist

#### Layout Issues

| Issue | Description | Severity |
|-------|-------------|----------|
| Element Overflow | Content overflows container or viewport | High |
| Element Overlap | Unintended overlapping of elements | High |
| Alignment Issues | Grid or flex alignment problems | Medium |
| Inconsistent Spacing | Padding/margin inconsistencies | Medium |
| Text Clipping | Long text not handled properly | Medium |

#### Responsive Issues

| Issue | Description | Severity |
|-------|-------------|----------|
| Non-mobile Friendly | Layout breaks on small screens | High |
| Breakpoint Issues | Unnatural transitions at breakpoints | Medium |
| Touch Targets | Buttons too small on mobile | Medium |

#### Accessibility Issues

| Issue | Description | Severity |
|-------|-------------|----------|
| Insufficient Contrast | Low contrast ratio text/background | High |
| No Focus State | Cannot see focus during keyboard nav | High |
| Missing alt Text | No alternative text for images | Medium |

#### Visual Consistency

| Issue | Description | Severity |
|-------|-------------|----------|
| Font Inconsistency | Mixed font families | Medium |
| Color Inconsistency | Non-unified brand colors | Medium |
| Spacing Inconsistency | Non-uniform spacing patterns | Low |

---

## Step 4: Issue Fixing

### 4.1 Issue Prioritization

| Priority | Criteria | Action |
|----------|----------|--------|
| P1 | Layout issues affecting functionality | Fix immediately |
| P2 | Visual issues degrading UX | Fix next |
| P3 | Minor visual inconsistencies | Fix if possible |

### 4.2 Identifying Source Files

1. **Selector-based Search**: Search codebase by class name or ID
2. **Component-based Search**: Identify components from element text/structure
3. **File Pattern Filtering**: `src/**/*.css`, `styles/**/*`, `src/components/**/*`

### 4.3 Fix Principles

1. **Minimal Changes**: Only make minimum changes necessary
2. **Respect Existing Patterns**: Follow existing code style
3. **Avoid Breaking Changes**: Be careful not to affect other areas
4. **Add Comments**: Explain reason for fixes where appropriate

---

## Step 5: Re-verification

### 5.1 Post-fix Confirmation

1. Reload browser (or wait for HMR)
2. Capture screenshots of fixed areas
3. Compare before and after

### 5.2 Regression Testing

- Verify fixes haven't affected other areas
- Confirm responsive display is not broken

### 5.3 Iteration

If issues remain after fix, return to Step 3. Limit to 3 fix attempts per issue before consulting user.

---

## Output Format

### Review Results Report

```markdown
# Web Design Review Results

## Summary

| Item | Value |
|------|-------|
| Target | {URL or files} |
| Framework | {Detected framework} |
| Styling | {CSS / Tailwind / etc.} |
| Review Mode | {Static / Visual / Full} |
| Issues Detected | {N} |
| Issues Fixed | {M} |

## Static Analysis Findings

{file:line format findings from guidelines check}

## Visual Inspection Findings

### [P1] {Issue Title}

- **Page**: {Page path}
- **Element**: {Selector or description}
- **Issue**: {Detailed description}
- **Fixed File**: `{File path}`
- **Fix Details**: {Description of changes}

### [P2] {Issue Title}
...

## Unfixed Issues (if any)

### {Issue Title}
- **Reason**: {Why it was not fixed}
- **Recommended Action**: {Recommendations for user}

## Recommendations

- {Suggestions for future improvements}
```

---

## Usage Examples

### Static Analysis Only

```
Review my UI in src/components/
Check accessibility of my forms
Audit design of src/pages/
```

### Visual Inspection

```
Review the design at http://localhost:3000
Check the UI at http://localhost:5173/dashboard
Find layout problems on my site
```

### Full Review (Recommended)

```
Review my UI at localhost:3000 and fix issues in src/
Audit the design and fix responsive problems
```

---

## Best Practices

### DO

- Always save screenshots before making fixes
- Fix one issue at a time and verify each
- Follow the project's existing code style
- Confirm with user before major changes

### DON'T

- Large-scale refactoring without confirmation
- Ignore design systems or brand guidelines
- Fix multiple issues at once (difficult to verify)
- Skip re-verification after fixes

---

## Troubleshooting

### Style files not found

1. Check dependencies in `package.json`
2. Consider CSS-in-JS possibility
3. Ask user about styling method

### Fixes not reflected

1. Check if dev server HMR is working
2. Clear browser cache
3. Check CSS specificity issues

### Fixes affecting other areas

1. Rollback changes
2. Use more specific selectors
3. Consider CSS Modules or scoped styles
