---
name: visual-verdict
description: Screenshot comparison QA for frontend development. Takes a screenshot of the current implementation, scores it across multiple visual dimensions, and returns a structured PASS/REVISE/FAIL verdict with concrete fixes. Use when implementing UI from a design reference or verifying visual correctness.
---

# Visual Verdict — Screenshot QA Skill

Pixel-imprecise human eyes miss visual bugs. This skill provides structured, scored visual review using screenshots, returning actionable verdicts rather than vague impressions.

## When to Activate

- After a frontend-dev agent implements a UI component or page
- When cloning an external website (pairs with clone-website skill)
- After CSS changes to verify no visual regressions
- When a designer provides a Figma export or reference screenshot
- Before marking any UI task as complete

## How It Works

```
1. Take screenshot of current implementation
2. Load reference (design mockup, Figma export, or previous version)
3. Score against 6 dimensions (0-100 each)
4. Compute weighted total score
5. Issue verdict: PASS (90+) / REVISE (60-89) / FAIL (<60)
6. List concrete mismatches with file + line fix hints
7. Loop: frontend-dev fixes → new screenshot → rescore → repeat until PASS
```

## Prerequisites

- browser-use MCP installed and active (`~/.mcp.json`)
- Reference image available (Figma PNG export, screenshot, or URL)
- Implementation running (local dev server or deployed URL)

## Scoring Dimensions

### Dimension Weights

| Dimension | Weight | Description |
|-----------|--------|-------------|
| Layout accuracy | 0.25 | Positioning, spacing, alignment of all elements |
| Typography | 0.15 | Font family, size, weight, line-height, letter-spacing |
| Color accuracy | 0.15 | Background, text, border, shadow, gradient colors |
| Responsive behavior | 0.15 | Breakpoint transitions, mobile/tablet rendering |
| Interactive states | 0.15 | Hover, focus, active, disabled, loading states |
| Content completeness | 0.15 | All text, images, icons, labels present |

### Weighted Score Formula

```
total = (layout * 0.25) + (typography * 0.15) + (color * 0.15)
      + (responsive * 0.15) + (interactive * 0.15) + (content * 0.15)
```

### Scoring Each Dimension (0-100)

**Layout accuracy**
- All elements exactly in position, spacing matches: 90-100
- Minor spacing deviation (< 4px): 75-89
- Noticeable misalignment (4-16px): 50-74
- Layout clearly wrong (columns swapped, elements missing): 0-49

**Typography**
- Font, size, weight, line-height all match: 90-100
- One attribute off (wrong weight only): 70-89
- Two attributes off: 50-69
- Wrong font family entirely: 0-49

**Color accuracy**
- All colors within 5% of reference: 90-100
- One element color clearly off: 65-89
- Multiple elements wrong color: 40-64
- Dark/light mode inverted: 0-39

**Responsive behavior**
- Tested at 3 breakpoints, all correct: 90-100
- One breakpoint breaks layout: 65-89
- Two breakpoints break: 40-64
- Not responsive at all: 0-39

**Interactive states**
- All states implemented and visible: 90-100
- Missing one minor state (loading): 70-89
- Missing hover or focus: 50-69
- No interactive states at all: 0-49

**Content completeness**
- All text, images, icons present: 90-100
- One non-critical item missing: 75-89
- One critical item missing (CTA, heading): 50-74
- Multiple items missing: 0-49

## Verdict Thresholds

| Verdict | Score | Meaning |
|---------|-------|---------|
| PASS | 90-100 | Acceptable for production |
| REVISE | 60-89 | Needs fixes, not shippable |
| FAIL | 0-59 | Major rework required |

## Verdict Output Format

```markdown
## Visual Verdict: [Component/Page Name]

**Score: 85/100 — REVISE**
**Attempt: 2/5**
**Previous score: 72 (+13 this iteration)**

### Dimension Scores
| Dimension | Score | Weight | Weighted | Issues |
|-----------|-------|--------|----------|--------|
| Layout | 92 | 0.25 | 23.0 | Minor padding on mobile |
| Typography | 68 | 0.15 | 10.2 | Wrong font-weight on H2 |
| Color | 96 | 0.15 | 14.4 | - |
| Responsive | 80 | 0.15 | 12.0 | Card grid breaks at 768px |
| Interactive | 82 | 0.15 | 12.3 | Missing hover on CTA |
| Content | 91 | 0.15 | 13.7 | - |
| **TOTAL** | | | **85.6** | |

### Concrete Mismatches (prioritized by impact)

1. **[Typography / HIGH]** H2 hero heading
   Expected: `font-weight: 700`
   Actual: `font-weight: 400` (normal weight)
   Fix: `src/components/Hero.tsx` → add `font-bold` class to `<h2>`

2. **[Responsive / MEDIUM]** Card grid layout
   Expected: 3-column grid collapses at 1024px
   Actual: Collapses at 768px — causes overflow between 768-1024
   Fix: `src/components/CardGrid.tsx` → change `md:grid-cols-3` to `lg:grid-cols-3`

3. **[Interactive / MEDIUM]** Primary CTA button
   Expected: Darker background on hover (`bg-blue-700`)
   Actual: No hover state change
   Fix: `src/components/Hero.tsx` → add `hover:bg-blue-700 transition-colors` to CTA

4. **[Layout / LOW]** Mobile padding
   Expected: 16px horizontal padding on mobile
   Actual: 12px
   Fix: `src/components/Layout.tsx` → change `px-3` to `px-4`

### Next Steps
Fix issues 1-3 above, then call visual-verdict again.
Estimated score after fixes: ~94 (PASS)
```

