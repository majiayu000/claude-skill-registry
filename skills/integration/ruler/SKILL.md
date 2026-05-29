---
name: ruler
description: Unified AI agent configuration propagation across 18+ coding assistants.
version: 1.0.0
---


# ruler

Unified AI agent configuration propagation across 18+ coding assistants.

**Repository**: https://github.com/intellectronica/ruler
**Documentation**: https://deepwiki.com/intellectronica/ruler

---

## Overview

Ruler centralizes AI agent instructions in `.ruler/` and distributes them to all configured agents via `ruler apply`. Supports Model Context Protocol (MCP) propagation with merge/overwrite strategies.

```
.ruler/
├── *.md           # Rules (concatenated alphabetically)
├── ruler.toml     # Agent config + MCP settings
└── mcp.json       # Shared MCP servers
```

---

## Installation

```bash
npm install -g ruler
# or
npx ruler init
```

---

## Commands

### ruler init

Creates `.ruler/` directory with default files:

```bash
ruler init           # Local project
ruler init --global  # ~/.config/ruler/
```

**Creates:**
- `instructions.md` - Central AI instructions
- `ruler.toml` - Configuration file
- `mcp.json` - MCP server definitions

### ruler apply

Propagates rules to all configured agents:

```bash
ruler apply                          # All default agents
ruler apply --agents claude,codex    # Specific agents
ruler apply --no-mcp                 # Skip MCP propagation
ruler apply --mcp-overwrite          # Replace native MCP configs
ruler apply --no-gitignore           # Skip .gitignore updates
```

### ruler revert

Restores files from backups:

```bash
ruler revert                  # Restore all, delete backups
ruler revert --keep-backups   # Restore but keep .bak files
```

---

## Supported Agents (18)

| Agent | Identifier | Instructions Output | MCP Config |
|-------|------------|---------------------|------------|
| **GitHub Copilot** | `copilot` | `.github/copilot-instructions.md` | `.vscode/mcp.json` |
| **Claude Code** | `claude` | `CLAUDE.md` | `.mcp.json` |
| **OpenAI Codex CLI** | `codex` | `AGENTS.md` | `.codex/config.toml` |
| **Jules** | `jules` | `AGENTS.md` | - |
| **Cursor** | `cursor` | `.cursor/rules/ruler_cursor_instructions.mdc` | `.cursor/mcp.json` |
| **Windsurf** | `windsurf` | `.windsurf/rules/ruler_windsurf_instructions.md` | `~/.codeium/windsurf/mcp_config.json` |
| **Cline** | `cline` | `.clinerules` | - |
| **Amp** | `amp` | `AGENT.md` | - |
| **Aider** | `aider` | `ruler_aider_instructions.md` + `.aider.conf.yml` | `.mcp.json` |
| **Firebase Studio** | `firebase` | `.idx/airules.md` | - |
| **Open Hands** | `openhands` | `.openhands/microagents/repo.md` | `.openhands/config.toml` |
| **Gemini CLI** | `gemini-cli` | `GEMINI.md` | `.gemini/settings.json` |
| **Junie** | `junie` | `.junie/guidelines.md` | - |
| **AugmentCode** | `augmentcode` | `.augment/rules/ruler_augment_instructions.md` | `.vscode/settings.json` |
| **Kilo Code** | `kilocode` | `.kilocode/rules/ruler_kilocode_instructions.md` | `.kilocode/mcp.json` |
| **OpenCode** | `opencode` | `AGENTS.md` | `opencode.json` |
| **Goose** | `goose` | `.goosehints` | - |
| **Crush** | `crush` | `CRUSH.md` | `.crush.json` |

---

## Configuration: ruler.toml

Complete configuration reference:

