---
name: interaction-physics
description: Master microinteractions, animations, transitions, and feedback systems. Create intentional, delightful interactions that guide users and provide clear feedback. Includes animation principles, timing, easing, state transitions, and best practices for performance and accessibility.
---

# Interaction Design

## Overview

Interactions are the moments when your interface comes alive. They're the transitions between states, the feedback when users take action, the animations that guide attention. When done well, interactions are invisible—they feel natural and right. When done poorly, they distract or confuse.

This skill teaches you to think about interactions systematically: understanding animation principles, designing intentional microinteractions, providing clear feedback, and ensuring performance and accessibility.

## Core Methodology: Microinteractions

A microinteraction is a small, contained interaction that accomplishes a specific task. Examples: button hover state, form validation feedback, loading spinner, success notification, menu open/close.

### The Anatomy of a Microinteraction

Every microinteraction has four parts:

1. **Trigger** — What initiates the interaction? (user action, system event, time-based)
2. **Rules** — What happens as a result? (what animates, what changes, how long)
3. **Feedback** — What does the user see/hear? (animation, sound, haptic)
4. **Loops & Modes** — Does it repeat? Can it be interrupted?

**Example: Button Hover State**

```
Trigger: User hovers over button
Rules: 
  - Background color changes to darker shade
  - Duration: 200ms
  - Easing: ease-out
Feedback: 
  - Visual: background color transition
  - Indicates: button is interactive
Loops & Modes: 
  - Repeats on every hover
  - Can be interrupted by click or mouse leave
```

### Designing Intentional Microinteractions

**Principle 1: Provide Feedback**
Every user action should result in visible feedback. Users need to know their action was registered.

**Principle 2: Guide Attention**
Use animation to guide users' attention to important elements.

**Principle 3: Communicate State**
Use animation to communicate state changes (loading, success, error, etc.).

**Principle 4: Delight Without Distraction**
Add personality and delight, but don't distract from the task.

## Animation Principles

### Principle 1: Timing

Timing is critical. Too fast and the animation feels abrupt. Too slow and it feels sluggish.

**General Guidelines:**
- **UI Feedback** (hover, focus, state change): 150-250ms
- **Transitions** (page changes, modal open/close): 300-500ms
- **Attention-Grabbing** (alerts, notifications): 500-1000ms
- **Loading** (spinners, progress bars): 1-2 seconds or continuous

```css
/* UI Feedback - Fast */
button {
  transition: background-color 200ms ease-out;
}

/* Transitions - Medium */
.modal {
  transition: opacity 400ms ease-out, transform 400ms ease-out;
}

/* Loading - Slower */
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.spinner {
  animation: spin 1s linear infinite;
}
```

### Principle 2: Easing

Easing functions control how an animation accelerates and decelerates. Different easing functions convey different meanings.

**Common Easing Functions:**

| Easing | Meaning | Use Case |
| :--- | :--- | :--- |
| `linear` | Constant speed | Continuous, mechanical (spinners, progress bars) |
| `ease-in` | Slow start, fast end | Exiting, dismissing |
| `ease-out` | Fast start, slow end | Entering, appearing, most interactions |
| `ease-in-out` | Slow start and end | Smooth, natural transitions |
| `cubic-bezier(0.34, 1.56, 0.64, 1)` | Elastic, bouncy | Playful, attention-grabbing |

```css
/* UI Feedback - ease-out (most common) */
button {
  transition: background-color 200ms ease-out;
}

/* Entering - ease-out */
.modal {
  animation: slideIn 400ms ease-out;
}

/* Exiting - ease-in */
.modal.closing {
  animation: slideOut 300ms ease-in;
}

/* Continuous - linear */
.spinner {
  animation: spin 1s linear infinite;
}

/* Playful - cubic-bezier */
.bounce {
  animation: bounce 600ms cubic-bezier(0.34, 1.56, 0.64, 1);
}
```

### Principle 3: Distance

The distance an element moves affects how long the animation should take. Larger distances need longer durations.

