---
name: accessibility-design-checker
description: Ensures designs meet accessibility requirements including WCAG compliance, color contrast, keyboard navigation, screen reader support, and focus management. Reviews designs for accessibility issues and provides recommendations.
---

# Accessibility Design Checker Skill

## Instructions

1. Review design specifications for accessibility
2. Check color contrast ratios
3. Verify keyboard navigation support
4. Check screen reader compatibility
5. Review focus management
6. Verify touch target sizes
7. Return accessibility review with:
   - Accessibility compliance status
   - Issues found
   - Recommendations
   - WCAG level compliance

## Examples

**Input:** Review design for accessibility
**Output:**
```markdown
### Accessibility Review

**Overall Compliance:** WCAG 2.1 Level AA ✓

**Color Contrast:**
- Primary text on white: 4.5:1 ✓ (WCAG AA)
- Secondary text on white: 4.2:1 ✗ (needs improvement)
- Large text on primary: 3.1:1 ✓ (WCAG AA)
- Recommendation: Increase secondary text contrast to 4.5:1

**Keyboard Navigation:**
- All interactive elements keyboard accessible ✓
- Focus indicators visible ✓
- Tab order logical ✓
- Skip links present ✓

**Screen Reader Support:**
- Semantic HTML structure ✓
- ARIA labels where needed ✓
- Alt text for images ✓
- Form labels properly associated ✓

**Touch Targets:**
- All interactive elements ≥ 44x44px ✓
- Adequate spacing between touch targets ✓

**Text Resizing:**
- Design works at 200% zoom ✓
- No horizontal scrolling required ✓

**Issues Found:**
1. Secondary text contrast below 4.5:1 (should be improved)
2. Missing ARIA label on icon-only button (needs label)

**Recommendations:**
- Increase secondary text color darkness
- Add aria-label="Close" to icon button
```

## Accessibility Areas to Check

- **Color Contrast**: Text/background contrast ratios (WCAG AA: 4.5:1)
- **Keyboard Navigation**: All interactive elements keyboard accessible
- **Focus Indicators**: Visible focus states
- **Screen Reader Support**: Semantic HTML, ARIA labels, alt text
- **Touch Targets**: Minimum 44x44px for mobile
- **Text Resizing**: Works at 200% zoom
- **Reading Order**: Logical content order
- **Form Labels**: Properly associated labels
- **Error Messages**: Accessible error communication
- **Skip Links**: Skip navigation links

## WCAG Compliance Levels

- **Level A**: Basic accessibility (minimum)
- **Level AA**: Standard compliance (recommended)
- **Level AAA**: Enhanced accessibility (ideal)

## Common Issues

- **Low Contrast**: Text/background contrast too low
- **Missing Alt Text**: Images without descriptive alt text
- **Missing Labels**: Form inputs without labels
- **Small Touch Targets**: Interactive elements too small
- **No Focus Indicators**: Missing visible focus states
- **Poor Semantic Structure**: Incorrect HTML structure
- **Keyboard Traps**: Elements that trap keyboard focus
