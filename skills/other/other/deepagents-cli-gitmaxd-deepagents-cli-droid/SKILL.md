---
name: deepagents-cli
description: |
  Deep Agents CLI reference and usage guide. Use when the user wants to:
  (1) Launch or configure the deepagents terminal coding assistant,
  (2) Set up interactive or non-interactive (automation/CI) agent sessions,
  (3) Manage agent memory, skills, or AGENTS.md context files,
  (4) Configure LLM providers, models, or sandbox execution environments,
  (5) Build scripted workflows or subagent patterns with deepagents.
---

# Deep Agents CLI

Terminal coding agent with persistent memory, skills, sandboxed execution, and 20+ LLM providers. Built on LangGraph. See the [official overview](https://docs.langchain.com/oss/python/deepagents/overview) and [CLI guide](https://docs.langchain.com/oss/python/deepagents/cli/overview).

## Quick Start

```bash
# Interactive session (default agent, default model)
deepagents

# Interactive with specific agent and model
deepagents -a myagent -M anthropic:claude-sonnet-4-5

# Non-interactive one-shot task
deepagents -n "Summarize README.md"

# Non-interactive with shell access
deepagents -n "List Python files and count lines" --shell-allow-list ls,wc,find

# Resume last session
deepagents -r
```

## Core Concepts

### Agents = Isolated Personas

Each agent has its own memory, skills, and AGENTS.md context file:

```
~/.deepagents/<agent_name>/
├── AGENTS.md          # Always-loaded context (preferences, conventions)
├── memories/          # Auto-saved topic memories
└── skills/            # User-level skills
```

```bash
deepagents -a researcher      # Use "researcher" agent
deepagents -a coder           # Use "coder" agent
deepagents list               # List all agents
deepagents reset --agent NAME # Clear agent memory
```

### Memory vs Skills

| Aspect | Memory (AGENTS.md + memories/) | Skills (SKILL.md) |
|--------|-------------------------------|-------------------|
| Loading | Always injected at startup | On-demand via progressive disclosure |
| Purpose | Preferences, conventions | Task-specific workflows |
| Use when | Context is always relevant | Instructions are large or situational |

See [Memory & Persistence](references/memory-and-persistence.md) and [Skills System](references/skills-system.md) for details on each system.

### Two Operating Modes

| Mode | Command | Use Case |
|------|---------|----------|
| **Interactive** | `deepagents` | Exploration, conversation, complex tasks |
| **Non-interactive** | `deepagents -n "task"` | Automation, scripting, CI/CD |

## Interactive Mode

Launch the REPL with `deepagents`. Key controls (see [CLI Reference](references/cli-reference.md) for the complete list):

| Action | Key/Command |
|--------|-------------|
| Submit | `Enter` |
| Newline | `Shift+Enter`, `Ctrl+J`, `Alt+Enter`, or `Ctrl+Enter` |
| Expand/collapse tool output | `Ctrl+E` |
| Toggle auto-approve | `Shift+Tab` or `Ctrl+T` |
| Select all text | `Ctrl+A` |
| File autocomplete | `@filename` |
| Run shell command | `!git status` |
| Interrupt | `Escape` or `Ctrl+C` |
| Exit | `Ctrl+D` or `/quit` |

### Slash Commands

```
/model               # Interactive model selector
/model provider:name # Switch to specific model
/remember [context]  # Update memory and skills from conversation
/tokens              # Show token usage
/clear               # Clear conversation history and start new thread
/threads             # Browse and resume previous threads
/trace               # Open current thread in LangSmith
/changelog           # Open CLI changelog in browser
/docs                # Open documentation in browser
/feedback            # File bug report or feature request
/version             # Show version
/quit                # Exit CLI (alias: /q)
/help                # Show all commands
```

## Non-Interactive Mode

For automation and scripting — runs a single task and exits (see [Workflows & Patterns](references/workflows.md) for CI/CD recipes):

```bash
# Basic task
deepagents -n "Analyze this codebase for security issues"

# With shell access (default: no shell in non-interactive)
deepagents -n "Run tests and report failures" --shell-allow-list recommended
deepagents -n "Search logs for errors" --shell-allow-list ls,cat,grep

# Auto-approve all tool calls
deepagents --auto-approve -n "Generate docs for all modules"

# Specific model
deepagents -M ollama:qwen3:8b -n "Explain this code"
```

**Shell access in non-interactive mode** is disabled by default. Use `--shell-allow-list`:
- `recommended` — safe defaults
- `ls,cat,grep,...` — explicit comma-separated list

### Piping and stdin

The CLI accepts piped input via stdin. When input is piped, the CLI automatically runs non-interactively:

```bash
# Pipe content for analysis
echo "Explain this code" | deepagents
cat error.log | deepagents -n "What's causing this error?"
git diff | deepagents -n "Review these changes"

# Clean output for piping to other commands
deepagents -n "Generate a .gitignore for Python" -q > .gitignore
deepagents -n "List dependencies" -q --no-stream | sort
```

When piped input is combined with `-n` or `-m`, the piped content is prepended to the flag's value. The maximum piped input size is 10 MiB.

## Model Selection

See [Providers & Models](references/providers.md) for all 20+ supported providers, API key setup, and config.toml format. See also the [official providers guide](https://docs.langchain.com/oss/python/deepagents/cli/providers).

### At Launch

```bash
deepagents -M anthropic:claude-sonnet-4-5
deepagents -M openai:gpt-4o
deepagents -M ollama:qwen3:8b
```

### During Session

```bash
/model                          # Interactive picker
/model anthropic:claude-opus-4-6  # Direct switch
```

### Default Model

```bash
deepagents --default-model anthropic:claude-sonnet-4-5  # Set default
deepagents --default-model                               # Show current
deepagents --clear-default-model                         # Clear default
```

### Resolution Order

1. `-M` flag (always wins)
2. `[models].default` in `~/.deepagents/config.toml`
3. `[models].recent` (last `/model` switch, auto-saved)
4. First available API key: `OPENAI_API_KEY` → `ANTHROPIC_API_KEY` → `GOOGLE_API_KEY` → `GOOGLE_CLOUD_PROJECT`

## Skills Management

See [Skills System](references/skills-system.md) for the full SKILL.md format and progressive disclosure. See also the [official skills docs](https://docs.langchain.com/oss/python/deepagents/skills).

```bash
deepagents skills create my-skill             # Create user skill
deepagents skills create my-skill --project   # Create project skill
deepagents skills list                        # List user skills
deepagents skills list --project              # List project skills
deepagents skills info my-skill               # Show skill details
deepagents skills delete my-skill             # Delete user skill
deepagents skills delete my-skill --project   # Delete project skill
```

**User skills:** `~/.deepagents/<agent>/skills/`
**Project skills:** `<project>/.deepagents/skills/` (requires `.git` in project root)

Project skills override user skills with the same name.

## Sandbox Execution

Run agent code in isolated environments (see [Sandboxes](references/sandboxes.md) for setup guides and [official sandbox docs](https://docs.langchain.com/oss/python/deepagents/sandboxes)):

```bash
deepagents --sandbox modal --sandbox-setup ./setup.sh
deepagents --sandbox runloop
deepagents --sandbox daytona
deepagents --sandbox langsmith
deepagents --sandbox-id EXISTING_ID    # Reuse sandbox
```

Sandbox providers: **Modal** (ML/GPU), **Runloop** (disposable devboxes), **Daytona** (fast cold starts), **LangSmith** (cloud deployment).

## Built-in Tools

| Tool | Description | Approval Required |
|------|-------------|:-:|
| `ls` | List files/directories | — |
| `read_file` | Read file contents; supports images (`.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`) | — |
| `write_file` | Create/overwrite files | ✓ |
| `edit_file` | Targeted string replacements | ✓ |
| `glob` | Find files by pattern | — |
| `grep` | Search file contents | — |
| `shell` | Execute shell commands (local) | ✓ |
| `execute` | Execute in sandbox | ✓ |
| `web_search` | Search web (Tavily) | ✓ |
| `fetch_url` | Fetch web pages as markdown | ✓ |
| `task` | Delegate to [subagents](references/sdk-customization.md#subagents) | ✓ |
| `write_todos` | Task planning/tracking | — |

Use `--auto-approve` or `Shift+Tab` in REPL to bypass approval prompts.

## Common Workflows

### Code Analysis (Safe, Read-Only)

```bash
deepagents -n "Analyze src/ for code quality issues"
```

### Code Generation with File Writing

```bash
deepagents --auto-approve -n "Generate unit tests for src/auth.py"
```

### Research with Memory Persistence

```bash
deepagents -a researcher -m "Research best practices for Python async"
# Agent saves findings to memories/ automatically
# Next session:
deepagents -a researcher -m "What did we learn about async?"
```

### Project-Scoped Agent

```bash
cd my-project
# Create .deepagents/AGENTS.md with project conventions
mkdir -p .deepagents
echo "# Project uses FastAPI, PostgreSQL, pytest" > .deepagents/AGENTS.md
deepagents -m "Help me add a new API endpoint"
```

## Configuration

Global config: `~/.deepagents/config.toml` (see [Providers & Models](references/providers.md) for the full config.toml schema)

```toml
[models]
default = "anthropic:claude-sonnet-4-5"

[models.providers.ollama]
base_url = "http://localhost:11434"
models = ["qwen3:8b", "llama3"]

[models.providers.ollama.params]
temperature = 0
num_ctx = 8192
```

## References

For detailed documentation:

- **[CLI Reference](references/cli-reference.md)** — Complete flags, commands, slash commands, keyboard shortcuts
- **[Providers & Models](references/providers.md)** — All 20+ providers, config.toml format, model switching
- **[Skills System](references/skills-system.md)** — Creating skills, progressive disclosure, SKILL.md format
- **[Memory & Persistence](references/memory-and-persistence.md)** — Auto-memory, AGENTS.md, SDK long-term memory
- **[Sandboxes](references/sandboxes.md)** — Modal/Runloop/Daytona setup, security considerations
- **[SDK Customization](references/sdk-customization.md)** — create_deep_agent(), middleware, subagents, backends
- **[Workflows & Patterns](references/workflows.md)** — Automation, CI/CD, subagent patterns, troubleshooting
- **[Streaming](references/streaming.md)** — Streaming modes, subgraph streaming, frontend integration
- **[Agent Client Protocol](references/acp.md)** — ACP server, editor integrations (Zed, VSCode, JetBrains, Neovim)

## Tips

- **`@filename` in REPL** auto-completes and injects file contents into your prompt
- **`!command`** runs shell commands directly without agent interpretation
- **`/remember [context]`** explicitly triggers memory/skill updates — pass optional context to guide the update
- **`-n` mode has no shell by default** — add `--shell-allow-list recommended` for safe commands
- **Local models** (Ollama) work for simple tasks but may struggle with complex tool-calling — use Anthropic/OpenAI for multi-step work
- **Reset an agent** with `deepagents reset --agent NAME` if memories accumulate irrelevant info
