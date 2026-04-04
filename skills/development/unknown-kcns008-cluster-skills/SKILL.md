# OSGrep - Semantic Code Search

**Purpose**: Provides fast, local, natural-language search over the repository using osgrep CLI for semantic code analysis without requiring MCP servers.

**When to Use**: When you need to find code patterns, understand implementations, locate features, or perform natural-language searches across the codebase.

---

## Overview

OSGrep is a lightweight semantic grep tool that enables natural-language search over codebases. It uses local embeddings to understand code semantically, making it ideal for finding implementations, patterns, and features without exact string matching.

Unlike traditional grep, osgrep understands the meaning of your query and returns semantically relevant results, making it perfect for exploratory code analysis in cluster-code projects.

---

## Installation & Setup

### Initial Installation

```bash
npm install -g osgrep
```

### Model Download (One-Time Setup)

```bash
osgrep setup
```

✅ **GOOD**: Run `osgrep setup` once after installation to download models
⚠️ **NOTE**: This is optional but significantly improves search performance

### Verification

```bash
osgrep doctor    # Verify installation and models
osgrep list      # Show indexed repositories
```

---

## Core Search Patterns

### Basic Natural Language Search

```bash
# Find authentication validation logic
osgrep "how do we validate auth?"

# Locate pagination helpers
osgrep "pagination helper"

# Find error handling patterns
osgrep "error handling"

# Search for feature flags
osgrep "feature flags"
```

✅ **GOOD**: Use natural language queries that describe what you're looking for
❌ **BAD**: Don't use exact string matching patterns like traditional grep

### Machine-Readable JSON Output

```bash
# Get structured JSON output for programmatic processing
osgrep --json "pagination helper"

# Save results to file for analysis
osgrep --json "authentication logic" > /tmp/osgrep-results.json
```

💡 **TIP**: Use `--json` when you need to process results programmatically or integrate with other tools

### Controlling Search Depth

```bash
# Get more results per file (default varies)
osgrep "error handling" --per-file 3

# Get comprehensive results per file
osgrep "kubernetes integration" --per-file 5
```

### Compact Output

```bash
# Show only file paths (no context)
osgrep "feature flags" --compact
```

✅ **GOOD**: Use `--compact` when you just need to know which files contain the pattern
💡 **TIP**: Combine with other tools like `xargs` for batch operations

---

## Index Management

### Keeping Index Fresh

```bash
# Re-index modified files before searching (recommended)
osgrep --sync "recent changes"

# Manual full re-index of the repository
osgrep index
```

⚠️ **IMPORTANT**: Always run from the repository root so auto-store detection works correctly

✅ **BEST PRACTICE**: Use `--sync` before important searches to ensure index is up-to-date
❌ **BAD**: Forgetting to sync after major code changes leads to stale results

### Index Storage

OSGrep stores embeddings in `~/.osgrep/data/<store>` by default.

```bash
# Clean slate - remove all indexed data for current repo
rm -rf ~/.osgrep/data/<store-name>

# Then re-index
osgrep index
```

---

## Hot Daemon (Performance Optimization)

### Starting the Daemon

```bash
# Start background daemon to keep embeddings warm
osgrep serve            # Default port: 4444

# Custom port
osgrep serve --port 5000
```

✅ **GOOD**: Use daemon for repeated searches during active development sessions
💡 **TIP**: The CLI automatically falls back to on-demand mode if daemon isn't running

### When to Use Daemon

- ✅ Active development sessions with frequent searches
- ✅ When working on large refactoring tasks
- ✅ During code review sessions
- ❌ One-off searches (daemon overhead not worth it)
- ❌ CI/CD pipelines (use direct mode)

---

## Cluster-Code Specific Patterns

### Finding Kubernetes Integration Points

```bash
# Locate kubectl client usage
osgrep "kubectl client initialization"

# Find pod management logic
osgrep "how do we manage pods?"

# Locate resource fetching patterns
osgrep "fetching kubernetes resources"
```

### LLM Provider Integration

```bash
# Find LLM provider implementations
osgrep "LLM provider registration"

# Locate streaming response handlers
osgrep "streaming LLM responses"
```

### Plugin System

```bash
# Find plugin registration logic
osgrep "plugin registration and lifecycle"

# Locate hook implementations
osgrep "command hooks implementation"
```

### Error Handling & Logging

```bash
# Find error handling patterns
osgrep "error handling and recovery"

# Locate logging implementations
osgrep "structured logging patterns"
```

---

## Integration with Claude Code Workflow

### Exploratory Code Analysis

When exploring unfamiliar parts of cluster-code:

```bash
# 1. Get overview of a feature area
osgrep "authentication middleware" --per-file 2

# 2. Dive deeper into specific files
osgrep "JWT token validation" --per-file 5

# 3. Export for detailed analysis
osgrep --json "auth implementation" > /tmp/auth-analysis.json
```

### Refactoring Support

```bash
# 1. Find all usages of a pattern before refactoring
osgrep "deprecated API calls" --json

# 2. Identify files needing updates
osgrep "old configuration pattern" --compact

# 3. Verify refactoring completeness
osgrep "old pattern that should be gone"  # Should return no results
```

### Code Review Assistance

```bash
# Find similar implementations for consistency
osgrep "similar validation logic"

# Locate test coverage patterns
osgrep "test cases for error handling"

# Check for security patterns
osgrep "input sanitization"
```

