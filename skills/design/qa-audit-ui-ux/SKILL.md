---
name: Audit UI/UX Consistency
description: COMPREHENSIVE UI/UX audit combining code analysis AND visual screenshot analysis. Detects design system violations, visual inconsistencies across views, button/card/modal style variants, color palette chaos, theme breaks, and accessibility issues. Provides detailed visual evidence and prioritized fixes. INCLUDES Storybook design decision workflow for user-driven choices. CRITICAL - Must analyze actual rendered screenshots, not just code.
keywords: design system, consistency, UI, UX, accessibility, design tokens, visual hierarchy, interaction patterns, component design, WCAG, screenshot analysis, visual inconsistency, button variants, card styles, color palette, cross-view comparison, storybook, design decisions, interactive comparison
category: audit
project: PomoFlow
version: "1.2.0"
last_updated: "2025-10-26"
---

# Audit UI/UX Consistency

🎨 **SKILL ACTIVATED: UI/UX Consistency Audit**

## 🎯 Activation Trigger

This skill activates when you mention:
- "audit UI consistency"
- "check design system compliance"
- "review component consistency"
- "UX consistency check"
- "visual inconsistencies"
- "design system violations"
- "accessibility audit"
- "check button styles" / "button inconsistency"
- "card style variants"
- "cross-view consistency"
- "screenshot analysis"
- "visual audit"
- "run the skill on everything"

## Overview

This skill provides comprehensive auditing of the entire Pomo-Flow application combining **code analysis** AND **visual screenshot analysis** to ensure:

### Code-Level Auditing:
1. **Design Token Compliance** - Colors, spacing, typography using CSS custom properties
2. **Component Patterns** - Props, emits, naming, structure consistency
3. **Interaction States** - Hover, focus, active implementation
4. **Accessibility** - WCAG 2.1 compliance, ARIA, keyboard navigation
5. **Animation Timing** - Transition consistency using design tokens

### Visual-Level Auditing (NEW):
6. **Button Style Variants** - Catalog all different button appearances across views
7. **Card/Modal Backgrounds** - Identify inconsistent container styles
8. **Color Palette Usage** - Map actual colors used vs design system
9. **Cross-View Comparison** - Document visual changes between views
10. **Theme Consistency** - Detect theme breaks (light cards in dark app)
11. **Visual Hierarchy** - Ensure similar elements look similar

**Critical Principle**: Code compliance ≠ Visual consistency. You must analyze actual screenshots!

## Audit Philosophy

**Systematic Approach:**
1. **Code Scanning** - Detect design token violations programmatically
2. **Visual Analysis** - Analyze actual screenshots for rendered inconsistencies
3. **Cross-Reference** - Compare code findings with visual evidence
4. **Manual Review** - Assess subjective UX quality and visual hierarchy
5. **Prioritization** - Classify issues by severity (Critical/High/Medium/Low)
6. **Actionable Recommendations** - Provide specific fixes with visual examples
7. **Metrics Tracking** - Measure improvement over time

**Consistency Principles:**
- **Predictability** - Similar actions should have similar visual styles
- **Visual Hierarchy** - Important elements should look important across all views
- **Visual Continuity** - Users shouldn't feel like they're switching apps
- **Feedback** - User actions should have clear, immediate feedback
- **Accessibility** - Everyone should be able to use the application
- **Brand Alignment** - ONE design system consistently applied everywhere

**Two-Level Auditing:**
- **Code Level**: Check design token usage, component patterns, ARIA attributes
- **Visual Level**: Verify how it actually looks to users across views (screenshots required!)

## Comprehensive Audit Checklist

### 1. Visual Consistency Audit

#### Color Usage
```bash
# Scan for hardcoded colors (should use design tokens instead)
grep -r "color: #" src/components
grep -r "background: #" src/components
grep -r "border.*#[0-9a-fA-F]" src/components

# Check for rgb() or hsl() values not using var()
grep -r "rgb(" src/components | grep -v "var(--"
grep -r "hsl(" src/components | grep -v "var(--"
```

