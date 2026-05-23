---
name: portfolio-code-review
description: Code review for Paweł Lipowczan portfolio project (React+Vite+Tailwind SPA). Use when user wants to review code changes, pull requests, commits, or modifications in portfolio project. Verifies architecture compliance, SEO standards, accessibility (WCAG 2.1 AA), performance (Core Web Vitals), blog system (markdown frontmatter, OG images), prerendering setup, and edge cases. References docs/{PRD.md,SRS.md,TODO.md,blog/BLOG_WORKFLOW.md}. Focuses on bugs, edge cases, and conditions causing errors after deployment.
license: Apache-2.0
---

# Portfolio Code Review

Code review skill for Paweł Lipowczan portfolio project.

## Project Documentation

Before starting review, familiarize yourself with:
- `docs/SRS.md` - Technical specification (architecture, components, functional requirements)
- `docs/PRD.md` - Product requirements (stack, features, visual style)
- `docs/maintenance/TODO.md` - Known issues and tasks
- `docs/blog/BLOG_WORKFLOW.md` - Blog posts workflow
- `docs/testing/README.md` - E2E tests

## Project Scope

**Stack:** React 19 + Vite 7 + Tailwind CSS 3 + Framer Motion 12 + React Router 7

**Architecture:** SPA with build-time prerendering (Puppeteer), file-based blog (markdown), static deployment (Vercel)

**Structure:** `components/{layout,sections,animations,seo,ui}`, `pages/`, `content/blog/`, `data/`, `utils/`

## Workflow

1. **Identify scope**: Ask user what changed (files, feature, component, blog post)
2. **Read files**: Read changed files using Read tool
3. **Verify**: Go through verification checklist (see below)
4. **Report**: Generate code review report (see template below)

## Verification Checklist

### Architecture & Stack

- React Hooks (not Class Components)
- Tailwind CSS (not inline styles)
- Framer Motion for animations
- React Router for routing
- Correct directory (components/layout, components/sections, pages/, etc.)

### SEO & Prerendering

- Meta tags (title, description, OG tags, Twitter cards) via react-helmet-async
- Structured data (JSON-LD) for Person/BlogPosting schemas
- Canonical URL
- Alt text on all images
- **Edge case:** New routes added to `scripts/prerender.mjs`?
- **Edge case:** Prerendering will work after changes (no dynamic content breaking SSR)?
- **Edge case:** Sitemap updated (`public/sitemap.xml`) for new pages/posts?

### Blog System

- Markdown files in `src/content/blog/`
- **Edge case:** Frontmatter YAML valid (separators `---`, proper indentation)?
- **Edge case:** Required fields: `id, slug, title, excerpt, date, readTime, image, tags, author, category`
- **Edge case:** File doesn't start with `_` or isn't `README.md` (filtered by `import.meta.glob`)?
- **Edge case:** OG image exists as WebP (1200x630px) in `public/images/og-{slug}.webp`?
- **Edge case:** Sitemap updated after new post?

### Accessibility (WCAG 2.1 AA)

- Semantic HTML (header, nav, main, section, article, footer)
- Keyboard navigation works
- Color contrast >=4.5:1 for text, >=3:1 for UI components
- Form labels present
- ARIA labels for icon-only buttons
- Heading hierarchy (H1 -> H2 -> H3)
- **Edge case:** Only ONE H1 per page

### Performance

- Images optimized (WebP, lazy loading with `loading="lazy"`)
- **Edge case:** Lazy loading doesn't cause CLS (Cumulative Layout Shift) - specify dimensions
- No unnecessary re-renders (useMemo/useCallback if needed)
- Animations use only transform/opacity (not width/height/top/left)
- **Edge case:** Canvas animations (NetworkBackground) don't block main thread (use requestAnimationFrame)
- **Edge case:** Font loading uses `font-display: swap` (TODO: fix slow FCP/LCP)
- **Edge case:** No `console.log` in production code

### Routing & Navigation

- **Edge case:** Smooth scroll works with new sections (`element.scrollIntoView({ behavior: 'smooth' })`)
- **Edge case:** Mobile menu closes after navigation
- **Edge case:** Mobile menu closes on Escape key
- **Edge case:** Mobile menu closes on click outside

### Security & Best Practices

- **Edge case:** External links have `target="_blank"` AND `rel="noopener noreferrer"`
- **Edge case:** Uses `SITE_CONFIG` from `src/utils/constants.js` (not hardcoded URLs)
- **Edge case:** No duplicate structured data schemas (check JSON-LD)
- Form validation present
- GDPR/RODO compliant (for contact forms, cookie banner)

### Testing

- E2E tests for new functionality (Playwright)
- Tests pass (`npm test`)
- No breaking changes to existing tests

### Code Quality

- Readable, clear code
- No duplication
- Descriptive names (variables, functions, components)
- Follows existing project style
- No new dependencies without justification
- Props validation (PropTypes or TypeScript)

### Known Issues (from TODO.md)

- **Check:** Changes don't introduce/worsen performance issues (FCP/LCP already slow)
- **Check:** Changes don't break prerendering (critical for SEO)
- **Check:** Changes follow mobile-first responsive design