---

## Best Practices

### ✅ DO

- **Run from repo root**: Ensures auto-store detection works correctly
- **Use natural language**: "how do we handle errors?" not "error.*catch"
- **Sync before important searches**: `osgrep --sync "query"` ensures fresh results
- **Use --json for automation**: Enables programmatic processing and integration
- **Start daemon for dev sessions**: Keeps embeddings warm for faster repeated searches
- **Keep queries focused**: Specific queries return more relevant results

### ❌ DON'T

- **Mix with traditional grep syntax**: osgrep uses semantic search, not regex
- **Forget to index**: Run `osgrep index` after cloning or major changes
- **Search from subdirectories**: Always run from repo root
- **Over-rely on cache**: Sync regularly when code changes frequently
- **Use for exact string matching**: Use traditional `grep` or `rg` for that

### ⚠️ WARNINGS

- **Stale Index**: If results seem outdated, run `osgrep --sync "query"` or `osgrep index`
- **Storage Growth**: Index data accumulates in `~/.osgrep/data/` - clean periodically
- **Model Download**: First `osgrep setup` requires internet and downloads ~100MB
- **Port Conflicts**: Default daemon port 4444 may conflict with other services

---

## Common Workflows

### 1. Initial Repository Setup

```bash
cd /home/user/cluster-code
npm install -g osgrep
osgrep setup          # One-time model download
osgrep index          # Index the repository
osgrep serve &        # Optional: start daemon
```

### 2. Daily Development

```bash
# Start of day: ensure fresh index
osgrep --sync "startup checks"

# During development: semantic searches
osgrep "how do we parse command line args?"

# Before commit: verify changes
osgrep --sync "new feature I just added"
```

### 3. Deep Code Investigation

```bash
# Step 1: Broad search
osgrep "authentication flow" --per-file 2 > /tmp/auth-overview.txt

# Step 2: Narrow down
osgrep "JWT token generation" --per-file 5 --json > /tmp/jwt-details.json

# Step 3: Analyze specific files (open in editor)
```

### 4. Troubleshooting

```bash
# Verify installation
osgrep doctor

# Check what's indexed
osgrep list

# Fresh start
rm -rf ~/.osgrep/data/cluster-code
osgrep index
```

---

## Performance Tips

### Optimize Search Speed

1. **Use daemon for repeated searches**: `osgrep serve &`
2. **Limit results**: Use `--per-file 1` for quick overview
3. **Use --compact**: When you only need file paths
4. **Keep index fresh**: Regular `--sync` is faster than full re-index

### Manage Storage

```bash
# Check index size
du -sh ~/.osgrep/data/*

# Clean old repositories
osgrep list
rm -rf ~/.osgrep/data/<unused-repo>
```

---

## Troubleshooting

### Common Issues

**Problem**: `osgrep: command not found`
```bash
# Solution: Install globally
npm install -g osgrep
```

**Problem**: Slow first search
```bash
# Solution: Run setup to download models
osgrep setup
```

**Problem**: Outdated results
```bash
# Solution: Sync or re-index
osgrep --sync "query"
# OR
osgrep index
```

**Problem**: Daemon won't start (port conflict)
```bash
# Solution: Use different port
osgrep serve --port 5000
```

**Problem**: No results for recent code
```bash
# Solution: Ensure running from repo root and re-index
cd /home/user/cluster-code
osgrep index
```

---

## Comparison with Other Tools

### OSGrep vs Traditional Grep

| Feature | osgrep | grep/rg |
|---------|--------|---------|
| Search Type | Semantic (meaning-based) | Literal (string/regex) |
| Query Style | Natural language | Regex patterns |
| Setup | Requires indexing | None |
| Speed (indexed) | Very fast | Fast |
| Best For | Exploratory, conceptual | Exact matches |

✅ **USE OSGREP** when:
- You don't know exact variable/function names
- Exploring unfamiliar code
- Finding conceptually similar code
- Natural language queries work better

✅ **USE GREP/RG** when:
- You need exact string matches
- Working with regex patterns
- No setup time available
- Searching non-code files

---

## Resources

### Official Documentation

- **OSGrep GitHub**: Check `npm info osgrep` for repository link
- **CLI Help**: `osgrep --help`
- **Diagnostics**: `osgrep doctor`

### Related Cluster-Code Skills

- **cluster-dev-guidelines.md**: TypeScript development patterns
- **skill-developer.md**: Creating new skills

### Integration Points

OSGrep works seamlessly with:
- Claude Code's exploration workflows
- Traditional grep/rg for hybrid searches
- Your editor's "open file" capabilities
- CI/CD pipelines (direct mode without daemon)

---

## Quick Reference

```bash
# Essential Commands
osgrep "natural language query"              # Basic search
osgrep --json "query"                        # JSON output
osgrep --sync "query"                        # Sync before search
osgrep "query" --per-file 3                  # More results per file
osgrep "query" --compact                     # File paths only

# Index Management
osgrep index                                 # Full re-index
osgrep list                                  # Show indexed repos
osgrep doctor                                # Verify setup

# Daemon
osgrep serve                                 # Start daemon (port 4444)
osgrep serve --port 5000                     # Custom port

# Cleanup
rm -rf ~/.osgrep/data/<store>                # Remove index
```

---

**Last Updated**: 2025-11-25
**Skill Version**: 1.0.0
**Compatible with**: cluster-code v0.x - v2.x
