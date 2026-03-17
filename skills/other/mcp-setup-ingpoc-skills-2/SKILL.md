---
name: mcp-setup
description: "Use when setting up MCP servers for the first time or verifying MCP configuration. Ensures token-efficient and context-graph MCP servers are properly installed and configured with API keys."
keywords: mcp, setup, installation, configuration, voyager-ai, token-efficient
---

# MCP Setup

Configure required MCP servers for agent-harness token efficiency and learning loops.

## Required MCP Servers

| Server | Purpose | API Key |
|--------|---------|---------|
| `token-efficient` | CSV/log processing, sandbox execution (98% token savings) | None |
| `context-graph` | Semantic decision trace search | Voyage AI |

## Setup Instructions

**Quick setup** - Run `scripts/setup-all.sh` in your project directory:

```bash
cd /path/to/your/project
bash ~/.claude/skills/mcp-setup/scripts/setup-all.sh
```

This will:
1. Create `mcp/` folder in your project
2. Clone and build token-efficient MCP
3. Clone and install context-graph MCP
4. Prompt for Voyage AI API key
5. Generate `.mcp.json` in project root

---

**Manual setup** (if needed):

### 1. Install token-efficient MCP in `mcp/`

```bash
mkdir -p mcp
git clone https://github.com/gurusharan/token-efficient-mcp.git mcp/token-efficient-mcp
cd mcp/token-efficient-mcp
npm install
npm run build
```

### 2. Install context-graph MCP in `mcp/`

```bash
git clone https://github.com/gurusharan/agent-harness.git mcp/context-graph-mcp
cd mcp/context-graph-mcp/context-graph-mcp  # or just mcp/context-graph-mcp
pip install -r requirements.txt
```

### 3. Create `.mcp.json` in project root

```json
{
  "mcpServers": {
    "token-efficient": {
      "command": "node",
      "args": ["mcp/token-efficient-mcp/dist/index.js"]
    },
    "context-graph": {
      "command": "uv",
      "args": ["--directory", "mcp/context-graph-mcp", "run", "python", "server.py"],
      "env": {
        "VOYAGE_API_KEY": "your_key_here"
      }
    }
  }
}
```

### 4. Restart Claude Code

After setup, restart Claude Code to load MCP servers.

## Verification

After setup, test:

```python
# Via context-graph MCP
context_store_trace(decision="Test setup", category="general")
context_list_categories()
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `module 'chromadb' not found` | `pip install chromadb` |
| `VOYAGE_API_KEY not found` | Set env var or add to mcp.json env |
| Tools not available | Restart Claude Code |
| `srt: command not found` | Install token-efficient MCP |

## Scripts

| Script | Purpose |
|--------|---------|
| `scripts/setup-all.sh` | **Use this** - Auto-detects paths, sets up both MCP servers |
| `scripts/verify-setup.sh` | Check if MCP servers are working |
| `scripts/install-token-efficient.sh` | Standalone token-efficient MCP installer |