**What to Check:**
- ✅ All colors use CSS custom properties from `design-tokens.css`
- ✅ No hardcoded hex values (#000000, #ffffff, etc.)
- ✅ Semantic color usage (--text-primary, not --gray-100)
- ✅ Proper use of tier system (Base → Semantic → Component)
- ❌ Hardcoded colors outside design token system
- ❌ Inconsistent color naming across components

#### Spacing & Layout
```bash
# Scan for hardcoded spacing values
grep -r "padding: [0-9]" src/components
grep -r "margin: [0-9]" src/components
grep -r "gap: [0-9]" src/components

# Check for non-8px-grid values
grep -r "padding: .*px" src/components | grep -v "0px\|4px\|8px\|12px\|16px\|20px\|24px\|32px\|40px\|48px"
```

**What to Check:**
- ✅ 8px grid system adherence (4px, 8px, 12px, 16px, etc.)
- ✅ Spacing uses design tokens (--space-2, --space-4, etc.)
- ✅ Consistent padding/margin within component types
- ✅ Proper use of Tailwind spacing classes (p-2, m-4, gap-3)
- ❌ Random spacing values (e.g., 13px, 17px)
- ❌ Inconsistent spacing patterns between similar components

#### Typography
```bash
# Check for hardcoded font sizes
grep -r "font-size: [0-9]" src/components
grep -r "line-height: [0-9]" src/components

# Find font-weight violations
grep -r "font-weight: [0-9]" src/components | grep -v "var(--font-"
```

**What to Check:**
- ✅ Font sizes use type scale (--text-xs through --text-3xl)
- ✅ Line heights use design tokens (--leading-tight, --leading-normal)
- ✅ Font weights consistent (--font-normal, --font-medium, --font-semibold)
- ✅ Consistent font family usage (--font-primary, --font-mono)
- ❌ Random font sizes outside type scale
- ❌ Inconsistent heading hierarchy

#### Border Radius
```bash
# Check for hardcoded border radius
grep -r "border-radius: [0-9]" src/components | grep -v "var(--radius-"
```

**What to Check:**
- ✅ Border radius uses design tokens (--radius-sm, --radius-md, --radius-lg)
- ✅ Consistent rounding for similar components (all buttons same, all cards same)
- ✅ Proper Tailwind classes (rounded-sm, rounded-md, rounded-lg)
- ❌ Random border-radius values
- ❌ Mixing radius scales within component type

#### Shadows & Elevation
```bash
# Check for hardcoded shadows
grep -r "box-shadow:" src/components | grep -v "var(--shadow-"
```

**What to Check:**
- ✅ Elevation system follows defined scale (--shadow-xs through --shadow-2xl)
- ✅ Glass effects use glass-specific shadows (--shadow-glass)
- ✅ Consistent shadow usage for similar elevations
- ❌ Custom shadow values outside design system
- ❌ Inconsistent elevation hierarchy

### 2. Component Design Audit

#### Component Structure
**Check Each Component For:**
```vue
<script setup lang="ts">
// ✅ Consistent import ordering
import { ref, computed, onMounted } from 'vue'
import { useTaskStore } from '@/stores/tasks'
import type { Task } from '@/types'

// ✅ Props interface with proper types
interface Props {
  taskId: string
  variant?: 'default' | 'compact'
}
const props = withDefaults(defineProps<Props>(), {
  variant: 'default'
})

// ✅ Emits definition
const emit = defineEmits<{
  update: [task: Task]
  delete: [id: string]
}>()

// ✅ Consistent reactive state pattern
const isLoading = ref(false)
const localState = computed(() => store.getTask(props.taskId))
</script>
```

**What to Check:**
- ✅ Consistent script setup structure (imports → props → emits → state → methods → lifecycle)
- ✅ TypeScript types for all props and emits
- ✅ Prop naming conventions (camelCase)
- ✅ Default values for optional props
- ✅ Computed properties for derived state
- ✅ Proper error handling in async operations
- ❌ Inconsistent prop naming across similar components
- ❌ Missing TypeScript types
- ❌ Inconsistent state management patterns

#### Component Naming
```bash
# Check component naming conventions
find src/components -name "*.vue" | grep -v "^[A-Z]"
```

**What to Check:**
- ✅ PascalCase for component filenames (TaskCard.vue, CalendarView.vue)
- ✅ Descriptive, self-documenting names
- ✅ Consistent prefixes (Base*, Canvas*, Kanban*)
- ✅ Matching filename and component name
- ❌ Vague names (Wrapper.vue, Container.vue, Thing.vue)
- ❌ Inconsistent naming patterns

#### Props Consistency
**Common Patterns to Verify:**
```typescript
// Task-related components should share prop patterns
interface TaskComponentProps {
  taskId: string          // ✅ Consistent ID prop
  variant?: 'default' | 'compact' | 'minimal'  // ✅ Shared variant types
  readonly?: boolean      // ✅ Shared modifier props
}

// Modal components should share patterns
interface ModalProps {
  show: boolean           // ✅ Consistent visibility prop
  title?: string
  closable?: boolean
}
```

### 3. Interaction Pattern Audit

#### Hover States
**Check for Consistency:**
```css
/* ✅ Good: Consistent hover pattern using design tokens */
.button {
  background: var(--surface-secondary);
  transition: all var(--duration-normal) var(--spring-smooth);
}

.button:hover {
  background: var(--surface-hover);
  transform: translateY(-1px);
  box-shadow: var(--shadow-md);
}

/* ❌ Bad: Hardcoded values, inconsistent timing */
.button:hover {
  background: #374151;
  transition: 0.3s;
}
```

**What to Check:**
- ✅ Transition timing uses design tokens (--duration-fast, --duration-normal)
- ✅ Easing curves consistent (--spring-smooth, --spring-bounce)
- ✅ Similar components have similar hover effects
- ✅ Visual feedback is immediate and obvious
- ❌ No hover state on interactive elements
- ❌ Inconsistent timing between similar components

#### Focus States (Keyboard Navigation)
```css
/* ✅ Good: Visible focus indicator */
.interactive:focus-visible {
  outline: 2px solid var(--brand-primary);
  outline-offset: 2px;
  box-shadow: var(--purple-glow-focus);
}

/* ❌ Bad: Focus state removed or invisible */
button:focus {
  outline: none; /* DON'T DO THIS */
}
```

**What to Check:**
- ✅ All interactive elements have visible focus indicators
- ✅ Focus indicators meet 3:1 contrast ratio (WCAG 2.1)
- ✅ Focus order is logical and intuitive
- ✅ Keyboard navigation works for all interactions
- ❌ outline: none without alternative focus indicator
- ❌ Invisible or insufficient focus indicators

#### Active/Pressed States
**What to Check:**
- ✅ Buttons show pressed state (transform: scale(0.98))
- ✅ Active states use design tokens (--state-active-bg, --state-active-border)
- ✅ Consistent feedback across button types
- ❌ No visual feedback when clicking
- ❌ Inconsistent active states

#### Loading & Disabled States
**What to Check:**
- ✅ Loading states show spinners or skeleton screens
- ✅ Disabled states use --text-disabled and reduce opacity
- ✅ Disabled elements not focusable or clickable
- ✅ Clear visual distinction between enabled/disabled
- ❌ Disabled elements still interactive
- ❌ No loading feedback for async operations

### 4. Accessibility Audit (WCAG 2.1)

#### Semantic HTML
```vue
<!-- ✅ Good: Semantic, accessible markup -->
<template>
  <article class="task-card">
    <h3>{{ task.title }}</h3>
    <p>{{ task.description }}</p>
    <button aria-label="Edit task">
      <EditIcon aria-hidden="true" />
    </button>
  </article>
</template>

<!-- ❌ Bad: Divs for everything, no labels -->
<template>
  <div class="task-card">
    <div>{{ task.title }}</div>
    <div>{{ task.description }}</div>
    <div @click="edit">
      <EditIcon />
    </div>
  </div>
</template>
```

**What to Check:**
- ✅ Proper heading hierarchy (h1 → h2 → h3, no skipping)
- ✅ Semantic elements (nav, main, article, section, aside)
- ✅ Buttons for actions, links for navigation
- ✅ Lists use ul/ol, not div soup
- ❌ Generic divs used for semantic content
- ❌ Headings used for styling, not structure

#### ARIA Labels & Roles
```vue
<!-- ✅ Good: Proper ARIA usage -->
<button
  aria-label="Delete task: Buy groceries"
  aria-describedby="delete-help"
>
  <TrashIcon aria-hidden="true" />
</button>
<span id="delete-help" class="sr-only">
  This action cannot be undone
</span>

<!-- ❌ Bad: Icon button with no label -->
<button @click="deleteTask">
  <TrashIcon />
</button>
```

**What to Check:**
- ✅ Icon buttons have aria-label or sr-only text
- ✅ Decorative icons have aria-hidden="true"
- ✅ Form inputs have associated labels
- ✅ Interactive elements have descriptive names
- ✅ Dynamic content changes announced (aria-live)
- ❌ Icon-only buttons without labels
- ❌ Forms without labels
- ❌ Missing or incorrect ARIA roles

#### Color Contrast
**Check Contrast Ratios:**
- ✅ Normal text: 4.5:1 minimum (WCAG AA)
- ✅ Large text (18px+): 3:1 minimum
- ✅ Interactive elements: 3:1 for boundaries
- ✅ Focus indicators: 3:1 against background
- ❌ Low contrast text (gray on gray)
- ❌ Insufficient focus indicator contrast

#### Keyboard Navigation
**Test All Interactions:**
- ✅ Tab order is logical
- ✅ All functionality available via keyboard
- ✅ Focus trap in modals (can't tab outside)
- ✅ Escape key closes modals/dropdowns
- ✅ Arrow keys for navigation where appropriate
- ✅ Enter/Space activates buttons
- ❌ Keyboard traps (can't escape element)
- ❌ Tab order jumping around randomly
- ❌ Mouse-only interactions

### 5. Design System Compliance

#### CSS Custom Properties Usage
```bash
# Find components not using design tokens
grep -r "color: #" src/components
grep -r "background: rgb" src/components | grep -v "var(--"
```

**Tier Compliance:**
```css
/* ✅ Good: Proper tier usage */
.component {
  background: var(--surface-secondary);  /* Semantic token */
  color: var(--text-primary);
  border: 1px solid var(--border-subtle);
  padding: var(--space-4);
  border-radius: var(--radius-md);
}

/* ❌ Bad: Using base palette directly */
.component {
  background: hsl(var(--gray-900));  /* Should use --surface-secondary */
  color: hsl(var(--gray-100));       /* Should use --text-primary */
}
```

**What to Check:**
- ✅ Semantic tokens used, not base palette
- ✅ Component-level tokens for specialized components
- ✅ Proper cascade: Base → Semantic → Component
- ❌ Direct use of base palette (--gray-100, --blue-500)
- ❌ Hardcoded values instead of tokens

#### Tailwind Class Consistency
```vue
<!-- ✅ Good: Consistent Tailwind usage -->
<div class="flex items-center gap-2 p-4 rounded-md bg-surface-secondary">
  <Icon class="w-5 h-5 text-text-muted" />
  <span class="text-sm font-medium">Content</span>
</div>

<!-- ❌ Bad: Mixing inline styles with Tailwind -->
<div class="flex items-center" style="gap: 8px; padding: 16px">
  <Icon style="width: 20px" />
  <span class="text-sm" style="font-weight: 500">Content</span>
</div>
```

**What to Check:**
- ✅ Prefer Tailwind classes over inline styles
- ✅ Consistent spacing (gap-2, gap-4, gap-6)
- ✅ Semantic color classes (bg-surface-secondary, text-text-primary)
- ❌ Mixing inline styles and Tailwind
- ❌ Hardcoded style attributes

#### Glass Morphism Consistency
**Check Glass Effects:**
```css
/* ✅ Good: Using glass utilities */
.glass-card {
  background: var(--glass-bg-light);
  backdrop-filter: blur(var(--blur-md));
  border: 1px solid var(--glass-border);
}

/* ❌ Bad: Custom glass effect */
.custom-glass {
  background: rgba(255, 255, 255, 0.07);
  backdrop-filter: blur(20px);
}
```

**What to Check:**
- ✅ Glass effects use design token opacity values
- ✅ Backdrop blur uses defined scale (--blur-sm, --blur-md, --blur-lg)
- ✅ Glass borders consistent (--glass-border, --glass-border-hover)
- ❌ Custom rgba values for glass backgrounds
- ❌ Inconsistent blur amounts

### 6. Animation & Transitions

#### Timing Consistency
```css
/* ✅ Good: Consistent timing from design system */
.button {
  transition: all var(--duration-normal) var(--spring-smooth);
}

.modal {
  transition: opacity var(--duration-fast) var(--spring-smooth);
}

/* ❌ Bad: Random timing values */
.button {
  transition: all 0.25s ease;
}

.modal {
  transition: opacity 150ms cubic-bezier(0.4, 0, 0.2, 1);
}
```

**What to Check:**
- ✅ Duration uses tokens (--duration-fast, --duration-normal, --duration-slow)
- ✅ Easing curves consistent (--spring-smooth, --spring-bounce)
- ✅ Similar animations have similar timing
- ✅ Respects prefers-reduced-motion
- ❌ Hardcoded timing values
- ❌ Inconsistent easing between components

#### Animation Performance
**What to Check:**
- ✅ Animations use transform/opacity (GPU accelerated)
- ✅ No layout thrashing (changing width/height in animations)
- ✅ Animations are cancelable/interruptible
- ❌ Animating width, height, top, left directly
- ❌ Forced synchronous layouts during animation

### 7. Visual Inconsistency Audit (Screenshot Analysis)

> **CRITICAL**: Code scanning alone is insufficient. You MUST analyze actual rendered screenshots to catch visual inconsistencies that don't show up in code audits.

#### Why Visual Auditing is Essential

**Code audits miss:**
- Different button styles that all use "correct" code but look completely different
- Color palette chaos (teal vs blue vs purple used inconsistently)
- Modal background variations that break visual continuity
- Theme inconsistencies (light cards in dark app)
- Component style variants across different views
- Visual hierarchy problems only visible when rendered

**The Rule**: If users see it, audit it visually - not just the code.

#### Visual Audit Methodology

##### Step 1: Screenshot Collection
```bash
# Required screenshots for complete audit
# Save to: docs/debug/ or docs/screenshots/

1. All main views:
   - Board view (with tasks)
   - Calendar view (with events)
   - Canvas view (with task nodes)
   - All Tasks view (list/table mode)

2. All modal states:
   - Settings modal (all tabs)
   - Create Task modal
   - Task Edit modal
   - Project modal
   - Context menus

3. Component states:
   - Buttons (default, hover, active, disabled)
   - Cards (default, selected, hover)
   - Forms (empty, filled, error)
   - Toggles/switches (on, off)

4. Theme variations:
   - Light theme (all views)
   - Dark theme (all views)
   - High contrast mode

5. Interaction states:
   - Hover effects
   - Focus indicators
   - Loading states
   - Error states
```

**Screenshot Naming Convention**:
```
docs/debug/
├── view-board-default.png
├── view-canvas-with-tasks.png
├── view-alltasks-light-theme.png
├── modal-settings-pomodoro.png
├── modal-create-task.png
├── component-buttons-all-variants.png
└── interaction-hover-states.png
```

##### Step 2: Visual Style Inventory

**Catalog ALL variants of each component type:**

**Button Style Variants**:
```
For EACH unique button style found, document:
- Screenshot location
- Visual description (color, shape, size, border)
- Where it's used (component/view)
- What makes it different from other buttons

Example findings:
1. Pomodoro time selection: Teal (#4ECDC4) rounded, dark bg
2. Create Task button: Blue (#4A90E2) rounded, prominent
3. Canvas toolbar: Square teal icons, transparent bg
4. Theme toggle: Yellow star emoji + teal border (UNIQUE!)
5. Test sound buttons: Dark + icon + text combo
6. View toggles: Blue pill group
7. Cancel buttons: Gray secondary style
```

**Card/Modal Variants**:
```
For EACH unique card/modal style, document:
- Background color/tint
- Border style and color
- Glass effect usage
- Padding/spacing
- Corner radius
- Shadow/elevation

Example findings:
1. Settings modal: Dark glass, light gray border
2. Create Task modal: Blue-tinted dark (DIFFERENT!)
3. All Tasks cards: WHITE background (breaks dark theme!)
4. Canvas task cards: Dark + TEAL borders
5. Board task cards: [need screenshot]
```

**Color Palette Usage**:
```
For EACH color used, catalog:
- Hex/RGB value (approximate from screenshot)
- Where it's used (which views/components)
- Semantic meaning (if any)
- Consistency across usage

Example findings:
1. Teal #4ECDC4:
   - Settings: Selection states, toggle active
   - Canvas: Borders, icons, theme toggle border
   - Inconsistent usage: Sometimes primary, sometimes accent

2. Blue #4A90E2:
   - Create Task: Primary button
   - All Tasks: View toggle selected state
   - Inconsistent: Not used in Canvas view at all

3. Yellow #FBBF24:
   - ONLY in Canvas theme toggle star emoji
   - No other usage found (orphaned color!)
```

##### Step 3: Cross-View Comparison Matrix

**Create side-by-side comparison table:**

| Element | Board View | Canvas View | Calendar View | All Tasks View | Settings Modal |
|---------|------------|-------------|---------------|----------------|----------------|
| **Background** | Dark | Dark | Dark | **WHITE!** | Dark glass |
| **Primary Color** | ? | **Teal** | ? | **Blue** | **Teal** |
| **Card Style** | Style A | Teal borders | Style C | White cards | N/A |
| **Button Style** | ? | Square teal | ? | Blue pills | Rounded teal |
| **Text Color** | White | White | White | **Dark!** | White |

**User Experience Test**:
- Navigate: Board → Canvas → All Tasks → Settings
- Document: What visual changes does user see?
- Identify: Which changes feel like "different app"?

##### Step 4: Visual Violation Detection

**Automated from screenshots:**
```python
# Pseudo-code for visual analysis
for each screenshot in screenshots_dir:
    extract_colors()  # Get all colors used
    detect_buttons()  # Find button shapes/styles
    measure_spacing()  # Check padding/margins
    analyze_hierarchy()  # Visual weight distribution
    check_contrast()  # WCAG color contrast ratios
```

**Manual review checklist:**
```
For each screenshot, ask:
□ Do buttons look consistent with other views?
□ Are card backgrounds the same style?
□ Is primary color used consistently?
□ Does theme (dark/light) match other views?
□ Are shadows/elevations consistent?
□ Do similar elements have similar visual weight?
□ Is spacing rhythm consistent?
□ Are border radii the same for similar elements?
```

##### Step 5: Visual Inconsistency Report

**Report format for visual findings:**

```markdown
## Visual Inconsistency: [Description]

### Evidence
**Screenshots**:
- [view-canvas.png] - Shows teal buttons
- [modal-create-task.png] - Shows blue button (DIFFERENT!)

### Visual Comparison
| Location | Button Color | Button Shape | Border | Background |
|----------|--------------|--------------|--------|------------|
| Canvas toolbar | Teal #4ECDC4 | Square | None | Transparent |
| Create Task | Blue #4A90E2 | Rounded | None | Solid blue |

### Impact
- **Severity**: 🔴 Critical
- **User Experience**: Feels like different design systems
- **Affected Views**: Canvas, All modals
- **Visual Disruption**: High - primary color changes

### Root Cause
Components hardcode different colors instead of using unified `var(--brand-primary)`

### Fix
**Standardize to ONE primary color:**
```css
/* Option 1: Use teal everywhere */
--brand-primary: #4ECDC4;

/* Option 2: Use blue everywhere */
--brand-primary: #4A90E2;

/* Then replace in components: */
.canvas-button {
  - color: #4ECDC4;
  + color: var(--brand-primary);
}

.modal-button {
  - background: #4A90E2;
  + background: var(--brand-primary);
}
```

### Verification
**After fix, verify:**
1. Take new screenshot of Canvas view
2. Take new screenshot of Create Task modal
3. Compare button colors - should match exactly
4. Verify no other colors leaked in
```

#### Common Visual Inconsistencies to Check

**1. Button Chaos**
```
Questions to answer:
- How many different button styles exist?
- Do similar buttons look similar?
- Is primary action always same style?
- Are icon buttons consistent?
- Do toggles/switches match?

Red flags:
❌ 5+ different button styles for same function
❌ Square buttons in one view, rounded in another
❌ Different primary colors (teal vs blue)
❌ Unique styles that exist nowhere else
```

**2. Card/Modal Inconsistency**
```
Questions to answer:
- Do all cards use same background?
- Are modal backgrounds consistent?
- Do borders match across views?
- Are shadows/elevation consistent?

Red flags:
❌ White cards in dark-themed app
❌ Blue-tinted modal vs neutral modal
❌ Thick borders in one view, subtle in another
❌ Different glass effects per component
```

**3. Color Palette Anarchy**
```
Questions to answer:
- What is THE primary brand color?
- Is it used consistently everywhere?
- How many accent colors are used?
- Do colors have semantic meaning?

Red flags:
❌ Teal in Canvas, blue in modals (no standard)
❌ 6+ different colors with no clear purpose
❌ Same color used for different meanings
❌ Different colors used for same meaning
```

**4. Theme Breaks**
```
Questions to answer:
- Is dark theme consistent across views?
- Do any components break theme?
- Are theme transitions smooth?

Red flags:
❌ Light cards appearing in dark theme
❌ Text color switching (white → dark)
❌ Different background tints per view
❌ Theme-breaking components
```

**5. Typography Chaos**
```
Questions to answer (from screenshots):
- Are heading sizes consistent?
- Is body text same size/weight?
- Do labels match across forms?

Red flags:
❌ Random font sizes visible
❌ Inconsistent heading hierarchy
❌ Different text weights for same element
```

#### Visual Audit Execution

**Complete workflow:**

1. **Collect Screenshots** (30 min)
   - Use Playwright MCP or manual screenshots
   - Cover all views, modals, states
   - Save with descriptive names

2. **Visual Inventory** (1 hour)
   - Catalog all button variants
   - Document all card/modal styles
   - List all colors used
   - Note spacing/typography patterns

3. **Cross-View Comparison** (30 min)
   - Create comparison matrix
   - Identify view-to-view inconsistencies
   - Document theme breaks

4. **Prioritize Issues** (30 min)
   - Critical: Breaks user experience
   - High: Confusing/inconsistent
   - Medium: Could be better
   - Low: Minor polish

5. **Generate Report** (1 hour)
   - Visual examples for each issue
   - Side-by-side comparisons
   - Specific fix recommendations
   - Implementation priority

**Total audit time**: ~3.5 hours for comprehensive visual audit

#### Visual Audit Checklist

Before completing visual audit, verify:

- [ ] Collected screenshots from all main views
- [ ] Captured all modal states
- [ ] Documented every button style variant (count them!)
- [ ] Cataloged all card/modal background variations
- [ ] Listed all colors used with hex values
- [ ] Created cross-view comparison matrix
- [ ] Identified theme-breaking components
- [ ] Measured visual hierarchy consistency
- [ ] Checked spacing rhythm across views
- [ ] Verified typography scale adherence
- [ ] Noted any "orphaned" styles (used once, nowhere else)
- [ ] Created prioritized fix list with visual examples
- [ ] Recommended ONE unified style for each component type

**Remember**: If you didn't look at screenshots, you didn't do a visual audit!

---

### 8. Composition & Alignment Audit (Layout Analysis)

> **PURPOSE**: Verify that elements are properly aligned, spaced, and balanced for professional visual composition.

#### Why Composition Auditing is Essential

**Layout issues that break professionalism:**
- Toolbar buttons not vertically aligned (ragged edges)
- Inconsistent spacing between grouped elements (visual chaos)
- Elements not aligned to grid/baseline (sloppy appearance)
- Poor visual balance (one side feels "heavier")
- Broken visual rhythm (random spacing breaks flow)
- Misaligned text baselines (amateur look)
- Floating elements without clear relationship to layout grid

**The Rule**: Professional UIs have invisible grids - everything aligns to something.

#### Composition Audit Methodology

##### 1. Element Alignment Check

**What to verify:**

```
Horizontal Alignment:
✅ Left-aligned elements share same left edge
✅ Right-aligned elements share same right edge
✅ Center-aligned elements share same center axis
✅ Text baselines align in horizontal layouts

Vertical Alignment:
✅ Stacked buttons align vertically (no ragged edges)
✅ Icon + text pairs align on same baseline
✅ Column content aligns to top/middle/bottom consistently
✅ Toolbar items distribute evenly or align to grid
```

**How to check** (screenshot analysis):
1. Draw imaginary vertical lines down element edges
2. Draw imaginary horizontal lines across text baselines
3. Check if elements snap to these invisible guides
4. Note any elements that "float" off-grid

**Red flags in screenshots:**
```
❌ Toolbar buttons with ragged left/right edges
❌ Icon buttons of different sizes in same toolbar
❌ Text labels starting at different X positions
❌ Stacked elements with random indentation
❌ Groups of buttons not forming clean rectangles
❌ Mixed alignment (some centered, some left, no pattern)
```

##### 2. Spacing Rhythm Verification

**The 8px Grid System Rule:**
```
All spacing MUST be multiples of 8px:
- 8px  (--space-2)  = Tight spacing within component
- 16px (--space-4)  = Standard component padding
- 24px (--space-6)  = Between related groups
- 32px (--space-8)  = Between sections
- 40px (--space-10) = Major section breaks
```

**What to verify:**

```
Within Component:
✅ Padding uses --space-4 (16px) consistently
✅ Icon-to-text gaps use --space-2 or --space-3
✅ Button internal padding matches across variants

Between Components:
✅ Sibling buttons have same gap (--space-2 or --space-3)
✅ Form field spacing matches (--space-4)
✅ Card content spacing follows rhythm

Between Sections:
✅ Major sections use --space-8+ consistently
✅ Toolbar-to-content gap standardized
✅ Modal content-to-actions gap matches
```

**How to check** (screenshot analysis):
1. Measure pixel distances between elements (browser DevTools or design tools)
2. Verify measurements are multiples of 8px
3. Check that similar spacing situations use same token
4. Note any random spacing values (e.g., 13px, 27px)

**Red flags in screenshots:**
```
❌ Random spacing values (13px, 27px, 35px)
❌ Inconsistent gaps between similar elements
❌ Tight spacing in one view, loose in another
❌ No clear visual rhythm (spacing feels arbitrary)
```

##### 3. Visual Balance Assessment

**Weight Distribution Check:**

```
Left-Right Balance:
✅ Heavy elements (buttons, icons) distributed evenly
✅ Negative space balanced on both sides
✅ Toolbar doesn't feel lopsided

Top-Bottom Balance:
✅ Header weight proportional to content
✅ Footer doesn't feel too heavy/light
✅ Vertical content distribution feels centered

Visual Weight Hierarchy:
✅ Primary actions are heaviest (size, color, position)
✅ Secondary actions are lighter
✅ Tertiary actions are lightest
```

**How to check** (screenshot analysis):
1. Squint at screenshot - does one area feel "heavier"?
2. Cover half the screen - does the visible half feel complete?
3. Check if primary button is visually dominant
4. Verify negative space doesn't create awkward "holes"

**Red flags in screenshots:**
```
❌ All buttons on one side (lopsided toolbar)
❌ Huge empty space on one side, cramped on other
❌ Primary and secondary actions same visual weight
❌ Important content buried in visual chaos
```

##### 4. Grid Alignment Verification

**The Invisible Grid:**

```
Desktop (1920x1080):
- Use 12-column grid system
- Gutters: 24px (--space-6)
- Margins: 32px (--space-8)

Component Internal Grid:
- Content aligns to left/right edges
- Text blocks align to baseline grid
- Icons align to pixel grid (no blurry icons)
```

**What to verify:**

```
Layout Grid:
✅ Main content respects grid columns
✅ Sidebars snap to grid boundaries
✅ Modals center on grid (not arbitrary position)

Content Grid:
✅ Form fields align left edges
✅ Button groups form clean rectangles
✅ Card content aligns to card padding

Pixel Grid:
✅ Icons render crisp (no 0.5px positions)
✅ Lines are full pixels thick (not blurry)
✅ Text doesn't sit on sub-pixels
```

**How to check** (screenshot analysis):
1. Overlay a grid in image editor
2. Check if major elements snap to grid lines
3. Verify content blocks align to grid columns
4. Check for blurry icons/text (sub-pixel rendering)

**Red flags in screenshots:**
```
❌ Content blocks randomly positioned
❌ Blurry icons (not on pixel grid)
❌ Text starting at random X positions
❌ Modals centered by eye, not by grid
```

##### 5. Composition Rules Check

**Rule of Thirds:**
```
✅ Important content in upper-third (natural eye position)
✅ Primary actions in lower-right (action area)
✅ Critical info not buried in middle-middle
```

**Visual Hierarchy:**
```
✅ Largest elements are most important
✅ Highest contrast for primary focus
✅ Color draws eye to key actions
✅ Spacing creates clear groupings
```

**Proximity Principle:**
```
✅ Related elements grouped tightly
✅ Unrelated elements separated clearly
✅ Whitespace defines relationships
✅ No orphaned elements (everything belongs)
```

**How to check** (screenshot analysis):
1. What's your eye drawn to first? (Should be primary action)
2. Can you tell what's related without reading? (Proximity grouping)
3. Is there a clear visual path? (Top → middle → action)
4. Do elements feel randomly placed or intentionally composed?

**Red flags in screenshots:**
```
❌ Eye drawn to secondary element first
❌ Can't tell what's grouped with what
❌ No clear visual path (chaos)
❌ Important content hidden in corner
❌ Random element placement (no composition)
```

#### Composition Audit Execution

**Step-by-step process:**

**1. Alignment Grid Overlay** (20 min)
```bash
# For each screenshot:
1. Open in image editor (Photoshop, Figma, etc.)
2. Create vertical guides at element edges
3. Create horizontal guides at baselines
4. Check if elements align to guides
5. Document misalignments with annotations
```

**2. Spacing Measurement** (30 min)
```bash
# For each component:
1. Measure gaps between elements (px)
2. Verify multiples of 8px
3. Check consistency across similar components
4. Note violations: "Button gap: 13px (should be 16px)"
```

**3. Visual Weight Map** (20 min)
```bash
# For each view:
1. Identify heaviest visual elements
2. Check left-right balance
3. Verify primary action is dominant
4. Note lopsided layouts
```

**4. Grid Conformance Check** (30 min)
```bash
# For each layout:
1. Overlay 12-column grid
2. Check main sections snap to columns
3. Verify content respects gutters
4. Check modal/dialog centering
```

**5. Composition Analysis** (30 min)
```bash
# For each screenshot:
1. Apply rule of thirds
2. Trace visual hierarchy
3. Check proximity grouping
4. Verify intentional composition vs random placement
```

**Total audit time**: ~2.5 hours for comprehensive composition audit

#### Composition Audit Checklist

Before completing composition audit, verify:

- [ ] Created alignment grids for all major views
- [ ] Measured spacing between all element groups
- [ ] Verified all spacing uses 8px multiples
- [ ] Checked visual balance (left-right, top-bottom)
- [ ] Overlaid grid on layouts to verify conformance
- [ ] Analyzed visual hierarchy (eye path)
- [ ] Verified proximity grouping (related elements close)
- [ ] Checked rule of thirds for key content placement
- [ ] Documented all alignment violations with screenshots
- [ ] Measured icon/button sizes for consistency
- [ ] Verified text baselines align in horizontal layouts
- [ ] Checked for blurry icons (sub-pixel rendering)
- [ ] Noted any orphaned elements (no clear relationship)
- [ ] Created annotated screenshots showing issues
- [ ] Recommended specific spacing/alignment fixes

**Composition Audit Report Template:**

```markdown
## Composition & Alignment Issues

### Alignment Violations
1. **Toolbar Button Misalignment** (Canvas View)
   - Issue: Vertical toolbar buttons have ragged right edge
   - Screenshot: [annotated image]
   - Fix: Align all buttons to same width or right-align

2. **Text Baseline Mismatch** (Settings Modal)
   - Issue: Label and value text on different baselines
   - Screenshot: [annotated image]
   - Fix: Use flexbox with items-baseline

### Spacing Violations
1. **Non-8px Gaps** (Calendar Event)
   - Issue: 13px gap between time and title (should be 16px)
   - Screenshot: [measurement annotation]
   - Fix: Change to --space-4 (16px)

### Visual Balance Issues
1. **Lopsided Toolbar** (Board View)
   - Issue: All action buttons on right, left side empty
   - Screenshot: [weight map overlay]
   - Fix: Distribute buttons or add left-side content

### Grid Conformance Issues
1. **Off-Grid Modal** (Create Task)
   - Issue: Modal centered by eye, not on grid
   - Screenshot: [grid overlay]
   - Fix: Use calc() to center on 12-column grid
```

**Remember**: Good composition is invisible - it just "feels right" without conscious thought!

---

### 9. Storybook Design Decision Workflow

> **PURPOSE**: Use Storybook to create interactive, visual comparisons for design decisions, allowing user to see options side-by-side before implementation.

#### Why Storybook for Design Decisions

**Benefits of Storybook showcase approach:**
- **Visual clarity**: User sees actual rendered examples, not just descriptions
- **Interactive comparison**: Side-by-side options make decision easier
- **No guesswork**: User makes informed choice based on real visuals
- **Preservation**: Design options documented for future reference
- **Fast iteration**: Change examples in real-time during discussion

**When to use this workflow:**
```
✅ Color palette decisions (primary brand color choice)
✅ Component variant selection (button styles, card designs)
✅ Typography scale comparison (font size/weight options)
✅ Layout alternatives (sidebar positions, toolbar layouts)
✅ Theme options (glass morphism intensity, shadow depth)
✅ Animation timing comparison (transition speeds, easing curves)
✅ Icon set selection (visual consistency check)
✅ Spacing scale decisions (8px vs 4px grid)
```

**When NOT to use:**
```
❌ Simple yes/no decisions (use direct communication)
❌ Technical choices invisible to user (internal architecture)
❌ Time-sensitive fixes (create story after if needed)
```

#### Storybook Design Decision Pattern

##### Story Structure for Design Choices

**File organization:**
```
src/stories/design-system/
├── Colors.stories.ts          # Color palette decisions
├── ButtonVariants.stories.ts  # Button style options
├── Typography.stories.ts      # Font scale comparisons
├── Spacing.stories.ts         # Grid system options
└── ThemeIntensity.stories.ts  # Glass effect levels
```

**Story template for design decisions:**
```typescript
import type { Meta, StoryObj } from '@storybook/vue3'

const meta: Meta = {
  title: 'Design System/[Category]/[Decision Name]',
  parameters: {
    layout: 'padded',
    docs: {
      description: {
        component: `
# [Decision Name]

## Context
[Why this decision matters]

## Impact
- Affected components: [list]
- Visual consistency: [description]
- User experience: [how it changes UX]

## Considerations
- **Pro/Con analysis** for each option
- **Current usage** in application
- **Migration effort** if changing from current state
        `
      }
    }
  },
  tags: ['autodocs'],
}

export default meta
type Story = StoryObj<typeof meta>

// Option 1: First alternative
export const Option1: Story = {
  name: '✅ RECOMMENDED: [Option 1 Name]',
  render: () => ({
    template: `
      <div class="space-y-8 p-8 bg-gray-900 text-white min-h-screen">
        <!-- Visual Examples Section -->
        <section>
          <h2 class="text-2xl font-bold mb-4">Visual Examples</h2>

          <!-- Color Swatches / Component Previews -->
          <div class="grid grid-cols-5 gap-4">
            <!-- Example elements using this option -->
          </div>
        </section>

        <!-- Interactive Demo Section -->
        <section>
          <h2 class="text-2xl font-bold mb-4">Interactive Demo</h2>

          <!-- Real component examples with this option applied -->
          <div class="space-y-4">
            <!-- Buttons, cards, modals showing this option -->
          </div>
        </section>

        <!-- Context Section -->
        <section>
          <h2 class="text-2xl font-bold mb-4">Current Usage</h2>

          <!-- Screenshots or descriptions of where this is used now -->
          <div class="grid grid-cols-2 gap-4">
            <!-- Examples from actual app -->
          </div>
        </section>

        <!-- Pros/Cons Section -->
        <section>
          <h2 class="text-2xl font-bold mb-4">Analysis</h2>

          <div class="grid grid-cols-2 gap-8">
            <!-- Pros -->
            <div>
              <h3 class="text-green-400 text-lg font-semibold mb-2">✅ Pros</h3>
              <ul class="space-y-1 text-sm">
                <li>• [Benefit 1]</li>
                <li>• [Benefit 2]</li>
                <li>• [Benefit 3]</li>
              </ul>
            </div>

            <!-- Cons -->
            <div>
              <h3 class="text-red-400 text-lg font-semibold mb-2">❌ Cons</h3>
              <ul class="space-y-1 text-sm">
                <li>• [Drawback 1]</li>
                <li>• [Drawback 2]</li>
              </ul>
            </div>
          </div>
        </section>
      </div>
    `
  })
}

// Option 2: Alternative
export const Option2: Story = {
  name: '🔵 ALTERNATIVE: [Option 2 Name]',
  // Same structure as Option1
}

// Side-by-side comparison
export const Comparison: Story = {
  name: '⚖️ Side-by-Side Comparison',
  render: () => ({
    template: `
      <div class="space-y-8 p-8 bg-gray-900 text-white min-h-screen">
        <h1 class="text-3xl font-bold mb-8">Direct Comparison</h1>

        <div class="grid grid-cols-2 gap-8">
          <!-- Option 1 Column -->
          <div class="space-y-4">
            <h2 class="text-xl font-bold text-center">[Option 1 Name]</h2>
            <!-- Examples with option 1 -->
          </div>

          <!-- Option 2 Column -->
          <div class="space-y-4">
            <h2 class="text-xl font-bold text-center">[Option 2 Name]</h2>
            <!-- Same examples with option 2 -->
          </div>
        </div>
      </div>
    `
  })
}
```

##### Real Example: Color Decision Story

**Successful pattern from TEAL vs BLUE decision:**

```typescript
// src/stories/design-system/Colors.stories.ts
export const TealOption: Story = {
  name: '✅ RECOMMENDED: TEAL (#4ECDC4)',
  render: () => ({
    template: `
      <div class="space-y-8 p-8 bg-gray-900 text-white min-h-screen">
        <!-- Color Swatches -->
        <section>
          <h2>Primary Teal + Shades</h2>
          <div class="flex gap-4">
            <div class="w-24 h-24 rounded" style="background: #4ECDC4"></div>
            <div class="w-24 h-24 rounded" style="background: #3DBDB5"></div>
            <div class="w-24 h-24 rounded" style="background: #2CADA6"></div>
          </div>
        </section>

        <!-- Interactive Button Examples -->
        <section>
          <h2>Button Examples (Hover to Test)</h2>
          <div class="space-x-4">
            <button class="px-6 py-3 rounded-lg" style="background: #4ECDC4">
              Primary Action
            </button>
            <button class="px-6 py-3 rounded-lg border-2"
                    style="border-color: #4ECDC4; color: #4ECDC4">
              Secondary Action
            </button>
          </div>
        </section>

        <!-- Real Toolbar Preview -->
        <section>
          <h2>Canvas Toolbar Preview</h2>
          <!-- Actual toolbar component with TEAL applied -->
        </section>

        <!-- Pros/Cons Analysis -->
        <section>
          <div class="grid grid-cols-2 gap-8">
            <div>
              <h3 class="text-green-400">✅ Pros</h3>
              <ul>
                <li>• Already used in Canvas + Settings (60% coverage)</li>
                <li>• Distinctive, modern, energetic feel</li>
                <li>• Good contrast on dark backgrounds</li>
              </ul>
            </div>
            <div>
              <h3 class="text-red-400">❌ Cons</h3>
              <ul>
                <li>• Would require changing All Tasks view</li>
                <li>• Less "professional" than blue</li>
              </ul>
            </div>
          </div>
        </section>
      </div>
    `
  })
}
```

**What made this effective:**
- ✅ User saw EXACT colors rendered, not just hex codes
- ✅ Interactive examples showed hover states in real-time
- ✅ Side-by-side comparison made decision obvious
- ✅ Pros/cons grounded in actual app usage
- ✅ Current usage stats showed migration effort
- ✅ User could navigate Storybook to compare at their pace

#### Storybook Design Decision Workflow

**Step-by-step process:**

**1. Identify Design Decision** (5 min)
```
During audit, when you find:
- Multiple inconsistent options (TEAL vs BLUE buttons)
- Need to choose between alternatives
- User needs visual comparison to decide

→ Create Storybook decision stories
```

**2. Create Comparison Stories** (30-60 min)
```bash
# Create story file
touch src/stories/design-system/[DecisionName].stories.ts

# Include:
- 2-3 option stories (Option 1, Option 2, Option 3)
- Side-by-side comparison story
- Real component examples (not mockups)
- Interactive states (hover, active, disabled)
- Pros/cons for each option
- Current usage documentation
- Migration effort notes
```

**3. Run Storybook** (2 min)
```bash
npm run storybook
# Opens at http://localhost:6006

# Verify:
- All stories render correctly
- Interactive examples work (hover, click)
- No console errors
- Visual comparison is clear
```

**4. User Review & Decision** (10-30 min)
```
Direct user to:
Design System → [Category] → [Decision Name]

User reviews:
- Each option story individually
- Side-by-side comparison
- Pros/cons analysis
- Current usage impact

User decides and communicates choice
```

**5. Record Decision** (5 min)
```bash
# Update documentation
docs/decisions/[decision-name].md

# Record:
- Chosen option
- Rationale
- Date decided
- Affected components
- Migration tasks

# Update todo list
TodoWrite: "USER DECISION: [Choice] - implement across system"
```

**6. Implement Decision** (varies)
```bash
# Use chosen option as source of truth
# Update design tokens
# Migrate affected components
# Verify with Playwright visual tests
# Keep Storybook stories as documentation
```

#### Design Decision Documentation Template

**After user makes decision, create documentation:**

```markdown
# Design Decision: [Name]

**Date:** [Date]
**Status:** ✅ DECIDED
**Decision:** [Chosen option]

## Context

[Why this decision was needed]

## Options Considered

### Option 1: [Name]
- **Storybook:** Design System/[Category]/[Name] - [Option 1 Story]
- **Pros:** [list]
- **Cons:** [list]

### Option 2: [Name]
- **Storybook:** Design System/[Category]/[Name] - [Option 2 Story]
- **Pros:** [list]
- **Cons:** [list]

## Decision

**Chosen:** [Option name]

**Rationale:**
- [Primary reason]
- [Secondary reason]
- [Additional factors]

## Implementation

**Affected Components:**
- [Component 1] - [Change needed]
- [Component 2] - [Change needed]

**Design Tokens to Update:**
```css
--brand-primary: [value];
--accent-color: [value];
```

**Migration Checklist:**
- [ ] Update design tokens
- [ ] Migrate Canvas components
- [ ] Migrate modals
- [ ] Update Storybook examples
- [ ] Verify with Playwright
- [ ] Document in CHANGELOG

## Verification

**Storybook:** Design System/[Category]/[Final Implementation]
**Playwright Tests:** tests/design-system/[test-name].spec.ts
**Screenshots:** docs/screenshots/[before-after].png

## Related Decisions

- [Link to related decision doc]
```

#### Storybook Organization for Design Decisions

**Recommended structure:**

```
src/stories/design-system/
├── Colors.stories.ts              # Brand color decisions
├── ButtonStyles.stories.ts        # Button variant choices
├── CardBackgrounds.stories.ts     # Card/modal bg options
├── Typography.stories.ts          # Font scale decisions
├── Spacing.stories.ts             # Grid system (8px vs 4px)
├── GlassMorphism.stories.ts       # Glass effect intensity
├── Shadows.stories.ts             # Elevation scale
├── Animations.stories.ts          # Timing/easing options
└── IconStyles.stories.ts          # Icon treatment
```

**Navigation path for users:**
```
Storybook Homepage
└── Design System (category)
    ├── Colors
    │   └── Brand Primary Decision ← User goes here
    │       ├── ✅ RECOMMENDED: TEAL
    │       ├── 🔵 ALTERNATIVE: BLUE
    │       └── ⚖️ Side-by-Side Comparison
    ├── Button Styles
    │   └── Primary Button Style Decision
    │       ├── Option 1: Rounded Solid
    │       ├── Option 2: Square Outline
    │       └── ⚖️ Side-by-Side Comparison
    └── ...
```

#### Checklist for Design Decision Stories

Before presenting to user, verify:

- [ ] Created dedicated story file in `src/stories/design-system/`
- [ ] Minimum 2 option stories + 1 comparison story
- [ ] Each story includes visual examples (colors, components, etc.)
- [ ] Interactive demos work (hover, click, animations)
- [ ] Pros/cons analysis for each option
- [ ] Current usage documented with examples
- [ ] Migration effort estimated
- [ ] Side-by-side comparison shows SAME examples
- [ ] Storybook runs without errors
- [ ] Navigation path is clear (Design System → Category → Decision)
- [ ] Story descriptions explain context and impact
- [ ] Real components used (not mockups)
- [ ] All interactive states shown (default, hover, active, disabled)
- [ ] User can make informed decision from stories alone

#### Success Metrics for Storybook Decisions

**Good design decision story achieves:**
- ✅ User can decide WITHOUT asking questions
- ✅ Visual comparison makes choice obvious
- ✅ Pros/cons are grounded in actual usage
- ✅ Migration effort is transparent
- ✅ Decision happens in < 30 minutes
- ✅ User feels confident in choice
- ✅ Stories serve as documentation afterward

**Red flags:**
- ❌ User asks "what will this look like?" (examples unclear)
- ❌ User can't tell the difference (comparison not clear enough)
- ❌ User needs to see "in actual app" (stories not realistic)
- ❌ Decision takes hours (too much analysis paralysis)
- ❌ User regrets decision later (implications not shown)

#### Real-World Example: TEAL vs BLUE Success

**What worked:**
1. **Fast creation**: 30 minutes to create all 3 stories
2. **Clear visuals**: User saw exact colors rendered
3. **Interactive**: Hover states worked in Storybook
4. **Realistic**: Used actual button/toolbar components
5. **Analytical**: Showed current usage (Canvas=TEAL, Tasks=BLUE)
6. **Decisive**: User chose TEAL in < 5 minutes
7. **Documented**: Stories remain as reference

**User feedback:**
> "this is a great way of showcasing design options or issues"

**Impact:**
- Eliminated back-and-forth about color descriptions
- User made informed decision based on visuals
- No regrets or change requests
- Pattern established for future decisions

#### When to Update This Workflow

**Add to this section when:**
- Discover better story structure patterns
- Find more effective comparison layouts
- Identify additional use cases
- Improve user decision speed
- Create reusable story templates
- Develop automated story generation

**Remember**: Storybook design decisions eliminate guesswork and make user the designer!

---

## Audit Execution Workflow

### Step 1: Automated Scanning
```bash
# Run all automated checks
npm run validate:all

# Scan for hardcoded colors
grep -rn "color: #\|background: #\|border.*#" src/components --include="*.vue"

# Scan for hardcoded spacing
grep -rn "padding: [0-9]\|margin: [0-9]" src/components --include="*.vue"

# Find missing ARIA labels on buttons
grep -rn "<button" src/components --include="*.vue" | grep -v "aria-label"

# Check for outline: none violations
grep -rn "outline: none" src/components --include="*.vue"
```

### Step 2: Manual Component Review
For each component category (base, canvas, kanban):
1. Select 3-5 representative components
2. Review against all checklist categories
3. Document patterns (both good and bad)
4. Identify inconsistencies
5. Create fix recommendations

### Step 3: Accessibility Testing
```bash
# Install and run axe-core for automated a11y testing
npm install --save-dev @axe-core/vue

# Test with keyboard navigation
# - Tab through all interactive elements
# - Verify focus indicators visible
# - Test Escape key for modals
# - Arrow keys for dropdowns/menus

# Test with screen reader (NVDA/JAWS/VoiceOver)
# - All content announced correctly
# - Labels make sense without visual context
```

### Step 4: Visual Hierarchy Review
Open each main view and ask:
- What is the most important element? Does it look most important?
- Is the reading order logical?
- Are related items visually grouped?
- Is there enough whitespace to prevent overwhelm?
- Do headings establish clear hierarchy?

### Step 5: Interaction Feedback Audit
Test every interactive element:
- Hover state provides clear feedback
- Click/press state is obvious
- Loading states show progress
- Error states are clear and actionable
- Success feedback confirms actions

## Report Format

```markdown
# UI/UX Consistency Audit Report
**Date:** [Date]
**Auditor:** Claude Code
**Scope:** [Components/Views audited]

## Executive Summary
[Brief overview of findings and overall consistency score]

## Metrics
- **Design Token Compliance:** X% (Y/Z checks passing)
- **Accessibility Score:** X/100 (WCAG 2.1 Level AA)
- **Component Pattern Consistency:** X%
- **Interaction Pattern Compliance:** X%

---

## ✅ Areas of Excellence
1. [Specific areas where consistency is excellent]
2. [Patterns that work well and should be maintained]
3. [Accessibility wins]

---

## ⚠️ Issues Found

### 🔴 Critical Issues (Must Fix Immediately)
**Issue #1: [Description]**
- **Impact:** [User impact]
- **Location:** src/components/[path]:[line]
- **Current:** [Code showing problem]
- **Fix:**
  ```vue
  [Code showing solution]
  ```

### 🟠 High Priority Issues (Fix Soon)
[Same format as critical]

### 🟡 Medium Priority Issues (Improvement Opportunities)
[Same format as critical]

### 🔵 Low Priority Issues (Nice to Have)
[Same format as critical]

---

## 📋 Recommended Actions

### Immediate (This Week)
1. [Specific actionable task]
2. [Specific actionable task]

### Short Term (This Month)
1. [Specific actionable task]
2. [Specific actionable task]

### Long Term (This Quarter)
1. [Specific actionable task]
2. [Specific actionable task]

---

## 📊 Detailed Findings by Category

### Visual Consistency
- Color Usage: [Score] - [Summary]
- Spacing: [Score] - [Summary]
- Typography: [Score] - [Summary]
- Border Radius: [Score] - [Summary]
- Shadows: [Score] - [Summary]

### Component Design
- Structure: [Score] - [Summary]
- Naming: [Score] - [Summary]
- Props: [Score] - [Summary]

### Interaction Patterns
- Hover States: [Score] - [Summary]
- Focus States: [Score] - [Summary]
- Loading States: [Score] - [Summary]

### Accessibility
- Semantic HTML: [Score] - [Summary]
- ARIA: [Score] - [Summary]
- Color Contrast: [Score] - [Summary]
- Keyboard Nav: [Score] - [Summary]

### Design System
- Token Usage: [Score] - [Summary]
- Tailwind Consistency: [Score] - [Summary]
- Glass Effects: [Score] - [Summary]

---

## 🎯 Next Audit
**Scheduled:** [Date]
**Focus Areas:** [Areas needing follow-up]
```

## Related Skills

- **dev-vue** - For implementing component fixes
- **dev-optimize-performance** - For animation performance issues
- **comprehensive-debugging** - For troubleshooting state/reactivity issues
- **dev-fix-keyboard** - For keyboard navigation fixes

## Usage Example

When you activate this skill by saying **"audit UI consistency"** or **"run the skill on everything"**, I will:

### Phase 1: Code Analysis
1. Run automated scans for design token violations
2. Check component patterns and TypeScript usage
3. Scan for accessibility issues (ARIA, keyboard nav)
4. Detect hardcoded values (colors, spacing, typography)

### Phase 2: Visual Analysis (CRITICAL!)
1. **Locate screenshots** in `docs/debug/` or request new ones
2. **Catalog style variants**:
   - Count all button styles (target: 1-3 variants max)
   - Document card/modal backgrounds (target: 1 unified style)
   - List all colors used (target: 1 primary color + semantic)
3. **Create cross-view comparison matrix**
4. **Identify theme breaks** (light components in dark theme)
5. **Document "orphaned" styles** (used once, nowhere else)

### Phase 3: Comprehensive Report
Generate detailed report with:
- **Visual evidence**: Screenshot references for each issue
- **Side-by-side comparisons**: Before/after examples
- **Severity classification**: Critical → Low priority
- **Specific fixes**: Exact code changes with design token usage
- **Metrics**: Design token compliance %, accessibility score
- **Recommended actions**: Prioritized by impact

### What Gets Audited:

**Code Level:**
- Design token compliance (colors, spacing, typography, shadows)
- Component patterns (props, emits, naming)
- Accessibility (WCAG 2.1, ARIA, keyboard)
- Interaction states (hover, focus, active)

**Visual Level:**
- Button style variants across all views
- Card/modal background consistency
- Color palette usage and consistency
- Cross-view visual continuity
- Theme consistency (no light in dark)
- Typography hierarchy adherence
- Visual weight and hierarchy

**The Difference:**
- ❌ Code audit alone: "35 hardcoded colors found"
- ✅ Visual audit: "7 different button styles make app feel inconsistent - here's the visual proof [screenshots] and exact fixes"

---

**Last Updated:** October 26, 2025
**Skill Version:** 1.2.0 (Added Storybook design decision workflow)
**Project:** Pomo-Flow

## Version History
- **v1.2.0** (2025-10-26): Added Section 9 - Storybook Design Decision Workflow for interactive visual comparisons
- **v1.1.0** (2025-10-23): Added Section 7 - Visual Inconsistency Audit with screenshot analysis
- **v1.0.0** (2025-10-23): Initial skill creation with code-level auditing
