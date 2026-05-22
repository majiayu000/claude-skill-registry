---
name: responsive-design-planner
description: Plans responsive design breakpoints, mobile-first approaches, and adaptive layouts. Defines how designs adapt across different screen sizes and devices. Considers touch vs mouse interactions.
---

# Responsive Design Planner Skill

## Instructions

1. Analyze responsive requirements from task
2. Define breakpoints (mobile, tablet, desktop)
3. Plan mobile-first design approach
4. Specify layout adaptations at each breakpoint
5. Define component variations for different screens
6. Consider touch vs mouse interactions
7. Return structured responsive design specifications with:
   - Breakpoint definitions
   - Layout adaptations
   - Component variations
   - Interaction differences
   - Content prioritization

## Examples

**Input:** "Plan responsive design for dashboard"
**Output:**
```markdown
### Responsive Design Plan

**Breakpoints:**
- Mobile: 320px - 767px
- Tablet: 768px - 1023px
- Desktop: 1024px - 1919px
- Large Desktop: 1920px+

**Mobile (320px - 767px):**
- Single column layout
- Stack all components vertically
- Hamburger menu navigation
- Full-width buttons
- Larger touch targets (44px minimum)
- Simplified content
- Bottom navigation for key actions

**Tablet (768px - 1023px):**
- Two-column layout possible
- Sidebar collapses to drawer
- Touch-optimized interactions
- Medium-sized components
- Tab navigation

**Desktop (1024px+):**
- Multi-column layouts
- Sidebar visible
- Hover interactions enabled
- Smaller touch targets acceptable
- More content visible
- Keyboard shortcuts available

**Component Adaptations:**
- Navigation: Hamburger (mobile) → Sidebar (desktop)
- Cards: Single column (mobile) → Grid (desktop)
- Forms: Stacked (mobile) → Inline (desktop)
- Tables: Scrollable (mobile) → Full table (desktop)

**Interaction Differences:**
- Mobile: Touch gestures, swipe, tap
- Desktop: Hover, click, keyboard shortcuts
```

## Breakpoint Strategies

- **Mobile First**: Start with mobile, enhance for larger screens
- **Desktop First**: Start with desktop, adapt for smaller screens
- **Common Breakpoints**: 320px, 480px, 768px, 1024px, 1280px, 1920px
- **Content-Based**: Breakpoints based on content needs
- **Device-Based**: Breakpoints based on common device sizes

## Layout Adaptations

- **Single Column → Multi-Column**: Stack to side-by-side
- **Sidebar**: Collapse to drawer/menu on mobile
- **Navigation**: Horizontal to vertical, hamburger menu
- **Grids**: Fewer columns on smaller screens
- **Content**: Hide/show content based on screen size

## Touch vs Mouse

- **Touch Targets**: Minimum 44x44px for mobile
- **Hover States**: Only on desktop (not mobile)
- **Gestures**: Swipe, pinch, tap on mobile
- **Keyboard**: More important on desktop
- **Click Areas**: Larger on mobile for easier tapping