```toml
# ═══════════════════════════════════════════════════════════════════
# DEFAULT AGENTS
# ═══════════════════════════════════════════════════════════════════

# Agents to run when --agents flag is not specified
# If omitted, all agents are active
default_agents = ["copilot", "claude", "codex", "cursor", "amp"]

# ═══════════════════════════════════════════════════════════════════
# GLOBAL MCP CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

[mcp]
# Enable/disable MCP propagation globally (default: true)
enabled = true

# How to combine with native configs: "merge" or "overwrite"
# merge: Union of servers, incoming takes precedence on conflicts
# overwrite: Replace native config entirely
merge_strategy = "merge"

# ═══════════════════════════════════════════════════════════════════
# GITIGNORE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════

[gitignore]
# Auto-add generated files to .gitignore (default: true)
enabled = true

# ═══════════════════════════════════════════════════════════════════
# AGENT-SPECIFIC CONFIGURATIONS
# ═══════════════════════════════════════════════════════════════════

[agents.copilot]
enabled = true
output_path = ".github/copilot-instructions.md"

[agents.claude]
enabled = true
output_path = "CLAUDE.md"

[agents.codex]
enabled = true
output_path = "AGENTS.md"
output_path_config = ".codex/config.toml"

# Agent-specific MCP override
[agents.codex.mcp]
enabled = true
merge_strategy = "merge"

[agents.cursor]
enabled = true
output_path = ".cursor/rules/ruler_cursor_instructions.mdc"

[agents.amp]
enabled = true
output_path = "AGENT.md"

[agents.aider]
enabled = true
output_path_instructions = "ruler_aider_instructions.md"
output_path_config = ".aider.conf.yml"

[agents.windsurf]
enabled = false  # Disable specific agent

[agents.opencode]
enabled = true
output_path = "AGENTS.md"

[agents.gemini-cli]
enabled = true
```

---

## Configuration: mcp.json

Define shared MCP servers:

```json
{
  "mcpServers": {
    "gay": {
      "type": "stdio",
      "command": "julia",
      "args": ["--project=@gay", "-e", "using Gay; Gay.serve_mcp()"],
      "env": {
        "GAY_SEED": "1069"
      }
    },
    "firecrawl": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "${FIRECRAWL_API_KEY}"
      }
    },
    "exa": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@anthropic/exa-mcp-server"],
      "env": {
        "EXA_API_KEY": "${EXA_API_KEY}"
      }
    },
    "tree-sitter": {
      "type": "stdio",
      "command": "uvx",
      "args": ["mcp-tree-sitter"]
    }
  }
}
```

---

## Architecture

### IAgent Interface

All agents implement:

```typescript
interface IAgent {
  getIdentifier(): string;        // e.g., "copilot", "claude"
  getName(): string;              // Human-readable name
  getDefaultOutputPath(): string | Record<string, string>;
  getMcpServerKey?(): string;     // e.g., "servers" for Copilot
  applyRulerConfig(
    concatenatedRules: string,
    projectRoot: string,
    rulerMcpJson: object,
    agentConfig?: AgentConfig
  ): Promise<void>;
}
```

### MCP Server Keys by Agent

| Agent | MCP Server Key |
|-------|----------------|
| Copilot | `servers` |
| Claude | `mcpServers` |
| OpenCode | `mcp` |
| Others | `mcpServers` |

### Orchestration Flow (src/lib.ts)

```
1. Load ruler.toml configuration
2. Find .ruler/ directory (local or global)
3. Concatenate all *.md files alphabetically
4. Load and validate mcp.json
5. For each selected agent:
   a. Determine output paths (with overrides)
   b. Backup existing files (.bak)
   c. Call agent.applyRulerConfig()
   d. If MCP enabled:
      - Read native MCP config
      - Merge with ruler mcp.json
      - Write merged config
6. Update .gitignore with generated paths
```

---

## MCP Merge Strategies

### Merge (default)

Combines servers from both configs, incoming takes precedence:

```javascript
// base (native)
{ "mcpServers": { "a": {...}, "b": {...} } }

// incoming (ruler)
{ "mcpServers": { "b": {...}, "c": {...} } }

// result
{ "mcpServers": { "a": {...}, "b": {...from ruler}, "c": {...} } }
```

### Overwrite

Replaces native config entirely:

```javascript
// result = incoming config only
{ "mcpServers": { "b": {...}, "c": {...} } }
```

---

## Backup Strategy

1. Before overwriting, create `file.bak`
2. On revert: restore from `.bak`, then delete `.bak`
3. With `--keep-backups`: restore but keep `.bak` files
4. Generated files (no backup) are simply deleted on revert

---

## Special Agent Handling

### OpenHands
- MCP config in `.openhands/config.toml`
- Uses `stdio_servers` key (TOML format)

### AugmentCode
- MCP embedded in `.vscode/settings.json`
- Custom propagation function

### OpenCode
- MCP in `opencode.json`
- Uses `mcp` key instead of `mcpServers`

