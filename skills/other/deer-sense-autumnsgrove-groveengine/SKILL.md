---
name: deer-sense
description: Sense accessibility barriers with gentle awareness. Listen to the forest, scan for obstacles, test the paths, guide toward inclusion, and protect all wanderers. Use when auditing accessibility, testing for a11y, or ensuring inclusive design.
---

# Deer Sense 🦌

The deer moves through the forest with heightened awareness. It hears what others miss—a twig snapping underfoot, a bird's warning call. It notices what blocks the path. The deer guides the herd around danger, ensuring everyone can travel safely. In the digital forest, the deer senses barriers that stop some wanderers from finding their way.

## When to Activate

- User asks to "check accessibility" or "a11y audit"
- User says "make this accessible" or "screen reader test"
- User calls `/deer-sense` or mentions deer/accessibility
- Building new UI components
- Reviewing existing interfaces
- After visual redesigns
- Before major releases
- When accessibility complaints arise

**Pair with:** `chameleon-adapt` for accessible UI implementation

---

## The Sense

```
LISTEN → SCAN → TEST → GUIDE → PROTECT
   ↓        ↲       ↲        ↓         ↓
Hear    Look for  Validate  Teach    Ensure
Needs   Barriers  Paths     Good     Inclusion
```

### Phase 1: LISTEN

*The deer's ears twitch, hearing what others miss...*

Understand accessibility needs:

**Who Are We Building For?**

| Disability Type | Assistive Technology | What They Need |
|----------------|---------------------|----------------|
| **Visual** | Screen readers, magnification | Alt text, semantic HTML, focus indicators |
| **Motor** | Keyboard, switch controls | Keyboard navigation, large touch targets |
| **Cognitive** | Simplified interfaces | Clear language, consistent patterns |
| **Auditory** | Captions, visual indicators | Transcripts, visual alerts |

**WCAG Levels:**

- **A** — Essential (must have)
- **AA** — Ideal (Grove standard)
- **AAA** — Enhanced (when possible)

**Grove Standard: WCAG 2.1 AA**

**Common Barriers:**

```
Visual Barriers:
  - Poor color contrast
  - Missing alt text
  - Keyboard traps
  - No focus indicators

Motor Barriers:
  - Small touch targets (<44px)
  - No keyboard support
  - Time limits too short
  - Required precision

Cognitive Barriers:
  - Confusing navigation
  - Missing error explanations
  - Inconsistent patterns
  - Too much information at once
```

**Output:** Accessibility requirements defined for this project

---

### Phase 2: SCAN

*The deer's eyes scan the forest floor, spotting what blocks the path...*

Automated accessibility scanning:

**axe-core (Recommended):**

```bash
# Install
npm install --save-dev @axe-core/cli

# Run on your site
npx axe https://localhost:5173 --tags wcag2aa

# Or in tests
npm install --save-dev @axe-core/puppeteer
```

**Lighthouse CI:**

```bash
# In CI pipeline
npx lighthouse https://yoursite.com \
  --only-categories=accessibility \
  --output=json

# Look for scores and specific failures
```

**Svelte Accessibility Warnings:**

```svelte
<!-- Svelte warns about common issues -->
<!-- ❌ Missing alt text -->
<img src="photo.jpg">

<!-- ✅ Descriptive alt -->
<img src="photo.jpg" alt="Sunset over the grove">

<!-- ❌ No label -->
<input type="text">

<!-- ✅ Associated label -->
<label for="email">Email</label>
<input id="email" type="text">

<!-- ❌ Click without keyboard -->
<div onclick={handleClick}>

<!-- ✅ Button with keyboard -->
<button onclick={handleClick}>
```

**Common Issues to Check:**

```typescript
// a11y-checklist.ts
const checks = {
  // Images
  imagesHaveAlt: 'All <img> have descriptive alt text',
  decorativeMarked: 'Decorative images have alt=""',
  
  // Forms
  labelsPresent: 'All inputs have associated labels',
  errorsClear: 'Error messages explain how to fix',
  requiredMarked: 'Required fields are indicated',
  
  // Navigation
  focusVisible: 'Focus indicators are visible',
  skipLinks: 'Skip navigation links present',
  headingOrder: 'Headings follow logical order (h1→h2→h3)',
  
  // Color
  contrastAA: 'Text contrast ratio >= 4.5:1',
  contrastLarge: 'Large text contrast >= 3:1',
  notColorOnly: 'Information not conveyed by color alone',
  
  // Structure
  landmarks: 'Page has main, nav, complementary landmarks',
  langAttribute: '<html lang="en"> set correctly',
  titlePresent: 'Each page has unique <title>'
};
```

