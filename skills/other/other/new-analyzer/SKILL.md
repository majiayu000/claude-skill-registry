---
name: new-analyzer
description: Guide for adding a new AI coding agent analyzer to Splitrail. Use when implementing support for a new tool like Copilot, Cline, or similar.
---

# Adding a New Analyzer

Splitrail tracks token usage from AI coding agents. Each agent has its own "analyzer" that discovers and parses its data files.

## Checklist

1. Add variant to `Application` enum in `src/types.rs`
2. Create `src/analyzers/{agent_name}.rs` implementing `Analyzer` trait from `src/analyzer.rs`
3. Export in `src/analyzers/mod.rs`
4. Register in `src/main.rs`
5. Add tests in `src/analyzers/tests/{agent_name}.rs`, export in `src/analyzers/tests/mod.rs`
6. Update README.md
7. (Optional) Add model pricing to `src/models.rs` if agent doesn't provide cost data

Test fixtures go in `src/analyzers/tests/source_data/`. See `src/types.rs` for message and stats types.

## VS Code Extensions

Use `discover_vscode_extension_sources()` and `get_vscode_extension_tasks_dirs()` helpers from `src/analyzer.rs`.

## Reference Analyzers

- **Simple JSONL CLI**: `src/analyzers/pi_agent.rs`, `src/analyzers/piebald.rs`
- **VS Code extension**: `src/analyzers/cline.rs`, `src/analyzers/roo_code.rs`
- **Complex with dedup**: `src/analyzers/claude_code.rs`
- **External data dirs**: `src/analyzers/opencode.rs`
