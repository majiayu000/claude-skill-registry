---
name: ui-audit
description: Comprehensive UI component audit for Momentum CMS. Use when asked to audit, review, check, or validate a UI component. Checks Storybook stories, interaction tests, variants, kitchen sink integration, admin dashboard usage, accessibility, and responsive design (mobile-first). AUTOMATICALLY FIXES issues found and verifies with visual inspection. Triggers include "audit button", "review the card component", "check accessibility of tabs", or "/ui-audit <component-name>".
argument-hint: <component-name>
allowed-tools: Bash(agent-browser:*), Bash(nx *), Read, Glob, Grep, Edit, Write
---

# UI Component Audit

Comprehensive audit combining static code analysis with visual browser inspection via Storybook and kitchen sink. **This skill automatically FIXES issues and VERIFIES fixes visually.**

## ⚠️ CRITICAL: DO NOT SKIP VISUAL INSPECTION ⚠️

**Static code analysis is NOT sufficient.** You MUST perform visual inspection using browser automation (Claude-in-Chrome MCP or agent-browser).

### MANDATORY Visual Inspection Steps

1. **Storybook Screenshots** - Navigate to the component's stories and take screenshots of EVERY story variant in BOTH light and dark mode. If you don't have screenshots, you haven't completed the audit.

2. **Admin Portal Verification** - Navigate to the admin dashboard and verify how the component is actually used. Take screenshots showing real usage. Many bugs are only visible in real usage context.

3. **Responsive Testing** - Resize browser to mobile (375px), tablet (768px), and desktop (1280px) and screenshot each.

### Why This Matters

**Code review alone misses these issues:**

- Badge text invisible against card backgrounds (duplicate CSS variables)
- Borders invisible due to matching colors
- Icons not rendering in Storybook (missing icon provider)
- Hover effects not working
- Focus states not visible
- Spacing issues only visible when rendered

### Verification Checklist (before completing audit)

- [ ] Did I take screenshots of Storybook stories?
- [ ] Did I verify both light AND dark mode visually?
- [ ] Did I navigate to admin portal and see the component in use?
- [ ] Did I test responsive breakpoints visually?
- [ ] Can I visually confirm badges/text are readable?
- [ ] Can I visually confirm hover effects work?

**If any checkbox is unchecked, the audit is INCOMPLETE.**

---

## Requirements Summary

1. **Browser automation** for visual inspection - MUST take screenshots
2. **Auto-fix** - MUST fix issues found, not just report them
3. **Visual verification** - MUST verify fixes with browser screenshots

## Quick Start

```bash
# Audit a component by name
/ui-audit button
/ui-audit data-table
/ui-audit sidebar
```

## Audit Workflow

### Phase 1: Component Discovery

Find all component files:

```bash
# Component location pattern
libs/ui/src/lib/<component>/
├── <component>.component.ts      # Main component
├── <component>.types.ts          # Type definitions (optional)
├── <component>.stories.ts        # Storybook stories
├── <component>.spec.ts           # Unit tests
└── index.ts                      # Barrel export (optional)
```

Verify export in `libs/ui/src/index.ts`.

### Phase 2: Static Code Analysis

Check component follows Angular 21 + Momentum patterns:

**Required Patterns:**

- [ ] Uses `input()` / `input.required()` (not `@Input()`)
- [ ] Uses `output()` (not `@Output()`)
- [ ] Uses `computed()` for derived state
- [ ] Uses `ChangeDetectionStrategy.OnPush`
- [ ] Host styling via `host: { '[class]': 'hostClasses()' }`
- [ ] Accepts `class` input for Tailwind customization
- [ ] Selector prefix: `mcms-`
- [ ] No `standalone: true` (default in Angular 21)

### Phase 3: Variant Coverage

Extract variants from types and verify story coverage:

```typescript
// Example: Button variants
type ButtonVariant = 'primary' | 'secondary' | 'destructive' | 'outline' | 'ghost' | 'link';
type ButtonSize = 'sm' | 'md' | 'lg' | 'icon';
```

