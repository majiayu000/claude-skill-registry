---
name: serena-mcp-agent
description: Expert integration for the Serena MCP Server - a powerful coding agent toolkit providing IDE-like semantic code understanding to LLMs. This skill should be used when working with codebases through Serena tools, setting up Serena projects, performing semantic code navigation and editing, managing project memories, debugging complex automation workflows, or integrating Serena with Claude Desktop, Claude Code, Codex, ChatGPT, or custom agents. Triggers on Serena tool usage, project activation/onboarding, symbolic code operations (find_symbol, replace_symbol_body, etc.), memory management (write_memory, read_memory), and MCP server configuration. Use for large/complex codebases requiring structural understanding, refactoring tasks, and token-efficient code operations.
---

# Serena MCP Agent Integration

Serena transforms LLMs into fully-featured coding agents with IDE-like intelligence by leveraging the Language Server Protocol (LSP) for structural code understanding.

## Core Value Proposition

| Capability | Benefit |
|------------|---------|
| Semantic code retrieval | Navigate by symbols, not text - 30x+ token reduction |
| Surgical editing | Modify function bodies while preserving structure |
| Project memory | Persist knowledge across sessions in `.serena/memories/` |
| Multi-client support | Claude Desktop, Claude Code, Codex, ChatGPT, custom agents |

## Project Lifecycle

### 1. Activation

Activate project before any operations:
```
"Activate the project /path/to/my_project"
```

First-time activation creates `.serena/project.yml` with default settings.

### 2. Onboarding

Run automatically on first session. Creates memories in `.serena/memories/`:
- `tech_stack_and_dependencies.md`
- `code_style_and_conventions.md`
- `task_completion_guidelines.md`

If not auto-triggered:
```
"Start the Serena onboarding process for this project."
```

**Critical:** Start NEW conversation after onboarding (context fills up during analysis).

### 3. Indexing (Large Projects)

Pre-index to prevent tool timeouts:
```bash
serena project index
```

Run once; auto-updates during use.

## Tool Usage Strategy

**Priority Order (Prefer Higher):**

1. **Symbolic tools** - Most efficient, LSP-powered
   - `get_symbols_overview` → File structure without reading content
   - `find_symbol` → Locate definitions precisely
   - `find_referencing_symbols` → Impact analysis before changes
   - `replace_symbol_body` → Rewrite functions safely

2. **Line-based tools** - When symbols don't apply
   - `replace_lines`, `insert_at_line`, `delete_lines`

3. **Full file operations** - Last resort
   - `read_file`, `create_text_file`

**See:** `references/tools-reference.md` for complete tool taxonomy.

## Memory Management

Persist knowledge in `.serena/memories/`:

| Tool | Purpose |
|------|---------|
| `write_memory` | Save contracts, schemas, progress |
| `read_memory` | Load prior session context |
| `list_memories` | Discover available memories |
| `prepare_for_new_conversation` | Generate continuation summary |
| `summarize_changes` | Document session work |

**Pattern:** End sessions with `summarize_changes` → `write_memory`.

## Thinking Tools

Force self-reflection during complex operations:

| Tool | When to Use |
|------|-------------|
| `think_about_collected_information` | Before implementing |
| `think_about_task_adherence` | During long operations |
| `think_about_whether_you_are_done` | Before declaring complete |

## Client Configuration

**Claude Desktop:** Edit `claude_desktop_config.json`
```json
{
  "mcpServers": {
    "serena": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/oraios/serena",
               "serena", "start-mcp-server", "--context", "desktop-app"]
    }
  }
}
```

**Claude Code:** From project directory:
```bash
claude mcp add serena -- uvx --from git+https://github.com/oraios/serena \
  serena start-mcp-server --context ide-assistant --project "$(pwd)"
```

**See:** `references/client-setup.md` for Codex, ChatGPT, Docker, etc.

## Contexts and Modes

**Contexts** (set at startup, immutable):
- `desktop-app` - Claude Desktop (full toolset)
- `claude-code` - Claude Code (no duplicates)
- `ide-assistant` - IDE extensions (minimal tools)
- `codex` - OpenAI Codex
- `chatgpt` - ChatGPT via MCPO

**Modes** (combinable, switchable):
- `editing` + `interactive` - Standard development (default)
- `planning` - Analysis before implementation
- `one-shot` - Single-response tasks
- `no-onboarding` - Skip if memories exist

Switch dynamically: "Switch to planning mode"

**See:** `references/contexts-and-modes.md` for full reference.

## Security Configuration

In `.serena/project.yml`:
```yaml
read_only: true  # Disable all editing (analysis only)
excluded_tools:
  - execute_shell_command  # Always disable for untrusted contexts
```

**Non-negotiables:**
1. Use version control (Git) for all projects
2. Disable `execute_shell_command` unless explicitly needed
3. Set `read_only: true` for code review/analysis tasks
4. Never expose MCPO API keys

## Debugging Framework

For complex automation workflows (n8n, Zapier, etc.):

1. **Behavior Contract** - Document expected behavior before changes
2. **Snapshot Before** - Capture current state
3. **Parity Grid** - Map contract → current → fix required
4. **Dry-Run** - Validate changes before applying
5. **Apply + Validate** - Execute with proof
6. **Memory Harden** - Persist final state

**See:** `references/debugging-framework.md` for canonical prompts and workflow.

## Session Protocol

**Start:**
1. Verify project activation: `get_current_config`
2. Check onboarding: `check_onboarding_performed`
3. Load relevant memories: `list_memories` → `read_memory`
4. Run build/type-check command (establish baseline)

**During:**
- Read files BEFORE editing (prevent duplicates)
- Use symbolic tools preferentially
- Run validation after each change
- Use thinking tools for complex tasks

**End:**
1. Final validation (build/lint/test)
2. `summarize_changes` → `write_memory`
3. For continuation: `prepare_for_new_conversation`

## When to Use Serena

**Optimal:**
- Large/complex/legacy codebases
- Refactoring across multiple files
- Analyzing dependencies and architecture
- Token-sensitive operations

**Not Needed:**
- New empty projects (nothing to analyze)
- Single-file scripts
- When entire context fits easily

## Dashboard

Monitor operations at: `http://localhost:24282/dashboard/index.html`

View: tool calls, logs, configuration, active languages.
