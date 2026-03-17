---
description: Use this skill when the user writes/edits components, asks to "fix accessibility issues", "add ARIA labels", "improve accessibility", "check WCAG compliance", "remediate a11y violations", mentions "screen reader support", "keyboard navigation", or wants AI-powered accessibility fixes with one-click application. Automatically analyzes components for a11y issues and suggests context-aware fixes. Trigger on PostToolUse hook or explicit request.
---

# Accessibility Remediation Skill

## Overview

Automatically detect and fix accessibility issues in components with AI-powered analysis, context-aware fix suggestions, and one-click application. Goes beyond detection to provide ranked remediation options based on WCAG 2.2 best practices.

This skill transforms accessibility from a manual checklist into an automated workflow with intelligent fix suggestions.

## What This Skill Provides

### Real-Time Accessibility Analysis
Automatically check components for WCAG 2.2 violations:
- **Missing accessible names**: Buttons, links, form inputs
- **Color contrast**: WCAG AA (4.5:1) and AAA (7:1) compliance
- **Keyboard navigation**: Focus management, tab order
- **ARIA usage**: Proper roles, labels, live regions
- **Semantic HTML**: Use of proper HTML5 elements
- **Form accessibility**: Labels, error messages, validation

### Context-Aware Fix Suggestions
AI understands component purpose and suggests appropriate fixes:
- **Ranked by best practice**: Best → Good → Acceptable
- **Explains trade-offs**: Pros and cons of each approach
- **Considers context**: Close button vs Submit button vs generic action
- **Provides code**: Ready-to-apply fix snippets
- **Educational**: Explains why each fix works

### One-Click Application
Apply fixes instantly without manual implementation:
- **Auto-detection**: Triggers on component creation/edit
- **Interactive prompts**: Choose from ranked suggestions
- **Automatic application**: Updates component code
- **Verification**: Confirms fix resolves issue
- **Learning system**: Remembers user preferences

### WCAG 2.2 Compliance
Built-in support for latest accessibility standards:
- **Level A**: Essential accessibility (mandatory)
- **Level AA**: Recommended compliance (standard)
- **Level AAA**: Enhanced accessibility (optional)
- **ARIA 1.2**: Latest ARIA patterns and practices
- **Section 508**: US federal compliance

## How It Works

### Automatic Detection (PostToolUse Hook)

When you create or edit a component, the accessibility-auditor agent automatically:

1. **Parses component code** (JSX/TSX/Vue/Svelte)
2. **Analyzes for violations** using WCAG 2.2 rules
3. **Generates fix suggestions** ranked by best practice
4. **Presents options** for user selection
5. **Applies chosen fix** and verifies success

### Manual Invocation

You can also explicitly request accessibility analysis:

```bash
User: "Check this Button component for accessibility issues"
Claude: [Runs accessibility-auditor agent]

User: "Fix the accessibility violations in Modal.tsx"
Claude: [Analyzes, suggests fixes, applies selected fix]
```

## Common Accessibility Issues & Fixes

### Issue 1: Missing Accessible Name

**Problem:** Buttons, links, or inputs without labels

**Examples:**

```tsx
// ❌ Bad: Button has no accessible name
<button onClick={handleClose}>×</button>

// ✅ Fix Option 1: Visible text with icon (BEST)
<button onClick={handleClose}>
  <span aria-hidden="true">×</span>
  <span className="sr-only">Close dialog</span>
</button>

// ✅ Fix Option 2: aria-label (GOOD)
<button onClick={handleClose} aria-label="Close dialog">×</button>

// ✅ Fix Option 3: title attribute (ACCEPTABLE)
<button onClick={handleClose} title="Close dialog">×</button>
```

**AI Suggestion:**
```
Context: Close button in modal header
Recommendation: Option 1 (best for all users - visible + announced)
WCAG: 4.1.2 Name, Role, Value (Level A)
```

### Issue 2: Poor Color Contrast

**Problem:** Text/UI elements don't meet WCAG contrast ratios

**Examples:**

