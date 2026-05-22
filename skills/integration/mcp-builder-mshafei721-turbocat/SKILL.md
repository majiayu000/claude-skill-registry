---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
---

# MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks.

## High-Level Workflow

### Phase 1: Deep Research and Planning

**API Coverage vs. Workflow Tools:**
Balance comprehensive API endpoint coverage with specialized workflow tools. When uncertain, prioritize comprehensive API coverage.

**Tool Naming and Discoverability:**
Use consistent prefixes (e.g., `github_create_issue`, `github_list_repos`) and action-oriented naming.

**Context Management:**
Design tools that return focused, relevant data. Support pagination where applicable.

**Actionable Error Messages:**
Error messages should guide agents toward solutions with specific suggestions.

### Phase 2: Implementation

**Recommended Stack:**
- Language: TypeScript
- Transport: Streamable HTTP for remote servers, stdio for local servers

**For each tool:**

1. **Input Schema**: Use Zod (TypeScript) or Pydantic (Python)
2. **Output Schema**: Define `outputSchema` where possible
3. **Tool Description**: Concise summary of functionality
4. **Implementation**: Async/await, proper error handling, pagination support
5. **Annotations**: `readOnlyHint`, `destructiveHint`, `idempotentHint`

### Phase 3: Review and Test

- No duplicated code (DRY principle)
- Consistent error handling
- Full type coverage
- Clear tool descriptions

**Testing:**
```bash
# TypeScript
npm run build
npx @modelcontextprotocol/inspector

# Python
python -m py_compile your_server.py
```

### Phase 4: Create Evaluations

Create 10 evaluation questions to test effectiveness:
- Independent, read-only, complex, realistic
- Verifiable with single clear answer
- Stable over time

## SDK Documentation

**TypeScript SDK**: https://github.com/modelcontextprotocol/typescript-sdk
**Python SDK**: https://github.com/modelcontextprotocol/python-sdk
**MCP Specification**: https://modelcontextprotocol.io
