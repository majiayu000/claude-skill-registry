---
name: mobile-patterns
description: Apply mobile navigation, layout patterns, and responsive strategies. Implements bottom nav, drawer menus, responsive grids, and mobile-specific component adaptations.
---

# Mobile Patterns Skill

Apply proven mobile navigation patterns, responsive layouts, and mobile-specific component adaptations to create thumb-friendly, platform-aware interfaces.

## When to Use

Use `/mobile-patterns` when you need to:
- Convert desktop navigation to mobile-friendly patterns
- Implement bottom navigation, drawer menus, or tab bars
- Create responsive grid systems with mobile-first breakpoints
- Adapt components for mobile (cards → lists, modals → sheets)
- Ensure thumb-zone ergonomics and safe area support

## Instructions

### Phase 1: Analyze Current Layout

**Goal**: Understand current navigation and layout structure

**I will:**
1. Read existing navigation components to understand structure
2. Identify layout patterns (grid, flex, absolute positioning)
3. Check for existing mobile breakpoints and responsive behavior
4. Note any mobile-specific components already in use

**Tools I use:**
- Read: Review navigation and layout component files
- Grep: Search for media queries, viewport meta tags, mobile classes

---

### Phase 2: Choose Mobile Navigation Pattern

**Goal**: Select the best navigation pattern for the use case

**Navigation Pattern Decision Matrix:**

| Pattern | Best For | Pros | Cons |
|---------|----------|------|------|
| **Bottom Nav** | 3-5 top-level sections | Thumb-friendly, always visible | Limited space, max 5 items |
| **Drawer** | Complex hierarchy, 6+ sections | Space-efficient, scalable | Hidden by default, requires tap |
| **Tab Bar + FAB** | Content + primary action | Combines nav + CTA | More complex, needs careful spacing |
| **Segmented Control** | 2-4 view modes (same context) | Clear, iOS-native feel | Only for switching views, not navigation |

**I will:**
1. Evaluate number of navigation items and hierarchy depth
2. Consider primary user action (read, create, switch views)
3. Recommend pattern based on matrix above
4. Provide rationale for choice

---

### Phase 3: Implement Navigation Pattern

**Goal**: Create mobile navigation with proper touch targets and safe areas

**Bottom Navigation Example:**

```css
/* Bottom nav with safe area support */
.bottomNav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 56px;
  padding-bottom: env(safe-area-inset-bottom);
  background: var(--color-bg);
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: space-around;
  align-items: center;
  z-index: 1000;
}

.navItem {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  min-width: 48px;
  min-height: 48px;
  padding: 8px;
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: color 0.2s ease;
}

.navItem:active {
  transform: scale(0.95);
}

.navItem.active {
  color: var(--color-primary);
}

.navIcon {
  width: 24px;
  height: 24px;
}

.navLabel {
  font-size: 12px;
  font-weight: 500;
}

.navBadge {
  position: absolute;
  top: 6px;
  right: 6px;
  min-width: 18px;
  height: 18px;
  padding: 0 4px;
  background: var(--color-error);
  color: white;
  border-radius: 9px;
  font-size: 11px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}
```

**Drawer Menu Example:**

```css
/* Slide-in drawer with backdrop */
.drawer {
  position: fixed;
  top: 0;
  left: -280px;
  width: 280px;
  height: 100vh;
  background: var(--color-bg);
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
  z-index: 2000;
  overflow-y: auto;
  padding-top: env(safe-area-inset-top);
}

.drawer.open {
  transform: translateX(280px);
}

.backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s ease;
  z-index: 1999;
}

.backdrop.visible {
  opacity: 1;
  pointer-events: auto;
}

.drawerItem {
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 48px;
  padding: 12px 16px;
  color: var(--color-text);
  text-decoration: none;
  transition: background 0.2s ease;
}

.drawerItem:active {
  background: var(--color-bg-hover);
}

.hamburger {
  width: 48px;
  height: 48px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 6px;
  background: none;
  border: none;
  cursor: pointer;
}

.hamburgerLine {
  width: 24px;
  height: 2px;
  background: var(--color-text);
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.hamburger.open .hamburgerLine:nth-child(1) {
  transform: translateY(8px) rotate(45deg);
}

.hamburger.open .hamburgerLine:nth-child(2) {
  opacity: 0;
}

.hamburger.open .hamburgerLine:nth-child(3) {
  transform: translateY(-8px) rotate(-45deg);
}
```

**Tab Bar with FAB Example:**

```css
.tabBar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: 56px;
  padding-bottom: env(safe-area-inset-bottom);
  background: var(--color-bg);
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: space-around;
  z-index: 1000;
}

.fab {
  position: fixed;
  bottom: calc(56px + env(safe-area-inset-bottom) + 16px);
  right: 16px;
  width: 56px;
  height: 56px;
  border-radius: 28px;
  background: var(--color-primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  border: none;
  z-index: 1001;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.fab:active {
  transform: scale(0.9);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}
```

---

### Phase 4: Implement Responsive Grid

**Goal**: Create mobile-first responsive grid with appropriate breakpoints

**Mobile-First Breakpoint System:**

```css
/* Mobile-first base styles (320px+) */
.container {
  width: 100%;
  padding: 16px;
  margin: 0 auto;
}

.grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

/* Small tablets (640px+) */
@media (min-width: 640px) {
  .container {
    padding: 24px;
  }

  .grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 24px;
  }
}

/* Tablets (768px+) */
@media (min-width: 768px) {
  .container {
    max-width: 768px;
  }

  .grid {
    grid-template-columns: repeat(3, 1fr);
  }
}

/* Desktop (1024px+) */
@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
    padding: 32px;
  }

  .grid {
    grid-template-columns: repeat(4, 1fr);
    gap: 32px;
  }
}

/* Large desktop (1280px+) */
@media (min-width: 1280px) {
  .container {
    max-width: 1280px;
  }
}
```