**Required Stories:**

- [ ] One story per variant value
- [ ] `AllVariants` or combined story showing all
- [ ] `Sizes` story (if applicable)
- [ ] `Disabled` story
- [ ] Interaction story with `play` function

### Phase 4: Storybook Visual Inspection ⚠️ MANDATORY

**DO NOT SKIP THIS PHASE.** Static code analysis cannot catch visual bugs.

Start Storybook and capture screenshots of EVERY story:

```bash
# Ensure Storybook is running
nx storybook ui --port 4400

# Navigate and screenshot
agent-browser open "http://localhost:4400/?path=/story/components-button--primary"
agent-browser wait --load networkidle
agent-browser screenshot ./audit/button-primary-light.png

# Toggle dark mode (click theme button in toolbar)
agent-browser snapshot -i
agent-browser click @e<theme-toggle-ref>
agent-browser wait 500
agent-browser screenshot ./audit/button-primary-dark.png
```

**What to look for in screenshots:**

- [ ] All text is readable (sufficient contrast)
- [ ] Badges and labels are visible against backgrounds
- [ ] Borders are distinguishable (not same color as background)
- [ ] Icons render correctly (not empty boxes or missing)
- [ ] Hover states show visual feedback
- [ ] Focus rings are visible
- [ ] Component layout matches expected design

**If ANY of these are wrong, you have found a visual bug that code review missed!**

### Phase 5: Interaction Tests

Verify interaction tests pass:

```bash
# Run component tests
nx test ui --testNamePattern="<Component>"

# Check Storybook play functions work
agent-browser open "http://localhost:4400/?path=/story/components-button--click-interaction"
agent-browser wait --load networkidle
# The play function should auto-run
agent-browser screenshot ./audit/button-interaction.png
```

### Phase 6: Kitchen Sink Integration ⚠️ MANDATORY

**DO NOT SKIP THIS PHASE.** Components must be verified in the kitchen sink context.

Verify component appears in kitchen sink:

```bash
# Check import exists in kitchen-sink.page.ts
grep -l "<Component>" libs/ui/src/lib/kitchen-sink/kitchen-sink.page.ts

# Visual verification
nx serve example-angular
agent-browser open "http://localhost:4200/kitchen-sink"
agent-browser wait --load networkidle
agent-browser find text "Buttons" scrollintoview  # or component section
agent-browser screenshot ./audit/kitchen-sink-buttons.png
```

### Phase 6.5: Admin Portal Usage Verification ⚠️ MANDATORY

**DO NOT SKIP THIS PHASE.** Components must be verified in their actual usage context in the admin portal.

Navigate to the admin portal and verify how the component is used in real context:

```bash
# Using Claude-in-Chrome MCP
mcp__claude-in-chrome__tabs_context_mcp({ createIfEmpty: true })
mcp__claude-in-chrome__navigate({ url: "http://localhost:4200/admin", tabId })
mcp__claude-in-chrome__computer({ action: "wait", duration: 2, tabId })
mcp__claude-in-chrome__computer({ action: "screenshot", tabId })
```

**What to verify in Admin Portal:**

- [ ] Component renders correctly in actual usage
- [ ] Component works with real data (not just placeholder)
- [ ] Interactions work (hover, click, expand/collapse)
- [ ] Component integrates well with surrounding components
- [ ] Dark mode toggle works and component looks correct

**Common issues found in Admin Portal:**

- Sidebar icons not rendering (icon provider missing)
- Badge counts invisible (CSS variable conflict)
- Hover effects not firing (event binding issues)
- Focus states not visible (accessibility regression)
- Layout breaking with real data lengths

### Phase 7: Responsive Testing

Test at mobile-first breakpoints:

```bash
# Mobile (iPhone)
agent-browser set viewport 375 812
agent-browser screenshot ./audit/responsive-mobile.png

# Tablet (iPad)
agent-browser set viewport 768 1024
agent-browser screenshot ./audit/responsive-tablet.png

# Desktop
agent-browser set viewport 1280 800
agent-browser screenshot ./audit/responsive-desktop.png

# Large Desktop
agent-browser set viewport 1920 1080
agent-browser screenshot ./audit/responsive-desktop-lg.png
```

