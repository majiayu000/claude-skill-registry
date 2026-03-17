---
name: accessibility-check
description: Run accessibility audit on frontend components for WCAG 2.1 AA compliance
user-invocable: true
---

# Accessibility Check

Perform a WCAG 2.1 AA compliance audit on frontend components.

## Audit Areas

### 1. Keyboard Navigation
- All interactive elements must be focusable
- Tab order must be logical
- No keyboard traps
- Visible focus indicators (use `.focus-ring`)

### 2. Screen Reader Support
Search for issues:
```bash
# Icon-only buttons missing aria-label
grep -rE "<Button[^>]*>[^<]*<svg" frontend/src/components/ --include="*.tsx" | grep -v "aria-label"

# Images missing alt text
grep -r "<img" frontend/src/components/ --include="*.tsx" | grep -v "alt="

# Missing form labels
grep -rE "<input[^>]*>" frontend/src/components/ --include="*.tsx" | grep -v "aria-label\|id.*label"
```

### 3. Color Contrast
Pierre design system colors meet contrast requirements:
- `pierre-gray-900` on white: 15.3:1 ✓
- `pierre-gray-700` on white: 8.5:1 ✓
- `pierre-gray-500` on white: 4.6:1 ✓ (minimum for large text)
- `pierre-violet` on white: 5.7:1 ✓

**Flag if using**:
- `pierre-gray-400` for body text (3.0:1 - FAILS)
- Light colors on light backgrounds
- Custom colors not in design system

### 4. Touch Targets
- Minimum 44x44px for touch targets
- Check Button `size="sm"` usage - ensure adequate padding

### 5. Motion & Animation
- Respect `prefers-reduced-motion`
- No auto-playing animations that distract

## Output Format

```
=== Accessibility Audit Report ===

📁 Files Analyzed: [count]

== Keyboard Navigation ==
✅/❌ Focus indicators: [details]
✅/❌ Tab order: [details]

== Screen Reader ==
✅/❌ Icon buttons: [count with aria-label / count missing]
✅/❌ Images: [count with alt / count missing]
✅/❌ Form labels: [details]

== Color Contrast ==
✅/❌ Text contrast: [details]
✅/❌ Interactive elements: [details]

== Touch Targets ==
✅/❌ Minimum size: [details]

== Issues Found ==
[CRITICAL] [file:line] - [issue]
[MAJOR] [file:line] - [issue]
[MINOR] [file:line] - [issue]

== Fixes Required ==
1. [specific fix with code example]

== Verdict ==
[PASS / NEEDS WORK - X critical, Y major, Z minor issues]
```

## WCAG Quick Reference

| Criteria | Requirement |
|----------|-------------|
| 1.1.1 | Non-text content has text alternative |
| 1.4.3 | Contrast ratio 4.5:1 (text) |
| 2.1.1 | All functionality keyboard accessible |
| 2.4.7 | Focus visible |
| 4.1.2 | Name, Role, Value for UI components |
