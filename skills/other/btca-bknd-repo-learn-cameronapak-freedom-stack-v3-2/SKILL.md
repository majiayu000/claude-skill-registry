---
name: btca-bknd-repo-learn
description: Use btca (Better Context App) to efficiently query and learn from the bknd backend framework. Use when working with bknd for (1) Understanding data module and schema definitions, (2) Implementing authentication and authorization, (3) Setting up media file handling, (4) Configuring adapters (Node, Cloudflare, etc.), (5) Learning from bknd source code and examples, (6) Debugging bknd-specific issues
---

# Query bknd with btca

btca is a CLI tool for asking questions about git repos. It clones repositories, indexes them, and answers queries using AI.

## Quick Setup

```bash
# Install btca and OpenCode
bun add -g btca opencode-ai

# Configure model (Big Pickle: free, fast, surprisingly good)
btca config model --provider opencode --model big-pickle

# Add bknd as a resource
btca config resources add --name bknd --type git --url https://github.com/bknd-io/bknd --branch main
```

Or create `btca.config.jsonc`:
```jsonc
{
  "$schema": "https://btca.dev/btca.schema.json",
  "model": "big-pickle",
  "provider": "opencode",
  "providerTimeoutMs": 300000,
  "resources": [
    {
      "type": "git",
      "name": "bknd",
      "url": "https://github.com/bknd-io/bknd",
      "branch": "main"
    }
  ]
}
```

## Core Commands

### Ask a question
```bash
btca ask --resource bknd --question "How do I define a schema?"
```

### Interactive chat
```bash
btca chat --resource bknd
```

### Launch TUI
```bash
btca
```

## Reference Files

For detailed information, see:

- **[setup.md](references/setup.md)** - Full installation, configuration options, resource management, troubleshooting setup issues
- **[query-patterns.md](references/query-patterns.md)** - Specific query patterns for data, auth, media, adapters, and framework integration
- **[advanced.md](references/advanced.md)** - Multi-resource queries, interactive workflows, performance optimization, debugging

## Query Best Practices

1. **Be specific** - "How do I define a schema with a one-to-many relation?" vs "How do I use the data module?"
2. **Provide context** - "I'm using Cloudflare Workers. How do I configure the database adapter?"
3. **Ask for examples** - "Show me a complete example of setting up password authentication"
4. **Reference specific files** - "How does src/App.ts initialize the modules?"

## Learning Workflow

1. **Explore high-level**: Ask about overall architecture and main modules
2. **Module deep-dive**: Use `btca chat --resource bknd` to focus on one module
3. **Implementation details**: Ask to see specific feature implementations
4. **Examples & patterns**: Query the examples directory for best practices

## Resources

- btca docs: https://btca.dev
- bknd docs: https://docs.bknd.io
- bknd repo: https://github.com/bknd-io/bknd
