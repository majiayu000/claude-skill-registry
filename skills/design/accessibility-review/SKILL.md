---
name: accessibility-review
description: Reviews UI for accessibility issues against WCAG 2.1/2.2 AA. Triggers on "is this accessible?", "check accessibility", or contrast/a11y review requests.
---

# Accessibility Review

## Overview

This skill enables manual accessibility reviews of web content, components, and applications against WCAG 2.1/2.2 Level AA standards. Reviews focus on practical, modern accessibility requirements without being overly pedantic.

## When to Use This Skill

Use this skill when the user asks questions like:
- "Is this accessible?"
- "Can you review the color contrast?"
- "Check this component for accessibility issues"
- "Does this meet accessibility standards?"
- Any request to review, check, or validate accessibility

## Review Process

### 1. Identify the Target

Determine what needs to be reviewed:
- Specific component (button, form, modal, etc.)
- Full page or application
- Code file or set of files
- Design mockup or screenshot

### 2. Conduct Manual Review

Use the WCAG checklist in `references/wcag-checklist.md` to systematically review the target against modern accessibility standards.

Focus on the most common and impactful issues:
- **Perceivable**: Color contrast, text alternatives, semantic structure
- **Operable**: Keyboard navigation, focus management, interactive elements
- **Understandable**: Clear labels, error handling, consistent navigation
- **Robust**: Valid HTML, ARIA usage, compatibility

### 3. Prioritize Findings

Classify each issue as:

**Critical** - Blocks users from accessing core functionality:
- Missing alt text on meaningful images
- Non-keyboard accessible interactive elements
- Insufficient color contrast (below 4.5:1 for normal text, 3:1 for large text)
- Forms without proper labels
- Missing focus indicators
- Inaccessible modal/dialog patterns
- Auto-playing media without controls

**Warning** - Creates friction but doesn't fully block access:
- Suboptimal heading hierarchy (skipped levels)
- Missing ARIA landmarks
- Link text that's unclear out of context
- Redundant or unnecessary ARIA
- Touch targets smaller than 44x44px
- Missing skip links
- Non-descriptive error messages

### 4. Stepped Review (One Issue at a Time)

**IMPORTANT**: Do NOT present all findings at once. Review issues one at a time, waiting for user decision before proceeding.

**4.1 Start with Overview**

Begin by telling the user how many issues were found:

```
Found [X] accessibility issues ([Y] critical, [Z] warnings).

Let's review them one at a time. I'll present each issue with a recommended fix, and you can decide to:
- **Fix** — I'll implement the change
- **Ignore** — Tell me why, and I'll note it

Starting with critical issues first.
```

**4.2 Present Each Issue**

For each issue, present ONE at a time using this format:

```
───────────────────────────────────
Issue [1/X]: [Critical/Warning]
───────────────────────────────────

**Problem**: [Clear description of the issue]

**Location**: `file_path:line_number`
[Show the relevant code snippet]

**Impact**: [How this affects users — be specific about who and how]

**Recommended Fix**:
[Specific code change or approach]

───────────────────────────────────
Fix this issue, or ignore? (If ignoring, please share why)
```

**4.3 Handle User Response**

**If user says "fix":**
1. Implement the fix
2. Confirm: "Fixed. [Brief description of what changed]"
3. Move to next issue

**If user says "ignore" with reason:**
1. Acknowledge: "Noted — ignoring because: [their reason]"
2. Track the decision (see 4.4)
3. Move to next issue

**If user says "ignore" without reason:**
1. Ask: "Got it. Quick note on why? (Helps for future reference)"
2. Accept any response and move on

**4.4 Track Decisions**

Keep a running tally as you go through issues. After all issues are reviewed, present a summary.

### 5. Final Summary

After reviewing all issues, present a summary:

```
## Accessibility Review Complete

**Reviewed**: [X] issues ([Y] critical, [Z] warnings)

### Fixed ([N])
- [Issue description] — `file:line`
- [Issue description] — `file:line`

### Ignored ([N])
- [Issue description] — Reason: [user's reason]
- [Issue description] — Reason: [user's reason]

### Remaining Concerns
[Any patterns noticed, suggestions for future, or issues that were ignored but warrant reconsideration]
```

## Review Guidelines

**Be Practical**: Focus on issues that genuinely impact users. Modern WCAG 2.1/2.2 Level AA is the standard—avoid over-engineering or citing obscure edge cases.

**Be Specific**: Reference actual code locations using `file_path:line_number` format when possible.

**Be Constructive**: Provide actionable fixes, not just problems. Include code examples when helpful.

**Consider Context**: Some patterns may have accessibility trade-offs. Acknowledge these and suggest the most accessible approach for the use case.

## Common Patterns to Check

### Interactive Elements
- All interactive elements must be keyboard accessible (Enter/Space to activate)
- Focus must be visible with clear indicators
- Custom controls need proper ARIA roles and states

### Forms
- All inputs must have associated labels (explicit or aria-label)
- Error messages must be programmatically associated with fields
- Required fields must be indicated clearly

### Color and Contrast
- Text contrast: 4.5:1 minimum for normal text, 3:1 for large text (18pt+ or 14pt+ bold)
- UI components: 3:1 contrast for interactive elements and their states
- Don't rely on color alone to convey information

### Images and Media
- Meaningful images need descriptive alt text
- Decorative images should have empty alt (alt="")
- Videos need captions, audio content needs transcripts

### Structure
- Use semantic HTML (nav, main, article, etc.)
- Heading hierarchy should be logical (h1 → h2 → h3)
- ARIA landmarks help screen reader navigation

## Resources

This skill includes:

### references/wcag-checklist.md
Comprehensive checklist of WCAG 2.1/2.2 Level AA requirements organized by principle (Perceivable, Operable, Understandable, Robust). Reference this during reviews to ensure thorough coverage of accessibility standards.
