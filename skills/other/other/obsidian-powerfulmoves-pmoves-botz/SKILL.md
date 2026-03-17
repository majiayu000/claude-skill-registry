---
name: obsidian
version: 1.1.0
description: Comprehensive guidelines for Obsidian.md plugin development including all 27 ESLint rules, TypeScript best practices, memory management, API usage (requestUrl vs fetch), UI/UX standards, and submission requirements. Use when working with Obsidian plugins, main.ts files, manifest.json, Plugin class, MarkdownView, TFile, vault operations, or any Obsidian API development.
---

# Obsidian Plugin Development Guidelines

You are assisting with Obsidian plugin development. Follow these comprehensive guidelines derived from the official Obsidian ESLint plugin rules, submission requirements, and best practices.

## Getting Started

### Quick Start Tool

For new plugin projects, an interactive boilerplate generator is available:
- **Script**: `tools/create-plugin.js` in the skill repository
- **Slash command**: `/create-plugin` for guided setup
- Generates minimal, best-practice boilerplate with no sample code
- Detects existing projects and only adds missing files
- All generated code follows these guidelines automatically

### When to Suggest the Tool

Recommend the boilerplate generator when users:
- Ask "how do I create a new Obsidian plugin?"
- Want to start a new plugin project
- Need help setting up the basic structure
- Want to ensure they start with best practices

## Core Principles

1. **Memory Safety**: Prevent memory leaks through proper resource management
2. **Type Safety**: Use proper type narrowing and avoid unsafe casts
3. **API Best Practices**: Follow Obsidian's recommended patterns
4. **User Experience**: Maintain consistency in UI/UX across plugins
5. **Platform Compatibility**: Ensure cross-platform support (including iOS)
6. **Accessibility**: Make all features keyboard and screen reader accessible

---

## Quick Reference

### Top 27 Most Critical Rules

**Submission & Naming:**
1. **Plugin ID: no "obsidian", can't end with "plugin"** - Validation bot enforced
2. **Plugin name: no "Obsidian", can't end with "Plugin"** - Validation bot enforced
3. **Plugin name: can't start with "Obsi" or end with "dian"** - Validation bot enforced
4. **Description: no "Obsidian", "This plugin", etc.** - Validation bot enforced
5. **Description must end with `.?!)` punctuation** - Validation bot enforced

**Memory & Lifecycle:**
6. **Use `registerEvent()` for automatic cleanup** - Prevents memory leaks
7. **Don't store view references in plugin** - Causes memory leaks

**Type Safety:**
8. **Use `instanceof` instead of type casting** - Type safety for TFile/TFolder

**UI/UX:**
9. **Use sentence case for all UI text** - "Advanced settings" not "Advanced Settings"
10. **No "command" in command names/IDs** - Redundant
11. **No plugin ID in command IDs** - Obsidian auto-namespaces
12. **No default hotkeys** - Avoid conflicts
13. **Use `.setHeading()` for settings headings** - Not manual HTML

**API Best Practices:**
14. **Use Editor API for active file edits** - Preserves cursor position
15. **Use `Vault.process()` for background file mods** - Prevents conflicts
16. **Use `normalizePath()` for user paths** - Cross-platform compatibility
17. **Use `Platform` API for OS detection** - Not navigator
18. **Use `requestUrl()` instead of `fetch()`** - Bypasses CORS restrictions
19. **No console.log in onload/onunload in production** - Pollutes console

**Styling:**
20. **Use Obsidian CSS variables** - Respects user themes
21. **Scope CSS to plugin containers** - Prevents style conflicts

**Accessibility (MANDATORY):**
22. **Make all interactive elements keyboard accessible** - Accessibility required
23. **Provide ARIA labels for icon buttons** - Accessibility required
24. **Define clear focus indicators** - Use `:focus-visible`

**Security & Compatibility:**
25. **Don't use `innerHTML`/`outerHTML`** - Security risk (XSS)
26. **Avoid regex lookbehind** - iOS < 16.4 incompatibility

**Code Quality:**
27. **Remove all sample/template code** - MyPlugin, SampleModal, etc.

---

## Detailed Guidelines

For comprehensive information on specific topics, see the reference files:

### [Memory Management & Lifecycle](reference/memory-management.md)
- Using `registerEvent()`, `addCommand()`, `registerDomEvent()`, `registerInterval()`
- Avoiding view references in plugin
- Not using plugin as component
- Proper leaf cleanup

### [Type Safety](reference/type-safety.md)
- Using `instanceof` instead of type casting
- Avoiding `any` type
- Using `const` and `let` over `var`

### [UI/UX Standards](reference/ui-ux.md)
- Sentence case enforcement
- Command naming conventions
- Settings and configuration best practices

### [File & Vault Operations](reference/file-operations.md)
- View access patterns
- Editor vs Vault API
- Atomic file operations
- File management
- Path handling

### [CSS Styling Best Practices](reference/css-styling.md)
- Avoiding inline styles
- Using Obsidian CSS variables
- Scoping plugin styles
- Theme support
- Spacing and layout

### [Accessibility (A11y)](reference/accessibility.md)
- Keyboard navigation (MANDATORY)
- ARIA labels and roles (MANDATORY)
- Tooltips and accessibility
- Focus management (MANDATORY)
- Focus visible styles (MANDATORY)
- Screen reader support (MANDATORY)
- Mobile and touch accessibility (MANDATORY)
- Accessibility checklist

### [Code Quality & Best Practices](reference/code-quality.md)
- Removing sample code
- Security best practices
- Platform compatibility
- API usage best practices
- Async/await patterns
- DOM helpers

### [Plugin Submission Requirements](reference/submission.md)
- Repository structure
- Submission process
- Semantic versioning
- Testing checklist

---

## Essential Do's and Don'ts

### Do's ✅