### Phase 8: Visual Design Quality ⚠️ CRITICAL - DO NOT SKIP

**THIS PHASE IS THE MOST IMPORTANT.** Code review and static analysis cannot catch visual bugs.

Use browser automation to ACTUALLY LOOK at the UI. Many bugs are only visible when rendered.

#### Theme CSS Variable Analysis

Check for duplicate color values in dark mode (common bug):

```bash
# Search for potentially identical values
grep -A 30 ".dark {" libs/admin/src/styles/theme.css | grep "mcms-"
```

**Red Flags** - Multiple variables with identical HSL values:

```css
/* BAD: These are all the same, badges will be invisible */
--mcms-card: 217 33% 17%;
--mcms-secondary: 217 33% 17%; /* Same as card! */
--mcms-border: 217 33% 17%; /* Same as card! */
```

**Required Color Differentiation:**
| Variable | Purpose | Relative Lightness |
|----------|---------|-------------------|
| `--mcms-card` | Base | 15% |
| `--mcms-secondary` | Badges | 25% (+10) |
| `--mcms-muted` | Subtle BG | 20% (+5) |
| `--mcms-accent` | Hover | 22% (+7) |
| `--mcms-border` | Borders | 22% (+7) |

#### Visual Verification with Browser

```typescript
// Navigate to admin dashboard
mcp__claude-in-chrome__navigate({ url: "http://localhost:4200/admin", tabId })
mcp__claude-in-chrome__computer({ action: "wait", duration: 2, tabId })
mcp__claude-in-chrome__computer({ action: "screenshot", tabId })

// Test hover effect on cards
mcp__claude-in-chrome__computer({ action: "hover", coordinate: [400, 240], tabId })
mcp__claude-in-chrome__computer({ action: "screenshot", tabId })
```

**What to Look For:**

- [ ] Badge counts visible against card backgrounds
- [ ] Card borders distinguishable from background
- [ ] Hover effects provide visual feedback
- [ ] Text contrast is adequate
- [ ] Visual hierarchy is clear

#### Card/Component Quality Checks

- [ ] Cards have hover effects with transitions
- [ ] Shadows are visible (not too subtle)
- [ ] Border radius is consistent (0.75rem recommended)
- [ ] Button spacing is adequate (gap-3 minimum)

#### Dashboard/Page Layout Quality

- [ ] Header has proper hierarchy (text-4xl + subtitle)
- [ ] Sections have headers (uppercase, tracking-wider)
- [ ] Empty states have icons and helpful text
- [ ] Grid responsive breakpoints work (1/2/3 columns)

### Phase 9: UX Design Quality Review ⚠️ CRITICAL - DO NOT SKIP

**Ask yourself: "Would I ship this?"** If the answer is no, the audit FAILS.

This phase catches design quality issues that technical audits miss. Compare against industry standards and ask critical UX questions.

#### Navigation Design Checklist

- [ ] **Icons present** - Every nav item has an icon (not just text)
- [ ] **Active state clear** - Current page has strong visual indicator (left border, background, etc.)
- [ ] **Hover states work** - Items respond visually on hover
- [ ] **Consistent spacing** - No awkward gaps or cramped areas

#### Visual Hierarchy Checklist

- [ ] **Brand presence** - Logo/app name is prominent, not lost
- [ ] **Section headers** - Clear separation between content groups
- [ ] **Empty space intentional** - No large unexplained gaps
- [ ] **Information density** - Not too sparse, not too cramped

#### Industry Comparison

Compare against established admin panels. Ask:

- [ ] Does our sidebar match Payload CMS quality? (icons, active states, collapsible sections)
- [ ] Does it match Strapi? (clean hierarchy, good spacing)
- [ ] Does it match Vercel dashboard? (minimal but complete)

