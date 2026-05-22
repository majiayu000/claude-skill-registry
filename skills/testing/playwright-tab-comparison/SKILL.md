---
name: playwright-tab-comparison
description: Open multiple browser tabs and compare content, behavior, or visual appearance across pages. Use when comparing staging vs production, A/B testing page variants, testing cross-browser consistency, verifying content parity, or analyzing differences between multiple URLs. Trigger phrases include "compare these pages", "open multiple tabs and compare", "test consistency across", "A/B test", "staging vs production", or "compare versions". Works with Playwright MCP browser automation tools for multi-tab workflows.
---

# Playwright Tab Comparison

Open multiple browser tabs and systematically compare content, behavior, or visual appearance across pages.

## Quick Start

```
User: "Compare the staging and production checkout pages"

Workflow:
1. Create/list tabs
2. Navigate tab 1 to staging URL
3. Navigate tab 2 to production URL
4. For each tab: capture snapshot + screenshot + extract data
5. Generate comparison report
```

## When to Use This Skill

**Explicit triggers:**
- "Compare these pages"
- "Open multiple tabs and compare"
- "Test cross-browser consistency"
- "A/B test these variants"
- "Compare staging vs production"

**Implicit triggers:**
- User provides multiple URLs to analyze
- Testing consistency across environments
- Verifying content parity
- Evaluating page variants

**Use cases:**
- A/B testing different landing page designs
- Comparing staging vs production environments
- Cross-browser consistency validation
- Multi-variant feature testing
- Content parity verification
- Performance comparison

## Core Workflow

### Step 1: Tab Setup

**List existing tabs:**
```python
browser_tabs(action="list")
```

**Create additional tabs:**
```python
# Create new tab
browser_tabs(action="new")

# Switch to specific tab (0-indexed)
browser_tabs(action="select", index=1)
```

### Step 2: Navigate Each Tab

Navigate each tab to its target URL:

```python
# Tab 1: Production
browser_tabs(action="select", index=0)
browser_navigate(url="https://example.com/checkout")

# Tab 2: Staging
browser_tabs(action="select", index=1)
browser_navigate(url="https://staging.example.com/checkout")

# Tab 3: Variant A
browser_tabs(action="select", index=2)
browser_navigate(url="https://example.com/checkout?variant=a")
```

### Step 3: Capture Data from Each Tab

For each tab, collect comparison data:

**a) Capture accessibility snapshot:**
```python
browser_snapshot(filename="tab1-snapshot.md")
```

**b) Take screenshot:**
```python
browser_take_screenshot(filename="tab1-screenshot.png", fullPage=True)
```

**c) Extract structured data:**
```python
browser_evaluate(function="""
() => {
    return {
        title: document.title,
        url: window.location.href,
        headingCount: document.querySelectorAll('h1, h2, h3').length,
        buttonCount: document.querySelectorAll('button').length,
        formCount: document.querySelectorAll('form').length,
        // Custom extraction logic
        productPrice: document.querySelector('.price')?.textContent,
        ctaText: document.querySelector('.cta-button')?.textContent
    };
}
""")
```

**d) Capture network activity (optional):**
```python
browser_network_requests()
```

### Step 4: Structure Tab Data

Organize captured data into JSON for comparison:

```json
[
    {
        "tab_index": 0,
        "url": "https://example.com/checkout",
        "snapshot": "tab1-snapshot.md",
        "screenshot": "tab1-screenshot.png",
        "data": {
            "title": "Checkout - Example",
            "headingCount": 5,
            "productPrice": "$49.99"
        },
        "timestamp": "2025-12-20T10:30:00Z"
    },
    {
        "tab_index": 1,
        "url": "https://staging.example.com/checkout",
        "snapshot": "tab2-snapshot.md",
        "screenshot": "tab2-screenshot.png",
        "data": {
            "title": "Checkout - Staging",
            "headingCount": 6,
            "productPrice": "$49.99"
        },
        "timestamp": "2025-12-20T10:30:15Z"
    }
]
```

Save to `tab-data.json`.

### Step 5: Compare Results

**Option A: Use comparison script**

```bash
python scripts/compare_tabs.py tab-data.json
```

Outputs:
- Text summary of differences
- JSON comparison file

**Option B: Manual comparison**

Compare key metrics:
- Element counts (headings, buttons, forms)
- Extracted data values (prices, CTA text)
- Visual appearance (review screenshots side-by-side)
- Network patterns (request counts, API endpoints)

