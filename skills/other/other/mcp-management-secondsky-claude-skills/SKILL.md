---
name: mcp-management
description: Manage MCP servers - discover, analyze, execute tools/prompts/resources. Use for MCP integrations, capability discovery, tool filtering, programmatic execution, or encountering context bloat, server configuration, tool execution errors.
metadata:
  keywords: "MCP, Model Context Protocol, MCP servers, tool discovery, MCP integration, capability discovery, tool filtering, MCP tools, MCP prompts, MCP resources, progressive disclosure, multi-server management, tool catalog, mcp client, mcp execution, server configuration, context-efficient"
license: MIT
---

# MCP Management

Skill for managing and interacting with Model Context Protocol (MCP) servers.

## Overview

MCP is an open protocol enabling AI agents to connect to external tools and data sources. This skill provides scripts and utilities to discover, analyze, and execute MCP capabilities from configured servers without polluting the main context window.

**Key Benefits**:
- Progressive disclosure of MCP capabilities (load only what's needed)
- Intelligent tool/prompt/resource selection based on task requirements
- Multi-server management from single config file
- Context-efficient: subagents handle MCP discovery and execution
- Persistent tool catalog: automatically saves discovered tools to JSON for fast reference

## When to Use This Skill

Use this skill when:
1. **Discovering MCP Capabilities**: Need to list available tools/prompts/resources from configured servers
2. **Task-Based Tool Selection**: Analyzing which MCP tools are relevant for a specific task
3. **Executing MCP Tools**: Calling MCP tools programmatically with proper parameter handling
4. **MCP Integration**: Building or debugging MCP client implementations
5. **Context Management**: Avoiding context pollution by delegating MCP operations to subagents

## Core Capabilities

### 1. Configuration Management

MCP servers configured in `.claude/.mcp.json`.

**Gemini CLI Integration** (recommended): Create symlink to `.gemini/settings.json`:
```bash
mkdir -p .gemini && ln -sf .claude/.mcp.json .gemini/settings.json
```

### 2. Capability Discovery

```bash
# Preferred: Using bun (faster)
bunx tsx scripts/cli.ts list-tools  # Saves to assets/tools.json
bunx tsx scripts/cli.ts list-prompts
bunx tsx scripts/cli.ts list-resources

# Alternative: Using bunx
bunx tsx scripts/cli.ts list-tools
bunx tsx scripts/cli.ts list-prompts
bunx tsx scripts/cli.ts list-resources
```

Aggregates capabilities from multiple servers with server identification.

### 3. Intelligent Tool Analysis

LLM analyzes `assets/tools.json` directly - better than keyword matching algorithms.

### 4. Tool Execution

**Primary: Gemini CLI** (if available)
```bash
gemini -y -m gemini-2.5-flash -p "Take a screenshot of https://example.com"
```

**Secondary: Direct Scripts**
```bash
# Preferred: Using bun
bunx tsx scripts/cli.ts call-tool memory create_entities '{"entities":[...]}'

# Alternative: Using bunx
bunx tsx scripts/cli.ts call-tool memory create_entities '{"entities":[...]}'
```

**Fallback: mcp-manager Subagent**

## Implementation Patterns

### Pattern 1: Gemini CLI Auto-Execution (Primary)

Use Gemini CLI for automatic tool discovery and execution.

**Quick Example**:
```bash
gemini -y -m gemini-2.5-flash -p "Take a screenshot of https://example.com"
```

**Benefits**: Automatic tool discovery, natural language execution, faster than subagent orchestration.

### Pattern 2: Subagent-Based Execution (Fallback)

Use `mcp-manager` agent when Gemini CLI unavailable. Subagent discovers tools, selects relevant ones, executes tasks, reports back.

**Benefit**: Main context stays clean, only relevant tool definitions loaded when needed.

### Pattern 3: LLM-Driven Tool Selection

LLM reads `assets/tools.json`, intelligently selects relevant tools using context understanding, synonyms, and intent recognition.

### Pattern 4: Multi-Server Orchestration

Coordinate tools across multiple servers. Each tool knows its source server for proper routing.

## Quick Start

**Method 1: Gemini CLI** (recommended)
```bash
bun install -g gemini-cli  # or: bun add -g gemini-cli
mkdir -p .gemini && ln -sf .claude/.mcp.json .gemini/settings.json
gemini -y -m gemini-2.5-flash -p "Take a screenshot of https://example.com"
```

**Method 2: Scripts**
```bash
cd .claude/skills/mcp-management/scripts
bun install  # or: bun install
bunx tsx cli.ts list-tools  # Saves to assets/tools.json
bunx tsx cli.ts call-tool memory create_entities '{"entities":[...]}'
```

**Method 3: mcp-manager Subagent**

Dispatch subagent to handle MCP operations, keeping main context clean.

## Integration Strategy

### Execution Priority

1. **Gemini CLI** (Primary): Fast, automatic, intelligent tool selection
   - Check: `command -v gemini`
   - Execute: `gemini -y -m gemini-2.5-flash -p "<task>"`
   - Best for: All tasks when available

2. **Direct CLI Scripts** (Secondary): Manual tool specification
   - Use when: Need specific tool/server control
   - Execute: `bunx tsx scripts/cli.ts call-tool <server> <tool> <args>`

3. **mcp-manager Subagent** (Fallback): Context-efficient delegation
   - Use when: Gemini unavailable or failed
   - Keeps main context clean

### Integration with Agents

The `mcp-manager` agent uses this skill to:
- Check Gemini CLI availability first
- Execute via `gemini` command if available
- Fallback to direct script execution
- Discover MCP capabilities without loading into main context
- Report results back to main agent

This keeps main agent context clean and enables efficient MCP integration.