**Output:** Automated scan results with specific violations

---

### Phase 3: TEST

*The deer tests each path, ensuring it can be traveled...*

Manual accessibility testing:

**Keyboard Navigation:**

```
Test Checklist:
□ Tab through entire page - does order make sense?
□ Can you activate every button/link with Enter/Space?
□ Is there a visible focus indicator on everything?
□ Can you escape modals with Escape key?
□ No keyboard traps (can't Tab away)?
□ Skip link works (jumps past navigation)?
```

**Screen Reader Testing:**

```bash
# NVDA (Windows) - Free
# JAWS (Windows) - Industry standard
# VoiceOver (macOS) - Built-in
# TalkBack (Android) - Built-in
```

**Screen Reader Checklist:**

```
□ Page title announced on load
□ Headings navigate correctly (H key)
□ Landmarks listed (D key)
□ Images have descriptive text
□ Buttons say what they do
□ Form labels read correctly
□ Error messages announced
□ Status updates announced (aria-live)
```

**Reduced Motion:**

```svelte
<script>
  import { reducedMotion } from '$lib/stores/accessibility';
</script>

{#if !$reducedMotion}
  <FallingLeavesLayer />
{:else}
  <!-- Static version for reduced motion -->
  <StaticLeaves />
{/if}
```

**Zoom Testing:**

```
Test at:
□ 100% (normal)
□ 150% (mild vision loss)
□ 200% (moderate vision loss)
□ 400% (severe vision loss)

Verify:
- No horizontal scrolling at 200%
- All content still visible
- No overlapping elements
```

---

**Example Walkthrough Scenarios:**

**Scenario 1: Testing a Form with Conditional Fields**

```
Setup: Multi-step registration form with conditional fields

1. Tab to email field
   ✓ Focus indicator visible?
   ✓ Label announced by screen reader?

2. Enter invalid email, Tab away
   ✓ Error message announced live?
   ✓ Error associated with field (aria-describedby)?

3. Check "Business account" checkbox
   ✓ New company name field appears
   ✓ Focus moves to new field OR stays logical?
   ✓ Screen reader announces new content?

4. Tab through to submit
   ✓ Skip link available to jump sections?
   ✓ Submit button clearly labeled?
   ✓ Can activate with Enter AND Space?
```

**Scenario 2: Testing GroveTerm Components**

```
Setup: Page using GroveTerm/GroveSwap/GroveText for terminology

1. Tab to a GroveTerm element
   ✓ Focus ring visible (2px outline)?
   ✓ aria-label reads "Grove term: [term], [category] category"?
   ✓ role="button" and tabindex="0" present?

2. Activate with Enter or Space
   ✓ Popup opens with definition?
   ✓ Focus moves to popup content?
   ✓ ESC closes popup and returns focus?

3. Toggle Grove Mode OFF
   ✓ Standard terms display (e.g., "Posts" not "Blooms")?
   ✓ Screen reader announces "Grove's name for [standard term]" in popup?
   ✓ GroveSwap silently updates without focus disruption?

4. Check prefers-reduced-motion
   ✓ No animations on GroveTerm hover/open?
   ✓ Popup appears instantly without transition?

5. GroveText with [[term]] syntax
   ✓ Parsed terms are keyboard-navigable?
   ✓ Each rendered GroveTerm has correct aria attributes?
```

**Scenario 3: Testing a Data Table with Sorting**

```
Setup: Posts table with sortable columns

1. Navigate to table
   ✓ Table has caption or aria-label?
   ✓ Column headers use <th scope="col">?
   ✓ Row headers use <th scope="row">?

2. Tab to "Sort by date" column header
   ✓ Sort button focusable?
   ✓ Current sort direction announced (aria-sort)?

3. Activate sort with Enter
   ✓ Table updates without losing focus?
   ✓ Sort change announced (aria-live)?
   ✓ New sort direction reflected?

4. Navigate table with arrow keys (screen reader)
   ✓ Can move cell-by-cell?
   ✓ Row/column context announced?
```