**Memory & Lifecycle**:
- Use `registerEvent()`, `addCommand()`, `registerDomEvent()`, `registerInterval()`
- Return views/components directly (don't store unnecessarily)

**Type Safety**:
- Use `instanceof` for type checking (not type casting)
- Use specific types or `unknown` instead of `any`
- Use `const` and `let` (not `var`)

**API Usage**:
- Use `this.app` (not global `app`)
- Use Editor API for active file edits
- Use `Vault.process()` for background file modifications
- Use `FileManager.processFrontMatter()` for YAML
- Use `fileManager.trashFile()` for deletions
- Use `normalizePath()` for user-defined paths
- Use `Platform` API for OS detection
- Use `AbstractInputSuggest` for autocomplete
- Use direct file lookups (not vault iteration)
- Use `requestUrl()` instead of `fetch()` for network requests

**UI/UX**:
- Use sentence case for all UI text
- Use `.setHeading()` for settings headings
- Use Obsidian DOM helpers (`createDiv()`, `createSpan()`, `createEl()`)
- Use `window.setTimeout/setInterval` with `number` type

**Styling**:
- Move all styles to CSS
- Use Obsidian CSS variables for all styling
- Scope CSS to plugin containers
- Support both light and dark themes via CSS variables
- Follow Obsidian's 4px spacing grid

**Accessibility (MANDATORY)**:
- Make all interactive elements keyboard accessible
- Provide ARIA labels for icon buttons
- Define clear focus indicators using `:focus-visible`
- Use `data-tooltip-position` for tooltips
- Ensure minimum touch target size (44×44px)
- Manage focus properly in modals
- Test with keyboard navigation

**Code Quality**:
- Use async/await (not Promise chains)
- Remove all sample/template code
- Test on mobile (if not desktop-only)
- Follow semantic versioning
- Minimize console logging (no console.log in onload/onunload in production)

### Don'ts ❌

**Memory & Lifecycle**:
- Don't store view references in plugin properties
- Don't pass plugin as component to MarkdownRenderer
- Don't detach leaves in `onunload()`

**Type Safety**:
- Don't cast to TFile/TFolder (use `instanceof`)
- Don't use `any` type
- Don't use `var`

**API Usage**:
- Don't use global `app` object
- Don't use `Vault.modify()` for active file edits
- Don't hardcode `.obsidian` path (use `vault.configDir`)
- Don't use `navigator.platform/userAgent` (use Platform API)
- Don't iterate vault when direct lookup exists
- Don't use `fetch()` (use `requestUrl()` instead)

**UI/UX**:
- Don't use Title Case in UI (use sentence case)
- Don't include "command" in command names/IDs
- Don't duplicate plugin ID in command IDs
- Don't set default hotkeys
- Don't create manual HTML headings (use `.setHeading()`)
- Don't use "General", "settings", or plugin name in settings headings

**Styling**:
- Don't assign styles via JavaScript
- Don't hardcode colors, sizes, or spacing (use CSS variables)
- Don't use broad CSS selectors (scope to plugin)
- Don't manually switch themes (CSS variables adapt automatically)
- Don't create `<link>` or `<style>` elements (use `styles.css` file)

**Security & Compatibility**:
- Don't use `innerHTML`/`outerHTML` (XSS risk)
- Don't use regex lookbehind (iOS < 16.4 incompatibility)

**Accessibility**:
- Don't create inaccessible interactive elements
- Don't use icon buttons without ARIA labels
- Don't remove focus indicators without alternatives
- Don't make touch targets smaller than 44×44px

**Code Quality**:
- Don't use Promise chains (use async/await)
- Don't use `document.createElement` (use Obsidian helpers)
- Don't keep sample class names (MyPlugin, SampleModal, etc.)
- Don't use console.log in onload/onunload (pollutes console in production)

---

## When Reviewing/Writing Code

Use this checklist for code review and implementation:

1. **Memory management**: Are components and views properly managed?
2. **Type safety**: Using `instanceof` instead of casts?
3. **UI text**: Is everything in sentence case?
4. **Command naming**: No redundant words?
5. **File operations**: Using preferred APIs?
6. **Mobile compatibility**: No iOS-incompatible features?
7. **Sample code**: Removed all boilerplate?
8. **Manifest**: Correct version, valid structure?
9. **Accessibility**: Keyboard navigation, ARIA labels, focus indicators?
10. **Testing**: Can you use the plugin without a mouse?
11. **Touch targets**: Are all interactive elements at least 44×44px?
12. **Focus styles**: Using `:focus-visible` and proper CSS variables?

---

## Common Patterns

### Proper Command Registration

```typescript
// ✅ CORRECT
this.addCommand({
  id: 'insert-timestamp',
  name: 'Insert timestamp',
  editorCallback: (editor: Editor, view: MarkdownView) => {
    editor.replaceSelection(new Date().toISOString());
  }
});
```

### Safe Type Narrowing

```typescript
// ✅ CORRECT
const file = this.app.vault.getAbstractFileByPath(path);
if (file instanceof TFile) {
  // TypeScript now knows it's a TFile
  await this.app.vault.read(file);
}
```

### Keyboard Accessible Button

```typescript
// ✅ CORRECT
const button = containerEl.createEl('button', {
  attr: {
    'aria-label': 'Open settings',
    'data-tooltip-position': 'top'
  }
});
button.setText('⚙️');

button.addEventListener('keydown', (e) => {
  if (e.key === 'Enter' || e.key === ' ') {
    e.preventDefault();
    performAction();
  }
});
```

### Themed CSS

```css
/* ✅ CORRECT */
.my-plugin-modal {
  background: var(--modal-background);
  color: var(--text-normal);
  padding: var(--size-4-4);
  border-radius: var(--radius-m);
  font-size: var(--font-ui-medium);
}

.my-plugin-button:focus-visible {
  outline: 2px solid var(--interactive-accent);
  outline-offset: 2px;
}
```

---

## Additional Resources

- ESLint Plugin: `eslint-plugin-obsidianmd` (install for automatic checking)
- Obsidian API Docs: https://docs.obsidian.md
- Sample Plugin: https://github.com/obsidianmd/obsidian-sample-plugin
- Community: Obsidian Discord, Forum

---

## Important Notes

- These guidelines are based on `eslint-plugin-obsidianmd` which is under active development
- Rules marked as auto-fixable can be automatically corrected with ESLint's `--fix` flag
- **Accessibility is NOT optional** - all interactive elements must be keyboard accessible
- Always test on mobile devices if your plugin is not desktop-only

When helping with Obsidian plugin development, proactively apply these rules and suggest improvements based on these guidelines. Refer to the detailed reference files for comprehensive information on specific topics.
