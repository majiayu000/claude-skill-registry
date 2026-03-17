---
name: touch-interactions
description: Implement touch-friendly interactions including proper target sizing, swipe gestures, pull-to-refresh, long-press menus, and haptic feedback patterns.
---

# Touch Interactions Skill

Add comprehensive touch interaction patterns to create responsive, gesture-driven mobile interfaces with proper target sizing and visual feedback.

## When to Use

Use `/touch-interactions` when you need to:
- Audit and fix touch target sizes (< 48px)
- Implement swipe actions (delete, archive, mark complete)
- Add pull-to-refresh functionality
- Create long-press context menus
- Implement drag-to-reorder lists
- Add touch-specific visual feedback (ripples, scale, haptics)

## Instructions

### Phase 1: Audit Touch Target Sizes

**Goal**: Identify interactive elements that are too small for comfortable touch

**Minimum Touch Target Standards:**
- **WCAG 2.1 Level AA**: 44x44 CSS pixels
- **WCAG 2.5.5 Level AAA**: 44x44 CSS pixels (same)
- **iOS HIG**: 44x44 points minimum
- **Material Design**: 48x48 dp minimum
- **Recommended**: 48x48px for web to be safe across platforms

**I will:**
1. Search for interactive elements (buttons, links, inputs, custom controls)
2. Check computed dimensions in CSS
3. Flag any elements < 48x48px
4. Prioritize fixes by usage frequency

**Common violations:**
```css
/* ❌ Too small */
.iconButton {
  width: 32px;
  height: 32px;
  padding: 0;
}

/* ✅ Correct - 48px minimum */
.iconButton {
  width: 48px;
  height: 48px;
  padding: 12px; /* Icon itself can be 24px */
}

/* ✅ Alternative - smaller visual with larger hit area */
.iconButton {
  width: 24px; /* Visual size */
  height: 24px;
  padding: 12px; /* Adds to hit area = 48x48 total */
}
```

**Audit bash command:**
```bash
# Find potentially small interactive elements in CSS
grep -rn "width:\s*[0-3][0-9]px\|height:\s*[0-3][0-9]px" --include="*.css" --include="*.module.css" src/
```

---

### Phase 2: Implement Swipe Actions

**Goal**: Add swipeable list items with action reveal

**Swipeable List Item Pattern:**

```css
.swipeableItem {
  position: relative;
  overflow: hidden;
  touch-action: pan-y; /* Allow vertical scroll, prevent horizontal browser gestures */
}

.swipeContent {
  position: relative;
  background: var(--color-bg);
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1;
}

.swipeActions {
  position: absolute;
  top: 0;
  right: 0;
  bottom: 0;
  display: flex;
  z-index: 0;
}

.swipeAction {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 80px;
  min-height: 48px;
  color: white;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: width 0.2s ease;
}

.swipeAction.delete {
  background: var(--color-error, #ef4444);
}

.swipeAction.archive {
  background: var(--color-warning, #f59e0b);
}

.swipeAction.complete {
  background: var(--color-success, #10b981);
}

/* Expanded state when swiped */
.swipeableItem.swiped .swipeContent {
  transform: translateX(-160px); /* Show 2 actions */
}

/* Delete confirmation - full width swipe */
.swipeableItem.swipedFull .swipeContent {
  transform: translateX(-100%);
}

.swipeableItem.swipedFull .swipeAction.delete {
  width: 100%;
}
```

**JavaScript touch handling:**

```javascript
// Basic swipe detection
let touchStartX = 0;
let touchCurrentX = 0;
let isSwiping = false;

element.addEventListener('touchstart', (e) => {
  touchStartX = e.touches[0].clientX;
  isSwiping = true;
});

element.addEventListener('touchmove', (e) => {
  if (!isSwiping) return;

  touchCurrentX = e.touches[0].clientX;
  const diff = touchStartX - touchCurrentX;

  if (diff > 0) { // Swipe left
    const translateX = Math.min(diff, 160); // Max 160px
    content.style.transform = `translateX(-${translateX}px)`;
  }
});

element.addEventListener('touchend', () => {
  const diff = touchStartX - touchCurrentX;

  if (diff > 80) { // Threshold for showing actions
    element.classList.add('swiped');
  } else {
    element.classList.remove('swiped');
    content.style.transform = '';
  }

  isSwiping = false;
});
```

---

### Phase 3: Implement Pull-to-Refresh

**Goal**: Add native-feeling pull-to-refresh with spring physics

**Pull-to-Refresh Pattern:**

```css
.pullToRefresh {
  position: relative;
  overflow: auto;
  -webkit-overflow-scrolling: touch;
}

.refreshIndicator {
  position: absolute;
  top: -60px;
  left: 50%;
  transform: translateX(-50%);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.pullToRefresh.pulling .refreshIndicator {
  transform: translateX(-50%) translateY(60px);
}

.pullToRefresh.refreshing .refreshIndicator {
  transform: translateX(-50%) translateY(60px);
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: translateX(-50%) translateY(60px) rotate(0deg); }
  to { transform: translateX(-50%) translateY(60px) rotate(360deg); }
}

.refreshIcon {
  width: 24px;
  height: 24px;
  color: var(--color-text-secondary);
}
```