**Content-First Responsive Patterns:**

```css
/* Stack on mobile, side-by-side on tablet+ */
.twoColumn {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

@media (min-width: 768px) {
  .twoColumn {
    flex-direction: row;
  }

  .twoColumn > * {
    flex: 1;
  }
}

/* Card grid - 1 col mobile, 2 col tablet, 3 col desktop */
.cardGrid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 16px;
}

@media (min-width: 640px) {
  .cardGrid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  }
}
```

---

### Phase 5: Mobile Component Adaptations

**Goal**: Transform desktop components for mobile constraints

**Table → List Transformation:**

```css
/* Desktop: table */
.dataTable {
  width: 100%;
  border-collapse: collapse;
}

.dataTable th,
.dataTable td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid var(--color-border);
}

/* Mobile: stacked cards */
@media (max-width: 640px) {
  .dataTable thead {
    display: none;
  }

  .dataTable tbody {
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .dataTable tr {
    display: flex;
    flex-direction: column;
    padding: 16px;
    background: var(--color-bg-card);
    border-radius: 8px;
    border: 1px solid var(--color-border);
  }

  .dataTable td {
    padding: 4px 0;
    border: none;
    display: flex;
    justify-content: space-between;
  }

  .dataTable td::before {
    content: attr(data-label);
    font-weight: 600;
    color: var(--color-text-secondary);
  }
}
```

**Modal → Bottom Sheet:**

```css
/* Desktop: centered modal */
.modal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 90%;
  max-width: 500px;
  max-height: 80vh;
  background: var(--color-bg);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  overflow-y: auto;
}

/* Mobile: bottom sheet */
@media (max-width: 640px) {
  .modal {
    top: auto;
    left: 0;
    right: 0;
    bottom: 0;
    transform: none;
    width: 100%;
    max-width: none;
    max-height: 85vh;
    border-radius: 16px 16px 0 0;
    padding: 24px;
    padding-bottom: calc(24px + env(safe-area-inset-bottom));
  }

  .modal::before {
    content: '';
    position: absolute;
    top: 12px;
    left: 50%;
    transform: translateX(-50%);
    width: 36px;
    height: 4px;
    background: var(--color-border);
    border-radius: 2px;
  }
}
```

---

## Mobile Pattern Checklist

Before completing this skill, verify:

### Touch Targets
- [ ] All interactive elements are at least 48x48px (WCAG AA)
- [ ] Navigation items have adequate spacing (no crowding)
- [ ] Buttons have visible tap states (opacity, scale, or color change)

### Safe Areas
- [ ] Bottom navigation includes `padding-bottom: env(safe-area-inset-bottom)`
- [ ] Fixed headers include `padding-top: env(safe-area-inset-top)`
- [ ] FAB placement accounts for safe areas
- [ ] Modals/sheets respect safe areas on all edges

### Responsive Breakpoints
- [ ] Mobile-first approach (base styles for smallest screens)
- [ ] Breakpoints match content needs, not arbitrary device sizes
- [ ] Grid adapts smoothly across breakpoints
- [ ] Typography scales appropriately

### Component Adaptations
- [ ] Tables transform to cards/lists on mobile
- [ ] Modals become bottom sheets on mobile
- [ ] Multi-column layouts stack on mobile
- [ ] Image galleries use appropriate mobile patterns

### Navigation UX
- [ ] Primary navigation is easily reachable (bottom or top)
- [ ] Drawer has backdrop and close button
- [ ] Active state is clearly visible
- [ ] Navigation doesn't obstruct content unnecessarily

### Orientation Support
- [ ] Layout works in both portrait and landscape
- [ ] Fixed elements don't overflow in landscape
- [ ] Navigation remains accessible in landscape

---

## Output Format

```markdown
## Mobile Pattern Implementation

### Navigation Pattern: [Bottom Nav / Drawer / Tab Bar + FAB]

**Rationale**: [Why this pattern was chosen]

### Breakpoint Strategy
- Mobile: 320px - 639px
- Tablet: 640px - 1023px
- Desktop: 1024px+

### Components Updated
1. **Navigation** - [Description of changes]
2. **Grid System** - [Description of responsive grid]
3. **[Component Name]** - [Mobile adaptation applied]

### Files Modified
- `[filepath]` - Navigation component
- `[filepath]` - Grid/layout styles
- `[filepath]` - Mobile-adapted components

### Mobile Checklist Results
✅ All touch targets ≥ 48px
✅ Safe areas handled
✅ Mobile-first breakpoints
✅ Components adapt appropriately
✅ Orientation support

### Next Steps
- Test on physical devices (iOS/Android)
- Verify safe area spacing on notched devices
- Test landscape orientation
- Validate touch target sizes with `/mobile-accessibility`
```

---

## Integration with Other Skills

This skill works well with:
- **/touch-interactions** - Add swipe gestures and touch feedback
- **/mobile-accessibility** - Ensure screen reader and keyboard support
- **/component-states** - Add proper interactive states to mobile components
- **/micro-interactions** - Polish with subtle animations

---

## Notes

- Always use mobile-first CSS (base styles for mobile, media queries for larger screens)
- Safe area insets are critical for modern iOS devices with notches
- Touch targets should be 48x48px minimum (WCAG AA), 44x44px is iOS minimum
- Bottom navigation works best for 3-5 items; use drawer for more
- Test on actual devices when possible - simulators don't capture thumb ergonomics
- Consider one-handed use - most users hold phones in bottom-right area
