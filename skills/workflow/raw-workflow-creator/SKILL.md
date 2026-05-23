---
name: raw-workflow-creator
description: Create and run RAW workflows. Use this skill when the user asks to create a workflow, automate a task, build a data pipeline, generate reports, or asks "How do I build X with RAW?".
---

# RAW Workflow Creator Skill

Create and implement RAW workflows from user intent.

## When to Use This Skill

Use this skill when the user wants to:
- Create a new automated workflow
- Build a data pipeline (fetch → process → save)
- Automate a repetitive task
- Generate reports from data sources

---

## ⛔ MANDATORY RULES - READ FIRST

These rules are **non-negotiable**. Violating them creates technical debt and defeats the purpose of RAW.

### Rule 1: NEVER Write API Calls Directly in run.py

```
⛔ WRONG - API call in workflow
─────────────────────────────────
@step("fetch")
def fetch_prices(self) -> dict:
    response = httpx.get("https://api.coingecko.com/...")  # ← VIOLATION
    return response.json()
```

```
✅ CORRECT - API call in tool, imported in workflow
─────────────────────────────────────────────────────
# First: raw create coingecko --tool -d "Fetch crypto prices from CoinGecko API"
# Then: implement tools/coingecko/tool.py
# Then: use in workflow

from tools.coingecko import fetch_prices

@step("fetch")
def fetch_prices(self) -> dict:
    return fetch_prices(coins=["bitcoin", "ethereum"])  # ← Uses tool
```

**Why this matters:** Tools are reusable. The next workflow needing crypto prices imports the existing tool instead of copy-pasting code. Without tools, every workflow becomes a silo.

### Rule 2: SEARCH Before Creating ANY Tool

```bash
# ALWAYS do this first - try multiple search terms
raw search "crypto price"
raw search "coingecko"
raw search "bitcoin"
```

Only create a tool if ALL relevant searches return nothing.

### Rule 3: Complete Tool Checklist

Before writing ANY code in run.py, complete this checklist:

```
□ Listed all external API calls needed
□ Searched for each capability (multiple search terms)
□ Created tools for any missing capabilities
□ Implemented tool.py and __init__.py for each new tool
□ ONLY NOW ready to write run.py
```

---

## Key Directives

1. **TOOLS ARE REUSABLE LIBRARIES** - Tools live in `tools/` as Python packages. They're created on-demand during workflow implementation when a capability is needed.
2. **SEARCH → CREATE → USE** - When a workflow step needs a capability: search with `raw search`, create the tool if missing, then import and use it.
3. **NEVER DUPLICATE** - If you're writing API calls, data processing, or service integrations that could be reused, put them in a tool first.
4. **ALWAYS use `raw create`** to scaffold workflows - do not manually create directories
5. **ALWAYS test with `raw run --dry`** before telling the user the workflow is ready
6. **Use Pydantic** for all workflow parameters - provides validation and documentation

## Prerequisites Checklist

Before creating a workflow, verify:
- [ ] RAW is initialized (`raw init` has been run, `.raw/` directory exists)
- [ ] User has provided clear intent (what data, what processing, what output)
- [ ] Required external APIs/services are accessible (if applicable)

If RAW is not initialized, run:
```bash
raw init
```

## Requirements Validation (Ask Before Building)

**Before implementing, ask clarifying questions when:**

| Ambiguity | Example Question |
|-----------|------------------|
| Data source unclear | "Should I use Alpha Vantage or Yahoo Finance for stock data?" |
| Output format unspecified | "Do you want the report as JSON, PDF, or Markdown?" |
| Parameters ambiguous | "How many items? What time range? Which categories?" |
| Delivery method unclear | "Should I save to file, post to Slack, or both?" |
| Provider choice needed | "You have OpenAI and Anthropic configured. Which should I use for summarization?" |

**Check available providers first:**
```python
from raw_runtime import get_available_providers
providers = get_available_providers()
# {'llm': ['openai', 'anthropic'], 'messaging': ['slack'], 'data': ['alphavantage']}
```

Inform the user what's configured before asking about preferences. If only one provider is available for a category, use it without asking.

## Workflow Creation Process

### Step 1: Create Workflow Draft

```bash
raw create <name> --intent "<detailed description>"
```

**IMPORTANT**: The intent should be specific and searchable. Extract details from user request:
- What data sources (APIs, files, databases)
- What processing (calculations, transformations)
- What outputs (files, reports, notifications)

**Writing searchable intents:**

Intents are indexed for semantic search. Structure them for discoverability:

`[Action] [domain-specific data] from [source], [process steps], then [output format]`

