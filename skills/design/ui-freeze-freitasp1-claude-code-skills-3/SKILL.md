---
name: ui-freeze
description: Protects design and theme files from unintended changes. Locks tailwind.config, global CSS, and theme variables. Requires explicit confirmation before modifying UI components. Activate on changes to CSS, theme config, or layout components.
---

# UI Freeze

> Skill to protect design and theme files from unintended changes

## Trigger

This skill activates automatically on changes to:

### Critical Theme Files (LOCKED)

- `tailwind.config.*` - Tailwind configuration
- `**/index.css` - Global styles
- `**/globals.css` - Global CSS variables
- `**/theme.css` - Theme variables
- `**/variables.css` - CSS custom properties

### Important UI Components (WARNING)

- `**/Header.*` - Navigation & Branding
- `**/Footer.*` - Footer & Legal Links
- `**/App.*` - Root Layout & Theme Provider
- `**/Layout.*` - Main Layout wrapper

## Rules

### On Changes to LOCKED Files:

1. **STOP** - Don't automatically make changes
2. **SHOW** - Display exactly what would change
3. **JUSTIFY** - Why is this change needed?
4. **IMPACT** - Which components are affected?
5. **PREVIEW** - If possible, show visual diff
6. **CONFIRM** - Explicit "Yes, change design"

### On Changes to WARNING Files:

1. **NOTE** - "This file affects the UI"
2. **JUSTIFY** - Brief explanation of change
3. **PROCEED** - Can continue without explicit confirmation

## Example Dialog

**User:** "Change the background color to gray"

**Claude (with this skill):**

```
UI FREEZE ACTIVE

You want to modify a theme file. This affects:
- File: tailwind.config.ts
- Change: backgroundColor from #0f172a to #374151
- Affected pages: ALL (global style)

Last stable version: v1.0-stable-ui

Preview:
- Before: Dark blue background (#0f172a)
- After: Gray background (#374151)

Should I proceed? (Answer with "Yes, change design")
Alternative: "Show me a before/after screenshot"
```

## Golden Screenshots (Reference)

Define baseline screenshots for visual regression:

| Page | File | Last Check |
|------|------|------------|
| Login | `tests/screenshots/login-baseline.png` | - |
| Dashboard | `tests/screenshots/dashboard-baseline.png` | - |
| Settings | `tests/screenshots/settings-baseline.png` | - |

## CSS Variables (Single Source of Truth)

All colors must be defined via CSS Variables:

```css
/* CORRECT - in theme.css or tailwind.config */
--color-primary: #3B82F6;
--color-background: #0f172a;

/* WRONG - hard values in components */
background-color: #0f172a; /* Not allowed */
className="bg-[#0f172a]"   /* Not allowed */
```

## Integration with Visual Regression

After every approved design change:

1. Run `npx playwright test --update-snapshots`
2. Commit new baseline screenshots
3. Update release tag (e.g., `v1.1-ui-gray-theme`)

## Emergency Rollback

If design was accidentally changed:

```bash
# Restore last stable state
git checkout <last-stable-tag> -- tailwind.config.ts src/index.css

# Or: Reset all theme files
git checkout <last-stable-tag> -- $(git diff --name-only HEAD <last-stable-tag> | grep -E '\.(css|config)')
```

## Configuration

Add to your CLAUDE.md:

```markdown
### UI Protection

Locked Files:
- tailwind.config.*
- src/index.css
- src/globals.css

Last Stable UI Tag: v1.0-stable-ui

Design System:
- Primary: #3B82F6
- Background: #0f172a
- Use CSS variables only
```

---

## Origin

Originally developed for [fabrikIQ](https://fabrikiq.com) - AI-powered manufacturing data analysis.

## License

MIT - Free to use and modify
