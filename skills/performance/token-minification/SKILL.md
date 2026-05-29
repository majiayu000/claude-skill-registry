---
name: token minifier
user-invocable: true
---

Refactor the selected file(s) to minimize token usage using **Conditional Flow-Style** formatting. Follow these strict rules:

### 1. JSON & Code Block Formatting (Conditional Flow-Style)
Apply "Flow Style" to `json` code blocks and generic arrays/objects:
- **Heuristic**: Detect short arrays `[...]` or objects `{...}` that are currently expanded vertically.
- **Action**: Inline them into a single row ("Flow Style") **IF AND ONLY IF** the resulting line is **≤ 140 characters**.
- **Visual Goal**: Bin-pack items to save vertical space without sacrificing readability.
  - *Example*: `"tags": [ "unicorn", "cat", "optimization" ]`
- **Fallback**: If the structure exceeds 140 characters, retain the vertical "Block Style".

### 2. Markdown Compaction
- **Whitespace**: Collapse 3+ consecutive newlines into 2 (standardize paragraph breaks).
- **Comments**: Delete all HTML comments ``.
- **Lists**: Enforce tight lists (no blank lines between items) unless the item contains a block element.

### 3. Safety & Constraints
- **Preservation**: Do NOT modify the internal formatting of non-JSON code blocks (e.g., Python, Bash) unless strictly trimming trailing whitespace.
- **Content**: Do not summarize text or remove valid documentation; focus purely on syntactic density.
