---
name: shopify-dev-mcp
description: Use Shopify Dev MCP tools for Liquid/theme work (call learn_shopify_api first, validate theme after edits).
---

When working on Shopify themes or Liquid:

1) If Shopify Dev MCP tools are available, ALWAYS call `learn_shopify_api` first.
   - Do NOT attempt to run it as a shell command; it is an MCP tool.
2) Prefer MCP doc tools when unsure:
   - `search_docs_chunks` for broad search
   - `fetch_full_docs` for full pages / deeper context
3) For theme changes:
   - Use theme validation tools (prefer full-theme validation).
   - After edits, validate the theme and fix issues before continuing.
4) Keep changes minimal, Dawn-compatible, and avoid guessing Liquid objects/filters.
