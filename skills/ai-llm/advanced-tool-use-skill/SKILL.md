---
name: advanced-tool-use
category: backend
version: 2.0.0
description: Context-efficient tool management via search, deferred loading, and programmatic calling
author: Unite Group
priority: 3
triggers:
  - tool use
  - context optimization
  - token efficiency
  - tool search
  - programmatic calling
---

# Advanced Tool Use System

Context-efficient tool management via search, deferred loading, and programmatic calling.

## Features

| Feature | Benefit | API Type |
|---------|---------|----------|
| Tool Search | 85% context reduction | `tool_search_tool_regex_20251119` |
| Programmatic Calling | 37% token reduction | `allowed_callers: ["code_execution_20250825"]` |
| Tool Examples | 72%→90% accuracy | Examples in tool definition |
| Deferred Loading | On-demand only | `defer_loading: true` |

## Tool Categories

| Category | Loading | Examples |
|----------|---------|----------|
| CORE | Always | health_check, get_task_status |
| VERIFICATION | Deferred | verify_task, collect_evidence |
| DATABASE | Deferred | query, insert |
| FILE_SYSTEM | Deferred | read, write, list |
| AUSTRALIAN_CONTEXT | Always | format_date_au, format_currency_aud, validate_abn |

## Configuration

```python
@dataclass
class ToolConfig:
    defer_loading: bool = False      # Load on-demand via search
    allowed_callers: list[str] = []  # ["code_execution_20250825"]
    parallel_safe: bool = True
    cache_results: bool = False
    australian_context: bool = False # Load with Australian locale
```

## Usage

```python
from src.tools import register_all_tools
from src.tools.search import ToolSearcher

registry = register_all_tools()
searcher = ToolSearcher(registry)

# Search for tools (85% context savings)
results = searcher.search("verify outputs", limit=3)

# Get API tools with deferred loading
api_tools = registry.to_api_format(
    include_search_tool=True,
    include_deferred=False,
    locale="en-AU"  # Australian English
)

# Beta header required
headers = {"anthropic-beta": "advanced-tool-use-2025-11-20"}
```

## Context Savings

| Metric | Before | After |
|--------|--------|-------|
| Upfront tokens | 55,000 | 8,000 (85%) |
| Per-call tokens | 1,200 | 760 (37%) |
| Parameter accuracy | 72% | 90% |

## Australian Context Integration

When working with Australian data:

```python
# Tool for formatting Australian dates
@tool(australian_context=True)
async def format_date_au(date: datetime) -> str:
    """Format date in Australian DD/MM/YYYY format."""
    return date.strftime("%d/%m/%Y")

# Tool for formatting Australian currency
@tool(australian_context=True)
async def format_currency_aud(amount: float) -> str:
    """Format currency in AUD with proper formatting."""
    return f"${amount:,.2f}"

# Tool for validating ABN (Australian Business Number)
@tool(australian_context=True)
async def validate_abn(abn: str) -> bool:
    """Validate Australian Business Number (11 digits)."""
    # Validation logic for ABN
    cleaned = abn.replace(" ", "")
    if len(cleaned) != 11 or not cleaned.isdigit():
        return False
    # ABN checksum validation
    weights = [10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    digits = [int(d) for d in cleaned]
    digits[0] -= 1
    checksum = sum(d * w for d, w in zip(digits, weights))
    return checksum % 89 == 0
```

## Parallel Tool Execution

```python
async def execute_tools_parallel(tools: list[Tool], inputs: list[dict]) -> list[Result]:
    """Execute multiple tools in parallel for efficiency."""
    tasks = [tool.execute(**input_data) for tool, input_data in zip(tools, inputs)]
    return await asyncio.gather(*tasks, return_exceptions=True)
```

## Rules

- Mark infrequent tools as `defer_loading: true`
- Enable `allowed_callers` for batch operations
- Add examples for complex parameters
- Use categories/keywords for better search
- Monitor with `orchestrator.get_context_stats()`
- **NEW**: Set `australian_context: true` for Australian locale tools
- **NEW**: Use en-AU spelling in tool descriptions (colour, organisation)
- **NEW**: Validate Australian regulations in compliance tools (Privacy Act 1988)

## Integration with Agents

This skill is automatically loaded by:
- `.claude/agents/backend-specialist/` - For API development
- `.claude/agents/orchestrator/` - For tool coordination

See: `tools/`, `verification/verification-first.skill.md`
