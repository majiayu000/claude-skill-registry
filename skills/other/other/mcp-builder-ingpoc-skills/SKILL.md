---
name: mcp-builder
description: Guide for creating high-quality MCP (Model Context Protocol) servers that enable LLMs to interact with external services through well-designed tools. Use when building MCP servers to integrate external APIs or services, whether in Python (FastMCP) or Node/TypeScript (MCP SDK).
license: Complete terms in LICENSE.txt
---

# MCP Server Development

Build MCP servers that enable LLMs to accomplish real-world tasks through well-designed tools.

## 4-Phase Process

**Research → Implement → Review → Evaluate**

Load resources on-demand (progressive disclosure):
- Protocol: `https://modelcontextprotocol.io/llms-full.txt`
- Python SDK: `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md`
- TypeScript SDK: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md`

## Core Design Principles

**Workflows over endpoints**: Consolidate operations (e.g., `schedule_event` checks availability + creates)
**Optimize context**: Return high-signal info, provide `concise`/`detailed` formats, use readable IDs
**Actionable errors**: Guide to correct usage ("Try filter='active_only'"), suggest next steps
**Natural task flow**: Name tools how humans think, group with consistent prefixes

---

## Phase 1: Research & Planning

**1.1 Core Docs**
- Load protocol: `https://modelcontextprotocol.io/llms-full.txt`
- Read [Best Practices](./reference/mcp_best_practices.md)

**1.2 Framework** (choose one)
- Python: Fetch SDK + read [Python Guide](./reference/python_mcp_server.md)
- TypeScript: Fetch SDK + read [TypeScript Guide](./reference/node_mcp_server.md)

**1.3 API Research**
Study exhaustively: auth, rate limits, pagination, endpoints, errors, schemas

**1.4 Plan**
- Tool selection (most valuable endpoints)
- Shared utilities (requests, pagination, formatting, errors)
- I/O design (validation schemas, response formats, 25k char limits)
- Error strategy (graceful failures, actionable messages)

---

## Phase 2: Implementation

**2.1 Structure**
Python: single `.py` or modules | TypeScript: `package.json` + `tsconfig.json`

**2.2 Infrastructure First**
Build shared utilities: API helpers, error handling, formatting, pagination, auth
See: [examples/basic-server.py](./examples/basic-server.py) or [.ts](./examples/basic-server.ts)

**2.3 Tools** (for each):
- **Schema**: Pydantic/Zod with constraints, clear descriptions
- **Docs**: Summary, purpose, params+examples, returns, usage, errors
- **Code**: Use utilities, async/await, multiple formats, respect limits
- **Annotations**: `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`

See: [examples/tool-with-context.py](./examples/tool-with-context.py), [error-handling.py](./examples/error-handling.py)

**2.4 Best Practices**
Python: `@mcp.tool()`, Pydantic v2, type hints, async/await, constants
TypeScript: `registerTool()`, Zod `.strict()`, strict mode, no `any`, `Promise<T>`

---

## Phase 3: Review & Refine

**3.1 Quality**: Check DRY, composability, consistency, error handling, types, docs

**3.2 Test**: MCP servers are long-running. See [testing.md](./reference/testing.md)
Quick check: `python -m py_compile server.py` or `npm run build`

**3.3 Checklist**: Load from [Python](./reference/python_mcp_server.md) or [TypeScript](./reference/node_mcp_server.md) guide

---

## Phase 4: Evaluations

Test LLM effectiveness with your server.

**Process**: Inspect tools → Explore data → Generate 10 questions → Verify answers

**Requirements**: Independent, read-only, complex, realistic, verifiable, stable

**Format**:
```xml
<evaluation>
  <qa_pair>
    <question>Complex question...</question>
    <answer>Verifiable answer</answer>
  </qa_pair>
</evaluation>
```

Complete guide: [evaluation.md](./reference/evaluation.md)

---

## Reference Library

| Resource | Load | Purpose |
|----------|------|---------|
| [Best Practices](./reference/mcp_best_practices.md) | Phase 1 | Universal guidelines |
| [Python Guide](./reference/python_mcp_server.md) | Phase 1/2 | Python patterns |
| [TypeScript Guide](./reference/node_mcp_server.md) | Phase 1/2 | TypeScript patterns |
| [Testing](./reference/testing.md) | Phase 3 | Safe testing |
| [Evaluation](./reference/evaluation.md) | Phase 4 | Creating evals |

## Examples

| File | Purpose |
|------|---------|
| [basic-server.py](./examples/basic-server.py) | Python structure |
| [basic-server.ts](./examples/basic-server.ts) | TypeScript structure |
| [tool-with-context.py](./examples/tool-with-context.py) | Workflows |
| [error-handling.py](./examples/error-handling.py) | Errors |

---

## Success Criteria

- Clear tool boundaries (single purpose)
- Efficient context (concise defaults)
- Educational errors (guide usage)
- Workflow optimization (consolidate steps)
- Production ready (errors, rate limits, logging)
- Agent effective (90%+ eval success)
