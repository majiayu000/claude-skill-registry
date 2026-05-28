---
name: managing-plugins
description: Creates, packs, bundles, and manages Claude Code plugins with manifest generation, directory structure, marketplace configuration. Use when user asks how plugins work, what plugins are, explaining plugin structure, understanding plugin.json manifest, describing plugin bundling process, creating plugins, bundling skills/commands/hooks/MCPs, generating plugin.json, setting up marketplaces, or distributing team-shared functionality.
---

# Managing Plugins

## When to Use This Skill

Activate when user mentions: plugin creation, bundling, packaging, plugin.json, marketplace, team distribution, .claude-plugin, plugin structure

## Terminology

**Manifest**: Refers to the plugin.json file located at `.claude-plugin/plugin.json`. These terms are used interchangeably throughout this skill.

**Subagents**: Referred to as "agents/" directory in plugins. Subagents are specialized agents started as subordinate processes from Claude Code's main agent instance. For detailed subagent creation guidance, see the managing-agents skill.

## Core Operations

### OP1: Create Plugin Structure

Input: plugin name, components list
Output: directory structure with manifest

Process:
1. Use Bash tool: `mkdir -p plugin-name/.claude-plugin` to create plugin directory
2. Use Write tool to create plugin-name/.claude-plugin/plugin.json with required fields: name, description, version, author.name
3. Use Bash tool: `mkdir -p plugin-name/{commands,skills,hooks,agents}` to create component directories
4. For each component file: Use Bash tool `cp -r source plugin-name/target-dir` to copy files to appropriate directories
5. Verify structure created:
   - Use Read tool to confirm plugin-name/.claude-plugin/plugin.json exists and is readable
   - Use Bash tool: `ls -la plugin-name` to list all created directories
   - Expected output includes: .claude-plugin/, commands/, skills/, hooks/, agents/
6. Validate structure (OP4)

Resulting directory structure:
```
plugin-name/
  .claude-plugin/
    plugin.json
  commands/
  skills/
  hooks/
  agents/
```

For detailed plugin.json schema and directory structure requirements, load plugin-spec.md

### OP2: Bundle Components by Prefix

Input: prefix pattern (e.g., "git")
Output: plugin with all matching components

Working directory assumptions:
- Search from user's .claude directories (~/.claude and .claude)
- Or use explicit paths if provided by user

Detection process:
1. Use Glob tool with pattern `commands/**/{prefix}-*.md` to find matching command files
2. Use Glob tool with pattern `skills/**/{prefix}-*/**` to find matching skill directories
3. Use Glob tool with pattern `hooks/hooks.json` to check if hooks config exists
   - If exists: Use Read tool to load hooks/hooks.json
   - Parse JSON to find event handlers with names matching prefix pattern
4. Use Glob tool with pattern `.mcp.json` to check if MCP config exists
   - If exists: Use Read tool to load .mcp.json
   - Parse JSON to check mcpServers section for keys starting with prefix
5. Collect all matched file paths into components list

Bundling process:
1. Create plugin structure (OP1)
2. For each matched component:
   - Use Bash tool: `cp -r source-path plugin-name/target-dir` to copy files
   - Preserve relative directory structure
3. Use Read tool to load first matched component's frontmatter/metadata
4. Generate manifest fields (name, description) from component metadata
5. Verify bundling completed:
   - Use Bash tool: `find plugin-name -type f` to list all bundled files
   - Confirm count matches expected number of components
6. Validate no broken references (OP4)

For detailed component formats and path rules, load plugin-spec.md

### OP3: Create Marketplace Config

Input: plugin paths, marketplace name, owner
Output: marketplace.json

Template:
```json
{"name":"MARKETPLACE","owner":{"name":"OWNER"},"plugins":[{"name":"NAME","source":"./path","description":"DESC"}]}
```

Sources: local path, git URL, or tarball

For complete marketplace.json schema and source types, load marketplace-spec.md

### OP4: Validate Plugin

Input: plugin directory path
Output: validation status with specific errors if any

Validation sequence:
1. Use Read tool to attempt loading .claude-plugin/plugin.json
   - If fails: Return error "Manifest not found at .claude-plugin/plugin.json"
2. Parse JSON content to extract fields
   - If invalid JSON: Return error "Invalid JSON syntax in plugin.json"
3. Check required field 'name' exists
   - If missing: Return error "Missing required field: name"
