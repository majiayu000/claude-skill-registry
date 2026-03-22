---
name: livekit-docs
description: Dynamic access to livekit-docs MCP server (7 tools)
version: 1.0.0
title: "Livekit Docs"
status: active
---

# livekit-docs Skill

Access livekit-docs MCP server capabilities.

## Context Efficiency

Traditional MCP approach:
- All 7 tools loaded at startup
- Estimated context: 3500 tokens

This skill approach:
- Metadata only: ~100 tokens
- Full instructions (when used): ~5k tokens
- Tool execution: 0 tokens (runs externally)

## How This Works

Instead of loading all MCP tool definitions upfront, this skill:
1. Tells you what tools are available (just names and brief descriptions)
2. You decide which tool to call based on the user's request
3. Generate a JSON command to invoke the tool
4. The executor handles the actual MCP communication

## Available Tools

- `get_docs_overview`: Returns a complete overview of the docs site and its table of contents, along with page descriptions. This is a great starting point to load context for browsing conceptual docs rather than relying wholly on search.
- `get_pages`: Render one or more docs pages to markdown, by relative path.

Also supports fetching code from public LiveKit repositories on GitHub.

Limitations:
- Pages under /reference are not supported and must be fetched via HTTP URL directly
- GitHub URLs must be from public LiveKit or LiveKit-Examples repositories

- `docs_search`: Search the docs for a given query. 
      Paged results will be returned, showing page titles, hiearchical placement, and (sometimes) a snippet of the content. 
      You must then use the get_page tool with any provided URL to get the full page content (except for reference pages, which you must fetch from the web directly by URL).
      The search index is not perfect, as it covers a large amount of content in many different programming languages. 
      Search should usually be used as a complement to browsing the docs directly, rather than as a replacement for it. To browse the docs directly, use the get_docs_overview and get_pages tools.
      So examine the returned results critically and perform additional searches or fetch individual pages if necessary to find what you're looking for.
- `get_changelog`: Get recent changelog/releases for a LiveKit repository.

Use for: "What's new in Python Agents?", "Recent Swift SDK updates", "Has feature X been added?"

Prefer using package identifiers (e.g., "npm:livekit-client", "pypi:livekit-agents", "cargo:livekit") over repository IDs. Package identifiers are automatically resolved to their corresponding repository. For monorepos like rust-sdks or python-sdks, package identifiers help disambiguate which specific package you're interested in. Repository IDs (e.g., "livekit/client-sdk-js") are also supported but package identifiers are preferred.
- `get_python_agent_example`: Browse and retrieve full example source code for various agents built with LiveKit Agents for Python, from the repository at http://github.com/livekit-examples/python-agents-examples

Without name parameter: Returns index of all 100+ examples with metadata (title, description, tags, difficulty, category).

With name parameter: Fetches full source code for the specific example directory. Do not use github URLs from another tools, check list of examples first using this tool.

Examples of names: "avatars/hedra/dynamically_created_avatar/agent.py", "basics/tool_calling.py", "complex-agents/drive-thru/agent.py"
- `submit_docs_feedback`: Submit constructive feedback on the LiveKit docs site in general or for a specific page.
      This feedback will be read by the LiveKit team and used to improve the docs.

      Examples of useful feedback
      - { 'page': '/agents/models/llm/inference/openai', 'feedback': 'It would be helpful to list more parameters that can be passed to the extra_kwargs parameter.' }
      - { 'feedback': 'The docs site is missing guides or examples for real-time object detection, and bounding box generation, in a video feed.' }

      Optional agent identification:
      - To help us understand how this MCP server is being used, and the context of the feedback, you can optionally identify yourself by agent name (e.g. "Cursor") and model ID (e.g. "gpt-5")

      IMPORTANT: Do not include any personal or proprietary information in the feedback or agent identification.
      
- `code_search`: Search GitHub code in LiveKit repos (scoped allowlist). Returns structured results.

High-precision GitHub code search across LiveKit repositories.
Search like code, not like English. Use actual class names, function names, method calls - not descriptions.
GOOD: "class AgentSession", "def on_enter", "@function_tool", "async def update_activity", "session.update_agent"
BAD: "how does handoff work", "agent transfer implementation", "context preservation strategy"
Workflow: Search class/function name to get snippets, then use returnFullFile=true to get implementation, then use get_pages() for related files.
Parameters: language="Python" (always), returnFullFile=false (exploration), returnFullFile=true (deep dive), scope="content" (default), limit=5-10
It's grep not RAG, search for code tokens not descriptions. Regex is not supported.
For examples use the get_python_agent_example tool instead.

Results come from default branches; very new code in feature branches may not appear.
When returnFullFile is true, complete file contents are fetched (may be slower for many results, use only with narrow queries)

## Usage Pattern

When the user's request matches this skill's capabilities:

**Step 1: Identify the right tool** from the list above

**Step 2: Generate a tool call** in this JSON format:

```json
{
  "tool": "tool_name",
  "arguments": {
    "param1": "value1",
    "param2": "value2"
  }
}
```

**Step 3: Execute via bash:**

```bash
python .claude/skills/mcp-skills/executor.py --skill livekit-docs --call 'YOUR_JSON_HERE'
```


## Getting Tool Details

If you need detailed information about a specific tool's parameters:

```bash
python .claude/skills/mcp-skills/executor.py --skill livekit-docs --describe tool_name
```

This loads ONLY that tool's schema, not all tools.

## Examples

### Example 1: Simple tool call

User: "Get LiveKit docs overview"

Your workflow:
1. Identify tool: `get_docs_overview`
2. Generate call JSON
3. Execute:

```bash
python .claude/skills/mcp-skills/executor.py --skill livekit-docs --call '{"tool": "get_docs_overview", "arguments": {}}'
```

### Example 2: Get tool details first

```bash
python .claude/skills/mcp-skills/executor.py --skill livekit-docs --describe docs_search
```

Returns the full schema, then you can generate the appropriate call.

## Error Handling

If the executor returns an error:
- Check the tool name is correct
- Verify required arguments are provided
- Ensure the MCP server is accessible

## Performance Notes

Context usage comparison for this skill:

| Scenario | MCP (preload) | Skill (dynamic) |
|----------|---------------|-----------------|
| Idle | 3500 tokens | 100 tokens |
| Active | 3500 tokens | 5k tokens |
| Executing | 3500 tokens | 0 tokens |

Savings: ~-42% reduction in typical usage

---

*This skill was auto-generated from an MCP server configuration.*
*Generator: mcp_to_skill.py*
