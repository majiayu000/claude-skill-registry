---
name: docusaurus-themes
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when swizzling Docusaurus theme components and editing theme elements
---

# Docusaurus Swizzle

## Quick Start

Swizzle components to customize Docusaurus theme behavior:

```bash
npm run swizzle @docusaurus/theme-classic ComponentName -- --wrap
```

## Core Principles

- **Wrap** (safe): Extends original component, easier to upgrade
- **Eject** (unsafe): Full copy for maximum control, harder to maintain
- **Interactive mode**: Use `npm run swizzle` to browse available components
- Swizzled components go in `src/theme/ComponentName/`

## Common Patterns

**List available components:**

```bash
npm run swizzle @docusaurus/theme-classic -- --list
```

**Commonly swizzled:** Footer, Navbar, DocItem, DocSidebar, TOC

## Reference Files

For detailed documentation, see:

- [references/commands.md](references/commands.md) - All swizzle commands and options
- [references/components.md](references/components.md) - Component-specific guides

## Notes

- Prefer `--wrap` for minor changes to maintain upgrade compatibility
- Test thoroughly after swizzling components
- Check official docs for component-specific swizzle safety ratings

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this file ~50 lines total (max ~150 lines)
- Use 1-2 code blocks only (recommend 1)
- Keep description <200 chars for Level 1 efficiency
- Move detailed docs to references/ for Level 3 loading
- This is Level 2 - quick reference ONLY, not a manual

LLM WORKFLOW (when editing this file):
1. Write/edit SKILL.md
2. Format (if formatter available)
3. Run: claude-skills-cli validate <path>
4. If multi-line description warning: run claude-skills-cli doctor <path>
5. Validate again to confirm
-->
