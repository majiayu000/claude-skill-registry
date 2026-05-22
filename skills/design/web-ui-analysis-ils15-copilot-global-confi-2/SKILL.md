---
name: web-ui-analysis
description: Analyze web interfaces for UX issues, accessibility compliance (WCAG 2.1), color contrast, typography hierarchy, responsive design, and Core Web Vitals. Returns actionable improvements with code examples.
---

# Web UI Analysis Skill

## When to Use

Use this skill when:
- Evaluating a web interface for UX issues
- Checking accessibility compliance (WCAG 2.1 AA/AAA)
- Analyzing color contrast ratios
- Reviewing typography and font hierarchy
- Checking responsive design breakpoints
- Measuring Core Web Vitals (LCP, FID, CLS)
- Comparing against Material Design or Apple HIG standards

## Analysis Framework

### 1. Accessibility (WCAG 2.1)

```
✅ Checklist:
- [ ] Color contrast ratio ≥ 4.5:1 (text), ≥ 3:1 (large text)
- [ ] Touch targets ≥ 44x44px
- [ ] Keyboard navigation works
- [ ] Screen reader labels present
- [ ] Focus states visible
- [ ] Alt text on images
- [ ] ARIA roles correct
```

### 2. Typography Hierarchy

```
Heading Scale (1.250 ratio):
- h1: 2.441rem (39px)
- h2: 1.953rem (31px)
- h3: 1.563rem (25px)
- h4: 1.25rem (20px)
- body: 1rem (16px)
- small: 0.8rem (13px)
```

### 3. Color Palette Analysis

```
Primary Colors:
- Main: #hex (contrast ratio)
- Light variant: #hex
- Dark variant: #hex

Semantic Colors:
- Success: #22c55e (green-500)
- Warning: #f59e0b (amber-500)
- Error: #ef4444 (red-500)
- Info: #3b82f6 (blue-500)
```

### 4. Layout & Spacing

```
8px Grid System:
- xs: 4px (0.25rem)
- sm: 8px (0.5rem)
- md: 16px (1rem)
- lg: 24px (1.5rem)
- xl: 32px (2rem)
- 2xl: 48px (3rem)

Breakpoints:
- mobile: 0-639px
- tablet: 640-1023px
- desktop: 1024-1279px
- wide: 1280px+
```

### 5. Core Web Vitals

```
Targets:
- LCP (Largest Contentful Paint): < 2.5s
- FID (First Input Delay): < 100ms
- CLS (Cumulative Layout Shift): < 0.1
- FCP (First Contentful Paint): < 1.8s
- TTFB (Time to First Byte): < 0.8s
```

## Output Format

```markdown
## UI Analysis Report

### Summary
- Overall Score: X/100
- Accessibility: ✅/⚠️/❌
- Performance: ✅/⚠️/❌
- Responsive: ✅/⚠️/❌

### Critical Issues
1. [Issue] - [Impact] - [Fix]

### Recommendations
1. [Improvement] - [Code example]

### Resources
- [Link to relevant docs]
```

## Example Usage

```
@webui Analyze the login page for accessibility issues
@webui Check color contrast on the dashboard
@webui Review typography hierarchy on landing page
@webui Measure Core Web Vitals for homepage
```