```tsx
// ❌ Bad: Contrast ratio 2.1:1 (fails WCAG AA)
<button style={{ color: '#999', background: '#fff' }}>Submit</button>

// ✅ Fix: Contrast ratio 4.6:1 (passes AA)
<button style={{ color: '#666', background: '#fff' }}>Submit</button>

// ✅ Better: Contrast ratio 7.2:1 (passes AAA)
<button style={{ color: '#333', background: '#fff' }}>Submit</button>
```

**AI Suggestion:**
```
Issue: Text color #999 on white background (2.1:1 - fails)
Required: 4.5:1 for normal text (WCAG AA)
Suggested colors:
  - #666 (4.6:1) ✓ WCAG AA
  - #555 (5.8:1) ✓ WCAG AA
  - #333 (7.2:1) ✓ WCAG AAA
WCAG: 1.4.3 Contrast (Minimum) (Level AA)
```

### Issue 3: Missing Form Labels

**Problem:** Form inputs without associated labels

**Examples:**

```tsx
// ❌ Bad: No label association
<input type="email" placeholder="Email" />

// ✅ Fix Option 1: Proper label element (BEST)
<label htmlFor="email">
  Email address
  <input id="email" type="email" placeholder="you@example.com" />
</label>

// ✅ Fix Option 2: Label with nesting (GOOD)
<label>
  Email address
  <input type="email" placeholder="you@example.com" />
</label>

// ✅ Fix Option 3: aria-label (ACCEPTABLE)
<input type="email" aria-label="Email address" placeholder="Email" />
```

**AI Suggestion:**
```
Context: Email input in login form
Recommendation: Option 1 (explicit label with htmlFor - most robust)
WCAG: 3.3.2 Labels or Instructions (Level A)
```

### Issue 4: Missing Focus Indicators

**Problem:** Interactive elements lack visible focus state

**Examples:**

```tsx
// ❌ Bad: Focus outline removed
<button style={{ outline: 'none' }} onClick={handleClick}>
  Click me
</button>

// ✅ Fix Option 1: Custom focus-visible (BEST)
<button
  className="focus-visible:ring-2 focus-visible:ring-blue-500 focus-visible:ring-offset-2"
  onClick={handleClick}
>
  Click me
</button>

// ✅ Fix Option 2: Custom outline (GOOD)
<button
  style={{ outline: 'none' }}
  className="focus:outline-blue focus:outline-2 focus:outline-offset-2"
  onClick={handleClick}
>
  Click me
</button>

// ✅ Fix Option 3: Default outline (ACCEPTABLE)
<button onClick={handleClick}>Click me</button>
```

**AI Suggestion:**
```
Issue: outline: none removes focus indicator
Solution: Use :focus-visible for keyboard-only focus styling
WCAG: 2.4.7 Focus Visible (Level AA)
```

### Issue 5: Invalid ARIA Usage

**Problem:** Incorrect or redundant ARIA attributes

**Examples:**

```tsx
// ❌ Bad: Redundant role on button
<button role="button" onClick={handleClick}>Submit</button>

// ✅ Fix: Remove redundant role (native button already has role)
<button onClick={handleClick}>Submit</button>

// ❌ Bad: Invalid ARIA attribute
<div role="button" onClick={handleClick}>Click</div>

// ✅ Fix: Use semantic button element (BEST)
<button onClick={handleClick}>Click</button>

// ✅ Fix: Add keyboard support if div required (ACCEPTABLE)
<div
  role="button"
  onClick={handleClick}
  onKeyDown={(e) => e.key === 'Enter' && handleClick()}
  tabIndex={0}
>
  Click
</div>
```

**AI Suggestion:**
```
Issue: Redundant role="button" on <button> element
Solution: Remove role attribute (native HTML provides this)
WCAG: 4.1.2 Name, Role, Value (Level A)
```

### Issue 6: Missing Alt Text

**Problem:** Images without alternative text

**Examples:**

```tsx
// ❌ Bad: No alt attribute
<img src="/avatar.jpg" />

// ✅ Fix Option 1: Descriptive alt (BEST - informative images)
<img src="/avatar.jpg" alt="Profile photo of John Doe" />

// ✅ Fix Option 2: Empty alt (GOOD - decorative images)
<img src="/decorative-pattern.png" alt="" aria-hidden="true" />

// ✅ Fix Option 3: aria-label (ACCEPTABLE - when alt insufficient)
<img
  src="/complex-chart.png"
  alt="Sales data visualization"
  aria-label="Bar chart showing 40% increase in Q4 sales"
/>
```

