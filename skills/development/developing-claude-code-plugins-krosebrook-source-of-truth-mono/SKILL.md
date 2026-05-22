---
name: developing-claude-code-plugins
description: Use when working on Claude Code plugins (creating, modifying, testing, releasing, or maintaining) - provides streamlined workflows, patterns, and examples for the complete plugin lifecycle
---

# Developing Claude Code Plugins

## Overview

This skill provides efficient workflows for creating Claude Code plugins. Use it to make plugin development fast and correct - it synthesizes official docs into actionable steps and provides working examples.

## When to Use

Use this skill when:
- Creating a new Claude Code plugin from scratch
- Adding components to an existing plugin (skills, commands, hooks, MCP servers)
- Setting up a development marketplace for testing
- Troubleshooting plugin structure issues
- Understanding plugin architecture and patterns
- Releasing a plugin (versioning, tagging, marketplace distribution)
- Publishing updates or maintaining existing plugins

**For comprehensive official documentation**, use the `working-with-claude-code` skill to access full docs.

## Quick Reference

| Need to... | Read This | Official Docs |
|-----------|-----------|---------------|
| Understand directory structure | `references/plugin-structure.md` | `plugins.md` |
| Choose a plugin pattern | `references/common-patterns.md` | `plugins.md` |
| Debug plugin issues | `references/troubleshooting.md` | Various |
| See working examples | `examples/` directory | N/A |

## Plugin Development Workflow

### Phase 1: Plan

Before writing code:

1. **Define your plugin's purpose**
   - What problem does it solve?
   - Who will use it?
   - What components will it need?

2. **Choose your pattern** (read `references/common-patterns.md`)
   - Simple plugin with one skill?
   - MCP integration with guidance?
   - Command collection?
   - Full-featured platform?

3. **Review examples**
   - `examples/simple-greeter-plugin/` - Minimal plugin
   - `examples/full-featured-plugin/` - All components
   - Installed plugins in `~/.claude/plugins/`

### Phase 2: Create Structure

1. **Create directories** (see `references/plugin-structure.md` for details):
   ```bash
   mkdir -p my-plugin/.claude-plugin
   mkdir -p my-plugin/skills
   # Add other component directories as needed
   ```

2. **Write plugin.json** (required):
   ```json
   {
     "name": "my-plugin",
     "version": "1.0.0",
     "description": "What your plugin does",
     "author": {"name": "Your Name"}
   }
   ```
   See `references/plugin-structure.md` for complete format.

3. **Create development marketplace** (for local testing):

   Create `.claude-plugin/marketplace.json`:
   ```json
   {
     "name": "my-dev",
     "plugins": [{
       "name": "my-plugin",
       "source": "./"
     }]
   }
   ```

   See `references/plugin-structure.md` for complete format.

### Phase 3: Add Components

Use TodoWrite to track component creation:

**Example:**
```
- Create skill: main-workflow
- Add command: /hello
- Configure hooks
- Write README
- Test installation
```

For each component type, see:
- **Format/syntax**: `references/plugin-structure.md`
- **When to use**: `references/common-patterns.md`
- **Working code**: `examples/` directory

### Phase 4: Test Locally

1. **Install for testing**:
   ```bash
   /plugin marketplace add /path/to/my-plugin
   /plugin install my-plugin@my-dev
   ```
   Then restart Claude Code.

2. **Test each component**:
   - Skills: Ask for tasks matching skill descriptions
   - Commands: Run `/your-command`
   - MCP servers: Check tools are available
   - Hooks: Trigger relevant events

3. **Iterate**:
   ```bash
   /plugin uninstall my-plugin@my-dev
   # Make changes
   /plugin install my-plugin@my-dev
   # Restart Claude Code
   ```

### Phase 5: Debug and Refine

If something doesn't work, read `references/troubleshooting.md` for:
- Plugin not loading
- Skill not triggering
- Command not appearing
- MCP server not starting
- Hooks not firing

Common issues are usually:
- Wrong directory structure
- Hardcoded paths (use `${CLAUDE_PLUGIN_ROOT}`)
- Forgot to restart Claude Code
- Missing executable permissions on scripts

### Phase 6: Release and Distribute

1. **Write README** with:
   - What the plugin does
   - Installation instructions
   - Usage examples
   - Component descriptions