```css
/* Small movement - short duration */
button:hover {
  transform: scale(1.05);
  transition: transform 150ms ease-out;
}

/* Medium movement - medium duration */
.modal {
  animation: slideIn 400ms ease-out;
}
@keyframes slideIn {
  from { transform: translateY(20px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

/* Large movement - longer duration */
.page-transition {
  animation: fadeIn 600ms ease-out;
}
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

## Common Microinteractions

### Microinteraction 1: Button States

```css
/* Default state */
button {
  background-color: var(--color-primary);
  color: white;
  transition: background-color 200ms ease-out;
}

/* Hover state */
button:hover:not(:disabled) {
  background-color: var(--color-primary-dark);
}

/* Active state */
button:active:not(:disabled) {
  background-color: var(--color-primary-darker);
  transform: scale(0.98);
}

/* Focus state */
button:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
}

/* Disabled state */
button:disabled {
  background-color: var(--color-disabled);
  cursor: not-allowed;
  opacity: 0.6;
}

/* Loading state */
button.loading {
  pointer-events: none;
  opacity: 0.8;
}

button.loading::after {
  content: '';
  display: inline-block;
  width: 16px;
  height: 16px;
  margin-left: 8px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}
```

### Microinteraction 2: Form Validation

```css
/* Input default state */
input {
  border: 1px solid var(--color-border);
  transition: border-color 200ms ease-out, box-shadow 200ms ease-out;
}

/* Input focus state */
input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Input valid state */
input.valid {
  border-color: var(--color-success);
}

input.valid:focus {
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.1);
}

/* Input error state */
input.error {
  border-color: var(--color-error);
}

input.error:focus {
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
}

