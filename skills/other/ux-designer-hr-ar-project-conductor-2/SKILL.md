---
name: ux-designer
description: Perfect UX/UI designer that eliminates bugs, improves usability, and ensures flawless user experience. Use when user mentions "perfect the UI", "fix UX bugs", "improve demo", or "make it flawless".
version: 1.0.0
agents: [codex-deep-research, gemini-research-analyst]
---

# UX Designer - Perfection-Focused UI/UX Skill

**Goal: Zero bugs, perfect usability, flawless user experience.**

## When to Use

Invoke this skill when:
- User mentions: "perfect the demo", "fix UX bugs", "make it flawless"
- UI has inconsistencies or bugs
- User experience is confusing or broken
- Demo has visual issues
- Interactive elements don't work properly

## UX Perfection Methodology

### Phase 1: Comprehensive UX Audit

**1A. Visual Inspection**
```bash
# Check all HTML files for common issues
find public -name "*.html" -type f

# For each file, check:
- Broken links (404s)
- Missing images
- JavaScript errors in console
- CSS rendering issues
- Responsive design breakpoints
- Color contrast (accessibility)
- Typography consistency
```

**1B. Interaction Testing**
```markdown
Test every interactive element:
- [ ] Buttons: Click response, hover states, disabled states
- [ ] Forms: Validation, error messages, success states
- [ ] Navigation: All links work, breadcrumbs accurate
- [ ] Modals: Open/close, backdrop click, ESC key
- [ ] Dropdowns: Open/close, keyboard navigation
- [ ] Tables: Sorting, filtering, pagination
- [ ] Real-time updates: WebSocket connection, live data
- [ ] Loading states: Spinners, skeletons, placeholders
```

**1C. User Flow Analysis**
```markdown
Map critical user journeys:
1. New user onboarding → Should be intuitive, max 3 steps
2. Core feature usage → Should be discoverable, max 2 clicks
3. Error recovery → Clear error messages, obvious next steps
4. Success confirmation → Visible feedback, celebratory if appropriate
```

### Phase 2: Research Best Practices

**Launch codex-deep-research agent**:
```markdown
Invoke Task tool with subagent_type="codex-deep-research"

Prompt:
"Research the best UX/UI practices for interactive demos and dashboards.

Context:
- Project Conductor is a workflow orchestration platform
- Demo showcases 7-module workflow (Onboarding → Implementation)
- Tech: HTML, CSS, JavaScript (vanilla), Socket.io
- Users: Product managers, engineers, stakeholders

Provide best practices for:
1. **Demo UX Patterns**
   - Interactive tutorials vs guided tours
   - Progress indicators
   - Contextual help
   - Error handling in demos

2. **Dashboard Design**
   - Card layouts
   - Data visualization
   - Real-time updates (WebSocket)
   - Empty states
   - Loading states

3. **Navigation**
   - Module-to-module flow
   - Breadcrumbs
   - Back button behavior
   - Deep linking

4. **Accessibility**
   - Keyboard navigation
   - Screen reader support
   - Focus management
   - ARIA labels

5. **Performance**
   - Perceived performance
   - Lazy loading
   - Animation frame rate
   - Memory leaks

6. **Error Handling**
   - User-friendly error messages
   - Recovery actions
   - Fallback UI
   - Offline behavior

Provide specific code examples and visual patterns."
```

**Check for AI-powered UX tools**:
```markdown
Invoke Task tool with subagent_type="gemini-research-analyst"

Prompt:
"Research if Google's Gemini AI provides any UX design, usability testing, or UI generation tools.

Investigate:
1. Gemini-powered UX analysis tools
2. Automated accessibility testing
3. UI component generation
4. User flow optimization
5. A/B testing recommendations
6. Heatmap analysis tools

If available, explain how to integrate with HTML/JS demos."
```

### Phase 3: Bug Hunting (Zero Tolerance)

**3A. Console Error Check**
```javascript
// Check browser console for errors
// Common issues:
- Uncaught ReferenceError (missing variables)
- Uncaught TypeError (null/undefined access)
- Failed to fetch (broken API calls)
- WebSocket connection failed
- CORS errors
- 404 for assets (images, CSS, JS)
```

