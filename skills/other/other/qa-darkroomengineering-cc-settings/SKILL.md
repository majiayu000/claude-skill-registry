---
name: qa
description: |
  Visual QA validation with agent-browser. Use when:
  - User asks to "validate", "check visually", "QA check"
  - After creating or modifying components
  - Before PR submission
  - User mentions "accessibility", "a11y", "contrast", "touch targets"
  - User wants to verify UI looks correct
  - User asks to "review this design" or "check this screenshot"
  - User wants to compare implementation vs mockup/reference
  - User asks "does this look right?" or "what's off about this?"
context: fork
allowed-tools: [Bash]
---

# Visual QA Validation

Comprehensive visual and accessibility validation using agent-browser. Combines automated tooling with structured design review methodology.

## Core Philosophy

- **Screenshot first, then critique.** Always look at the actual rendered output, not just the code.
- **Be specific.** "The spacing looks off" is useless. "The gap between the heading and paragraph is 32px but should be 16px based on the surrounding spacing rhythm" is useful.
- **Prioritize impact.** Not every pixel matters. Focus on what users will actually notice.
- **Reference the intent.** Compare against design tokens, mockups, or stated design goals.

## Quick Start

```bash
# Validate dev server
agent-browser navigate http://localhost:3000
agent-browser screenshot
agent-browser snapshot
```

---

## Review Categories (Priority Order)

### 1. Layout & Spacing

**Check for:**
- Consistent spacing rhythm (is everything on the spacing grid?)
- Alignment -- are elements that should be aligned actually aligned?
- Padding consistency within similar components
- Container widths and max-widths
- No horizontal overflow
- Responsive behavior (if multiple viewport screenshots available)

**Common issues:**
- Inconsistent padding in cards (e.g., 24px top, 16px sides)
- Elements slightly off-grid (15px instead of 16px)
- Text not aligned with adjacent elements
- Sections with wildly different vertical spacing

### 2. Typography

**Check for:**
- Hierarchy -- is it clear what's a heading vs body vs caption?
- Line length -- body text should be 45-75 characters per line
- Line height -- too tight or too loose for the font size?
- Font weight usage -- are weights used consistently for the same role?
- Heading hierarchy is correct (h1 > h2 > h3)
- Orphans/widows -- single words on their own line in headings

**Common issues:**
- Heading that doesn't look like a heading (weight/size too close to body)
- Body text line length > 80 characters (hard to read)
- Inconsistent heading sizes across sections
- All-caps text without letter-spacing adjustment

### 3. Color & Contrast

**Check for:**
- Text meets 4.5:1 contrast ratio
- UI elements meet 3:1 contrast ratio
- Consistent use of brand colors
- Color meaning consistency (is the same blue used for links AND errors?)
- Dark mode issues (if applicable)
- Hover/active state visibility
- UI elements are distinguishable

**Common issues:**
- Light gray text on white background (contrast fail)
- Primary color used for too many different purposes
- Borders that are nearly invisible
- Status colors that conflict (green for danger, red for success)

### 4. Visual Hierarchy

**Check for:**
- Eye flow -- where does the eye go first? Is that correct?
- CTA prominence -- is the primary action the most visible element?
- Information density -- too sparse or too crowded?
- Grouping -- are related items visually grouped?
- White space -- is it used intentionally or just leftover?

**Common issues:**
- Two equally prominent CTAs competing for attention
- Important information buried below less important elements
- Sections that feel disconnected from each other
- Dense walls of text without visual breaks

### 5. Component Quality

**Check for:**
- Button sizing and padding consistency
- Input field styling consistency
- Card styling consistency (shadows, borders, radius)
- Icon sizing and alignment with text
- Image aspect ratios and cropping

**Common issues:**
- Buttons with inconsistent padding or height
- Mixed border-radius values (some 8px, some 12px, some 4px)
- Icons misaligned with adjacent text baselines
- Images stretched or poorly cropped

### 6. Accessibility

- [ ] All images have `alt` text
- [ ] Icon-only buttons have `aria-label`
- [ ] Form inputs have labels
- [ ] Heading hierarchy is correct
- [ ] Focus order is logical
- [ ] Interactive elements >= 44x44px
- [ ] Adequate spacing between touch targets
- [ ] Focus indicators present (no `outline: none` without replacement)

### 7. Polish & Micro-details

**Check for:**
- Hover states exist and are visible
- Focus states for keyboard navigation
- Loading states (skeleton screens, spinners)
- Empty states (what shows when there's no data?)
- Transitions between states (abrupt vs smooth)
- Error states are clear

**Common issues:**
- No hover state on interactive elements
- Focus ring removed with no replacement
- Abrupt content shifts when data loads
- No empty state -- just a blank area

### 8. Responsive Issues (if multiple viewports available)

**Check for:**
- Content readable on mobile (not too small)
- Touch targets >= 44px on mobile
- Navigation accessible on small screens
- Images not overflowing containers
- Horizontal scroll (almost always a bug)

---

## Workflow

1. **Navigate** to target URL
2. **Screenshot** current state
3. **Snapshot** accessibility tree
4. **Analyze** against review categories above
5. **Score** using the output format below
6. **Report** issues with actionable fixes

### After Building a Component

1. Render the component in the browser
2. Take a screenshot
3. Run visual QA review
4. Fix issues
5. Re-screenshot and verify

### After Building a Full Page

1. Screenshot at desktop (1440px), tablet (768px), and mobile (375px)
2. Run responsive review across all three
3. Run full review on the desktop version
4. Fix issues, prioritizing critical ones

### Comparing to a Mockup

1. Get the mockup image (Figma export, screenshot, user-provided)
2. Screenshot the implementation at the same viewport size
3. Run comparison review
4. Fix deviations by priority

---

## Commands

```bash
# Navigate
agent-browser navigate http://localhost:3000/page

# Screenshot
agent-browser screenshot

# Accessibility tree
agent-browser snapshot

# Interact with elements
agent-browser click @e5
agent-browser type @e3 "test input"
```

---

## Output Formats

### Full Review

```
## QA Report: [Page/Component]

**Overall impression:** [One sentence -- first gut reaction]
**Quality score:** [1-10] / 10

### Critical Issues (fix before shipping)
1. **[Category]:** [Specific issue with exact details]
   -> **Fix:** [Actionable recommendation]

### Improvements (should fix)
1. **[Category]:** [Specific issue]
   -> **Fix:** [Recommendation]

### Minor Polish (nice to fix)
1. **[Category]:** [Specific issue]
   -> **Fix:** [Recommendation]

### What's Working Well
- [Specific praise -- what's well-executed]
- [Another positive]

### Passed Checks
- [x] Touch targets adequate
- [x] Heading hierarchy correct

### Issues Found
- [ ] Missing alt text on hero image
  -> Add alt="..." to components/hero/index.tsx:15

- [ ] Contrast too low on muted text
  -> Change text-gray-400 to text-gray-500

### Recommendations
- Consider adding loading skeleton for async content
```

### Quick Review

```
## Quick QA: [Page/Component Name]

Score: [X]/10

Top 3 fixes:
1. [Most impactful issue + fix]
2. [Second issue + fix]
3. [Third issue + fix]

Looks good: [What's working]
```

### Comparison Review (Implementation vs Mockup)

```
## Design vs Implementation Review

**Fidelity score:** [1-10] / 10

### Deviations Found
1. **[Element]:** Mockup shows [X], implementation has [Y]
   Impact: [High/Medium/Low]
   -> **Fix:** [How to match the mockup]

### Matching Well
- [Elements that accurately match the design]
```

---

## Prerequisites

```bash
npm i -g agent-browser@latest
```
