---
name: bump-plugin-version
description: Bump the version of a plugin in this repository. Use to increment plugin versions and update marketplace metadata.
model: haiku
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Edit, Glob, AskUserQuestion, Bash
---

# Plugin Version Bumper

Bump the version of any plugin in this repository. This skill discovers available plugins, prompts for the bump level, and updates both the plugin configuration and marketplace metadata.

## Workflow

Execute these steps in order.

---

### Step 1: Discover Available Plugins

Find all plugins in this repository:

```bash
# List plugin directories
ls -d plugins/*/
```

For each discovered plugin directory, read its `plugin.json`:
- Path: `plugins/{plugin_name}/.claude-plugin/plugin.json`
- Extract the `name` and `version` fields

Build a list of plugins with their current versions for display to the user.

---

### Step 2: Select Plugin

Use AskUserQuestion to prompt the user to select a plugin.

Display each plugin as an option with its current version:
- Format: "{plugin_name} (v{current_version})"
- Example: "sdd-tools (v0.3.1)"

---

### Step 3: Select Bump Level

Use AskUserQuestion to ask which version component to bump.

Options:
1. **patch** - Bug fixes and minor changes (0.1.0 → 0.1.1)
2. **minor** - New features, backwards compatible (0.1.0 → 0.2.0)
3. **major** - Breaking changes (0.1.0 → 1.0.0)

---

### Step 4: Calculate New Version

Parse the current version string (format: MAJOR.MINOR.PATCH).

Apply the bump:
- **patch**: Increment PATCH, keep MAJOR and MINOR
  - Example: 1.2.3 → 1.2.4
- **minor**: Increment MINOR, reset PATCH to 0, keep MAJOR
  - Example: 1.2.3 → 1.3.0
- **major**: Increment MAJOR, reset MINOR and PATCH to 0
  - Example: 1.2.3 → 2.0.0

---

### Step 5: Update Plugin Configuration

Edit the plugin's configuration file:
- Path: `plugins/{plugin_name}/.claude-plugin/plugin.json`
- Update the `version` field to the new version

Use the Edit tool to make this change.

Report: "Updated plugins/{plugin_name}/.claude-plugin/plugin.json"

---

### Step 6: Update Marketplace Metadata

Read `.claude-plugin/marketplace.json` and locate the plugin entry in the `plugins` array by matching the `name` field.

Update the `version` field for that plugin entry.

Use the Edit tool to make this change.

Report: "Updated .claude-plugin/marketplace.json"

---

### Final Report

Summarize the completed operation:

```
Version bump complete!

Plugin: {plugin_name}
Version: {current_version} → {new_version}

Updated files:
- plugins/{plugin_name}/.claude-plugin/plugin.json
- .claude-plugin/marketplace.json
```
