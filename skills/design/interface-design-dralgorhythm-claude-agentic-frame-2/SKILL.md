---
name: interface-design
description: Design user interfaces. Use when creating layouts, wireframes, or UI specifications. Covers design principles and UI patterns.
allowed-tools: Read, Write, Glob, Grep
---

# Interface Design

## Design Principles

### 1. Clarity
Make the interface obvious. Users shouldn't have to guess.

### 2. Consistency
Same actions, same results. Maintain patterns throughout.

### 3. Feedback
Respond to every action. Show progress, confirm success, explain errors.

### 4. Efficiency
Minimize steps. Optimize common workflows.

### 5. Forgiveness
Allow undo. Confirm destructive actions. Recover gracefully.

## UI Patterns

### Navigation
- **Top Nav**: Primary navigation, global actions
- **Side Nav**: Section navigation, hierarchical content
- **Breadcrumbs**: Show location in hierarchy
- **Tabs**: Switch between related views

### Forms
- Label above input
- Clear validation messages
- Inline validation where helpful
- Logical field grouping
- Clear call-to-action

### Feedback
- Loading states
- Success confirmations
- Error messages
- Empty states
- Progress indicators

### Actions
- Primary action prominent
- Secondary actions subtle
- Destructive actions require confirmation
- Disabled states clear

## Layout Principles

### Visual Hierarchy
- Size indicates importance
- Color draws attention
- Spacing groups elements
- Alignment creates order

### Grid System
```css
.container {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1rem;
}
```

### Responsive Design
- Mobile-first approach
- Breakpoints: 640px, 768px, 1024px, 1280px
- Fluid typography
- Flexible images

## Design Specification

When handing off to development:
- [ ] Color values (hex/RGB)
- [ ] Typography (font, size, weight, line-height)
- [ ] Spacing (margins, padding)
- [ ] Component states (default, hover, active, disabled)
- [ ] Responsive behavior
- [ ] Animations/transitions
