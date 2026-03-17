---
name: research-library-stats
description: Show statistics about the product research evidence library
user-invocable: true
---

You are helping the user understand the current state of the product research evidence library.

**IMPORTANT: Before doing anything else**, use the ToolSearch tool with query `+product-research` to load the product-research MCP tools. All tools below are prefixed with `mcp__product-research__` (e.g., `mcp__product-research__get_library_stats`).

Follow these steps:

### Step 1: Query Library Statistics

Use `mcp__product-research__get_library_stats` to retrieve current library metrics.

### Step 2: Present Overview

Display library statistics:

**Library Overview:**
- Total evidence entries
- Total ingredients covered
- Total clinical trials indexed
- Last updated date

**Evidence by Type:**
- Meta-analyses and systematic reviews
- Randomized controlled trials (RCTs)
- Controlled studies
- Observational studies
- Case reports and other

**Coverage by Category:**
- Amino acids and proteins
- Vitamins and minerals
- Herbal extracts and botanicals
- Performance and ergogenic aids
- Other categories

### Step 3: Coverage Assessment

Highlight:
- **Well-covered ingredients** — ingredients with strong evidence depth
- **Gaps** — ingredients or categories with limited coverage
- **Recent additions** — newly added evidence

### Step 4: Follow-Up Actions

Offer:
- Search for a specific ingredient (`/jf-product-intelligence:research-ingredient`)
- Browse clinical trials (`/jf-product-intelligence:clinical-trials`)
- Check if a specific ingredient has evidence in the library

### Error Handling

- If MCP tools are unavailable, inform the user that the product-research server may need reconnection
- If statistics are not available, note the limitation