**JavaScript implementation:**

```javascript
let startY = 0;
let currentY = 0;
let isPulling = false;

const container = document.querySelector('.pullToRefresh');

container.addEventListener('touchstart', (e) => {
  if (container.scrollTop === 0) { // Only at top of scroll
    startY = e.touches[0].clientY;
    isPulling = true;
  }
});

container.addEventListener('touchmove', (e) => {
  if (!isPulling) return;

  currentY = e.touches[0].clientY;
  const pullDistance = currentY - startY;

  if (pullDistance > 0 && pullDistance < 100) {
    e.preventDefault(); // Prevent default scroll
    container.classList.add('pulling');
    // Optional: rotate icon based on pull distance
    const rotation = (pullDistance / 100) * 360;
    indicator.style.transform = `rotate(${rotation}deg)`;
  }
});

container.addEventListener('touchend', () => {
  if (!isPulling) return;

  const pullDistance = currentY - startY;

  if (pullDistance > 60) { // Threshold to trigger refresh
    container.classList.add('refreshing');
    container.classList.remove('pulling');

    // Trigger refresh action
    onRefresh().then(() => {
      container.classList.remove('refreshing');
    });
  } else {
    container.classList.remove('pulling');
  }

  isPulling = false;
});
```

---

### Phase 4: Add Touch Feedback

**Goal**: Provide immediate visual and haptic feedback for touch interactions

**Ripple Effect Pattern:**

```css
.touchable {
  position: relative;
  overflow: hidden;
  -webkit-tap-highlight-color: transparent;
}

.ripple {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.3);
  transform: scale(0);
  animation: ripple 0.6s ease-out;
  pointer-events: none;
}

@keyframes ripple {
  to {
    transform: scale(4);
    opacity: 0;
  }
}
```

```javascript
function createRipple(e) {
  const button = e.currentTarget;
  const ripple = document.createElement('span');
  const rect = button.getBoundingClientRect();
  const size = Math.max(rect.width, rect.height);
  const x = e.clientX - rect.left - size / 2;
  const y = e.clientY - rect.top - size / 2;

  ripple.classList.add('ripple');
  ripple.style.width = ripple.style.height = `${size}px`;
  ripple.style.left = `${x}px`;
  ripple.style.top = `${y}px`;

  button.appendChild(ripple);

  setTimeout(() => ripple.remove(), 600);
}

document.querySelectorAll('.touchable').forEach(button => {
  button.addEventListener('click', createRipple);
});
```

**Scale Feedback Pattern:**

```css
.scaleButton {
  transition: transform 0.1s ease;
  -webkit-tap-highlight-color: transparent;
}

.scaleButton:active {
  transform: scale(0.95);
}

/* For important primary actions */
.scaleButton.primary:active {
  transform: scale(0.98); /* Subtle scale for larger buttons */
}
```

**Haptic Feedback (Web Vibration API):**

```javascript
function hapticFeedback(type = 'light') {
  if (!navigator.vibrate) return;

  const patterns = {
    light: 10,
    medium: 20,
    heavy: 30,
    success: [10, 50, 10],
    error: [20, 100, 20, 100, 20],
    warning: [15, 75, 15]
  };

  navigator.vibrate(patterns[type]);
}

// Usage
deleteButton.addEventListener('click', () => {
  hapticFeedback('warning');
  // ... delete logic
});

completeButton.addEventListener('click', () => {
  hapticFeedback('success');
  // ... completion logic
});
```

---

### Phase 5: Long-Press Context Menu

**Goal**: Implement long-press to show context actions

```css
.contextMenu {
  position: fixed;
  background: var(--color-bg-elevated);
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
  padding: 8px 0;
  min-width: 200px;
  opacity: 0;
  transform: scale(0.9);
  transition: opacity 0.2s ease, transform 0.2s ease;
  pointer-events: none;
  z-index: 9999;
}

.contextMenu.visible {
  opacity: 1;
  transform: scale(1);
  pointer-events: auto;
}

.contextMenuItem {
  display: flex;
  align-items: center;
  gap: 12px;
  min-height: 48px;
  padding: 12px 16px;
  color: var(--color-text);
  background: none;
  border: none;
  width: 100%;
  text-align: left;
  font-size: 16px;
  transition: background 0.15s ease;
}

.contextMenuItem:active {
  background: var(--color-bg-hover);
}

.contextMenuItem.destructive {
  color: var(--color-error);
}
```

```javascript
let longPressTimer;
const LONG_PRESS_DURATION = 500; // 500ms

element.addEventListener('touchstart', (e) => {
  const touch = e.touches[0];
  const x = touch.clientX;
  const y = touch.clientY;

  longPressTimer = setTimeout(() => {
    hapticFeedback('medium');
    showContextMenu(x, y);
  }, LONG_PRESS_DURATION);
});

element.addEventListener('touchmove', () => {
  clearTimeout(longPressTimer);
});

element.addEventListener('touchend', () => {
  clearTimeout(longPressTimer);
});

function showContextMenu(x, y) {
  const menu = document.querySelector('.contextMenu');
  menu.style.left = `${x}px`;
  menu.style.top = `${y}px`;
  menu.classList.add('visible');

  // Close on outside tap
  document.addEventListener('click', () => {
    menu.classList.remove('visible');
  }, { once: true });
}
```