2. **Version your release** using semantic versioning:
   - Update `version` in `.claude-plugin/plugin.json`
   - Document changes in CHANGELOG.md or RELEASE-NOTES.md
   - Example: `"version": "1.2.1"` (major.minor.patch)

3. **Commit and tag your release**:
   ```bash
   git add .
   git commit -m "Release v1.2.1: [brief description]"
   git tag v1.2.1
   git push origin main
   git push origin v1.2.1
   ```

4. **Choose distribution method**:

   **Option A: Direct GitHub distribution**
   - Users add: `/plugin marketplace add your-org/your-plugin-repo`
   - Your plugin.json serves as the manifest

   **Option B: Marketplace distribution** (recommended for multi-plugin collections)
   - Create separate marketplace repository
   - Add `.claude-plugin/marketplace.json` with plugin references:
     ```json
     {
       "name": "my-marketplace",
       "owner": {"name": "Your Name"},
       "plugins": [{
         "name": "your-plugin",
         "source": {
           "source": "url",
           "url": "https://github.com/your-org/your-plugin.git"
         },
         "version": "1.2.1",
         "description": "Plugin description"
       }]
     }
     ```
   - Users add: `/plugin marketplace add your-org/your-marketplace`
   - Update marketplace manifest for each plugin release

   **Option C: Private/team distribution**
   - Configure in team's `.claude/settings.json`:
     ```json
     {
       "extraKnownMarketplaces": {
         "team-tools": {
           "source": {"source": "github", "repo": "your-org/plugins"}
         }
       }
     }
     ```

5. **Test the release**:
   ```bash
   # Test fresh installation
   /plugin marketplace add your-marketplace-source
   /plugin install your-plugin@marketplace-name
   # Verify functionality, then clean up
   /plugin uninstall your-plugin@marketplace-name
   ```

6. **Announce and maintain**:
   - GitHub releases (optional)
   - Team notifications
   - Monitor for issues and user feedback
   - Plan maintenance updates

## Critical Rules

**Always follow these** (from `references/plugin-structure.md`):

1. **`.claude-plugin/` contains ONLY manifests** (`plugin.json` and optionally `marketplace.json`)
   - ❌ Don't put skills, commands, or other components inside
   - ✅ Put them at plugin root

2. **Use `${CLAUDE_PLUGIN_ROOT}` for all paths in config files**
   - Makes plugin portable across systems
   - Required for hooks, MCP servers, scripts

3. **Use relative paths in `plugin.json`**
   - Start with `./`
   - Relative to plugin root

4. **Make scripts executable**
   - `chmod +x script.sh`
   - Required for hooks and MCP servers

## Resources in This Skill

- **`references/plugin-structure.md`** - Directory layout, file formats, component syntax
- **`references/common-patterns.md`** - When to use each plugin pattern, examples
- **`references/troubleshooting.md`** - Debug guide for common issues
- **`examples/simple-greeter-plugin/`** - Minimal working plugin (one skill)
- **`examples/full-featured-plugin/`** - Complete plugin with all components

## Cross-References

For deep dives into official documentation, use the `working-with-claude-code` skill to access:
- `plugins.md` - Plugin development overview
- `plugins-reference.md` - Complete API reference
- `skills.md` - Skill authoring guide
- `slash-commands.md` - Command format
- `hooks.md`, `hooks-guide.md` - Hook system
- `mcp.md` - MCP server integration
- `plugin-marketplaces.md` - Distribution

## Best Practices

1. **Start simple** - Begin with minimal structure, add complexity when needed
2. **Test frequently** - Install → test → uninstall → modify → repeat
3. **Use examples** - Copy patterns from working plugins
4. **Follow conventions** - Match style of existing plugins
5. **Document everything** - Clear README helps users and future you
6. **Version properly** - Use semantic versioning (major.minor.patch)

## Workflow Summary

```
Plan → Choose pattern, review examples
Create → Make structure, write manifests
Add → Build components (skills, commands, etc.)
Test → Install via dev marketplace
Debug → Use troubleshooting guide
Release → Version, tag, distribute via marketplace
Maintain → Monitor, update, support users
```

**The correct path is the fast path.** Use references, follow patterns, test frequently.
