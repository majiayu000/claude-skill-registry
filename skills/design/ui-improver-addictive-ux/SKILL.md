# UI Improver: Addictive UX & Visual Consistency Skill

**Version**: 2.0.0
**Agent**: ui-improver
**Last Updated**: 2025-10-26

---

## 📋 Table of Contents

1. [Skill Purpose](#skill-purpose)
2. [Phase 0: Setup & Style Guide Review](#phase-0-setup--style-guide-review)
3. [Phase 1: Deep Visual Analysis](#phase-1-deep-visual-analysis)
4. [Phase 2: Research-Driven Planning](#phase-2-research-driven-planning)
5. [Phase 3: Iterative Implementation](#phase-3-iterative-implementation)
6. [Phase 4: Comprehensive Verification](#phase-4-comprehensive-verification)
7. [Embedded STYLE_GUIDE](#embedded-style_guide)
8. [Addictive UX Patterns Library](#addictive-ux-patterns-library)
9. [MCP Integration Workflows](#mcp-integration-workflows)
10. [Success Metrics](#success-metrics)

---

## Skill Purpose

This skill provides a **complete 4-phase workflow** for creating **addictive, delightful user experiences** while ensuring **100% STYLE_GUIDE compliance**. You will transform functional interfaces into experiences that users **LOVE** to interact with through:

- **Visual Consistency**: Every component follows the established style guide
- **Addictive Patterns**: Gamification, micro-interactions, feedback loops
- **Satisfying Animations**: 60fps spring physics with delightful timing
- **Accessibility**: WCAG 2.1 AA compliance mandatory
- **Screenshot Verification**: Chrome DevTools MCP for iterative visual confirmation
- **Component Discovery**: shadcn MCP for optimal component patterns

---

## Phase 0: Setup & Style Guide Review

**Objective**: Load the style guide into memory and understand design constraints.

### 0.1 Read Style Guide (MANDATORY)

The complete STYLE_GUIDE is embedded in this skill (see section below). Before ANY visual work:

1. **Review Color Palette**: 5-color brand progression (black → navy → purple → light purple → lavender)
2. **Review Typography**: Fluid type scale, font weights, line heights
3. **Review Spacing**: Spacing scale (4px to 96px)
4. **Review Components**: Button styles, card patterns, input states
5. **Review Animations**: Duration principles, easing curves, keyframes
6. **Review Accessibility**: WCAG 2.1 AA contrast requirements, ARIA patterns
7. **Review Responsive**: Breakpoints, mobile-first approach, touch targets
8. **Review Dark Mode**: Semantic color mapping, elevation strategy

### 0.2 Identify Current Request Context

**Questions to answer**:
- What page/component needs improvement?
- Is there a design reference (screenshot, mockup)?
- What specific visual issues were reported?
- What is the current state vs. desired state?
- Are there accessibility concerns?

### 0.3 Baseline Screenshot (Chrome DevTools MCP)

**MANDATORY**: Take baseline screenshots BEFORE any changes.

```typescript
// Take screenshot of current state (light mode)
await chromeDevTools.navigate_page({
  url: 'http://localhost:3000/page-to-improve'
})

await chromeDevTools.take_screenshot({
  path: '.claude/skills/ui-improver-addictive-ux/assets/before-light.png',
  fullPage: true
})

// Switch to dark mode
await chromeDevTools.evaluate_script({
  script: 'document.documentElement.classList.add("dark")'
})

await chromeDevTools.take_screenshot({
  path: '.claude/skills/ui-improver-addictive-ux/assets/before-dark.png',
  fullPage: true
})
```

**Checkpoint**: ✅ STYLE_GUIDE reviewed, baseline screenshots taken

---

## Phase 1: Deep Visual Analysis

**Objective**: Systematically analyze visual inconsistencies and improvement opportunities.

### 1.1 Component Audit

**Read target page/component** and identify:

1. **Color Violations**:
   - [ ] Hardcoded colors outside palette
   - [ ] Insufficient contrast (use WebAIM contrast checker)
   - [ ] Missing dark mode styles
   - [ ] Non-semantic color usage

2. **Typography Issues**:
   - [ ] Font sizes outside type scale
   - [ ] Incorrect font weights
   - [ ] Poor line heights for readability
   - [ ] Inconsistent heading hierarchy

3. **Spacing Inconsistencies**:
   - [ ] Arbitrary spacing values (not from scale)
   - [ ] Uneven padding/margins
   - [ ] Inconsistent component spacing
   - [ ] Poor visual rhythm

4. **Component Violations**:
   - [ ] Non-shadcn/Aceternity components
   - [ ] Missing hover/focus states
   - [ ] Inconsistent button styles
   - [ ] Improper card elevation

5. **Animation Gaps**:
   - [ ] Missing micro-interactions
   - [ ] Jarring transitions (wrong duration/easing)
   - [ ] Layout shifts on interaction
   - [ ] No loading states

6. **Accessibility Violations**:
   - [ ] Missing ARIA labels
   - [ ] No keyboard navigation
   - [ ] Insufficient focus indicators
   - [ ] Poor screen reader support

### 1.2 User Experience Analysis

**Identify addictive UX opportunities**:

1. **Feedback Loops**:
   - Are user actions acknowledged immediately?
   - Do interactions feel responsive and satisfying?
   - Are loading states clear and non-blocking?

2. **Progressive Disclosure**:
   - Is information revealed at the right time?
   - Are advanced features hidden until needed?
   - Does the UI guide users naturally?

3. **Gamification Potential**:
   - Can we add progress indicators?
   - Are achievements/milestones celebrated?
   - Can we use points/badges/streaks?

4. **Micro-Interactions**:
   - Button press feedback (spring animation)
   - Hover lift effects on cards
   - Input focus animations
   - Success/error state transitions

### 1.3 Context7 Research (MANDATORY)

**Consult Context7 for latest patterns** based on findings:

#### For Animation Issues:
```typescript
await context7.get_library_docs({
  context7CompatibleLibraryID: "/framer/motion",
  topic: "spring animations stagger variants gestures useAnimation",
  tokens: 4000
})
```

#### For Tailwind Patterns:
```typescript
await context7.get_library_docs({
  context7CompatibleLibraryID: "/tailwindlabs/tailwindcss",
  topic: "dark mode animations arbitrary values responsive design",
  tokens: 3000
})
```

#### For React Patterns:
```typescript
await context7.get_library_docs({
  context7CompatibleLibraryID: "/facebook/react",
  topic: "useCallback useMemo performance optimization re-renders",
  tokens: 2000
})
```

#### For Accessibility:
```typescript
await context7.get_library_docs({
  context7CompatibleLibraryID: "/w3c/wcag",
  topic: "ARIA labels keyboard navigation focus management color contrast",
  tokens: 2000
})
```

**Checkpoint**: ✅ Complete audit documented, Context7 research completed

---

## Phase 2: Research-Driven Planning

**Objective**: Create improvement plan with shadcn MCP integration and addictive UX patterns.

### 2.1 shadcn Component Discovery

**Search shadcn for optimal components**:

```bash
# Example: Looking for button variants
npx shadcn@latest add button

# Example: Looking for form components
npx shadcn@latest add form input label

# Example: Looking for feedback components
npx shadcn@latest add toast alert-dialog progress
```

**Document**:
- Which shadcn/Aceternity components to use
- Which components need custom styling (following STYLE_GUIDE)
- Which components need animation enhancements

### 2.2 Animation Strategy

**Plan animations using Context7 patterns**:

1. **Micro-Interactions** (200ms):
   - Button press: `whileTap={{ scale: 0.95 }}`
   - Hover lift: `hover:-translate-y-1`
   - Focus ring: `focus:ring-2 focus:ring-ring`

2. **Layout Changes** (300ms):
   - Card expansion
   - Sidebar slide-in
   - Modal fade-in + scale

3. **Page Transitions** (500ms):
   - Route changes
   - View switching
   - Progressive loading

4. **Spring Physics** (for satisfying feel):
   ```typescript
   transition={{
     type: "spring",
     stiffness: 400,  // Higher = snappier
     damping: 17      // Lower = more bounce
   }}
   ```

### 2.3 Addictive UX Pattern Selection

**Choose from addictive patterns library** (see section below):

- [ ] **Progress Indicators**: Show completion status, encourage continuation
- [ ] **Instant Feedback**: Haptic-like visual feedback on every interaction
- [ ] **Celebration Moments**: Confetti/animations on task completion
- [ ] **Streaks & Consistency**: Show consecutive days/actions
- [ ] **Gamification**: Points, levels, badges, leaderboards
- [ ] **Personalization**: Remember user preferences, adapt UI
- [ ] **Social Proof**: Show other users' activity (if applicable)
- [ ] **Scarcity/Urgency**: Limited-time offers, countdown timers
- [ ] **Variable Rewards**: Surprise delights, random positive feedback

### 2.4 Accessibility Compliance Plan

**Ensure WCAG 2.1 AA** for all improvements:

1. **Color Contrast**:
   - Normal text: 4.5:1 minimum
   - Large text: 3:1 minimum
   - UI components: 3:1 minimum

2. **Keyboard Navigation**:
   - Tab order logical
   - Enter/Space activate buttons
   - Escape closes modals
   - Arrow keys for lists/menus

3. **ARIA Labels**:
   - `aria-label` for icon-only buttons
   - `aria-describedby` for error messages
   - `aria-live` for dynamic content
   - `aria-busy` for loading states

4. **Focus Management**:
   - Visible focus indicators (2px ring)
   - Focus trap in modals
   - Focus restoration on close
   - Skip to content link

**Checkpoint**: ✅ Complete plan documented with component list, animation strategy, UX patterns, accessibility checklist

---

## Phase 3: Iterative Implementation

**Objective**: Implement improvements iteratively with screenshot verification at each step.

### 3.1 Implementation Order (STRICT)

**NEVER implement all changes at once**. Follow this order:

1. **Colors & Typography** (foundation)
2. **Spacing & Layout** (structure)
3. **Component Consistency** (shadcn/STYLE_GUIDE)
4. **Accessibility** (ARIA, keyboard nav)
5. **Micro-Interactions** (hover, focus, active states)
6. **Animations** (transitions, spring physics)
7. **Addictive UX Patterns** (gamification, feedback loops)
8. **Dark Mode Optimization** (final polish)

### 3.2 Iteration Pattern

**For EACH improvement step**:

1. **Implement Change** (Edit tool)
2. **Take Screenshot** (Chrome DevTools MCP)
3. **Compare with Before** (visual diff)
4. **Verify STYLE_GUIDE Compliance** (checklist)
5. **Test Accessibility** (keyboard nav, screen reader)
6. **Approve or Rollback** (keep only improvements)

**Example Iteration**:

```typescript
// Step 1: Fix button colors
// BEFORE: <Button className="bg-blue-500">Click</Button>
// AFTER: <Button className="bg-primary text-primary-foreground hover:bg-primary/90">Click</Button>

// Step 2: Take screenshot
await chromeDevTools.take_screenshot({
  path: '.claude/skills/ui-improver-addictive-ux/assets/iteration-01-buttons.png'
})

// Step 3: Compare (visual inspection)
// Step 4: Verify STYLE_GUIDE
// - ✅ Uses semantic color (--primary)
// - ✅ Has hover state (hover:bg-primary/90)
// - ✅ Correct text color (text-primary-foreground)

// Step 5: Test accessibility
// - ✅ Tab navigable
// - ✅ Enter/Space activate
// - ✅ Focus ring visible

// Step 6: APPROVED → Continue to next iteration
```

### 3.3 Animation Implementation (Context7 Validated)

**Use patterns from Context7 research**:

#### Tailwind Animations (Simple):
```tsx
// Fade in on mount
<div className="animate-fade-in">Content</div>

// Hover lift
<Card className="transition-all duration-300 hover:-translate-y-1 hover:shadow-lg">
  Card content
</Card>

// Button press
<Button className="active:scale-95 transition-transform duration-100">
  Press Me
</Button>
```

#### Framer Motion (Complex):
```tsx
import { motion } from 'framer-motion'

// Spring button (ADDICTIVE feel)
<motion.button
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
  transition={{
    type: "spring",
    stiffness: 400,
    damping: 17
  }}
  className="bg-primary text-primary-foreground px-4 py-2 rounded-md"
>
  Satisfying Click
</motion.button>

// Staggered list
<motion.ul
  initial="hidden"
  animate="visible"
  variants={{
    visible: {
      transition: { staggerChildren: 0.05 }
    }
  }}
>
  {items.map(item => (
    <motion.li
      key={item.id}
      variants={{
        hidden: { opacity: 0, x: -20 },
        visible: { opacity: 1, x: 0 }
      }}
    >
      {item.content}
    </motion.li>
  ))}
</motion.ul>

// Page transition
<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  transition={{ duration: 0.3, ease: "easeInOut" }}
>
  Page content
</motion.div>
```

### 3.4 Addictive UX Implementation

**Implement selected patterns** (see Addictive UX Patterns Library below):

#### Example: Progress Indicator
```tsx
import { Progress } from '@/components/ui/progress'
import { motion } from 'framer-motion'

export function TaskProgress({ completed, total }: { completed: number; total: number }) {
  const percentage = (completed / total) * 100

  return (
    <div className="space-y-2">
      <div className="flex justify-between text-sm">
        <span className="text-muted-foreground">Progress</span>
        <motion.span
          key={percentage}
          initial={{ scale: 1.5, color: 'hsl(var(--primary))' }}
          animate={{ scale: 1, color: 'hsl(var(--muted-foreground))' }}
          className="font-semibold"
        >
          {completed}/{total}
        </motion.span>
      </div>
      <Progress value={percentage} className="h-2" />

      {percentage === 100 && (
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="text-sm text-primary font-medium flex items-center gap-2"
        >
          🎉 All done!
        </motion.div>
      )}
    </div>
  )
}
```

#### Example: Instant Feedback
```tsx
import { Button } from '@/components/ui/button'
import { motion } from 'framer-motion'
import { Check } from 'lucide-react'
import { useState } from 'react'

export function FeedbackButton() {
  const [clicked, setClicked] = useState(false)

  return (
    <motion.div whileTap={{ scale: 0.95 }}>
      <Button
        onClick={() => {
          setClicked(true)
          setTimeout(() => setClicked(false), 2000)
        }}
        className="relative"
      >
        {clicked ? (
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            className="flex items-center gap-2"
          >
            <Check className="h-4 w-4" />
            Saved!
          </motion.div>
        ) : (
          'Save Changes'
        )}
      </Button>
    </motion.div>
  )
}
```

### 3.5 Dark Mode Verification

**For EACH iteration, verify dark mode**:

```typescript
// Switch to dark mode
await chromeDevTools.evaluate_script({
  script: 'document.documentElement.classList.add("dark")'
})

await chromeDevTools.take_screenshot({
  path: '.claude/skills/ui-improver-addictive-ux/assets/iteration-01-dark.png'
})
```

**Dark mode checklist**:
- [ ] All text readable (sufficient contrast)
- [ ] Semantic colors adapt correctly
- [ ] Shadows visible (lighter shadows in dark)
- [ ] Focus indicators visible
- [ ] Images/logos have dark variants

**Checkpoint**: ✅ All improvements implemented iteratively with screenshot verification

---

## Phase 4: Comprehensive Verification

**Objective**: Final validation across all dimensions before delivery.

### 4.1 STYLE_GUIDE Compliance Audit

**Run through complete checklist** (from STYLE_GUIDE section):

#### Visual Consistency
- [ ] Uses only colors from defined palette
- [ ] Follows spacing scale (no arbitrary values)
- [ ] Matches typography scale
- [ ] Has consistent border radius (0.5rem default)
- [ ] Has appropriate shadows/elevation

#### Interactivity
- [ ] Has visible hover state (on pointer devices)
- [ ] Has visible focus state (keyboard navigation)
- [ ] Has active/pressed state
- [ ] Has disabled state (if applicable)
- [ ] Has loading state (if applicable)

#### Accessibility
- [ ] Has proper ARIA labels
- [ ] Has sufficient color contrast (4.5:1 minimum)
- [ ] Is keyboard navigable
- [ ] Has focus trap (if modal/dialog)
- [ ] Screen reader compatible

#### Responsiveness
- [ ] Works on mobile (320px+)
- [ ] Works on tablet (768px+)
- [ ] Works on desktop (1024px+)
- [ ] Touch targets are 44px minimum
- [ ] Text is readable at all sizes

#### Dark Mode
- [ ] Looks good in light mode
- [ ] Looks good in dark mode
- [ ] Images have appropriate versions
- [ ] Maintains semantic meaning

#### Performance
- [ ] Uses GPU-accelerated animations
- [ ] Images are optimized
- [ ] No layout shift on load
- [ ] Smooth 60fps animations

### 4.2 Accessibility Testing (MANDATORY)

**Keyboard Navigation Test**:
1. Tab through all interactive elements
2. Verify logical tab order
3. Ensure Enter/Space activate buttons
4. Escape closes modals/dropdowns
5. Arrow keys work for lists/menus

**Screen Reader Test** (if available):
1. Navigate with NVDA/JAWS/VoiceOver
2. Verify all content is announced
3. Verify form labels are associated
4. Verify error messages are announced
5. Verify dynamic content is announced (aria-live)

**Color Contrast Test**:
```typescript
// Use WebAIM Contrast Checker or browser DevTools
// Verify all text meets 4.5:1 ratio
// Verify UI components meet 3:1 ratio
```

### 4.3 Performance Verification

**Chrome DevTools Performance Tab**:
```typescript
// Record interaction performance
await chromeDevTools.evaluate_script({
  script: `
    performance.mark('interaction-start');
    // Trigger interaction (button click, etc.)
    performance.mark('interaction-end');
    performance.measure('interaction', 'interaction-start', 'interaction-end');
  `
})
```

**Verify**:
- [ ] Animations run at 60fps
- [ ] No layout thrashing
- [ ] No excessive repaints
- [ ] Smooth scrolling
- [ ] Fast interaction response (<100ms)

### 4.4 Final Screenshot Gallery

**Take comprehensive screenshots** for documentation:

```bash
# Light mode - Desktop
.claude/skills/ui-improver-addictive-ux/assets/final-light-desktop.png

# Dark mode - Desktop
.claude/skills/ui-improver-addictive-ux/assets/final-dark-desktop.png

# Light mode - Mobile
.claude/skills/ui-improver-addictive-ux/assets/final-light-mobile.png

# Dark mode - Mobile
.claude/skills/ui-improver-addictive-ux/assets/final-dark-mobile.png

# Hover states
.claude/skills/ui-improver-addictive-ux/assets/final-hover-states.png

# Focus states
.claude/skills/ui-improver-addictive-ux/assets/final-focus-states.png
```

### 4.5 Documentation

**Create improvement report**:

```markdown
# UI Improvement Report

## Page/Component
[Name and path]

## Before/After Comparison
![Before Light](.claude/skills/ui-improver-addictive-ux/assets/before-light.png)
![After Light](.claude/skills/ui-improver-addictive-ux/assets/final-light-desktop.png)

## Changes Made

### 1. Color & Typography
- Fixed non-semantic colors (before: `bg-blue-500`, after: `bg-primary`)
- Corrected font sizes to match type scale
- Improved heading hierarchy

### 2. Spacing & Layout
- Applied spacing scale consistently
- Fixed responsive breakpoints
- Improved touch targets (44px minimum)

### 3. Animations Added
- Button spring animation (stiffness: 400, damping: 17)
- Card hover lift effect (translate-y: -4px, duration: 300ms)
- Staggered list entrance (50ms delay per item)

### 4. Addictive UX Patterns
- Progress indicator with celebration on completion
- Instant feedback on button clicks
- Streak counter for consecutive days

### 5. Accessibility Improvements
- Added ARIA labels to icon buttons
- Improved keyboard navigation order
- Enhanced focus indicators (2px ring)
- Fixed color contrast (all text now >4.5:1)

## STYLE_GUIDE Compliance
✅ All checklist items passed

## Accessibility Audit
✅ WCAG 2.1 AA compliant
✅ Keyboard navigable
✅ Screen reader compatible

## Performance
✅ 60fps animations
✅ No layout shift
✅ <100ms interaction response

## Dark Mode
✅ Verified in both modes
✅ Semantic colors adapt correctly
✅ Sufficient contrast maintained
```

**Checkpoint**: ✅ All verification complete, documentation created

---

## Embedded STYLE_GUIDE

**Complete embedded copy for reference during improvements**:

### Design Philosophy

#### Core Principles
1. **Consistency Over Creativity**: Uniform patterns across the entire application
2. **Subtle Satisfaction**: Micro-interactions and animations that delight without overwhelming
3. **Accessibility First**: WCAG 2.1 AA compliance is mandatory, not optional
4. **Performance Matters**: Animations should be 60fps, prefer CSS transforms over layout changes
5. **Progressive Enhancement**: Core functionality works without JavaScript, enhanced with it

#### Design Values
- **Clarity**: Information hierarchy is obvious
- **Efficiency**: Users accomplish tasks quickly
- **Delight**: Subtle animations make interactions satisfying
- **Trust**: Professional appearance builds user confidence

### Color Palette

#### Brand Colors (5-Color Progression)
```css
:root {
  --color-brand-1: 0 0% 0%;        /* #000000 - Pure black */
  --color-brand-2: 230 38% 25%;    /* #1f2546 - Deep navy blue */
  --color-brand-3: 235 33% 43%;    /* #4c5393 - Medium purple */
  --color-brand-4: 236 76% 72%;    /* #8289eb - Light purple */
  --color-brand-5: 236 100% 88%;   /* #c1c5ff - Pale lavender */
}
```

#### Light Mode Semantic Mapping
```css
:root {
  --background: 0 0% 100%;                    /* White */
  --foreground: 230 38% 25%;                  /* Brand-2 */
  --primary: 235 33% 43%;                     /* Brand-3 */
  --primary-foreground: 0 0% 100%;            /* White */
  --secondary: 236 100% 96%;                  /* Very light lavender */
  --secondary-foreground: 235 33% 43%;        /* Brand-3 */
  --muted: 236 100% 96%;                      /* Light lavender */
  --muted-foreground: 235 20% 60%;            /* Muted purple */
  --accent: 236 76% 72%;                      /* Brand-4 */
  --accent-foreground: 230 38% 25%;           /* Brand-2 */
  --border: 236 50% 90%;                      /* Subtle lavender */
  --ring: 235 33% 43%;                        /* Brand-3 */
  --destructive: 0 84% 60%;                   /* Red */
  --destructive-foreground: 0 0% 100%;        /* White */
}
```

#### Dark Mode Semantic Mapping
```css
.dark {
  --background: 230 38% 8%;                   /* Very dark navy */
  --foreground: 236 100% 96%;                 /* Light lavender */
  --primary: 236 76% 72%;                     /* Brand-4 (brighter) */
  --primary-foreground: 230 38% 10%;          /* Dark */
  --card: 230 38% 12%;                        /* Elevated surface */
  --border: 230 38% 20%;                      /* Subtle border */
  --ring: 236 76% 72%;                        /* Brand-4 */
}
```

#### Color Usage Guidelines
- **Primary (Brand-3)**: Main CTAs, active states, primary navigation
- **Brand-4**: Hover states, secondary CTAs, accents
- **Brand-5**: Subtle backgrounds, disabled states (light mode)
- **Brand-2**: Text color in light mode, card backgrounds in dark mode
- **DON'T**: Use Brand-1 for large surfaces, use Brand-5 for text, create new color variations

### Typography

#### Font Stack
```css
--font-sans: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
--font-mono: "Fira Code", "Cascadia Code", Consolas, Monaco, monospace;
```

#### Type Scale (Fluid)
```css
--text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);    /* 12-14px */
--text-sm: clamp(0.875rem, 0.85rem + 0.3vw, 1rem);       /* 14-16px */
--text-base: clamp(1rem, 0.95rem + 0.35vw, 1.125rem);    /* 16-18px */
--text-lg: clamp(1.125rem, 1.05rem + 0.4vw, 1.25rem);    /* 18-20px */
--text-xl: clamp(1.25rem, 1.15rem + 0.5vw, 1.5rem);      /* 20-24px */
--text-2xl: clamp(1.5rem, 1.35rem + 0.75vw, 2rem);       /* 24-32px */
--text-3xl: clamp(1.875rem, 1.65rem + 1vw, 2.5rem);      /* 30-40px */
--text-4xl: clamp(2.25rem, 1.95rem + 1.5vw, 3rem);       /* 36-48px */
```

#### Font Weights
```css
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

#### Heading Guidelines
- **H1**: `text-4xl font-bold`, primary color, once per page
- **H2**: `text-3xl font-semibold`, main sections
- **H3**: `text-2xl font-semibold`, subsections
- **H4**: `text-xl font-medium`, card titles

### Spacing Scale
```css
--spacing-1: 0.25rem;   /* 4px */
--spacing-2: 0.5rem;    /* 8px */
--spacing-3: 0.75rem;   /* 12px */
--spacing-4: 1rem;      /* 16px */
--spacing-6: 1.5rem;    /* 24px */
--spacing-8: 2rem;      /* 32px */
--spacing-12: 3rem;     /* 48px */
--spacing-16: 4rem;     /* 64px */
```

### Animation Principles
1. **Duration**: 200ms micro-interactions, 300ms layout changes, 500ms page transitions
2. **Easing**: `ease-in-out` default, `ease-out` entrances, `ease-in` exits
3. **Performance**: Prefer `transform` and `opacity` over layout properties
4. **Subtlety**: Enhance, don't distract

### Accessibility Requirements (WCAG 2.1 AA)
- **Normal text**: 4.5:1 contrast minimum
- **Large text**: 3:1 contrast minimum
- **UI components**: 3:1 contrast minimum
- **Focus indicators**: 2px visible ring
- **Keyboard navigation**: All interactive elements
- **ARIA labels**: Icon buttons, form inputs, dynamic content

### Responsive Breakpoints
```css
--screen-sm: 640px;    /* Mobile landscape */
--screen-md: 768px;    /* Tablets */
--screen-lg: 1024px;   /* Laptops */
--screen-xl: 1280px;   /* Desktops */
--screen-2xl: 1536px;  /* Large desktops */
```

---

## Addictive UX Patterns Library

**Researched patterns from Context7, HIG, and UX best practices**:

### 1. Progress & Achievement

#### Pattern: Progress Bars with Celebration
**Psychology**: Variable rewards + achievement recognition
**Implementation**:
```tsx
<motion.div>
  <Progress value={percentage} />
  {percentage === 100 && (
    <motion.div
      initial={{ scale: 0, rotate: -180 }}
      animate={{ scale: 1, rotate: 0 }}
      transition={{ type: "spring", stiffness: 200 }}
    >
      🎉 Complete!
    </motion.div>
  )}
</motion.div>
```

#### Pattern: Streak Counters
**Psychology**: Loss aversion + consistency bias
**Implementation**:
```tsx
<div className="flex items-center gap-2">
  <Flame className="text-orange-500" />
  <span className="text-2xl font-bold">{streakDays}</span>
  <span className="text-sm text-muted-foreground">day streak</span>
</div>
```

### 2. Instant Feedback

#### Pattern: Spring Button Press
**Psychology**: Haptic feedback simulation
**Implementation**:
```tsx
<motion.button
  whileHover={{ scale: 1.02 }}
  whileTap={{ scale: 0.98 }}
  transition={{
    type: "spring",
    stiffness: 400,
    damping: 17
  }}
>
  Click Me
</motion.button>
```

#### Pattern: Success State Morph
**Psychology**: Immediate positive reinforcement
**Implementation**:
```tsx
const [state, setState] = useState<'idle' | 'loading' | 'success'>('idle')

<Button onClick={handleSave}>
  {state === 'idle' && 'Save'}
  {state === 'loading' && <Loader2 className="animate-spin" />}
  {state === 'success' && (
    <motion.div
      initial={{ scale: 0 }}
      animate={{ scale: 1 }}
      transition={{ type: "spring" }}
    >
      <Check /> Saved!
    </motion.div>
  )}
</Button>
```

### 3. Gamification

#### Pattern: Points & Levels
**Psychology**: Progression mechanics
**Implementation**:
```tsx
<Card>
  <div className="flex items-center justify-between">
    <div>
      <div className="text-sm text-muted-foreground">Level {level}</div>
      <div className="text-2xl font-bold">{points} XP</div>
    </div>
    <Trophy className="h-8 w-8 text-primary" />
  </div>
  <Progress value={(points % 1000) / 10} className="mt-2" />
  <div className="text-xs text-muted-foreground mt-1">
    {1000 - (points % 1000)} XP to Level {level + 1}
  </div>
</Card>
```

#### Pattern: Badge Collection
**Psychology**: Completionism + social proof
**Implementation**:
```tsx
<div className="grid grid-cols-4 gap-2">
  {badges.map(badge => (
    <motion.div
      key={badge.id}
      whileHover={{ scale: 1.1 }}
      className={cn(
        "aspect-square rounded-lg border-2 p-2",
        badge.unlocked ? "border-primary" : "border-muted opacity-50"
      )}
    >
      {badge.icon}
    </motion.div>
  ))}
</div>
```

### 4. Social Proof

#### Pattern: Live Activity Feed
**Psychology**: FOMO + social validation
**Implementation**:
```tsx
<motion.div
  initial={{ opacity: 0, y: -20 }}
  animate={{ opacity: 1, y: 0 }}
  className="text-sm text-muted-foreground"
>
  <Users className="inline h-3 w-3" /> 127 users active now
</motion.div>
```

#### Pattern: Recent Actions
**Psychology**: Activity creates perceived value
**Implementation**:
```tsx
<div className="space-y-2">
  {recentActions.map((action, i) => (
    <motion.div
      key={action.id}
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: i * 0.05 }}
      className="text-sm"
    >
      <span className="font-medium">{action.user}</span>
      <span className="text-muted-foreground"> {action.action}</span>
      <span className="text-xs text-muted-foreground ml-2">{action.time}</span>
    </motion.div>
  ))}
</div>
```

### 5. Personalization

#### Pattern: Adaptive UI
**Psychology**: Perceived intelligence + relevance
**Implementation**:
```tsx
// Remember user preferences
const [view, setView] = useLocalStorage('preferred-view', 'grid')

<div className="flex gap-2">
  <Button
    variant={view === 'grid' ? 'default' : 'ghost'}
    onClick={() => setView('grid')}
  >
    <Grid className="h-4 w-4" />
  </Button>
  <Button
    variant={view === 'list' ? 'default' : 'ghost'}
    onClick={() => setView('list')}
  >
    <List className="h-4 w-4" />
  </Button>
</div>
```

#### Pattern: Smart Suggestions
**Psychology**: Reduced cognitive load + anticipation
**Implementation**:
```tsx
<Command>
  <CommandInput placeholder="Search or create..." />
  <CommandList>
    <CommandGroup heading="Suggestions">
      {suggestions.map(item => (
        <CommandItem key={item.id}>
          <Sparkles className="mr-2 h-4 w-4 text-primary" />
          {item.title}
        </CommandItem>
      ))}
    </CommandGroup>
  </CommandList>
</Command>
```

### 6. Scarcity & Urgency

#### Pattern: Countdown Timer
**Psychology**: Time pressure + scarcity bias
**Implementation**:
```tsx
<div className="flex items-center gap-2 text-sm">
  <Clock className="h-4 w-4 text-destructive" />
  <span className="text-destructive font-medium">
    {formatDistanceToNow(deadline)} left
  </span>
</div>
```

#### Pattern: Limited Slots
**Psychology**: Scarcity creates value
**Implementation**:
```tsx
<Card>
  <CardHeader>
    <CardTitle>Premium Feature</CardTitle>
    <CardDescription>
      <motion.span
        key={slotsRemaining}
        initial={{ scale: 1.2, color: 'hsl(var(--destructive))' }}
        animate={{ scale: 1, color: 'hsl(var(--muted-foreground))' }}
      >
        Only {slotsRemaining} spots left!
      </motion.span>
    </CardDescription>
  </CardHeader>
</Card>
```

### 7. Variable Rewards

#### Pattern: Random Positive Feedback
**Psychology**: Dopamine trigger + anticipation
**Implementation**:
```tsx
const encouragements = [
  "Great work!",
  "You're on fire!",
  "Fantastic!",
  "Keep it up!",
  "Amazing progress!"
]

const randomEncouragement = encouragements[Math.floor(Math.random() * encouragements.length)]

<motion.div
  initial={{ opacity: 0, y: 20 }}
  animate={{ opacity: 1, y: 0 }}
  exit={{ opacity: 0, y: -20 }}
  className="text-sm text-primary font-medium"
>
  ✨ {randomEncouragement}
</motion.div>
```

### 8. Progressive Disclosure

#### Pattern: Expandable Details
**Psychology**: Reduced cognitive load + user control
**Implementation**:
```tsx
<Collapsible>
  <CollapsibleTrigger className="flex items-center gap-2">
    <ChevronDown className="h-4 w-4 transition-transform data-[state=open]:rotate-180" />
    Advanced Options
  </CollapsibleTrigger>
  <CollapsibleContent className="space-y-2">
    {/* Advanced options */}
  </CollapsibleContent>
</Collapsible>
```

---

## MCP Integration Workflows

### Chrome DevTools MCP

**Complete workflow for visual verification**:

#### 1. Setup Local Server
```bash
# Ensure dev server is running
cd app && npm run dev
```

#### 2. Navigate to Page
```typescript
await chromeDevTools.navigate_page({
  url: 'http://localhost:3000/dashboard'
})

// Wait for page load
await chromeDevTools.wait_for({
  selector: 'main',
  timeout: 5000
})
```

#### 3. Take Baseline Screenshots
```typescript
// Light mode
await chromeDevTools.take_screenshot({
  path: '.claude/skills/ui-improver-addictive-ux/assets/before-light.png',
  fullPage: true
})

// Switch to dark mode
await chromeDevTools.evaluate_script({
  script: 'document.documentElement.classList.add("dark")'
})

// Dark mode
await chromeDevTools.take_screenshot({
  path: '.claude/skills/ui-improver-addictive-ux/assets/before-dark.png',
  fullPage: true
})
```

#### 4. Test Interactions
```typescript
// Hover state
await chromeDevTools.evaluate_script({
  script: `
    document.querySelector('button').dispatchEvent(
      new MouseEvent('mouseover', { bubbles: true })
    )
  `
})

await chromeDevTools.take_screenshot({
  path: '.claude/skills/ui-improver-addictive-ux/assets/hover-state.png'
})

// Focus state
await chromeDevTools.click({ selector: 'input[type="text"]' })
await chromeDevTools.take_screenshot({
  path: '.claude/skills/ui-improver-addictive-ux/assets/focus-state.png'
})
```

#### 5. Mobile Viewport Testing
```typescript
// Set mobile viewport
await chromeDevTools.evaluate_script({
  script: `
    const meta = document.querySelector('meta[name="viewport"]')
    meta.setAttribute('content', 'width=375, initial-scale=1')
  `
})

await chromeDevTools.take_screenshot({
  path: '.claude/skills/ui-improver-addictive-ux/assets/mobile.png',
  fullPage: true
})
```

### shadcn MCP

**Component discovery workflow**:

```bash
# Search for available components
npx shadcn@latest

# Add specific components
npx shadcn@latest add button
npx shadcn@latest add card
npx shadcn@latest add form
npx shadcn@latest add progress
npx shadcn@latest add toast

# Add dialog components
npx shadcn@latest add dialog alert-dialog

# Add navigation components
npx shadcn@latest add navigation-menu tabs

# Add feedback components
npx shadcn@latest add badge tooltip
```

### Context7 MCP

**Latest patterns research**:

```typescript
// Framer Motion patterns
await context7.resolve_library_id({ libraryName: "framer-motion" })
// Returns: "/framer/motion"

await context7.get_library_docs({
  context7CompatibleLibraryID: "/framer/motion",
  topic: "spring animations variants stagger gestures drag",
  tokens: 5000
})

// Tailwind CSS patterns
await context7.resolve_library_id({ libraryName: "tailwindcss" })
// Returns: "/tailwindlabs/tailwindcss"

await context7.get_library_docs({
  context7CompatibleLibraryID: "/tailwindlabs/tailwindcss",
  topic: "dark mode animations custom properties arbitrary values",
  tokens: 4000
})

// React patterns
await context7.resolve_library_id({ libraryName: "react" })
// Returns: "/facebook/react"

await context7.get_library_docs({
  context7CompatibleLibraryID: "/facebook/react",
  topic: "hooks performance optimization useCallback useMemo",
  tokens: 3000
})
```

---

## Success Metrics

**Every UI improvement MUST meet these criteria**:

### Visual Consistency (100% Required)
- [ ] ✅ All colors from STYLE_GUIDE palette
- [ ] ✅ All spacing from spacing scale
- [ ] ✅ All typography from type scale
- [ ] ✅ Consistent component patterns (shadcn/Aceternity)
- [ ] ✅ No arbitrary values (use semantic tokens)

### Addictive UX (3+ Patterns Minimum)
- [ ] ✅ Implemented at least 3 addictive UX patterns
- [ ] ✅ Spring animations for satisfying feel
- [ ] ✅ Instant feedback on all interactions
- [ ] ✅ Progress indicators where applicable
- [ ] ✅ Celebration moments for achievements

### Accessibility (WCAG 2.1 AA Mandatory)
- [ ] ✅ All text meets 4.5:1 contrast
- [ ] ✅ All UI components meet 3:1 contrast
- [ ] ✅ Keyboard navigable (Tab, Enter, Escape, Arrows)
- [ ] ✅ ARIA labels on icon buttons
- [ ] ✅ Focus indicators visible (2px ring)
- [ ] ✅ Screen reader compatible

### Responsiveness (All Breakpoints)
- [ ] ✅ Mobile (320px-639px) tested
- [ ] ✅ Tablet (640px-1023px) tested
- [ ] ✅ Desktop (1024px+) tested
- [ ] ✅ Touch targets 44px minimum
- [ ] ✅ Mobile-first approach

### Dark Mode (Both Modes)
- [ ] ✅ Light mode looks good
- [ ] ✅ Dark mode looks good
- [ ] ✅ Semantic colors adapt correctly
- [ ] ✅ Sufficient contrast in both modes
- [ ] ✅ Images/logos have variants

### Performance (60fps Target)
- [ ] ✅ Animations run at 60fps
- [ ] ✅ No layout thrashing
- [ ] ✅ No excessive repaints
- [ ] ✅ Interaction response <100ms
- [ ] ✅ No layout shift on load

### Documentation (Complete Evidence)
- [ ] ✅ Before/after screenshots (light & dark)
- [ ] ✅ Mobile screenshots
- [ ] ✅ Hover/focus state screenshots
- [ ] ✅ Improvement report written
- [ ] ✅ Addictive UX patterns documented

---

## Final Checklist

**Before completing any UI improvement task, verify ALL of the following**:

### Phase Completion
- [ ] ✅ Phase 0: STYLE_GUIDE reviewed, baseline screenshots taken
- [ ] ✅ Phase 1: Complete audit documented, Context7 research done
- [ ] ✅ Phase 2: Improvement plan with components, animations, UX patterns
- [ ] ✅ Phase 3: Iterative implementation with screenshot verification
- [ ] ✅ Phase 4: Comprehensive verification across all dimensions

### MCP Integration
- [ ] ✅ Context7 consulted for latest patterns (Framer Motion, Tailwind, React)
- [ ] ✅ shadcn MCP used for component discovery
- [ ] ✅ Chrome DevTools MCP used for screenshot verification
- [ ] ✅ All screenshots saved in `.claude/skills/ui-improver-addictive-ux/assets/`

### Quality Gates
- [ ] ✅ STYLE_GUIDE compliance: 100%
- [ ] ✅ Addictive UX patterns: Minimum 3 implemented
- [ ] ✅ Accessibility: WCAG 2.1 AA compliant
- [ ] ✅ Responsiveness: All breakpoints tested
- [ ] ✅ Dark mode: Both modes verified
- [ ] ✅ Performance: 60fps animations confirmed

### Deliverables
- [ ] ✅ Improved code committed
- [ ] ✅ Screenshot gallery created
- [ ] ✅ Improvement report documented
- [ ] ✅ No business logic modified
- [ ] ✅ No tests broken

---

**This skill is your complete guide to creating addictive, accessible, high-performance user experiences. Follow it rigorously, and you will transform functional interfaces into experiences that users LOVE.**