**3B. Network Tab Analysis**
```markdown
Check Network tab for:
- [ ] All resources load successfully (no 404s)
- [ ] API endpoints respond <200ms
- [ ] WebSocket connection established
- [ ] No unnecessary requests (optimize)
- [ ] Proper caching headers
- [ ] Compressed assets (gzip)
```

**3C. Responsive Design Testing**
```bash
# Test breakpoints
- Mobile: 320px, 375px, 414px
- Tablet: 768px, 1024px
- Desktop: 1280px, 1440px, 1920px

# Check for:
- Horizontal scroll (should be none)
- Text overflow
- Image scaling
- Button touch targets (min 44x44px)
- Readable font sizes (min 16px)
```

**3D. Cross-Browser Testing**
```markdown
Test in:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

Check for:
- CSS compatibility (flexbox, grid)
- JavaScript APIs (fetch, WebSocket)
- Event handlers (click, keyboard)
- CSS animations
```

### Phase 4: Usability Improvements

**4A. First-Time User Experience**
```markdown
Checklist:
- [ ] Clear value proposition (what is this?)
- [ ] Obvious starting point (where do I begin?)
- [ ] Contextual help (tooltips, hints)
- [ ] Progress indicators (how far have I gone?)
- [ ] Success feedback (I completed something!)
- [ ] Error prevention (guard rails)
- [ ] Easy recovery (undo, reset)
```

**4B. Visual Hierarchy**
```css
/* Apply visual hierarchy principles */
- Primary actions: Bold, high contrast, larger
- Secondary actions: Less prominent
- Tertiary actions: Text links, subtle
- Destructive actions: Red, confirmation required
- Disabled states: Greyed out, not clickable

/* Example */
.btn-primary {
  background: #007bff;
  color: white;
  font-weight: 600;
  padding: 12px 24px;
  font-size: 16px;
}

.btn-secondary {
  background: transparent;
  border: 1px solid #6c757d;
  color: #6c757d;
  padding: 10px 20px;
  font-size: 14px;
}
```

**4C. Feedback & Confirmation**
```javascript
// Every user action needs feedback
function handleAction(action) {
  // 1. Immediate feedback (button state)
  button.disabled = true;
  button.textContent = 'Processing...';

  // 2. Action execution
  await performAction(action);

  // 3. Success feedback
  showToast('✅ Action completed successfully!', 'success');
  button.disabled = false;
  button.textContent = 'Done';

  // 4. Update UI to reflect change
  refreshData();
}

// Toast notification system
function showToast(message, type = 'info', duration = 3000) {
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.classList.add('fade-out');
    setTimeout(() => toast.remove(), 300);
  }, duration);
}
```

**4D. Error Handling (User-Friendly)**
```javascript
// Bad: Generic error
catch (error) {
  alert('Error');
}

// Good: Helpful error with action
catch (error) {
  showError({
    title: 'Unable to Load Projects',
    message: 'We couldn\'t connect to the server. Please check your internet connection and try again.',
    actions: [
      { label: 'Retry', onClick: () => retryLoad() },
      { label: 'Go Back', onClick: () => history.back() }
    ],
    icon: '🔌'
  });

  // Log detailed error for debugging
  console.error('Project load failed:', error);
}
```

### Phase 5: Accessibility Perfection

**5A. Keyboard Navigation**
```javascript
// Ensure all interactive elements are keyboard accessible
document.querySelectorAll('button, a, input, select, textarea').forEach(el => {
  // Add focus visible styles
  el.addEventListener('focus', (e) => {
    e.target.classList.add('focus-visible');
  });

  // Support Enter/Space on custom buttons
  if (el.getAttribute('role') === 'button') {
    el.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        el.click();
      }
    });
  }
});

// Trap focus in modals
function trapFocus(modal) {
  const focusableElements = modal.querySelectorAll(
    'a[href], button, textarea, input, select, [tabindex]:not([tabindex="-1"])'
  );
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  modal.addEventListener('keydown', (e) => {
    if (e.key === 'Tab') {
      if (e.shiftKey && document.activeElement === firstElement) {
        e.preventDefault();
        lastElement.focus();
      } else if (!e.shiftKey && document.activeElement === lastElement) {
        e.preventDefault();
        firstElement.focus();
      }
    } else if (e.key === 'Escape') {
      closeModal();
    }
  });
}
```

