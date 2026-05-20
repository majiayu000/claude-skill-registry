---
name: accessibility
description: Ensure terminal applications are usable by everyone including users with disabilities
category: UI Frameworks
---

# Skill: accessibility
## What I do

I ensure terminal applications are accessible to everyone, including users with disabilities. This skill covers WCAG principles, keyboard navigation, screen reader support, and testing strategies for inclusive TUIs.
## When to use me

- Building terminal applications used by diverse audiences
- Implementing keyboard shortcuts and navigation
- Testing with screen readers
- Designing for users with disabilities
- Ensuring colour contrast compliance
## Core principles

1. Keyboard navigation first—every feature accessible without mouse
2. Screen reader compatible—semantic structure, ARIA labels where applicable
3. High contrast—minimum 4.5:1 ratio for readability
4. Focus visible—clear indicator of current position
5. Test with real users—accessibility requires actual validation
## Patterns & examples

### Keyboard Navigation
Map all features to keyboard shortcuts. Test with Tab/Shift+Tab. Ensure focus wraps correctly.

### Screen Reader Support
Use semantic output. Test with common readers (NVDA, JAWS). Provide text labels for non-text elements.
## Anti-patterns to avoid

Relying on colour alone to convey information—always add text, icons, or patterns
Missing focus indicators—make keyboard navigation invisible to users
Audio/visual-only feedback—provide text alternatives for all signals

## KB Reference

`~/vaults/baphled/3. Resources/Knowledge Base/AI Development System/Skills/Agent-Guidance/Accessibility.md`

## Related skills

- `clean-code` – Applies across all domains
- `critical-thinking` – For evaluating when to use this skill
