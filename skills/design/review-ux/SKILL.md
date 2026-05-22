---
name: review:ux
description: UX-focused review covering accessibility, frontend accessibility, frontend performance, and UX copy. Spawns the senior-review-specialist agent for user experience analysis.
---

# UX Code Review

Run a UX-focused review using 4 user experience checklists via the senior-review-specialist agent.

## Instructions

Spawn the `senior-review-specialist` agent to perform this review.

## Checklists to Apply

Load and apply these review checklists:

- `commands/review/accessibility.md` - Keyboard, assistive technology, ARIA
- `commands/review/frontend-accessibility.md` - SPA-specific accessibility issues
- `commands/review/frontend-performance.md` - Bundle size, rendering, latency
- `commands/review/ux-copy.md` - User-facing text clarity, error recovery

## Agent Instructions

The agent should:

1. **Get working tree changes**: Run `git diff` to see all changes
2. **Identify frontend files**:
   - React, Vue, Angular, Svelte components
   - CSS, styling files
   - Localization/i18n files
   - User-facing text in any file
3. **For each changed file**:
   - Read the full file content
   - Go through each diff hunk
   - Apply all 4 UX checklists
   - Focus on user impact and accessibility
4. **Cross-reference related files**: Check component hierarchy, shared styles
5. **Assess user impact**: How does this affect real users?

## Output Format

Generate a UX review report with:

- **Critical Issues (BLOCKER)**: Accessibility violations (WCAG A/AA)
- **High Priority Issues**: Usability problems, poor error handling
- **Medium Priority Issues**: Performance concerns, copy improvements
- **Accessibility Assessment**: WCAG compliance, screen reader compatibility
- **Performance Assessment**: Bundle impact, rendering efficiency
- **Copy Assessment**: Clarity, consistency, actionability
- **File Summary**: UX issues per file
- **Overall Assessment**: User experience quality recommendation
