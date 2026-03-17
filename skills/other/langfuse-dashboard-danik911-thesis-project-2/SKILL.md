---
name: langfuse-dashboard
description: Automates Langfuse Cloud dashboard interactions using Playwright MCP. Captures screenshots for documentation, extracts metrics for monitoring, navigates trace details for investigation, and handles authentication. Use when documenting workflows, creating compliance screenshots, monitoring dashboard metrics, or investigating traces visually. MUST use Playwright MCP tools (mcp__playwright__*) for browser automation.
allowed-tools: ["Bash", "Read", "Write", "mcp__playwright__browser_navigate", "mcp__playwright__browser_snapshot", "mcp__playwright__browser_take_screenshot", "mcp__playwright__browser_click", "mcp__playwright__browser_wait_for", "mcp__playwright__browser_evaluate", "mcp__playwright__browser_close"]
---

# Langfuse Dashboard Skill

**Purpose**: Automate Langfuse Cloud dashboard interactions via Playwright MCP for screenshots, metrics, and trace investigation.

**Dashboard URL**: https://cloud.langfuse.com/project/cmhuwhcfe006yad06cqfub107

---

## When to Use This Skill

✅ **Use when**:
- Capturing dashboard screenshots for documentation or compliance reports
- Extracting metrics (trace count, costs, latency) for monitoring/alerting
- Navigating to specific trace details for visual investigation
- Creating walkthrough documentation with annotated screenshots
- Automating repetitive dashboard checks

❌ **Do NOT use when**:
- Programmatic data extraction (use `langfuse-extraction` skill with API)
- Adding instrumentation to code (use `langfuse-integration` skill)

---

## Prerequisites

1. **Playwright MCP server enabled** (`/mcp` command)
2. **Langfuse Cloud account** with project access
3. **Authentication**: Login cookies or credentials ready

---

## Common Workflows

### Workflow 1: Capture Dashboard Overview Screenshot

```
Purpose: Document current dashboard state for reports

Steps:
1. Navigate to dashboard
2. Wait for content to load (CRITICAL: networkidle)
3. Take full-page screenshot
4. Save with timestamp
```

**MCP Tools Sequence**:
```python
# Step 1: Navigate
mcp__playwright__browser_navigate(
    url="https://cloud.langfuse.com/project/cmhuwhcfe006yad06cqfub107/traces"
)

# Step 2: Wait for load (CRITICAL)
mcp__playwright__browser_wait_for(time=3)  # Wait 3 seconds for React app

# Step 3: Take screenshot
mcp__playwright__browser_take_screenshot(
    fullPage=True,
    filename=f"langfuse_dashboard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
)
```

### Workflow 2: Extract Dashboard Metrics

```
Purpose: Get metrics for monitoring/alerting

Steps:
1. Navigate to dashboard
2. Wait for networkidle
3. Snapshot accessibility tree
4. Evaluate JavaScript to extract metrics from DOM
5. Return metrics as structured data
```

**MCP Tools Sequence**:
```python
# Navigate and wait
mcp__playwright__browser_navigate(
    url="https://cloud.langfuse.com/project/cmhuwhcfe006yad06cqfub107"
)

mcp__playwright__browser_wait_for(time=5)

# Snapshot (better than screenshot for data extraction)
snapshot = mcp__playwright__browser_snapshot()

# Evaluate JavaScript to extract metrics
metrics = mcp__playwright__browser_evaluate(
    function="""
    () => {
        return {
            total_traces: document.querySelector('[data-testid="trace-count"]')?.textContent || 'N/A',
            avg_latency: document.querySelector('[data-testid="avg-latency"]')?.textContent || 'N/A',
            total_cost: document.querySelector('[data-testid="total-cost"]')?.textContent || 'N/A'
        };
    }
    """
)

print(f"Metrics: {metrics}")
```

### Workflow 3: Navigate to Specific Trace

```
Purpose: Investigate specific trace visually in dashboard

Steps:
1. Navigate directly to trace URL
2. Wait for trace tree to load
3. Click "Expand All" to show all spans
4. Take screenshot of full trace
5. Optionally extract span data from DOM
```

