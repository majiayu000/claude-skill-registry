---
name: interaction-design
description: Design meaningful interactions and microinteractions. Create delightful user experiences through thoughtful animation, feedback, and responsive interface design.
---

# Interaction Design

## Overview

Interaction design focuses on how users engage with systems, creating intuitive and delightful experiences through feedback and responsiveness.

## When to Use

- Designing user flows and touchpoints
- Creating animations and transitions
- Defining error and loading states
- Building microinteractions
- Improving usability and feedback
- Mobile interaction patterns

## Instructions

### 1. **Interaction Patterns**

```yaml
Common Interaction Patterns:

Swipe:
  Use: Mobile lists, carousels
  Feedback: Visual sliding, momentum
  Accessibility: Keyboard alternative (arrows)

Tap & Hold:
  Use: Context menus, drag prep
  Feedback: Visual feedback after delay
  Duration: ~500ms before trigger

Pinch & Zoom:
  Use: Image viewing, maps
  Feedback: Smooth zoom animation
  Boundaries: Set min/max zoom levels

Drag & Drop:
  Use: Reordering, moving items
  Feedback: Visual during drag, drop confirmation
  Fallback: Alternative method (buttons)

Double Tap:
  Use: Zoom, favorite, select
  Feedback: Immediate visual response
  Conflict: Avoid 300ms delay confusion

---

## Microinteractions

Loading States:
  - Show immediately for >0.5s waits
  - Animate progress bar for long waits
  - Show percentage for determinate progress
  - Skeleton screens for content

Empty States:
  - Show friendly illustration
  - Explain what's empty
  - Provide action to fill (CTA)
  - Consider helpful suggestions

Error States:
  - Clear error message (what, why, how to fix)
  - Highlight error field
  - Provide recovery action
  - Don't repeat error on retry

Success Feedback:
  - Confirmation message (1-2 seconds)
  - Subtle animation or sound
  - Clear next step or action

Pull-to-Refresh:
  - Familiar mobile pattern
  - Clear visual feedback during pull
  - Confirmation when complete
  - Alternative: Manual refresh button
```

### 2. **Animation & Transition Design**

```python
# Define animations and transitions

class InteractionDesign:
    def define_animation(self, interaction):
        """Specify animation properties"""
        return {
            'trigger': interaction.trigger,  # Click, hover, load
            'element': interaction.element,
            'animation': {
                'type': interaction.animation_type,  # Fade, slide, scale
                'duration': interaction.duration,     # 200-400ms typical
                'easing': interaction.easing_fn,      # Ease-in-out
                'delay': interaction.delay_ms
            },
            'purpose': interaction.purpose,  # Feedback, guidance, delight
            'platform': ['Desktop', 'Mobile'],  # Platform-specific
            'accessibility': {
                'respects_prefers_reduced_motion': True,
                'non_distract': 'Critical interactions only'
            }
        }

    def define_transitions(self):
        """Page/screen transitions"""
        return {
            'navigation_forward': {
                'animation': 'Slide right',
                'duration': '300ms',
                'easing': 'ease-out'
            },
            'navigation_back': {
                'animation': 'Slide left',
                'duration': '300ms',
                'easing': 'ease-out'
            },
            'modal_open': {
                'animation': 'Fade + Scale up',
                'duration': '200ms',
                'easing': 'ease-out'
            },
            'modal_close': {
                'animation': 'Fade + Scale down',
                'duration': '150ms',
                'easing': 'ease-in'
            }
        }

    def animation_guidelines(self):
        """Best practices for animation"""
        return {
            'duration': {
                'micro_interactions': '100-200ms',
                'transitions': '200-400ms',
                'entrance_animations': '300-500ms',
                'avoid': '>500ms (feels sluggish)'
            },
            'easing': {
                'entrance': 'Ease out (fast start, slow end)',
                'exit': 'Ease in (slow start, fast end)',
                'focus': 'Ease-in-out for smooth feel'
            },
            'purpose': [
                'Provide feedback',
                'Guide user attention',
                'Communicate state change',
                'Delight users',
                'Avoid: Distraction, slowness'
            ]
        }
```

### 3. **Error Handling & Feedback**

```yaml
Error State Design:

Primary Error Message:
  "Payment declined"  (clear, non-technical)

Secondary Explanation:
  "Your card was declined by the bank. This might be due to
  insufficient funds, security concerns, or an expired card."

Recovery Action:
  [ Retry Payment ] [ Use Different Card ] [ Contact Support ]

Form Field Errors:
  - Highlight field with error color (red)
  - Show error icon
  - Place error message near field
  - Show error on blur, not on keystroke

Form Validation:
  - Real-time validation for good UX
  - Server-side validation for security
  - Show success state after valid input
  - Clear error when corrected

---

Success States:

Confirmation Message:
  "Payment successful!"
  Duration: 2-3 seconds
  Action: Auto-dismiss or click to close

Next Step:
  - Order confirmation email sent
  - What happens next?
  - Related actions

Visual Feedback:
  - Check mark animation
  - Subtle celebration animation
  - Sound (optional, if enabled)
```

### 4. **Accessibility in Interactions**

```javascript
// Ensure interactions are accessible

class AccessibleInteractions {
  ensureKeyboardAccess() {
    return {
      tab_order: 'Logical, top-to-bottom',
      focus_visible: 'Clear focus indicator (not removed)',
      enter_key: 'Activates buttons and links',
      space_key: 'Activates buttons',
      escape_key: 'Closes modals and menus',
      arrow_keys: 'Navigate lists, menus, carousels'
    };
  }

  respectMotionPreferences() {
    return {
      prefers_reduced_motion: {
        media_query: '@media (prefers-reduced-motion: reduce)',
        actions: [
          'Disable animations',
          'Reduce animation duration',
          'Remove parallax effects',
          'Disable autoplay'
        ]
      }
    };
  }

  screenReaderConsiderations() {
    return {
      announcements: 'Use ARIA live regions for updates',
      feedback: 'Provide screen reader feedback for interactions',
      labels: 'Clear, descriptive button labels',
      states: 'Announce state changes (expanded, selected)'
    };
  }
}
```

## Best Practices

### ✅ DO
- Keep animations under 400ms
- Provide clear visual feedback
- Use animations to guide attention
- Respect motion preferences
- Make interactions reversible
- Test with keyboard and screen readers
- Provide multiple interaction methods
- Design for touch and mouse
- Use appropriate easing curves
- Document interaction behavior

### ❌ DON'T
- Animate for decoration only
- Use animations longer than 500ms
- Ignore motion-sensitive users
- Remove focus indicators
- Trap users in modals
- Use confusing animations
- Animate everything
- Ignore loading states
- Forget error states
- Skip accessibility testing

## Interaction Design Tips

- Animation should feel instant (<200ms) or natural (300-500ms)
- Use consistent easing across experience
- Pair animations with haptic feedback on mobile
- Test animations on actual devices