**Scenario 3: Testing a Modal Dialog**

```
Setup: "Delete post" confirmation modal

1. Trigger modal from button
   ✓ Focus moves INTO modal?
   ✓ First focusable element receives focus?
   ✓ Modal has role="dialog" and aria-modal="true"?
   ✓ Modal has accessible name (aria-labelledby)?

2. Tab through modal
   ✓ Focus trapped inside modal?
   ✓ Tab wraps from last to first element?
   ✓ Shift+Tab works backwards?

3. Press Escape
   ✓ Modal closes?
   ✓ Focus returns to trigger button?

4. Click overlay/backdrop
   ✓ Modal closes (if intended behavior)?
   ✓ Or click does nothing (if modal is critical)?
```

**Output:** Manual testing complete with issue log

---

### Phase 4: GUIDE

*The deer guides the herd around obstacles, showing the clear path...*

Fix accessibility issues:

**Color Contrast:**

```svelte
<!-- Check contrast ratios -->
<!-- Use WebAIM contrast checker or similar -->

<!-- Bad: Light gray on white (fails) -->
<p class="text-gray-400">Subtle text</p>

<!-- Good: Darker gray (passes AA) -->
<p class="text-gray-600">Readable text</p>

<!-- Use the palette (already tested for contrast) -->
<p class="text-greens-grove">Brand text</p>
```

**Semantic HTML:**

```svelte
<!-- ❌ Div soup -->
<div class="card" onclick={handleClick}>
  <div class="title">Heading</div>
  <div class="text">Content</div>
</div>

<!-- ✅ Proper semantics -->
<article class="card">
  <h2>Heading</h2>
  <p>Content</p>
  <button onclick={handleClick}>Action</button>
</article>
```

**Focus Management:**

```svelte
<script>
  let modalOpen = $state(false);
  let modalRef: HTMLDivElement;
  let previousFocus: Element;
  
  function openModal() {
    previousFocus = document.activeElement;
    modalOpen = true;
    // Focus first input when modal opens
    tick().then(() => {
      modalRef?.querySelector('input')?.focus();
    });
  }
  
  function closeModal() {
    modalOpen = false;
    // Return focus to trigger button
    previousFocus?.focus();
  }
  
  function handleKeydown(event: KeyboardEvent) {
    if (event.key === 'Escape') closeModal();
  }
</script>

{#if modalOpen}
  <div 
    bind:this={modalRef}
    role="dialog"
    aria-modal="true"
    aria-labelledby="modal-title"
    onkeydown={handleKeydown}
  >
    <h2 id="modal-title">Modal Title</h2>
    <!-- Content -->
  </div>
{/if}
```

**ARIA Labels:**

```svelte
<!-- When visible text isn't enough -->
<button aria-label="Close dialog">
  <XIcon />
</button>

<!-- For icon-only buttons -->
<button aria-label="Add to favorites">
  <HeartIcon />
</button>

<!-- Current state -->
<button aria-pressed={isExpanded}>
  Expand section
</button>

<!-- Live regions for updates -->
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>
```

**Form Accessibility:**

```svelte
<form onsubmit={handleSubmit}>
  <div>
    <label for="email">Email Address *</label>
    <input 
      id="email"
      type="email"
      required
      aria-required="true"
      aria-invalid={emailError ? 'true' : 'false'}
      aria-describedby={emailError ? 'email-error' : undefined}
      bind:value={email}
    />
    {#if emailError}
      <span id="email-error" role="alert" class="error">
        {emailError}
      </span>
    {/if}
  </div>
  
  <button type="submit">Submit</button>
</form>
```

**Output:** Issues fixed with accessible implementations

---

### Phase 5: PROTECT

*The deer stands watch, ensuring the path stays clear...*

Prevent future accessibility issues:

**Automated Testing:**