---

### Phase 6: Drag-to-Reorder

**Goal**: Enable touch-based list reordering

```css
.draggableList {
  position: relative;
}

.draggableItem {
  position: relative;
  background: var(--color-bg);
  border-radius: 8px;
  margin-bottom: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  touch-action: none; /* Prevent scroll during drag */
}

.draggableItem.dragging {
  z-index: 1000;
  transform: scale(1.05) rotate(2deg);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  opacity: 0.9;
}

.dragHandle {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-secondary);
  cursor: grab;
  touch-action: none;
}

.dragHandle:active {
  cursor: grabbing;
}
```

```javascript
let draggedElement = null;
let startY = 0;
let currentY = 0;

handle.addEventListener('touchstart', (e) => {
  draggedElement = e.target.closest('.draggableItem');
  startY = e.touches[0].clientY;
  draggedElement.classList.add('dragging');
  hapticFeedback('light');
});

document.addEventListener('touchmove', (e) => {
  if (!draggedElement) return;

  currentY = e.touches[0].clientY;
  const diff = currentY - startY;
  draggedElement.style.transform = `translateY(${diff}px) scale(1.05) rotate(2deg)`;

  // Check for reorder position
  const siblings = Array.from(draggedElement.parentElement.children);
  const targetElement = siblings.find(sibling => {
    if (sibling === draggedElement) return false;
    const rect = sibling.getBoundingClientRect();
    return currentY > rect.top && currentY < rect.bottom;
  });

  if (targetElement) {
    hapticFeedback('light');
    // Insert before/after logic
  }
});

document.addEventListener('touchend', () => {
  if (!draggedElement) return;

  draggedElement.classList.remove('dragging');
  draggedElement.style.transform = '';
  hapticFeedback('medium');
  draggedElement = null;
});
```

---

## Touch Interaction Checklist

Before completing this skill, verify:

### Touch Targets
- [ ] All interactive elements are ≥ 48x48px
- [ ] Icon buttons have adequate padding (visual can be smaller)
- [ ] Link text has sufficient line-height for touch
- [ ] Form inputs have large enough tap targets

### Gesture Implementation
- [ ] Swipe actions are discoverable (hint animation or tutorial)
- [ ] Swipe threshold is comfortable (not too sensitive)
- [ ] Actions can be canceled by swiping back
- [ ] Pull-to-refresh only triggers at top of scroll

### Visual Feedback
- [ ] All touches have immediate visual response
- [ ] Active states are clearly visible
- [ ] Ripple effects don't overflow container
- [ ] Scale animations are subtle (< 10% change)

### Haptic Feedback
- [ ] Haptics enhance but don't replace visual feedback
- [ ] Error actions use appropriate vibration pattern
- [ ] Haptics respect user preferences (when API available)
- [ ] Vibration is not excessive

### Performance
- [ ] Touch handlers use passive event listeners where possible
- [ ] Animations use transform and opacity (GPU-accelerated)
- [ ] No layout thrashing during drag/swipe
- [ ] 60fps maintained during interactions

### Accessibility
- [ ] Touch interactions have keyboard equivalents
- [ ] Screen readers announce action availability
- [ ] Focus indicators visible for keyboard users
- [ ] Long-press duration is not too long (< 600ms)

---

## Output Format

```markdown
## Touch Interaction Audit & Implementation

### Touch Target Audit Results
**Violations Found**: [number]
- `[selector]` - [current size] → [fixed size]
- `[selector]` - [current size] → [fixed size]

### Gestures Implemented
1. **Swipe Actions** - Delete, archive on list items
2. **Pull-to-Refresh** - Main content feed
3. **Long-Press Menu** - Context actions on cards
4. **Drag-to-Reorder** - Task list items

### Visual Feedback Added
- Ripple effects on all buttons
- Scale feedback on primary actions
- Haptic feedback on destructive actions

### Files Modified
- `[filepath]` - Touch target fixes
- `[filepath]` - Swipe implementation
- `[filepath]` - Touch feedback styles

### Checklist Results
✅ All targets ≥ 48px
✅ Gestures are discoverable
✅ Immediate visual feedback
✅ 60fps maintained
✅ Keyboard equivalents provided
```

---

## Integration with Other Skills

- **/mobile-patterns** - Combine with mobile navigation for complete mobile UX
- **/mobile-accessibility** - Ensure touch interactions work with screen readers
- **/component-states** - Add proper states to touch-enabled components
- **/micro-interactions** - Polish touch feedback with refined animations

---

## Notes

- Always test on actual mobile devices - desktop touch simulation misses nuances
- iOS and Android have different touch behaviors - test both
- `touch-action: none` prevents default browser gestures but may affect accessibility
- Haptic feedback is progressive enhancement - not all devices support it
- Consider reduced motion preferences for animation-heavy touch feedback
- Swipe gestures should have visual hints for discoverability