4. If 'version' field present: Validate semver format (pattern: MAJOR.MINOR.PATCH)
   - If invalid: Return error "Invalid version format, must be semver (e.g., 1.0.0)"
5. If 'author' field present: Verify it has 'name' subfield
   - If missing author.name: Return error "author object must have 'name' field"
6. Use Glob tool with pattern `plugin-name/**/*.md` to find all markdown files
7. For each .md file: Use Read tool to load and verify YAML frontmatter is valid
   - If invalid YAML: Collect error "Invalid YAML frontmatter in {filepath}"
8. Use Glob tool to list component directories: commands/, skills/, hooks/, agents/
9. For each directory: Verify expected file structure (commands have .md, skills have SKILL.md)
   - If structure invalid: Collect error "Invalid structure in {directory}"
10. Check for duplicate names across components
    - If duplicates found: Return error "Duplicate component names: {list}"
11. If no errors collected: Return "Validation passed"
    - If errors collected: Return all errors as list

For comprehensive validation checklist and debugging guidance, load validation-rules.md

### OP5: Pack for Distribution

Input: plugin dir
Output: ready-to-distribute structure

Steps:
1. Validate plugin (OP4)
2. If .gitignore patterns specified: Use Bash tool to remove matching files
3. If archive requested: Use Bash tool `tar -czf plugin-name.tar.gz -C plugin-name .` to create tarball
4. Use Write tool to create plugin-name/README.md with usage instructions
5. Include installation command in README: `/plugin install name@marketplace`

For semver versioning guidelines and distribution methods, load distribution-guide.md

## Component Integration

**Commands**: Copy to commands/, preserve .md extension, keep frontmatter
**Skills**: Copy entire skill dir to skills/, preserve SKILL.md and supporting files
**Hooks**: Merge hooks.json or copy individual hook configs
**MCPs**: Copy .mcp.json, merge mcpServers section if exists
**Subagents**: Copy to agents/ directory (subordinate agents created via managing-agents skill)

## Context Detection Rules

Prefix matching priority:
1. Exact prefix match (git-commit matches git)
2. Semantic grouping (auth-login, auth-register both auth-related)
3. Explicit file lists override auto-detection
4. Check descriptions for shared keywords

Decision tree for bundling:
1. Count total matches from detection process (OP2 step 5)
2. Check if user provided explicit file list
3. Apply decision logic:

   IF match_count == 0:
   - Generate suggestions: Use Glob to find similar prefixes
   - Use AskUserQuestion tool: "No components found matching prefix '{prefix}'. Did you mean: {suggestions}?"
   - Wait for user response before proceeding

   ELSE IF match_count == 1:
   - Proceed directly to bundling process
   - No user confirmation needed

   ELSE IF match_count >= 2 AND user_provided_explicit_list == false:
   - List all matched components with types (command/skill/hook/mcp)
   - Use AskUserQuestion tool: "Found {count} components matching '{prefix}': {list}. Bundle all matching components or select specific ones?"
   - Wait for user selection

   ELSE IF user_provided_explicit_list == true:
   - Proceed with explicit list only
   - Ignore auto-detected matches

## Progressive References

Load when detailed information needed:

**plugin-spec.md**: Complete plugin.json schema, directory structure requirements, component formats, path rules, environment variables
**marketplace-spec.md**: marketplace.json schema, source types, distribution patterns, installation commands
**distribution-guide.md**: Semver versioning, distribution methods (local/git/team/archive), testing workflow, pre-distribution checklist
**validation-rules.md**: Comprehensive validation checklist, debugging with --debug flag, common issues and fixes, error messages reference

## Anti-Patterns

- Don't include non-plugin files in bundle
- Don't auto-generate descriptions (require user input)
- Don't modify original files (copy only)
- Don't create plugins without validation
- Don't bundle unrelated components

## Quick Checks

- [ ] plugin.json has all required fields
- [ ] Component dirs match actual files
- [ ] No absolute paths in manifests
- [ ] Version is valid semver
- [ ] No broken references
- [ ] Descriptions are specific

## Output Format

Completion report:
- Plugin name and location
- Components included (count by type)
- Validation status
- Installation command
- Next steps

## Error Handling

Common failures:
- Missing required fields → prompt user
- Invalid semver → suggest correction
- Broken references → list broken paths
- Duplicate names → list conflicts
- No components found → show search paths