**5B. ARIA Labels**
```html
<!-- Bad: No context for screen readers -->
<button onclick="save()">
  <svg>...</svg>
</button>

<!-- Good: Descriptive label -->
<button onclick="save()" aria-label="Save project changes">
  <svg aria-hidden="true">...</svg>
</button>

<!-- Dynamic content -->
<div role="status" aria-live="polite" aria-atomic="true">
  <span id="status-message">Loading projects...</span>
</div>

<!-- Form validation -->
<input
  type="email"
  id="email"
  aria-describedby="email-error"
  aria-invalid="true"
>
<span id="email-error" role="alert">
  Please enter a valid email address
</span>
```

**5C. Color Contrast Check**
```javascript
// Ensure WCAG AA compliance (4.5:1 for normal text, 3:1 for large)
// Use tools: Chrome DevTools Lighthouse, axe DevTools

// Example: Check programmatically
function checkContrast(foreground, background) {
  const ratio = getContrastRatio(foreground, background);
  return {
    passAA: ratio >= 4.5,
    passAAA: ratio >= 7,
    ratio: ratio.toFixed(2)
  };
}

// Fix: Increase contrast
/* Before */
.text-muted { color: #999; } /* 2.8:1 - FAILS */

/* After */
.text-muted { color: #6c757d; } /* 4.5:1 - PASSES */
```

### Phase 6: Performance Optimization

**6A. Perceived Performance**
```javascript
// Instant feedback, lazy load heavy content
async function loadDashboard() {
  // 1. Show skeleton immediately (0ms)
  showSkeleton();

  // 2. Load critical data first (100ms)
  const criticalData = await fetchCritical();
  renderCritical(criticalData);
  hideSkeleton();

  // 3. Load secondary data (background)
  fetchSecondary().then(renderSecondary);

  // 4. Prefetch likely next page
  prefetchNextPage();
}

// Skeleton UI
function showSkeleton() {
  const skeleton = `
    <div class="skeleton-card">
      <div class="skeleton-line skeleton-title"></div>
      <div class="skeleton-line"></div>
      <div class="skeleton-line"></div>
    </div>
  `;
  container.innerHTML = skeleton.repeat(6);
}
```

**6B. Animation Performance**
```css
/* Bad: Causes layout thrashing */
.animate-bad {
  animation: slide-in 0.3s ease;
}
@keyframes slide-in {
  from { margin-left: -100px; }
  to { margin-left: 0; }
}

/* Good: GPU-accelerated */
.animate-good {
  animation: slide-in 0.3s ease;
}
@keyframes slide-in {
  from { transform: translateX(-100px); }
  to { transform: translateX(0); }
}

/* Use will-change for complex animations */
.will-animate {
  will-change: transform, opacity;
}
```

**6C. Memory Leak Prevention**
```javascript
// Bad: Event listeners not cleaned up
socket.on('update', handleUpdate);

// Good: Clean up on unmount
const listeners = [];

function addListener(event, handler) {
  socket.on(event, handler);
  listeners.push({ event, handler });
}

function cleanup() {
  listeners.forEach(({ event, handler }) => {
    socket.off(event, handler);
  });
  listeners.length = 0;
}

// Call cleanup when leaving page
window.addEventListener('beforeunload', cleanup);
```

### Phase 7: Final Polish

**7A. Micro-interactions**
```css
/* Smooth button interactions */
button {
  transition: all 0.2s ease;
  transform: scale(1);
}

button:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 8px rgba(0,0,0,0.2);
}

button:active {
  transform: scale(0.98);
}

/* Loading spinner */
@keyframes spin {
  to { transform: rotate(360deg); }
}

.spinner {
  animation: spin 1s linear infinite;
}
```

**7B. Empty States**
```html
<!-- Instead of blank screen -->
<div class="empty-state">
  <svg class="empty-icon"><!-- Icon --></svg>
  <h3>No projects yet</h3>
  <p>Create your first project to get started</p>
  <button class="btn-primary">Create Project</button>
</div>
```

**7C. Consistency Check**
```markdown
Ensure consistency across:
- [ ] Button styles (primary, secondary, danger)
- [ ] Spacing (use 8px grid: 8, 16, 24, 32, 48, 64)
- [ ] Typography (max 3 font sizes, consistent weights)
- [ ] Colors (stick to design system palette)
- [ ] Icons (same style, size, stroke width)
- [ ] Shadows (consistent elevation levels)
- [ ] Border radius (consistent rounding)
- [ ] Animations (consistent timing, easing)
```

