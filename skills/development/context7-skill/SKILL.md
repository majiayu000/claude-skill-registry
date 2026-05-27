---
name: context7-skill
description: Access up-to-date, version-specific documentation and code examples from Context7. Use this skill to verify library and framework details.
---

# Context7 Skill

## Overview

The Context7 skill connects you to accurate, version-specific documentation and code examples directly from the source. Use this skill to verify syntax, API details, and usage patterns for third-party libraries and frameworks, ensuring your code is based on the correct version.

**Access Methods:**

1.  **MCP Tools (Primary):** Direct calls to `resolve_library_id` and `query_docs`.
2.  **CLI Fallback (Secondary):** A Python script (`scripts/context7_cli.py`) using the FastMCP v2 client, intended for use when direct MCP tools are unavailable.

## Prerequisites

- **Context7 API Key:** Must be set as the environment variable `CONTEXT7_API_KEY`.
- **Python Manager (`uv`):** Required only if using the CLI fallback script.

## Available Tools

### 1. Library Resolver (`resolve-library-id`)

Resolves a package or library name to a Context7-compatible library ID and returns a list of matches.

- **MCP Call:** `resolve_library_id(query="...", libraryName="...")`
- **CLI Command:** `uv run scripts/context7_cli.py resolve-library-id <name>`

### 2. Documentation Query (`query-docs`)

Retrieves documentation and code examples using a specific library ID.

- **MCP Call:** `query_docs(libraryId="/org/project/version", query="...")`
- **CLI Command:** `uv run scripts/context7_cli.py query-docs <library_id> <query>`

> **IMPORTANT:** Tool names may have prefixes (e.g., `context7_resolve_library_id`) depending on the runtime environment. Always check available tools first.

## Usage Guidelines

1.  **Resolve First:** Always obtain a valid library ID via `resolve_library_id` before querying, unless the user provides a full ID (e.g., `/org/project/version`).
2.  **Limit Attempts:** Do not retry a tool call more than three times for the same query. If unsuccessful, proceed with the best available information.

## Workflow

### Step 1: Check Availability

Determine if the `resolve_library_id` and `query_docs` tools are directly available in your environment. If not, default to the CLI fallback commands.

### Step 2: Resolve Library ID

Use `resolve-library-id` to identify the correct library.

**Selection Criteria:**

- **Exact Match:** Prioritize names that exactly match the user's request.
- **Relevance:** Ensure the description aligns with the user's intent.
- **Quality:** Look for high documentation coverage (snippet counts), reputation, and benchmark scores.

_Action:_

- If ambiguous, ask the user for clarification.
- Briefly explain the selected library to the user.
- If no good match is found, clearly state this and suggest query refinements.

### Step 3: Query Documentation

Use `query-docs` with the resolved `libraryId`.

**Handling Results:**

- The tool returns a snippet or summary.
- **Example Output:**
  ```markdown
  Source: https://github.com/context7/react_dev/blob/main/learn.md
  ... (content) ...
  ```
- **Insufficient Info?** If the returned text is incomplete, use a web fetch tool (if available) to retrieve the full content from the provided source URL.

## Configuration

| Variable           | Description                               | Required |
| :----------------- | :---------------------------------------- | :------- |
| `CONTEXT7_API_KEY` | API key for authenticating with Context7. | Yes      |

## Resources

- **`scripts/context7_cli.py`**: Unified CLI entry point for fallback access.
- **`references/troubleshooting.md`**: Solutions for common integration issues.
