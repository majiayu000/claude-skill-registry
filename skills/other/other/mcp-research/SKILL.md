---
name: mcp-research
description: Use when tasks require current, source-backed technical information from MCP tools. Apply for library/API questions, dependency version checks, third-party integration work, framework- or SDK-specific debugging, and any case where stale model knowledge could cause incorrect guidance.
---

# MCP Docs and Research (Context7, Exa, Jina)

## Overview

Use MCP-provided tools to retrieve current, verifiable information instead of relying on memory for fast-changing libraries, APIs, and ecosystem guidance.

## When to Use

- Working with any external library or framework (for example, FastAPI, SQLAlchemy, pandas, boto3, or requests).
- Installing or upgrading dependencies and verifying current versions or migration guidance.
- Implementing features tied to third-party SDKs or APIs.
- Debugging behavior that may be version-specific.
- Looking up current best practices, changelogs, or breaking changes.

## Tool Selection

1. Use `mcp__context7__resolve-library-id` and `mcp__context7__query-docs` for official library documentation and API usage.
2. Use `mcp__exa__get_code_context_exa` for code-centric examples across docs, GitHub, and Stack Overflow.
3. Use `mcp__exa__web_search_exa` for broader current web context (announcements, release notes, ecosystem updates).
4. Use `mcp__jina__search_web` to discover relevant pages, then `mcp__jina__read_url` for clean page extraction.
5. Use `mcp__jina__search_arxiv` and `mcp__jina__extract_pdf` only when the task needs paper-level or PDF-structured research.

## Default Workflow

1. Classify the request: official API docs, implementation examples, or broad web research.
2. Start with the narrowest reliable source:
   - Official docs first (`Context7`) for API correctness.
   - Add `Exa`/`Jina` only when you need cross-source confirmation or broader context.
3. For Context7 docs, always resolve the library id before querying docs unless the exact `/org/project` id is already provided.
4. Keep queries specific (library + feature + version/error) to reduce noisy results.
5. Synthesize findings and clearly separate sourced facts from inferences.

## Quality Rules

- Prefer primary/official documentation for API signatures and behavior.
- For dependency/version decisions, verify with current documentation before recommending versions.
- Avoid unsupported claims; cite concrete tool findings.
- If sources conflict, report the conflict and recommend the safest path (pin version, test in isolation, or check release notes).
- If coverage is weak, state limits explicitly and proceed with best available evidence.