/* Error message animation */
.error-message {
  animation: slideDown 300ms ease-out;
  color: var(--color-error);
  font-size: 14px;
  margin-top: 4px;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-8px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### Microinteraction 3: Loading States

```css
/* Skeleton loading */
.skeleton {
  background: linear-gradient(
    90deg,
    var(--color-skeleton) 0%,
    var(--color-skeleton-light) 50%,
    var(--color-skeleton) 100%
  );
  background-size: 200% 100%;
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Spinner */
.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid var(--color-border);
  border-top-color: var(--color-primary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Progress bar */
.progress-bar {
  height: 4px;
  background-color: var(--color-border);
  overflow: hidden;
}

.progress-bar-fill {
  height: 100%;
  background-color: var(--color-primary);
  transition: width 300ms ease-out;
}
```

### Microinteraction 4: Notifications

```css
/* Notification container */
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  padding: 16px;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  animation: slideIn 300ms ease-out;
  z-index: 1000;
}

/* Notification variants */
.notification.success {
  border-left: 4px solid var(--color-success);
}

.notification.error {
  border-left: 4px solid var(--color-error);
}

.notification.warning {
  border-left: 4px solid var(--color-warning);
}

/* Notification exit animation */
.notification.exiting {
  animation: slideOut 300ms ease-in forwards;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(400px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideOut {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(400px);
  }
}
```

### Microinteraction 5: Transitions Between Pages

```css
/* Page fade transition */
.page {
  animation: fadeIn 400ms ease-out;
}

.page.exiting {
  animation: fadeOut 300ms ease-in forwards;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeOut {
  from { opacity: 1; }
  to { opacity: 0; }
}

/* Page slide transition */
.page {
  animation: slideIn 400ms ease-out;
}

.page.exiting {
  animation: slideOut 300ms ease-in forwards;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes slideOut {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(-30px);
  }
}
```

## Performance Considerations

### Use GPU-Accelerated Properties

Animate properties that are GPU-accelerated for smooth performance:

**Good (GPU-accelerated):**
- `transform` (translate, rotate, scale)
- `opacity`

**Avoid (CPU-intensive):**
- `left`, `top`, `width`, `height`
- `background-color` (unless necessary)
- `box-shadow`

```css
/* Good - GPU-accelerated */
button:hover {
  transform: scale(1.05);
  transition: transform 200ms ease-out;
}

/* Avoid - CPU-intensive */
button:hover {
  width: 110px;
  height: 110px;
  transition: width 200ms ease-out, height 200ms ease-out;
}
```

### Reduce Motion for Users Who Prefer It

Respect the `prefers-reduced-motion` media query:

```css
/* Default animations */
button {
  transition: background-color 200ms ease-out;
}

/* Reduced motion */
@media (prefers-reduced-motion: reduce) {
  button {
    transition: none;
  }
}
```

## Accessibility Considerations

### 1. Provide Non-Animation Feedback

Don't rely on animation alone for feedback. Combine with color, text, or icons.

```css
/* Bad - only animation */
button:hover {
  transform: scale(1.1);
}

/* Good - animation + color change */
button:hover {
  background-color: var(--color-primary-dark);
  transform: scale(1.05);
}
```

### 2. Ensure Keyboard Navigation

Interactions should work with keyboard navigation:

```css
/* Hover state for mouse users */
button:hover {
  background-color: var(--color-primary-dark);
}

/* Focus state for keyboard users */
button:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
  background-color: var(--color-primary-dark);
}
```

### 3. Avoid Motion Sickness

Avoid rapid, flashing, or disorienting animations:

```css
/* Bad - rapid flashing */
.alert {
  animation: flash 100ms infinite;
}

/* Good - subtle, slow animation */
.alert {
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
```

## How to Use This Skill with Claude Code

### Audit Your Interactions

```
"I'm using the interaction-design skill. Can you audit my interactions?
- Identify microinteractions that are missing
- Check animation timing and easing
- Identify performance issues (CPU-intensive animations)
- Check accessibility (reduced motion, keyboard navigation)
- Suggest improvements"
```

### Design Microinteractions

```
"Can you help me design microinteractions for:
- Button states (hover, active, disabled, loading)
- Form validation feedback
- Loading states
- Success/error notifications
- Page transitions"
```

### Implement Animations

```
"Can you implement animations for:
- Button hover and active states
- Modal open/close
- Page transitions
- Loading spinner
- Notification entrance/exit
Include timing, easing, and accessibility considerations"
```

### Optimize Animation Performance

```
"Can you optimize my animations for performance?
- Identify CPU-intensive animations
- Suggest GPU-accelerated alternatives
- Check for unnecessary animations
- Ensure smooth 60fps performance"
```

## Design Critique: Evaluating Your Interactions

Claude Code can critique your interactions:

```
"Can you evaluate my interactions?
- Are my animations intentional and purposeful?
- Is my timing appropriate?
- Are my easing functions right?
- Are my interactions accessible?
- What's one thing I could improve immediately?"
```

## Integration with Other Skills

- **design-foundation** — Animation tokens and timing
- **component-architecture** — Interactions in components
- **accessibility-excellence** — Accessible interactions
- **layout-system** — Transitions between layouts

## Key Principles

**1. Animation Should Have Purpose**
Every animation should serve a purpose: provide feedback, guide attention, or communicate state.

**2. Timing Matters**
Appropriate timing makes animations feel natural. Too fast or too slow feels wrong.

**3. Easing Conveys Meaning**
Different easing functions convey different meanings (ease-out for entering, ease-in for exiting).

**4. Performance is Critical**
Smooth animations require GPU-accelerated properties and careful performance optimization.

**5. Accessibility is Essential**
Respect user preferences for reduced motion and provide non-animation feedback.

## Checklist: Is Your Interaction Design Ready?

- [ ] All user actions provide visible feedback
- [ ] Animation timing is appropriate (150-250ms for UI feedback)
- [ ] Easing functions are intentional (ease-out for entering, ease-in for exiting)
- [ ] Animations use GPU-accelerated properties (transform, opacity)
- [ ] Reduced motion preferences are respected
- [ ] Keyboard navigation works well
- [ ] Non-animation feedback is provided (color, text, icons)
- [ ] Loading states are clear and communicative
- [ ] Error states are clear and helpful
- [ ] Success states are clear and satisfying
- [ ] Page transitions are smooth and intentional

Intentional, delightful interactions transform a functional product into one that feels loved.