**If our UI is notably worse than these, the audit FAILS.**

#### The "Ship It" Test

Look at the screenshot and honestly answer:

- [ ] Would I be proud to show this to a client?
- [ ] Does it look like a finished product or a prototype?
- [ ] Are there obvious missing elements (icons, borders, indicators)?
- [ ] Is there wasted space that makes it look incomplete?

**If ANY answer is negative, document the issues and FIX THEM before completing the audit.**

#### Common Design Quality Failures

| Issue             | What It Looks Like             | Fix                                     |
| ----------------- | ------------------------------ | --------------------------------------- |
| No icons          | Plain text nav items           | Add Lucide/Heroicons to each item       |
| Weak active state | Subtle background only         | Add left border accent + stronger bg    |
| Empty space       | Big gap between nav and footer | Add more nav items or collapse spacing  |
| No brand          | App name same size as nav      | Make logo/name larger, add icon         |
| Invisible borders | Sidebar bleeds into content    | Increase border-sidebar-border contrast |

### Phase 10: CDK & ARIA Primitives Audit

Verify component uses Angular CDK and @angular/aria primitives correctly.

**Responsive Detection (CDK Layout):**

- [ ] Uses `BreakpointObserver` for responsive detection (NOT `window.innerWidth`)
- [ ] Breakpoints align between CSS (Tailwind) and JS (CDK)
- [ ] SSR-safe with `isPlatformBrowser` check

**Bad:**

```typescript
ngOnInit(): void {
  this.isMobile = window.innerWidth < 768; // WRONG
}
```

**Good:**

```typescript
readonly isMobile = toSignal(
  this.breakpointObserver.observe(['(max-width: 767px)'])
    .pipe(map(result => result.matches)),
  { initialValue: false }
);
```

**Focus Management (CDK A11y):**

- [ ] Uses `cdkTrapFocus` for modals and drawers
- [ ] Uses `FocusMonitor` for focus tracking
- [ ] Uses `LiveAnnouncer` for screen reader announcements

**Positioned Content (CDK Overlay):**

- [ ] Uses CDK Overlay for dropdowns, tooltips, popovers (NOT custom CSS positioning)
- [ ] Handles backdrop click to close
- [ ] Handles Escape key to close

**ARIA Directives (@angular/aria):**

- [ ] Uses `hostDirectives` pattern for semantic behavior
- [ ] Uses Menu/MenuItem for dropdown navigation
- [ ] Uses Tabs/TabList for tab navigation
- [ ] Uses Accordion for collapsible sections

**Flex Child Wrappers:**

- [ ] Wrapper components use `host: { class: 'shrink-0 h-full' }` for proper flex sizing
- [ ] Parent flex layouts properly pass height to children
- [ ] Avoid `class="contents"` - it breaks height inheritance

See [references/angular-primitives.md](references/angular-primitives.md) for complete patterns.

### Phase 10.5: Debugging Common Layout Issues

**⚠️ Dev Server Caching:** Angular dev server may cache stale library code. If fixes aren't appearing:

```bash
# Kill port and restart
lsof -i :4200 | awk 'NR>1 {print $2}' | xargs kill -9
nx serve example-angular
```

**Sidebar Footer Not at Bottom:**

| Symptom                                 | Likely Cause                        | Fix                                       |
| --------------------------------------- | ----------------------------------- | ----------------------------------------- |
| Footer in middle, nav stretches         | ng-content not wrapped              | Add wrapper divs with `shrink-0`/`flex-1` |
| Footer at bottom only when content tall | Using `min-h-screen`                | Change to `h-screen` on aside             |
| Entire sidebar has wrong height         | Parent wrapper uses `contents`      | Change to `shrink-0`                      |
| Footer moves when content grows         | Content not using `overflow-y-auto` | Add `overflow-y-auto` to content div      |

**Key Pattern for Sidebar Flex Layout:**

