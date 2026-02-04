---
name: mcp-converter
description: Converts MCP servers to Claude Skills to save tokens. Runs the introspection tool to generate skill wrappers.
version: 1.0
model: sonnet
invoked_by: both
user_invocable: true
tools: [Bash, Read, Write]
best_practices:
  - Use introspection to analyze MCP servers
  - Generate skill wrappers with progressive disclosure
  - Test converted skills before use
error_handling: graceful
streaming: supported
---

# MCP-to-Skill Converter

## Installation

The skill invokes `.claude/tools/integrations/mcp-converter/batch_converter.py`. Requirements:

- **Python 3.10+**: [python.org](https://www.python.org/downloads/) or `winget install Python.Python.3.12` (Windows), `brew install python@3.12` (macOS).
- **pip**: Usually included with Python; verify with `pip --version`.
- **Dependencies**: From the repo root, install deps for the integration (e.g. PyYAML if required):
  ```bash
  pip install pyyaml
  ```
  Run from project root; the script uses `.claude/tools/integrations/mcp-converter/` (catalog: `mcp-catalog.yaml`).

## Cheat Sheet & Best Practices

**MCP design:** Single responsibility per server; bounded toolsets; contracts first (strict I/O schemas); stateless by default; additive changes; security (identity, auth, audit). Prefer stdio for local, Streamable HTTP for remote; use a gateway for multi-tenant/centralized policy.

**Conversion:** Introspect server; estimate token usage of tool schemas; generate skill with progressive disclosure. Test converted skills before relying on them. Use catalog + batch_converter for rules-driven conversion.

**Hacks:** Focus on high-token or high-value servers first. Keep generated SKILL.md and wrappers in version control. Use `mcp-catalog.yaml` to mark `keep_as_mcp` or auto-convert thresholds.

## Certifications & Training

**MCP:** [MCP Best Practices](https://mcp-best-practice.github.io/mcp-best-practice/), [modelcontextprotocol.info](https://modelcontextprotocol.info/docs/best-practices/). **Skill data:** Single responsibility, bounded tools, contracts first, stateless; stdio vs HTTP; gateway pattern; introspect → generate skill.

## Hooks & Workflows

**Suggested hooks:** Post–MCP config change: optional batch_converter run to refresh skills. Use with **evolution-orchestrator** (add mcp-converter to secondary) when creating skills from MCP servers.

**Workflows:** Use with **evolution-orchestrator**. Flow: list servers → convert server or batch → test converted skill. See `creators/skill-creator-workflow.yaml`; mcp-converter feeds skill-creator input.

## 🚀 Usage

### 1. List Available MCP Servers

See which servers are configured in your `.mcp.json`:

```bash
python .claude/tools/mcp-converter/mcp_analyzer.py --list
```

### 2. Convert a Server

Convert a specific MCP server to a Skill:

```bash
python .claude/tools/mcp-converter/mcp_analyzer.py --server <server_name>
```

### 3. Batch Conversion (Catalog)

Convert multiple servers based on rules:

```bash
python .claude/tools/mcp-converter/batch_converter.py
```

## ℹ️ How it Works

1.  **Introspect**: Connects to the running MCP server.
2.  **Analyze**: Estimates token usage of tool schemas.
3.  **Generate**: Creates a `SKILL.md` wrapper that creates dynamic tool calls only when needed.

## 🔧 Dependencies

Requires `mcp` python package:

```bash
pip install mcp
```

## Memory Protocol (MANDATORY)

**Before starting:**
Read `.claude/context/memory/learnings.md`

**After completing:**

- New pattern -> `.claude/context/memory/learnings.md`
- Issue found -> `.claude/context/memory/issues.md`
- Decision made -> `.claude/context/memory/decisions.md`

> ASSUME INTERRUPTION: If it's not in memory, it didn't happen.
