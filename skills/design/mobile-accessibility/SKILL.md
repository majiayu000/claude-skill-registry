---
name: mobile-accessibility
description: Ensure mobile interfaces work with VoiceOver, TalkBack, and screen readers. Audits touch target sizes, focus management, and WCAG 2.1 mobile criteria.
---

# Mobile Accessibility Skill

Comprehensive mobile accessibility audit and implementation for VoiceOver (iOS), TalkBack (Android), and touch-based screen reader navigation.

## When to Use

Use `/mobile-accessibility` when you need to:
- Audit mobile interface for accessibility issues
- Implement VoiceOver/TalkBack support
- Fix focus management in modals and bottom sheets
- Add screen reader announcements for dynamic content
- Ensure touch targets meet WCAG 2.1 mobile criteria
- Support switch control and alternative input methods

## Instructions

### Phase 1: Mobile Accessibility Audit

**Goal**: Identify mobile-specific accessibility issues

**WCAG 2.1 Mobile Criteria:**

| Criterion | Level | Requirement |
|-----------|-------|-------------|
| **2.5.5 Target Size** | AAA | 44x44 CSS pixels minimum |
| **2.5.1 Pointer Gestures** | A | Multi-point/path-based gestures have single-point alternative |
| **2.5.2 Pointer Cancellation** | A | Completion on up-event, can abort |
| **2.5.3 Label in Name** | A | Accessible name contains visible text |
| **2.5.4 Motion Actuation** | A | Motion-triggered functions can be disabled |
| **1.3.4 Orientation** | AA | Content works in portrait and landscape |
| **1.4.10 Reflow** | AA | Content reflows to 320px without horizontal scroll |

**I will:**
1. Check all interactive element sizes (44x44px minimum)
2. Verify screen reader labels are present and descriptive
3. Test focus order and keyboard navigation
4. Audit ARIA landmarks and roles
5. Check color contrast ratios (4.5:1 for normal text)
6. Verify form inputs have associated labels
7. Check that dynamic content announces to screen readers

**Audit bash commands:**

```bash
# Find small touch targets
grep -rn "width:\s*[0-3][0-9]px\|height:\s*[0-3][0-9]px" --include="*.css" src/

# Find images without alt text
grep -rn "<img" --include="*.tsx" --include="*.jsx" src/ | grep -v "alt="

# Find buttons without accessible labels
grep -rn "<button" --include="*.tsx" src/ | grep -v "aria-label\|>.*</"

# Find inputs without labels
grep -rn "<input" --include="*.tsx" src/ | grep -v "aria-label\|id="
```

---

### Phase 2: Screen Reader Support

**Goal**: Ensure VoiceOver and TalkBack can navigate and understand content

**ARIA Landmarks for Mobile:**

```html
<!-- Header with navigation -->
<header role="banner">
  <nav role="navigation" aria-label="Main navigation">
    <!-- Nav items -->
  </nav>
</header>

<!-- Main content -->
<main role="main">
  <h1>Page Title</h1>
  <!-- Content -->
</main>

<!-- Search -->
<div role="search">
  <label for="search">Search</label>
  <input type="search" id="search" />
</div>

<!-- Footer -->
<footer role="contentinfo">
  <!-- Footer content -->
</footer>
```

**Button Accessibility:**

```html
<!-- ❌ Bad - no label for icon-only button -->
<button>
  <svg><!-- icon --></svg>
</button>

<!-- ✅ Good - aria-label for screen readers -->
<button aria-label="Close dialog">
  <svg aria-hidden="true"><!-- icon --></svg>
</button>

<!-- ✅ Good - visually hidden text -->
<button>
  <svg aria-hidden="true"><!-- icon --></svg>
  <span class="visuallyHidden">Close dialog</span>
</button>
```

**Visually Hidden CSS:**

```css
.visuallyHidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}
```

**Form Accessibility:**

```html
<!-- ❌ Bad - placeholder is not a label -->
<input type="email" placeholder="Email address" />

<!-- ✅ Good - proper label association -->
<label for="email">Email address</label>
<input type="email" id="email" autocomplete="email" />

<!-- ✅ Good - error announcement -->
<label for="password">Password</label>
<input
  type="password"
  id="password"
  aria-invalid="true"
  aria-describedby="password-error"
/>
<div id="password-error" role="alert">
  Password must be at least 8 characters
</div>
```

---

### Phase 3: Focus Management

**Goal**: Proper focus handling for modals, sheets, and navigation

**Modal/Sheet Focus Management:**

