---
name: visual-qa
description: Use vision models to self-review screenshots against design intent. Catches spacing issues, alignment problems, color inconsistencies, responsive bugs, and accessibility gaps. Use when reviewing designs, comparing implementations to mockups, or doing pre-ship QA.
---

# Visual QA

Use vision models to self-review screenshots against design intent. Catch spacing issues, alignment problems, color inconsistencies, responsive bugs, and accessibility gaps before shipping.

## When to Use

- User asks to "review this design" or "check this screenshot"
- After building a page/component, before shipping
- User wants to compare implementation vs mockup/reference
- User asks "does this look right?" or "what's off about this?"
- Automated design QA step in a build workflow

## Core Philosophy

- **Screenshot first, then critique.** Always look at the actual rendered output, not just the code.
- **Be specific.** "The spacing looks off" is useless. "The gap between the heading and paragraph is 32px but should be 16px based on the surrounding spacing rhythm" is useful.
- **Prioritize impact.** Not every pixel matters. Focus on what users will actually notice.
- **Reference the intent.** Compare against design tokens, mockups, or stated design goals.

---

## How to Review

### Step 1: Capture the Screenshot

Use one of these methods to get a screenshot:

**Via browser tool:**
```
browser: screenshot (captures the current page)
```

**Via node screen capture (if available):**
```
nodes: screen_record
```

**Via Peekaboo (macOS):**
```
exec: peekaboo screenshot
```

**User-provided:** The user may paste/attach a screenshot directly.

### Step 2: Analyze with Vision

Use the `image` tool to analyze the screenshot:

```
image: [path or URL to screenshot]
prompt: "Review this UI screenshot for design quality..."
```

### Step 3: Structured Review

Analyze the screenshot against these categories (in priority order):

---

## Review Categories

### 1. Layout & Spacing

**Check for:**
- Consistent spacing rhythm (is everything on the spacing grid?)
- Alignment — are elements that should be aligned actually aligned?
- Padding consistency within similar components
- Container widths and max-widths
- Responsive behavior (if multiple viewport screenshots available)

**Common issues:**
- Inconsistent padding in cards (e.g., 24px top, 16px sides)
- Elements slightly off-grid (15px instead of 16px)
- Text not aligned with adjacent elements
- Sections with wildly different vertical spacing

### 2. Typography

**Check for:**
- Hierarchy — is it clear what's a heading vs body vs caption?
- Line length — body text should be 45–75 characters per line
- Line height — too tight or too loose for the font size?
- Font weight usage — are weights used consistently for the same role?
- Orphans/widows — single words on their own line in headings

**Common issues:**
- Heading that doesn't look like a heading (weight/size too close to body)
- Body text line length > 80 characters (hard to read)
- Inconsistent heading sizes across sections
- All-caps text without letter-spacing adjustment

### 3. Color & Contrast

**Check for:**
- Text/background contrast (does it look readable?)
- Consistent use of brand colors
- Color meaning consistency (is the same blue used for links AND errors?)
- Dark mode issues (if applicable)
- Hover/active state visibility

**Common issues:**
- Light gray text on white background (contrast fail)
- Primary color used for too many different purposes
- Borders that are nearly invisible
- Status colors that conflict (green for danger, red for success)

### 4. Visual Hierarchy

**Check for:**
- Eye flow — where does the eye go first? Is that correct?
- CTA prominence — is the primary action the most visible element?
- Information density — too sparse or too crowded?
- Grouping — are related items visually grouped?
- White space — is it used intentionally or just leftover?

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

### 6. Polish & Micro-details