**AI Suggestion:**
```
Context: User avatar in profile card
Recommendation: Descriptive alt text with user name
WCAG: 1.1.1 Non-text Content (Level A)
```

## Workflow Example

### Scenario: Creating a Modal Component

```tsx
// User creates Modal component
export function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-content">
        <button onClick={onClose}>×</button>
        {children}
      </div>
    </div>
  );
}
```

**AI Detection (Automatic):**

```
❌ 4 accessibility issues detected in Modal.tsx

Issue 1: Missing accessible name (Line 7)
  Element: <button>×</button>
  WCAG: 4.1.2 Name, Role, Value (Level A)
  Fix options:
    [1] Add sr-only text: <button><span aria-hidden>×</span><span class="sr-only">Close</span></button>
    [2] Add aria-label: <button aria-label="Close modal">×</button>
    [3] Add title: <button title="Close">×</button>

Issue 2: Missing ARIA role (Line 5)
  Element: <div className="modal-overlay">
  WCAG: 4.1.2 Name, Role, Value (Level A)
  Fix: Add role="dialog" and aria-modal="true"

Issue 3: Missing focus trap (Line 6)
  Element: Modal content
  WCAG: 2.4.3 Focus Order (Level A)
  Fix: Implement focus trap to prevent tabbing out of modal

Issue 4: No Escape key handler (Line 5)
  Element: Modal
  WCAG: 2.1.2 No Keyboard Trap (Level A)
  Fix: Add onKeyDown handler for Escape key

Apply fixes? [All] [Select] [Custom] [Skip]
```

**User selects: "All"**

**AI applies fixes:**

```tsx
import { useEffect, useRef } from 'react';
import { FocusTrap } from './FocusTrap';

export function Modal({ isOpen, onClose, children }) {
  const modalRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!isOpen) return;

    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };

    document.addEventListener('keydown', handleEscape);
    modalRef.current?.focus();

    return () => document.removeEventListener('keydown', handleEscape);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div
      className="modal-overlay"
      onClick={onClose}
      aria-hidden={!isOpen}
    >
      <FocusTrap>
        <div
          ref={modalRef}
          className="modal-content"
          role="dialog"
          aria-modal="true"
          tabIndex={-1}
          onClick={(e) => e.stopPropagation()}
        >
          <button
            onClick={onClose}
            aria-label="Close modal"
          >
            <span aria-hidden="true">×</span>
            <span className="sr-only">Close</span>
          </button>
          {children}
        </div>
      </FocusTrap>
    </div>
  );
}
```

**Verification:**

```
✓ All issues resolved
✓ Modal now passes WCAG 2.2 Level AA
✓ Added focus trap component (FocusTrap.tsx)
✓ Added sr-only CSS utility

Run accessibility test? [Yes] [No]
```

## Integration with Testing Suite

This skill works seamlessly with the testing-suite skill:

1. **Remediation skill**: Fixes issues during development
2. **Testing suite**: Validates fixes with axe-core
3. **Storybook stories**: Test all accessibility states
4. **CI/CD**: Automated a11y checks in pipeline

**Combined workflow:**

```
1. Create component → AI detects issues → Apply fixes
2. Run tests → Verify with axe-core → Pass ✓
3. Create stories → Test keyboard navigation → Pass ✓
4. Commit → CI runs a11y tests → Deploy ✓
```

## Advanced Features

### Learning System

AI remembers your fix preferences:

```
You've chosen aria-label for icon buttons 5 times.
Default suggestion updated to rank aria-label first for icon buttons.
```

### Batch Remediation

Fix multiple components at once:

```bash
User: "Fix all accessibility issues in src/components/"

Scanning 23 components...
  ✓ Button.tsx: 2 issues fixed
  ✓ Input.tsx: 3 issues fixed
  ✓ Modal.tsx: 4 issues fixed
  ⚠️ Dropdown.tsx: 1 issue requires custom fix
  ✓ Card.tsx: 1 issue fixed

21/23 components now pass WCAG AA
2 components need manual review
```

