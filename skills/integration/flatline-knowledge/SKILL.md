# Flatline Knowledge Skill

## Purpose

Provides optional NotebookLM integration for the Flatline Protocol, enabling external knowledge retrieval from curated AI-powered notebooks.

## Overview

This skill automates browser interaction with Google NotebookLM to query organizational knowledge bases. It serves as a Tier 2 knowledge source, supplementing the local grimoire search (Tier 1).

## Architecture

```
Flatline Protocol
       │
       ▼
┌─────────────────┐
│ Knowledge Hub   │
├─────────────────┤
│ Tier 1: Local   │◄── Framework learnings, project context
│ Weight: 1.0     │    (always available)
├─────────────────┤
│ Tier 2: NLML    │◄── NotebookLM curated sources
│ Weight: 0.8     │    (this skill, optional)
└─────────────────┘
```

## Prerequisites

1. **Python 3.10+** with Patchright installed
2. **Chromium browser** available on PATH
3. **Google account** with NotebookLM access
4. **Initial authentication** completed (one-time setup)

## Workflow

### 1. Check Availability

```python
# Check if NotebookLM is configured and authenticated
if not config.notebooklm.enabled:
    return {"status": "disabled", "results": []}

if not auth_session_valid():
    warn("NotebookLM session expired. Using local knowledge only.")
    return {"status": "auth_expired", "results": []}
```

### 2. Query NotebookLM

```python
# Launch browser with persistent session
async with patchright.async_playwright() as p:
    browser = await p.chromium.launch_persistent_context(
        user_data_dir="~/.claude/notebooklm-auth/",
        headless=True
    )

    # Navigate to notebook
    page = await browser.new_page()
    await page.goto(f"https://notebooklm.google.com/notebook/{notebook_id}")

    # Submit query
    query = f"{domain} {phase} best practices"
    await page.fill("textarea[aria-label='Ask']", query)
    await page.click("button[aria-label='Submit']")

    # Wait for response
    await page.wait_for_selector(".response-content", timeout=30000)

    # Extract results
    response = await page.text_content(".response-content")
    citations = await page.query_selector_all(".citation")
```

### 3. Format Results

```python
# Return structured knowledge
return {
    "status": "success",
    "results": [
        {
            "content": response,
            "citations": [c.text for c in citations],
            "source": "notebooklm",
            "weight": 0.8,
            "latency_ms": elapsed
        }
    ]
}
```

## Error Handling

| Scenario | Behavior | User Impact |
|----------|----------|-------------|
| NotebookLM disabled | Skip gracefully | None (silent) |
| Auth expired | Warn, fallback to local | Warning message |
| Timeout (>30s) | Warn, fallback to local | Warning message |
| Browser unavailable | Warn, fallback to local | Warning message |
| Network error | Warn, fallback to local | Warning message |

**Critical**: This skill NEVER blocks the Flatline Protocol workflow. All failures result in graceful fallback to local knowledge.

## Configuration

In `.loa.config.yaml`:

```yaml
flatline_protocol:
  knowledge:
    notebooklm:
      enabled: false  # Disabled by default
      notebook_id: "your-notebook-id"
      timeout_ms: 30000
      headless: true
```

## Authentication Setup

See `resources/auth-setup.md` for detailed instructions.

Quick start:
1. Run `python resources/notebooklm-query.py --setup-auth`
2. Complete Google sign-in in the browser window
3. Session is saved to `~/.claude/notebooklm-auth/`

## Usage

### From Orchestrator

The orchestrator calls this skill automatically when:
- `flatline_protocol.knowledge.notebooklm.enabled: true`
- Local knowledge retrieval completes

### Manual Testing

```bash
# Dry run (no browser)
python resources/notebooklm-query.py --domain "security" --phase prd --dry-run

# With authentication
python resources/notebooklm-query.py --domain "crypto wallet" --phase sdd --notebook "loa-learnings"

# Setup authentication
python resources/notebooklm-query.py --setup-auth
```

## Integration Points

### Input (from Flatline Orchestrator)

```json
{
  "domain": "crypto wallet authentication",
  "phase": "prd",
  "notebook_id": "abc123",
  "timeout_ms": 30000
}
```

### Output (to Flatline Orchestrator)

```json
{
  "status": "success",
  "results": [
    {
      "content": "Key considerations for crypto wallet PRDs include...",
      "citations": ["Source 1", "Source 2"],
      "source": "notebooklm",
      "weight": 0.8
    }
  ],
  "latency_ms": 5234
}
```

## Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Latency P50 | <10s | From query submit to response |
| Latency P95 | <25s | Browser automation overhead |
| Success rate | >90% | When enabled and authenticated |
| Timeout rate | <5% | Queries exceeding 30s |

## Privacy Considerations

- Requires Google account authentication
- Queries are sent to Google NotebookLM service
- Session data stored locally in `~/.claude/notebooklm-auth/`
- No query logging by default (configurable)

## Troubleshooting

### Common Issues

**"Auth session expired"**
- Re-run `--setup-auth` to refresh authentication

**"Browser not found"**
- Ensure Chromium is installed: `which chromium`
- Or install: `apt install chromium` / `brew install chromium`

**"Timeout waiting for response"**
- Check NotebookLM service status
- Increase timeout in config
- Network latency may exceed 30s for complex queries

**"Module patchright not found"**
- Install: `pip install patchright`
- Ensure correct Python environment is active

## Resources

- `resources/notebooklm-query.py` - Browser automation script
- `resources/requirements.txt` - Python dependencies
- `resources/auth-setup.md` - Authentication documentation