**Check for:**
- Hover states exist and are visible
- Focus states for keyboard navigation
- Loading states (skeleton screens, spinners)
- Empty states (what shows when there's no data?)
- Transitions between states (abrupt vs smooth)
- Favicon and OG image (if reviewing a full page)

**Common issues:**
- No hover state on interactive elements
- Focus ring removed with no replacement
- Abrupt content shifts when data loads
- No empty state — just a blank area

### 7. Responsive Issues (if multiple viewports available)

**Check for:**
- Content readable on mobile (not too small)
- Touch targets ≥ 44px on mobile
- Navigation accessible on small screens
- Images not overflowing containers
- Horizontal scroll (almost always a bug)

---

## Output Format

### Full Review

```
### Visual QA Review

**Overall impression:** [One sentence — first gut reaction]
**Quality score:** [1-10] / 10

#### 🔴 Critical Issues (fix before shipping)
1. **[Category]:** [Specific issue with exact details]
   → **Fix:** [Actionable recommendation]

#### 🟡 Improvements (should fix)
1. **[Category]:** [Specific issue]
   → **Fix:** [Recommendation]

#### 🟢 Minor Polish (nice to fix)
1. **[Category]:** [Specific issue]
   → **Fix:** [Recommendation]

#### ✅ What's Working Well
- [Specific praise — what's well-executed]
- [Another positive]
```

### Quick Review

```
### Quick QA: [Page/Component Name]

Score: [X]/10

Top 3 fixes:
1. [Most impactful issue + fix]
2. [Second issue + fix]
3. [Third issue + fix]

Looks good: [What's working]
```

### Comparison Review (Implementation vs Mockup)

```
### Design vs Implementation Review

**Fidelity score:** [1-10] / 10

#### Deviations Found
1. **[Element]:** Mockup shows [X], implementation has [Y]
   Impact: [High/Medium/Low]
   → **Fix:** [How to match the mockup]

#### Matching Well
- [Elements that accurately match the design]
```

---

## Review Prompts for Vision Model

Use these prompts with the `image` tool depending on what you need:

### General Review
```
Review this UI screenshot for design quality. Check spacing consistency,
typography hierarchy, color contrast, visual hierarchy, and component
quality. Be specific about issues — reference exact elements and suggest
fixes. Prioritize by impact.
```

### Spacing & Layout Focus
```
Analyze the spacing and layout of this UI. Check if elements follow a
consistent spacing grid, if padding within similar components matches,
if alignment is correct, and if the overall spacing rhythm feels right.
Note any elements that appear off-grid or inconsistently spaced.
```

### Comparison Review
```
Compare these two images. The first is the design mockup, the second is
the implementation. Identify every deviation — differences in spacing,
color, typography, alignment, or missing elements. Rate the fidelity
on a 1-10 scale.
```

### Responsive Check
```
Review this mobile screenshot for responsive design quality. Check that
text is readable, touch targets are large enough (≥44px), nothing
overflows the viewport, and the layout adapts well to the narrow width.
```

### Accessibility Focus
```
Review this UI screenshot for visual accessibility. Check text contrast
against backgrounds, focus indicator visibility, touch target sizes,
color-only information (anything that relies solely on color to convey
meaning), and text readability at the shown sizes.
```

---

## Integration with Build Workflow

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

## Examples

### Example 1: "Review this landing page screenshot"

```
image: [screenshot path]
prompt: "Review this landing page for design quality. Check spacing
consistency, typography hierarchy, visual hierarchy (where does the eye
go first?), CTA prominence, color contrast, and overall polish. Be
specific about issues and suggest fixes. Rate 1-10."
```

### Example 2: "Does my implementation match this Figma design?"

```
image: [mockup.png, implementation.png]
prompt: "Compare these two images. First is the Figma mockup, second
is the implementation. Identify every deviation in spacing, color,
typography, alignment, and missing elements. Rate fidelity 1-10."
```

### Example 3: "Check if this component looks good on mobile"

```
image: [mobile-screenshot.png]
prompt: "Review this mobile UI. Is text readable? Are touch targets
large enough (≥44px)? Does anything overflow? Is the layout well-adapted
to mobile width? Check contrast and spacing."
```
