---
name: building-mcp-servers
description: |
  Guides creation of high-quality MCP (Model Context Protocol) servers that enable LLMs
  to interact with external services through well-designed tools. Use when building MCP
  servers to integrate external APIs or services, whether in Python (FastMCP) or
  Node/TypeScript (MCP SDK). Covers tool design, authentication, Docker deployment,
  and evaluation creation. NOT when consuming existing MCP servers (use the server directly).
---

# MCP Server Development Guide

## Overview

Create MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. The quality of an MCP server is measured by how well it enables LLMs to accomplish real-world tasks.

---

## High-Level Workflow

Creating a high-quality MCP server involves four main phases:

### Phase 1: Deep Research and Planning

#### 1.1 Understand Modern MCP Design

**API Coverage vs. Workflow Tools:**
Balance comprehensive API endpoint coverage with specialized workflow tools. When uncertain, prioritize comprehensive API coverage.

**Tool Naming and Discoverability:**
Use consistent prefixes (e.g., `github_create_issue`, `github_list_repos`) and action-oriented naming.

**Context Management:**
Design tools that return focused, relevant data. Support filtering/pagination.

**Actionable Error Messages:**
Error messages should guide agents toward solutions with specific suggestions.

#### 1.2 Study MCP Protocol Documentation

Start with the sitemap: `https://modelcontextprotocol.io/sitemap.xml`

Fetch pages with `.md` suffix (e.g., `https://modelcontextprotocol.io/specification/draft.md`).

Key pages: Specification overview, transport mechanisms, tool/resource/prompt definitions.

#### 1.3 Study Framework Documentation

**Recommended stack:**
- **Language**: TypeScript (high-quality SDK, good AI code generation)
- **Transport**: Streamable HTTP for remote servers, stdio for local servers

**Load framework documentation:**
- [MCP Best Practices](references/mcp_best_practices.md) - Core guidelines
- [TypeScript Guide](references/node_mcp_server.md) - TypeScript patterns
- [Python Guide](references/python_mcp_server.md) - Python/FastMCP patterns

**SDK Documentation:**
- TypeScript: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`
- Python: `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`

#### 1.4 Plan Your Implementation

Review the service's API documentation. List endpoints to implement, starting with most common operations.

---

### Phase 2: Implementation

#### 2.1 Set Up Project Structure

See language-specific guides:
- [TypeScript Guide](references/node_mcp_server.md) - Project structure, package.json, tsconfig.json
- [Python Guide](references/python_mcp_server.md) - Module organization, dependencies

#### 2.2 Implement Core Infrastructure

Create shared utilities:
- API client with authentication
- Error handling helpers
- Response formatting (JSON/Markdown)
- Pagination support

#### 2.3 Implement Tools

For each tool:

**Input Schema:**
- Use Zod (TypeScript) or Pydantic (Python)
- Include constraints and clear descriptions

**Output Schema:**
- Define `outputSchema` where possible
- Use `structuredContent` in responses

**Tool Description:**
- Concise summary, parameter descriptions, return type

**Annotations:**
- `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`

---

### Phase 3: Review and Test

#### 3.1 Code Quality

Review for: DRY principle, consistent error handling, full type coverage, clear descriptions.

#### 3.2 Build and Test

**TypeScript:**
```bash
npm run build
npx @modelcontextprotocol/inspector
```

**Python:**
```bash
python -m py_compile your_server.py
# Test with MCP Inspector
```

---

### Phase 4: Create Evaluations

Create 10 evaluation questions to test LLM effectiveness with your server.

**Requirements for each question:**
- Independent, read-only, complex, realistic, verifiable, stable

**Output Format:**
```xml
<evaluation>
  <qa_pair>
    <question>Your question here</question>
    <answer>Expected answer</answer>
  </qa_pair>
</evaluation>
```

See [Evaluation Guide](references/evaluation.md) for complete guidelines.

---

## Docker/Containerization

### Transport Security (allowed_hosts)

FastMCP validates Host headers. For Docker, configure:

```python
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

transport_security = TransportSecuritySettings(
    allowed_hosts=[
        "127.0.0.1:*", "localhost:*", "[::1]:*",
        "mcp-server:*",  # Docker container name
        "0.0.0.0:*",
    ],
)
mcp = FastMCP("my_server", transport_security=transport_security)
```

### Health Check Endpoint

Add `/health` endpoint via middleware (see references for full example).

---

## Verification

Run: `python3 scripts/verify.py`

Expected: `✓ building-mcp-servers skill ready`

## If Verification Fails

1. Run diagnostic: Check references/ folder exists
2. Check: All reference files present
3. **Stop and report** if still failing

## References

- [MCP Best Practices](references/mcp_best_practices.md) - Universal guidelines
- [Python Guide](references/python_mcp_server.md) - Python/FastMCP patterns
- [TypeScript Guide](references/node_mcp_server.md) - TypeScript patterns
- [TaskFlow Patterns](references/taskflow_patterns.md) - Internal server patterns
- [Evaluation Guide](references/evaluation.md) - Creating evaluations