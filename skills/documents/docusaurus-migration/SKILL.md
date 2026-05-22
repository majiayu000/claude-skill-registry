---
name: docusaurus-v2-to-v3-migration
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when migrating Docusaurus projects from v2 to v3
---

# Docusaurus V2 To V3 Migration

## Quick Start

```json
{
  "@docusaurus/core": "^3.0.0",
  "@mdx-js/react": "^3.0.0",
  "prism-react-renderer": "^2.1.0",
  "react": "^18.2.0"
}
```

## Core Principles

- **MDX v1 → v3**: Main challenge - escape `{` and `<` characters or wrap in code blocks
- **Node.js >=18.0**: Required for Docusaurus v3
- **React 18**: Breaking changes may affect custom components

## Migration Steps

1. **Pre-check**: Run `npx docusaurus-mdx-checker` to identify MDX issues
2. **Update deps**: Upgrade all @docusaurus packages, React, MDX, prism-react-renderer
3. **Fix MDX**: Escape bare `{` `<` characters, convert GFM autolinks, use code fences
4. **Update config**: Replace `@tsconfig/docusaurus` with `@docusaurus/tsconfig`, update Prism imports
5. **Test**: Run `npm start` then `npm run build`

## Reference Files

- [breaking-changes.md](references/breaking-changes.md) - Complete migration guide with examples

<!--
PROGRESSIVE DISCLOSURE GUIDELINES:
- Keep this file ~50 lines total (max ~150 lines)
- Use 1-2 code blocks only (recommend 1)
- Keep description <200 chars for Level 1 efficiency
- Move detailed docs to references/ for Level 3 loading
- This is Level 2 - quick reference ONLY, not a manual

LLM WORKFLOW (when editing this file):
1. Write/edit SKILL.md
2. Format (if formatter available)
3. Run: claude-skills-cli validate <path>
4. If multi-line description warning: run claude-skills-cli doctor <path>
5. Validate again to confirm
-->
