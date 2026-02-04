---
name: lsp
description: >
  Code navigation with LSP. When user says "find references", "go to definition",
  "where defined", "show type", "list symbols", "what uses", or "who calls" -
  use native LSP tools if available, otherwise fall back to specweave lsp commands.
user-invocable: false
---

# LSP Code Intelligence

Semantic code navigation and analysis.

## Current Status (v2.1.0+)

**⚠️ Native LSP is BROKEN** in Claude Code v2.1.0+ ([Issue #17468](https://github.com/anthropics/claude-code/issues/17468))

| Version | Native LSP | SpecWeave CLI |
|---------|------------|---------------|
| ≤2.0.76 | ✅ Works | ✅ Works |
| ≥2.1.0 | ❌ Broken | ✅ Works |

**Always use SpecWeave CLI** until native LSP is fixed.

## SpecWeave LSP CLI (Always Works)

```bash
# Find all references to a symbol (SEMANTIC, not grep!)
specweave lsp refs <file> <symbol>

# Go to definition
specweave lsp def <file> <symbol>

# Get type information (hover)
specweave lsp hover <file> <symbol>

# List all symbols in a file
specweave lsp symbols <file>

# Search workspace for symbols
specweave lsp search <query>
```

## File Path Required

If user doesn't specify a file path, find it first:

```bash
# Step 1: Find which file(s) contain the symbol
grep -rn --include="*.ts" "function symbolName\|class symbolName" .

# Step 2: Then use LSP on the found file
specweave lsp refs <found-file> <symbol>
```

## Why Use SpecWeave CLI over Grep

| Aspect | Grep | SpecWeave LSP |
|--------|------|---------------|
| Type | Text matching | Semantic analysis |
| Results | Includes comments, strings, docs | Actual code usages only |
| Speed | Fast | 52x faster than grep |
| Accuracy | Many false positives | Zero false positives |

**⚠️ Never use Grep for "find references"** - Grep finds TEXT matches (including comments, strings, docs). LSP finds SEMANTIC references (actual code usages only).

## Workarounds for Native LSP

If you need native LSP tools:

```bash
# Option 1: Use older Claude Code version
ENABLE_LSP_TOOL=1 npx @anthropic-ai/claude-code@2.0.76

# Option 2: Use tweakcc patch
npx tweakcc --apply
```

## Multi-Repo LSP Setup (v1.0.203+)

For umbrella projects with multiple repositories, use the interactive setup:

```bash
# Scan project and install LSP plugins interactively
specweave lsp setup

# Options:
specweave lsp setup --max 5       # Limit to top 5 languages
specweave lsp setup --min-files 10  # Min files to consider a language
specweave lsp setup --scope project # Install to .claude/settings.json
specweave lsp setup --dry-run       # Show what would be installed
```

### What Setup Does

1. **Scans all repos** - Finds languages in `repositories/`, `packages/`, `services/`, etc.
2. **Ranks by file count** - Shows top languages with file counts
3. **Shows implications** - Restart required, startup time impact
4. **Prompts for approval** - User selects which plugins to install
5. **Installs plugins** - Uses `claude plugin install` with specified scope

### Scan Coverage

Scans these directories for nested repositories:
- `repositories/` - Multi-repo umbrella pattern
- `packages/` - Monorepo (Lerna, Nx, etc.)
- `services/` - Microservices
- `apps/`, `libs/`, `modules/` - Nx/Turborepo patterns

### Status and Diagnostics

```bash
# Check current LSP status
specweave lsp status

# Shows:
#   - LSP env ready (ENABLE_LSP_TOOL)
#   - Detected languages
#   - Missing servers/plugins
#   - Warm-up state
```

## Supported Languages (10 LSPs)

SpecWeave LSP supports 10 major languages via their respective language servers:

| Language | Server | Install Command |
|----------|--------|-----------------|
| **TypeScript/JavaScript** | tsserver (built-in) | `npm i -g typescript` |
| **Python** | pyright | `npm i -g pyright` or `pip install pyright` |
| **Go** | gopls | `go install golang.org/x/tools/gopls@latest` |
| **Rust** | rust-analyzer | `rustup component add rust-analyzer` |
| **Java** | jdtls | Via VS Code or manual install |
| **C#** | csharp-ls | `dotnet tool install -g csharp-ls` |
| **Kotlin** | kotlin-language-server | Via IntelliJ or manual install |
| **Swift** | sourcekit-lsp | Comes with Xcode/Swift toolchain |
| **PHP** | intelephense | `npm i -g intelephense` |
| **Ruby** | solargraph | `gem install solargraph` |

### Auto-Detection

SpecWeave automatically detects which language servers to use based on project files:

| Language | Detection Files |
|----------|----------------|
| TypeScript | `tsconfig.json`, `package.json` |
| Python | `pyproject.toml`, `requirements.txt`, `setup.py` |
| Go | `go.mod`, `go.sum` |
| Rust | `Cargo.toml` |
| Java | `pom.xml`, `build.gradle` |
| C# | `*.csproj`, `*.sln` |
| Kotlin | `build.gradle.kts`, `*.kt` |
| Swift | `Package.swift`, `*.xcodeproj` |
| PHP | `composer.json` |
| Ruby | `Gemfile`, `*.gemspec` |

## How to Enable LSP in Your Project

### 1. Install the Language Server

```bash
# For Python projects
pip install pyright
# OR
npm install -g pyright

# For Go projects
go install golang.org/x/tools/gopls@latest

# For Rust projects
rustup component add rust-analyzer

# For C# projects
dotnet tool install -g csharp-ls
```

### 2. Run SpecWeave LSP

```bash
# It auto-detects languages!
specweave lsp refs src/file.py MyClass
specweave lsp def src/main.go HandleRequest
specweave lsp hover src/lib.rs calculate
```

### 3. Verify Setup

```bash
specweave lsp status
```

## How SpecWeave CLI Works

Uses language-specific clients:
- **TypeScript**: `TsServerClient` (direct tsserver protocol, fastest)
- **Other languages**: Generic `LSPClient` (JSON-RPC over stdio)

Features:
1. Spawns language server directly
2. Uses native LSP protocol
3. Provides real semantic analysis
4. Works in any environment (CI/CD, Claude Code, scripts)

## Project-Specific Learnings

**Before starting work, check for project-specific learnings:**

```bash
# Check if skill memory exists for this skill
cat .specweave/skill-memories/lsp.md 2>/dev/null || echo "No project learnings yet"
```

Project learnings are automatically captured by the reflection system when corrections or patterns are identified during development. These learnings help you understand project-specific conventions and past decisions.