```javascript
class AccessibleModal {
  constructor(modalElement) {
    this.modal = modalElement;
    this.focusableElements = null;
    this.previousFocus = null;
  }

  open() {
    // Store current focus
    this.previousFocus = document.activeElement;

    // Get all focusable elements in modal
    this.focusableElements = this.modal.querySelectorAll(
      'a[href], button:not([disabled]), textarea, input, select, [tabindex]:not([tabindex="-1"])'
    );

    // Focus first element
    if (this.focusableElements.length > 0) {
      this.focusableElements[0].focus();
    }

    // Trap focus within modal
    this.modal.addEventListener('keydown', this.trapFocus.bind(this));

    // Announce modal to screen readers
    this.modal.setAttribute('aria-modal', 'true');
    this.modal.setAttribute('role', 'dialog');
  }

  trapFocus(e) {
    if (e.key !== 'Tab') return;

    const firstElement = this.focusableElements[0];
    const lastElement = this.focusableElements[this.focusableElements.length - 1];

    if (e.shiftKey && document.activeElement === firstElement) {
      e.preventDefault();
      lastElement.focus();
    } else if (!e.shiftKey && document.activeElement === lastElement) {
      e.preventDefault();
      firstElement.focus();
    }
  }

  close() {
    this.modal.removeEventListener('keydown', this.trapFocus);

    // Return focus to trigger element
    if (this.previousFocus) {
      this.previousFocus.focus();
    }
  }
}
```

**Bottom Sheet Focus:**

```css
.bottomSheet {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--color-bg);
  border-radius: 16px 16px 0 0;
  padding: 24px;
  transform: translateY(100%);
  transition: transform 0.3s ease;
}

.bottomSheet.open {
  transform: translateY(0);
}

/* Focus indicator for keyboard users */
.bottomSheet *:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Hide focus outline for mouse users, show for keyboard */
.bottomSheet *:focus:not(:focus-visible) {
  outline: none;
}

.bottomSheet *:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```

---

### Phase 4: Live Regions & Announcements

**Goal**: Announce dynamic content changes to screen readers

**Toast/Snackbar Announcements:**

```html
<!-- Polite announcement - doesn't interrupt -->
<div role="status" aria-live="polite" aria-atomic="true" class="visuallyHidden">
  <!-- Announcement text injected here -->
</div>

<!-- Assertive announcement - interrupts immediately -->
<div role="alert" aria-live="assertive" aria-atomic="true" class="visuallyHidden">
  <!-- Error messages injected here -->
</div>
```

```javascript
function announce(message, priority = 'polite') {
  const liveRegion = document.querySelector(`[aria-live="${priority}"]`);

  // Clear and re-add to trigger announcement
  liveRegion.textContent = '';
  setTimeout(() => {
    liveRegion.textContent = message;
  }, 100);

  // Auto-clear after announcement
  setTimeout(() => {
    liveRegion.textContent = '';
  }, 5000);
}

// Usage
saveButton.addEventListener('click', async () => {
  await saveData();
  announce('Changes saved successfully', 'polite');
});

deleteButton.addEventListener('click', async () => {
  try {
    await deleteItem();
    announce('Item deleted', 'polite');
  } catch (error) {
    announce('Error: Could not delete item', 'assertive');
  }
});
```

**Loading States:**

```html
<!-- Loading button with status -->
<button
  aria-label="Save changes"
  aria-busy="true"
  disabled
>
  <span aria-hidden="true">
    <!-- Spinner icon -->
  </span>
  <span>Saving...</span>
</button>

<!-- Completed state -->
<button aria-label="Save changes">
  Save
</button>
```

**Dynamic Content:**

```html
<!-- List that updates -->
<ul role="list" aria-live="polite" aria-relevant="additions removals">
  <li>Item 1</li>
  <li>Item 2</li>
  <!-- New items announced automatically -->
</ul>

<!-- Pagination -->
<nav aria-label="Pagination">
  <button aria-label="Previous page" disabled>Previous</button>
  <span aria-current="page" aria-label="Page 1 of 5">1</span>
  <button aria-label="Next page, Page 2">Next</button>
</nav>
```

---

### Phase 5: VoiceOver/TalkBack Testing

**Goal**: Manual testing with actual screen readers

**VoiceOver Gestures (iOS):**
- Swipe right: Next item
- Swipe left: Previous item
- Double tap: Activate
- Three-finger swipe: Scroll
- Two-finger double tap: Magic Tap (primary action)
- Rotor: Two-finger rotation to change navigation mode

**TalkBack Gestures (Android):**
- Swipe right: Next item
- Swipe left: Previous item
- Double tap: Activate
- Swipe down then up: First item
- Swipe up then down: Last item
- Local context menu: Swipe up then right

**Testing Checklist:**

```markdown
### VoiceOver Testing (iOS)

- [ ] Can navigate through all interactive elements
- [ ] Button labels are descriptive ("Close" not "X")
- [ ] Form inputs announce their purpose and state
- [ ] Images have meaningful alt text (or aria-hidden if decorative)
- [ ] Modals trap focus and announce as dialogs
- [ ] Page title announces on navigation
- [ ] Headings create logical document outline
- [ ] Custom controls have appropriate ARIA roles
- [ ] Loading states announce to user
- [ ] Error messages are announced immediately
- [ ] Dynamic content updates are announced
- [ ] Can dismiss modals with swipe gestures
- [ ] Rotor navigation works (headings, links, form controls)

### TalkBack Testing (Android)

- [ ] All interactive elements are reachable
- [ ] Touch exploration works (drag finger to explore)
- [ ] Local context menu provides actions
- [ ] Swipe gestures navigate correctly
- [ ] Custom gestures have TalkBack equivalents
- [ ] Reading order matches visual order
- [ ] Lists announce item count
- [ ] Expandable sections announce state (expanded/collapsed)

### Switch Control Testing

- [ ] Can navigate with single switch
- [ ] All actions reachable via scanning
- [ ] Scanning speed is reasonable
- [ ] No focus traps for switch users
```

