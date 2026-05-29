---
name: obsidian-common-errors
description: |
  Diagnose and fix common Obsidian plugin errors and exceptions.
  Use when encountering plugin errors, debugging failed operations,
  or troubleshooting Obsidian plugin issues.
  Trigger with phrases like "obsidian error", "fix obsidian plugin",
  "obsidian not working", "debug obsidian plugin".
allowed-tools: Read, Grep, Bash(node:*)
version: 1.0.0
license: MIT
author: Jeremy Longshore <jeremy@intentsolutions.io>
---

# Obsidian Common Errors

## Overview
Quick reference for the most common Obsidian plugin errors and their solutions.

## Prerequisites
- Obsidian plugin development environment set up
- Access to Developer Console (Ctrl/Cmd+Shift+I)
- Plugin source code access

## Instructions

### Step 1: Open Developer Console
Press `Ctrl+Shift+I` (Windows/Linux) or `Cmd+Option+I` (macOS) to open Developer Tools.

### Step 2: Identify the Error
Check the Console tab for red error messages related to your plugin.

### Step 3: Match Error to Solutions Below
Find your error type and apply the fix.

## Error Handling

### TypeError: Cannot read properties of undefined

**Error Message:**
```
TypeError: Cannot read properties of undefined (reading 'xyz')
```

**Cause:** Accessing a property on a null/undefined object, often when vault or workspace isn't ready.

**Solution:**
```typescript
// WRONG: Direct access without check
const file = this.app.workspace.getActiveFile();
const content = await this.app.vault.read(file); // Error if file is null

// RIGHT: Null check first
const file = this.app.workspace.getActiveFile();
if (!file) {
  new Notice('No file is currently open');
  return;
}
const content = await this.app.vault.read(file);
```

---

### Plugin failed to load

**Error Message:**
```
Plugin 'my-plugin' failed to load
```

**Causes and Solutions:**

1. **Syntax error in main.js:**
```bash
# Check for syntax errors
node -c main.js
```

2. **Missing manifest.json fields:**
```json
{
  "id": "my-plugin",          // Required: unique identifier
  "name": "My Plugin",         // Required: display name
  "version": "1.0.0",          // Required: semver version
  "minAppVersion": "1.0.0",    // Required: minimum Obsidian version
  "description": "...",        // Required
  "author": "Your Name"        // Required
}
```

3. **No default export:**
```typescript
// WRONG: Named export
export class MyPlugin extends Plugin { }

// RIGHT: Default export
export default class MyPlugin extends Plugin { }
```

---

### This plugin failed to load and has been disabled

**Error Message:**
```
This plugin failed to load and has been disabled. Check the developer console for more information.
```

**Common Causes:**

1. **Runtime error in onload():**
```typescript
// WRONG: Error thrown during load
async onload() {
  const data = await someAsyncOperation(); // Throws if fails
}

// RIGHT: Wrap in try-catch
async onload() {
  try {
    const data = await someAsyncOperation();
  } catch (error) {
    console.error('Failed to load data:', error);
    new Notice('Plugin initialization failed');
  }
}
```

2. **Incorrect module import:**
```typescript
// WRONG: Importing from wrong package
import { Something } from 'wrong-package';

// RIGHT: Check external modules in build config
// esbuild.config.mjs
external: ['obsidian', 'electron', '@codemirror/*', '@lezer/*'],
```

---

### Command not found / Command not registered

**Error Message:**
```
Command 'my-plugin:my-command' not found
```

**Cause:** Command not registered or wrong command ID.

**Solution:**
```typescript
// Verify command registration
this.addCommand({
  id: 'my-command',  // ID without plugin prefix
  name: 'My Command',
  callback: () => {
    // Handler
  },
});

// Obsidian automatically prefixes with plugin ID:
// Full ID becomes: 'my-plugin:my-command'
```

---

### View type not registered

**Error Message:**
```
View type 'custom-view' not registered
```

**Cause:** Trying to use a view before registering it.

