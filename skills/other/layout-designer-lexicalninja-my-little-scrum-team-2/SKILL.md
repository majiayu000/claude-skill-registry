---
name: layout-designer
description: Designs page layouts, grid systems, and structural arrangements. Use when creating layouts for pages, sections, or components. Considers responsive design, visual hierarchy, and accessibility.
---

# Layout Designer Skill

## Instructions

1. Analyze layout requirements from task
2. Design page/section structure and organization
3. Create grid system or layout approach
4. Define visual hierarchy and content flow
5. Specify responsive breakpoints and adaptations
6. Consider accessibility (semantic structure, reading order)
7. Return structured layout specifications with:
   - Layout structure description
   - Grid system specifications
   - Component positioning
   - Responsive breakpoints
   - Spacing and alignment
   - Visual hierarchy

## Examples

**Input:** "Design layout for user profile page"
**Output:**
```markdown
### Layout Structure

**Desktop (1024px+):**
- Container: max-width 1200px, centered
- Grid: 12-column grid system
- Header: Full width, fixed top, height 64px
- Sidebar: 3 columns (left), fixed width 240px
- Main Content: 9 columns (right), flexible width
- Footer: Full width, height 80px

**Tablet (768px - 1023px):**
- Container: max-width 100%, padding 24px
- Grid: Single column
- Header: Full width, height 56px
- Sidebar: Hidden (collapsed into menu)
- Main Content: Full width
- Footer: Full width, height 64px

**Mobile (320px - 767px):**
- Container: Full width, padding 16px
- Grid: Single column
- Header: Full width, height 48px, hamburger menu
- Sidebar: Hidden (drawer menu)
- Main Content: Full width
- Footer: Full width, height 56px

### Visual Hierarchy
1. Header (navigation)
2. Main content area
3. Sidebar (secondary content)
4. Footer (tertiary content)

### Grid System
- 12-column grid
- Gutter: 24px (desktop), 16px (tablet), 12px (mobile)
- Column width: Flexible based on container
```

## Layout Types

- **Single Column**: Simple vertical layout
- **Multi-Column**: Sidebar + main content
- **Grid Layout**: Card grids, image galleries
- **Flexbox Layout**: Flexible component arrangements
- **CSS Grid**: Complex two-dimensional layouts
- **Fixed Header/Footer**: Sticky navigation patterns
- **Split Screen**: Two-panel layouts
- **Dashboard**: Multi-widget layouts

## Responsive Considerations

- **Mobile First**: Start with mobile layout
- **Breakpoints**: Define clear breakpoints (320px, 768px, 1024px, 1920px)
- **Adaptive Layouts**: How layout changes at each breakpoint
- **Content Reflow**: How content reorders on smaller screens
- **Navigation Patterns**: Mobile menu patterns (hamburger, drawer, tabs)

## Accessibility Considerations

- **Semantic HTML**: Use proper HTML5 semantic elements
- **Reading Order**: Logical content reading order
- **Focus Order**: Keyboard navigation follows visual order
- **Landmarks**: Proper use of ARIA landmarks
- **Skip Links**: Skip navigation links for keyboard users
