---
name: ace-tool
description: |
  Semantic codebase search and prompt enhancement via standalone CLI. Use when: (1) Semantic code search with natural language queries, (2) Prompt enhancement with codebase context, (3) Before grep/find/glob operations for better accuracy, (4) Complex requirements clarification, (5) Large codebase navigation. Triggers: "search context", "enhance prompt", "find code that", "clarify requirements". IMPORTANT: Always use ace-tool BEFORE grep/find/glob for semantic-level code location.
---

# ACE-Tool - Semantic Code Search & Prompt Enhancement

High-performance semantic search and AI-powered prompt enhancement. Standalone CLI (no MCP dependency).

## Execution Methods

```bash
# Prerequisites: pip install httpx tenacity
# Environment: ACE_API_URL, ACE_API_TOKEN (optional for local fallback)

# Search codebase with natural language
python scripts/ace_cli.py search_context -p /path/to/project -q "function that handles authentication"

# Enhance prompt (interactive mode - default, opens browser)
python scripts/ace_cli.py enhance_prompt -p "implement login feature" -H "User: what auth method?\nAssistant: JWT"

# Enhance prompt (non-interactive, JSON output)
python scripts/ace_cli.py enhance_prompt --no-interactive -p "implement login feature"

# Enhance prompt with specific endpoint
python scripts/ace_cli.py --endpoint claude enhance_prompt -p "implement login feature"

# Check configuration
python scripts/ace_cli.py get_config
```

## Tool Routing Policy

### Prefer ACE-Tool Over Built-in Tools

| Task | Avoid | Use ACE-Tool CLI |
|------|-------|------------------|
| Find function by purpose | `grep "def func"` | `search_context -q "function that..."` |
| Locate feature code | `find . -name "*.py"` | `search_context -q "feature description"` |
| Clarify requirements | Manual analysis | `enhance_prompt -p "requirement"` |
| Understand code flow | Multiple grep/read | `search_context -q "flow description"` |

### When to Use Built-in Tools
- Exact string matching (known identifiers)
- File path patterns (known naming conventions)
- Simple text replacement

## Command Reference

### search_context
Search codebase using natural language descriptions.

```bash
python scripts/ace_cli.py search_context -p <project_root> -q <query>

Options:
  -p, --project-root    Project root path (required)
  -q, --query           Natural language query (required)
```

### enhance_prompt
Enhance prompts with codebase context and conversation history.

```bash
python scripts/ace_cli.py [--endpoint TYPE] enhance_prompt -p <prompt> [options]

Global Options:
  --endpoint            Endpoint type: new, old, claude, openai, gemini (default: new)
  --api-url             Override API base URL
  --token               Override API token

Command Options:
  -p, --prompt          Original prompt (required)
  -H, --history         Conversation history: "User: xxx\nAssistant: yyy"
  --history-file        File containing conversation history
  --project-root        Project root path (optional)
  --no-interactive      Disable web UI, output JSON directly
  --no-browser          Don't auto-open browser, just print URL
  --port                Port for web server (default: 8765)
```

### get_config
Show current configuration status.

```bash
python scripts/ace_cli.py get_config
```

## Interactive Enhancement

Default mode opens web UI with actions:

| Button | Action |
|--------|--------|
| **Regenerate** | Discard current, generate new enhancement from original prompt |
| **Refine** | Iteratively improve current version, preserving your edits |
| **Use Original** | Return the original prompt without enhancement |
| **Send Enhanced** | Confirm and use the current enhanced prompt |
| **Cancel** | Abort the enhancement process |

**Keyboard Shortcuts:** `Ctrl+Enter` Send | `Esc` Cancel

## Workflow

### Phase 1: Semantic Search
```bash
search_context -p . -q "database connection pooling"  # Find relevant code
# Review returned file locations
# Read specific files for details
```

### Phase 2: Prompt Enhancement
```bash
enhance_prompt -p "optimize query performance"        # Opens interactive UI
# Review and refine enhanced prompt
# Use Regenerate/Refine as needed
# Send Enhanced to confirm
```

## Error Handling

```json
{"error": "error message", "status_code": 401}
```

| Error | Recovery |
|-------|----------|
| No API configured | Uses local fallback for search_context |
| Token invalid (401) | Check API token |
| Access denied (403) | Token may be disabled |
| Connection timeout | Retries up to 3 times with exponential backoff |
| No results | Broaden search query |

## Anti-Patterns

| Prohibited | Correct |
|------------|---------|
| Grep before semantic search | Use `search_context` first |
| Skip prompt enhancement | Use `enhance_prompt` for complex tasks |
| Ignore conversation history | Include history in `enhance_prompt` |
| Use exact match for conceptual search | Use natural language query |
| Always use non-interactive mode | Use interactive mode for review |
