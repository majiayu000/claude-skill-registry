---
name: code-sandbox
description: Execute JavaScript code in a sandboxed VM for data processing and computation
---

## Code Sandbox

You have sandboxed JavaScript execution tools for computation and data processing:

**Full scripts:**
- `execute_js` — run JavaScript code in an isolated V8 sandbox
  - Pass data via the `input` parameter (JSON) — access it as `INPUT` in your code
  - Use `console.log()` to capture intermediate values (returned in `logs` array)
  - Available globals: `JSON`, `Math`, `Date`, `Array`, `Object`, `String`, `Number`, `RegExp`, `Map`, `Set`, `parseInt`, `parseFloat`, `isNaN`, `isFinite`, `encodeURIComponent`, `decodeURIComponent`, `atob`, `btoa`
  - No network access, no filesystem, no imports — pure computation only
  - Default timeout 5 seconds, max 30 seconds
  - 10MB output limit

**Quick expressions:**
- `eval_expression` — evaluate a single JavaScript expression and return the result
  - Use for quick math: `"15 * 4500 * 0.01"` → `675`
  - Date calculations: `"new Date().toISOString()"`
  - Array operations: `"[1,2,3].map(x => x*x)"` → `[1, 4, 9]`

**Best practices:**
- Use `execute_js` for multi-step data processing, algorithm testing, code validation
- Use `eval_expression` for quick math, string ops, date calculations
- Pass large datasets via `input` parameter rather than embedding in code
- Combine with `parse_csv` (structured-data skill) for CSV → transform → output workflows
- Combine with `store_deliverable` to save computed results as job evidence