## Report Template

Generate report in this format:

```markdown
# Code Review Report - [Change Description]

## Scope

[Brief description of what changed: files, components, features]

## Positive Aspects

- [Good practices observed]
- [Well-implemented features]

## Potential Bugs & Edge Cases

CRITICAL: Focus on bugs and error conditions

### Critical (fix before merge)

- [ ] **[Bug/Edge Case]**: Description
  - **Impact:** What breaks if not fixed
  - **Fix:** Suggested solution
  - **Reference:** docs/[file]#section

### Warnings (should fix)

- [ ] **[Issue]**: Description
  - **Impact:** Potential problem
  - **Fix:** Suggested solution

### Suggestions (nice to have)

- [Non-critical improvements]

## Checklist

**Architecture:**
- [ ] React Hooks used correctly
- [ ] Tailwind CSS styling
- [ ] Component in correct directory

**SEO & Prerendering:**
- [ ] Meta tags present (react-helmet-async)
- [ ] New routes added to prerender.mjs
- [ ] Sitemap updated
- [ ] OG images exist (WebP, 1200x630px)

**Blog System (if applicable):**
- [ ] Frontmatter valid YAML
- [ ] All required fields present
- [ ] File not starting with _ or README.md
- [ ] OG image exists

**Accessibility:**
- [ ] Semantic HTML
- [ ] Keyboard navigation
- [ ] Color contrast >=4.5:1
- [ ] Only one H1 per page

**Performance:**
- [ ] Images optimized (WebP, lazy loading)
- [ ] No CLS (dimensions specified)
- [ ] Animations use transform/opacity only
- [ ] No console.log in production

**Routing & Navigation:**
- [ ] Smooth scroll works
- [ ] Mobile menu closes properly (nav, Escape, outside click)

**Security & Best Practices:**
- [ ] External links: target="_blank" + rel="noopener noreferrer"
- [ ] Uses SITE_CONFIG (not hardcoded URLs)
- [ ] No duplicate structured data

**Testing:**
- [ ] E2E tests for new functionality
- [ ] Tests pass
- [ ] No breaking changes

**Code Quality:**
- [ ] Readable, clear
- [ ] No duplication
- [ ] Descriptive names
- [ ] Follows project style

## Summary

[Overall assessment: 1-2 paragraphs]

**Recommendation:**
- **APPROVE** - Ready to merge
- **APPROVE WITH COMMENTS** - Non-critical suggestions, can merge
- **REQUEST CHANGES** - Critical issues must be fixed first

## References

- docs/SRS.md - [specific sections]
- docs/maintenance/TODO.md - [relevant known issues]
- docs/PRD.md - [if architecture/design questions]
- docs/blog/BLOG_WORKFLOW.md - [if blog-related changes]
```

## Examples

### Example 1: Review new Hero component

User: "Review Hero.jsx changes"

Steps:
1. Read src/components/sections/Hero.jsx
2. Verify against checklist (especially: React Hooks, Framer Motion, NetworkBackground performance, semantic HTML)
3. Check if smooth scroll works with new sections
4. Generate report focusing on potential bugs (e.g., canvas blocking main thread, missing alt text, performance impact)

### Example 2: Review new blog post

User: "Review new blog post about automation"

Steps:
1. Find new .md file in src/content/blog/
2. Verify frontmatter YAML (valid syntax, all required fields)
3. Check OG image exists (public/images/og-{slug}.webp, 1200x630px)
4. Verify sitemap updated
5. Check blog post doesn't start with _ or isn't README.md
6. Generate report focusing on edge cases (frontmatter parsing errors, missing OG image, sitemap not updated)

### Example 3: Review routing changes

User: "Review new /projects/:slug route"

Steps:
1. Read routing files (App.jsx, new page component)
2. Verify route added to scripts/prerender.mjs (CRITICAL for SEO)
3. Check smooth scroll, mobile menu behavior
4. Verify meta tags for new route
5. Check sitemap updated
6. Generate report focusing on prerendering issues, SEO implications

## Guidelines

### Philosophy

- **Constructive:** Point out problems AND suggest solutions
- **Prioritize:** Critical (breaks app) > Warnings (bad UX) > Suggestions (nice to have)
- **Reference:** Always cite docs/* for justification
- **Edge cases first:** Focus on what can go wrong, not just what works

### Process

1. Read relevant docs FIRST (docs/SRS.md for architecture, docs/maintenance/TODO.md for known issues)
2. Read changed files
3. Think: "What edge cases could break this?"
4. Think: "What happens on mobile? On slow network? With different data?"
5. Check against docs/maintenance/TODO.md - does this worsen known issues?
6. Generate detailed report with clear fix suggestions

### Common pitfalls to check

- Frontmatter YAML syntax errors (very common in blog posts)
- Missing OG images (breaks social sharing)
- Routes not in prerender.mjs (empty HTML in source, bad SEO)
- CLS from lazy-loaded images without dimensions
- Mobile menu not closing (bad UX)
- External links without rel="noopener noreferrer" (security)
- Hardcoded URLs instead of SITE_CONFIG (maintenance nightmare)
- Console.log in production (performance, security)
