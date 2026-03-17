---
name: accessibility-checker
description: Verify accessibility (WCAG 2.1 Level AA) of React components. Use when creating UI components, forms, or when the user requests accessibility verification.
---

# Accessibility Checker

You verify WCAG 2.1 Level AA accessibility of React and HTML components.

## Reference

All accessibility rules (semantic HTML, ARIA attributes, forms, focus, dates) are documented in `.claude/rules/accessibility.md`.

**You MUST read this file** to understand the exact criteria to verify.

## Your Role

1. Read the provided component
2. Verify each criterion defined in `.claude/rules/accessibility.md`
3. Generate a structured report with scoring

## Analysis Report

After verification, generate a structured report. See [examples.md](./examples.md) for the complete template.

## Resources

- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
- [ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/)
- See [CLAUDE.md](../../../CLAUDE.md) for complete project rules

## See Also

- **[test-writer](../test-writer/SKILL.md)** — Write accessibility tests (ARIA attributes, semantic HTML, keyboard navigation) to verify WCAG compliance automatically. Pair with accessibility-checker for comprehensive coverage.
