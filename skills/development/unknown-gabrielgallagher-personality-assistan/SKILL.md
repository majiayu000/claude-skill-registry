---
name: registry-management
description: Guide for adding and managing entries in the personality-assistant-registry. Use when adding MCP servers, skills, bundles, templates, or heartbeat tasks to the registry.
---

# Registry Management

## Overview

The `personality-assistant-registry` provides MCP server definitions and templates for the desktop app.

Primary files:
- `registry.json` (source of truth)
- `templates/` JSON files (human-editable copies; keep in sync)
- `docs/` markdown referenced by `docs.path`

## Registry Structure

```json
{
  "version": "X.Y.Z",
  "updatedAt": "ISO timestamp",
  "entries": [ /* MCP server definitions */ ],
  "templates": [ /* Prompts, skills, bundles, presets */ ]
}
```

## Adding MCP Server Entries

Add to the `entries` array:

```json
{
  "id": "my-mcp",
  "name": "My MCP Server",
  "summary": "Short description",
  "version": "1.0.0",
  "homepage": "https://github.com/...",
  "category": "workspace|communication|developer-tools|analytics|etc",
  "docs": {
    "path": "docs/my-mcp.md"
  },
  "runtime": {
    "preferred": "native|node",
    "fallback": "native|node"
  },
  "install": {
    "method": "manual|command",
    "instructions": "For manual installs...",
    "command": "npx -y @scope/mcp-server",
    "notes": "Required env vars..."
  },
  "artifacts": [
    {
      "platform": "windows|macos|linux",
      "arch": "x86_64|aarch64",
      "url": "https://github.com/.../releases/download/vX.Y.Z/file.zip",
      "sha256": "hash...",
      "filename": "file.zip",
      "entrypoint": "dist/index.js",
      "size": 12345
    }
  ],
  "env": [
    {
      "key": "API_TOKEN",
      "type": "secret|string|boolean|enum",
      "required": true,
      "label": "API Token",
      "help": "Description...",
      "placeholder": "...",
      "default": "...",
      "values": ["option1", "option2"],
      "advanced": false,
      "picker": "file|directory",
      "multiline": false
    }
  ]
}
```

Notes:
- `install.method: "command"` should be non-interactive (`npx -y ...`), especially for `mcp-remote`.
- `docs.path` must be a repo-relative file committed to the registry repo (no local absolute paths).
- `requires` values must reference `entries[].id` and must not include `mcp:` prefixes.

## Adding Templates

Templates go in the `templates` array. Template types:

- `assistant-prompt` - Agent templates shown in Discover -> Agent Templates
- `assistant-preset` - Model presets shown in Discover -> Models & presets
- `heartbeat-task` - Background task prompts
- `skill` - Reusable skill definitions shown in Discover -> Skills
- `skill-bundle` - Skill pack metadata (Superpowers-style)
- `plugin` - Plugin definitions

### Agent Templates (assistant-prompt)

```json
{
  "id": "my-template",
  "type": "assistant-prompt",
  "name": "My Template",
  "summary": "Short description",
  "tags": ["tag1", "tag2"],
  "requires": ["some-mcp-id"],
  "prompt": "System prompt for this assistant...",
  "suggestions": ["A useful starter prompt", "Another suggested question"]
}
```

### Heartbeat Tasks

```json
{
  "id": "my-heartbeat",
  "type": "heartbeat-task",
  "name": "My Task",
  "summary": "Short description",
  "tags": ["tag1"],
  "requires": ["slack-mcp"],
  "task": {
    "prompt": "HEARTBEAT TASK: ...\n\n1. Step one\n2. Step two",
    "intervalMinutes": 60,
    "useGlobalSources": true,
    "sources": [],
    "schemaTargets": ""
  }
}
```

### Skills

```json
{
  "id": "my-skill",
  "type": "skill",
  "name": "My Skill",
  "summary": "Short description",
  "tags": ["tag1", "tag2"],
  "prompt": "Description of when to use this skill and what it does..."
}
```

### Skill Bundles

Use `skill-bundle` to describe packs that need a bootstrap, shared install, or
cross-skill workflow (e.g., Superpowers). Keep bundle metadata lightweight and
put detailed instructions in `docs`.

