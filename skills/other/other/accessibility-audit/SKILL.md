---
name: accessibility-audit
description: Fast, high-signal accessibility triage for pages, components, or PRs targeting WCAG 2.2 AA compliance.
keywords:
  - accessibility
  - a11y
  - wcag
  - audit
  - compliance
triggers:
  - accessibility check
  - a11y audit
  - wcag compliance
  - screen reader
  - keyboard navigation
---

# Accessibility Audit Skill

Fast, high-signal accessibility triage for pages, components, or PRs. This is a lightweight check, not a full compliance audit.

## When to Use This Skill

- Quick accessibility triage before releases
- Component-level a11y verification
- PR review for accessibility regressions
- Smoke checks for WCAG compliance
- Validating keyboard navigation on new features

## Quick Audit Checklist

### 1. Automated Snapshot (Recommended)

Run one of these automated tools first:
- `npx @axe-core/cli <url>` - Quick axe-core scan
- `npx pa11y <url> --standard WCAG2AA` - Pa11y audit
- Lighthouse Accessibility score (Chrome DevTools > Lighthouse > Accessibility)

### 2. Keyboard Basics

| Check | Expected |
|-------|----------|
| All interactive elements reachable via Tab | Yes |
| Focus indicator always visible | Yes |
| No keyboard traps | Yes |
| Logical tab order | Yes |
| Skip link works for long pages | Yes |

### 3. Semantics and Labels

| Check | Expected |
|-------|----------|
| Single, descriptive H1 | Yes |
| Logical heading order (no large jumps) | Yes |
| Form inputs have visible labels or aria-label | Yes |
| Buttons and links have clear names | Yes |
| Images have meaningful alt text (or empty for decorative) | Yes |

### 4. Visual Contrast

| Element | Minimum Ratio |
|---------|---------------|
| Normal text | 4.5:1 |
| Large text (18pt+ or 14pt bold+) | 3:1 |
| UI components (inputs, buttons, focus rings) | 3:1 |

### 5. Motion and Updates

| Check | Expected |
|-------|----------|
| Respects `prefers-reduced-motion` | Yes |
| Dynamic updates announced (aria-live) | Yes |

## Output Format

After running the audit, report findings as:

```markdown
## Accessibility Audit: [Component/Page Name]

### Result: [Pass | Needs Fixes | Escalate to Full Audit]

### Findings

| Severity | Issue | Location | Fix Guidance |
|----------|-------|----------|--------------|
| Critical | [Description] | [Selector/Line] | [How to fix] |
| Major | [Description] | [Selector/Line] | [How to fix] |
| Minor | [Description] | [Selector/Line] | [How to fix] |

### Escalation Recommendation
[If applicable, explain why a full audit is needed]
```

## Escalate to Full Audit When

- New or changed navigation structure
- Complex forms or authentication flows
- Custom widgets or advanced interactions (modals, accordions, tabs)
- Public releases or compliance requirements
- Significant page structure changes
- Failed automated scans with multiple critical issues

## Notes

- This smoke check targets **WCAG 2.2 AA** by default
- If a different compliance level is required, state it explicitly
- Automated tools catch ~30-40% of issues; manual testing is essential
- Test with actual screen readers (VoiceOver, NVDA) for comprehensive coverage
