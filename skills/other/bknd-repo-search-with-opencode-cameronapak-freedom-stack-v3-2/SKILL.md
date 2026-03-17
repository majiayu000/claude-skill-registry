---
name: bknd-repo-search-with-opencode
description: Use when querying the bknd source repository with btca CLI. Covers setup, configuration, and query patterns for learning bknd internals including data module, authentication, media handling, and adapter configuration.
compatibility: Requires bun or npm, btca, opencode-ai, and access to the internet
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
