---
name: check-landing
description: |
  Audit landing page: value prop, CTA, social proof, mobile, load time.
  Outputs structured findings. Use log-landing-issues to create issues.
  Invoke for: landing page review, conversion audit, launch readiness.
---

# /check-landing

Audit landing page quality. Output findings as structured report.

## What This Does

1. Check value proposition clarity
2. Check call-to-action (CTA) effectiveness
3. Check social proof elements
4. Check mobile responsiveness
5. Check performance/load time
6. Output prioritized findings (P0-P3)

**This is a primitive.** It only investigates and reports. Use `/log-landing-issues` to create GitHub issues or `/fix-landing` to fix.

## Process

### 1. Landing Page Existence

```bash
# Landing page exists?
[ -f "app/page.tsx" ] || [ -f "app/(marketing)/page.tsx" ] || [ -f "pages/index.tsx" ] && echo "✓ Landing page exists" || echo "✗ No landing page"

# Is it a marketing page or app redirect?
grep -qE "redirect|SignIn|Dashboard" app/page.tsx 2>/dev/null && echo "⚠ Landing page redirects (no marketing page)" || echo "✓ Landing page is content"
```

### 2. Value Proposition Check

```bash
# Hero section?
grep -rE "hero|Hero|headline|Headline" --include="*.tsx" app/ components/ 2>/dev/null | head -5

# Tagline/headline in content?
grep -rE "<h1|className.*text-(4xl|5xl|6xl)" --include="*.tsx" app/page.tsx 2>/dev/null | head -3

# Feature list?
grep -rE "features|Features|benefits|Benefits" --include="*.tsx" app/ components/ 2>/dev/null | head -5
```

### 3. CTA Check

```bash
# Primary CTA button?
grep -rE "Get Started|Sign Up|Try Free|Start|Join" --include="*.tsx" app/page.tsx components/ 2>/dev/null | head -5

# CTA links to signup/action?
grep -rE "href.*(signup|sign-up|register|get-started|try)" --include="*.tsx" app/ 2>/dev/null | head -5

# Multiple CTAs (hero + below fold)?
cta_count=$(grep -cE "Get Started|Sign Up|Try|Start" app/page.tsx 2>/dev/null || echo "0")
echo "CTA count: $cta_count"
```

### 4. Social Proof Check

```bash
# Testimonials?
grep -rE "testimonial|Testimonial|quote|Quote|review|Review" --include="*.tsx" app/ components/ 2>/dev/null | head -5

# Logos/trust badges?
grep -rE "logo|Logo|trust|Trust|client|Client|company|Company" --include="*.tsx" app/ components/ 2>/dev/null | head -5

# Stats/numbers?
grep -rE "[0-9]+.*users|[0-9]+.*customers|[0-9]+k|[0-9]+\+" --include="*.tsx" app/ 2>/dev/null | head -5
```

### 5. Mobile Responsiveness Check

```bash
# Mobile-first classes?
grep -rE "sm:|md:|lg:|xl:" --include="*.tsx" app/page.tsx 2>/dev/null | head -5

# Mobile menu?
grep -rE "mobile|Mobile|hamburger|Menu.*Icon" --include="*.tsx" components/ 2>/dev/null | head -5

# Responsive images?
grep -rE "sizes=|srcSet|Image.*fill" --include="*.tsx" app/ 2>/dev/null | head -5
```

### 6. Performance Check

```bash
# Static generation?
grep -q "export const dynamic = 'force-static'" app/page.tsx 2>/dev/null && echo "✓ Static page" || echo "- Dynamic page (check if needed)"

# Image optimization?
grep -qE "next/image|Image from" app/page.tsx 2>/dev/null && echo "✓ Next.js Image" || echo "✗ Not using next/image"

# Font optimization?
grep -qE "next/font|font-display" app/layout.tsx 2>/dev/null && echo "✓ Font optimization" || echo "✗ Font not optimized"

# Bundle size concerns?
grep -rE "import.*from 'react-icons|import.*lodash|import.*moment" --include="*.tsx" app/page.tsx 2>/dev/null && echo "⚠ Heavy imports on landing" || echo "✓ No heavy imports"
```

### 7. SEO Essentials

```bash
# Metadata configured?
grep -qE "metadata.*=|generateMetadata" app/page.tsx app/layout.tsx 2>/dev/null && echo "✓ Metadata configured" || echo "✗ No metadata"

# Title and description?
grep -rE "title:|description:" --include="*.tsx" app/page.tsx app/layout.tsx 2>/dev/null | head -3
```

## Output Format

```markdown
## Landing Page Audit

### P0: Critical (No Marketing Presence)
- No landing page - Only app UI, no marketing content
- Landing page redirects to app (no value prop visible)

### P1: Essential (Conversion Blockers)
- No clear value proposition/headline
- No primary CTA button
- CTA text is vague ("Submit" instead of "Start Free Trial")
- No mobile menu (hamburger broken)
- Page not using next/image (slow load)

### P2: Important (Conversion Optimization)
- No social proof (testimonials, logos)
- Only one CTA (need above + below fold)
- No feature comparison section
- No pricing visibility
- Metadata missing (SEO issues)

### P3: Polish (Excellence)
- No customer stats/numbers
- Hero image could be more compelling
- Consider adding demo video
- Add trust badges (security, compliance)
- Add FAQ section

## Current Status
- Landing page: Exists (marketing content)
- Value prop: Unclear
- CTA: Present but weak
- Social proof: None
- Mobile: Responsive
- Performance: Needs optimization

## Summary
- P0: 0 | P1: 4 | P2: 4 | P3: 4
- Recommendation: Strengthen headline and CTA, add testimonials
```

## Priority Mapping

| Gap | Priority |
|-----|----------|
| No landing page | P0 |
| Landing redirects to app | P0 |
| No value prop/headline | P1 |
| No CTA | P1 |
| Weak CTA text | P1 |
| Mobile broken | P1 |
| Slow load time | P1 |
| No social proof | P2 |
| Single CTA | P2 |
| Missing metadata | P2 |
| No stats/numbers | P3 |
| Polish items | P3 |

## Expert Panel Review

When fixing issues found by this audit, all design changes MUST pass expert panel review (90+ average) before delivery. See `ui-skills/references/expert-panel-review.md`.

## Related

- `/log-landing-issues` - Create GitHub issues from findings
- `/fix-landing` - Fix landing page issues (includes mandatory expert review)
- `/copywriting` - Improve marketing copy
- `/cro` - Conversion rate optimization