**MCP Tools Sequence**:
```python
trace_id = "abc123def456"

# Navigate to trace
mcp__playwright__browser_navigate(
    url=f"https://cloud.langfuse.com/trace/{trace_id}"
)

# Wait for trace tree
mcp__playwright__browser_wait_for(time=5)

# Expand all spans (if button exists)
try:
    mcp__playwright__browser_click(
        element="Expand All button",
        ref="[data-testid='expand-all']"
    )
except:
    pass  # Button may not exist

# Screenshot
mcp__playwright__browser_take_screenshot(
    fullPage=True,
    filename=f"trace_{trace_id}_investigation.png"
)
```

### Workflow 4: Filter Traces by Tag

```
Purpose: View only pharmaceutical/gamp5 tagged traces

Steps:
1. Navigate to traces page
2. Wait for load
3. Click filter dropdown
4. Select "pharmaceutical" tag
5. Screenshot filtered view
```

**MCP Tools Sequence**:
```python
mcp__playwright__browser_navigate(
    url="https://cloud.langfuse.com/project/cmhuwhcfe006yad06cqfub107/traces"
)

mcp__playwright__browser_wait_for(time=3)

# Click filter button
mcp__playwright__browser_click(
    element="Filter button",
    ref="[data-testid='filter-button']"
)

# Click tag filter
mcp__playwright__browser_click(
    element="Tag filter: pharmaceutical",
    ref="[data-tag='pharmaceutical']"
)

# Screenshot filtered results
mcp__playwright__browser_take_screenshot(
    fullPage=True,
    filename="filtered_pharmaceutical_traces.png"
)
```

---

## Best Practices

### Always Wait for Network Idle

**CRITICAL**: Langfuse dashboard is a React app that loads asynchronously.

```python
# WRONG (will capture blank page)
mcp__playwright__browser_navigate(url=dashboard_url)
mcp__playwright__browser_take_screenshot(...)  # Too fast!

# CORRECT
mcp__playwright__browser_navigate(url=dashboard_url)
mcp__playwright__browser_wait_for(time=5)  # Wait for React to render
mcp__playwright__browser_take_screenshot(...)
```

### Use Snapshots for Data Extraction

**Snapshots** (accessibility tree) are better than screenshots for extracting data:

```python
# For visual documentation: Use screenshot
mcp__playwright__browser_take_screenshot(fullPage=True)

# For data extraction: Use snapshot
snapshot = mcp__playwright__browser_snapshot()
# Returns structured accessibility tree with text content
```

### Handle Authentication

If not logged in, Langfuse redirects to login page. Options:

1. **Manual login** before automation (recommended for development)
2. **Cookie injection** (for CI/CD)
3. **Clerk auth flow** (complex, avoid if possible)

---

## Common Dashboard URLs

```python
PROJECT_ID = "cmhuwhcfe006yad06cqfub107"

urls = {
    "traces": f"https://cloud.langfuse.com/project/{PROJECT_ID}/traces",
    "sessions": f"https://cloud.langfuse.com/project/{PROJECT_ID}/sessions",
    "users": f"https://cloud.langfuse.com/project/{PROJECT_ID}/users",
    "metrics": f"https://cloud.langfuse.com/project/{PROJECT_ID}/metrics",
    "settings": f"https://cloud.langfuse.com/project/{PROJECT_ID}/settings",
    "specific_trace": lambda trace_id: f"https://cloud.langfuse.com/trace/{trace_id}"
}
```

---

## Troubleshooting

### Issue: Blank Screenshots

**Cause**: Page not fully loaded.

**Solution**: Increase wait time.

```python
mcp__playwright__browser_wait_for(time=10)  # Increase to 10 seconds
```

### Issue: Element Not Found

**Cause**: Langfuse UI changed or element not visible.

**Solution**: Use accessibility snapshot to find correct selector.

```python
snapshot = mcp__playwright__browser_snapshot()
# Inspect snapshot for correct element reference
```

### Issue: Authentication Required

**Cause**: Not logged in.

**Solution**: Login manually first, or skip dashboard skill and use API (`langfuse-extraction`).

---

## Success Criteria

- ✅ Screenshots captured with full page content
- ✅ Metrics extracted successfully from DOM
- ✅ Trace navigation works with correct URL
- ✅ No timeout errors (proper wait times)
- ✅ Authentication handled (manual login or cookies)

---

## Reference Materials

- **playwright-patterns.md**: Common Playwright MCP automation patterns
- **dashboard-navigation.md**: Langfuse UI structure and selectors

---

**Skill Version**: 1.0.0
**Last Updated**: 2025-01-17
**Playwright MCP**: Enabled via /mcp command
**Dashboard**: cloud.langfuse.com