### Custom Rules

Define project-specific a11y rules:

```yaml
# .storybook/a11y-config.yml
rules:
  - id: 'custom-button-label'
    description: 'All buttons must have aria-label or visible text'
    severity: 'error'
    fix: 'suggest-aria-label'

  - id: 'custom-min-contrast'
    description: 'Require WCAG AAA contrast (7:1) for all text'
    severity: 'warning'
    fix: 'suggest-darker-color'
```

## Supporting Scripts

This skill includes Python scripts for deep analysis:

### analyze_component.py

Analyzes component AST for accessibility issues:
- Parses JSX/TSX/Vue/Svelte syntax
- Checks WCAG 2.2 rules
- Identifies missing ARIA attributes
- Calculates color contrast ratios
- Detects keyboard navigation issues

See: `skills/accessibility-remediation/scripts/analyze_component.py`

### generate_fixes.py

Generates context-aware fix suggestions:
- Infers component purpose from code
- Ranks fixes by best practice
- Provides code snippets for each fix
- Explains trade-offs and WCAG compliance

See: `skills/accessibility-remediation/scripts/generate_fixes.py`

## Reference Documentation

### WCAG 2.2 Rules Reference

Complete reference of all WCAG 2.2 success criteria with:
- Rule descriptions
- Level (A, AA, AAA)
- Common violations
- Fix patterns
- Code examples

See: `skills/accessibility-remediation/references/wcag-rules.md`

### Common Fix Patterns

Library of proven fix patterns:
- Button accessible names
- Form label associations
- Color contrast adjustments
- Focus management
- ARIA usage patterns
- Keyboard navigation

See: `skills/accessibility-remediation/examples/fix-patterns.md`

## Best Practices

### Do's ✅

- **Fix during development**: Catch issues early
- **Use semantic HTML first**: Native elements over ARIA
- **Test with keyboard**: Tab through all interactions
- **Test with screen readers**: NVDA, JAWS, VoiceOver
- **Maintain contrast ratios**: 4.5:1 minimum (AA)
- **Provide text alternatives**: Alt text, labels, captions
- **Enable keyboard navigation**: Tab order, focus management

### Don'ts ❌

- **Don't ignore warnings**: Address all detected issues
- **Don't use ARIA unnecessarily**: Semantic HTML first
- **Don't remove focus indicators**: Custom style instead
- **Don't rely on color alone**: Use icons, patterns, text
- **Don't skip form labels**: Every input needs a label
- **Don't block keyboard users**: Ensure all features accessible

## Troubleshooting

### False Positives

If AI suggests unnecessary fixes:

```bash
User: "This is a false positive - the component is decorative"

Claude: Understood. I'll:
  1. Mark this pattern as acceptable
  2. Update detection rules
  3. Remember for future similar cases

Would you like to add this to .storybook/a11y-ignore.yml?
```

### Complex Components

For components with complex accessibility needs:

```bash
User: "This datepicker needs custom keyboard navigation"

Claude: This component requires manual implementation:
  1. Arrow keys for date navigation
  2. Page Up/Down for month navigation
  3. Home/End for week navigation
  4. Escape to close

I can provide a reference implementation from accessible datepicker patterns.
Would you like me to generate a template?
```

## Related Skills

- **testing-suite**: Run automated accessibility tests
- **component-scaffold**: Generate accessible components from start
- **story-generation**: Create stories testing all a11y states
- **style-guide-generator**: Document accessibility guidelines

## References

- WCAG 2.2 Guidelines: https://www.w3.org/WAI/WCAG22/quickref/
- ARIA Authoring Practices: https://www.w3.org/WAI/ARIA/apg/
- axe-core Rules: https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md
- WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/

## Summary

Transform accessibility from manual checklist to automated workflow:

1. **Automatic detection**: Catches issues as you code
2. **Context-aware fixes**: AI suggests best solutions
3. **One-click application**: No manual implementation
4. **Educational feedback**: Learn best practices
5. **WCAG 2.2 compliant**: Latest standards built-in

**Result:** Ship accessible components by default with 80% less effort.