Good examples:
```
Fetch TSLA stock data from Yahoo Finance, calculate 50-day moving average and RSI, generate PDF report with price charts
Scrape product prices from e-commerce sites, track changes over time, send email alerts when prices drop
Parse server logs from CloudWatch, aggregate error counts by service, export daily summary to Slack
```

Rules:
- Start with action verb: Fetch, Scrape, Parse, Analyze, Generate, Monitor
- Name specific sources: Yahoo Finance, AWS S3, PostgreSQL, Slack API
- List processing steps: calculate, aggregate, filter, transform
- Specify output: PDF report, email alert, JSON file, Slack message
- Include domain keywords users might search for

### Step 2: Implement run.py (with tools)

**Write the implementation file** at `.raw/workflows/<id>/run.py`.

**For each capability needed in your workflow steps:**

1. **Search for existing tools:**
   ```bash
   raw search "hackernews"        # Does a HN tool exist?
   raw search "llm summarize"     # Does an LLM tool exist?
   ```

2. **If LOCAL tool exists** → Import and use it:
   ```python
   from tools.hackernews import fetch_top_stories
   stories = fetch_top_stories(limit=3)
   ```

3. **If REMOTE tool exists** → Install it:
   ```bash
   raw install <git-url>
   # Then import as above
   ```

4. **If NO tool exists** → Create it as a reusable library:
   ```bash
   raw create hackernews --tool -d "Fetch top stories from HackerNews API"
   ```
   Then implement `tools/hackernews/tool.py` and `tools/hackernews/__init__.py`.

**Tools are just Python packages in `tools/`.** They're created on-demand or installed.

**Automatic tool snapshotting:** When you run a workflow with `raw run`, RAW automatically:
1. Copies used tools from `tools/` to `_tools/` in the workflow run directory
2. Rewrites imports from `tools.X` to `_tools.X`
3. Records provenance (git commit, content hash) in `origin.json`

This makes workflows self-contained and portable. Write imports as `from tools.X import ...` - RAW handles the rest.

**Example tool (`tools/hackernews/tool.py`):**
```python
"""Fetch stories from HackerNews API."""
import httpx

def fetch_top_stories(limit: int = 10) -> list[dict]:
    """Fetch top stories from HackerNews."""
    response = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    story_ids = response.json()[:limit]
    # ... fetch each story
    return stories
```

**Example `__init__.py`:**
```python
"""HackerNews API client."""
from .tool import fetch_top_stories

__all__ = ["fetch_top_stories"]
```

**Workflow template using tools:**

```python
#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["pydantic>=2.0", "rich>=13.0"]
# ///
"""<Workflow description>"""

from pydantic import BaseModel, Field
from raw_runtime import BaseWorkflow, step

# Import from tools - capabilities created during implementation
from tools.hackernews import fetch_top_stories


class WorkflowParams(BaseModel):
    limit: int = Field(default=3, description="Number of stories")


class MyWorkflow(BaseWorkflow[WorkflowParams]):
    @step("fetch")
    def fetch_stories(self) -> list[dict]:
        # Use the tool - don't reimplement the API call here
        return fetch_top_stories(limit=self.params.limit)

    def run(self) -> int:
        stories = self.fetch_stories()
        self.save("stories.json", stories)
        return 0


if __name__ == "__main__":
    MyWorkflow.main()
```

### Step 3: Create dry_run.py

Generate template or create manually:
```bash
raw run <id> --dry --init
```

Then edit `.raw/workflows/<id>/dry_run.py` to use mock data instead of real API calls.

### Step 4: Add Mock Data

Create mock files in `.raw/workflows/<id>/mocks/`:
```json
// mocks/api_response.json
{
  "status": "ok",
  "data": [...]
}
```

### Step 5: Test

```bash
raw run <id> --dry
```

**ONLY tell the user the workflow is ready if dry-run succeeds.**

### Step 6: Report to User

After successful dry-run, tell the user:
```
Workflow created and tested:
- ID: <workflow-id>
- Run: raw run <id> [--args]
- To publish: raw publish <id>
```

## Decorators

See [references/decorator_usage.md](references/decorator_usage.md) for `@step`, `@retry`, and `@cache_step` usage.

## Decision tree

