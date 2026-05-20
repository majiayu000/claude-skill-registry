---
name: claude-code
version: 2.0.0
description: '[Utilities] Claude Code CLI setup, configuration, troubleshooting, and feature guidance. Triggers on claude code setup, hook not firing, MCP connection, context limit, skill creation, slash command setup.'

allowed-tools: Read, Bash, Grep, Glob
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI may ask user whether to skip.

## Quick Summary

**Goal:** Help users install, configure, troubleshoot, and extend Claude Code CLI (hooks, MCP, skills, commands).

**Workflow:**

1. **Categorize** — Identify problem type (Setup, Hooks, MCP, Context, Extensibility, Config)
2. **Diagnose** — Follow category-specific diagnostic steps
3. **Fix & Verify** — Apply solution and confirm it resolves the issue

**Key Rules:**

- Not for writing application code -- use feature/fix/refactor skills instead
- Never modify settings without user approval
- For hooks: check event type, script executability, and JSON output format

# Claude Code

## Purpose

Help users install, configure, troubleshoot, and extend Claude Code CLI -- Anthropic's agentic coding tool with skills, hooks, MCP servers, and slash commands.

## When to Use

- Setting up Claude Code for the first time (installation, authentication)
- Troubleshooting hooks that don't fire or produce errors
- Diagnosing MCP server connection failures
- Understanding or resolving context window limits
- Creating or modifying slash commands and agent skills
- Configuring settings (model, allowed tools, output style)

## When NOT to Use

- Writing application code -- use `feature-implementation`, `fix`, or `refactoring` skills
- Creating MCP servers from scratch -- use `mcp-builder` skill
- Managing existing MCP server connections -- use `mcp-management` skill
- AI prompt engineering -- use `ai-artist` skill

## Prerequisites

- Access to `.claude/` directory in the project root
- For hooks: read `.claude/hooks/` directory structure
- For skills: read `.claude/skills/` directory structure

## Workflow

### Step 1: Identify the Problem Category

| User Says                                       | Category       | Go To   |
| ----------------------------------------------- | -------------- | ------- |
| "install", "set up", "authenticate"             | Setup          | Step 2A |
| "hook not firing", "hook error"                 | Hook Issues    | Step 2B |
| "MCP not connecting", "MCP error"               | MCP Issues     | Step 2C |
| "context too long", "compaction", "token limit" | Context Issues | Step 2D |
| "create skill", "create command"                | Extensibility  | Step 2E |
| "configure", "settings", "model"                | Configuration  | Step 2F |

### Step 2A: Setup

1. Check prerequisites: Node.js 18+, npm
2. Verify authentication: `claude auth status`
3. IF auth fails: guide through `claude auth login`
4. Verify project detection: check for `CLAUDE.md` in project root

### Step 2B: Hook Issues

1. Read the hook file causing issues
2. Check hook event type matches expected trigger (PreToolUse, PostToolUse, SessionStart, Stop, SubagentStop)
3. Verify hook script is executable and has correct shebang
4. Check `.claude/settings.json` for hook registration
5. Test hook in isolation: run the script directly with mock input
6. Check for syntax errors in hook output (must be valid JSON for PreToolUse/PostToolUse)

**Common fixes:**

- Hook not firing: wrong event name or tool matcher pattern
- Hook errors: script not finding dependencies (check relative paths)
- Hook blocks unexpectedly: PreToolUse returning `{ "decision": "block" }` incorrectly

### Step 2C: MCP Issues

1. Check `.claude/settings.json` for MCP server configuration
2. Verify the MCP server process can start: run the command manually
3. Check environment variables (API keys, tokens) are set
4. Test connectivity: `claude mcp list` to see registered servers
5. IF timeout: increase timeout in config or check network

**Common fixes:**

- "Connection refused": MCP server not running or wrong port
- "Authentication failed": expired or missing API token
- "Tool not found": MCP server registered but tool name mismatch

### Step 2D: Context Issues

1. Check current context usage (Claude will report when near limit)
2. IF approaching limit: suggest `/compact` command
3. Review if large files are being read unnecessarily
4. Check for recovery files in `/tmp/ck/swap/` after compaction
5. Verify `post-compact-recovery` hook is configured for session continuity

### Step 2E: Extensibility

1. For skills: read `references/agent-skills.md` for structure
2. For custom slash commands: create skills in `.claude/skills/{name}/SKILL.md`
3. Verify SKILL.md frontmatter has required fields (name, version, description)
4. Test: invoke the skill/command and verify it loads

### Step 2F: Configuration

1. Read `references/configuration.md` for settings hierarchy
2. Settings locations: `.claude/settings.json` (project), `~/.claude/settings.json` (user)
3. IMPORTANT: Never modify settings without user approval
4. Common settings: model selection, allowed tools, output verbosity

### Step 3: Verification

- Confirm the fix resolves the user's issue
- Document any configuration changes made
- Warn if changes affect other team members (project-level settings)

## Output Format

```markdown
## Claude Code: [Issue/Task Summary]

### Problem

[What was wrong or what was requested]

### Solution

[Step-by-step fix or setup instructions]

### Files Changed

[List any config files modified, with before/after]

### Verification

[How to confirm the fix works]
```

## Examples

### Example 1: Hook Not Firing

**User**: "My PreToolUse hook for blocking large file reads isn't triggering"

**Diagnosis**:

1. Read `.claude/settings.json` -- hook registered under `hooks.PreToolUse`
2. Check tool matcher: `"matcher": "Read"` -- correct
3. Run script directly: `node .claude/hooks/block-large-reads.cjs` -- works
4. **Found**: Hook command uses `%CLAUDE_PROJECT_DIR%` but runs from wrong CWD

**Fix**: Update hook command to use absolute path or verify `%CLAUDE_PROJECT_DIR%` resolves correctly. Check that the hook entry in settings uses the correct variable syntax for the platform (Windows vs Unix).

### Example 2: Setting Up a New Slash Command

**User**: "I want a /deploy command that runs our staging deployment"

**Steps**:

1. Create `.claude/skills/deploy/SKILL.md`:

```markdown
Deploy to staging environment.

Run the following steps:

1. Verify all tests pass: `npm test`
2. Build the project: `npm run build`
3. Deploy: `npm run deploy:staging`
4. Report deployment status
```

2. Test: type `/deploy` in Claude Code CLI
3. Verify: command appears in autocomplete and executes the workflow

## Reference Files

Load these for detailed guidance on specific topics:

| Topic           | File                                |
| --------------- | ----------------------------------- |
| Installation    | `references/getting-started.md`     |
| Slash commands  | `references/slash-commands.md`      |
| Skills creation | `references/agent-skills.md`        |
| MCP servers     | `references/mcp-integration.md`     |
| Hooks system    | `references/hooks-comprehensive.md` |
| Configuration   | `references/configuration.md`       |
| Troubleshooting | `references/troubleshooting.md`     |
| Enterprise      | `references/enterprise-features.md` |

## Related Skills

- `mcp-builder` -- for creating new MCP servers from scratch
- `mcp-management` -- for managing existing MCP server connections
- `skill-creator` -- for creating new agent skills with best practices

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
