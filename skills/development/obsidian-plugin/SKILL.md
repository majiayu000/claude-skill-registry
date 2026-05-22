---
name: obsidian-plugin
description: Guide Obsidian plugin development following official guidelines. Use when creating/modifying Obsidian plugins, implementing commands, creating UI elements, or handling file operations.
---

# INSTRUCTIONS

Develop Obsidian plugins following official best practices for security, API usage, and UI consistency.

## Core Rules

1. **Use `this.app`** - Never use global `app` object (debugging only)
2. **Minimize logging** - Errors shown by default, not debug messages
3. **Build DOM safely** - See `security.md` for mandatory patterns
4. **Use managed cleanup** - `registerEvent()`, `addCommand()` for auto-cleanup
5. **Replace placeholders** - Change `MyPlugin`, `SampleSettingTab` to actual names

## When to Use

Apply this skill when:
- Creating new Obsidian plugins
- Adding commands, settings, or views
- Handling file/folder operations
- Building plugin UI components
- Reviewing Obsidian plugin code

## Project Structure

```
my-plugin/
├── main.ts                 # Plugin entry point
├── settings.ts             # Settings tab and defaults
├── commands/               # Command handlers
├── views/                  # Custom views
├── modals/                 # Modal dialogs
└── styles.css              # Plugin styles (use CSS variables)
```

## Resource Management

Always use Obsidian's managed registration:

```typescript
// ✅ GOOD: Auto-cleanup on plugin unload
this.registerEvent(
    this.app.vault.on('create', (file) => { ... })
);

this.addCommand({
    id: 'my-command',
    name: 'My Command',
    callback: () => { ... }
});

// ❌ BAD: Manual cleanup required (avoid)
this.app.vault.on('create', this.handler);
```

**NEVER detach leaves in `onunload()`** - Obsidian handles this automatically.

## Key References

- **Security**: See `security.md` for DOM manipulation rules (CRITICAL)
- **API Patterns**: See `api-patterns.md` for workspace, vault, and editor patterns
- **UI Components**: See `ui-components.md` for settings, modals, and views

## Terminology (for Documentation)

| Use | Avoid |
|-----|-------|
| keyboard shortcut | hotkey |
| note | file (for .md) |
| folder | directory |
| select | click/tap |
| perform | invoke |

Use sentence case for headings. Bold button text in docs.

## Quality Checklist

Before releasing a plugin:

- [ ] No `innerHTML`, `outerHTML`, or `insertAdjacentHTML` usage
- [ ] All events registered via `registerEvent()`
- [ ] User file paths normalized with `normalizePath()`
- [ ] CSS uses Obsidian variables, not hardcoded colors
- [ ] Settings have general options at top (no heading)
- [ ] Placeholder class names replaced with actual plugin name
- [ ] Minimal console logging (errors only)
