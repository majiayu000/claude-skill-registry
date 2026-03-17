---
name: analyze-claude-code
description: Analyze Claude Code CLI source code to understand its architecture, implementation details, and design patterns. Use when users want to explore how Claude Code works internally, understand specific features like tools/hooks/MCP/permissions, or learn from its codebase design. Triggers on questions about Claude Code internals, source code analysis requests, or "how does Claude Code implement X" or "what's the prompts of claude code's tools" or "what's the system prompt of claude code" queries.
---

# Analyze Claude Code

Deep dive into Claude Code CLI source code to understand its architecture and implementation.

## Setup: Download and Format Source

```bash
# One-liner: download, extract, and format
curl -sL "$(curl -s https://registry.npmjs.org/@anthropic-ai/claude-code/latest | jq -r '.dist.tarball')" -o claude-code.tgz && tar -xzf claude-code.tgz && npx js-beautify --replace package/cli.js
```

## Official Documentation

**Access official docs via WebFetch tool:**

Use the WebFetch tool to query Claude Code's official documentation when you need authoritative information about features, API, or best practices.

**Documentation entry point:**
- URL: `https://code.claude.com/docs/llms.txt`
- Contains: Quickstart, CLI Reference, Settings, Hooks, MCP, Skills, Plugins, Security, and more

**Example queries:**

```bash
# Get documentation overview
Use WebFetch tool with:
  url: https://code.claude.com/docs/llms.txt
  prompt: "Show me the table of contents and main sections"

# Query specific topics
Use WebFetch tool with:
  url: https://code.claude.com/docs/llms.txt
  prompt: "How do hooks work? Explain with examples"

Use WebFetch tool with:
  url: https://code.claude.com/docs/llms.txt
  prompt: "What are the available MCP transport types and their differences?"
```

**When to use:**
- Verify implementation details not clear from source code
- Understand intended behavior and design philosophy
- Check for recent updates or documentation changes
- Find usage examples and best practices
- Cross-reference source code with official documentation

---

## Key Modules

### 1. Prompts
System prompts that define Claude's behavior and capabilities.

**Quick extraction:**
```bash
# Find Claude identity
grep -n "You are Claude" package/cli.js

# Find prompt sections (around line 435350)
grep -n "# Tone and style\|# Doing tasks\|# Tool usage policy" package/cli.js

# Find tool descriptions
grep -n "Executes a given bash command\|Reads a file from\|Fast file pattern" package/cli.js
```

**Key locations:**
- `l10` variable: Base identity "You are Claude Code..."
- `rc` function: Main system prompt builder
- Tool descriptions as template strings (e.g., `SEB` for Read, `c10` for Glob)

**Prompt sections:** Tone/style, Professional objectivity, Task management, Tool usage policy, Code references

---

#### Advanced Prompt Discovery

**Core Principle:** Trace prompts from function entry points using code structure, not content keywords.

**Three-Layer Abstraction:**
- **Layer 3 (Code):** Long strings, template vars, API calls (most stable, start here)
- **Layer 2 (Structure):** Imperative patterns, examples, lists (medium abstraction)
- **Layer 1 (Content):** Specific text keywords (fragile, avoid dependency)

**Tracing Flow:**
```
/command → Command registry → Handler function → Prompt construction
```

**Key search patterns:**

```bash
# Layer 3: Code characteristics (start here)
grep -n "return \`" package/cli.js           # Template strings
grep -n "messages\s*:\|system\s*:" package/cli.js  # API calls
awk '/return `/{start=NR} /^`/&&NR-start>15{print "Line",start}' package/cli.js  # Long strings

# Layer 2: Structure characteristics
grep -n "You are\|Your task\|Please" package/cli.js  # Imperative patterns
grep -n "<example>" package/cli.js           # Example blocks
grep -n "format.*response\|output.*should" package/cli.js  # Format descriptions

# Combined: Long strings with imperative content
grep -n "return \`" package/cli.js | while read l; do
    line=$(echo $l | cut -d: -f1)
    sed -n "$line,$((line+20))p" package/cli.js | grep -q "You are\|Your task" && echo "Line $line"
done
```

**Tracing workflow (from command):**

```bash
# 1. Find command definition
grep -n 'name.*"compact"' package/cli.js
# → Line 12345

# 2. Extract command object (check type: "prompt" or "local")
sed -n '12340,12370p' package/cli.js
# → type: "local", handler: (args) => kv1(args)

# 3. Find handler function
grep -n 'function kv1\|const kv1' package/cli.js
# → Line 45678

# 4. Search for prompt construction in handler
sed -n '45678,45900p' package/cli.js | grep -n 'return `\|messages:\|system:'
# → Line 23: return `Your task is to create...

# 5. Extract full prompt
sed -n '45700,46200p' package/cli.js
```

**Prompt identification heuristics:**

A code block is likely a prompt if it scores ≥4:
- Contains "You are|Your task|Please|Analyze" (+3)
- Contains "format|structure|output|response" (+2)
- Contains `<example>` or `Example:` (+2)
- Contains lists (^[0-9].|^-) with 3+ items (+1)
- Has 3+ paragraphs (blank lines) (+1)

**Example: Trace any local command**

```bash
COMMAND="init"  # or any command name

# Step 1-2: Find command and handler
HANDLER=$(sed -n "$(grep -n "name.*\"$COMMAND\"" package/cli.js | cut -d: -f1),+30p" package/cli.js | \
          grep -o 'handler.*[a-zA-Z_][a-zA-Z0-9_]*' | tail -1)

# Step 3: Find handler line
HANDLER_LINE=$(grep -n "function $HANDLER\|const $HANDLER" package/cli.js | cut -d: -f1)

