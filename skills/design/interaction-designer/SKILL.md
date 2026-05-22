---
name: interaction-designer
description: Designs interactions, animations, transitions, and micro-interactions. Specifies hover states, click feedback, loading states, and user feedback mechanisms. Ensures interactions are accessible and performant.
---

# Interaction Designer Skill

## Instructions

1. Analyze interaction requirements from task
2. Design interaction patterns and behaviors
3. Specify hover, active, focus states
4. Define animations and transitions
5. Design loading and feedback states
6. Ensure accessibility (keyboard, screen readers)
7. Return structured interaction specifications with:
   - Interaction descriptions
   - State transitions
   - Animation specifications
   - Timing and easing
   - Accessibility considerations

## Examples

**Input:** "Design button interactions"
**Output:**
```markdown
### Interactions: Button

**Hover State:**
- Background color darkens by 10%
- Transform: scale(1.02)
- Transition: 150ms ease-in-out
- Cursor changes to pointer

**Active State:**
- Background color darkens by 20%
- Transform: scale(0.98)
- Transition: 100ms ease-in-out

**Focus State:**
- Outline: 2px solid primary color
- Outline offset: 2px
- No animation (instant for accessibility)

**Loading State:**
- Show spinner icon
- Disable interaction
- Opacity: 0.7
- Cursor: not-allowed

**Success Feedback:**
- Show checkmark icon
- Background changes to success color
- Animation: fade in 200ms

**Accessibility:**
- Keyboard accessible (Enter/Space)
- Focus indicator visible
- Screen reader announces state changes
- Reduced motion: Disable animations if user prefers
```

## Interaction Types

- **Hover**: Mouse over interactions
- **Active**: Click/press interactions
- **Focus**: Keyboard focus interactions
- **Loading**: Processing/loading states
- **Success**: Success feedback
- **Error**: Error feedback
- **Transitions**: State change animations
- **Micro-interactions**: Small, delightful interactions
- **Gestures**: Touch/swipe interactions (mobile)

## Animation Guidelines

- **Duration**: 150-300ms for most interactions
- **Easing**: ease-in-out for most, ease-out for entrances
- **Performance**: Use transform and opacity (GPU accelerated)
- **Reduced Motion**: Respect prefers-reduced-motion
- **Purpose**: Animations should have purpose, not decoration

## Accessibility Considerations

- **Keyboard Accessible**: All interactions work with keyboard
- **Focus Indicators**: Clear focus states
- **Screen Reader Support**: Announce state changes
- **Reduced Motion**: Disable animations if user prefers
- **Touch Targets**: Minimum 44x44px for mobile
