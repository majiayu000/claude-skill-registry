---
name: shopify-theme-wc-portable
description: Build portable web components for Shopify themes that work across any theme structure
allowed-tools:
  - Read
  - Grep
  - glob
  - edit_file
  - create_file
  - Bash
---

# Shopify Theme Web Components (Portable)

<!-- theme-kit:begin managed id=skill-main -->

## Overview

This skill provides guidance for creating web components in Shopify themes that:

- Work in any theme structure (custom, Dawn-based, third-party)
- Don't impose folder conventions
- Follow progressive enhancement principles
- Support theme editor live preview

## Mandatory Discovery

Before creating any component:

1. **Check CLAUDE.local.md** for project-specific patterns
2. **Scan existing JS files** for naming and structure conventions
3. **Identify initialization patterns** used in the theme
4. **Find where scripts are loaded** in layout files

## Integration Policy (Portable)

### File Placement

- Use existing file locations—do not create new folders
- If theme uses single `theme.js`, add to that file
- If theme has component files, create new file in same location

### Registration Pattern

```javascript
// Always use define-once guard
if (!customElements.get("component-name")) {
  customElements.define("component-name", ComponentName);
}
```

### Script Loading

- Follow existing script loading pattern in theme
- If theme uses `defer`, use `defer`
- If theme uses `async`, use `async`
- Match existing asset_url patterns

## Verification Steps

After creating a component:

1. [ ] Component initializes without console errors
2. [ ] Works after section reload in theme editor
3. [ ] Properly cleans up on disconnect
4. [ ] Doesn't break existing theme styles
5. [ ] `shopify theme check` passes
6. [ ] HTML is functional before JS loads

## Common Patterns

See PATTERNS.md for implementation examples of:

- Accordion/Tabs
- Modal/Drawer
- Product Gallery
- Predictive Search enhancements
- Lazy initialization
<!-- theme-kit:end managed id=skill-main -->
