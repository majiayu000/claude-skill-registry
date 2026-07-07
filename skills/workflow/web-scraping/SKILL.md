---
name: web-scraping
description: |
  Extract structured data from websites, scrape page content, and collect information across multiple pages.
  Trigger when the user asks to: extract data from a website, scrape a page, collect information from URLs,
  pull content from web pages, gather data across multiple pages, or download page content.
allowed-tools: Bash(openbrowser-ai:*) Bash(curl:*) Bash(uv:*) Bash(irm:*) Read Write
---

# Web Scraping

Extract structured data from websites using Python code execution with browser automation functions. Handles JavaScript-rendered content, pagination, and multi-page scraping.

All code runs via `openbrowser-ai -c`. The daemon starts automatically and persists variables across calls. All browser functions are async -- use `await`.

The CLI daemon also persists cookies and login state in `~/.config/openbrowser/profiles/daemon/storage_state.json`, so authenticated sessions can be reused across later runs.

## Setup

Before running, verify openbrowser-ai is installed:

```bash
openbrowser-ai --help
```

If not found, install:

```bash
# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/billy-enrizky/openbrowser-ai/main/install.sh | sh

# Windows (PowerShell)
irm https://raw.githubusercontent.com/billy-enrizky/openbrowser-ai/main/install.ps1 | iex
```

## Workflow

### Step 1 -- Navigate and get content overview

```bash
openbrowser-ai -c - <<'EOF'
await navigate("https://example.com/data")

# Get browser state to see page title, URL, element count
state = await browser.get_browser_state_summary()
print(f"Title: {state.title}")
print(f"URL: {state.url}")
print(f"Elements: {len(state.dom_state.selector_map)}")
EOF
```

### Step 2 -- Extract data with JavaScript

Use `evaluate()` to run JS in the browser and return structured data directly as Python objects:

```bash
openbrowser-ai -c - <<'EOF'
data = await evaluate("""
(function(){
  return Array.from(document.querySelectorAll(".product-card")).map(el => ({
    name: el.querySelector(".title")?.textContent?.trim(),
    price: el.querySelector(".price")?.textContent?.trim(),
    url: el.querySelector("a")?.href
  }))
})()
""")

import json
print(json.dumps(data, indent=2))
EOF
```

### Step 3 -- Process data with Python

Use pandas, regex, or other Python tools to clean and transform extracted data:

```bash
openbrowser-ai -c - <<'EOF'
import json

# Filter and transform
filtered = [item for item in data if item.get("price")]
for item in filtered:
    # Extract numeric price
    price_str = item["price"].replace("$", "").replace(",", "")
    item["price_float"] = float(price_str)

# Sort by price
filtered.sort(key=lambda x: x["price_float"])
print(json.dumps(filtered, indent=2))
EOF
```

Or with pandas if available:

```bash
openbrowser-ai -c - <<'EOF'
import pandas as pd
df = pd.DataFrame(data)
print(df.to_string())
EOF
```

### Step 4 -- Handle pagination

```bash
openbrowser-ai -c - <<'EOF'
results = []
page = 1

while True:
    # Extract data from current page
    page_data = await evaluate("""
    (function(){
      return Array.from(document.querySelectorAll(".item")).map(el => ({
        name: el.textContent.trim()
      }))
    })()
    """)
    results.extend(page_data)
    print(f"Page {page}: {len(page_data)} items")

    # Check for next button
    has_next = await evaluate("""
    (function(){ return !!document.querySelector(".pagination .next:not(.disabled)") })()
    """)

    if not has_next:
        break

    # Replace with the actual index from browser.get_browser_state_summary()
    await click(next_button_index)
    await wait(2)
    page += 1

print(f"Total: {len(results)} items")
EOF
```

### Step 5 -- Handle infinite scroll

```bash
openbrowser-ai -c - <<'EOF'
results = []
prev_count = 0

for _ in range(20):  # Max 20 scroll attempts
    # Get current items
    count = await evaluate("""
    (function(){ return document.querySelectorAll(".item").length })()
    """)

    if count == prev_count:
        break  # No new content loaded

    prev_count = count
    await scroll(down=True, pages=3)
    await wait(1)

# Now extract all loaded items
results = await evaluate("""
(function(){
  return Array.from(document.querySelectorAll(".item")).map(el => ({
    text: el.textContent.trim()
  }))
})()
""")
print(f"Extracted {len(results)} items")
EOF
```

### Step 6 -- Multi-page scraping

```bash
openbrowser-ai -c - <<'EOF'
urls = [
    "https://example.com/page-1",
    "https://example.com/page-2",
    "https://example.com/page-3",
]

all_data = []
for url in urls:
    await navigate(url)
    await wait(1)

    page_data = await evaluate("""
    (function(){
      return document.querySelector("h1")?.textContent?.trim()
    })()
    """)
    all_data.append({"url": url, "title": page_data})
    print(f"{url}: {page_data}")

import json
print(json.dumps(all_data, indent=2))
EOF
```

## Tips

- Code is piped via stdin using heredoc (`-c - <<'EOF'`), so all Python syntax works without shell escaping issues.
- Use `evaluate()` for structured DOM extraction -- it returns Python objects directly.
- Use Python for post-processing: filtering, sorting, deduplication, format conversion.
- For large datasets, process pages incrementally rather than loading everything into memory.
- Check for rate limiting; add `await wait(2)` between page loads if needed.
- Variables persist between `-c` calls while the daemon is running, so you can build up results across multiple calls.

## Cleanup

This step is **mandatory**. Run it after the scrape finishes, whether you collected every page or hit a rate limit halfway through. Without it, the daemon keeps Chrome running until its 10-minute idle timeout, leaving a stale browser process, a locked profile, and (on macOS/Linux desktop) a visible window.

Stop the daemon, then verify it is gone:

```bash
openbrowser-ai daemon stop
openbrowser-ai daemon status
```

`daemon stop` closes every tab, exits Chrome, flushes saved cookies/login state to the profile, and shuts down the daemon process. `daemon status` should report the daemon is not running. If it still reports running, the daemon is wedged, force-kill it:

```bash
pkill -f 'openbrowser.*daemon' || true
```

Long scrapes fail often (rate limits, network drops, pagination dead-ends). Guarantee cleanup with a shell trap so a partial run never leaks a browser:

```bash
trap 'openbrowser-ai daemon stop >/dev/null 2>&1 || true' EXIT
# ... openbrowser-ai -c calls here ...
```

Persist scraped data to disk *before* calling `daemon stop`, in-memory variables die with the daemon. Do not rely on the idle timeout. Do not call `done()` as a substitute, `done()` only marks the task complete inside the agent loop, it does not close the browser.
