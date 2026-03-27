---
name: wip-version
description: "{{ 𝚫𝚫𝚫 }} Check all version number props and update them"
model: haiku
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Edit"]
argument-hint: [version number]
---

# Version Checker

Check the following properties and update to the value show (coercing type if necessary)

- `README.md` - `# Iris v$ARGUMENTS`
- `package.json` - `"version": "$ARGUMENTS"`
- `src-tauri/tauri.conf.json` - `"version": "$ARGUMENTS"`
- `src-tauri/Cargo.toml` - `[package] name = "app" version = "$ARGUMENTS"`
- `src/tui/utils/layout.ts` - `this.term.colorRgbHex(theme.textMuted)('$ARGUMENTS');`

If no args are passed, do not execute this command.