# Step 4-5: Extract prompts
sed -n "$HANDLER_LINE,$((HANDLER_LINE+300))p" package/cli.js | grep -B2 -A20 'return `'
```

---

### 2. Tools
Built-in tools: Bash, Read, Write, Edit, Glob, Grep, Task, WebFetch, etc.

**Search patterns:**
```bash
grep -n "tool.*schema\|toolName\|Tool.*definition" package/cli.js
```

**Key aspects:**
- JSON Schema definitions for parameters
- Validation logic
- Execution sandboxing (macOS sandbox-exec, Docker)
- Result handling and token limits

---

### 3. Subagents
Specialized agents for task delegation: Explore, Plan, General-purpose, Bash, etc.

**Search patterns:**
```bash
grep -n "subagent\|agentType\|Task.*agent" package/cli.js
```

**Key aspects:**
- Agent types: `Explore` (Haiku, read-only), `Plan` (inherit model), `General-purpose` (full tools)
- Context isolation (fork mode)
- Permission inheritance
- Background vs foreground execution

---

### 4. Hooks
Event-driven extensibility mechanism.

**Search patterns:**
```bash
grep -n "registeredHooks\|PreToolUse\|PostToolUse\|hookEvent" package/cli.js
```

**Hook events:**
| Event | Trigger | Matcher Support |
|-------|---------|-----------------|
| `PreToolUse` | Before tool execution | Yes |
| `PostToolUse` | After tool success | Yes |
| `UserPromptSubmit` | User sends prompt | No |
| `SessionStart` | Session begins | Yes |
| `Stop` | Agent completes | No |

**Key aspects:**
- Exit codes: 0=success, 2=blocking error
- JSON output for decisions (`allow`/`deny`/`ask`)
- `updatedInput` to modify tool parameters

---

### 5. Skills
Modular knowledge packages (SKILL.md files).

**Search patterns:**
```bash
grep -n "SKILL\.md\|skill.*description\|loadSkill" package/cli.js
```

**Key aspects:**
- Discovery: Only name/description loaded initially
- Activation: Full content loaded when triggered
- Frontmatter: `name`, `description`, `allowed-tools`, `model`, `context`, `hooks`
- Locations: `~/.claude/skills/`, `.claude/skills/`, plugin bundles

---

### 6. Plugins
Extension packages containing skills, commands, MCP servers.

**Search patterns:**
```bash
grep -n "plugin\.json\|loadPlugin\|pluginRoot" package/cli.js
```

**Structure:**
```
plugin/
├── .claude-plugin/plugin.json  # Metadata
├── commands/                   # Slash commands
├── agents/                     # Custom subagents
├── skills/                     # Skills
├── hooks/hooks.json            # Hook configs
└── .mcp.json                   # MCP servers
```

**Key aspects:**
- Namespace isolation (`/plugin-name:command`)
- Resource isolation for hooks
- Installation via marketplace or `--plugin-dir`

---

### 7. Slash Commands
User-invoked commands with `/` prefix.

**Search patterns:**
```bash
grep -n "slashCommand\|commands/.*\.md\|ARGUMENTS" package/cli.js
```

**Types:**
- Built-in: `/clear`, `/compact`, `/config`, `/model`, etc.
- Custom: `.claude/commands/*.md`
- Plugin: `/plugin:command`
- MCP: `/mcp__server__prompt`

**Frontmatter:** `allowed-tools`, `description`, `model`, `context`, `hooks`

---

### 8. MCP (Model Context Protocol)
External tool integration via MCP servers.

**Search patterns:**
```bash
grep -n "MCP\|mcpServer\|mcp__" package/cli.js
```

**Key aspects:**
- Transport: HTTP (recommended), SSE, stdio
- Scopes: local, project, user
- Tool format: `mcp__<server>__<tool>`
- Dynamic tool discovery via `list_changed`

---

### 9. Memory (CLAUDE.md)
Persistent instructions loaded into context.

**Search patterns:**
```bash
grep -n "CLAUDE\.md\|loadMemory\|rules/.*\.md" package/cli.js
```

**Hierarchy (high to low priority):**
1. Enterprise: `/Library/Application Support/ClaudeCode/CLAUDE.md`
2. Project: `./CLAUDE.md` or `./.claude/CLAUDE.md`
3. Rules: `./.claude/rules/*.md`
4. User: `~/.claude/CLAUDE.md`
5. Local: `./CLAUDE.local.md`

---

### 10. Settings
Configuration with four-level scope system.

**Search patterns:**
```bash
grep -n "settings\.json\|loadSettings\|settingsScope" package/cli.js
```

**Priority (high to low):**
1. Managed: System-level, IT-deployed
2. CLI args: Temporary session override
3. Local: `.claude/settings.local.json`
4. Project: `.claude/settings.json`
5. User: `~/.claude/settings.json`

**Key configs:** `permissions`, `hooks`, `model`, `env`, `sandbox`

---

## Analysis Tips

**Search tools** - Examples use `grep`, but any search tool works:
- `grep -n "pattern" file` - Basic search
- `rg -n "pattern" file` - Ripgrep (faster)
- `ag "pattern" file` - The Silver Searcher
- Use Claude Code's built-in `Grep` tool for best integration

**View context** - After finding line numbers:
- `sed -n 'START,ENDp' file` - Extract line range
- `rg -A5 -B5 "pattern" file` - Show context around matches

**Key principles:**
1. **Variable names are minified** - Search for string literals, not variable names
2. **Template strings** - Many prompts use backtick templates with `${}`
3. **Adjacent code** - Functions are often defined near their string constants
4. **Follow the strings** - Start from user-visible text to trace implementation