## Screenshot Workflow with browser-use MCP

### Taking the Current Implementation Screenshot

```
Use browser-use MCP:
1. Navigate to implementation URL (e.g., http://localhost:3000/dashboard)
2. Wait for page fully loaded (no spinners)
3. Take full-page screenshot
4. Save to /tmp/verdict-current-{timestamp}.png
```

### Loading the Reference

Three reference types accepted:

**Figma PNG export**: Designer exports component/page as PNG at 2x
```
Reference path: ~/Desktop/designs/dashboard-v2.png
```

**Previous production screenshot**: Regression check
```
Reference path: ~/.claude/benchmarks/screenshots/dashboard-prod.png
```

**Live URL comparison**: Compare two running versions
```
Reference URL A: http://localhost:3000/dashboard (current)
Reference URL B: https://staging.app.com/dashboard (baseline)
```

### Responsive Testing Breakpoints

Always test at these three widths unless told otherwise:

| Name | Width | Target |
|------|-------|--------|
| Mobile | 375px | iPhone SE |
| Tablet | 768px | iPad portrait |
| Desktop | 1440px | Standard laptop |

## Integration with frontend-dev Agent

The typical iteration loop:

```
frontend-dev implements component
  → visual-verdict takes screenshot + scores
  → REVISE: sends concrete fix list to frontend-dev
  → frontend-dev applies fixes
  → visual-verdict rescores
  → Repeat until PASS (max 5 iterations)
  → PASS: task marked complete
```

### Iteration Limit

Maximum 5 iterations per component. If PASS is not reached after 5 attempts:

```
ESCALATION: Visual QA failed after 5 iterations
Component: [name]
Best score achieved: [score]
Blocker: [specific issue that keeps failing]
Recommendation: [designer clarification needed / fundamentally wrong approach]
```

## Integration with clone-website Skill

When cloning an external site, visual-verdict is the quality gate:

```
1. clone-website skill produces initial implementation
2. visual-verdict screenshots both original and clone
3. Scores similarity across all 6 dimensions
4. REVISE verdict triggers targeted fixes
5. PASS verdict confirms clone is production-ready
```

## Color Comparison Method

Color is compared by extracting computed CSS values and comparing:

```
Reference color:      #1D4ED8  (rgb 29, 78, 216)
Actual color:         #2563EB  (rgb 37, 99, 235)
Delta E (perceived):  6.2 — noticeable, score -15
```

Delta E thresholds:
- Delta E < 2: Imperceptible — full score
- Delta E 2-5: Barely noticeable — minor deduction
- Delta E 5-10: Noticeable — moderate deduction
- Delta E > 10: Clearly wrong — major deduction

## Typography Extraction

Typography is checked by reading computed styles, not pixels:

```javascript
// Extract from running implementation
const element = document.querySelector('.hero-title')
const styles = window.getComputedStyle(element)

{
  fontFamily: styles.fontFamily,        // Compare against reference
  fontSize: styles.fontSize,            // "32px" vs expected "36px"
  fontWeight: styles.fontWeight,        // "400" vs expected "700"
  lineHeight: styles.lineHeight,        // "1.5" vs expected "1.25"
  letterSpacing: styles.letterSpacing   // "normal" vs expected "-0.02em"
}
```

## Common Visual Bugs Caught

- Font weight 400 instead of 700 (bold not applying)
- Tailwind class not included in safelist (purged in build)
- Media query breakpoint uses px when rem expected
- Hover state not added after copy-paste from design
- Icon imported but wrong size prop
- Color defined in CSS variable but variable not set in theme
- Padding/margin using `px-3` when design shows `px-4`
- Z-index issue hiding interactive element
- Border-radius value wrong (rounded vs rounded-lg vs rounded-full)
- Line-clamp not applied, text overflows on mobile

## Saving Screenshots for Regression History

After a PASS verdict, save the screenshot as the new baseline:

```bash
cp /tmp/verdict-current-{timestamp}.png \
   ~/.claude/benchmarks/screenshots/{component-name}-{date}.png
```

On the next change, this saved screenshot becomes the reference for regression comparison.

---

**Remember**: A visual that looks "pretty close" in a quick glance often has 3-5 compounding issues that add up to a broken experience. Score it. Trust the number, not the impression.
