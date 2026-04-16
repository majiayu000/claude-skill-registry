---
name: export-config
description: Export dotforge configuration to other AI code editors (Cursor, Codex, Windsurf, OpenClaw).
---

# Export Configuration

Convert the current project's dotforge configuration into formats compatible with other AI coding tools.

## Input
$ARGUMENTS contains the target format: `cursor`, `codex`, `windsurf`, or `openclaw`.

If no argument provided, show available targets and ask.

## Step 1: Read current configuration

Read these files from the current project:
- `CLAUDE.md` — project instructions
- `.claude/rules/*.md` — contextual rules (strip YAML frontmatter)
- `.claude/settings.json` — permissions and hooks

If none exist, error: "No dotforge configuration found. Run `/forge bootstrap` first."

## Step 2: Transform based on target

### `cursor` → `.cursorrules`

Generate a single `.cursorrules` file at project root:
1. Extract content from `CLAUDE.md` (skip forge markers)
2. Append all rules from `.claude/rules/*.md` (strip YAML frontmatter — `globs:`, `paths:`, `alwaysApply:`, etc. — keep content)
3. Convert deny list to text: "DO NOT: read/modify files matching: .env, *.key, *.pem, *credentials*"
4. Convert hooks to text instructions: "Before executing bash commands, check for destructive patterns: rm -rf, DROP TABLE, force push"
5. Wrap in a single markdown document

### `codex` → `AGENTS.md`

Generate `AGENTS.md` at project root:
1. Start with project context from `CLAUDE.md`
2. Append rules as "## Rules" section
3. Convert permissions to "## Permissions" section: list allowed and denied commands
4. Add "## Workflow" section from agent orchestration rules if present
5. Format as flat markdown (Codex expects simple instructions)

### `windsurf` → `.windsurfrules`

Generate `.windsurfrules` at project root:
1. Same content extraction as cursor
2. Windsurf format is similar to `.cursorrules` — single markdown file
3. Add Windsurf-specific header: "You are an AI assistant working on this project."
4. Append all rules and converted hooks/permissions

### `openclaw` → `~/.openclaw/skills/{project}/SKILL.md` + workspace agent config

Generate an OpenClaw workspace skill for the current project:

1. Create skill directory: `~/.openclaw/skills/{project-slug}/`
2. Generate `SKILL.md` with frontmatter:
   ```yaml
   ---
   name: {project-slug}
   description: "AI assistant for {project-name} — {stack description}"
   user-invocable: true
   metadata: {"openclaw":{"requires":{"bins":["claude"]}}}
   ---
   ```
3. Body content:
   - Project context from `CLAUDE.md` (skip forge markers, keep substance)
   - Build/test commands as executable instructions
   - Rules converted to behavioral instructions (strip `globs:` frontmatter)
   - Deny list as explicit "NEVER read or modify" instructions
   - Hook logic as text: "Before executing commands, check for destructive patterns: ..."
   - Agent roles summarized: "For architecture decisions, think like an architect. For security, scan for OWASP top 10."
4. Add execution section:
   ```markdown
   ## Execution
   When asked to work on this project:
   1. cd to {project-path}
   2. Use `claude --print "<task>"` to execute via Claude Code
   3. Return the result formatted for the current channel
   ```

Additionally, if the project has specific commands (`.claude/commands/*.md`), list them as available actions:
```markdown
## Available commands
- /audit — audit project configuration
- /health — health check
- /debug — assisted debugging
- /review — code review
```

### What OpenClaw export preserves vs loses

| Feature | Preserved | How |
|---------|-----------|-----|
| Project context | ✅ | CLAUDE.md content in skill body |
| Rules | ✅ | Converted to text instructions |
| Deny list | ✅ | "NEVER read/modify" instructions |
| Hook logic | ⚠️ Partial | Text instructions (no enforcement) |
| Agent orchestration | ⚠️ Partial | Summarized as behavioral guidance |
| Audit scoring | ✅ | Via `claude --print "/forge audit"` bridge |
| Session metrics | ❌ | OpenClaw sessions don't generate dotforge metrics |
| Stack-specific auto-loading | ❌ | All rules flattened into single skill |

## Step 3: Handle conflicts

Before writing:
1. Check if target file already exists
2. If exists: show diff preview and ask user to confirm overwrite
3. If user declines: suggest alternative filename (e.g., `.cursorrules.dotforge`)

## Step 4: Report

Show:
```
Export complete: {{target}}
  Output: {{filename}}
  Sources: CLAUDE.md, {{N}} rules, settings.json
  Note: hooks and deny list converted to text instructions (no enforcement outside Claude Code)
```

Warn: "Exported rules are advisory only. Hook enforcement (destructive command blocking) only works in Claude Code."

## Limitations

- Hooks cannot be enforced outside Claude Code — converted to text instructions
- Agent orchestration is Claude Code-specific — simplified to workflow instructions
- Stack-specific rules are included but glob-based auto-loading is Claude Code-only