```html
<aside class="flex flex-col h-screen sticky top-0">
	<div class="shrink-0">Header</div>
	<!-- Fixed size -->
	<div class="flex-1 overflow-y-auto">Content</div>
	<!-- Fills, scrolls -->
	<div class="shrink-0">Footer</div>
	<!-- Fixed size, always at bottom -->
</aside>
```

**Why wrapper divs are required for ng-content:**

- `ng-content` alone creates NO DOM element
- Flex classes (`shrink-0`, `flex-1`) need an element to apply to
- Wrap each `ng-content select="..."` in a div with appropriate flex classes

### Phase 11: Accessibility Audit

Check accessibility requirements:

**ARIA Attributes:**

- [ ] Proper `role` attribute (if not native element)
- [ ] `aria-label` for non-text content
- [ ] `aria-expanded` for expandable elements
- [ ] `aria-selected` for selectable items
- [ ] `aria-disabled` for disabled state

**Focus Management:**

- [ ] Visible focus ring (`:focus-visible`)
- [ ] Logical tab order
- [ ] Keyboard navigation (Arrow keys for lists)

**Color Contrast:**

- [ ] Minimum 4.5:1 for text
- [ ] Focus indicators visible in both themes

### Phase 12: Auto-Fix Issues

**CRITICAL: This skill MUST automatically fix issues, not just report them.**

For each issue found, apply the appropriate fix:

#### Visual Design Fixes

**Fixing invisible badges (duplicate CSS variables):**

```css
/* Before - in theme.css .dark block */
--mcms-secondary: 217 33% 17%; /* Same as card! */

/* After - distinct from card */
--mcms-secondary: 215 28% 25%; /* Visible badge */
```

**Adding card hover effects:**

```typescript
// Before
styles: `
  :host {
    box-shadow: 0 1px 2px 0 rgb(0 0 0 / 0.05);
  }
`,

// After - with hover effect
styles: `
  :host {
    box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
  }
  :host(:hover) {
    box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
  }
`,
```

**Improving dashboard layout:**

```typescript
// Before
<header class="mb-8">
  <h1 class="text-3xl font-bold">Dashboard</h1>
</header>

// After - proper hierarchy with sections
<header class="mb-10">
  <h1 class="text-4xl font-bold tracking-tight">Dashboard</h1>
  <p class="text-muted-foreground mt-3 text-lg">Manage your content</p>
</header>
<section>
  <h2 class="text-sm font-semibold uppercase tracking-wider text-muted-foreground mb-4">
    Collections
  </h2>
  ...
</section>
```

#### Accessibility Fixes

**Missing `aria-label` on icon buttons:**

```typescript
// Before
<button mcms-button variant="ghost" size="icon">
  <svg>...</svg>
</button>

// After - ADD aria-label
<button mcms-button variant="ghost" size="icon" aria-label="Actions menu">
  <svg aria-hidden="true">...</svg>
</button>
```

**Missing `aria-hidden` on decorative icons:**

```typescript
// Before
<svg xmlns="..." class="text-muted-foreground">

// After - ADD aria-hidden="true"
<svg aria-hidden="true" xmlns="..." class="text-muted-foreground">
```

**Missing `aria-label` on search inputs:**

```typescript
// Before
<mcms-input type="text" [placeholder]="searchPlaceholder()" />

// After
<mcms-input type="text" [placeholder]="searchPlaceholder()" aria-label="Search" />
```

#### Story Fixes

**Missing interaction test with `play` function:**

```typescript
// Add to stories file
export const ClickInteraction: Story = {
	render: () => ({
		template: `<mcms-component data-testid="test-element" />`,
	}),
	play: async ({ canvasElement }) => {
		const canvas = within(canvasElement);
		const element = canvas.getByTestId('test-element');
		await expect(element).toBeVisible();
		// Add component-specific interaction tests
	},
};
```

#### Kitchen Sink Fixes

**Component not in kitchen sink:**

1. Add import to `kitchen-sink.page.ts`
2. Add component to imports array
3. Add showcase section in template

### Phase 13: Visual Verification with agent-browser

**REQUIRED: After fixing, verify visually with agent-browser.**

