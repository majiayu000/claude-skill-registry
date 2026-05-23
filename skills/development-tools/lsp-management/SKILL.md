---
name: lsp-management
description: LSP server recommendations, .lsp.json configuration, installation guides, and troubleshooting for Language Server Protocol in Claude Code
allowed-tools: Read, Glob, Grep, Skill
user-invocable: false
---

# LSP Management Skill

> ## 🚨 MANDATORY: Invoke docs-management First
>
> **STOP - Before providing ANY response about LSP configuration:**
>
> 1. **INVOKE** `docs-management` skill for Claude Code LSP documentation
> 2. **QUERY** for the user's specific LSP topic
> 3. **BASE** all responses on official documentation + this skill's knowledge base
>
> **Skipping this step results in outdated or incorrect information.**

## ⚠️ EXPERIMENTAL: Claude Code LSP Status

**LSP support in Claude Code is experimental and has known issues.** Key points:

| Requirement | Details |
|-------------|---------|
| **Environment Variable** | `ENABLE_LSP_TOOL=1` (singular) required to expose LSP tool |
| **Current Version** | v2.1.0+ has partial support (regression #17468) |
| **Stable Version** | v2.0.67 is last known stable LSP version |
| **Configuration** | `.lsp.json` at project root or `lspServers` in plugin.json |

**See [troubleshooting.md](references/troubleshooting.md) for version-specific issues and workarounds.**

## Overview

Central authority for Language Server Protocol (LSP) configuration in Claude Code. This skill provides:

- **LSP server recommendations** by language/technology
- **Configuration patterns** for `.lsp.json` files
- **Installation guides** for each recommended server
- **Troubleshooting** for common LSP issues

**Architecture:** Keyword registry + curated knowledge base. Delegates to docs-management for official Claude Code LSP documentation.

## When to Use This Skill

**Keywords:** LSP, language server, language-server-protocol, code intelligence, hover, go-to-definition, find-references, diagnostics, pyright, typescript-language-server, gopls, rust-analyzer, csharp-ls, .lsp.json, LSP configuration, LSP setup, LSP troubleshooting

**Use this skill when:**

- Setting up LSP servers for a project
- Choosing between LSP server options for a language
- Configuring `.lsp.json` files
- Troubleshooting LSP issues (hover not working, diagnostics missing, etc.)
- Understanding LSP server installation requirements
- Auto-detecting needed LSPs based on project file types

## Keyword Registry for docs-management Queries

Use these keywords when querying docs-management skill for official documentation:

### Core Concepts

| Topic | Keywords |
| --- | --- |
| LSP Overview | "LSP", "language server protocol", "code intelligence" |
| Configuration File | ".lsp.json", "LSP configuration", "language server config" |
| Features | "hover", "go-to-definition", "find-references", "diagnostics", "document symbols" |

### Server-Specific

| Topic | Keywords |
| --- | --- |
| Python | "pyright", "pylsp", "python language server" |
| TypeScript/JavaScript | "typescript-language-server", "vtsls", "tsserver" |
| Go | "gopls", "go language server" |
| Rust | "rust-analyzer", "rust language server" |
| C# | "csharp-ls", "OmniSharp", "C# language server" |
| C/C++ | "clangd", "ccls", "C++ language server" |

### Troubleshooting

| Topic | Keywords |
| --- | --- |
| Server Issues | "LSP not working", "language server crash", "LSP restart" |
| Feature Issues | "hover not working", "diagnostics missing", "go-to-definition failing" |
| Configuration Issues | "LSP config invalid", ".lsp.json error", "extension mapping" |

## Quick Decision Tree

**What do you need?**

1. **Set up LSP for a new project** → See [server-database.md](references/server-database.md) for recommended servers
2. **Configure .lsp.json** → See [configuration-patterns.md](references/configuration-patterns.md) for patterns
3. **Install a specific LSP server** → See [installation-guide.md](references/installation-guide.md) for per-server commands
4. **Fix LSP issues** → See [troubleshooting.md](references/troubleshooting.md) for common problems
5. **Understand Claude Code LSP support** → Query docs-management: "LSP configuration Claude Code"

## LSP Server Recommendations (Quick Reference)

| Language | Recommended Server | Why |
| --- | --- | --- |
| Python | Pyright | Fast, accurate type checking, broad ecosystem support |
| TypeScript/JavaScript | typescript-language-server | Official TypeScript support, widely used |
| Go | gopls | Official Go team server, comprehensive |
| Rust | rust-analyzer | De facto standard, excellent performance |
| C# | csharp-ls | Lightweight, cross-platform, dotnet tool |
| C/C++ | clangd | LLVM-backed, fast, accurate |
| Java | Eclipse JDTLS | Full-featured, widely supported |
| Ruby | solargraph | Type inference, documentation support |
| PHP | intelephense | Premium features, fast |
| Lua | lua-language-server | Official, well-maintained |
| YAML | yaml-language-server | Schema validation, completion |
| JSON | vscode-json-languageserver | Schema validation, formatting |

For detailed recommendations with alternatives and trade-offs, see [server-database.md](references/server-database.md).

## .lsp.json Configuration Format

Claude Code reads LSP configuration from `.lsp.json` in the project root.

**Basic Structure:**

```json
{
  "server-name": {
    "command": "server-executable",
    "args": ["--stdio"],
    "extensionToLanguage": {
      ".ext": "language-id"
    },
    "restartOnCrash": true,
    "maxRestarts": 3
  }
}
```

**Required Fields:**

| Field | Type | Description |
| --- | --- | --- |
| `command` | string | Executable command for the server |
| `args` | string[] | Command-line arguments (typically `["--stdio"]`) |
| `extensionToLanguage` | object | Maps file extensions to language IDs |

**Optional Fields:**

| Field | Type | Default | Description |
| --- | --- | --- | --- |
| `restartOnCrash` | boolean | `true` | Auto-restart server on crash |
| `maxRestarts` | number | `3` | Maximum restart attempts |

For complete patterns and examples, see [configuration-patterns.md](references/configuration-patterns.md).

## Auto-Detection Strategy

When auto-detecting needed LSPs for a project:

1. **Scan for file extensions** using Glob patterns
2. **Match extensions to languages** using the mapping table below
3. **Recommend servers** from server-database.md

### Extension to Language Mapping

| Extensions | Language | Recommended Server |
| --- | --- | --- |
| `.py`, `.pyi` | Python | pyright |
| `.ts`, `.tsx`, `.js`, `.jsx` | TypeScript/JavaScript | typescript-language-server |
| `.go` | Go | gopls |
| `.rs` | Rust | rust-analyzer |
| `.cs`, `.csx` | C# | csharp-ls |
| `.c`, `.h`, `.cpp`, `.hpp`, `.cc` | C/C++ | clangd |
| `.java` | Java | jdtls |
| `.rb` | Ruby | solargraph |
| `.php` | PHP | intelephense |
| `.lua` | Lua | lua-language-server |
| `.yaml`, `.yml` | YAML | yaml-language-server |
| `.json` | JSON | vscode-json-languageserver |

## Integration with Existing Infrastructure

### Relationship to audit-lsp

The `audit-lsp` command validates existing `.lsp.json` configurations. This skill provides:

- Server recommendations that audit-lsp can validate against
- Configuration patterns that audit-lsp checks for compliance
- Troubleshooting guidance when audit-lsp finds issues

### Relationship to setup-lsp

The `setup-lsp` command creates/updates `.lsp.json` configurations. This skill provides:

- Server database for recommendations
- Installation guides for chosen servers
- Configuration templates for generation

## Test Scenarios

These scenarios should activate this skill:

1. **Direct activation**: "Use the lsp-management skill to recommend a Python LSP"
2. **Setup question**: "How do I set up LSP for my TypeScript project?"
3. **Configuration question**: "What should my .lsp.json look like for Go?"
4. **Troubleshooting**: "My hover tooltips aren't working in Python files"
5. **Comparison**: "Should I use pyright or pylsp for Python?"

## Related Skills

| Skill | Relationship |
| --- | --- |
| **docs-management** | Delegates to for official Claude Code LSP documentation |
| **plugin-development** | Plugins can provide LSP configurations via `lspServers` field |

## References

**Detailed guides (load on-demand):**

- [Server Database](references/server-database.md) - Curated recommendations by language
- [Configuration Patterns](references/configuration-patterns.md) - Common .lsp.json patterns
- [Installation Guide](references/installation-guide.md) - Per-server installation commands
- [Troubleshooting](references/troubleshooting.md) - Common issues and fixes

**Official Documentation (via docs-management):**

- Query: "LSP configuration Claude Code"
- Query: ".lsp.json format"

## Version History

- **v1.0.0** (2026-01-11): Initial release
  - LSP server recommendations for 12+ languages
  - Configuration pattern documentation
  - Installation guides per server
  - Troubleshooting guide
  - Integration with audit-lsp and setup-lsp

---

## Last Updated

**Date:** 2026-01-11
**Model:** claude-opus-4-5-20251101