```
User wants workflow
    │
    ├─► Is RAW initialized?
    │       NO → Run `raw init`
    │       YES → Continue
    │
    ├─► Extract intent details
    │       - Data sources?
    │       - Processing steps?
    │       - Output format?
    │
    ├─► Create draft: `raw create <name> --intent "..."`
    │
    │   ╔══════════════════════════════════════════════════════════════╗
    │   ║  ⛔ STOP - TOOL CHECKPOINT                                   ║
    │   ║                                                              ║
    │   ║  List ALL external calls your workflow needs:                ║
    │   ║    • API calls (REST, GraphQL)                               ║
    │   ║    • Database queries                                        ║
    │   ║    • File downloads                                          ║
    │   ║    • Service integrations                                    ║
    │   ║                                                              ║
    │   ║  For EACH capability:                                        ║
    │   ║    1. raw search "<capability>"                              ║
    │   ║    2. raw search "<service name>"                            ║
    │   ║    3. If not found: raw create <name> --tool -d "..."        ║
    │   ║    4. Implement tools/<name>/tool.py                         ║
    │   ║                                                              ║
    │   ║  DO NOT proceed to run.py until all tools exist!             ║
    │   ╚══════════════════════════════════════════════════════════════╝
    │
    ├─► Implement run.py
    │       - WorkflowParams from intent
    │       - Import tools (from tools.X import ...)
    │       - NO direct API calls - only tool imports
    │       - fetch/process/save steps using tools
    │
    ├─► Create dry_run.py with mocks
    │       `raw run <id> --dry --init`
    │
    ├─► Test: `raw run <id> --dry`
    │       FAIL → Fix and retry
    │       PASS → Continue
    │
    └─► Report success to user
```

See [references/workflow_patterns.md](references/workflow_patterns.md) for data pipeline, aggregation, and report generation patterns.

## Validation checklist

Before reporting success:
- [ ] **All external calls use tools** (no `httpx.get`, `requests.get`, etc. in run.py)
- [ ] Tools exist in `tools/` for every API/service integration
- [ ] `run.py` only imports from tools, no direct HTTP/DB calls
- [ ] `run.py` exists and has no syntax errors
- [ ] `dry_run.py` exists with mock data
- [ ] `raw run <id> --dry` completes without errors
- [ ] Output files are created in `results/`

## Error Recovery

When things go wrong, follow this recovery process:

### Dependency Errors
```
Error: No module named 'pandas'
```
**Fix:** Add missing dependency to PEP 723 header in `run.py`:
```python
# /// script
# dependencies = ["pandas>=2.0"]
# ///
```

### API Failures
```
requests.exceptions.HTTPError: 429 Too Many Requests
```
**Fix:** Add retry logic with backoff:
```python
from raw_runtime import retry

@retry(retries=3, backoff="exponential")
def fetch(self) -> dict:
    return requests.get(url).json()
```

### Test Failures
1. Read the error message carefully
2. Check if mock data matches expected format
3. Verify API responses haven't changed
4. Tell the user what failed and ask if they want you to fix it

### When Stuck
If you cannot resolve an error after 2 attempts:
1. Explain clearly what's failing and why
2. Show the error message
3. Suggest alternatives or workarounds
4. Ask the user how they'd like to proceed

## Common pitfalls

**#1 mistake: Direct API calls in workflows.** Never write `httpx.get()` or `requests.get()` in run.py. Move API logic to a tool, then import it.

See [references/testing_guide.md](references/testing_guide.md) for error catalog and troubleshooting.

## Progress communication

Keep the user informed during workflow creation:

### During Implementation
```
Creating crypto-report workflow...

  1. TOOL CHECKPOINT
     ├─ Need: Crypto price API
     │   └─ raw search "crypto price"... not found
     │   └─ raw search "coingecko"... not found
     │   └─ Creating tool: raw create coingecko --tool
     │   └─ ✓ Implemented tools/coingecko/tool.py
     │
     └─ All tools ready ✓

  2. WORKFLOW IMPLEMENTATION
     ├─ ✓ Created workflow scaffold
     ├─ ✓ Implementing run.py (imports tools/coingecko)
     ├─ ✓ Creating dry_run.py with mock data
     └─ ⏳ Testing with dry-run...
```

### For Long Operations
If a step takes more than a few seconds, explain what's happening:
```
Fetching stock data for TSLA (this may take 10-15 seconds due to API rate limits)...
```

### After Completion
Always provide a clear summary:
```
✓ Workflow created and tested successfully!

  ID: 20251207-stock-report-abc123

  To run: raw run stock-report --ticker TSLA
  To publish: raw publish stock-report

  The workflow fetches stock data from Yahoo Finance,
  calculates technical indicators, and saves a report to results/.
```

### On Failure
Be specific about what failed and what to do:
```
✗ Workflow test failed

  Error: API returned 401 Unauthorized

  This usually means the API key is missing or invalid.

  To fix:
  1. Check that ALPHAVANTAGE_API_KEY is set in your .env file
  2. Verify the key is valid at alphavantage.co

  Would you like me to help troubleshoot?
```

## Security

See [references/security.md](references/security.md) for security checklist and secure coding patterns.

## References

- [Workflow Patterns](references/workflow_patterns.md)
- [Decorator Usage](references/decorator_usage.md)
- [Testing Guide](references/testing_guide.md)