```bash
# 1. Start Storybook if not running
nx storybook ui --port 4400 &

# 2. Wait for Storybook to be ready
sleep 10

# 3. Open component story
agent-browser open "http://localhost:4400/?path=/story/components-<component>--default"
agent-browser wait --load networkidle

# 4. Take screenshot to verify fix
agent-browser screenshot ./audit/<component>-fixed-light.png

# 5. Toggle dark mode and verify
agent-browser snapshot -i
agent-browser click @e<theme-toggle>  # or find theme toggle
agent-browser wait 500
agent-browser screenshot ./audit/<component>-fixed-dark.png

# 6. Test responsive at mobile
agent-browser set viewport 375 812
agent-browser screenshot ./audit/<component>-fixed-mobile.png

# 7. Run interaction test story if exists
agent-browser open "http://localhost:4400/?path=/story/components-<component>--click-interaction"
agent-browser wait --load networkidle
agent-browser screenshot ./audit/<component>-interaction.png
```

### Phase 14: Run Unit Tests

```bash
# Verify all tests still pass after fixes
nx test ui --testNamePattern="<Component>"
```

### Phase 15: Generate Report

Create markdown audit report with BEFORE/AFTER status:

```markdown
# UI Audit Report: <Component>

**Date**: YYYY-MM-DD
**Component**: libs/ui/src/lib/<component>/

## Summary

| Category          | Before | After | Fixed |
| ----------------- | ------ | ----- | ----- |
| Code Patterns     | PASS   | PASS  | -     |
| Variant Coverage  | PASS   | PASS  | -     |
| Interaction Tests | FAIL   | PASS  | ✅    |
| Accessibility     | WARN   | PASS  | ✅    |
| Visual (Light)    | PASS   | PASS  | -     |
| Visual (Dark)     | PASS   | PASS  | -     |
| Responsive        | PASS   | PASS  | -     |
| Kitchen Sink      | PASS   | PASS  | -     |

**Overall**: PASS (2 issues fixed)

## Fixes Applied

1. Added `aria-hidden="true"` to decorative SVG icons
2. Added interaction test with `play` function

## Screenshots (Visual Verification)

- Light mode: ./audit/<component>-fixed-light.png
- Dark mode: ./audit/<component>-fixed-dark.png
- Mobile: ./audit/<component>-fixed-mobile.png

## Tests Passed

✅ All unit tests pass after fixes
```

## Deep-Dive Documentation

| Reference                                                                      | When to Use                                                              |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------ |
| [references/component-patterns.md](references/component-patterns.md)           | Angular 21 signal patterns, host styling                                 |
| [references/variant-coverage.md](references/variant-coverage.md)               | Story requirements, interaction tests                                    |
| [references/accessibility-checklist.md](references/accessibility-checklist.md) | ARIA, focus, keyboard navigation                                         |
| [references/visual-inspection.md](references/visual-inspection.md)             | Storybook URLs, viewport sizes                                           |
| [references/visual-design-quality.md](references/visual-design-quality.md)     | Theme CSS analysis, color contrast, card hover effects, dashboard layout |
| [references/angular-primitives.md](references/angular-primitives.md)           | CDK BreakpointObserver, FocusTrap, Overlay, @angular/aria hostDirectives |

## Ready-to-Use Templates

| Template                                                           | Description                            |
| ------------------------------------------------------------------ | -------------------------------------- |
| [templates/storybook-audit.sh](templates/storybook-audit.sh)       | Screenshot all variants in Storybook   |
| [templates/kitchen-sink-audit.sh](templates/kitchen-sink-audit.sh) | Verify kitchen sink integration        |
| [templates/responsive-audit.sh](templates/responsive-audit.sh)     | Test mobile/tablet/desktop breakpoints |
| [templates/theme-audit.sh](templates/theme-audit.sh)               | Light/dark theme validation            |

## Prerequisites

Before running audit:

1. **Storybook running**: `nx storybook ui --port 4400`
2. **Dev server running**: `nx serve example-angular`
3. **Browser automation**: Either agent-browser CLI OR Claude-in-Chrome MCP tools

