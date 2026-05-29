---
name: ai-rules-adapter-builder
description: Add rules or skills adapters for a new AI tool and wire config, CLI, completion, and tests.
---

# AI Rules Adapter Builder

## Instructions
1. Confirm adapter mode, defaultSourceDir, targetDir, and suffix strategy based on existing adapters
2. Add adapter files and register them in the adapter registry
3. Extend ProjectConfig and sourceDir resolution to cover the new tool
4. Wire CLI subcommands and _complete types
5. Update shell completion scripts
6. Add or update adapter tests

## Examples
Request: Add rules and skills for a new tool and sync to its project directories
Result: Adapters, config support, CLI, completion, and tests all green