## Validation Checklist

Before marking UX as "perfect":

### Functionality
- [ ] All buttons work (no broken onClick handlers)
- [ ] All links go to correct destinations
- [ ] Forms validate properly
- [ ] API calls succeed
- [ ] WebSocket connects and receives updates
- [ ] Error states display correctly
- [ ] Success states display correctly
- [ ] Loading states show during async operations

### Visual
- [ ] No layout shift (CLS score <0.1)
- [ ] No horizontal scroll
- [ ] Consistent spacing
- [ ] Consistent typography
- [ ] High color contrast (WCAG AA)
- [ ] Icons are clear and consistent
- [ ] Images load correctly
- [ ] No visual bugs (overlapping, cutoff text)

### Usability
- [ ] Clear navigation
- [ ] Obvious primary actions
- [ ] Helpful error messages
- [ ] Success confirmation
- [ ] Undo/cancel available
- [ ] Keyboard accessible
- [ ] Screen reader compatible
- [ ] Mobile responsive (320px - 1920px)

### Performance
- [ ] Page load <2s
- [ ] API calls <200ms
- [ ] Smooth animations (60fps)
- [ ] No memory leaks
- [ ] Efficient rendering (no jank)

### Browser Compatibility
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

## Demo-Specific Checks

For Project Conductor demo:

### Module Navigation
```bash
# Test all module transitions
Module 0 (Onboarding) → Module 1 (Dashboard)
Module 1 (Dashboard) → Module 2 (BRD)
Module 2 (BRD) → Module 3 (PRD)
Module 3 (PRD) → Module 4 (Engineering Design)
Module 4 (Engineering Design) → Module 5 (Conflicts)
Module 5 (Conflicts) → Module 6 (Implementation)
Module 6 (Implementation) → Module 1 (Dashboard)

# Check:
- [ ] All links work
- [ ] Navigation breadcrumbs update
- [ ] Back button works
- [ ] State persists (if applicable)
```

### Real-Time Features
```javascript
// Test WebSocket functionality
- [ ] Connection establishes on page load
- [ ] Live updates appear without refresh
- [ ] Multiple tabs stay in sync
- [ ] Reconnects after disconnect
- [ ] Shows offline indicator if disconnected
- [ ] No duplicate updates
```

### Data Display
```markdown
- [ ] Projects list loads correctly
- [ ] Requirements display properly
- [ ] Status badges show correct colors
- [ ] Progress bars update in real-time
- [ ] Filters work correctly
- [ ] Sorting works correctly
- [ ] Pagination works correctly
- [ ] Search works correctly
```

## Output Format

After UX audit, provide:

```markdown
## UX Audit Report

**Status**: [PERFECT ✅ / NEEDS FIXES ⚠️ / CRITICAL ISSUES ❌]

### Issues Found

#### Critical (Must Fix) 🔴
1. [Issue description]
   - Impact: [How this affects users]
   - Fix: [Specific code changes needed]
   - File: [path/to/file.html]
   - Line: [line number]

#### Important (Should Fix) 🟡
1. [Issue description]
   - Impact: [How this affects users]
   - Fix: [Specific code changes needed]

#### Nice to Have (Polish) 🟢
1. [Issue description]
   - Enhancement: [How this improves UX]
   - Suggestion: [Code example]

### UX Score

- Functionality: [X/10]
- Visual Design: [X/10]
- Usability: [X/10]
- Accessibility: [X/10]
- Performance: [X/10]

**Overall**: [X/50] - [Grade: A+ to F]

### Next Steps

1. Fix critical issues first
2. Implement important fixes
3. Add polish enhancements
4. Re-test all flows
5. Final validation

### Code Fixes

[Provide specific code changes with file paths and line numbers]
```

## Example Usage

User: "Make sure the demo is perfect"

This skill will:
1. Audit all demo HTML files
2. Test every interactive element
3. Research best UX practices
4. Find and document all bugs
5. Provide specific fixes with code
6. Validate accessibility
7. Check performance
8. Test across browsers
9. Generate comprehensive report
10. Implement fixes if requested