## Browser Automation Options

### Option 1: agent-browser CLI

```bash
agent-browser open "http://localhost:4400/?path=/story/components-button--primary"
agent-browser wait --load networkidle
agent-browser screenshot ./audit/button.png
```

### Option 2: Claude-in-Chrome MCP (Preferred)

Use the MCP browser tools when available:

```typescript
// Get tab context
mcp__claude-in-chrome__tabs_context_mcp({ createIfEmpty: true })

// Navigate to Storybook
mcp__claude-in-chrome__navigate({ url: "http://localhost:4400/?path=/story/components-button--primary", tabId })

// Take screenshot
mcp__claude-in-chrome__computer({ action: "screenshot", tabId })

// Resize for responsive testing
mcp__claude-in-chrome__resize_window({ width: 375, height: 812, tabId })

// Read page for accessibility audit
mcp__claude-in-chrome__read_page({ tabId, filter: "interactive" })
```

## Example Audit Output (with Auto-Fix)

```
Auditing: data-table

Phase 1: Discovery
  Found: data-table.component.ts
  Found: data-table.stories.ts (10 stories)
  Found: data-table.spec.ts
  Exported: YES

Phase 2: Static Analysis
  [PASS] Uses input() signals
  [PASS] Uses computed() for hostClasses
  [PASS] ChangeDetectionStrategy.OnPush
  [PASS] Host styling (no wrapper div)
  [PASS] Accepts class input

Phase 3: Variant Coverage
  Stories: 10/10 covered
  [PASS] All features have stories

Phase 4: Storybook Visual (via browser)
  📸 Taking screenshot: data-table-default-light.png
  📸 Taking screenshot: data-table-default-dark.png
  [PASS] Renders correctly in both themes

Phase 5: Interaction Tests
  [WARN] No story with play function found

Phase 6: Kitchen Sink
  [PASS] Component imported
  [PASS] Renders in showcase

Phase 7: Responsive (via browser)
  📸 Screenshot at 375px: data-table-mobile.png
  📸 Screenshot at 768px: data-table-tablet.png
  📸 Screenshot at 1280px: data-table-desktop.png
  [PASS] Responsive layout works

Phase 8: Visual Design Quality (CRITICAL)
  Analyzing theme CSS variables...
  [FAIL] --mcms-secondary same as --mcms-card (badges invisible!)
  [FAIL] --mcms-border same as --mcms-card (borders invisible!)
  [WARN] Card missing hover effect
  📸 Admin dashboard screenshot captured
  [WARN] Dashboard missing section headers

Phase 9: UX Design Quality Review (CRITICAL)
  Comparing against industry standards...
  [FAIL] Nav items missing icons (Payload/Strapi have icons)
  [FAIL] Active state weak (no left border accent)
  [WARN] Large empty space between nav and user section
  [WARN] Brand/logo not prominent enough
  📸 Side-by-side comparison with Payload captured
  "Would I ship this?" → NO

Phase 10: Accessibility
  [WARN] Search input missing aria-label
  [WARN] Sort headers missing aria-label
  [WARN] Row actions button missing aria-label

Phase 11: Auto-Fix
  🔧 Fixing theme.css: --mcms-secondary 217 33% 17% → 215 28% 25%
  🔧 Fixing theme.css: --mcms-border 217 33% 17% → 217 33% 22%
  🔧 Adding card hover effects with transitions
  🔧 Adding icons to all nav items
  🔧 Adding left border accent to active nav state
  🔧 Adding aria-label to search input...
  🔧 Adding interaction test story with play function...

Phase 12: Visual Verification (via browser)
  📸 Verifying fix: badges now visible in dark mode ✅
  📸 Verifying fix: card hover effect working ✅
  📸 Verifying fix: nav icons now visible ✅
  📸 Verifying fix: active state has left border ✅
  📸 Verifying fix: data-table-fixed-dark.png
  [PASS] All fixes verified visually

Phase 13: Unit Tests
  Running: nx test ui --testNamePattern="DataTable"
  [PASS] All 428 tests pass

Phase 14: Report Generated
  Report: ./audit/data-table-report.md

Summary:
  Before: 9 issues (2 CSS, 2 UX design, 3 accessibility, 1 interaction, 1 layout)
  After:  0 issues
  Status: ✅ ALL FIXED
```