**Solution:**
```typescript
// MUST register view in onload, BEFORE using it
async onload() {
  // 1. Register view type first
  this.registerView(
    VIEW_TYPE_CUSTOM,
    (leaf) => new CustomView(leaf)
  );

  // 2. Then you can activate it
  this.addCommand({
    id: 'open-view',
    name: 'Open View',
    callback: () => this.activateView(), // Now safe to call
  });
}
```

---

### Settings not persisting

**Error Message:** No error, but settings reset on reload.

**Cause:** Missing `saveData()` call or wrong data structure.

**Solution:**
```typescript
// WRONG: Modifying settings without saving
this.settings.myOption = newValue;

// RIGHT: Save after modifying
this.settings.myOption = newValue;
await this.saveSettings();

// Implement save properly:
async saveSettings() {
  await this.saveData(this.settings);
}

async loadSettings() {
  this.settings = Object.assign(
    {},
    DEFAULT_SETTINGS,
    await this.loadData()
  );
}
```

---

### File not found / Path errors

**Error Message:**
```
Error: ENOENT: no such file or directory
```

**Cause:** Incorrect file path or file doesn't exist.

**Solution:**
```typescript
// Always verify file exists
const file = this.app.vault.getAbstractFileByPath(path);

if (!file) {
  new Notice(`File not found: ${path}`);
  return;
}

if (!(file instanceof TFile)) {
  new Notice(`Not a file: ${path}`);
  return;
}

// Now safe to use
const content = await this.app.vault.read(file);
```

---

### Memory leaks / Event handlers not cleaned up

**Symptoms:** Plugin slows down, duplicate events firing.

**Cause:** Event listeners not properly removed.

**Solution:**
```typescript
// WRONG: Direct event listener
document.addEventListener('click', this.handleClick);

// RIGHT: Use registerDomEvent (auto-cleanup)
this.registerDomEvent(document, 'click', this.handleClick.bind(this));

// WRONG: Direct workspace event
this.app.workspace.on('file-open', callback);

// RIGHT: Use registerEvent (auto-cleanup)
this.registerEvent(
  this.app.workspace.on('file-open', callback)
);
```

---

### Build errors: Cannot find module 'obsidian'

**Error Message:**
```
Cannot find module 'obsidian' or its corresponding type declarations
```

**Solution:**
```bash
# Verify obsidian types are installed
npm install obsidian@latest

# Check tsconfig.json
{
  "compilerOptions": {
    "moduleResolution": "node",
    "types": ["node"]
  }
}

# Note: 'obsidian' is external - not bundled
# Check esbuild.config.mjs
external: ['obsidian'],
```

## Examples

### Debug Logging Helper
```typescript
// Add at top of main.ts for debugging
const DEBUG = true;

function debug(...args: any[]) {
  if (DEBUG) {
    console.log('[MyPlugin]', ...args);
  }
}

// Use throughout code
debug('Loading settings', this.settings);
debug('Processing file', file.path);
```

### Quick Diagnostic Commands
```typescript
// Add debug commands during development
this.addCommand({
  id: 'debug-dump-settings',
  name: 'Debug: Dump Settings',
  callback: () => {
    console.log('Settings:', JSON.stringify(this.settings, null, 2));
  }
});

this.addCommand({
  id: 'debug-list-views',
  name: 'Debug: List Open Views',
  callback: () => {
    const leaves = this.app.workspace.getLeavesOfType('markdown');
    console.log('Open views:', leaves.length);
    leaves.forEach(leaf => {
      console.log('-', leaf.view.file?.path);
    });
  }
});
```

### Escalation Path
1. Check Developer Console for errors
2. Collect evidence with `obsidian-debug-bundle`
3. Search [Obsidian Forum](https://forum.obsidian.md/)
4. Check [GitHub Issues](https://github.com/obsidianmd/obsidian-api/issues)
5. Ask in [Obsidian Discord](https://discord.gg/obsidianmd)

## Resources
- [Obsidian Developer Docs](https://docs.obsidian.md/Plugins)
- [Obsidian Forum - Developers](https://forum.obsidian.md/c/developers/14)
- [Obsidian Discord](https://discord.gg/obsidianmd)

## Next Steps
For comprehensive debugging, see `obsidian-debug-bundle`.