### Step 6: Generate Report

Create HTML report with side-by-side comparison:

```bash
python scripts/generate_comparison_report.py tab-data.json comparison-report.html
```

Open `comparison-report.html` in browser to view:
- Screenshots side-by-side
- Extracted data comparison
- Element count statistics

## Comparison Strategies

Choose strategy based on what you're testing:

**Visual Comparison** - Screenshots for design consistency
**Content Comparison** - Snapshots for structure/content parity
**Behavioral Comparison** - Network requests for functionality testing
**Performance Comparison** - Network timing for optimization
**Data Extraction Comparison** - Evaluate for structured data validation

See [references/comparison-strategies.md](references/comparison-strategies.md) for detailed guidance.

## Example: Staging vs Production

```python
# 1. Setup tabs
browser_tabs(action="list")  # Check existing
browser_tabs(action="new")   # Create second tab

# 2. Navigate tabs
browser_tabs(action="select", index=0)
browser_navigate(url="https://example.com/products")

browser_tabs(action="select", index=1)
browser_navigate(url="https://staging.example.com/products")

# 3. Collect data from both tabs
tabs_data = []

for i in [0, 1]:
    browser_tabs(action="select", index=i)

    # Snapshot
    browser_snapshot(filename=f"tab{i}-snapshot.md")

    # Screenshot
    browser_take_screenshot(filename=f"tab{i}-screenshot.png", fullPage=True)

    # Extract data
    result = browser_evaluate(function="""
    () => ({
        url: window.location.href,
        productCount: document.querySelectorAll('.product-card').length,
        categories: Array.from(document.querySelectorAll('.category')).map(c => c.textContent)
    })
    """)

    tabs_data.append({
        "tab_index": i,
        "snapshot": f"tab{i}-snapshot.md",
        "screenshot": f"tab{i}-screenshot.png",
        "data": result
    })

# Save for comparison
import json
with open('tab-data.json', 'w') as f:
    json.dump(tabs_data, f, indent=2)

# 4. Generate report
# Run: python scripts/generate_comparison_report.py tab-data.json report.html
```

## Resources

### scripts/

**compare_tabs.py** - Analyzes tab data and generates comparison summary
- Input: `tab-data.json` (structured tab data)
- Output: Text summary + JSON comparison file
- Compares element counts, identifies differences

**generate_comparison_report.py** - Creates HTML visual comparison report
- Input: `tab-data.json` + `assets/report-template.html`
- Output: HTML file with side-by-side screenshots and data
- Embeds screenshots as base64

### references/

**mcp-playwright-tools.md** - Quick reference for Playwright MCP tools used in this workflow (browser_tabs, browser_navigate, browser_snapshot, browser_evaluate, browser_take_screenshot)

**comparison-strategies.md** - Detailed guide for choosing comparison approach (visual, content, behavioral, performance, data extraction, hybrid)

### assets/

**report-template.html** - HTML template for comparison reports with responsive grid layout and embedded styling

## Expected Outcomes

**Successful comparison:**
- Multiple tabs opened and navigated
- Data captured from each tab (snapshots, screenshots, extracted data)
- Differences identified and documented
- HTML report generated showing side-by-side comparison

**Common differences to identify:**
- Element count variations
- Content changes (text, prices, CTAs)
- Visual appearance differences
- Network request patterns
- Performance metrics

## Requirements

**Tools:**
- Playwright MCP browser automation
- Python 3.x for scripts
- Browser with tab support

**Data structure:**
- tab-data.json with consistent schema
- Screenshots saved to accessible paths
- Snapshots saved as markdown files

## Red Flags to Avoid

- Opening too many tabs (>5) without cleanup
- Not waiting for page load before capturing data
- Inconsistent viewport sizes across tabs (affects visual comparison)
- Not saving tab data before closing tabs
- Forgetting to switch tabs before navigation/capture
- Comparing pages in different states (e.g., logged in vs logged out)
- Not handling dynamic content (timers, ads, animations)

## Notes

- Tab indices are 0-based (first tab = 0)
- Always select tab before performing actions on it
- Screenshots capture current viewport unless fullPage=True
- Snapshots provide accessibility tree (better for content analysis)
- Evaluate runs JavaScript in tab context (has access to document/window)
- Network requests captured from page load onwards
- Reports embed screenshots as base64 (no external dependencies)