---

## ⛔ MANDATORY: Phase Completion Enforcement

**You CANNOT complete the audit until ALL phases are executed.**

Before finishing, you MUST confirm each phase was completed:

| Phase | Name                      | Required Evidence                                           |
| ----- | ------------------------- | ----------------------------------------------------------- |
| 1     | Component Discovery       | Listed all component files                                  |
| 2     | Static Code Analysis      | Checked all code patterns                                   |
| 3     | Variant Coverage          | Verified all variants have stories                          |
| 4     | **Storybook Visual**      | 📸 Took screenshots of stories                              |
| 5     | Interaction Tests         | Ran tests or noted missing play functions                   |
| 6     | **Kitchen Sink**          | 📸 Verified component in kitchen sink                       |
| 6.5   | **Admin Portal**          | 📸 Verified component in admin dashboard                    |
| 7     | **Responsive**            | 📸 Tested at 375px, 768px, 1280px                           |
| 8     | **Visual Design Quality** | Checked CSS variables, hover effects                        |
| 9     | **UX Design Quality**     | Asked "Would I ship this?" - compared to industry           |
| 10    | **CDK & ARIA Primitives** | Checked BreakpointObserver, FocusTrap, Overlay, flex sizing |
| 10.5  | **Debugging**             | Verified dev server cache cleared, layout issues fixed      |
| 11    | Accessibility             | Checked ARIA, focus, keyboard                               |
| 12    | Auto-Fix                  | Fixed all issues found                                      |
| 13    | **Visual Verification**   | 📸 Verified fixes with screenshots                          |
| 14    | Unit Tests                | All tests pass                                              |
| 15    | Report                    | Generated summary                                           |

**Phases marked with 📸 REQUIRE screenshots. If you don't have them, GO BACK.**

### Completion Checklist

Copy and complete this checklist in your final report:

```markdown
## Phase Completion Verification

- [ ] Phase 1: Discovery - files found
- [ ] Phase 2: Static Analysis - patterns checked
- [ ] Phase 3: Variant Coverage - stories verified
- [ ] Phase 4: Storybook - SCREENSHOTS TAKEN (light + dark)
- [ ] Phase 5: Interaction - tests run
- [ ] Phase 6: Kitchen Sink - SCREENSHOT TAKEN
- [ ] Phase 6.5: Admin Portal - SCREENSHOT TAKEN
- [ ] Phase 7: Responsive - SCREENSHOTS at 3 breakpoints
- [ ] Phase 8: Visual Design - CSS variables analyzed
- [ ] Phase 9: UX Design - "Would I ship this?" answered
- [ ] Phase 10: CDK & ARIA - BreakpointObserver, FocusTrap, flex sizing checked
- [ ] Phase 10.5: Debugging - dev server cache cleared, layout issues verified
- [ ] Phase 11: Accessibility - ARIA/focus checked
- [ ] Phase 12: Auto-Fix - all issues fixed
- [ ] Phase 13: Visual Verification - SCREENSHOTS of fixes
- [ ] Phase 14: Unit Tests - all pass
- [ ] Phase 15: Report - generated

**If any box is unchecked, the audit is INCOMPLETE. Go back and finish.**
```

### Why This Enforcement Exists

In a previous audit, I:

- ✓ Did static code analysis
- ✓ Took screenshots
- ✗ Did NOT critically analyze the screenshots
- ✗ Did NOT ask "would I ship this?"
- ✗ Missed obvious issues: no icons, weak active state, empty space

**Result: A technically-passing audit that missed glaring UX problems.**

This enforcement ensures every audit includes genuine design quality review, not just technical compliance.