```typescript
// vitest + @axe-core/puppeteer
import { test } from 'vitest';
import { AxePuppeteer } from '@axe-core/puppeteer';
import puppeteer from 'puppeteer';

test('page has no accessibility violations', async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('http://localhost:5173');
  
  const results = await new AxePuppeteer(page).analyze();
  
  expect(results.violations).toEqual([]);
  await browser.close();
});
```

**ESLint Plugin:**

```bash
npm install --save-dev eslint-plugin-jsx-a11y

# .eslintrc
{
  "plugins": ["jsx-a11y"],
  "extends": ["plugin:jsx-a11y/recommended"]
}
```

**CI Integration:**

```yaml
# .github/workflows/a11y.yml
name: Accessibility Tests
on: [pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: npm ci
      - name: Build site
        run: npm run build
      - name: Run axe-core
        run: npx axe http://localhost:4173 --exit
```

**Documentation:**

```markdown
## Accessibility Standards

This project maintains WCAG 2.1 AA compliance:

### Requirements
- All images have alt text
- Color contrast minimum 4.5:1
- Keyboard navigable
- Screen reader tested
- Reduced motion respected

### Testing
- Automated: axe-core in CI
- Manual: Keyboard + screen reader
- Checklist: See a11y-checklist.md

### Tools
- axe DevTools browser extension
- WAVE evaluation tool
- Lighthouse accessibility audit
```

**Final Report:**

```markdown
## 🦌 DEER SENSE AUDIT COMPLETE

### Pages Tested
- Home page
- Dashboard
- Settings
- Content editor

### Automated Results
- axe-core violations: 3 → 0
- Lighthouse score: 82 → 96

### Manual Testing
- ✅ Keyboard navigation: All paths work
- ✅ Screen reader (VoiceOver): Content readable
- ✅ 200% zoom: Layout intact
- ✅ Reduced motion: Animations disabled

### Issues Fixed
1. Missing alt text on 12 images
2. Color contrast on secondary buttons
3. Missing form labels on search
4. Focus indicator on glass cards

### Ongoing Protection
- axe-core in CI pipeline
- ESLint jsx-a11y plugin enabled
- Accessibility checklist in docs
```

**Output:** Accessibility maintained with ongoing monitoring

---

## Deer Rules

### Awareness
Notice what others miss. Accessibility barriers hide in details.

### Inclusion
Design for everyone. The forest is for all wanderers.

### Persistence
Accessibility is ongoing, not one-time. Keep testing, keep improving.

### Communication
Use sensory metaphors:
- "Listening for barriers..." (understanding needs)
- "Scanning the path..." (automated testing)
- "Testing the route..." (manual verification)
- "Guiding around obstacles..." (fixing issues)

---

## Anti-Patterns

**The deer does NOT:**
- Skip testing with real assistive technology
- Rely only on automated tools (catch ~30% of issues)
- Use "accessibility overlays" (they don't work)
- Ignore cognitive accessibility
- Treat a11y as an afterthought

---

## Example Audit

**User:** "Audit the new dashboard for accessibility"

**Deer flow:**

1. 🦌 **LISTEN** — "Dashboard has complex data, charts, tables. Users: screen reader, keyboard, motor. WCAG AA target."

2. 🦌 **SCAN** — "axe-core: 5 violations. Missing alt on charts, low contrast on metrics, no table headers."

3. 🦌 **TEST** — "Keyboard: Can't reach filter dropdowns. Screen reader: Tables not navigable. Zoom: Sidebar overlaps at 200%."

4. 🦌 **GUIDE** — "Add aria-labels to charts, increase metric contrast, proper table markup, responsive sidebar, keyboard-accessible filters."

5. 🦌 **PROTECT** — "axe-core in CI, component a11y tests, documentation updated."

---

## Quick Decision Guide

| Situation | Action |
|-----------|--------|
| New component | Build with semantic HTML, test keyboard/screen reader |
| Color choice | Check contrast ratio (4.5:1 minimum) |
| Interactive element | Ensure keyboard accessible, visible focus |
| Image | Add descriptive alt text (or alt="" if decorative) |
| Form | Associate labels, error messages, required indicators |
| Animation | Respect prefers-reduced-motion |

---

*The forest welcomes all who seek it. Remove the barriers.* 🦌