### Cursor
- Adds YAML front-matter to rules
- `.mdc` extension for instructions

### Aider
- Two output files: instructions + config
- Config is `.aider.conf.yml`

---

## Configuration Precedence

```
CLI flags (highest)
    ↓
ruler.toml settings
    ↓
Built-in defaults (lowest)
```

Examples:
- `--no-gitignore` overrides `[gitignore] enabled = true`
- `--agents claude` overrides `default_agents`
- Agent-specific `[agents.X.mcp]` overrides global `[mcp]`

---

## Example Workflow

```bash
# 1. Initialize
ruler init

# 2. Add rules
cat > .ruler/01-style.md << 'EOF'
# Code Style
- Use TypeScript
- Prefer functional programming
- Maximum line length: 100
EOF

cat > .ruler/02-security.md << 'EOF'
# Security
- Never log secrets
- Use parameterized queries
- Validate all inputs
EOF

# 3. Configure MCP
cat > .ruler/mcp.json << 'EOF'
{
  "mcpServers": {
    "gay": {
      "command": "julia",
      "args": ["--project=@gay", "-e", "using Gay; Gay.serve_mcp()"]
    }
  }
}
EOF

# 4. Configure agents
cat > .ruler/ruler.toml << 'EOF'
default_agents = ["claude", "codex", "amp"]

[mcp]
enabled = true
merge_strategy = "merge"

[agents.claude]
enabled = true

[agents.codex]
enabled = true

[agents.amp]
enabled = true
EOF

# 5. Apply
ruler apply

# 6. Verify
cat CLAUDE.md
cat AGENTS.md
cat AGENT.md

# 7. Iterate and refine
vim .ruler/01-style.md
ruler apply

# 8. Revert if needed
ruler revert
```

---

## Integration with Music-Topos

The `.ruler/` directory in music-topos extends the standard ruler with:

### GF(3) Bisimulation

```toml
[bisimulation]
enabled = true
polarity_rotation = true

[bisimulation.agents]
claude = "PLUS"      # +1
codex = "ERGODIC"    # 0
cursor = "MINUS"     # -1
# Sum = 0 mod 3 ✓
```

### propagate.clj (Babashka)

```clojure
(def AGENTS
  {:codex   {:trit 0   :skills-path ".codex/skills"}
   :claude  {:trit -1  :skills-path ".claude/skills"}
   :amp     {:trit 0   :skills-path ".ruler/skills"}
   :cursor  {:trit -1  :skills-path ".cursor/skills"}
   :copilot {:trit 1   :skills-path ".vscode/skills"}
   :aider   {:trit 1   :skills-path ".skillz"}})

;; Propagate with GF(3) conservation check
(propagate-all!)
```

---

## References

- GitHub: https://github.com/intellectronica/ruler
- DeepWiki: https://deepwiki.com/intellectronica/ruler
- Author: intellectronica (Eran Kampf)



## Scientific Skill Interleaving

This skill connects to the K-Dense-AI/claude-scientific-skills ecosystem:

### Graph Theory
- **networkx** [○] via bicomodule
  - Universal graph hub

### Bibliography References

- `general`: 734 citations in bib.duckdb



## SDF Interleaving

This skill connects to **Software Design for Flexibility** (Hanson & Sussman, 2021):

### Primary Chapter: 10. Adventure Game Example

**Concepts**: autonomous agent, game, synthesis

### GF(3) Balanced Triad

```
ruler (+) + SDF.Ch10 (+) + [balancer] (+) = 0
```

**Skill Trit**: 1 (PLUS - generation)

### Secondary Chapters

- Ch8: Degeneracy
- Ch1: Flexibility through Abstraction
- Ch2: Domain-Specific Languages
- Ch7: Propagators

### Connection Pattern

Adventure games synthesize techniques. This skill integrates multiple patterns.
## Cat# Integration

This skill maps to **Cat# = Comod(P)** as a bicomodule in the equipment structure:

```
Trit: 0 (ERGODIC)
Home: Prof
Poly Op: ⊗
Kan Role: Adj
Color: #26D826
```

### GF(3) Naturality

The skill participates in triads satisfying:
```
(-1) + (0) + (+1) ≡ 0 (mod 3)
```

This ensures compositional coherence in the Cat# equipment structure.