---

### Phase 6: Reduced Motion & Preferences

**Goal**: Respect user preferences for motion and accessibility

```css
/* Disable animations for users who prefer reduced motion */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }

  .pullToRefresh .refreshIndicator,
  .swipeableItem .swipeContent {
    transition: none !important;
  }
}

/* High contrast mode */
@media (prefers-contrast: high) {
  .button {
    border: 2px solid currentColor;
  }

  .card {
    border: 1px solid var(--color-text);
  }
}

/* Dark mode preference */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #121212;
    --color-text: #ffffff;
  }
}
```

---

## Mobile Accessibility Checklist

### Touch Targets
- [ ] All interactive elements ≥ 44x44px (WCAG AAA) or ≥ 48x48px (recommended)
- [ ] Adequate spacing between targets (8px minimum)
- [ ] Touch targets don't overlap

### Screen Reader Support
- [ ] All images have alt text (or aria-hidden if decorative)
- [ ] Icon-only buttons have aria-label
- [ ] Form inputs have associated labels
- [ ] Custom controls have appropriate ARIA roles
- [ ] Page landmarks (header, nav, main, footer) are defined
- [ ] Headings create logical document outline (h1 → h2 → h3)

### Focus Management
- [ ] Focus order matches visual order
- [ ] All interactive elements are keyboard accessible
- [ ] Focus indicators are clearly visible (2px outline minimum)
- [ ] Modals trap focus and return focus on close
- [ ] Skip links provided for navigation

### Live Regions
- [ ] Loading states announce with aria-busy or live region
- [ ] Success messages use aria-live="polite"
- [ ] Error messages use role="alert" or aria-live="assertive"
- [ ] Dynamic content updates are announced

### Forms
- [ ] All inputs have visible labels
- [ ] Required fields are indicated (not just color)
- [ ] Error messages are associated with inputs (aria-describedby)
- [ ] Validation errors are announced
- [ ] Autocomplete attributes for common fields

### Motion & Preferences
- [ ] Respects prefers-reduced-motion
- [ ] Animations can be paused or disabled
- [ ] Motion-triggered actions have static alternatives
- [ ] High contrast mode supported

### Mobile-Specific
- [ ] Content reflows to 320px without horizontal scroll
- [ ] Works in portrait and landscape orientation
- [ ] No pinch-to-zoom disabled (allow zoom)
- [ ] Text can be resized to 200% without loss of content

---

## Output Format

```markdown
## Mobile Accessibility Audit Results

### Critical Issues (WCAG Level A)
- [ ] **Touch Target Too Small** - Button at `[selector]` is 32x32px (requires 44x44px)
- [ ] **Missing Label** - Input at `[selector]` has no associated label
- [ ] **Focus Trap** - Modal does not return focus on close

### Important Issues (WCAG Level AA)
- [ ] **Insufficient Contrast** - Text on background is 3.2:1 (requires 4.5:1)
- [ ] **Missing Landmark** - Page missing main landmark

### Enhancements (WCAG Level AAA)
- [ ] **Touch Target Enhancement** - Increase to 48x48px for better usability
- [ ] **Enhanced Announcements** - Add more descriptive loading states

### Files Modified
- `[filepath]` - Touch target fixes
- `[filepath]` - ARIA labels and landmarks
- `[filepath]` - Focus management
- `[filepath]` - Live region announcements

### Testing Notes
**VoiceOver (iOS):**
- Navigation works correctly through all elements
- Buttons announce purpose clearly
- Modal focus trapping works

**TalkBack (Android):**
- All elements reachable via swipe
- Local context menu provides expected actions
- Reading order matches visual layout

### Checklist Results
✅ Touch targets ≥ 44px
✅ Screen reader labels present
✅ Focus management implemented
✅ Live regions for dynamic content
✅ Reduced motion respected
⚠️ High contrast mode needs testing
```

---

## Integration with Other Skills

- **/mobile-patterns** - Ensure navigation patterns are accessible
- **/touch-interactions** - Verify gestures have keyboard alternatives
- **/component-states** - Add accessible focus and disabled states
- **/accessibility-audit** - General accessibility (this skill is mobile-focused)

---

## Notes

- Test with actual screen readers on real devices - simulators don't fully replicate experience
- VoiceOver and TalkBack have different behaviors - test both
- Touch target size is the #1 mobile accessibility issue
- Don't rely on color alone to convey information
- Keep forms short and use appropriate input types for mobile keyboards
- Respect user preferences (reduced motion, dark mode, high contrast)
- Live regions should be in DOM from page load, not dynamically added
