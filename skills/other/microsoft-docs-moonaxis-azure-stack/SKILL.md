---
name: microsoft-docs
description: 'Query official Microsoft documentation to find concepts, tutorials, and code examples across Azure, .NET, Agent Framework, Aspire, VS Code, GitHub, and more. Uses Microsoft Learn MCP as the default, with Context7 and Aspire MCP for content that lives outside learn.microsoft.com.'
---

# Microsoft Docs

Research skill for the Microsoft technology ecosystem. Covers learn.microsoft.com and documentation that lives outside it (VS Code, GitHub, Aspire, Agent Framework repos).

---

## Default: Microsoft Learn MCP

Use these tools for **everything on learn.microsoft.com** — Azure, .NET, M365, Power Platform, Agent Framework, Semantic Kernel, Windows, and more. This is the primary tool for the vast majority of Microsoft documentation queries.

| Tool | Purpose |
|------|---------|
| `microsoft_docs_search` | Search learn.microsoft.com — concepts, guides, tutorials, configuration |
| `microsoft_code_sample_search` | Find working code snippets from Learn docs. Pass `language` (`python`, `csharp`, etc.) for best results |
| `microsoft_docs_fetch` | Get full page content from a specific URL (when search excerpts aren't enough) |

Use `microsoft_docs_fetch` after search when you need complete tutorials, all config options, or when search excerpts are truncated.

---

## Exceptions: When to Use Other Tools

The following categories live **outside** learn.microsoft.com. Use the specified tool instead.

### .NET Aspire — Use Aspire MCP Server (preferred) or Context7

Aspire docs live on **aspire.dev**, not Learn. The best tool depends on your Aspire CLI version:

**CLI 13.2+** (recommended) — The Aspire MCP server includes built-in docs search tools:

| MCP Tool | Description |
|----------|-------------|
| `list_docs` | Lists all available documentation from aspire.dev |
| `search_docs` | Weighted lexical search across aspire.dev content |
| `get_doc` | Retrieves a specific document by slug |

These ship in Aspire CLI 13.2 ([PR #14028](https://github.com/dotnet/aspire/pull/14028)). To update: `aspire update --self --channel daily`. Ref: https://davidpine.dev/posts/aspire-docs-mcp-tools/

**CLI 13.1** — The MCP server provides integration lookup (`list_integrations`, `get_integration_docs`) but **not** docs search. Fall back to Context7:

| Library ID | Use for |
|---|---|
| `/microsoft/aspire.dev` | Primary — guides, integrations, CLI reference, deployment |
| `/dotnet/aspire` | Runtime source — API internals, implementation details |
| `/communitytoolkit/aspire` | Community integrations — Go, Java, Node.js, Ollama |

### VS Code — Use Context7

VS Code docs live on **code.visualstudio.com**, not Learn.

| Library ID | Use for |
|---|---|
| `/websites/code_visualstudio` | User docs — settings, features, debugging, remote dev |
| `/websites/code_visualstudio_api` | Extension API — webviews, TreeViews, commands, contribution points |

### GitHub — Use Context7

GitHub docs live on **docs.github.com** and **cli.github.com**.

| Library ID | Use for |
|---|---|
| `/websites/github_en` | Actions, API, repos, security, admin, Copilot |
| `/websites/cli_github` | GitHub CLI (`gh`) commands and flags |

### Agent Framework — Use Learn MCP + Context7

Agent Framework tutorials are on learn.microsoft.com (use `microsoft_docs_search`), but the **GitHub repo** has API-level detail that is often ahead of published docs — particularly DevUI REST API reference, CLI options, and .NET integration.

| Library ID | Use for |
|---|---|
| `/websites/learn_microsoft_en-us_agent-framework` | Tutorials — DevUI guides, tracing, workflow orchestration |
| `/microsoft/agent-framework` | API detail — DevUI REST endpoints, CLI flags, auth, .NET `AddDevUI`/`MapDevUI` |

**DevUI tip:** Query the Learn website source for how-to guides, then the repo source for API-level specifics (endpoint schemas, proxy config, auth tokens).

---

## Context7 Setup

For any Context7 query, resolve the library ID first (one-time per session):

1. Call `mcp_context7_resolve-library-id` with the technology name
2. Call `mcp_context7_query-docs` with the returned library ID and a specific query

---

## Writing Effective Queries

Be specific — include version, intent, and language:

```
# ❌ Too broad
"Azure Functions"
"agent framework"

# ✅ Specific
"Azure Functions Python v2 programming model"
"Cosmos DB partition key design best practices"
"GitHub Actions workflow_dispatch inputs matrix strategy"
"Aspire AddUvicornApp Python FastAPI integration"
"DevUI serve agents tracing OpenTelemetry directory discovery"
"Agent Framework workflow conditional edges branching handoff"
```

Include context:
- **Version** when relevant (`.NET 8`, `Aspire 13`, `VS Code 1.96`)
- **Task intent** (`quickstart`, `tutorial`, `overview`, `limits`, `API reference`)
- **Language** for polyglot docs (`Python`, `TypeScript`, `C#`)