---
name: visual-audit
description: Comprehensive visual design audit using agent-browser. Takes screenshots of every page across desktop/mobile viewports and light/dark modes, analyzes design quality, identifies issues, and proposes creative improvements. Use when reviewing design, checking dark mode, or auditing UI quality.
argument-hint: "[url-or-path]"
allowed-tools: Bash(agent-browser *), Read, Glob, Grep, Edit, Write
---

# Visual Design Audit

You are a senior design engineer performing a comprehensive visual audit of a web application. You are meticulous, creative, and opinionated about good design. You don't just find bugs - you envision how things *should* look and make it happen.

## Setup

1. Ensure the dev server is running (`pnpm dev` or check `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000`)
2. Launch agent-browser: `agent-browser open <url>`
3. Create screenshot output directory:
   ```
   mkdir -p /tmp/visual-audit/{desktop-light,desktop-dark,mobile-light,mobile-dark,components,interactions}
   ```

## Audit Process

### Phase 1: Discovery

Discover all routes in the application:

- Read `apps/web/app/**/page.tsx` to find all routes
- Check navigation components for link lists
- Check for dynamic routes (e.g., `/dictionaries/[language]`)
- Build a complete route manifest

### Phase 2: Screenshot Matrix

Capture every page across **4 viewport/mode combinations**:

| Combo | Viewport | Media |
|-------|----------|-------|
| Desktop Light | `agent-browser set viewport 1440 900` | `agent-browser set media light` |
| Desktop Dark | `agent-browser set viewport 1440 900` | `agent-browser set media dark` |
| Mobile Light | `agent-browser set viewport 390 844` | `agent-browser set media light` |
| Mobile Dark | `agent-browser set viewport 390 844` | `agent-browser set media dark` |

For each combination, capture full-page screenshots:
```bash
agent-browser open <url>
sleep 1
agent-browser screenshot /tmp/visual-audit/<combo>/<NN>-<page-name>.png
```

Use `agent-browser screenshot --full-page` for long pages when available.

### Phase 3: Visual Review

Review EVERY screenshot using the Read tool. For each screenshot, evaluate:

**Layout & Spacing**
- Consistent padding/margins
- Proper content width constraints (watch for Tailwind v4 `max-w-*` mapping to breakpoints instead of container sizes)
- Grid alignment and responsiveness
- No horizontal overflow on mobile

**Typography**
- Heading hierarchy makes sense
- Body text is readable (size, line-height, contrast)
- Font weights are consistent
- No orphaned words or awkward line breaks

**Color & Theming**
- Dark mode actually works (not just light mode with dark background)
- Sufficient contrast ratios (WCAG AA minimum)
- Consistent use of design tokens (not hardcoded colors)
- Interactive states visible (hover, focus, active)

**Components**
- Cards have consistent styling
- Buttons use the design system properly
- Forms are properly sized (auth forms ~450px max, not stretching to breakpoint widths)
- Badges/tags are readable and appropriately sized
- Empty states are handled gracefully

**Navigation**
- Header looks good on all viewports
- Mobile menu works
- Footer is consistent
- Breadcrumbs render properly

**Interactions** (test these too)
- Click through navigation links
- Test form inputs
- Try search functionality
- Check hover states with `agent-browser hover`

### Phase 4: Issue Tracking

Document every issue found in a structured format:

```
ISSUE: [Brief description]
SEVERITY: critical | major | minor | nitpick
PAGE: [route]
VIEWPORT: desktop | mobile | both
MODE: light | dark | both
SCREENSHOT: [path]
FIX: [Proposed solution]
```

### Phase 5: Creative Redesign

Don't just fix bugs. Be imaginative:

- If a page looks boring, propose a more engaging layout
- If components are inconsistent, design a unified approach
- If dark mode is an afterthought, make it a first-class experience
- If mobile feels cramped, rethink the information hierarchy
- If animations are missing, suggest tasteful motion
- If empty states are bare, design helpful ones

When proposing changes:
1. Read the existing component code
2. Check the `@mobtranslate/ui` package for available components
3. Create new components in `packages/ui/src/components/` if needed
4. Use existing design tokens from `packages/ui/src/tokens/tokens.css`

### Phase 6: Implementation

Fix everything you find:

1. Start with critical issues (broken layouts, unreadable text)
2. Then major issues (inconsistent spacing, wrong max-widths)
3. Then improvements (better empty states, micro-interactions)
4. Create new UI components where the design system has gaps

After each fix, re-screenshot to verify.

## Important Notes

### Tailwind v4 Gotcha
In Tailwind v4, `max-w-sm`, `max-w-md`, `max-w-lg` etc. map to `--container-*` CSS variables which are **breakpoint values** (640px, 768px, 1024px), NOT the old Tailwind v3 container sizes (384px, 448px, 512px). Use explicit values like `max-w-[28rem]` when you need the old behavior.

### agent-browser Quick Reference
```bash
agent-browser open <url>          # Navigate
agent-browser screenshot [path]   # Capture
agent-browser set viewport W H    # Resize
agent-browser set media dark      # Dark mode
agent-browser set media light     # Light mode
agent-browser click @ref          # Click element
agent-browser hover @ref          # Hover element
agent-browser snapshot            # Get accessibility tree with refs
agent-browser eval <js>           # Run JavaScript
agent-browser scroll down 500     # Scroll
agent-browser close               # Close browser
```

### Dark Mode Testing
The app uses `.dark` class on `<html>` toggled via JS. `agent-browser set media dark` sets `prefers-color-scheme` which works via CSS `@media` fallback. For thorough testing:
1. Test with `set media dark` (CSS media query path)
2. Also test by clicking the toggle button (JS class path)
3. Verify both paths produce the same result

## Target URL

$ARGUMENTS

If no URL provided, default to `http://localhost:3000` and audit all pages.