```json
{
  "id": "superpowers-bundle",
  "type": "skill-bundle",
  "name": "Superpowers",
  "summary": "Workflow bundle of interdependent skills and bootstraps.",
  "version": "x.y.z",
  "docs": { "url": "https://github.com/obra/superpowers" },
  "skills": ["superpowers:brainstorming", "superpowers:writing-plans"],
  "install": {
    "method": "manual",
    "instructions": "Claude Code: /plugin install superpowers@superpowers-marketplace\nCodex: clone https://github.com/obra/superpowers into ~/.codex/superpowers and add the AGENTS bootstrap.",
    "notes": "Codex CLI currently requires a CJS/ESM fix for skills-core import."
  },
  "backends": ["claude-code", "codex-cli"]
}
```

## External Skill Packs (Normalization)

When adding skills from external repos (Superpowers, Automattic/agent-skills):

1. Inspect the repo to identify `SKILL.md` files or `skill.yaml`.
2. Extract name/summary and convert each to `templates[]` entries (`type: "skill"`).
3. Add a `skill-bundle` entry if the pack requires shared bootstrap or workflow.
4. Inject a compatibility preamble for multi-backend usage (tool mapping + fallbacks).
5. Update the desktop app types/UI if you add a new template type.

Example conversion:
```json
{
  "id": "wp-block-development",
  "type": "skill",
  "name": "WP Block Development",
  "summary": "Gutenberg blocks: block.json, attributes, rendering, deprecations.",
  "tags": ["wordpress", "gutenberg", "blocks"],
  "prompt": "Use when developing WordPress (Gutenberg) blocks..."
}
```

## Multi-Backend Compatibility

For Claude Code, Codex, and OpenAI Agents, include deterministic tool mapping:

- Define canonical tools (read, write, shell, mcp, plan)
- Map to backend-specific names (ex: `TodoWrite -> update_plan`, `Bash -> shell_command`)
- Note unsupported features (subagents, web search, image support) in the prompt

When a skill is backend-specific, declare the scope in docs or tags and provide
fallback instructions for other backends.

## Validation Checklist

After editing `registry.json`:

1. **Validate JSON syntax:**
   ```bash
   node -e "JSON.parse(require('fs').readFileSync('registry.json', 'utf8')); console.log('JSON valid')"
   ```

2. **Update version fields:**
   - Increment `version` at the top (semver: major.minor.patch)
   - Update `updatedAt` timestamp

3. **Check required fields:**
   - MCP entries: `id`, `name`, `summary`, `runtime`, `install`
   - Templates: `id`, `type`, `name`, `summary`
   - `requires` values match `entries[].id` (no `mcp:` prefixes)

4. **Update app types when adding new template types:**
   - `apps/desktop/src/lib/registry.ts` (type unions)
   - `apps/desktop/src/pages/Discover.tsx` (filters and labels)

## Desktop App Code References

The registry is consumed by:

- `apps/desktop/src/lib/registry.ts` - TypeScript types
- `apps/desktop/src/pages/Discover.tsx` - Template display
- `apps/desktop/src/pages/McpStore.tsx` - MCP management
- `apps/desktop/DISCOVER.md` - IA reference and registry model notes
- `apps/desktop/CLAUDE.md` - Registry update instructions

Key type definitions:

```typescript
// RegistryTemplate types
type: "heartbeat-task" | "assistant-prompt" | "assistant-preset" | "skill" | "skill-bundle" | "plugin"

// Discover.tsx filters:
// - Agent Templates: templates.filter(t => t.type === "assistant-prompt")
// - Skills: templates.filter(t => t.type === "skill" or "skill-bundle")
// - Prompt Templates: types "assistant-prompt", "heartbeat-task", "plugin"
```

## Common Mistakes to Avoid

1. **Putting skills in wrong location**: Skills go in `templates[]` with `type: "skill"`, not a separate `skills[]` array
2. **Missing type field**: Templates must have a `type` field
3. **Invalid JSON**: Always validate after editing
4. **Stale version**: Remember to bump `version` and `updatedAt`
5. **Interactive install commands**: Use `npx -y ...` to avoid prompts
6. **Wrong requires syntax**: Use plain MCP IDs (no `mcp:` prefix)
7. **Docs pointing to local paths**: `docs.path` must be repo-relative and committed
8. **New template types without UI support**: Update `registry.ts` + `Discover.tsx`
