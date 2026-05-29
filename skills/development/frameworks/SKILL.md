---
name: frameworks
description: Approved frameworks and libraries for this codebase. Apply when selecting libraries, checking if a framework is approved, or fetching documentation for approved tools.
user-invocable: false
---

# Frameworks

Approved frameworks and libraries for this codebase with Context7 IDs for documentation lookup.

## Critical Rules

1. **Use ONLY approved frameworks** - NEVER introduce alternatives or substitutes
2. **Fetch docs when uncertain** - Use Context7 MCP with the library ID directly
3. **Use modern patterns** - Avoid deprecated methods; check latest docs if uncertain

## Quick Reference

| Framework | Purpose | Context7 ID | Docs |
|-----------|---------|-------------|------|
| LangChain | Agent architecture, LLM integrations | `/websites/langchain` | [docs](https://docs.langchain.com/oss/python/langchain/overview) |
| LangGraph | Stateful agent orchestration | `/websites/langgraph` | [docs](https://docs.langchain.com/oss/python/langgraph/overview) |
| FastMCP | MCP server implementations | `/jlowin/fastmcp` | [docs](https://gofastmcp.com/getting-started/welcome) |
| Polars | DataFrame operations | `/pola-rs/polars` | [docs](https://docs.pola.rs/api/python/stable/reference/index.html) |
| Pydantic | Data validation, settings | `/pydantic/pydantic` | [docs](https://docs.pydantic.dev/latest) |
| diskcache | Disk-based caching | `/grantjenks/python-diskcache` | [docs](https://grantjenks.com/docs/diskcache/) |
| loguru | Logging | `/delgan/loguru` | [docs](https://loguru.readthedocs.io/en/stable/) |
| pytest | Testing | `/pytest-dev/pytest` | [docs](https://docs.pytest.org/en/stable/) |
| pytest-check | Multiple failures per test | `/okken/pytest-check` | [docs](https://github.com/okken/pytest-check) |
| ruff | Linter and formatter | `/astral-sh/ruff` | [docs](https://docs.astral.sh/ruff/) |
| sqlglot | SQL parsing, transpiling, optimization | `/tobymao/sqlglot` | [docs](https://sqlglot.com/sqlglot.html) |
| ty | Type checker | `/astral-sh/ty` | [docs](https://docs.astral.sh/ty/) |
| uv | Package manager | `/astral-sh/uv` | [docs](https://docs.astral.sh/uv/) |

## Fetching Documentation

When uncertain about API details, use Context7 MCP directly with the library ID:

```
mcp__context7__query-docs(libraryId="/pydantic/pydantic", query="field validators")
```
