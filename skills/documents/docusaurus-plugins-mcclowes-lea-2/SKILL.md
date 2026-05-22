---
name: docusaurus-plugins
# IMPORTANT: Keep description on ONE line for Claude Code compatibility
# prettier-ignore
description: Use when creating Docusaurus plugins (remark, rehype, theme, content, lifecycle) to extend markdown, modify HTML, or add custom functionality
---

# Docusaurus Plugin Guide

## Quick Start

```javascript
// Remark plugin - transforms markdown AST
module.exports = function remarkPlugin(options = {}) {
  return async function transformer(ast, vfile) {
    const { visit } = require('unist-util-visit');

    visit(ast, 'link', (node) => {
      // Transform nodes
      node.data = node.data || {};
      node.data.hProperties = { className: 'custom' };
    });

    return ast;
  };
};

// In docusaurus.config.js:
// remarkPlugins: [require('./plugins/my-plugin')]
```

## Core Principles

- **5 Plugin Types**: Remark (markdown), Rehype (HTML), Lifecycle (routes/webpack), Theme (components), Content (custom data)
- **Remark**: Transforms markdown before HTML conversion, use `unist-util-visit` for AST traversal
- **Rehype**: Transforms HTML after compilation, processes HAST (HTML AST)
- **Lifecycle**: Most flexible, implements hooks like `loadContent()`, `contentLoaded()`, `postBuild()`
- **Export function**: Returns transformer (remark/rehype) or plugin object (lifecycle)

## Reference Files

Detailed guides for each plugin type:

- [references/remark-plugins.md](references/remark-plugins.md) - Markdown transformation
- [references/rehype-plugins.md](references/rehype-plugins.md) - HTML processing
- [references/lifecycle-plugins.md](references/lifecycle-plugins.md) - Routes, webpack, global data
- [references/theme-plugins.md](references/theme-plugins.md) - Themes and swizzling
- [references/content-plugins.md](references/content-plugins.md) - Custom content types
- [references/package-structure.md](references/package-structure.md) - Publishing and config

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
